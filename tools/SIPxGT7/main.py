import asyncio
import x
import SIPx
from notify import status
HB = 'A'
HB_port = 33739
PS_port = 33740
PS_list = x.get_PlayStation()
PS_socket = x.get_socket(PS_port)
SIP_size = SIPx.SIP_size(HB)
async def main():
  while True:
    for PS_name, ip in PS_list:
      await SIPx.HB_send(HB, HB_port, PS_list, PS_socket)
      await SIPx.SIP_get_raw(PS_socket, SIP_size)
try:
  asyncio.run(main())
except KeyboardInterrupt:
  x.shutdown()
