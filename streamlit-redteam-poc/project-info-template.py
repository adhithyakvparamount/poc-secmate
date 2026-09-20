# Copy one target block into TARGETS in data.py.

TARGET_TEMPLATE = {
    "id": "project_short_id",
    "name": "ProjectName",
    "surface": "Short description of the AI/agent surface",
    "guides": ["Agents", "RAG", "Business logic"],
    "rate": 75,
    "high": 0,
    "medium": 0,
    "last": "not assessed yet",
    "next": "Tier 2 - planned",
    "classes": {
        "ExcessiveAgency": 70,
        "ToolOrchestrationAbuse": 70,
        "IndirectInstruction": 70,
        "PIILeakage": 70,
    },
}


# Copy one finding block into FINDINGS in data.py.

FINDING_TEMPLATE = {
    "id": "F-XXX",
    "target": "ProjectName",
    "vulnerability": "VulnerabilityName",
    "severity": "High",
    "status": "Open",
    "layer": "Action",
    "runs": 1,
    "chain": ["tool_one", "tool_two", "tool_three"],
    "hot": ["tool_two", "tool_three"],
    "attack": "The red-team input or attack prompt goes here.",
    "agent": "What the agent did or said goes here.",
    "verdict": "Why this behavior is unsafe goes here.",
    "fix": "Recommended remediation goes here.",
}
