require 'cbor-diagnostic'
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

def hex_to_diag(h)
  CBOR.decode(h.xeh).cbor_diagnostic
end



test_data = JSON.load_file("tests.json")

baseuri = test_data["base-uri"]
basecri_hex = test_data["base-cri"]
basecri_diag = hex_to_diag(basecri_hex)

data = [
  ["base", baseuri, # basecri_hex,
   basecri_diag]
]

tests = test_data["test-vectors"]
tests.each do |td|
  uri_in = td["uri"]
  cri_in = td["cri"]
  uri_from_cri = td["uri-from-cri"]
  resolved_cri = td["resolved-cri"]
  resolved_uri = td["resolved-uri"]
  data << [
    "ok", uri_in, # cri_in,
    hex_to_diag(cri_in),
    (uri_from_cri == uri_in ? "=" : uri_from_cri),
    # resolved_cri,
    hex_to_diag(resolved_cri), resolved_uri,
  ]
end


=begin
| Key Name            | Description                                                                                      |
| ---                 | ---                                                                                              |
| `type`              | kind of test: `ok`, `fail`; special value `base`                                                 |
| `uri`               | a URI reference                                                                                  |
| `cri`               | hex-encoded CBOR representation of the CRI reference corresponding to `uri`                      |
| `cri-diag`          | `cri` in CBOR diagnostic format                                                                  |
| `uri-from-cri`      | the URI obtained translating the CRI reference `cri`, or "=" if identical to `uri`               |
| `resolved-cri`      | hex-encoded CBOR representation of the resolved CRI reference relative to the [base CRI](#bases) |
| `resolved-cri-diag` | `resolved-cri` in CBOR diagnostic format                                                         |
| `resolved-uri`      | resolved URI relative to the [base URI](#bases)

=end                     |


puts csv_generate(data)
