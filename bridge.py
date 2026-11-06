import asyncio
import glob
import http.server
import json
import os
import shutil
import socket
import struct
import subprocess
import threading
import webbrowser

def check_deps():
	deps = {
	"tomli": "tomli",
	"websockets": "websockets",
	"salsa20": "salsa20",
	}
	missing = []
	for mod, pip_name in deps.items():
		try:
			__import__(mod)
		except ImportError:
			missing.append(pip_name)
	if missing:
		print(f"Missing: pip install {' '.join(missing)}")
		exit(1)

	import websockets
	v = tuple(int(x) for x in websockets.__version__.split('.')[:2])
	if v < (10, 0):
		print(f"websockets >= 10 required (you have {websockets.__version__}). To upgrade run: pip install --user --upgrade websockets")   
		exit(1)

check_deps()

import tomli
import websockets
from salsa20 import Salsa20_xor

# --- Config ---
config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.toml")
with open(config_file, "rb") as f:
	config = tomli.load(f)
PLAYSTATION = {}
for name, c in config.get("playstation", {}).items():
	if c.get("ip"):
		PLAYSTATION[name] = c["ip"]

if not PLAYSTATION:
	print("No PlayStation IP address found in config.toml")
	exit(1)

def valid_ip(ip):
	parts = ip.split('.')
	return len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)

bad = [name for name, ip in PLAYSTATION.items() if not valid_ip(ip)]
if bad:
	for name in bad:
		print(f"Invalid IP for {name}: {PLAYSTATION[name]}")
	exit(1)

# Ping check
for name, ip in PLAYSTATION.items():
	result = subprocess.run(["ping", "-c", "1", "-W", "1", ip], capture_output=True)
	if result.returncode != 0:
		print(f"WARNING: {name} at {ip} is not responding to ping")

# --- GT7 decryption ---
KEY = b"Simulator Interface Packet GT7 ver 0.0"[:32]

def decrypt(data):
	if len(data) not in (296, 316, 344):
		return None
	iv1 = int.from_bytes(data[0x40:0x44], 'little')
	mask = 0xDEADBEAF if len(data) == 296 else (0xDEADBEEF if len(data) == 316 else 0x55FABB4F)
	iv2 = iv1 ^ mask
	nonce = iv2.to_bytes(4, 'little') + iv1.to_bytes(4, 'little')
	plain = Salsa20_xor(data, nonce, KEY)
	if int.from_bytes(plain[0:4], 'little') != 0x47375330:
		return None
	return plain

# --- Websocket ---
connected = set()

async def ws_handler(ws):
	connected.add(ws)
	try:
		async for msg in ws:
			for c in connected:
				if c is not ws:
					await c.send(msg)
	except:
		pass
	finally:
		connected.discard(ws)
		
# --- Room ID ---
room_id = ""
answer = input("Map for Room ID? [y/n]: ").strip().lower()
if answer == "y":
	room_id = input("Room ID: ").strip()

# --- create url ---

cf_path = None
for f in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cloudflared*")):
	if os.access(f, os.X_OK):
		cf_path = f
		break

if not cf_path:
	cf_path = shutil.which("cloudflared")
	
cf_proc = None

def start_relay(cf_path):
	global cf_proc
	cf_proc = subprocess.Popen(
		[cf_path, "tunnel", "--url", "http://localhost:8765"],
		stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
	)
	for line in cf_proc.stdout:
		if "trycloudflare.com" in line and "https://" in line:
			return "wss://" + line.split("https://")[1].strip()
	cf_proc.kill()
	return None

if room_id:
	if cf_path:
		relay_url = start_relay(cf_path)
	else:
		relay_url = None
	if relay_url:
		url = f"https://osaka78-on-github.github.io/map_maker_gt7_nbr24/?room_id={room_id}&relay={relay_url}"
	else:
		print("Error: cloudflared not found or failed to start.")
		if input("Run localhost? [y/n]: ").strip().lower() != "y":
			exit(1)
		url = "http://localhost:8080/index.html"

else:
	url = "http://localhost:8080/index.html"   


	
# --- HTTP server (serves index.html) ---
if not room_id:
	def serve_http():
		handler = http.server.SimpleHTTPRequestHandler
		httpd = http.server.HTTPServer(('127.0.0.1', 8080), handler)
		httpd.serve_forever()

	http_thread = threading.Thread(target=serve_http, daemon=True)
	http_thread.start()
	
# --- Main loop ---
async def main():
	hb = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	hb.settimeout(1)

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(('0.0.0.0', 33740))
	sock.settimeout(1)

	loop = asyncio.get_event_loop()

	async with websockets.serve(ws_handler, '0.0.0.0', 8765):
		print(f"Listening for telemetry from: {PLAYSTATION}")
		print(f"Map: {url}")
		print("(Ctrl+C to stop)")

		webbrowser.open(url)

		# Test: wait for first packet
		print("Waiting for first packet...")
		try:
			data, addr = await loop.run_in_executor(None, sock.recvfrom, 65536)
			plain = decrypt(data)
			if not plain:
				print("Error: packet received but decryption failed.")
				exit(1)
			print(f"OK: {len(data)} bytes from {addr[0]}")
		except socket.timeout:
			print("Error: no telemetry received. Is GT7 running and IP correct?")
			exit(1)

		while True:
			for name, ip in PLAYSTATION.items():
				try:
					hb.sendto(b'B', (ip, 33739))
				except:
					pass
			try:
				data, addr = await loop.run_in_executor(None, sock.recvfrom, 65536)
				plain = decrypt(data)
				if plain:
					x, y, z = struct.unpack_from('fff', plain, 0x04)
					speed = struct.unpack_from('f', plain, 0x4C)[0]
					console = "unknown"
					for name, ip in PLAYSTATION.items():
						if addr[0] == ip:
							console = name
					msg = json.dumps({"console": console, "x": x, "y": y, "z": z, "speed": speed})
					if connected:
						await asyncio.wait_for(
							asyncio.gather(*[v.send(msg) for v in connected], return_exceptions=True),
							timeout=0.1
						)
			except socket.timeout:
				pass
			except asyncio.TimeoutError:
				pass
try:
	asyncio.run(main())
except KeyboardInterrupt:
	if cf_proc:
		cf_proc.kill()
	print("\nStopped.")
