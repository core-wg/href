---
v: 3

docname: draft-ietf-core-href-latest
cat: std
submissiontype: IETF
consensus: true
lang: en
title: Constrained Resource Identifiers
updates: 7595
wg: CoRE Working Group

v3xml2rfc:
  table_borders: light
kramdown_options:
  ol_start_at_first_marker: true

author:
- name: Carsten Bormann
  org: Universität Bremen TZI
  street: Postfach 330440
  city: Bremen
  code: D-28359
  country: Germany
  phone: +49-421-218-63921
  email: cabo@tzi.org
  role: editor
- name: Henk Birkholz
  org: Fraunhofer SIT
  email: henk.birkholz@sit.fraunhofer.de
  street: Rheinstrasse 75
  code: '64295'
  city: Darmstadt
  country: Germany

contributor:
- name: Klaus Hartke
  org: Ericsson
  street: Torshamnsgatan 23
  city: Stockholm
  code: '16483'
  country: Sweden
  email: klaus.hartke@ericsson.com
- name: Christian Amsüss
  street: Hollandstr. 12/4
  city: Vienna
  code: 1020
  country: Austria
  email: christian@amsuess.com

venue:
  group: Constrained RESTful Environments
  mail: core@ietf.org
  github: core-wg/href

informative:
  RFC3490: toascii
  RFC7228: term
  I-D.ietf-iotops-7228bis: termbis
  STD97: http
# RFC9110
  RFC7252: coap
  RFC8141: urn
  RFC8288: web-linking
  RFC9164: ip
  BCP190: lawn
#  BCP205:
  # RFC8820
  W3C.REC-html52-20171214:
  I-D.ietf-cbor-edn-literals: edn
  I-D.carpenter-6man-rfc6874bis: zonebis
  I-D.ietf-cbor-packed: packed
  I-D.bormann-cbor-notable-tags: notable
  RFC9170: use-lose
  GREENSPUN-10:
    target: https://en.wikipedia.org/wiki/Greenspun's_tenth_rule
    title: Greenspun's tenth rule
    date: false
    author:
      org: Wikipedia
  MNU: I-D.bormann-dispatch-modern-network-unicode
normative:
  STD66: uri
  STD63: utf-8
# RFC 3986
  RFC3987: iri
  RFC6874: zone
  BCP35: schemes
# RFC7595
  IANA.uri-schemes:
  BCP26:
    -: ianacons
#    =: RFC8126
  IANA.media-type-sub-parameters: mtsub
  RFC9237: aif
  IANA.core-parameters:
  IANA.cbor-tags: tags
  RFC8610: cddl
  Unicode:
    target: https://www.unicode.org/versions/Unicode13.0.0/
    title: The Unicode Standard, Version 13.0.0
    author:
    - org: The Unicode Consortium
    date: 2020-03
    seriesinfo:
      ISBN: 978-1-936213-26-9
  STD94: cbor
# RFC8949
  RFC9165: cddlcontrol

--- abstract


The Constrained Resource Identifier (CRI) is a complement to the Uniform
Resource Identifier (URI) that represents the URI components in Concise
Binary Object Representation (CBOR) rather than as a sequence of characters.
This approach simplifies parsing, comparison, and reference resolution in
environments with severe limitations on processing power, code size, and
memory size.

This RFC updates RFC 7595 to add a note on how the "URI Schemes"
registry of RFC 7595 cooperates with the "CRI Scheme Numbers"
registry created by the present RFC.

[^status]

[^status]: (This "cref" paragraph will be removed by the RFC editor:)\\
    The present revision –22 addresses a few remaining post-WGLC nits.

--- middle

{:cabo: source=" -- cabo"}

[^replace-xxxx]: RFC Ed.: throughout this section, please replace
    RFC-XXXX with the RFC number of this specification and remove this
    note.

# Introduction

The [Uniform Resource Identifier (URI)](#STD66) and its most common
usage, the URI reference, are the Internet standard for linking to
resources in hypertext formats such as [HTML](#W3C.REC-html52-20171214)
or the [HTTP "Link" header field](#RFC8288).

A URI reference is a sequence of characters chosen from the repertoire
of US-ASCII characters ({{Section 4.1 of RFC3986@-uri}}).
The individual components of a URI reference are delimited by a number
of reserved characters, which necessitates the use of a character escape
mechanism called "percent-encoding" when these reserved characters are
used in a non-delimiting function.
The resolution of URI references ({{Section 5 of RFC3986@-uri}})
involves parsing a character sequence
into its components, combining those components with the components of a
base URI, merging path components, removing dot-segments (`"." and
".."`, see {{Section 3.3
of RFC3986@-uri}}), and
recomposing the result back into a character sequence.

Overall, the proper handling of URI references is quite intricate.
This can be a problem especially in constrained environments {{-term}}{{-termbis}},
where nodes often have severe code size and memory size limitations.
As a result, many implementations in such environments support only an
ad-hoc, informally-specified, bug-ridden, non-interoperable subset of
half of {{STD66}} (aperçu adapted from {{GREENSPUN-10}}).

This document defines the *Constrained Resource Identifier (CRI)* by
constraining URIs to a simplified subset and representing their
components in [Concise Binary Object Representation (CBOR)](#STD94)
instead of a sequence of characters.
Analogously, *CRI references* are to CRIs what URI references are to
URIs.

CRIs and CRI references allow typical operations on URIs and URI references such as parsing,
comparison, and reference resolution (including all corner cases) to be
implemented in a comparatively small amount of code and to be less
prone to bugs and interoperability issues.

As a result of simplification, however, _Simple CRIs_ (i.e., not using
CRI extensions, see {{extending}}) are not capable of
expressing all URIs permitted by the generic syntax of {{STD66}} (hence
the "constrained" in "Constrained Resource Identifier").
The supported subset includes all URIs of the
[Constrained Application Protocol (CoAP)](#RFC7252), most URIs of the
[Hypertext Transfer Protocol (HTTP)](#STD97),
[Uniform Resource Names (URNs)](#RFC8141), and other similar URIs.
The exact constraints are defined in {{constraints}}.
CRI extensions ({{extending}}) can be defined to address some of the
constraints and/or to provide more convenient representations for
certain areas of application.

This RFC creates a "CRI Scheme Numbers" registry and updates {{RFC7595}}
to add a note on how this new registry cooperates with the "URI Schemes"
registry that {{RFC7595}} describes.


## Notational Conventions

{::boilerplate bcp14-tagged-bcp14}

In this specification, the term "byte" is used in its now customary
sense as a synonym for "octet".

Terms defined in this document appear in *cursive* where they
are introduced (in the plaintext form of this document, they are
rendered as the new term surrounded by underscores).

The general structure of data items is shown in the [Concise Data Definition
Language (CDDL)](#RFC8610) [including its control
extensions](#RFC9165).
Specific examples are notated in CBOR Extended
Diagnostic Notation (EDN), as originally introduced in {{Section 8 of
RFC8949@-cbor}} and extended in {{Appendix G of -cddl}}.
({{-edn}} more rigorously defines and further extends EDN.)


# From URIs to CRIs: Considerations and Constraints {#constraints}

## The CRI interchange data model

A Constrained Resource Identifier consists of the same five components
as a URI: scheme, authority, path, query, and fragment.

Many components of a URI can be "absent", i.e., they are optional.
This is not mirrored in CRIs, where all components are part of all
CRIs.
Some CRI components can have values that are `null` or empty arrays.
By defining a default value for each of certain components, they often can
be elided at the tail of the serialized form during interchange.
(Note that some subcomponents such as port numbers or userinfo are
optional in a CRI as well and therefore can be absent from a CRI.)

In a CRI reference, components can additionally be _not set_
(indicated by interchanging a discard value instead of scheme and
authority, or by `null` for the scheme, path and query components that
can otherwise not have that value).
(For example, for a CRI reference where authority is either not set or
has either of the NOAUTHORITY values, the equivalent URI reference's
authority is absent.)

<!-- possibly too confusing at this point.
for a CRI reference where the query is an
empty array or not set, the equivalent URI reference's query is absent).
 -->

The components are subject to the considerations and constraints
listed in this section.
Note that CRI extensions can relax constraints; for
example, see {{pet}} for partially relaxing constraint {{<c-nfc}}.

{: type="C%d."}
0. {:#c-nfc} Text strings in CRIs ("CRI text strings") are CBOR text
   strings (i.e., in UTF-8 form {{-utf-8}}) that represent Unicode
   strings (see Definition D80 in {{Unicode}}) in Unicode Normalization
   Form C (NFC) (see Definition D120 in {{Unicode}} and specifically
   {{norm-nfc}}).

1. {:#c-scheme} The scheme name can be any CRI text string that
   matches the syntax of a URI scheme (see {{Section 3.1 of
   RFC3986@-uri}}, which constrains scheme names to a subset of ASCII),
   in its canonical form.
   (The canonical form as per {{Section 3.1 of RFC3986@-uri}} requires
   alphabetic characters to be in lowercase.)
   <!-- see also Definition D139 in {{Unicode}}). -->
   The scheme is always present.

2. {:#c-authority} An authority is always a host identified by an IP
   address or a "registered name" (see {{<c-reg-name}} below), along with
   optional port information, and optionally preceded by user
   information.

   Alternatively, URIs can be formed without an authority.
   The two cases for this defined in {{Section 3.3 of RFC3986@-uri}} are
   modeled by two different special values used in the CRI authority component:

   * the path can be root-based (zero or more path segments that are
     each started in the URI with "/", as when the authority is
     present), or
   * the path can be rootless, which requires at least one path
     segment, the first one of which has non-zero length and is not
     started in the URI with "/".

   (Note that, in {{cddl}}, `no-authority` is marked as a feature, as
   not all CRI implementations will support authority-less URIs.)

3. {:#c-userinfo} A userinfo is a text string built out of unreserved
  characters ({{Section 2.3 of RFC3986@-uri}}) or "sub-delims" ({{Section 2.2
  of RFC3986@-uri}}); any other character needs to be percent-encoded ({{pet}}).
   Note that this excludes the ":" character, which is commonly
   deprecated as a way to delimit a cleartext password in a userinfo.

4. {:#c-ip-address} An IP address can be either an IPv4 address or an
   IPv6 address (optionally with a zone identifier {{-zone}}; see
   {{zone-id-issue}}).
   Future versions of IP are not supported (it is likely that a binary
   mapping would be strongly desirable, and that cannot be designed
   ahead of time, so these versions need to be added as a future
   extension if needed).

5. {:#c-reg-name} A _registered name_ is represented as a sequence of
   one or more lowercase CRI text string *labels* that do not contain
   dots (".").
   (These labels joined with dots (".") in between them result in the
   CRI equivalent of a URI registered name as per {{Section 3.2.2 of
   RFC3986@-uri}}.
   The syntax may be further restricted by the scheme.
   A URI registered name can be empty, for which case a scheme can
   define a default for the host.)

6. {:#c-port-range} A port is always an integer in the range from 0 to 65535.
   Ports outside this range, empty ports (port subcomponents with no
   digits, see {{Section 3.2.3 of RFC3986@-uri}}), or ports with redundant
   leading zeros, are not supported.

7. {:#c-port-omitted} If the scheme's port handling is known to the
   CRI creator, it is RECOMMENDED to omit the port if and only if the
   port would be the same as the scheme's default port (provided the
   scheme is defining such a default port) or the scheme is not using
   ports.

8. {:#c-path} A path consists of zero or more path segments.
   Note that a path of just a single zero-length path segment is allowed —
   this is considered equivalent to a path of zero path segments by
   HTTP and CoAP, but this equivalence does not hold for CRIs in general as they only perform
   normalization on the Syntax-Based Normalization level ({{Section
   6.2.2 of RFC3986@-uri}}), not on the scheme-specific Scheme-Based
   Normalization level ({{Section 6.2.3 of RFC3986@-uri}}).

   (A CRI implementation may want to offer scheme-cognizant
   interfaces, performing this scheme-specific normalization for
   schemes it knows.  The interface could assert which schemes the
   implementation knows and provide pre-normalized CRIs.  This can
   also relieve the application from removing a lone zero-length path
   segment before putting path segments into CoAP Options, i.e., from
   performing the check and jump in item 8 of {{Section 6.4 of
   -coap}}.  See also {{<sp-leading-empty}} in {{the-small-print}}.)

9. {:#c-path-segment} A path segment can be any CRI text string, with
   the exception of the special "." and ".." complete path segments.
   Note that this includes the zero-length string.

   If no authority is present in a CRI, the leading path segment cannot be empty.
   (See also {{<sp-leading-empty}} in {{the-small-print}}.)

10. {:#c-query} Queries are optional in URIs; there is a difference
   between an absent query and a single query parameter that is the
   empty string.
   A CRI represents its query component as an array of zero or more query
   parameters, which are CRI text strings.
   Zero query parameters (an empty array) is equivalent to a URI
   where the query is absent.
   A query in a URI is represented in a CRI by splitting its text up
   on any ampersand ("&") characters into one or more query
   parameters, which may contain certain characters (including
   ampersands) that were percent-encoded in the URI.
   Query parameters are often in the form of a "key=value" pair.
   When converting a CRI to a URI, one or more query parameters are
   constructed into a URI query by joining them together with
   ampersand characters, where certain characters (including
   ampersands) present in the query parameters are percent-encoded.
   (This matches the structure and encoding of the target URI in CoAP
   requests.)

11. {:#c-fragment} A fragment identifier can be any CRI text string.
   Fragment identifiers are optional in URIs; in CRIs there is a
   difference between a `null` fragment identifier and a fragment
   identifier that is the empty string.

12. {:#c-escaping} The syntax of registered names, path segments, query
   parameters, and fragment identifiers may be further restricted and
   sub-structured by the scheme.
   There is no support, however, for escaping sub-delimiters
   that are not intended to be used in a delimiting function.

13. {:#c-mapping} When converting a CRI to a URI, any character that is
   outside the allowed character range or is a delimiter in the URI syntax
   is percent-encoded.
   For CRIs, percent-encoding always uses the UTF-8 encoding form (see
   Definition D92 in {{Unicode}}) to convert the character to a sequence
   of bytes, which are then converted to a sequence of %HH triplets.
   <!-- As per 3986 2.1, use uppercase hex. -->

Examples for URIs at or beyond the boundaries of these constraints are in {{<sp-constraints}} in {{the-small-print}}.

## CRI References: The `discard` Component {#discard}

As with URI references and URIs, CRI references are a shorthand for a
CRI that is expressed relative to a base CRI.
URI and CRI references often *discard* part or all of the trailing
path segments of the base URI or CRI.

In a URI reference, this is expressed by syntax for its path component
such as leading special path segments `.` and `..` or a leading
slash before giving the path segments to be added at the end of the
(now truncated) base URI.
For use in CRI references, we instead add in a `discard` component as
an alternative to the `scheme` and `authority` components, making the
specification of discarding base URI path segments separate from
adding new path segments from the CRI reference.

The discarding intent of a CRI reference is thus fully condensed to a
single value in its discard component:

* An unsigned integer as the discard component specifies the number of
  path segments to be discarded from the base CRI (note that this
  includes the value 0 which cannot be expressed in URI references that then add any path component);

* the value `true` as the discard component
  specifies discarding all path segments from the base CRI.

If a scheme or authority is present in a CRI reference, the discard
component is implicitly equivalent to a value of `true` and thus not
included in the interchanged data item.

## Constraints not expressed by the data model

There are syntactically valid CRIs and CRI references that cannot be converted into a URI or URI reference, respectively.

CRI references of this kind can be acceptable -- they still can be resolved
and result in a valid full CRI that can be converted back.
Examples of this are:

* `[0, ["p"]]`: appends a slash and the path segment "p" to its base,
  sets the query to an empty array and the fragment to `null`
* `[0, null, []]`: leaves the path alone but sets the query to an
  empty array and the fragment to `null`

(Full) CRIs that do not correspond to a valid URI are not valid on their own, and cannot be used.
Normatively they are characterized by the {{cri-to-uri}} process not producing a valid and syntax-normalized URI.
For easier understanding, they are listed here:

* CRIs (and CRI references) containing dot-segments (path segment `"."` or `".."`).

  These segments would be removed by the remove_dot_segments algorithm of {{STD66}},
  and thus never produce a normalized URI after resolution.

  (In CRI references, the `discard` value is used to afford segment
  removal (see {{discard}}),
  and with "." being an unreserved character, expressing them as "%2e" and "%2e%2e" is not even viable,
  let alone practical).

* CRIs without authority whose path starts with a leading empty segment
  followed by at least one more segment.

  When converted to URIs, these would violate the requirement that in
  absence of an authority, a URI's path cannot begin with two slash
  characters.
  (E.g., two leading empty segments would be indistinguishable from a URI with a shorter path and a present but empty authority component.)
  (Compare {{<c-path-segment}}.)

* {:#naked-rootless} CRIs without authority that are rootless and have
  an empty path
  component (e.g., `["a", true, []]`), which would be indistinguishable
  from its root-based equivalent (`["a", null, []]`) as both would have the URI `a:`.

# Creation and Normalization {#norm}

In general, resource identifiers are generated when a
resource is initially created or exposed under a certain resource identifier.

The naming authority that creates
a Constrained Resource Identifier SHOULD be the authority that governs
the namespace of the resource identifier (see also {{BCP190}}).
For example, for the resources of an HTTP origin server,
that server is responsible for creating the CRIs for those resources.
If the naming authority creates a URI instead that can be obtained as
a conversion result from a CRI ({{cri-to-uri}}) that CRI can be
considered to have been created by the naming authority.

The naming authority MUST ensure that any CRI created
satisfies the required constraints defined in {{constraints}}. The creation of a
CRI fails if the CRI cannot be validated to satisfy all of the required
constraints.

If a naming authority creates a CRI from user input, it may need to apply
the following (and only the following) normalizations to get the CRI
more likely to validate:

* map the scheme name to lowercase ({{<c-scheme}});
* map the registered name to NFC ({{<c-reg-name}}) and split it on
  embedded dots;
* elide the port if it is the default port for the scheme
({{<c-port-omitted}});
<!-- * elide a single zero-length path segment ({{<c-path}}); -->
* map path segments, query parameters, and the fragment identifier to
  NFC form ({{<c-path-segment}}, {{<c-query}}, {{<c-fragment}}).

Once a CRI has been created, it can be used and transferred without
further normalization.
All operations that operate on a CRI SHOULD rely on the
assumption that the CRI is appropriately pre-normalized.
(This does not contradict the requirement that, when CRIs are
transferred, recipients must operate on as-good-as untrusted input and
fail gracefully in the face of malicious inputs.)

{:#norm-nfc}
Note that the processing of CRIs does not imply that all the
constraints continuously need to be checked and enforced.
Specifically, the text normalization constraints (NFC) can be expanded
as:
The recipient of a CRI MAY reasonably expect the text strings to be in
NFC form, but as with any input MUST NOT fail (beyond possibly not
being able to process the specific CRI) if they are not.
So the onus of fulfilling the expectation is on the original creator
of the CRI, not on each processor (including consumer).
This consideration extends to the sources the CRI creator uses in
building the text strings, which the CRI creator MAY in turn expect to be in
NFC form if that expectation is reasonable.
See {{Appendix C of MNU}} for some background.

CRIs have been designed with the objective that, after the above
normalization, conversion of two distinct CRIs to URIs do
not yield the "same" URI, including equivalence under syntax-based
normalization ({{Section 6.2.2 of RFC3986@-uri}}), but not including
protocol-based normalization.
Note that this objective exclusively applies to (full) CRIs, not
to CRI references: these need to be resolved relative to a base URI,
with results that may be equivalent or not depending on the base.

# Comparison

One of the most common operations on CRIs is comparison: determining
whether two CRIs are equivalent, without dereferencing the CRIs (i.e.,
using
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
retrieval of a representation, fragment components (if any) do not
play a role and typically are excluded from the comparison.


# CRI References

The most common usage of a Constrained Resource Identifier is to embed
it in resource representations, e.g., to express a hyperlink between the
represented resource and the resource identified by the CRI.

{{cbor-representation}} first defines the representation of CRIs in
[Concise Binary Object Representation (CBOR)](#STD94).
When reduced representation size is desired, CRIs are often not represented directly.
Instead, CRIs are indirectly referenced through *CRI references*.
These take advantage of hierarchical locality and provide a very compact
encoding.
The CBOR representation of CRI references also is specified in
{{cbor-representation}}.

The only operation defined on a CRI reference is *reference resolution*:
the act of transforming a CRI reference into a CRI.
<!-- , relative to a base URI -->
An application MUST implement this operation by applying
the algorithm specified in {{reference-resolution}} (or any algorithm
that is functionally equivalent to it).

The reverse operation of transforming a CRI into a CRI reference is
not specified in detail in this document;
implementations are free to use any algorithm as long as reference
resolution of the resulting CRI reference yields the original CRI.
Notably, a CRI reference is not required to satisfy all of the
constraints of a CRI; the only requirement on a CRI reference is that
reference resolution MUST yield the original CRI.

When testing for equivalence or difference, it is rarely appropriate
for applications to directly compare CRI references; instead, the
references are typically resolved to their respective CRI before
comparison.

## CBOR Representation {#cbor-representation}

[^replace-xxxx]

A CRI or CRI reference is encoded as a CBOR array (Major type 4 in
{{Section 3.1 of RFC8949@-cbor}}).
{{fig-railroad}} has a coarse visualization of the structure of this
array, without going into the details of the elements.

~~~ railroad-utf8
cri-reference = ((scheme authority) / discard) local-part

local-part = [path [query [fragment]]]
~~~
{: #fig-railroad title="Overall Structure of a CRI or CRI Reference"}

{{cddl}} has a more detailed description of the structure, in CDDL.

~~~~ cddl
{::include cddl/cri.cddl}
~~~~
{: #cddl title="CDDL for CRI CBOR representation"}

{:#discard1}
We call the elements of the top-level array *sections*.
The sections containing the rules `scheme`, `authority`, `path`, `query`, `fragment`
correspond to the components of a URI and thus of a CRI, as described in
{{constraints}}.
For use in CRI references, the `discard` section (see also {{discard}}) provides an
alternative to the `scheme` and `authority` sections.

{:#prose}
This CDDL specification is simplified for exposition and needs to be
augmented by the following rules for interchange of CRIs and CRI
references:

* Trailing default values ({{tbl-default}}) MUST be removed.
* Two leading null values (scheme and authority both not given) MUST
  be represented by using the `discard` alternative instead.
* An empty path in a `CRI` is represented as the empty array
  `[]`.
  Note that for `CRI-Reference` there is a difference between empty
  paths and paths that are not set, represented by `[]` and `null`, respectively.
* An empty query in a `CRI` (no query parameters, not even an empty
  string) is represented as the empty array
  `[]`; note that this is equivalent to the absence of the question
  mark in a URI, while the equivalent of just a question mark in a URI is
  an array with a single query parameter represented by an empty
  string `[""]`).
  Note that for `CRI-Reference` there is a difference between providing
  a query as above and a query that is not set, represented by `null`.
* An empty outer array (`[]`) is not a valid CRI.
  It is a valid CRI reference,
  equivalent to `[0]` as per {{ingest}}, which essentially copies the
  base CRI up to and including the path section, setting query and
  fragment to absent.

| Section   | Default Value |
|-----------|---------------|
| scheme    | –             |
| authority | `null`        |
| discard   | `0`           |
| path      | `[]`          |
| query     | `[]`          |
| fragment  | `null`        |
{:#tbl-default title="Default Values for CRI Sections"}

{:#no-indef}
For interchange as separate encoded data items, CRIs MUST NOT use
indefinite length encoding (see
{{Section 3.2 of RFC8949@-cbor}}).
This requirement is relaxed for
specifications that embed CRIs into an encompassing CBOR
representation that does provide for indefinite length encoding;
those specifications that are selective in where they provide for
indefinite length encoding are RECOMMENDED to not provide it for
embedded CRIs.

### `scheme-name` and `scheme-id` {#scheme-id}

In the scheme section, a CRI scheme can be given as a negative integer
`scheme-id` derived from the *scheme number*, or optionally by its
`scheme-name` (a text string giving the scheme name as in URIs' scheme
section, mapped to lower case).
(Note that, in {{cddl}}, `scheme-name` is marked as a feature, as only
less constrained CRI implementations might support `scheme-name`.)

Scheme numbers are unsigned integers that are mapped to and from URI
scheme names by the "CRI Scheme Numbers" registry ({{cri-reg}}).
The relationship of a scheme number to its `scheme-id` is as follows:

~~~ math
scheme\text{-}id = -1 - scheme\text{-}number
\\
scheme\text{-}number = -1 - scheme\text{-}id
~~~

For example, the scheme-name `coap` has the (unsigned integer)
scheme-number `0` which is represented in a (negative integer)
scheme-id `-1`.


### The `discard` Section

The `discard` section can be used in a CRI reference when neither a
scheme nor an authority is present.
It then expresses the operations performed on a base CRI by CRI references that
are equivalent to URI references with relative paths and path prefixes such as "/", "./", "../", "../../", etc.\\
"." and ".." are not available in CRIs and are therefore expressed
using `discard` after a normalization step, as is the presence or absence of a leading "/".

E.g., a simple URI reference "foo" specifies to remove one trailing
segment, if any,
from the base URI's path, which is represented in the equivalent CRI
reference discard section as the value `1`; similarly "../foo" removes
two trailing segments, if any, represented as `2`;
and "/foo" removes all segments, represented in the `discard` section as the value `true`.
The exact semantics of the section values are defined by
{{reference-resolution}}.

Most URI references that {{Section 4.2 of RFC3986@-uri}} calls "relative
references" (i.e., references that need to undergo a resolution
process to obtain a URI) correspond to the CRI reference form that starts with
`discard`.  The exception are relative references with an `authority`
(called a "network-path reference" in {{Section 4.2 of RFC3986@-uri}}), which
discard the entire path of the base CRI.
These CRI references never carry a `discard` section: the value of
`discard` defaults to `true`.


### Examples

~~~~ cbor-diag
[-1,             / scheme-id -- equivalent to "coap" /
 [h'C6336401',   / host /
  61616],        / port /
 [".well-known", / path /
  "core"]
]
~~~~
{: #fig-ex-1 title="CRI for coap://198.51.100.1:61616/.well-known/core"}

~~~~ cbor-diag
[true,                  / discard /
 [".well-known",        / path /
  "core"],
 ["rt=temperature-c"]  / query /
]
~~~~
{: #fig-ex-2 title="CRI Reference for /.well-known/core?rt=temperature-c"}

~~~~ cbor-diag
[-6,                / scheme-id -- equivalent to "did" /
 true,              / authority = NOAUTH-ROOTLESS /
 ["web:alice:bob"]  / path /
]
~~~~
{: #fig-ex-3 title="CRI for did:web:alice:bob"}

### Specific Terminology

A CRI reference is considered *well-formed* if it matches the
structure as expressed in {{cddl}} in CDDL, with the additional
requirement that trailing `null` values are removed from the array.

A CRI reference is considered a *full* CRI if it is well-formed
and the sequence of sections starts with a non-null `scheme`.

A CRI reference is considered *relative* if it is well-formed
and the sequence of sections is empty or starts with a section other
than those that would constitute a `scheme`.

## Ingesting and encoding a CRI Reference {#ingest}

From an abstract point of view, a CRI reference is a data structure
with six sections:

scheme, authority, discard, path, query, fragment

We refer to this as the *abstract form*, while the *interchange form* ({{cddl}}) has either
two sections for scheme and authority or one section for discard, but
never both of these alternatives.

Each of the sections in the abstract form can be _not set_ ("null"),
<!-- "not defined" in RFC 3986 -->
except for discard,
which is always an unsigned integer or `true`.  If scheme and/or
authority are non-null, discard is set to `true`.

When ingesting a CRI reference that is in interchange form, those
sections are filled in from interchange form (sections not set are
filled with null), and the following steps are performed:

* If the array is empty, replace it with `[0]`.
* If discard is present in interchange form (i.e., the outer array
  starts with true or an unsigned integer), set scheme and authority to null.
* If scheme and/or authority are present in interchange form (i.e.,
  the outer array starts with null, a text string, or a negative integer), set
  discard to `true`.

Upon encoding the abstract form into interchange form, the inverse
processing is performed:  If scheme and/or authority are not null, the
discard value is not transferred (it must be true in this case).  If
they are both null, they are both left out and only discard is
transferred.
Trailing null values are removed from the array.
As a special case, an empty array is sent in place for a remaining
`[0]` (URI reference "").

### Error handling and extensibility {#unprocessable}

It is recommended that specifications that describe the use of CRIs in CBOR-based protocols
use the error handling mechanisms outlined in this section.
Implementations of this document MUST adhere to these rules
unless a containing document overrides them.

When encountering a CRI that is well-formed in terms of CBOR, but that

* is not well-formed as a CRI,
* does not meet the other requirements on CRIs that are not covered by
  the term "well-formed", or
* uses features not supported by the implementation,

the CRI is treated as "unprocessable".

When encountering an unprocessable CRI,
the processor skips the entire CRI top-level array, including any CBOR
items contained in there,
and continues processing the CBOR items surrounding the unprocessable CRI.
(Note: this skipping can be implemented in bounded memory for CRIs
that do not use indefinite length encoding, as mandated in
{{cbor-representation}}.)

The unprocessable CRI is treated as an opaque identifier
that is distinct from all processable CRIs,
and distinct from all unprocessable CRIs with different CBOR representations.
It is up to the implementation whether unprocessable CRIs with identical representations
are treated as identical to each other or not.
Unprocessable CRIs cannot be dereferenced,
and it is an error to query any of their components.

This mechanism ensures that CRI extensions
(using originally defined features or later extensions)
can be used without extending the compatibility hazard to the containing document.
For example,
if a collection of possible interaction targets contains several CRIs,
some of which use the "no-authority" feature,
an application consuming that collection that does not support that
feature can still offer the supported interaction targets.

The duty of checking validity is with the recipients that rely on this
validity.
An intermediary that does not use the detailed information in a CRI
(or merely performs reference resolution) MAY pass on a CRI/CRI
reference without having fully checked it, relying on the producer
having generated a valid CRI/CRI reference.
This is true for both Simple CRIs (e.g., checking for valid UTF-8) and
for extensions (e.g., checking both for valid UTF-8 and the minimal
use of PET elements in the text-or-pet feature as per {{pet}}).

A system that is checking a CRI for some reason but is not its
ultimate recipient needs to consider the tension between security
requirements and the danger of ossification {{-use-lose}}: If the system rejects
anything that it does not know, it prevents the other components from
making use of extensions.
If it passes through extensions unknown to it, that might allow
semantics pass through that the system should have been designed to
filter out.

## Reference Resolution {#reference-resolution}

The term "relative" implies that a "base CRI" exists against which the
relative reference is applied. Aside from fragment-only references,
relative references are only usable when a base CRI is known.

The following steps define the process of resolving any well-formed CRI
reference against a base CRI so that the result is a full CRI in the form of
an CRI reference:

1. Establish the base CRI of the CRI reference (compare {{Section 5.1 of
   RFC3986@-uri}}) and express it in the form of an abstract (full) CRI
   reference.

2. Initialize a buffer with the sections from the base CRI.

3. If the value of discard is `true` in the CRI reference (which is
   implicitly the case when scheme and/or authority are present in the reference), replace the
   path in the buffer with the empty array, set query to empty and fragment
   to null, and set a `true` authority to `null`.  If the value of
   discard is an unsigned integer, remove as many elements
   from the end of the path array; if it is non-zero, set query to empty and
   fragment to null.

   Set discard to `true` in the buffer.

4. If the path section is non-null in the CRI reference, append all
   elements from the path array to the array in the path section in
   the buffer; set query to empty and fragment to null.

5. Apart from the path and discard, copy all non-null sections from
   the CRI reference to the buffer in sequence; set fragment to `null`
   in the buffer if query is non-null in the CRI reference.

6. Return the sections in the buffer as the resolved CRI.


# Relationship between CRIs, URIs, and IRIs

CRIs are meant to replace both [Uniform Resource Identifiers (URIs)](#STD66)
and [Internationalized Resource Identifiers (IRIs)](#RFC3987)
in constrained environments {{-term}}{{-termbis}}.
Applications in these environments may never need to use URIs and IRIs
directly, especially when the resource identifier is used simply for
identification purposes or when the CRI can be directly converted into a
CoAP request.

However, it may be necessary in other environments to determine the
associated URI or IRI of a CRI, and vice versa. Applications can perform
these conversions as follows:

{:vspace}
CRI to URI
: A CRI is converted to a URI as specified in {{cri-to-uri}}.

URI to CRI
: The method of converting a URI to a CRI is unspecified;
  implementations are free to use any algorithm as long as converting
  the resulting CRI back to a URI yields an equivalent URI.

  Note that CRIs are defined to enable implementing conversions from
  or to URIs analogously to processing URIs into CoAP Options and
  back, with the exception that item 8 of {{Section 6.4 of -coap}}
  and item 7 of {{Section 6.5 of -coap}} do not apply to CRI processing.
  See {{<sp-leading-empty}} in {{the-small-print}} for more details.

CRI to IRI
: {:#critoiri} A CRI can be converted to an IRI by first converting it to a URI as
  specified in {{cri-to-uri}}, and then converting the URI
  to an IRI as described in {{Section 3.2 of RFC3987}}.

IRI to CRI
: An IRI can be converted to a CRI by first converting it to a URI as
  described in {{Section 3.1 of RFC3987}}, and then
  converting the URI to a CRI as described above.

<!-- What? -->
Everything in this section also applies to CRI references, URI
references, and IRI references.


## Converting CRIs to URIs {#cri-to-uri}

Applications MUST convert a CRI reference to a URI
reference by determining the components of the URI reference according
to the following steps and then recomposing the components to a URI
reference string as specified in {{Section 5.3 of RFC3986@-uri}}.

{:vspace}
scheme
: If the CRI reference contains a `scheme` section, the scheme
  component of the URI reference consists of the value of that
  section, if text (`scheme-name`); or, if a negative integer is given
  (`scheme-id`), the lower case scheme name corresponding to the
  scheme-id as per {{scheme-id}}.
  Otherwise, the scheme component is not set.

authority
: If the CRI reference contains a `host-name` or `host-ip` item, the
  authority component of the URI reference consists of a host
  subcomponent, optionally followed by a colon (":") character and a
  port subcomponent, optionally preceded by a `userinfo` subcomponent.
  Otherwise, the authority component is not set.

  The host subcomponent consists of the value of the `host-name` or
  `host-ip` item.

  The `userinfo` subcomponent, if present, is turned into a single
  string by
  appending a "@".  Otherwise, both the subcomponent and the "@" sign
  are omitted.
  Any character in the value of the `userinfo` element that is not in
  the set of unreserved characters ({{Section 2.3 of RFC3986@-uri}}) or
  "sub-delims" ({{Section 2.2 of RFC3986@-uri}}) or a colon (":") MUST be
  percent-encoded.

  The `host-name` is turned into a single string by joining the
  elements separated by dots (".").
  Any character in the elements of a `host-name` item that is not in
  the set of unreserved characters ({{Section 2.3 of RFC3986@-uri}}) or
  "sub-delims" ({{Section 2.2 of RFC3986@-uri}}) MUST be
  percent-encoded.
  If there are dots (".") in such elements, the conversion fails
  (percent-encoding is not able to represent such elements, as
  normalization would turn the percent-encoding back to the unreserved
  character that a dot is.)

  {:aside}
  > Implementations with scheme-specific knowledge MAY convert
    individual elements by using the ToASCII procedure {{Section 4.1 of
    -toascii}} as discussed in more detail in {{Section 3.1 of -iri}}.
    This should not be done if the next step of conversion is to an
    IRI as defined in {{critoiri}} (CRI to IRI).

  {: #host-ip-to-uri}
  The value of a `host-ip` item MUST be
  represented as a string that matches the "IPv4address" or
  "IP-literal" rule ({{Section 3.2.2 of RFC3986@-uri}}).

  {: #zone-id-issue}
  Any zone-id is appended to the string; the details for how this is
  done are currently in flux in the URI specification: {{Section 2 of
  -zone}} uses percent-encoding and a separator of "%25", while
  proposals for a future superseding zone-id specification document
  (such as {{-zonebis}}) are being prepared; this also leads to a modified
  "IP-literal" rule as specified in these documents.
  While the discussion about the representation of zone-id information
  in URIs is ongoing, CRIs maintain a position in the grammar for it
  (`zone-id`).
  This can be used by consenting implementations to exchange zone
  information without being concerned by the ambiguity at the URI
  syntax level.
  The assumption is that the present specification (1) either will be
  updated eventually to obtain consistent URI conversion of zone-id
  information (2) or there will be no representation of zone-id
  information in URIs.

  If the CRI reference contains a `port` item, the port
  subcomponent consists of the value of that item in decimal
  notation.
  Otherwise, the colon (":") character and the port subcomponent are
  both omitted.

path
: If the CRI reference contains a `discard` item of value `true`, the
  path component is considered *rooted*.  If it
  contains a `discard` item of value `0` and the `path` item is
  present, the conversion fails.  If it contains a positive discard
  item, the path component is considered *unrooted* and
  prefixed by as many "../" components as the `discard` value minus
  one indicates.  If the discard value is `1` and the first element of
  the path contains a `:`, the path component is prefixed by "./"
  (this avoids the first element to appear as supplying a URI scheme;
  compare `path-noscheme` in {{Section 4.2 of RFC3986@-uri}}).
  {:#colon}

  If the discard item is not present and the CRI reference contains an
  authority that is `true`, the path component of the URI reference is
  considered unrooted.  Otherwise, the path component is considered
  rooted.

  If the CRI reference contains one or more `path` items, the path
  component is constructed by concatenating the sequence of
  representations of these items.  These representations generally
  contain a leading slash ("/") character and the value of each item,
  processed as discussed below.  The leading slash character is
  omitted for the first path item only if the path component is
  considered "unrooted".  <!-- A path segment that contains a colon
  character (e.g., --> <!-- "this:that") cannot directly be used as
  the first such item.  Such a --> <!-- segment MUST be preceded by a
  dot-segment (e.g., "./this:that") --> <!-- unless scheme and/or
  authority are present. -->

  Any character in the value of a `path` item that is not
  in the set of unreserved characters or "sub-delims" or a colon
  (":") or commercial at ("@") character MUST be
  percent-encoded.

  If the authority component is present (not `null` or `true`) and the
  path component does not match the "path-abempty" rule ({{Section 3.3
  of RFC3986@-uri}}), the conversion fails.

  If the authority component is not present, but the scheme component
  is, and the path component does not match the "path-absolute",
  "path-rootless" (authority == `true`) or "path-empty" rule ({{Section
  3.3 of RFC3986@-uri}}), the conversion fails.

  If neither the authority component nor the scheme component are
  present, and the path component does not match the "path-absolute",
  "path-noscheme" or "path-empty" rule ({{Section 3.3 of RFC3986@-uri}}), the
  conversion fails.

query
: If the CRI reference contains one or more `query` items,
  the query component of the URI reference consists of the value of
  each item, separated by an ampersand ("&") character.
  Otherwise, the query component is not set.

  Any character in the value of a `query` item that is not
  in the set of unreserved characters or "sub-delims" or a colon
  (":"), commercial at ("@"), slash ("/"), or question mark ("?")
  character MUST be percent-encoded.
  Additionally, any ampersand character ("&") in the item
  value MUST be percent-encoded.

fragment
: If the CRI reference contains a fragment item, the fragment
  component of the URI reference consists of the value of that
  item.
  Otherwise, the fragment component is not set.

  Any character in the value of a `fragment` item that is
  not in the set of unreserved characters or "sub-delims" or a colon
  (":"), commercial at ("@"), slash ("/"), or question mark ("?")
  character MUST be percent-encoded.

# Extending CRIs {#extending}

The CRI structure described up to this point, without enabling any
feature ("scheme-name", "no-authority", "userinfo"), is termed the
_Basic CRI_.
It should be sufficient for all applications that use the CoAP
protocol, as well as most other protocols employing URIs.

With one or more of the three features enabled, we speak of _Simple
CRIs_, which cover a larger subset of protocols that employ URIs.
To overcome remaining limitations, _Extended Forms_ of CRIs may be
defined to enable further applications.
They will generally extend the CRI structure to accommodate more potential
values of text components of URIs, such as userinfo, hostnames, paths,
queries, and fragments.

Extensions may also be defined to afford a more natural
representation of the information in a URI.
_Stand-in Items_ ({{stand-in}}) are one way to provide such
representations.
For instance, information that needs to be base64-encoded in a URI can
be represented in a CRI in its natural form as a byte string instead.

Extensions are or will be necessary to cover two limitations of
Simple CRIs:

* Simple CRIs do not support IPvFuture ({{Section 3.2.2 of RFC3986@-uri}}).
  Definition of such an extension probably best waits until a wider
  use of new IP literal formats is planned.
* More important in practice:

  Simple CRIs do not support URI components that *require*
  percent-encoding ({{Section 2.1 of RFC3986@-uri}}) to represent them
  in the URI syntax, except where that percent-encoding is used to
  escape the main delimiter in use.


  E.g., the URI

  ~~~ uri
  https://alice/3%2f4-inch
  ~~~

  is represented by the Basic CRI

  ~~~ coap-diag
  [-4, ["alice"], ["3/4-inch"]]
  ~~~

  However, percent-encoding that is used at the application level is not
  supported by Simple CRIs:

  ~~~ uri
  did:web:alice:7%3A1-balun
  ~~~

  CRIs have been designed to relieve implementations operating on CRIs
  from string scanning, which both helps constrained implementations and
  implementations that need to achieve high throughput.

  An extension supporting application-level percent-encoded text in
  CRIs is described in {{pet}}.

Consumers of CRIs will generally notice when an extended form is in
use, by finding structures that do not match the CDDL rules given in
{{cddl}}.
Future definitions of extended forms need to strive to be
distinguishable in their structures from the extended form presented
here as well as other future forms.

Extensions to CRIs are not intended to change encoding constraints;
e.g., {{no-indef}} is applicable to extended forms of CRIs as well.
This also ensures that recipients of CRIs can deal with unprocessable CRIs
as described in {{unprocessable}}.

## Extended CRI: Stand-In Items {#stand-in}

Application specifications that use CRIs may explicitly enable the use
of "stand-in" items (tags or simple values).
These are data items used in place of original representation items
such as strings or arrays, where the tag or simple value is defined to
stand for a data item that can be used in the position of the stand-in
item.
Examples would be (1) tags such as 21 to 23 ({{Section 3.4.5.2 of
RFC8949@-cbor}}) or 108 ({{Section 2.1 of -notable}}), which stand for text string components but internally
employ more compact byte string representations, or (2) reference tags and
simple values as defined in {{-packed}}.

Application specifications need to be explicit about which
stand-in items are allowed; otherwise, inconsistent interpretations at
different places in a system can lead to check/use vulnerabilities.

(Note that specifications that define CBOR tags may be employed in CRI
extensions without actually using the tags defined there as stand-in
tags; e.g., compare the way IP addresses are represented in Basic CRIs
with {{-ip}}.)

## Extended CRI: Accommodating Percent Encoding (PET) {#pet}

This section presents a method to represent percent-encoded segments
of userinfo, hostnames, paths, and queries, as well as fragments.

The four CDDL rules

~~~ cddl
userinfo    = (false, text .feature "userinfo")
host-name   = (*text)
path        = [*text]
query       = [*text]
fragment    = text
~~~

are replaced with

~~~ cddl
userinfo    = (false, text-or-pet .feature "userinfo")
host-name   = (*text-or-pet)
path        = [*text-or-pet]
query       = [*text-or-pet]
fragment    = text-or-pet

text-or-pet = text /
    text-pet-sequence .feature "text-or-pet"

; text1 and pet1 alternating, at least one pet1:
text-pet-sequence = [?text1, ((+(pet1, text1), ?pet1) // pet1)]
; pet is percent-encoded bytes
pet1 = bytes .ne ''
text1 = text .ne ""
~~~

That is, for each of the host-name, path, and query segments, and for
the userinfo and fragment components, an alternate representation is provided
besides a simple text string: a non-empty array of alternating non-blank text and byte
strings, the text strings of which stand for non-percent-encoded text,
while the byte strings retain the special
semantics of percent-encoded text without actually being
percent-encoded.

The abovementioned DID URI

~~~ uri
did:web:alice:7%3A1-balun
~~~

can now be represented as:

~~~ cbor-diag
[-6, true, [["web:alice:7", ':', "1-balun"]]]
~~~

(Note that, in CBOR diagnostic notation, single quotes delimit
literals for byte strings, double quotes for text strings.)

To yield a valid CRI using the `text-or-pet` feature, the use of byte
strings MUST be minimal.
Both the following examples are therefore not valid:

~~~ cbor-diag
[-6, true, [["web:alice:", '7:', "1-balun"]]]
~~~
~~~ cbor-diag
[-6, true, [["web:alice:7", ':1', "-balun"]]]
~~~

An algorithm for constructing a valid `text-pet-sequence` might
repeatedly examine the byte sequences in each byte string; if such a
sequence stands for an unreserved ASCII character, or constitutes a
valid UTF-8 character ≥ U+0080, move this character over into a text
string by appending it to the end of the preceding text string,
prepending it to the start of the following text string, or splitting
the byte string and inserting a new text string with this character,
all while preserving the order of the bytes.
(Note that the properties of UTF-8 make this a simple linear process;
working around the NFC constraint {{<c-nfc}} in this way may be more
complex.)

{:aside}
> Unlike the text elements of a path or a query, which through CoAP's
> heritage are designed to be processable element by element, a
> text-pet-sequence does not usually produce a semantically meaningful
> division into array elements.
> This consequence of the flexibility in delimiters offered in URIs is
> demonstrated by this example, which structurally singles out the one
> ':' that is *not* a delimiter at the application level.
> Applications specifically designed for using CRIs will generally
> avoid using the `text-or-pet` feature.
> Applications using existing URI structures that require
> text-pet-sequence elements for their representation typically need
> to process them byte by byte.

# Integration into CoAP and ACE

This section discusses ways in which CRIs can be used in the context
of the CoAP protocol {{-coap}} and of Authorization for Constrained
Environments (ACE), specifically the Authorization Information Format
(AIF) {{-aif}}.

## Converting Between CoAP CRIs and Sets of CoAP Options

This section provides an analogue to {{Sections 6.4 and 6.5 of -coap}}:
Computing a set of CoAP options from a request CRI ({{decompose-coap}}) and computing a
request CRI from a set of COAP options ({{compose-coap}}).

This section makes use of the mapping between CRI scheme numbers
and URI scheme names shown in {{scheme-map}}:

| CRI scheme number | URI scheme name |
|-------------------|-----------------|
|                 0 | coap            |
|                 1 | coaps           |
|                 6 | coap+tcp        |
|                 7 | coaps+tcp       |
|                24 | coap+ws         |
|                25 | coaps+ws        |
{: #scheme-map title="Mapping CRI scheme numbers and URI scheme names"}


### Decomposing a Request CRI into a set of CoAP Options {#decompose-coap}

   The steps to parse a request's options from a CRI »cri« are as
   follows.  These steps either result in zero or more of the Uri-Host,
   Uri-Port, Uri-Path, and Uri-Query Options being included in the
   request or they fail.

Where the following speaks of deriving a text-string for a CoAP Option
value from a data item in the CRI, the presence of any
`text-pet-sequence` subitem ({{pet}}) in this item fails this algorithm.

   1.  If »cri« is not a full CRI, then fail this algorithm.

   2.  Translate the scheme-id into a URI scheme name as per
       {{scheme-id}} and
       {{scheme-map}}; if a scheme-id that corresponds to a scheme
       number not in this list is being used, or if a scheme-name is
       being used,
       fail this algorithm.
       Remember the specific variant of CoAP to be used based on this
       URI scheme name.

   3.  If the »cri«'s `fragment` component is non-null, then fail this algorithm.

   4.  If the `host` component of »cri« is a `host-name`, include a
       Uri-Host Option and let that option's value be the text string
       values of the `host-name` elements joined by dots.

       If the `host` component of »cri« is a `host-ip`, check whether
       the IP address given represents the request's
       destination IP address (and, if present, zone-id).
       Only if it does not, include a Uri-Host Option, and let that
       option's value be the text value of the URI representation of
       the IP address, as derived in {{host-ip-to-uri}}.

   5.  If the `port` subcomponent in a »cri« is not absent, then let »port« be that
       subcomponent's unsigned integer value; otherwise, let »port« be
       the default port number for the scheme.

   6.  If »port« does not equal the request's destination port,
       include a Uri-Port Option and let that option's value be »port«.

   7.  If the value of the `path` component of »cri« is empty or
       consists of a single empty string, then move to the next step.

       Otherwise, for each element in the »path« component, include a
       Uri-Path Option and let that option's value be the text string
       value of that element.

   8.  If the value of the `query` component of »cri« is non-empty,
       then, for each element in the `query` component, include a
       Uri-Query Option and let that option's value be the text string
       value of that element.

### Composing a Request CRI from a Set of CoAP Options {#compose-coap}

   The steps to construct a CRI from a request's options are as follows.
   These steps either result in a CRI or they fail.


   1.   Based on the variant of CoAP used in the request, choose a
        `scheme-id` as per {{scheme-id}} and table {{scheme-map}}.  Use
        that as the first value in the resulting CRI array.

   2.   If the request includes a Uri-Host Option, insert an
        `authority` with its value determined as follows:
        If the value of the Uri-Host Option is a `reg-name`, split it
        on any dots in the name and use the resulting text string
        values as the elements of the `host-name` array.
        If the value is an IP-literal or IPv4address, extract any
        `zone-id`, and represent the IP address as a byte string of
        the correct length in `host-ip`, followed by any `zone-id`
        extracted if present.
        If the value is none of the three, fail this algorithm.

        If the request does not include a Uri-Host Option, insert an
        `authority` with `host-ip` being the byte string that
        represents the request's destination IP address and,
        if one is present in the request's destination, add a `zone-id`.

   3.   If the request includes a Uri-Port Option, let »port« be that
        option's value.  Otherwise, let »port« be the request's
        destination port.
        If »port« is not the default port for the scheme, then insert
        the integer value of »port« as the value of `port` in the
        authority.
        Otherwise, elide the `port`.

   4.   Insert a `path` component that contains an array built from
        the text string values of the Uri-Path Options in the request,
        or an empty array if no such options are present.

   5.   Insert a `query` component that contains an array built from
        the text string values of the Uri-Query Options in the request,
        or an empty array if no such options are present.


## CoAP Options for Forward-Proxies {#coap-options}

Apart from the above procedures to convert CoAP CRIs to and from sets
of CoAP Options, two additional CoAP Options are defined in {{Section
5.10.2 of -coap}} that support requests to forward-proxies:

* Proxy-Uri, and
* its more lightweight variant, Proxy-Scheme

This section defines analogues of these that employ CRIs and the URI
Scheme numbering provided by the present specification.

### Proxy-CRI

   | No.    | C | U | N | R | Name         | Format | Length | Default |
   | TBD235 | x | x | - |   | Proxy-Cri    | opaque | 1-1023 | (none)  |
{: #tab-proxy-cri title="Proxy-Cri CoAP Option"}

The Proxy-CRI Option carries an encoded CBOR data item that represents
a full CRI.
It is used analogously to Proxy-Uri as defined in {{Section 5.10.2
of -coap}}.
The Proxy-Cri Option MUST take precedence over any of the Uri-Host,
Uri-Port, Uri-Path or Uri-Query options, as well as over any
Proxy-Uri Option (each of which MUST NOT be
included in a request containing the Proxy-Cri Option).


### Proxy-Scheme-Number


   | No.    | C | U | N | R | Name                | Format | Length | Default |
   | TBD239 | x | x | - |   | Proxy-Scheme-Number | uint   |    0-3 | (none)  |
{: #tab-proxy-scheme-number title="Proxy-Scheme-Number CoAP Option"}

The Proxy-Scheme-Number Option carries a CRI Scheme Number represented as a
CoAP unsigned integer.
It is used analogously to Proxy-Scheme as defined in {{Section 5.10.2
of -coap}}.

The Proxy-Scheme Option MUST NOT be included in a request that also
contains the Proxy-Scheme-Number Option; servers MUST reject the
request if this is the case.

As per {{Section 3.2 of -coap}}, CoAP Options are only defined as one of empty, (text) string,
opaque (byte string), or uint (unsigned integer).
The Option therefore carries an
unsigned integer that represents the CRI scheme-number (which relates to
a CRI scheme-id as defined in {{scheme-id}}).
For instance, the scheme name "coap" has the scheme-number 0 and is
represented as an unsigned integer by a zero-length CoAP Option value.

## ACE AIF {#toid}

The AIF (Authorization Information Format, {{-aif}}) defined by ACE by
default uses the local part of a URI to identify a resource for which
authorization is indicated.
The type and target of this information is an extension point, briefly
called *Toid* (Type of object identifier).
{{toidreg}} registers "CRI-local-part" as a Toid.
Together with *Tperm*, an extension point for a way to indicate
individual access rights (permissions), {{Section 2 of -aif}}
defines its general Information Model as:

~~~ cddl
AIF-Generic<Toid, Tperm> = [* [Toid, Tperm]]
~~~

Using the definitions in {{cddl}} together with the {{-aif}} default Tperm
choice `REST-method-set`, this information model can be specialized as
in:

~~~ cddl
CRI-local-part = [path, ?query]
AIF-CRI = AIF-Generic<CRI-local-part, REST-method-set>
~~~

<!-- cddlc -irfc9237 -sAIF-CRI -r2u -tcddl - -->

# Implementation Status {#impl}

{::boilerplate rfc7942info}

A golang implementation of revision -10 of this document is found at:
`https://github.com/thomas-fossati/href`.
A Rust implementation is available at `https://codeberg.org/chrysn/cri-ref`;
it is being updated to revision -18 at the time of writing.
A python implementation is available as part of `https://gitlab.com/chrysn/micrurus`
but is based on revision -05.

# Security Considerations {#security}

Parsers of CRI references must operate on input that is assumed to be
untrusted. This means that parsers MUST fail gracefully
in the face of malicious inputs.
Additionally, parsers MUST be prepared to deal with
resource exhaustion (e.g., resulting from the allocation of big data
items) or exhaustion of the call stack (stack overflow).
See {{Section 10 of RFC8949@-cbor}} for additional
security considerations relating to CBOR.

The security considerations discussed in {{Section 7 of RFC3986@-uri}} and
{{Section 8 of RFC3987}} for URIs and IRIs also apply to CRIs.
The security considerations discussed for URIs in {{Section 6 of -aif}}
apply analogously to AIF-CRI {{toid}}.

# IANA Considerations

[^removenumbers]

[^removenumbers]: RFC-editor: Please replace all references to
    {{sec-numbers}} by a reference to the IANA registry.

## CRI Scheme Numbers Registry {#cri-reg}

This specification defines a new "CRI Scheme Numbers" registry in the
"Constrained RESTful Environments (CoRE) Parameters" registry group
{{IANA.core-parameters}}, with the policy "Expert Review" ({{Section 4.5
of RFC8126@-ianacons}}).
The objective is to have CRI scheme number values registered for all
registered URI schemes (Uniform Resource Identifier (URI) Schemes
registry), as well as exceptionally for certain text strings that the
Designated Expert considers widely used in constrained applications in
place of URI scheme names.

### Instructions for the Designated Expert {#de-instructions}

The expert is instructed to be frugal in the allocation of CRI scheme
number values whose scheme-id values ({{scheme-id}}) have short
representations (1+0 and 1+1 encoding), keeping them in
reserve for applications that are likely to enjoy wide use and can
make good use of their shortness.

When the expert notices that a registration has been made in the
Uniform Resource Identifier (URI) Schemes registry (see also {{upd}}),
the expert is requested to initiate a parallel registration in the CRI
Scheme Numbers registry.
CRI scheme number values in the range between 1000 and
20000 (inclusive) should be assigned unless a shorter representation
in CRIs appears desirable.

The expert exceptionally also may make such a registration for text
strings that have not been registered in the Uniform Resource
Identifier (URI) Schemes registry if and only if the expert considers
them to be in wide use in place of URI scheme names in constrained
applications.
(Note that registrations in the CRI Scheme Numbers registry are
oblivious to the details of any URI Schemes registry registration, so
if a registration is later made in the URI Schemes registry that uses
such a previously unregistered text string as a name, the CRI Scheme
Numbers registration simply stays in place, even if the URI Schemes
registration happens to be for something different from what the
expert had in mind at the time for the CRI Scheme Numbers
registration.
Also note that the initial registrations in {{tab-numbers}} in
{{sec-numbers}} already include such registrations for the text strings
"mqtt" and "mqtts".)

A registration in the CRI Scheme Numbers registry does not imply that
a URI scheme under this name exists or has been registered in the
Uniform Resource Identifier (URI) Schemes registry -- it essentially
is only providing an integer identifier for an otherwise uninterpreted
text string.

Any questions or issues that might interest a wider audience might be
raised by the expert on the core-parameters@ietf.org mailing list for
a time-limited discussion.

### Structure of Entries

Each entry in the registry must include:

{:vspace}
CRI scheme number:
: An unsigned integer unique in this registry

URI scheme name:
: a text string that would be acceptable for registration as a URI
  Scheme Name in the Uniform Resource Identifier (URI) Schemes
  registry

Reference:
: a reference to a document, if available, or the registrant

The Reference field can simply be a copy of the reference field for the
URI-Scheme registration if that exists.
If not, it can contain helpful information (including the name of the
registrant) that may be available for the registration, with the
expectation that this will be updated if a URI-Scheme registration
under that URI scheme name is later made.

### Initial Registrations

The initial registrations for the CRI Scheme Numbers registry are
provided in {{tab-numbers}} in {{sec-numbers}}.


## Update to "Uniform Resource Identifier (URI) Schemes" Registry {#upd}

{{RFC7595@-schemes}} is updated to add the following note in the "Uniform
Resource Identifier (URI) Schemes" Registry {{IANA.uri-schemes}}:

{:quote}
>
The CRI Scheme Numbers Registry registers numeric identifiers for what
essentially are URI Scheme names.
Registrants for the Uniform Resource Identifier (URI) Schemes Registry
are requested to make a parallel registration in the CRI Scheme
Numbers registry.
The number for this registration will be assigned by the Designated
Expert for that registry.


## CBOR Diagnostic Notation Application-extension Identifiers Registry {#cri-iana}

In the "Application-Extension Identifiers" registry in the "CBOR
Diagnostic Notation" registry group \[IANA.cbor-diagnostic-notation],
IANA is requested to register the application-extension identifier
`cri` as described in {{tab-iana}} and defined in {{edn-cri}}.

| Application-extension Identifier | Description                     | Change Controller | Reference         |
|----------------------------------|---------------------------------|-------------------|-------------------|
| cri                              | Constrained Resource Identifier | IETF              | RFC-XXXX, {{edn-cri}} |
{: #tab-iana title="CBOR Extended Diagnostic Notation (EDN) Application-extension Identifier for CRI"}

[^replace-xxxx]

## CBOR Tags Registry {#tags-iana}

[^cpa]

[^cpa]: RFC-Editor: This document uses the CPA (code point allocation)
      convention described in [I-D.bormann-cbor-draft-numbers].  For
      each usage of the term "CPA", please remove the prefix "CPA"
      from the indicated value and replace the residue with the value
      assigned by IANA; perform an analogous substitution for all other
      occurrences of the prefix "CPA" in the document.  Finally,
      please remove this note.

In the "CBOR Tags" registry {{-tags}}, IANA is requested to assign the
tags in {{tab-tag-values}} from the "specification required" space
(suggested assignment: 99), with the present document as the
specification reference.

| Tag   | Data Item | Semantics                                            | Reference |
| CPA99 | array     | CRI Reference | RFC-XXXX  |
{: #tab-tag-values cols='r l l' title="Values for Tags"}



## CoAP Option Numbers Registry

In the "CoAP Option Numbers" registry in the "CoRE Parameters" registry group [IANA.core-parameters],
IANA is requested to register the CoAP Option Numbers
as described in {{tab-iana-options}} and defined in {{coap-options}}.

   | No.    | Name                | Reference |
   | TBD235 | Proxy-Cri           | RFC-XXXX  |
   | TBD239 | Proxy-Scheme-Number | RFC-XXXX  |
{: #tab-iana-options title="New CoAP Option Numbers"}

[^replace-xxxx]

## Media-Type subparameters for ACE AIF {#toidreg}

In the "Sub-Parameter Registry for application/aif+cbor and
application/aif+json" in the "Media Type Sub-Parameter Registries"
registry group {{IANA.media-type-sub-parameters}}, IANA is requested to
register:

| Parameter | Name           | Description/Specification | Reference           |
|-----------|----------------|---------------------------|---------------------|
| Toid      | CRI-local-part | local-part of CRI         | {{toid}} of RFC-XXXX  |
{: #tab-iana-toid title="ACE AIF Toid for CRI"}


[^replace-xxxx]


## Content-Format for CRI in AIF

IANA is requested to register a Content-Format identifier in the "CoAP
Content-Formats" registry (range 256-999), within the "Constrained
RESTful Environments (CoRE) Parameters" registry group
[IANA.core-parameters], as follows:

| Content Type                             | Content Coding | ID  | Reference |
| application/aif+cbor;Toid=CRI-local-part | -              | TBD | RFC-XXXX  |
{: #tab-iana-toid-ct title="Content-Format for ACE AIF with CRI-local-part Toid"}

[^replace-xxxx]


--- back

# The Small Print

{:sp: type="SP%d." group="SP"}

This appendix lists a few corner cases of URI semantics that
implementers of CRIs need to be aware of, but that are not
representative of the normal operation of CRIs.

{:sp}
1. {:#sp-leading-empty} Initial (Lone/Leading) Empty Path Segments:

  * *Lone empty path segments:*
  As per {{-uri}}, `s://x` is distinct from `s://x/` -- i.e., a URI
  with an empty path (`[]` in CRI) is different from one with a lone
  empty path segment (`[""]`).
  However, in HTTP and CoAP, they are implicitly aliased (for CoAP, in
  item 8 of {{Section 6.4 of -coap}}).
  As per item 7 of {{Section 6.5 of -coap}}, recomposition of a URI
  without Uri-Path Options from the other URI-related CoAP Options
  produces `s://x/`, not `s://x` -- CoAP prefers the lone empty path
  segment form.
  Similarly, after discussing HTTP semantics, {{Section 6.2.3 of RFC3986@-uri}} states:

  {:quote}
  > In general, a URI that uses the generic syntax for authority with an
  empty path should be normalized to a path of "/".

  * *Leading empty path segments without authority*:
  Somewhat related, note also that URIs and URI references that do not
  carry an authority cannot represent leading empty path segments
  (i.e., that are followed by further path segments): `s://x//foo`
  works, but in a `s://foo` URI or an (absolute-path) URI reference of
  the form `//foo` the double slash would be mis-parsed as leading in
  to an authority.

{:sp}
2. {:#sp-constraints} Constraints ({{constraints}}) of CRIs/basic CRIs

   While most URIs in everyday use can be converted to CRIs and back to URIs
   matching the input after syntax-based normalization of the URI,
   these URIs illustrate the constraints by example:

   * `https://host%ffname`, `https://example.com/x?data=%ff`

     All URI components must, after percent decoding, be valid UTF-8 encoded text.
     Bytes that are not valid UTF-8 show up, for example, in BitTorrent web seeds.
     <!-- <https://www.bittorrent.org/beps/bep_0017.html>, not sure this warrants an informative reference -->

     These URIs can be expressed when using the `text-or-pet` feature.

   * `https://example.com/component%3bone;component%3btwo`, `http://example.com/component%3dequals`

     While delimiters can be used in an escaped and unescaped form in URIs with generally distinct meanings,
     basic CRIs (i.e., without percent-encoded text {{pet}}) only support one escapable delimiter character per component,
     which is the delimiter by which the component is split up in the CRI.

     Note that the separators `.` (for authority parts), `/` (for paths), `&` (for query parameters)
     are special in that they are syntactic delimiters of their
     respective components in CRIs (note that `.` is doubly special
     because it is not a `reserved` character in {{-uri}} and therefore
     any percent-encoding would be normalized away).

     Thus, the following examples *are* convertible to basic CRIs without the `text-or-pet` feature:

     `https://example.com/path%2fcomponent/second-component`

     `https://example.com/x?ampersand=%26&questionmark=?`

   * `https://alice@example.com/`

     The user information can be expressed in CRIs if the "userinfo"
     feature is present.  The URI `https://@example.com` is
     represented as `[-4, [false, "", "example", "com"]]`; the `false`
     serves as a marker that the next element is the userinfo.

     The rules explicitly cater for unencoded ":" in userinfo (without
     needing the `text-or-pet` feature).
     (We opted for including this syntactic feature instead of
     disabling it as a mechanism against potential uses of colons for
     the deprecated inclusion of unencrypted secrets.)

# CBOR Extended Diagnostic Notation (EDN): The "cri" Extension {#edn-cri}

{{-edn}} more rigorously defines and further extends the CBOR Extended
Diagnostic Notation (EDN), as originally introduced in {{Section 8 of
RFC8949@-cbor}} and extended in {{Appendix G of -cddl}}.
Among others, it provides an extension point for
"application-extension identifiers" that can be used to notate CBOR
data items in application-specific ways.

The present document defines and registers ({{cri-iana}}) the
application-extension identifier "`cri`", which can be used to notate
an EDN literal for a CRI reference as defined in this document.

The text of the literal is a URI Reference as per {{-uri}} or an IRI
Reference as per {{-iri}}.

The value of the literal is a CRI reference that can be converted to
the text of the literal using the procedure of {{cri-to-uri}}.
Note that there may be more than one CRI reference that can be
converted to the URI/IRI reference given; implementations are expected
to favor the simplest variant available and make non-surprising
choices otherwise.
In the all-upper-case variant of the app-prefix, the value is enclosed
in a tag number CPA99.

[^cpa]

As an example, the CBOR diagnostic notation

~~~ cbor-diag
cri'https://example.com/bottarga/shaved'
CRI'https://example.com/bottarga/shaved'
~~~

is equivalent to

~~~ cbor-diag
[-4, ["example", "com"], ["bottarga", "shaved"]]
CPA99([-4, ["example", "com"], ["bottarga", "shaved"]])
~~~

See {{cri-grammar}} for an ABNF definition for the content of `cri` literals.


## cri: ABNF Definition of URI Representation of a CRI {#cri-grammar}

It can be expected that implementations of the application-extension
identifier "`cri`" will make use of platform-provided URI
implementations, which will include a URI parser.

In case such a URI parser is not available or inconvenient to
integrate,
a grammar of the content of `cri` literals is provided by the
ABNF for `URI-reference` in {{Section 4.1 of RFC3986@-uri}} with certain
re-arrangements taken from {{figure-5 (Figure 5)<I-D.ietf-cbor-edn-literals}} of {{I-D.ietf-cbor-edn-literals}};
these are reproduced in {{abnf-grammar-cri}}.
If the content is not ASCII only (i.e., for IRIs), first apply
{{Section 3.1 of RFC3987}} and apply this grammar to the result.

~~~ abnf
app-string-cri = URI-reference
; ABNF from RFC 3986:

URI           = scheme ":" hier-part [ "?" query ] [ "#" fragment ]

hier-part     = "//" authority path-abempty
                 / path-absolute
                 / path-rootless
                 / path-empty

URI-reference = URI / relative-ref

absolute-URI  = scheme ":" hier-part [ "?" query ]

relative-ref  = relative-part [ "?" query ] [ "#" fragment ]

relative-part = "//" authority path-abempty
                 / path-absolute
                 / path-noscheme
                 / path-empty

scheme        = ALPHA *( ALPHA / DIGIT / "+" / "-" / "." )

authority     = [ userinfo "@" ] host [ ":" port ]
userinfo      = *( unreserved / pct-encoded / sub-delims / ":" )
host          = IP-literal / IPv4address / reg-name
port          = *DIGIT

IP-literal    = "[" ( IPv6address / IPvFuture  ) "]"

IPvFuture     = "v" 1*HEXDIG "." 1*( unreserved / sub-delims / ":" )

; Use IPv6address, h16, ls32, IPv4adress, dec-octet as re-arranged
; for PEG Compatibility in Figure 5 of [I-D.ietf-cbor-edn-literals]:

IPv6address   =                            6( h16 ":" ) ls32
              /                       "::" 5( h16 ":" ) ls32
              / [ h16               ] "::" 4( h16 ":" ) ls32
              / [ h16 *1( ":" h16 ) ] "::" 3( h16 ":" ) ls32
              / [ h16 *2( ":" h16 ) ] "::" 2( h16 ":" ) ls32
              / [ h16 *3( ":" h16 ) ] "::"    h16 ":"   ls32
              / [ h16 *4( ":" h16 ) ] "::"              ls32
              / [ h16 *5( ":" h16 ) ] "::"              h16
              / [ h16 *6( ":" h16 ) ] "::"

h16           = 1*4HEXDIG
ls32          = ( h16 ":" h16 ) / IPv4address
IPv4address   = dec-octet "." dec-octet "." dec-octet "." dec-octet
dec-octet     = "25" %x30-35         ; 250-255
              / "2" %x30-34 DIGIT    ; 200-249
              / "1" 2DIGIT           ; 100-199
              / %x31-39 DIGIT        ; 10-99
              / DIGIT                ; 0-9
ALPHA         = %x41-5a / %x61-7a
DIGIT         = %x30-39
HEXDIG        = DIGIT / "A" / "B" / "C" / "D" / "E" / "F"
; case insensitive matching, i.e., including lower case

reg-name      = *( unreserved / pct-encoded / sub-delims )

path          = path-abempty    ; begins with "/" or is empty
                 / path-absolute   ; begins with "/" but not "//"
                 / path-noscheme   ; begins with a non-colon segment
                 / path-rootless   ; begins with a segment
                 / path-empty      ; zero characters

path-abempty  = *( "/" segment )
path-absolute = "/" [ segment-nz *( "/" segment ) ]
path-noscheme = segment-nz-nc *( "/" segment )
path-rootless = segment-nz *( "/" segment )
path-empty    = 0<pchar>

segment       = *pchar
segment-nz    = 1*pchar
segment-nz-nc = 1*( unreserved / pct-encoded / sub-delims / "@" )
                 ; non-zero-length segment without any colon ":"

pchar         = unreserved / pct-encoded / sub-delims / ":" / "@"

query         = *( pchar / "/" / "?" )

fragment      = *( pchar / "/" / "?" )

pct-encoded   = "%" HEXDIG HEXDIG

unreserved    = ALPHA / DIGIT / "-" / "." / "_" / "~"
reserved      = gen-delims / sub-delims
gen-delims    = ":" / "/" / "?" / "#" / "[" / "]" / "@"
sub-delims    = "!" / "$" / "&" / "'" / "(" / ")"
                 / "*" / "+" / "," / ";" / "="
~~~
{: #abnf-grammar-cri sourcecode-name="cbor-edn-cri.abnf"
title="ABNF Definition of URI Representation of a CRI"
}


# Mapping Scheme Numbers to Scheme Names {#sec-numbers}
{:removeinrfc}

[^replace-xxxx]

{{tab-numbers}} defines the initial mapping from CRI scheme numbers to
URI scheme names.

{::include code/schemes-numbers.md}
{: #tab-numbers title="Mapping Scheme Numbers to Scheme Names"}

The assignments from this table can be extracted from the XML form of
this document (when stored in a file "this.xml") into CSV form
{{?RFC4180}} using this short Ruby program:

~~~ ruby
{::include code/extract-schemes-numbers.rb}
~~~


# Change Log
{:removeinrfc}

Changes from -16 to -17

(Provisional integration of active PRs, please see github.)

Changes from -15 to -16

* Add note that CRI Scheme Number registrations are oblivious of the
  actual URI Scheme registrations (if any).

* Add information about how this RFC updates {{RFC7595}} to abstract and
  introduction.

Changes from -14 to -15

* Make scheme numbers unsigned and map them to negative numbers used
  as scheme-id values

Changes from -09 to -14

* Editorial changes; move some examples to {{the-small-print}}, break up
  railroad diagram; mention commonalities with (and tiny difference
  from) CoAP Options; mention failure of percent-encoding for dots in
  host-name components

* Explicitly mention invalid case in {{naked-rootless}} (rootless CRIs without
  authority that do not have a path component)

* Generalize {{extending}}, discuss PET (percent-encoded text) extension in more detail

* Add registry of URI scheme numbers ({{sec-numbers}}, {{iana-considerations}})

* Add user information to the authority ("userinfo" feature)

* {{cddl}}: Use separate rule for CRI, allow `[]` for query in CRI
  Reference; generalize scheme numbers, add userinfo; add list of
  additional requirements in prose ({{prose}})

* Discuss {{<<unprocessable}} ({{unprocessable}})

* Conversion to URI: Handle `:` in first pathname component of a
  CRI-Reference ({{colon}})

* Add Christian Amsüss as contributor

* Add CBOR EDN application-extension "`cri`" (see {{edn-cri}} and
  {{cri-iana}}).

* Add Section on CoAP integration (and new CoAP Options Proxy-Cri and
  Proxy-Scheme-Number).

Changes from -08 to -09

* Identify more esoteric features with a CDDL ".feature".

* Clarify that well-formedness requires removing trailing nulls.

* Fragments can contain PET.

* Percent-encoded text in PET is treated as byte strings.

* URIs with an authority but a completely empty path (e.g.,
  `http://example.com`): CRIs with an authority component no longer
  always produce at least a slash in the path component.

  For generic schemes, the conversion of `scheme://example.com` to a
  CRI is now possible
  because CRI produces a URI with an authority not followed by a slash
  following the updated rules of {{cri-to-uri}}.
  Schemes like http and coap do not distinguish between the empty path
  and the path containing a single slash when an authority is set (as
  recommended in {{STD66}}).
  For these schemes, that equivalence allows implementations to
  convert the just-a-slash URI to a CRI with a zero length path array
  (which, however, when converted back, does not produce a slash after
  the authority).

  (Add an appendix "the small print" for more detailed discussion of
  pesky corner cases like this.)

Changes from -07 to -08

* Fix the encoding of NOAUTH-NOSLASH / NOAUTH-LEADINGSLASH

* Add URN and DID schemes, add example.

* Add PET

* Remove hopeless attempt to encode "remote trailing nulls" rule in
  CDDL (which is not a transformation language).

Changes from -06 to -07

* More explicitly discuss constraints ({{constraints}}), add examples ({{sp-constraints}}).

* Make CDDL more explicit about special simple values.

* Lots of gratuitous changes from XML2RFC redefinition of `<tt>`
  semantics.

Changes from -05 to -06

* rework authority:
  * split reg-names at dots;
  * add optional zone identifiers {{-zone}} to IP addresses

Changes from -04 to -05

* Simplify CBOR structure.

* Add implementation status section.

Changes from -03 to -04:

* Minor editorial improvements.

* Renamed path.type/path-type to discard.

* Renamed option to section, substructured into items.

* Simplified the table "resolution-variables".

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

CRIs were developed by {{{Klaus Hartke}}} for use in the Constrained
RESTful Application Language (CoRAL).
The current author team is completing this work with a view to achieve
good integration with the potential use cases, both inside and outside of CoRAL.

Thanks to
{{{Christian Amsüss}}},
{{{Thomas Fossati}}},
{{{Ari Keränen}}},
{{{Jim Schaad}}},
{{{Dave Thaler}}},
and
{{{Marco Tiloca}}}
for helpful comments and discussions that have shaped the
document.


<!--  LocalWords:  CRI normalizations dereferencing dereference CRIs
 -->
<!--  LocalWords:  untrusted subcomponent
 -->
