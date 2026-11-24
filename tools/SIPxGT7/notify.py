
import sys
import logging

logger = logging.getLogger("notify")
logger.setLevel(logging.INFO)
_handler = logging.StreamHandler()
logger.addHandler(_handler)
logger.propagate = False


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
