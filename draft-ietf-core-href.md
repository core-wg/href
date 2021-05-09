---
stand_alone: true
ipr: trust200902
docname: draft-ietf-core-href-latest
cat: std
submissiontype: IETF
consensus: true
lang: en
pi:
  toc: 'true'
  tocdepth: '3'
  symrefs: 'true'
  sortrefs: 'true'
title: Constrained Resource Identifiers
wg: CoRE Working Group

author:
- ins: K. Hartke
  name: Klaus Hartke
  org: Ericsson
  street: Torshamnsgatan 23
  city: Stockholm
  code: '16483'
  country: Sweden
  email: klaus.hartke@ericsson.com
-
  ins: C. Bormann
  name: Carsten Bormann
  org: Universitaet Bremen TZI
  street: Postfach 330440
  city: Bremen
  code: D-28359
  country: Germany
  phone: +49-421-218-63921
  email: cabo@tzi.org
  role: editor

informative:
  RFC7228:
  RFC7230:
  RFC7252:
  RFC8141:
  RFC8288:
  RFC8820:
  W3C.REC-html52-20171214:
normative:
  RFC3986:
  RFC3987:
  RFC8610:
  Unicode:
    target: https://www.unicode.org/versions/Unicode13.0.0/
    title: The Unicode Standard, Version 13.0.0
    author:
    - org: The Unicode Consortium
    date: 2020-03
    seriesinfo:
      ISBN: 978-1-936213-26-9
  RFC8949: cbor

--- abstract


The Constrained Resource Identifier (CRI) is a complement to the Uniform
Resource Identifier (URI) that serializes the URI components in Concise
Binary Object Representation (CBOR) instead of a sequence of characters.
This simplifies parsing, comparison and reference resolution in
environments with severe limitations on processing power, code size, and
memory size.

--- to_be_removed_note_Note_to_Readers

The issues list for this Internet-Draft can be found at
\<https://github.com/core-wg/coral/labels/href>.

A reference implementation and a set of test vectors can be found at
\<https://github.com/core-wg/coral/tree/master/binary/python>.

--- middle

# Introduction

The [Uniform Resource Identifier (URI)](#RFC3986) and its most common
usage, the URI reference, are the Internet standard for linking to
resources in hypertext formats such as [HTML](#W3C.REC-html52-20171214)
or the [HTTP "Link" header field](#RFC8288).

A URI reference is a sequence of characters chosen from the repertoire
of US-ASCII characters.
The individual components of a URI reference are delimited by a number
of reserved characters, which necessitates the use of a character escape
mechanism called "percent-encoding" when these reserved characters are
used in a non-delimiting function.
The resolution of URI references involves parsing a character sequence
into its components, combining those components with the components of a
base URI, merging path components, removing dot-segments, and
recomposing the result back into a character sequence.

Overall, the proper handling of URI references is quite intricate.
This can be a problem especially in [constrained environments](#RFC7228),
where nodes often have severe code size and memory size limitations.
As a result, many implementations in such environments support only an
ad-hoc, informally-specified, bug-ridden, non-interoperable subset of
half of RFC 3986.

This document defines the Constrained Resource Identifier (CRI) by
constraining URIs to a simplified subset and serializing their
components in [Concise Binary Object Representation (CBOR)](#RFC8949)
instead of a sequence of characters.
This allows typical operations on URI references such as parsing,
comparison and reference resolution (including all corner cases) to be
implemented in a comparatively small amount of code.

As a result of simplification, however, CRIs are not capable of
expressing all URIs permitted by the generic syntax of RFC 3986 (hence
the "constrained" in "Constrained Resource Identifier").
The supported subset includes all URIs of the
[Constrained Application Protocol (CoAP)](#RFC7252), most URIs of the
[Hypertext Transfer Protocol (HTTP)](#RFC7230),
[Uniform Resource Names (URNs)](#RFC8141), and other similar URIs.
The exact constraints are defined in {{constraints}}.

## Notational Conventions

{::boilerplate bcp14-tagged}

In this specification, the term "byte" is used in its now customary
sense as a synonym for "octet".

Terms defined in this document appear in *cursive* where they
are introduced (rendered in plain text as the new term surrounded by
underscores).



# Constraints {#constraints}

A Constrained Resource Identifier consists of the same five components
as a URI: scheme, authority, path, query, and fragment.
The components are subject to the following constraints:

{: type="C%d."}
1. {:#c-scheme} The scheme name can be any Unicode string (see
   Definition D80 in {{Unicode}}) that matches the syntax of a URI
   scheme (see {{Section 3.1 of RFC3986}}) and is lowercase (see
   Definition D139 in {{Unicode}}).

1. {:#c-authority} An authority is always a host identified by an IP
   address or registered name, along with optional port information.
   User information is not supported.

1. {:#c-ip-address} An IP address can be either an IPv4 address or an IPv6 address.
   IPv6 scoped addressing zone identifiers and future versions of IP are
   not supported.

1. {:#c-reg-name} A registered name can be any Unicode string that is lowercase and in
   Unicode Normalization Form C (NFC) (see Definition D120 in {{Unicode}}).
   (The syntax may be further restricted by the scheme.)

1. {:#c-port-range} A port is always an integer in the range from 0 to 65535.
   Empty ports or ports outside this range are not supported.

1. {:#c-port-omitted} The port is omitted if and only if the port would be the same as the
   scheme's default port (provided the scheme is defining such a default
   port) or the scheme is not using ports.

1. {:#c-path} A path consists of zero or more path segments.
   A path must not consist of a single zero-length path segment, which
   is considered equivalent to a path of zero path segments.

1. {:#c-path-segment} A path segment can be any Unicode string that is
   in NFC, with the exception of the special "." and ".." complete path
   segments.
   It can be the zero-length string. No special constraints are placed
   on the first path segment.

1. {:#c-query} A query always consists of one or more query parameters.
   A query parameter can be any Unicode string that is in NFC.
   It is often in the form of a "key=value" pair.
   When converting a CRI to a URI, query parameters are separated by an
   ampersand ("&") character.
   (This matches the structure and encoding of the target URI in CoAP
   requests.)
   Queries are optional; there is a difference between an absent query
   and a single query parameter that is the empty string.

1. {:#c-fragment} A fragment identifier can be any Unicode string that
   is in NFC.
   Fragment identifiers are optional; there is a difference between an
   absent fragment identifier and a fragment identifier that is the
   empty string.

1. {:#c-escaping} The syntax of registered names, path segments, query
   parameters, and fragment identifiers may be further restricted and
   sub-structured by the scheme.
   There is no support, however, for escaping sub-delimiters
   that are not intended to be used in a delimiting function.

1. {:#c-mapping} When converting a CRI to a URI, any character that is
   outside the allowed character range or is a delimiter in the URI syntax
   is percent-encoded.
   For CRIs, percent-encoding always uses the UTF-8 encoding form (see
   Definition D92 in {{Unicode}}) to convert the character to a sequence
   of bytes (that is then converted to a sequence of %HH triplets).


# Creation and Normalization

In general, resource identifiers are created on the initial creation of a
resource with a certain resource identifier, or the initial exposition
of a resource under a particular resource identifier.

A Constrained Resource Identifier SHOULD be created by
the naming authority that governs the namespace of the resource
identifier (see also {{RFC8820}}).
For example, for the resources of an HTTP origin server,
that server is responsible for creating the CRIs for those resources.

The naming authority MUST ensure that any CRI created
satisfies the constraints defined in {{constraints}}. The creation of a
CRI fails if the CRI cannot be validated to satisfy all of the
constraints.

{:ctr: format="counter"}

If a naming authority creates a CRI from user input, it MAY apply
the following (and only the following) normalizations to get the CRI
more likely to validate:

* map the scheme name to lowercase ({{c-scheme}}{:ctr});
* map the registered name to NFC ({{c-reg-name}}{:ctr});
* elide the port if it is the default port for the scheme
({{c-port-omitted}}{:ctr});
* elide a single zero-length path segment ({{c-path}}{:ctr});
* map path segments, query parameters and the fragment identifier to NFC
({{c-path-segment}}{:ctr}, {{c-query}}{:ctr}, {{c-fragment}}{:ctr}).

Once a CRI has been created, it can be used and transferred without
further normalization.
All operations that operate on a CRI SHOULD rely on the
assumption that the CRI is appropriately pre-normalized.
(This does not contradict the requirement that when CRIs are
transferred, recipients must operate on as-good-as untrusted input and
fail gracefully in the face of malicious inputs.)


# Comparison

One of the most common operations on CRIs is comparison: determining
whether two CRIs are equivalent, without dereferencing the CRIs (using
them to access their respective resource(s)).

Determination of equivalence or difference of CRIs is based on simple
component-wise comparison. If two CRIs are identical
component-by-component (using code-point-by-code-point comparison for
components that are Unicode strings) then it is safe to conclude that
they are equivalent.

This comparison mechanism is designed to minimize false negatives while
strictly avoiding false positives.
The constraints defined in {{constraints}} imply the most
common forms of syntax- and scheme-based normalizations in URIs, but do
not comprise protocol-based normalizations that require accessing the
resources or detailed knowledge of the scheme's dereference algorithm.
False negatives can be caused, for example, by CRIs that are not
appropriately pre-normalized and by resource aliases.

When CRIs are compared to select (or avoid) a network action, such as
retrieval of a representation, fragment components (if any) should be
excluded from the comparison.


# CRI References

The most common usage of a Constrained Resource Identifier is to embed
it in resource representations, e.g., to express a hyperlink between the
represented resource and the resource identified by the CRI.

This section defines the serialization of CRIs in
[Concise Binary Object Representation (CBOR)](#RFC8949).
To reduce representation size, CRIs are not serialized directly.
Instead, CRIs are indirectly referenced through *CRI references*.
These take advantage of hierarchical locality and provide a very compact
encoding.
The CBOR serialization of CRI references is specified in
{{cbor-serialization}}.

The only operation defined on a CRI reference is *reference resolution*:
the act of transforming a CRI reference into a CRI.
An application MUST implement this operation by applying
the algorithm specified in {{reference-resolution}} (or any algorithm
that is functionally equivalent to it).

The reverse operation of transforming a CRI into a CRI reference is
unspecified;
implementations are free to use any algorithm as long as reference
resolution of the resulting CRI reference yields the original CRI.
Notably, a CRI reference is not required to satisfy all of the
constraints of a CRI; the only requirement on a CRI reference is that
reference resolution MUST yield the original CRI.

When testing for equivalence or difference, applications SHOULD NOT
directly compare CRI references; the references should be
resolved to their respective CRI before comparison.

## CBOR Serialization {#cbor-serialization}

A CRI reference is encoded as a CBOR array {{RFC8949}}, with the
structure as described in the [Concise Data Definition Language
(CDDL)](#RFC8610) as follows:

~~~~ cddl
{::include cddl/cri.cddl}
~~~~

The rules `scheme`, `host`, `port`, `path`, `query`, `fragment`
correspond to the (sub-)components of a CRI, as described in
{{constraints}}, with the addition of the `discard` section.
As `scheme` and `host` can comprise two array elements, and `path`
segments and `query` parameters can occur zero or more times, we will treat
such combinations as a single "section" in the following exposition.
(For `scheme` and `host`, the combination is needed to disambiguate what would otherwise be a
leading text string as a scheme, host, or path segment.)
The `discard` section or its absence can be used to express path
prefixes such as "/",
"./", "../", "../../", etc.
The exact semantics of the section values are defined by
{{reference-resolution}}.

Examples:
:  

: ~~~~ cbor
{::include example/href-cri-reference-1.diag}
  ~~~~

: ~~~~ cbor
{::include example/href-cri-reference-2.diag}
  ~~~~


A CRI reference is considered *well-formed* if it matches the CDDL
structure.

A CRI reference is considered *absolute* if it is well-formed
and the sequence of sections starts with a `scheme`.

A CRI reference is considered *relative* if it is well-formed
and the sequence of sections is empty or starts with an section other
than those that would constitute a `scheme`.


## Reference Resolution {#reference-resolution}

The term "relative" implies that a "base CRI" exists against which the
relative reference is applied. Aside from fragment-only references,
relative references are only usable when a base CRI is known.

The following steps define the process of resolving any well-formed CRI
reference against a base CRI so that the result is a CRI in the form of
an absolute CRI reference:

1. Establish the base CRI of the CRI reference and express it in the
  form of an absolute CRI reference.
  (The base CRI can be established in a number of ways; see
  {{Section 5.1 of RFC3986}}.)
  Assign each section an section number according to the number E for
  that section in {{resolution-variables}}.

1. Determine the values of two variables, T and E, based on the first
   section in the sequence of sections of the CRI reference to be
   resolved, according to {{resolution-variables}}.

1. Initialize a buffer with all the sections from the base CRI where
   the section number is less than the value of E.

1. If the value of T is greater than 0, remove the last T-many `path`
   segments from the end of the buffer (up to the number of `path`
   segments in the buffer).

1. Append all the sections from the CRI reference to the buffer, except
  for any `discard` section.

1. If the number of `path` segments in the buffer is one and the
  value of that segment is the zero-length string, remove that segment
  from the buffer.

1. Return the sequence of sections in the buffer as the resolved CRI.
n
| First Section       |             T | E |
| (scheme)            |             0 | 0 |
| (host)              |             0 | 1 |
| (discard)           | item value | 4 |
| (path)              |             0 | 2 |
| (query)             |             0 | 3 |
| (fragment)          |             0 | 4 |
| none/empty sequence |             0 | 4 |
{: #resolution-variables align="center" title="Values of the Variables T and E"}


# Relationship between CRIs, URIs and IRIs

CRIs are meant to replace both [Uniform Resource Identifiers (URIs)](#RFC3986)
and [Internationalized Resource Identifiers (IRIs)](#RFC3987)
in [constrained environments](#RFC7228).
Applications in these environments may never need to use URIs and IRIs
directly, especially when the resource identifier is used simply for
identification purposes or when the CRI can be directly converted into a
CoAP request.

However, it may be necessary in other environments to determine the
associated URI or IRI of a CRI, and vice versa. Applications can perform
these conversions as follows:

{: vspace='0'}
CRI to URI
: A CRI is converted to a URI as specified in {{cri-to-uri}}.

URI to CRI
: The method of converting a URI to a CRI is unspecified;
  implementations are free to use any algorithm as long as converting
  the resulting CRI back to a URI yields an equivalent URI.

CRI to IRI
: A CRI can be converted to an IRI by first converting it to a URI as
  specified in {{cri-to-uri}}, and then converting the URI
  to an IRI as described in {{Section 3.2 of RFC3987}}.

IRI to CRI
: An IRI can be converted to a CRI by first converting it to a URI as
  described in {{Section 3.1 of RFC3987}}, and then
  converting the URI to a CRI as described above.

Everything in this section also applies to CRI references, URI
references and IRI references.


## Converting CRIs to URIs {#cri-to-uri}

Applications MUST convert a CRI reference to a URI
reference by determining the components of the URI reference according
to the following steps and then recomposing the components to a URI
reference string as specified in {{RFC3986}}{: section="5.3"}.

{: vspace='0'}

scheme
: If the CRI reference contains a `scheme` section, the scheme
  component of the URI reference consists of the value of that
  section.
  Otherwise, the scheme component is unset.

authority
: If the CRI reference contains a `host-name` or `host-ip` item, the
  authority component of the URI reference consists of a host
  subcomponent, optionally followed by a colon (":") character and a
  port subcomponent.  Otherwise, the authority component is unset.

  The host subcomponent consists of the value of the `host-name` or
  `host-ip` item.

  Any character in the value of a `host-name` item that is not in
  the set of unreserved characters ({{Section 2.3 of RFC3986}}) or
  "sub-delims" ({{Section 2.2 of RFC3986}}) MUST be
  percent-encoded.

  The value of a `host-ip` item MUST be
  represented as a string that matches the "IPv4address" or
  "IP-literal" rule ({{Section 3.2.2 of RFC3986}}).

  If the CRI reference contains a `port` item, the port
  subcomponent consists of the value of that item in decimal
  notation.
  Otherwise, the colon (":") character and the port subcomponent are
  both omitted.

path
: If the CRI reference is an empty sequence of items or starts with
  a `port` item, a `path` item, or a `discard` item where the
  value is not 0, the conversion fails.

  If the CRI reference contains a `host-name` item, a `host-ip`
  item or a `discard` section, the path
  component of the URI reference is prefixed by a slash ("/")
  character.  Otherwise, the path component is prefixed by the
  zero-length string.

  If the CRI reference contains one or more `path` items,
  the prefix is followed by the value of each item, separated by a
  slash ("/") character.

  Any character in the value of a `path` item that is not
  in the set of unreserved characters or "sub-delims" or a colon
  (":") or commercial at ("@") character MUST be
  percent-encoded.

  If the authority component is defined and the path component does not
  match the "path-abempty" rule ({{Section 3.3 of RFC3986}}), the
  conversion fails.

  If the authority component is unset and the scheme component is
  defined and the path component does not match the "path-absolute",
  "path-rootless" or "path-empty" rule ({{Section 3.3 of RFC3986}}), the
  conversion fails.

  If the authority component is unset and the scheme component is
  unset and the path component does not match the "path-absolute",
  "path-noscheme" or "path-empty" rule ({{Section 3.3 of RFC3986}}), the
  conversion fails.

query
: If the CRI reference contains one or more `query` items,
  the query component of the URI reference consists of the value of
  each item, separated by an ampersand ("&") character.
  Otherwise, the query component is unset.

  Any character in the value of a `query` item that is not
  in the set of unreserved characters or "sub-delims" or a colon
  (":"), commercial at ("@"), slash ("/") or question mark ("?")
  character MUST be percent-encoded.
  Additionally, any ampersand character ("&") in the item
  value MUST be percent-encoded.

fragment
: If the CRI reference contains a fragment item, the fragment
  component of the URI reference consists of the value of that
  item.
  Otherwise, the fragment component is unset.

  Any character in the value of a `fragment` item that is
  not in the set of unreserved characters or "sub-delims" or a colon
  (":"), commercial at ("@"), slash ("/") or question mark ("?")
  character MUST be percent-encoded.



# Security Considerations {#security}

Parsers of CRI references must operate on input that is assumed to be
untrusted. This means that parsers MUST fail gracefully
in the face of malicious inputs.
Additionally, parsers MUST be prepared to deal with
resource exhaustion (e.g., resulting from the allocation of big data
items) or exhaustion of the call stack (stack overflow).
See {{Section 10 of RFC8949}} for additional
security considerations relating to CBOR.

The security considerations discussed in {{Section 7 of RFC3986}} and
{{Section 8 of RFC3987}} for URIs and IRIs also apply to CRIs.


# IANA Considerations

This document has no IANA actions.


--- back

# Change Log
{: removeInRFC="true"}

Changes from -03 to -04:

* Minor editorial improvements.

* Renamed path.type/path-type to discard.

* Renamed option to section, substructured into items.

* Simplied {{resolution-variables}}.

* Use the CBOR structure inspired by Jim Schaad's proposals.

Changes from -02 to -03:

* Expanded the set of supported schemes (#3).

* Specified creation, normalization and comparison (#9).

* Clarified the default value of the `path.type` option (#33).

* Removed the `append-relation` path.type option (#41).

* Renumbered the remaining path.types.

* Renumbered the option numbers.

* Restructured the document.

* Minor editorial improvements.

Changes from -01 to -02:

* Changed the syntax of schemes to exclude upper case characters (#13).

* Minor editorial improvements (#34 #37).

Changes from -00 to -01:

* None.


# Acknowledgements
{: numbered="false"}

Thanks to
{{{Christian Amsüss}}},
{{{Ari Keränen}}},
{{{Jim Schaad}}} and
{{{Dave Thaler}}}
for helpful comments and discussions that have shaped the
document.


<!--  LocalWords:  CRI normalizations dereferencing dereference CRIs
 -->
<!--  LocalWords:  untrusted subcomponent
 -->
