require 'cbor-diagnostic'
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

test_data = {}

tv = []

CSV.read("tests.csv").each do |row|
  case row
  in ["base", baseuri, basecri_diag]
    test_data["base-uri"] = baseuri
    test_data["base-cri"] = diag_to_hex(basecri_diag)
    test_data["test-vectors"] = tv
  in ["ok", uri_in, cri_in_diag, uri_from_cri_opt, resolved_cri_diag, resolved_uri]
    tv << {
      "uri" => uri_in,
      "cri" => diag_to_hex(cri_in_diag),
      "uri-from-cri" => (uri_from_cri_opt == "=" ? uri_in : uri_from_cri_opt),
      "resolved-cri" => diag_to_hex(resolved_cri_diag),
      "resolved-uri" => resolved_uri,
    }
  end
end

puts JSON.pretty_generate(test_data)
