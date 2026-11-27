
import sys
import logging

logger = logging.getLogger('status')
logger.setLevel(logging.INFO)
_handler = logging.FileHandler('tmp', mode='w')
logger.addHandler(_handler)
logger.propagate = False
def blank_tmp(): open('tmp', 'w').close()

def IDLE():
  with open('tmp') as f:
    x = f.read().strip()
  print(f"\r{x}", end="", flush=True)
  blank_tmp()

def SIPr(PS_addr, SIP_raw):
  xf = f'SIP_raw-{PS_addr}'
  print(
  f"\r\033[2K"
  f"[ {funcname(depth=1)} ]", end="", flush=True)
  with open(xf, 'wb') as f:
    f.write(SIP_raw)
  with open(xf, 'rb') as f:
    x = f.read()
  x = x[:1].hex()
  sys.stdout.buffer.write(b"\r\033[10G" + x.encode())
  sys.stdout.buffer.flush()
  print(f"\r\033[13G{xf}", end="", flush=True)
def msg_body(msg,whoami=True):
  if whoami == True:
    logger.info("[ %s ] %s %s %s [%s]",
    funcname(depth=2),
    modulename(depth=3),
    funcname(depth=4),
    funcname(depth=3),
    msg or "no message",
    )
  if whoami == False:
    logger.info("[ %s ] [%s]",
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
0000
0001
0002
0003
bash
busy
call
dead
done
down
drop
echo
end
fail
fine
fire
go
hint
idle
info
live
lock
miss
name
note
off
on
pass
ping
play
poll
recv
ride
run
send
skip
spam
stop
sync
test
user
wait
warn
"""
