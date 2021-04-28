from .sequences import Option, is_wellformed, is_absolute, is_relative
from .resolution import resolve
from .urimapping import recompose
from .coapmapping import coap

def rfc5952str(address):
  import ipaddress
  return str(ipaddress.IPv6Address(bstr))
