from agent import ReinspectionDecisionAgent


def example_reinspect():
    """Example where Zone B triggers a re-inspection."""
    agent = ReinspectionDecisionAgent()

    result = agent.decide(
        zones_inspected=["Zone A", "Zone B", "Zone C"],
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
                "risk_level": "high",
                "re_inspect_recommended": True,
                "re_inspect_reason": "Crack pattern detected along load-bearing wall",
                "detection_count": 3,
                "pass_number": 1,
            },
            {
                "zone": "Zone C",
                "risk_level": "medium",
                "re_inspect_recommended": True,
                "re_inspect_reason": "Minor surface anomalies near foundation",
                "detection_count": 1,
                "pass_number": 1,
            },
        ],
        max_passes_allowed=3,
        re_inspect_threshold="medium",
    )
    print("=== Example 1: Re-inspect ===")
    print(result)


def example_proceed():
    """Example where all zones are clear."""
    agent = ReinspectionDecisionAgent()

    result = agent.decide(
        zones_inspected=["Zone A", "Zone B"],
        zone_results=[
            {
                "zone": "Zone A",
                "risk_level": "clear",
                "re_inspect_recommended": False,
                "re_inspect_reason": None,
                "detection_count": 0,
                "pass_number": 1,
            },
            {
                "zone": "Zone B",
                "risk_level": "low",
                "re_inspect_recommended": False,
                "re_inspect_reason": None,
                "detection_count": 0,
                "pass_number": 1,
            },
        ],
        max_passes_allowed=3,
        re_inspect_threshold="medium",
    )
    print("=== Example 2: Proceed to report ===")
    print(result)


def example_max_passes():
    """Example where max passes reached forces proceed."""
    agent = ReinspectionDecisionAgent()

    result = agent.decide(
        zones_inspected=["Zone A"],
        zone_results=[
            {
                "zone": "Zone A",
                "risk_level": "critical",
                "re_inspect_recommended": True,
                "re_inspect_reason": "Structural damage suspected",
                "detection_count": 7,
                "pass_number": 3,
            },
        ],
        max_passes_allowed=3,
        re_inspect_threshold="medium",
    )
    print("=== Example 3: Max passes reached ===")
    print(result)


def example_critical_pass1():
    """Example where critical zone on pass 1 triggers re-inspection."""
    agent = ReinspectionDecisionAgent()

    result = agent.decide(
        zones_inspected=["Zone A", "Zone B"],
        zone_results=[
            {
                "zone": "Zone A",
                "risk_level": "critical",
                "re_inspect_recommended": True,
                "re_inspect_reason": "Severe foundation crack detected",
                "detection_count": 5,
                "pass_number": 1,
            },
            {
                "zone": "Zone B",
                "risk_level": "medium",
                "re_inspect_recommended": True,
                "re_inspect_reason": "Surface discoloration observed",
                "detection_count": 2,
                "pass_number": 1,
            },
        ],
        max_passes_allowed=3,
        re_inspect_threshold="medium",
    )
    print("=== Example 4: Critical zone pass 1 ===")
    print(result)


if __name__ == "__main__":
    example_reinspect()
    example_proceed()
    example_max_passes()
    example_critical_pass1()
