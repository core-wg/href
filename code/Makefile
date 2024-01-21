schemes-numbers.md: schemes-numbers.rb uri-schemes.xml
	ruby $< > $@.new
	mv $@.new $@

extracted-schemes-numbers.csv: extract-schemes-numbers.rb this.xml
	ruby $< > $@.new
	mv $@.new $@
