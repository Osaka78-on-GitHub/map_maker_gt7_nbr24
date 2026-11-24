import notify
import sys
from config import PlayStations

def startup():
  PS = get_addr()
  is_valid(PS)
  return PS

def get_addr():
  x = [ (PS_name, ip) for PS_name, ip in PlayStations ]
  if not x:
    notify.FAIL(msg="check config.py")
    sys.exit(1)
  PS_name, ip = x[0]
  for PS_name, ip in x:
    notify.PASS(msg=f"{PS_name} {ip}")
  return x

def get_socket(SIP_port):
  import socket
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('0.0.0.0', SIP_port))
  s.settimeout(1)
  return s

def is_valid(PS_list):
  for PS_name, ip in PS_list:
    if not is_ip(ip):
      notify.FAIL(msg=f"{PS_name} {ip}")
      sys.exit(1)
    notify.PASS(msg=f"{PS_name} {ip}")

def is_ip(ip):
  octet = ip.split('.')
  return \
  len(octet) == 4 \
  and all(o.isdigit() \
  and 0 <= int(o) <= 255 for o in octet)

def shutdown():
  print("\n")
  notify.STOP()
  sys.exit()

