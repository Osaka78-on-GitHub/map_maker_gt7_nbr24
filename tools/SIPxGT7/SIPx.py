import asyncio
import notify
from Crypto.Cipher import Salsa20

async def decryt(SIP_raw):
  key = b"Simulator Interface Packet GT7 ver 0.0"[:32]
  if len(SIP_raw) not in (296, 316, 344):
    return None
  iv1 = int.from_bytes(SIP_raw[0x40:0x44], "little")
  if len(SIP_raw) == 296: mask = 0xDEADBEAF
  if len(SIP_raw) == 316: mask = 0xDEADBEEF
  if len(SIP_raw) == 344: mask = 0x55FABB4F
  iv2 = iv1 ^ mask
  nonce = iv2.to_bytes(4,"little")
  nonce += iv1.to_bytes(4,"little")
  SIP_plaintext = Salsa20.new(key,nonce).decrypt(SIP_raw)
  x = int.from_bytes(SIP_plaintext[0:4], "little")
  if x != 0x47375330:
    return None
  return SIP_plaintext

async def get_telemetry(PS_socket, SIP_size):
  loop = asyncio.get_event_loop()
  try:
    x = loop.run_in_executor(
    None, PS_socket.recvfrom, SIP_size)
    SIP_raw, PS_addr = await x
    return SIP_raw
  except TimeoutError:
    pass

async def heartbeat(HB, PlayStation, PS_socket):
  loop = asyncio.get_event_loop()
  if HB == 'A': b = 296
  if HB == 'B': b = 316
  if HB == 'T': b = 344
  if HB == 'C': b = 368
  HB_port = 33739
  for PS_name, ip in PlayStation:
    try:
      PS_socket.sendto(HB.encode('utf-8'), (ip, HB_port))
    except:
      pass
  return b









