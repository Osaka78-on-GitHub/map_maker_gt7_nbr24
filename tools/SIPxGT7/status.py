
import sys
import logging

logger = logging.getLogger('status')
logger.setLevel(logging.INFO)
_handler = logging.FileHandler('tmp', mode='w')
logger.addHandler(_handler)
logger.propagate = False
def blank():
  open('tmp', 'w').close()

def IDLE():
  with open('tmp') as f:
    x = f.read().strip()
  print(f"\r{x}", end="", flush=True)
  blank()
def raw(SIP_raw):
  print(
  f"\r\033[10GSIP_raw", end="", flush=True)
  with open('SIP_raw', 'wb') as f:
    f.write(SIP_raw)
  with open('SIP_raw', 'rb') as f:
    x = f.read()
  x = x[:3].hex()
  sys.stdout.buffer.write(b"\r\033[18G" + x.encode())
  sys.stdout.buffer.flush()
def GOOD(SIP_raw):
  print(
  f"\r\033[2K"
  f"[ {funcname(depth=1)} ]", end="", flush=True)
  raw(SIP_raw)
def msg_body(msg,whoami=True):
  if whoami == True:
    logger.info("[ %s ] %s %s %s %s",
    funcname(depth=2),
    modulename(depth=3),
    funcname(depth=4),
    funcname(depth=3),
    msg or "no message",
    )
  if whoami == False:
    logger.info("[%s] %s",
    funcname(depth=2),
    msg or "",
    )
def funcname(depth=1):
  return sys._getframe(depth).f_code.co_name
def modulename(depth=1):
  return sys._getframe(depth).f_globals['__name__']
def FAIL(msg=None): msg_body(msg)
def INFO(msg=None): msg_body(msg)
def PASS(msg=None): msg_body(msg)
def STOP(msg=None): msg_body(msg)
def TEST(msg=None): msg_body(msg)
def DBUG(msg=None): msg_body(msg)
"""
Footnotes:
WIP:
call
spam
drop
bash
busy
dead
done
down
echo
end
fail
fine
fire
go
on
off
ride
0003
0002
0001
0000
hint
idle
info
live
lock
miss
name
note
pass
ping
poll
recv
run
send
skip
stop
sync
test
user
wait
warn
"""
