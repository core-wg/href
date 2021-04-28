from . import *

def coap(href, to_proxy=False):
  if not is_absolute(href):
    return None

  result = b''
  previous = 0

  for option, value in href:
    if option == Option.SCHEME:
      continue
    elif option == Option.HOST_NAME:
      opt = 3  # Uri-Host
      val = value.encode('utf-8')
    elif option == Option.HOST_IP:
      opt = 3  # Uri-Host
      val = _encode_ip_address(value).encode('utf-8')
    elif option == Option.PORT:
      opt = 7  # Uri-Port
      val = value.to_bytes((value.bit_length() + 7) // 8, 'big')
    elif option == Option.BASE_PATH:
      return None
    elif option == Option.PATH:
      opt = 11  # Uri-Path
      val = value.encode('utf-8')
    elif option == Option.QUERY:
      opt = 15  # Uri-Query
      val = value.encode('utf-8')
    elif option == Option.FRAGMENT:
      continue
    result += _encode_coap_option(opt - previous, val)
    previous = opt

  if to_proxy:
    (option, value) = href[0]
    opt = 39  # Proxy-Scheme
    val = value.encode('utf-8')
    result += _encode_coap_option(opt - previous, val)
    previous = opt

  return result


def _encode_ip_address(b):
  if len(b) == 4:
    return '.'.join(str(c) for c in b)
  elif len(b) == 16:
    return '[' + rfc5952str(b) + ']'


def _encode_coap_option(delta, value):
  length = len(value)
  delta_nibble = _encode_coap_option_nibble(delta)
  length_nibble = _encode_coap_option_nibble(length)
  result = bytes([delta_nibble << 4 | length_nibble])
  if delta_nibble == 13:
    delta -= 13
    result += bytes([delta])
  elif delta_nibble == 14:
    delta -= 256 + 13
    result += bytes([delta >> 8, delta & 255])
  if length_nibble == 13:
    length -= 13
    result += bytes([length])
  elif length_nibble == 14:
    length -= 256 + 13
    result += bytes([length >> 8, length & 255])
  result += value
  return result


def _encode_coap_option_nibble(n):
  if n < 13:
    return n
  elif n < 256 + 13:
    return 13
  elif n < 65536 + 256 + 13:
    return 14
