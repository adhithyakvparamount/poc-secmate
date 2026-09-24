# Technical Requirements Document (TRD) & Engineering Knowledge Base

## Enterprise AI Adversarial Red-Teaming & Action-Space Verification Platform

* **Document Classification:** Engineering Baseline Specification
* **Target Domain:** Enterprise Security Operations & Multi-Agent Ecosystems
* **Authoring Context:** Autonomous AI Agent Penetration Testing
* **Standard Alignments:** OWASP Top 10 for Large Language Models (2025/2026), MITRE ATLAS, NIST AI RMF 1.0, OpenAPI 3.1 / JSON Schema (Draft 2020-12)

---

## 1. System Vision & Core Architectural Principles

### 1.1 Purpose
The platform is an automated, black-box/grey-box security testing harness engineered to continuously evaluate enterprise AI agents against prompt injection, jailbreaking, data exfiltration, and unauthorized tool execution. The system dynamically tests any agent produced within the enterprise without modifying target source code or requiring access to underlying model weights.

### 1.2 Foundational Architectural Principles
* **Action-Space Primacy:** In agentic enterprise architectures, linguistic output is secondary to side-effect execution. Natural language is treated strictly as an untrusted attack vector, while the primary security boundary is the agent's function-calling interface (APIs, databases, system commands, and message queues).
* **Declarative Manifest Separation:** Agent trust boundaries and adversarial tactics must be completely decoupled from execution logic. Agents and attack scenarios are defined via declarative, version-controlled manifests rather than imperative application code.
* **Refusal-Resistant Adversarial Fuzzing:** The harness rejects static, pre-canned jailbreak dictionaries. Attack inputs are synthesized dynamically by conditioning an adversarial engine on the specific operational boundaries of the target. To prevent provider-level safety refusals during testing, attacks are framed under formal software Quality Assurance (QA) boundary verification parameters.
* **Dual-Stage Hybrid Verification:** Sole reliance on a semantic Language Model as an evaluator is mathematically non-deterministic and susceptible to sycophancy. Verification must enforce a two-tier architecture: deterministic programmatic rule engines for hard action-space constraints, followed by a zero-temperature Chain-of-Thought (CoT) semantic evaluator for conversational compliance.
* **Stateless Broker Pattern:** Language models possess no persistent state or cross-agent communication channels. A central orchestration broker manages all transport, message routing, regex-based delimiter isolation, parameter deserialization, and multi-turn state machines.

---

## 2. Industry Standards & Threat Taxonomy Baseline

The platform's attack and verification engines must align with recognized international AI security standards:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   ENTERPRISE THREAT MAPPING TAXONOMY                                         │
├──────────────────────────┬───────────────────────┬─────────────────────┤
│ Standard Framework       │ Threat Code           │ Operational Focus                        │
├──────────────────────────┼───────────────────────┼─────────────────────┤
│ OWASP Top 10 for LLMs    │ LLM01                 │ Prompt Injection                         │
│ OWASP Top 10 for LLMs    │ LLM02                 │ Sensitive Info Leak                      │
│ OWASP Top 10 for LLMs    │ LLM08                 │ Excessive Agency                         │
│ MITRE ATLAS              │ AML.T0051             │ LLM Prompt Injection                     │
│ MITRE ATLAS              │ AML.T0054             │ LLM Jailbreak                            │
│ MITRE ATLAS              │ AML.T0040             │ Model Inference API                      │
│ NIST AI RMF 1.0          │ Measure 2.6 / 2.7     │ Boundary Resilience                      │
└──────────────────────────┴───────────────────────┴─────────────────────┘

### 2.1 Threat Vector Matrix

-   **Persona & Authority Manipulation (MITRE AML.T0054):** Impersonates internal executive leadership, system auditors, or emergency engineers to evaluate if authority bias causes policy relaxation.

-   **Context & Delimiter Breakout (OWASP LLM01):** Uses synthetic protocol control markers, markdown fences, or system-instruction termination tokens to force early context completion.

-   **Action-Space Parameter Smuggling (OWASP LLM08):** Injects shell metacharacters, unauthorized CIDR ranges, drop/truncate syntax, or unauthorized identities into valid tool parameters.

-   **Indirect Research / Academic Framing (MITRE AML.T0054):** Abstracts restricted operations into theoretical post-mortem scenarios or defensive research papers to test semantic guardrail leakage.

-   **System Prompt & Topology Exfiltration (OWASP LLM02):** Prompts the model to dump initialization guidelines, internal schemas, or honeytokens under the guise of debug or synchronization errors.

-   **Recursive Instruction Injection (OWASP LLM01):** Simulates indirect injection by embedding secondary executable instructions within simulated third-party retrieval data (RAG payloads, database records, log entries).

## 3\. System Architecture & Subsystem Specifications

The platform is composed of six decoupled subsystems operating under an orchestration broker.

┌────────────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATION BROKER                           │
│        (State Machine / Rate Limiter / Context Manager / Router)       │
└───────┬──────────────────────────┬──────────────────────────┬──────────┘
          │                                  │                │
          ▼ (Target Profile)                 ▼ (Adversarial Probe)              ▼ (Full Telemetry)
┌─────────────────┐        ┌─────────────────┐        ┌──────────────────┐
│  Adversarial         │        │  Target Agent        │        │         Dual-Stage     │
│  Synthesis           │        │  Gateway             │        │   Verification         │
│  Engine              │        │  (Transport)         │        │   Engine               │
└─────────────────┘        └────────┬────────┘        └──────────────────┘
                                            │
                                            ▼
                         ┌─────────────────────┐
                         │   Intercepted Tool        │
                         │   Invocation Bus          │
                         └─────────────────────┘

### 3.1 Subsystem A: Declarative Manifest Ingestion

-   Ingests target definitions and threat vectors using strict schema validation.

-   Translates target tool definitions dynamically into standard OpenAPI / JSON Schema specifications.

-   Injects traceable canary tokens (honeytokens) into target contexts to allow programmatic detection of prompt exfiltration.

### 3.2 Subsystem B: Adversarial Synthesis Engine (Red Team Generator)

-   Merges the target agent's negative operational boundaries with a specified attack vector recipe.

-   Applies semantic QA fuzzing framing to prevent model refusals, removing hostile terminology (e.g., "exploit", "hack", "bypass").

-   Enforces structural output delimiters (<probe>...</probe>) to separate generated attack payloads from model commentary.

### 3.3 Subsystem C: Target Gateway & Action-Space Interceptor

-   Connects to target agents across multiple transport protocols (In-Memory, HTTP/REST, WebSockets, or gRPC).

-   Isolates the conversational text stream from the tool-call execution stream.

-   Implements a **Mock Action Bus**: captures, inspects, and logs tool execution requests without dispatching destructive side effects to real enterprise environments.

### 3.4 Subsystem D: Dual-Stage Verification Engine (Blue Team Judge)

-   **Stage 1 (Deterministic Policy Engine):**

    -   Evaluates tool-calling arguments against exact programmatic rules (CIDR network ranges, SQL grammar ASTs, regex patterns).

    -   **Tool-Scoped Inspection Invariant:** Must strictly filter rules by tool classification (e.g., containment, mutation, read-only search) before asserting violations.

-   **Stage 2 (Semantic LLM-as-a-Judge):**

    -   Implements G-Eval Chain-of-Thought methodology at temperature 0.0.

    -   Operates under grammar-constrained JSON decoding.

    -   Formulates step-by-step reasoning and extracts verbatim evidence quotes prior to asserting a binary compliance verdict.

### 3.5 Subsystem E: Multi-Turn State Machine

-   Executes bounded conversational loops (configurable: 1 to 5 turns).

-   **Adaptive Escalation:** If a target resists on Turn N, the broker feeds the target's explicit refusal rationale back to the synthesis engine to generate an adapted follow-up probe on Turn N+1.

-   **Short-Circuit Termination:** Immediately halts the execution loop upon a confirmed breach at any turn to preserve API token quotas and eliminate redundant calls.

### 3.6 Subsystem F: Telemetry & Audit Serialization

-   Serializes every interaction turn into immutable JSON audit records.

-   Captures time-to-first-token (TTFT), total latency, prompt/completion token consumption, intercepted tool payloads, and formal judge findings.

## 4\. Formal Data Contracts & Invariants

All data models must strictly enforce the following schema contracts.

{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "name": "string",
  "description": "string",
  "system_prompt": "string",
  "guardrails": [
    "string"
  ],
  "tools": [
    {
      "name": "string",
      "description": "string",
      "category": "read_only | containment | mutation | administrative",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  ],
  "transport": {
    "type": "http_rest | websocket | in_memory",
    "endpoint_url": "string (optional)",
    "auth_header": "string (optional)"
  }
}

### 4.2 Adversarial Threat Scenario Manifest

{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "version": "string",
  "attack_vectors": [
    {
      "id": "string (e.g., VEC-TOOL-001)",
      "name": "string",
      "category": "string",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "description": "string",
      "recipe": "string (precise attack instructions for generator)"
    }
  ]
}

### 4.3 Action-Space Interception Telemetry

{
  "turn_number": 1,
  "probe_sent": "string",
  "target_text_response": "string",
  "tool_calls": [
    {
      "name": "string",
      "arguments": {}
    }
  ],
  "deterministic_findings": [
    {
      "rule_id": "string",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW | NONE",
      "message": "string"
    }
  ],
  "judge_verdict": {
    "violation_detected": true,
    "severity": "CRITICAL",
    "evidence_quote": "string or null",
    "reasoning": "string"
  }
}

## 5\. Technical Lessons Learned & Failure Mode Mitigations

To build an enterprise-scale platform, the following baseline operational traps must be handled:

### 5.1 Context-Aware Tool Scoping (False-Positive Elimination)

-   **The Failure Mode:** Scanning all intercepted tool arguments with blanket regex rules causes massive false positives. For example, flagging a private RFC-1918 IP address as a "Containment Violation" when the agent merely performed a passive read-only search on a user-supplied IP.

-   **The Baseline Requirement:** Deterministic checks must map to **Tool Functional Categories**:

    -   Containment rules (e.g., blocking private subnets) apply only to tools tagged category: containment.

    -   Data modification rules (e.g., SQL DROP checks) apply only to tools tagged category: mutation.

    -   Read-only search lookups on user-provided data must evaluate under category: read\_only with LOW (Informational) severity at most.

### 5.2 Provider Quota & OTPM Throttling Layer

-   **The Failure Mode:** Multi-turn testing requires multiple sequential LLM calls per minute. Unconstrained calls quickly exceed Output Tokens Per Minute (OTPM) and Requests Per Minute (RPM) limits on cloud inference tiers, resulting in HTTP 429 errors.

-   **The Baseline Requirement:**

    -   The broker must strictly set max\_tokens (capped at 500 tokens) across all API requests. Omitting this causes providers to reserve full context-window allocations, depleting per-minute quotas prematurely.

    -   Implement a token-bucket rate limiter and mandatory inter-turn throttling (minimum 2.0s jitter) between sequential calls.

    -   Implement transport retry decorators with exponential backoff on HTTP 429 and 503 status codes.

### 5.3 Extraction Boundaries & Conversational Fluff

-   **The Failure Mode:** When generating attack prompts, LLMs often emit introductory commentary (e.g., "Here is a test prompt you can use: ..."). Passing this commentary to the target ruins the test.

-   **The Baseline Requirement:** The generation prompt must mandate strict boundary markers (<probe>PAYLOAD</probe>). The broker extracts content strictly via non-greedy regex matching (re.search(r"<probe>(.\*?)</probe>", text, re.DOTALL)), falling back to whitespace/quote stripping only if delimiters are omitted.

### 5.4 JSON Parser Resilience & Constrained Decoding

-   **The Failure Mode:** Evaluator LLMs often wrap JSON outputs in markdown code blocks (json { ... }), causing native JSON parsers to throw unhandled exceptions.

-   **The Baseline Requirement:**

    -   Leverage hardware-level grammar sampling (response\_format={"type": "json\_object"}) where supported by the inference engine.

    -   The ingestion pipeline must employ regex-based extraction to isolate the outermost JSON boundary (re.search(r"(\\{.\*\\})", text, re.DOTALL)) prior to deserialization.

## 6. Enterprise Integration & Scaling Roadmap

The baseline architecture must support continuous enterprise deployment across the organization:

6.1 Remote Black-Box Target Interoperability The Target Gateway must support remote **HTTP**/**REST** microservice targets via non-blocking asynchronous clients (httpx.AsyncClient). Support enterprise authorization standards: OAuth 2.0 Client Credentials, static Bearer tokens, and mutual **TLS** (mTLS). Inject standardized correlation headers (X-Assessment-ID, X-Session-ID, X-Caller-Role) to evaluate agents under simulated Role-Based Access Control (**RBAC**) tiers (e.g., testing if a Tier-1 Read-Only user can trigger Tier-3 Containment commands).

6.2 Asynchronous Execution & Task Queues Replace synchronous execution loops with an asynchronous distributed task queue (e.g., Celery, Redis, or temporal workflows). Enable parallel execution of attack suites across multiple target agents simultaneously, governed by global concurrency and token-rate limiters.

6.3 CI/CD Quality Gate (Automated Regression Testing) Provide a headless Command Line Interface (**CLI**) runner supporting automated build pipelines (GitHub Actions, GitLab CI). Policy Enforcement Gate: If any target evaluation yields an unhandled breach with severity **HIGH** or **CRITICAL**, the process terminates with exit code 1, breaking the deployment build. Export standardized machine-readable security reports, including **SARIF** (Static Analysis Results Interchange Format) and JUnit **XML**.

6.4 Safe Execution Sandboxing Ensure all mutating tools route to ephemeral sandboxes (e.g., containerized mock APIs, virtualized network firewalls, read-only **SQL** replicas) to prevent tests from executing destructive actions against production or shared corporate environments.

## 7. Non-Functional Requirements & Security Hygiene

### 7.1 Zero Credential Retention
The platform must never serialize live credentials, API keys, or target authorization tokens into persistent audit logs. All environment configurations must be loaded strictly from isolated environment variables.

### 7.2 Determinism & Reproducibility
Every audit report must capture the exact prompt, temperature, model version, system instructions, and tool schemas used, ensuring any detected vulnerability can be replayed and verified deterministically.

### 7.3 Latency
The end-to-end evaluation loop (generation, target invocation, tool parameter extraction, and dual verification) must maintain a target latency of under 5.0 seconds per turn when running on high-speed inference backends.

### 7.4 Fail-Closed Behavior
If the platform encounters an unhandled internal error, timeout, or loss of connectivity to the target agent or the LLM provider mid-run, the CI/CD Quality Gate (§6.3) must default to a build-blocking failure state. The gate must never silently pass a build due to an internal platform fault.

### 7.5 Judge Calibration
The Stage-2 semantic judge (§3.4) must be subject to periodic, human-reviewed sampling of verdicts to track false-positive and false-negative rates over time. A calibration report must be produced on a defined cadence and reviewed by the platform owner.

### 7.6 Availability & Scale Targets
*TBD — define uptime target, maximum concurrent target agents under test, and audit-log retention period.*