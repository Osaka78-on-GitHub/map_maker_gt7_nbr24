import socket
import struct
import asyncio
import json
import os
import subprocess
import webbrowser
import http.server
import threading

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

# --- WebSocket (host: accepts players + viewers) ---
viewers = set()
players = set()

async def ws_handler(ws):
	# First message from a player is {"type": "player", "name": "ps5"}
	# Viewers just connect and wait
	is_player = False
	try:
		first = await asyncio.wait_for(ws.recv(), timeout=2)
		data = json.loads(first)
		if data.get("type") == "player":
			is_player = True
			players.add(ws)
			print(f"Player connected: {data.get('name')}")
	except (asyncio.TimeoutError, json.JSONDecodeError):
		pass

	if not is_player:
		viewers.add(ws)

	try:
		async for msg in ws:
			if is_player:
				# Player is pushing telemetry, broadcast to viewers
				if viewers:
					await asyncio.wait_for(
						asyncio.gather(*[v.send(msg) for v in viewers], return_exceptions=True),
						timeout=0.1
					)
	except:
		pass
	finally:
		viewers.discard(ws)
		players.discard(ws)

# --- HTTP server (serves index.html) ---
def serve_http():
	handler = http.server.SimpleHTTPRequestHandler
	httpd = http.server.HTTPServer(('127.0.0.1', 8080), handler)
	httpd.serve_forever()

http_thread = threading.Thread(target=serve_http, daemon=True)
htt   
