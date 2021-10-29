# HREF Test Vectors

The file [tests.json](tests.json) contains a set of test vectors for [draft-ietf-core-href-07](https://www.ietf.org/archive/id/draft-ietf-core-href-07.html) derived from [Carsten's initial proposal](https://notes.ietf.org/2Y2YyFstQ5uenofIGBa4IQ).

> NOTE: some tests are currently broken, see annotations in the [master copy](https://notes.ietf.org/2Y2YyFstQ5uenofIGBa4IQ).

## Test Input

### Bases

All test vectors use the same base URI `coaps://foo:4711/pa/th?query#frag`, which corresponds to the base CRI `[-2, ["foo", 4711], ["pa", "th"], ["query"], "frag"]`.

### Test Vector Layout

Each test vector is organized as follows:

| Key Name | Description |
| --- | --- |
| `uri` | a URI reference |
| `cri` | hex-encoded binary representation of the CRI reference corresponding to `uri` |
| `uri-from-cri` | the URI obtained translating the CRI reference `cri` |
| `resolved-cri` | hex-encoded binary representation of the resolved CRI reference relative to the [base CRI](#bases) |
| `resolved-uri` | resolved URI relative to the [base URI](#bases) |

## Test Logics

### CBOR deserialization

* Parse `cri` according to [§5.1](https://www.ietf.org/archive/id/draft-ietf-core-href-07.html#section-5.1) and assert there are no errors

### Converting CRIs to URIs

* Convert `cri` to URI according to [§6.1](https://www.ietf.org/archive/id/draft-ietf-core-href-07.html#section-6.1) and assert the result matches `uri-from-cri`
* Convert `resolved-cri` to URI and assert the result matches `resolved-uri`

### Reference Resolution

* Resolve `cri` relative to the [base CRI](#bases) according to [§5.3](https://www.ietf.org/archive/id/draft-ietf-core-href-07.html#section-5.3) and assert the result matches `resolved-cri`
