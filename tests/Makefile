all: check

# find out what has changed
check: tests.csv
	ruby csv-to-json.rb $< | diff tests.json -
	echo OK

# Call this explicitly to overwrite tests.json
tests.json: tests.csv
	ruby csv-to-json.rb $< >$@.new
	-mv $@ $@.bak
	mv $@.new $@

# Call this explicitly and then manually move to tests.csv
new-tests.csv: tests.json
	ruby json-to-csv.rb $< >$@.new
	mv $@.new $@
	-diff tests.csv $@

