# ABBREVIATIIONS
# sip		Simulator Interface Packet GT7 ver 0.0

# TRAPS
async def exit_async(sock=None):
	if sock:
		sock.close()
	exit(1)

import asyncio
import json
import os
from Crypto.Cipher import Salsa20
import socket
import struct
import subprocess
import sys
import time
import tomllib

# NOTIFICATIONS
def notify_fail(msg):
	print(f"[fail] {msg}")
	notify_stop()

def notify_info(msg):
	print(f"[info] {msg}")

def notify_pass(msg):
	print(f"[pass] {msg}")

def notify_stop(msg=None):
	if msg:
		print(f"\n[stop] {msg}")
	else:
		print(f"\n[stop]")

def notify_test(msg):
	print(f"[test] {msg}")

def config_open():
	config_file = os.path.join(
	os.path.dirname(
	os.path.abspath(__file__)), 
	"config.toml")
	
	with open(config_file, "rb") as f:
		config = tomllib.load(f)
	
	return config

def host_ping(host):
	for name, ip in host:
		result = subprocess.run(
		["ping", "-c", "1", "-W", "1", ip],
		capture_output=True)
		
		if result.returncode != 0:
			notify_fail(f"[host_ping] {name} {ip}")
			exit(1)

def host_valid(host):
	ip_fail = []
	
	for name, ip in host:
		if not ip_valid(ip):
			ip_fail.append((name,ip))
	
	if ip_fail:
		msg = "\n".join(
			f"[host_valid] "
			f"{name} {ip} check config.toml"
			for name, ip in ip_fail)
		notify_fail(msg)
		exit(1)

def ip_valid(ip):
	octet = ip.split('.')
	return \
	len(octet) == 4 \
	and all(o.isdigit() \
	and 0 <= int(o) <= 255 for o in octet)

def playstation_ip():
	config = config_open()
	playstation_ip = []
	for name, entry in config.get(
	"playstation", {}).items():
		if entry.get("ip"):
			playstation_ip.append((name, entry["ip"]))
	
	if not playstation_ip:
		msg = (
		f"[playstation_ip] check config.toml")
		notify_fail(msg)
		exit(1)
		
	return playstation_ip

def print_telem(x,y):
	sys.stdout.write(
	f"\r[info] x: {x:.20f} y: {y:.20f}")
	sys.stdout.flush()
	
def sip_decryt(sip_input):
	if len(sip_input) not in (296, 316, 344):
		return None
	
	iv1 = int.from_bytes(sip_input[0x40:0x44], 'little')
	
	mask = 0xDEADBEAF	if len(sip_input) == 296 \
	else (0xDEADBEEF if len(sip_input) == 316 \
	else 0x55FABB4F)
	
	iv2 = iv1 ^ mask
	
	nonce = iv2.to_bytes\
	(4,'little') + iv1.to_bytes(4,'little')
	
	sip_output = Salsa20.new(
	key,nonce).decrypt(sip_input)
	
	if int.from_bytes\
	(sip_output[0:4], 'little') != 0x47375330:
		return None
	
	return sip_output

async def sip_none(sip_timeout,sock):
	sip_timeout += 1
	if sip_timeout == 180:
		notify_info("no telemetry for 3 mins")
	if sip_timeout == 300:
		notify_info("no telemetry for 5 mins")
	if sip_timeout == 480:
		notify_stop("no telemetry for 8 mins")
		await exit_async(sock)
	return sip_timeout

# VARIABLES SEQ FREE

# sip
key = b"Simulator Interface Packet GT7 ver 0.0"[:32]

# playstation
playstation = playstation_ip()

# EXPRESSIONS SEQUENTIAL
host_valid(playstation)
host_ping(playstation)

# --- Main loop ---
async def main():
	sip_timeout = 0
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(('0.0.0.0', 33740))
	sock.settimeout(1)
	for name, ip in playstation:
		sock.sendto(b'A', (ip, 33739))

	loop = asyncio.get_event_loop()
	notify_info(
	f"listening for telemetry from {playstation}")
	notify_info("waiting for first telemetry packet")
	try:
		sip_input, addr = await loop.run_in_executor(None, sock.recvfrom, 65536)
		sip_output = sip_decryt(sip_input)
		
		msg = (f"{len(sip_input)} bytes from {addr[0]}")
		notify_pass(msg)
	except TimeoutError:
		msg = ("no telemetry, check GT7 and config.toml")
		notify_info(msg)

	while True:
		for name, ip in playstation:
			try:
				sock.sendto(b'A', (ip, 33739))
			except:
				pass
		try:
			sip_input, addr = await loop.run_in_executor(
			None, sock.recvfrom, 65536)
			sip_output = sip_decryt(sip_input)

			if sip_output:
				sip_timeout = 0
				x, y = struct.unpack_from('ff', sip_output, 0x04)
				console = "unknown"
				for name, ip in playstation:
					if addr[0] == ip:
						console = name
				msg = json.dumps({"console": console, "x": x, "y": y})
				output_json = open("xy.jsonl", "w")
				output_json.write(msg + "\n")
				output_json.flush()
				print_telem(x,y)
		except TimeoutError:
			sip_timeout = await sip_none(
			sip_timeout,sock)   
try:
	asyncio.run(main())
except KeyboardInterrupt:
	notify_stop()
