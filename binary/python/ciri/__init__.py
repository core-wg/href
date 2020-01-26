from .sequences import Option, PathType, is_well_formed, is_absolute, is_relative
from .resolution import resolve
from .irimapping import recompose
from .coapmapping import coap

def rfc5952str(address):
  import ipaddress
  return str(ipaddress.IPv6Address(bstr))
