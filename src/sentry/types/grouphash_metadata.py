from __future__ import annotations

from typing import NotRequired, TypedDict

# NOTE: The structure in these metadata types is intentionaly flat, to make it easier to query in
# Redash or BigQuery, and they are all merged into a single flat JSON blob (which is then stored in
# `GroupHashMetadata.hashing_metadata`). Therefore, if entries are added, they should be namespaced
# according to their corresponding hash basis (so, for example, `fingerprint_source` and
# `message_source`, rather than just `source`), both for clarity and to avoid collisions.


class FingerprintHashingMetadata(TypedDict):
    """
    Fingerprint data, gathered both during stand-alone custom/built-in fingerprinting and hybrid
    fingerprinting involving message, stacktrace, security, or template hashing
    """

    # The fingerprint value
    fingerprint: str
    # Either "client", "server_builtin_rule", or "server_custom_rule". (We don't have a "none of the
    # above" option here because we only record fingerprint metadata in cases where there's some
    # sort of custom fingerprint.)
    fingerprint_source: str
    # The fingerprint value set in the SDK, if anything other than ["{{ default }}"]. Note that just
    # because this is set doesn't mean we necessarily used it for grouping, since server-side rules
    # take precedence over client fingerprints. See `fingerprint_source` above.
    client_fingerprint: NotRequired[str]
    # The server-side rule applied, if any
    matched_fingerprinting_rule: NotRequired[str]
    # Whether or not a hybrid fingerprint (one involving both the signal value `{{ default }}` and a
    # custom value) was used. In that case, we group as we normally would, but then split the events
    # into more granular groups based on the custom value.
    is_hybrid_fingerprint: bool


class MessageHashingMetadata(TypedDict):
    """
    Data gathered when an event is grouped by log message or error type and value
    """

    # Either "message" (from "message" or "logentry") or "exception" (error type and value, in cases
    # where there's no stacktrace)
    message_source: str
    # Whether we've done any parameterization of the message, such as replacing a number with "<int>"
    message_parameterized: bool


class SaltedMessageHashingMetadata(MessageHashingMetadata, FingerprintHashingMetadata):
    """
    Data from message-based bybrid fingerprinting
    """

    pass


class StacktraceHashingMetadata(TypedDict):
    """
    Data gathered when an event is grouped based on a stacktrace found in an exception, a thread, or
    diretly in the event
    """

    # Either "in-app" or "system"
    stacktrace_type: str
    # Where in the event data the stacktrace was found - either "exception", "thread", or
    # "top-level"
    stacktrace_location: str
    # The number of stacktraces used for grouping (will be more than 1 in cases of chained
    # exceptions)
    num_stacktraces: int


class SaltedStacktraceHashingMetadata(StacktraceHashingMetadata, FingerprintHashingMetadata):
    """
    Data from stacktrace-based bybrid fingerprinting
    """

    pass


class SecurityHashingMetadata(TypedDict):
    """
    Data gathered when grouping browser-based security (Content Security Policy, Certifcate
    Transparency, Online Certificate Status Protocol Stapling, or HTTP Public Key Pinning) reports
    """

    # Either "csp", "expect-ct", "expect-staple", or "hpkp"
    security_report_type: str
    # Domain name of the blocked address
    blocked_host: str
    # The CSP directive which was violated
    csp_directive: NotRequired[str]
    # In the case of a local `script-src` violation, whether it's an `unsafe-inline` or an
    # `unsafe-eval` violation
    csp_script_violation: NotRequired[str]


class SaltedSecurityHashingMetadata(SecurityHashingMetadata, FingerprintHashingMetadata):
    """
    Data from security-report-based bybrid fingerprinting
    """

    pass


class TemplateHashingMetadata(TypedDict):
    """
    Data gathered when grouping errors generated by Django templates
    """

    # The name of the template with the invalid template variable
    template_name: NotRequired[str]
    # The text of the line in the template containing the invalid variable
    template_context_line: NotRequired[str]


class SaltedTemplateHashingMetadata(TemplateHashingMetadata, FingerprintHashingMetadata):
    """
    Data from template-based bybrid fingerprinting
    """

    pass


class ChecksumHashingMetadata(TypedDict):
    """
    Data gathered when legacy checksum grouping (wherein a hash is provided directly in the event)
    is used
    """

    # The checksum used for grouping
    checksum: str
    # The incoming checksum value, if it was something other than a 32-digit hex value and we
    # therefore had to hash it before using it
    raw_checksum: NotRequired[str]


class FallbackHashingMetadata(TypedDict):
    """
    Data gathered when no other grouping method produces results
    """

    # Whether we landed in the fallback because of a lack of data, because we had a stacktrace but
    # all frames were ignored, or some other reason
    fallback_reason: str


HashingMetadata = (
    FingerprintHashingMetadata
    | MessageHashingMetadata
    | SaltedMessageHashingMetadata
    | StacktraceHashingMetadata
    | SaltedStacktraceHashingMetadata
    | SecurityHashingMetadata
    | SaltedSecurityHashingMetadata
    | TemplateHashingMetadata
    | SaltedTemplateHashingMetadata
    | ChecksumHashingMetadata
    | FallbackHashingMetadata
)
