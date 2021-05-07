# The Constrained RESTful Application Language (CoRAL)


## Specifications

* Constrained RESTful Application Language
    * [draft-ietf-core-coral-03](https://www.ietf.org/id/draft-ietf-core-coral-03.html) ([datatracker](https://datatracker.ietf.org/doc/draft-ietf-core-coral/))
* Constrained Resource Identifiers
    * [draft-ietf-core-href-03](https://www.ietf.org/id/draft-ietf-core-href-03.html) ([datatracker](https://datatracker.ietf.org/doc/draft-ietf-core-href/))


## Companion Material 

* binary/
    * [python/](binary/python/)
    * [grammar.cddl](binary/grammar.cddl)
* textual/
    * [unicode/](textual/unicode/)
    * [lexical-grammar.abnf](textual/lexical-grammar.abnf)
    * [syntactic-grammar.abnf](textual/syntactic-grammar.abnf)


## Implementations

* C
    * [RIOT](https://github.com/leandrolanzieri/RIOT/tree/pr/sys-coral)
* Python
    * [micrurus](https://gitlab.com/chrysn/micrurus)


# Build the href draft

* install prerequisite tooling:
```
gem install cbor-diag cddl
```

* create the HTML and TXT version from the markdown source (also validate all the examples):
```
make -f href.mk
```

* remove build output and by-products:
```
make -f href.mk clean
```

