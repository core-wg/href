SRC := draft-ietf-core-href.md

DIAGS := $(wildcard example/*.diag)
CBORS := $(DIAGS:.diag=.cbor)

CLEANFILES += $(CBORS)

%.cbor: %.diag ; diag2cbor.rb $< > $@

HTML := $(SRC:.md=.html)

CLEANFILES += $(HTML)

TEXT := $(SRC:.md=.txt)

CLEANFILES += $(TEXT)

XML := $(SRC:.md=.xml)

CLEANFILES += $(XML)

SUBMIT_XML := $(SRC:.md=.v2v3.xml)

CLEANFILES += $(SUBMIT_XML)

$(SUBMIT_XML) $(HTML) $(XML) $(TXT): $(SRC) $(CBORS)
	for f in $(CBORS) ; do cddl cddl/cri.cddl v $$f ; done
	kdrfc -3chi $<

.PHONY: clean
clean: ; $(RM) $(CLEANFILES)

.DEFAULT_GOAL := $(HTML)
