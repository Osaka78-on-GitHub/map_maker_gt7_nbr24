# WIP milestone

## get SIP raw is done

archive #folder dump for WIP milestones

async def decryt(SIP_raw):

async def get_telemetry(PS_socket, SIP_size):

async def heartbeat(HB, PlayStation, PS_socket):

b #bytes

bridge.py #working title

config.py #user configuration, blank for github

def FAIL(msg=None): msg_body(msg)

def funcname(depth=1):

def get_ip():

def get_socket(SIP_port):

def INFO(msg=None): msg_body(msg)

def is_ip(ip):

def is_valid(PS_list):

def modulename(depth=1):

def msg_body(msg,whoami=True):

def PASS(msg=None): msg_body(msg)

def ping(PS_list):

def shutdown():

def startup():

def STOP(msg=None): msg_body(msg)

def TEST(msg=None): msg_body(msg)

depth=1 #notify gets modulename funcname etc

from config import PlayStation

from Crypto.Cipher import Salsa20

_handler = logging.StreamHandler() #notify msg printing

HB_A = 'A'

HB_B = 'B'

HB_C = 'C'

HB = '' #heartbeat

HB_port = 33739

HB_T = '~'

import asyncio

import bridge

import logging

import notify

import SIPx

import socket

import subprocess

import sys

ip #PlayStation ip address

key = b"Simulator Interface Packet GT7 ver 0.0"[:32]

logger = logging.getLogger("notify")

loop = asyncio.get_event_loop()

main.py

msg #generic name for message

names #file

notify.py

octet = ip.split('.') #math term used in bridge.is_ip

PS_addr #return address (source_ip, source_port).

PS_list #list from config.py, presumably PlayStation(s)

PS_name, ip in PlayStation

PS_name, ip in PS_list:

PS_socket #socket for PlayStation(s)

__pycache__ #folder python creates

rename #file

SIP_G7S0 = 0x47375330

SIP_mask_A = 0xDEADBEAF

SIP_mask_B = 0xDEADBEEF

SIP_mask_C = 0x55FABB4F

SIP_mask_T = 0x55FABB4F

SIP_plaintext #plaintext decrypted PIP

SIP_port #where SIP is received

SIP_raw #raw encrypted SIP

SIP_size_A = 296

SIP_size_B = 316

SIP_size_C = 368

SIP_size #in bytes (varies based on HB)

SIP_size_T = 344

SIPx.py

s #socket

tmp #file

whoami=True #True/False toggle for notify message body

x #throwaway variable name

