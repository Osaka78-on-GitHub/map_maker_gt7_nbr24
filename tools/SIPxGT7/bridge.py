import socket
import notify
import subprocess
import sys
from config import PlayStation
def startup():
  PlayStation = get_ip()
  is_valid(PlayStation)
  ping(PlayStation)
  return PlayStation

def get_ip():
  x = [ (PS_name, ip) for PS_name, ip in PlayStation ]
  
  if not x:
    notify.FAIL(msg="check config.py")
    sys.exit(1)
  PS_name, ip = x[0]
  for PS_name, ip in x:
    notify.PASS(msg=f"{PS_name} {ip}")
  return x

def get_socket(SIP_port):
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

def ping(PS_list):
  for PS_name, ip in PS_list:
    x = subprocess.run(
    ["ping", "-c", "1", "-W", "1", ip],
    capture_output=True)
    
    if result.returncode != 0:
      notify.FAIL(msg=f"{PS_name} {ip}")
      sys.exit(1)
      
    notify.PASS(msg=f"{PS_name} {ip}")

def shutdown():
  notify.STOP()
  sys.exit()


