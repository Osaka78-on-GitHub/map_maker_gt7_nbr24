import socket, asyncio, websockets, struct, json

# GT7 telemetry: Salsa20 encrypted, port 33740
# Use an existing parser like gt7-datalogger or gt7dashboard
# This is the skeleton:

async def handle_client(ws):
    try:
        async for msg in ws:
            pass
    except:
        pass

async def udp_to_ws():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 33740))

    # Send heartbeat to PS5 to start telemetry
    # (IP of your PS5, port 33739)
    # heartbeat = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    # sock.sendto(heartbeat, ('PS5_IP', 33739))

    async with websockets.serve(handle_client, '0.0.0.0', 8765):
        loop = asyncio.get_event_loop()
        while True:
            data, addr = await loop.run_in_executor(None, sock.recvfrom, 65536)
            # Parse here — for now just send raw length as test
            # Real: parse Salsa20, extract x, y, speed, etc.
            msg = json.dumps({"x": 0, "y": 0, "speed": 0})
            await websockets.broadcast("race", msg)

asyncio.run(udp_to_ws())   
