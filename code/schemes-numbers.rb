require 'rexml/document'
require 'digest'

class String
  def vlb
    n = 0
    each_byte { |b| n <<= 8; n += b}
    n
  end
end

def get_one(el, xp)
  v = REXML::XPath.each(el, xp).map {|el| el.text()}
  fail if v.size != 1
  v.first
end

schemes = REXML::Document.new(File.read("/Users/cabo/std/iana/uri-schemes/uri-schemes.xml"))

a = REXML::XPath.each(schemes.root, "//record").map do |rec|
  get_one(rec, "value")
end
warn a.count
a << "mqtt" # Unregistered
a << "mqtts" # Unregistered
warn a.count

prefill = DATA.read
prefill.each_line do |li|
  if /-[0-9]+\s+\|\s+([a-z][a-z0-9+.-]*)\s+\|/ =~ li
    a.delete($1)
  end
end

warn a.count

result = (0...240).each do |start|
  reg = {}
  endmask = (1 << 14) - 1
  offset = 1024

  begin
    a.each do |v, s|
      dig = Digest::SHA256.digest v
      n = (dig.vlb >> start & endmask) + offset
      if n == 0 || reg[-n]
        fail [start, v, n, reg[-n]].inspect
      end
      reg[-n] = v
    end
    warn [:OK, start].inspect
    # result = reg
    break reg
  rescue RuntimeError => e
    warn e.detailed_message
  end
end
puts prefill
result.sort {|a, b| b <=> a}.each do |value, scheme|
puts "| %9s | %16s | \\[RFC-XXXX] |"  % [value, scheme]
end

__END__

| CRI value | URI scheme | Reference   |
|-----------|------------|-------------|
|        -1 | coap       | \[RFC-XXXX] |
|        -2 | coaps      | \[RFC-XXXX] |
|        -3 | http       | \[RFC-XXXX] |
|        -4 | https      | \[RFC-XXXX] |
|        -5 | urn        | \[RFC-XXXX] |
|        -6 | did        | \[RFC-XXXX] |
|        -7 | coap+tcp   | \[RFC-XXXX] |
|        -8 | coaps+tcp  | \[RFC-XXXX] |
|        -9 | coap+ws    | \[RFC-XXXX] |
|       -10 | coaps+ws   | \[RFC-XXXX] |
