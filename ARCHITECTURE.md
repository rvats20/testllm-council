# 🏗️ Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER QUERY                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    LLM COUNCIL SYSTEM                        │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              AGENT GENERATION PHASE                   │  │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐        │  │
│  │  │  Agent 1  │  │  Agent 2  │  │  Agent 3  │        │  │
│  │  │Analytical │  │ Creative  │  │ Practical │        │  │
│  │  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘        │  │
│  │        │              │              │              │  │
│  │        ▼              ▼              ▼              │  │
│  │   Response 1     Response 2     Response 3         │  │
│  └────────┬───────────────┬─────────────┬──────────────┘  │
│           │               │             │                 │
│           ▼               ▼             ▼                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              JUDGE EVALUATION PHASE                   │  │
│  │  ┌─────────────────┐    ┌─────────────────┐         │  │
│  │  │   Judge 1       │    │   Judge 2       │         │  │
│  │  │   (Primary)     │    │  (Secondary)    │         │  │
│  │  │                 │    │                 │         │  │
│  │  │  Scores:        │    │  Scores:        │         │  │
│  │  │  - Accuracy     │    │  - Accuracy     │         │  │
│  │  │  - Safety       │    │  - Safety       │         │  │
│  │  │  - Completeness │    │  - Completeness │         │  │
│  │  └────────┬────────┘    └────────┬────────┘         │  │
│  │           │                      │                  │  │
│  │           └──────────┬───────────┘                  │  │
│  │                      ▼                              │  │
│  │           ┌──────────────────────┐                  │  │
│  │           │  Vote Aggregation    │                  │  │
│  │           │  - Winner Selection  │                  │  │
│  │           │  - Confidence Calc   │                  │  │
│  │           │  - Risk Identification│                  │  │
│  │           └──────────┬───────────┘                  │  │
│  └──────────────────────┼──────────────────────────────┘  │
│                         │                                 │
│                         ▼                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              SAFETY GATE                              │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │  │
│  │  │ APPROVED │  │ REQUIRES │  │ BLOCKED  │           │  │
│  │  │          │  │ APPROVAL │  │          │           │  │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘           │  │
│  └───────┼─────────────┼─────────────┼──────────────────┘  │
│          │             │             │                     │
│          └─────────────┴─────────────┘                     │
│                        │                                   │
└────────────────────────┼───────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                       OUTPUT                                 │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │ Decision Object  │         │   Audit Log      │         │
│  │  - Winner        │         │  - All Responses │         │
│  │  - Confidence    │         │  - Judge Scores  │         │
│  │  - Risks         │         │  - Final Decision│         │
│  │  - Citations     │         │  - Timestamps    │         │
│  │  - Gate Status   │         │                  │         │
│  └──────────────────┘         └──────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Agent Generation (3 Agents)

**Agent Types:**
- **Analytical**: Logical reasoning, factual accuracy, evidence-based
- **Creative**: Innovative solutions, alternative perspectives
- **Practical**: Real-world applicability, actionable advice

**Output:** Each agent produces a complete response to the user query

### 2. Judge Evaluation (2 Judges)

**Judge Roles:**
- **Primary Judge**: Overall quality and safety assessment
- **Secondary Judge**: Risk identification and edge cases

**Evaluation Rubric (0-10 scale):**
- **Accuracy**: Factual correctness and logical soundness
- **Safety**: Absence of harmful, biased, or problematic content
- **Completeness**: Thoroughness in addressing the query

**Output:** Each judge selects a winner and provides scores

### 3. Decision Aggregation

**Process:**
1. Count votes from judges
2. Calculate average confidence
3. Identify risks (low safety scores, low confidence)
4. Extract citations from responses
5. Select winner (most votes)

### 4. Safety Gate

**Three-Tier System:**

| Status | Condition | Action |
|--------|-----------|--------|
| **APPROVED** | confidence ≥ 0.5 AND safety ≥ 6 AND risks ≤ 2 | Allow output |
| **REQUIRES_APPROVAL** | confidence < 0.5 OR risks > 2 | Flag for review |
| **BLOCKED** | safety < 6 | Block output |

### 5. Output Generation

**Decision Object (JSON):**
```json
{
  "winner": "agent_id",
  "confidence": 0.85,
  "risks": ["List of identified risks"],
  "citations": ["List of sources"],
  "agent_responses": [...],
  "judge_scores": [...],
  "safety_gate_status": "APPROVED",
  "timestamp": "ISO-8601"
}
```

**Audit Log (JSON):**
```json
[
  {"type": "agent_response", "data": {...}},
  {"type": "judge_score", "data": {...}},
  {"type": "final_decision", "data": {...}}
]
```

## Data Flow

```
User Query
    ↓
[LLM API] → Agent 1 Response
[LLM API] → Agent 2 Response
[LLM API] → Agent 3 Response
    ↓
[LLM API] → Judge 1 Scores (reads all 3 responses)
[LLM API] → Judge 2 Scores (reads all 3 responses)
    ↓
Aggregation Logic
    ↓
Safety Gate Check
    ↓
Decision Object + Audit Log
```

## Key Design Decisions

### Why 3 Agents?
- Provides diversity of perspectives
- Odd number prevents tie votes
- Enough variation without excessive cost

### Why 2 Judges?
- Primary for quality assessment
- Secondary for risk/edge case detection
- Balances thoroughness with efficiency

### Why Separate Judge Phase?
- Reduces bias (agents don't know they're being judged)
- Allows for consistent evaluation criteria
- Enables transparent scoring

### Why Safety Gate?
- Prevents harmful outputs
- Provides audit trail for compliance
- Allows human-in-the-loop for borderline cases

## Performance Characteristics

### API Calls per Query
- 3 agent calls (parallel possible)
- 2 judge calls (parallel possible)
- **Total: 5 LLM API calls**

### Latency
- ~5-10 seconds per agent (3 parallel)
- ~5-10 seconds per judge (2 parallel)
- **Total: ~10-20 seconds** (with parallelization)

### Cost (Anthropic Sonnet 4)
- ~1000 tokens per agent response (3 agents)
- ~1500 tokens per judge evaluation (2 judges)
- **Total: ~6000 tokens per query**
- At $3/$15 per MTok (input/output): **~$0.05-0.10 per query**

## Extension Points

### Add More Agents
```python
agents.append({
    "id": "agent_security",
    "system": "Security-focused perspective"
})
```

### Customize Rubric
```python
# Modify judge_prompt to include custom criteria
# Add new scoring dimensions
```

### Add Caching
```python
# Cache agent responses by query hash
# Reduces cost for repeated queries
```

### Add Parallelization
```python
# Use asyncio for concurrent API calls
# Reduce latency significantly
```

## Security Considerations

1. **API Key Security**
   - Never commit API keys
   - Use environment variables
   - Rotate keys regularly

2. **Input Validation**
   - Sanitize user queries
   - Check for injection attempts
   - Rate limit requests

3. **Output Filtering**
   - Safety gate prevents harmful content
   - Log all decisions for audit
   - Allow manual review for flagged content

## Monitoring & Observability

**What to Monitor:**
- Total queries processed
- Average confidence scores
- Safety gate blocks/approvals
- API errors and retries
- Response times
- Cost per query

**Logging:**
- All agent responses
- All judge scores
- Final decisions
- Safety gate outcomes
- Timestamps for everything

This architecture provides a balance of:
- ✅ Quality (multiple perspectives)
- ✅ Safety (scoring + gating)
- ✅ Transparency (audit logs)
- ✅ Extensibility (easy to modify)
- ✅ Cost-effectiveness (minimal API calls)
