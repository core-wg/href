require 'rexml/document'; include REXML
XPath.each(Document.new(File.read("this.xml")),"//tr") {|row|
  puts XPath.each(row,"td").map{|d|d.text()}[0..1].join(",")}
