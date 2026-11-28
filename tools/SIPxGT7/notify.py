import sys
import logging
def funcname(depth=1):
  return sys._getframe(depth).f_code.co_name
def modulename(depth=1):
  return sys._getframe(depth).f_globals['__name__']
def msg_body(_x, msg):
  _x.info("[ %s ] %s %s %s [%s]",
  funcname(depth=3),
  modulename(depth=4),
  funcname(depth=5),
  funcname(depth=4),
  msg or "no message",
  )
def _do(_x, msg): msg_body(_x.LOG, msg); _x.action(msg)
class scenario:
  def __init__(_x, name, handler):
    _x.LOG = logging.getLogger(name)
    _x.LOG.setLevel(logging.INFO)
    _x.LOG.addHandler(handler)
    _x.LOG.propagate = False
  def action(_x, msg): pass
  def FAIL(_x, msg=None): _do(_x, msg)
  def INFO(_x, msg=None): _do(_x, msg)
  def PASS(_x, msg=None): _do(_x, msg)
  def STOP(_x, msg=None): _do(_x, msg)
  def IDLE(_x, msg=None): _do(_x, msg)
class _n(scenario): pass
notify = _n("notify", logging.StreamHandler())
class _s(scenario):
  def action(_x, msg):
    _x.LOG.handlers[0].flush()
    with open('tmp') as f:
      x = f.read().strip()
    print(f"\r\033[2K{x}", end="", flush=True)
    open('tmp', 'w').close()
  def SIPr(_x, PS_addr, SIP_raw):
    xf = f'SIP_raw-{PS_addr}'
    print(f"\r\033[2K[ {funcname(depth=1)} ]", end="", flush=True)
    with open(xf, 'wb') as f:
      f.write(SIP_raw)
    with open(xf, 'rb') as f:
      x = f.read()
    x = x[:1].hex()
    sys.stdout.buffer.write(b"\r\033[10G" + x.encode())
    sys.stdout.buffer.flush()
    print(f"\r\033[13G{xf}", end="", flush=True)
status = _s("status", logging.FileHandler('tmp'))
