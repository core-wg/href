require 'cbor-cri'
require 'cbor-diagnostic'
require 'json'
require 'csv'

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

def w(x)
  warn x.inspect
end

def hex_to_cri(h)
  CBOR::CRI.new(*CBOR.decode(h.xeh))
end

def hex_to_diag(h)
  CBOR.decode(h.xeh).cbor_diagnostic
end

def check(sym, a, b, strict = false)
  unless a == b
    w [sym, a.item_diag, b.item_diag]
    fail if strict
  end
end

class Object
  def item_diag
    inspect
  end
end

class CBOR::CRI
  def item_diag
    to_item.cbor_diagnostic
  end
end

test_data = JSON.load(ARGF.read)

seen = Set[]

result = CSV.generate(col_sep: ";", quote_char: "|", quote_empty: false) do |csv|

  csv << ["type", "uri", "cri", "red",
          "resolved_uri", "resolved_cri",
          "cri_hex", "resolved_cri_hex", "comment"]

  baseuri = test_data["base-uri"]
  basecri_hex = test_data["base-cri"]
  basecri = hex_to_cri(basecri_hex)
  csv << ["base", baseuri, basecri.item_diag, "",
          "", "",
          basecri_hex]

  rt_basecri = CBOR::CRI.from_uri(baseuri)
  fail ["*** basecri", basecri, "basecri from baseuri", rt_basecri].inspect if basecri != rt_basecri
  fail ["*** basecri.to_item", basecri.to_item, "(basecri from baseuri).to_item", rt_basecri.to_item].inspect if basecri.to_item != rt_basecri.to_item
  baseuri_out = basecri.to_uri
  fail ["*** basecri.to_uri", baseuri_out, "baseuri", rt_basecri.to_item].inspect if baseuri_out != baseuri

  tests = test_data["test-vectors"]
  tests.each do |td|
    uri_in = td["uri"]

    cri_in_hex = td["cri"].downcase
    cri_in = hex_to_cri(cri_in_hex)
    cri_in_diag = cri_in.item_diag
    check("hex cri_in", cri_in_hex, cri_in.to_item.to_cbor.hexi) # ,true

    uri_from_cri = td["uri-from-cri"]
    red = uri_from_cri != uri_in

    resolved_cri_hex = td["resolved-cri"].downcase
    resolved_cri = hex_to_cri(resolved_cri_hex)
    check("hex resolved_cri", resolved_cri_hex, resolved_cri.to_item.to_cbor.hexi, true)
    
    # warn "resolved: #{hex_to_diag(td["resolved-cri"])}"
    resolved_uri = td["resolved-uri"]

    cri_out = CBOR::CRI.from_uri(uri_in) if uri_in
    # w cri_out.item_diag
    check :_CRI_IN_OUT, cri_in, cri_out if uri_in
    uri_out = cri_out.to_uri if uri_in
    check :_URI_IN_OUT, uri_out, uri_from_cri
    check :_RES_IN_URI,  resolved_uri, resolved_cri.to_uri
    my_resolved_cri = basecri.merge(cri_in)
    check :_RES_CRI, resolved_cri, my_resolved_cri
    my_resolved_cri_to_uri = my_resolved_cri.to_uri
    check :_RES_CRI_URI, my_resolved_cri_to_uri, resolved_uri
    my_resolved_uri_cri = CBOR::CRI.from_uri(resolved_uri)
    check :_RES_URI_CRI, my_resolved_uri_cri, resolved_cri

    comment = td["description"] || ""

    item = [red ? "red" : "rt", 
            uri_in, cri_in_diag, red ? uri_from_cri : "",
            resolved_uri, resolved_cri.item_diag,
            cri_in_hex, resolved_cri_hex, comment]
    unless seen === item
      csv << item
      seen << item
    end
  end

end

# puts result.lines.uniq
puts result

exit

