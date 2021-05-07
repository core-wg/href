.DEFAULT_GOAL := all

SRC := draft-ietf-core-href.md

DIAGS := $(wildcard example/*.diag)
CBORS := $(DIAGS:.diag=.cbor)

CLEANFILES += $(CBORS)

%.cbor: %.diag ; diag2cbor.rb $< > $@

HTML := $(SRC:.md=.html)

CLEANFILES += $(HTML)

TEXT := $(SRC:.md=.txt)

CLEANFILES += $(TEXT)

.PHONY: check
check: $(CBORS)
	for f in $(CBORS) ; do cddl cddl/cri.cddl v $$f ; done

all: $(HTML)

$(TEXT) $(HTML): $(SRC) check
	kdrfc -3 -h -i $<

.PHONY: clean
clean: ; $(RM) $(CLEANFILES)
