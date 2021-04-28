REV = 04

OUTDIR=__build__/

SOURCES = $(wildcard *.xml)
INCLUDES = $(wildcard textual/examples/*.coral) $(wildcard binary/python/ciri/*.py)

TEXT = $(addprefix $(OUTDIR),$(SOURCES:.xml=-$(REV).txt))
HTML = $(addprefix $(OUTDIR),$(SOURCES:.xml=-$(REV).html))
XML = $(addprefix $(OUTDIR),$(SOURCES:.xml=-$(REV).xml))

all: html txt xml

html: $(HTML)

txt: $(TEXT)

xml: $(XML)

$(OUTDIR)%-$(REV).xml: %.xml $(INCLUDES)
	@mkdir -p $(dir $@)
	xml2rfc -p $(dir $@) -o $@ --expand $<

$(OUTDIR)%-$(REV).txt: %.xml $(INCLUDES)
	@mkdir -p $(dir $@)
	xml2rfc -p $(dir $@) -o $@ --v3 --no-pagination $<

$(OUTDIR)%-$(REV).html: %.xml $(INCLUDES)
	@mkdir -p $(dir $@)
	xml2rfc -p $(dir $@) -o $@ --html $<

clean:
	rm -f $(TEXT) $(HTML) $(XML)

cleancache:
	xml2rfc --clear-cache

.PHONY: all html txt xml clean cleancache
