import asyncio
import bridge
import SIPx
HB = "A"

try:
  PlayStation = bridge.startup()
  socket_PS = bridge.get_socket(port=33740)
except KeyboardInterrupt:
  bridge.shutdown()

async def main():
  
  while True:
    for PS_name, ip in PlayStation:
      x = SIPx.heartbeat(HB, PlayStation, socket_PS)
      SIP_size = await x
      x = SIPx.get_telemetry(socket_PS, SIP_size)
      SIP_raw = await x
      print(SIP_raw)

try:
  asyncio.run(main())
except KeyboardInterrupt:
  bridge.shutdown()
