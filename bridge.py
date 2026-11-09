# LOGICAL FLOW
# DECLARATION SECTION
# traps
# dependencies
# functions
# variables

# EXECUTABLE SECTION
# sequential flow top down

# ABBREVIATIIONS
# sip 	Simulator Interface Packet GT7 ver 0.0

# DEPENDENCIES

def check_dependency():
	dependency = [
	"tomli",
	"websockets",
	"salsa20",
	]
	
	check_fail = []
	for module in dependency:
		try:
			__import__(module)
		except ImportError:
			check_fail.append(module)
	
	if check_fail:
		missing_dependency = " ".join(check_fail)
		print(f"[check_dependency]")
		print(f"pip install {missing_dependency}")
		exit(1)

def check_version():
	dependency = {
	"websockets": 10,
	}
	
	check_fail = []
	for module, version_min in dependency.items():
		evaluate = __import__(module)
		x = int(evaluate.__version__.split('.')[0])
		if x < version_min:
			check_fail.append((
			module,
			version_min,
			evaluate.__version__))
	
	if check_fail:
		print(f"[check_version]")
		for module, version_min, version_sys \
		in check_fail:
			print(f"{module} {version_min}+ required")
			print(f"{version_sys} on system")
		
		minimum_requirement = \
		" ".join(module for module, *x in check_fail)
		print(f"To upgrade run:")
		print(
		f"pip install "
		f"--user --upgrade "
		f"{minimum_requirement}")   
		exit(1)

check_dependency()
check_version()

# IMPORTS

import asyncio
import json
import os
from salsa20 import Salsa20_xor
import socket
import struct
import subprocess
import time
import tomli
import websockets

# FUNCTIONS

async def cloudflared_worker():
	return await websockets.connect(
	"wss://sipworker.osaka78.workers.dev")

def config_open():
	config_file = os.path.join(
	os.path.dirname(
	os.path.abspath(__file__)), 
	"config.toml")
	
	with open(config_file, "rb") as f:
		config = tomli.load(f)

def host_ping(host):
	for name, ip in host.items():
		result = subprocess.run(
		["ping", "-c", "1", "-W", "1", ip],
		capture_output=True)
		
		if result.returncode != 0:
			print(
			f"[host_ping]"
			f"{name} at {ip} is not responding to ping")

def host_valid(host):
	ip_fail = []
	
	for name, ip in host.items():
		if not ip_valid(ip):
			ip_fail.append(name)
	
	if ip_fail:
		for name in ip_fail:
			print(
			f"[ip_fail]"
			f"{name}: {host[name]}")
		exit(1)

def ip_valid(ip):
	octet = ip.split('.')
	return \
	len(octet) == 4 \
	and all(o.isdigit() \
	and 0 <= int(o) <= 255 for o in octet)

def playstation_ip():
	config = config_open()
	playstation_ip = {}
	for name, entry in config.get(
	"playstation", {}).items():
		if entry.get("ip"):
			playstation_ip[name] = entry["ip"]
	
	if not playstation_ip:
		print(
		f"[playstation_ip]"
		f"PlayStation IP not at config.toml")
		exit(1)
	
	return playstation_ip

def sip_decryt(sip_input):
	if len(sip_input) not in (296, 316, 344):
		return None
	
	iv1 = int.from_bytes(sip_input[0x40:0x44], 'little')
	
	mask = 0xDEADBEAF	if len(sip_input) == 296 \
	else (0xDEADBEEF if len(sip_input) == 316 \
	else 0x55FABB4F)
	
	iv2 = iv1 ^ mask
	
	nonce = iv2.to_bytes\
	(4, 'little') + iv1.to_bytes(4, 'little')
	
	sip_output = Salsa20_xor(sip_input, nonce, key)
	
	if int.from_bytes\
	(sip_output[0:4], 'little') != 0x47375330:
		return None
	
	return sip_output

# VARIABLES SEQ FREE

# sip
key = b"Simulator Interface Packet GT7 ver 0.0"[:32]

# playstation
playstation = playstation_ip()

# gran turismo
room_id = None

# EXPRESSIONS SEQUENTIAL
host_valid(playstation)
host_ping(playstation)

# --- Main loop ---
async def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(('0.0.0.0', 33740))
	sock.settimeout(1)
	for name, ip in playstation.items():
		sock.sendto(b'A', (ip, 33739))

	loop = asyncio.get_event_loop()

	ws = await cloudflared_worker()
	print(f"Connected to worker")
	print(f"Listening for telemetry from: {playstation}")
	print("(Ctrl+C to stop)")

	# Test: wait for first packet
	print("Waiting for first packet...")
	try:
		sip_input, addr = await loop.run_in_executor(None, sock.recvfrom, 65536)
		sip_output = sip_decryt(sip_input)
		if not sip_output:
			print("Error: packet received but decryption failed.")
			exit(1)
		print(f"OK: {len(sip_input)} bytes from {addr[0]}")
	except socket.timeout:
		print("Error: no telemetry received. Is GT7 running and IP correct?")
		exit(1)

	while True:
		for name, ip in playstation.items():
			try:
				sock.sendto(b'A', (ip, 33739))
			except:
				pass
		try:
			sip_input, addr = await loop.run_in_executor(None, sock.recvfrom, 65536)
			sip_output = sip_decryt(sip_input)
			if sip_output:
				x, y, z = struct.unpack_from('fff', sip_output, 0x04)
				speed = struct.unpack_from('f', sip_output, 0x4C)[0]
				console = "unknown"
				for name, ip in playstation.items():
					if addr[0] == ip:
						console = name
				msg = json.dumps({"console": console, "x": x, "y": y, "z": z, "speed": speed})
				await ws.send(msg)
		except socket.timeout:
			pass

try:
	asyncio.run(main())
except KeyboardInterrupt:
	print("\nStopped.")   
