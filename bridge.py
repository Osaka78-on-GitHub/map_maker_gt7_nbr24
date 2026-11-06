import socket
import struct
import asyncio
import json
import subprocess
import websockets
from salsa20 import Salsa20_xor

# --- Config ---
config = json.load(open("config.json"))
CONSOLES = {}
if config.get("ps5_ip"):
    CONSOLES["ps5"] = config["ps5_ip"]
if config.get("ps4_ip"):
    CONSOLES["ps4"] = config["ps4_ip"]

if not CONSOLES:
    print("No console IP found in config.json")
    exit(1)

def valid_ip(ip):
    parts = ip.split('.')
    return len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)

bad = [name for name, ip in CONSOLES.items() if not valid_ip(ip)]
if bad:
    for name in bad:
        print(f"Invalid IP for {name}: {CONSOLES[name]}")
    exit(1)

# Ping check (warning only, doesn't stop)
for name, ip in CONSOLES.items():
    result = subprocess.run(["ping", "-c", "1", "-W", "1", ip], capture_output=True)
    if result.returncode != 0:
        print(f"WARNING: {name} at {ip} is not responding to ping")

print(f"Listening for telemetry from: {CONSOLES}")
print(f"WebSocket on port 8765")
print("Waiting for packets... (Ctrl+C to stop)")

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

# --- WebSocket ---
clients = set()

async def ws_handler(ws):
    clients.add(ws)
    try:
        async for _ in ws:
            pass
    finally:
        clients.discard(ws)   
