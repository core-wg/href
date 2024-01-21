require 'rexml/document'; include REXML
XPath.each(Document.new(File.read("this.xml")),"/rfc/back//tr") {|r|
  puts XPath.each(r,"td").map{|d|d.text()}[0..1].join(",")}
