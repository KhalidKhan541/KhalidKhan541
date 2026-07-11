# Re-inspection Decision Agent

A decision-making agent that determines whether additional inspection passes are needed before generating a final report.

## Decision Rules

1. If any zone has `risk_level == "critical"` AND `pass_number < max_passes_allowed` → re-inspect
2. If `re_inspect_recommended == true` for ANY zone AND `pass_number == 1` → re-inspect that zone
3. If `pass_number >= max_passes_allowed` → proceed_to_report regardless
4. If all zones are `"clear"` or `"low"` → proceed_to_report immediately
5. Never re-inspect `"clear"` or `"low"` zones — only medium and above

## Usage

```python
from agent import ReinspectionDecisionAgent

agent = ReinspectionDecisionAgent()

result = agent.decide(
    zones_inspected=["Zone A", "Zone B"],
    zone_results=[
        {
            "zone": "Zone A",
            "risk_level": "low",
            "re_inspect_recommended": False,
            "re_inspect_reason": None,
            "detection_count": 0,
            "pass_number": 1,
        },
        {
            "zone": "Zone B",
            "risk_level": "critical",
            "re_inspect_recommended": True,
            "re_inspect_reason": "Structural crack detected",
            "detection_count": 5,
            "pass_number": 1,
        },
    ],
    max_passes_allowed=3,
    re_inspect_threshold="medium",
)
```

## Output Format

```json
{
  "decision": "re_inspect",
  "zones_for_reinspection": ["Zone B"],
  "reason": "Zone B is critical (pass 1/3)",
  "pass_instructions": {
    "Zone B": "Critical findings in Zone B. Perform thorough re-inspection with elevated sensitivity."
  }
}
```

## Input Schema

| Field | Type | Description |
|-------|------|-------------|
| `zones_inspected` | `string[]` | List of zone names inspected |
| `zone_results` | `object[]` | Per-zone inspection results |
| `max_passes_allowed` | `int` | Max inspection passes before forced proceed |
| `re_inspect_threshold` | `string` | Min risk level to trigger re-inspection (`critical`, `high`, `medium`) |

### Zone Result Object

| Field | Type | Description |
|-------|------|-------------|
| `zone` | `string` | Zone identifier |
| `risk_level` | `string` | `clear`, `low`, `medium`, `high`, or `critical` |
| `re_inspect_recommended` | `bool` | Whether re-inspection is recommended |
| `re_inspect_reason` | `string|null` | Reason for re-inspection recommendation |
| `detection_count` | `int` | Number of anomalies detected |
| `pass_number` | `int` | Current pass number (1-indexed) |
