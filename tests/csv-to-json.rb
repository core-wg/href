require 'cbor-diagnostic'
require 'cbor-deterministic'
require 'treetop'
require 'cbor-diag-parser'
require 'sid-csv'               # steal from sid-csv gem
include CSV::SID

class String
  def hexi
    bytes.map{|x| "%02x" % x}.join
  end
  def hexs
    bytes.map{|x| "%02x" % x}.join(" ")
  end
  def xeh
    gsub(/\s/, "").chars.each_slice(2).map{ |x| Integer(x.join, 16).chr("BINARY") }.join
  end
end

def hex_to_cri(h)
  CBOR::CRI.new(*CBOR.decode(h.xeh))
end

def hex_to_diag(h)
  CBOR.decode(h.xeh).cbor_diagnostic
end

def diag_to_hex(d)
  parser = CBOR_DIAGParser.new
  parser.parse(d).to_rb.to_cbor.hexi
end

def check(sym, a, b, strict = false)
  unless a == b
    w [sym, a.item_diag, b.item_diag]
    fail if strict
  end
end

def w(x)
  warn x.inspect
end

test_data = {}

tv = []
seen = Set[]

CSV.read("tests.csv", col_sep: ";", quote_char: "|", quote_empty: false).each do |row|
  case row
  in ["type", "uri", "cri", "red", "resolved_uri", "resolved_cri", "cri_hex", "resolved_cri_hex", "comment"]
  in ["base", baseuri, basecri_diag, *_foo]
    test_data["base-uri"] = baseuri
    test_data["base-cri"] = diag_to_hex(basecri_diag)
    test_data["test-vectors"] = tv
  in ["rt" | "red", uri_in, cri_in_diag, uri_from_cri_opt, resolved_uri, resolved_cri_diag, cri_hex_in, resolved_cri_hex_in, comment]
    cri_hex = diag_to_hex(cri_in_diag)
    check "** CRI_HEX", cri_hex_in, cri_hex
    resolved_cri_hex = diag_to_hex(resolved_cri_diag)
    check "** RESOLVED_CRI_HEX", resolved_cri_hex_in, resolved_cri_hex
    val = {
      "description" => comment || "",
      "uri" => uri_in || "",
      "cri" => cri_hex,
      "uri-from-cri" => uri_from_cri_opt || uri_in || "",
      "resolved-cri" => diag_to_hex(resolved_cri_diag),
      "resolved-uri" => resolved_uri,
    }
    valdet = val.cbor_prepare_deterministic.to_cbor
    unless seen === valdet
      tv << val
      seen << valdet
    end
  end
end

puts JSON.pretty_generate(test_data)
