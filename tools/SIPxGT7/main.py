import asyncio
import bridge
import SIPx
import status
HB = 'A'
HB_port = 33739
PS_port = 33740
PS_list = bridge.get_PlayStation()
PS_socket = bridge.get_socket(PS_port)
SIP_size = SIPx.SIP_size(HB)
async def main():
  while True:
    for PS_name, ip in PS_list:
      await SIPx.HB_send(HB, HB_port, PS_list, PS_socket)
      x = SIPx.SIP_get_raw(PS_socket, SIP_size)
      y = await x
      if not y: status.IDLE(); continue
      PS_addr, SIP_raw = y
      if SIP_raw:
        status.SIPr(PS_addr, SIP_raw)
try:
  asyncio.run(main())
except KeyboardInterrupt:
  bridge.shutdown()
