import asyncio
import bridge
import SIPx
import status
HB = 'A'
HB_port = 33739
PS_port = 33740
PS_list = bridge.startup()
PS_socket = bridge.get_socket(PS_port)
SIP_size = SIPx.SIP_size(HB)
async def main():
  while True:
    for PS_name, ip in PS_list:
      await SIPx.HB_send(HB, HB_port, PS_list, PS_socket)
      x = SIPx.SIP_get_raw(PS_socket, SIP_size)
      SIP_raw = await x
      if SIP_raw:
        status.GOOD(SIP_raw)
      if not SIP_raw:
        status.IDLE()
try:
  asyncio.run(main())
except KeyboardInterrupt:
  bridge.shutdown()
