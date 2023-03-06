schemes-numbers.md: schemes-numbers.rb
	ruby $< > $@.new
	mv $@.new $@

extracted-schemes-numbers.csv: extract-schemes-numbers.rb this.xml
	ruby $< > $@.new
	mv $@.new $@
