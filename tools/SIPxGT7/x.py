from notify import notify
import sys
from config import PlayStations

def get_PlayStation():
  PS = check_config()
  is_validated(PS)
  PS_search()
  return PS

def check_config():
  x = [ (PS_name, ip) for PS_name, ip in PlayStations ]
  if not x:
    notify.FAIL(msg="check config.py")
    sys.exit(1)
  PS_name, ip = x[0]
  #for PS_name, ip in x:notify.PASS(msg=f"{PS_name} {ip}")
  return x

def get_socket(SIP_port):
  import socket
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('0.0.0.0', SIP_port))
  s.settimeout(.1)
  return s

def is_validated(PS_list):
  for PS_name, ip in PS_list:
    if not is_ip(ip):
      notify.FAIL(msg=f"check config.py {PS_name} {ip}")
      sys.exit(1)
    #notify.PASS(msg=f"{PS_name} {ip}")

def is_ip(ip):
  octet = ip.split('.')
  return \
  len(octet) == 4 \
  and all(x.isdigit() \
  and 0 <= int(x) <= 255 for x in octet)
def PS_search():
  import socket
  x = []
  for port, ver in [(987, "00020020"), (9302, "00030010")]:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(1)
    SRCH = (f"SRCH * HTTP/1.1\ndevice-discovery-protocol-version:{ver}\n").encode()
    try:
      s.sendto(SRCH, ('255.255.255.255', port))
      while True:
        data, addr = s.recvfrom(512)
        body = data.decode(errors='replace')
        #notify.INFO(f"\n{body}")
        x.append(addr[0])
    except socket.timeout: pass
    finally: s.close()
  if x: notify.INFO(f"PlayStation(s) {x}")
  else: notify.INFO("no PlayStation")

  in_config = {ip for _, ip in PlayStations}
  discovered = set(x)
  extra = discovered - set(in_config)
  dead = set(in_config) - discovered

  if discovered & in_config:
    notify.PASS(f"{discovered}")
  else: notify.FAIL(f"check config.py {in_config}")

  if dead: notify.FAIL(f"check PlayStation: {dead}")


def shutdown():
  print("\n")
  notify.STOP()
  sys.exit()

