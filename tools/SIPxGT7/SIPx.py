import asyncio
import status
async def SIP_decryt(SIP_raw):
  '''Decrypt SIP with Salsa20.'''
  from Crypto.Cipher import Salsa20
  key = b"Simulator Interface Packet GT7 ver 0.0"[:32]
  if len(SIP_raw) not in (296, 316, 344, 368):
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
async def SIP_get_raw(PS_socket, SIP_size):
  '''Get SIP in raw "binary over UDP" format.'''
  loop = asyncio.get_event_loop()
  try:
    x = loop.run_in_executor(
    None, PS_socket.recvfrom, SIP_size)
    SIP_raw, PS_addr = await x
    return SIP_raw
  except TimeoutError:
    status.INFO("[check GT7]")
    pass
def SIP_size(HB):
  '''SIP size in bytes.'''
  if HB == 'A': x = 296
  if HB == 'B': x = 316
  if HB == 'T': x = 344
  if HB == 'C': x = 368
  return x
async def HB_send(HB, HB_port, PS_list, PS_socket):
  '''Send heartbeat to GT7.'''
  loop = asyncio.get_event_loop()
  for PS_name, ip in PS_list:
    try:
      PS_socket.sendto(HB.encode('utf-8'), (ip, HB_port))
    except:
      pass






