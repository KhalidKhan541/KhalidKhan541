from typing import List, Dict, Any


class ReinspectionDecisionAgent:
    """
    Re-inspection Decision Agent.
    After each inspection cycle, decides whether additional passes are needed
    before the final report is generated.
    """

    RISK_LEVELS_ORDER = ["clear", "low", "medium", "high", "critical"]

    def __init__(self):
        pass

    def decide(
        self,
        zones_inspected: List[str],
        zone_results: List[Dict[str, Any]],
        max_passes_allowed: int,
        re_inspect_threshold: str = "medium",
    ) -> Dict[str, Any]:
        """
        Decide whether to re-inspect or proceed to report.

        Args:
            zones_inspected: List of zone names that have been inspected.
            zone_results: List of zone result dicts.
            max_passes_allowed: Maximum number of inspection passes allowed.
            re_inspect_threshold: Minimum risk level to trigger re-inspection.

        Returns:
            Decision dict with keys: decision, zones_for_reinspection, reason, pass_instructions.
        """
        zones_for_reinspection: List[str] = []
        pass_instructions: Dict[str, str] = {}
        reasons: List[str] = []

        threshold_index = self.RISK_LEVELS_ORDER.index(re_inspect_threshold)

        for result in zone_results:
            zone = result["zone"]
            risk_level = result["risk_level"]
            re_inspect_recommended = result["re_inspect_recommended"]
            re_inspect_reason = result.get("re_inspect_reason")
            pass_number = result["pass_number"]

            # Never re-inspect "clear" or "low" zones
            if risk_level in ("clear", "low"):
                continue

            # If pass_number >= max_passes_allowed → proceed_to_report regardless
            if pass_number >= max_passes_allowed:
                continue

            risk_index = self.RISK_LEVELS_ORDER.index(risk_level)

            # Rule 1: If any zone has risk_level == "critical" AND pass_number < max_passes_allowed → re_inspect
            if risk_level == "critical" and pass_number < max_passes_allowed:
                zones_for_reinspection.append(zone)
                instruction = self._generate_instruction(zone, risk_level, re_inspect_reason)
                pass_instructions[zone] = instruction
                reasons.append(f"{zone} is critical (pass {pass_number}/{max_passes_allowed})")
                continue

            # Rule 2: If re_inspect_recommended == true AND pass_number == 1 → re_inspect that zone
            if re_inspect_recommended and pass_number == 1:
                if risk_index >= threshold_index:
                    zones_for_reinspection.append(zone)
                    instruction = self._generate_instruction(zone, risk_level, re_inspect_reason)
                    pass_instructions[zone] = instruction
                    reasons.append(
                        f"{zone} recommended re-inspection at {risk_level} risk (pass 1)"
                    )
                    continue

            # Rule 4: If risk_level is at or above threshold and re_inspect_recommended
            if risk_index >= threshold_index and re_inspect_recommended:
                zones_for_reinspection.append(zone)
                instruction = self._generate_instruction(zone, risk_level, re_inspect_reason)
                pass_instructions[zone] = instruction
                reasons.append(
                    f"{zone} is {risk_level} with re-inspection recommended"
                )

        # Determine final decision
        if zones_for_reinspection:
            decision = "re_inspect"
            reason = "; ".join(reasons) if reasons else "One or more zones require additional inspection"
        else:
            decision = "proceed_to_report"
            reason = self._generate_proceed_reason(zone_results, max_passes_allowed)

        return {
            "decision": decision,
            "zones_for_reinspection": zones_for_reinspection,
            "reason": reason,
            "pass_instructions": pass_instructions,
        }

    def _generate_instruction(
        self, zone: str, risk_level: str, re_inspect_reason: str | None
    ) -> str:
        """Generate pass instructions for a zone needing re-inspection."""
        if re_inspect_reason:
            return f"Re-inspect {zone}: {re_inspect_reason}. Increase detection sensitivity."
        if risk_level == "critical":
            return f"Critical findings in {zone}. Perform thorough re-inspection with elevated sensitivity."
        if risk_level == "high":
            return f"High-risk indicators in {zone}. Re-inspect with increased detection sensitivity."
        return f"Medium-risk indicators in {zone}. Perform follow-up inspection."

    def _generate_proceed_reason(
        self, zone_results: List[Dict[str, Any]], max_passes_allowed: int
    ) -> str:
        """Generate reason string for proceeding to report."""
        if not zone_results:
            return "No zones inspected. Proceeding to report."

        risk_levels = [r["risk_level"] for r in zone_results]
        all_clear = all(level in ("clear", "low") for level in risk_levels)
        if all_clear:
            return "All zones are clear or low risk. No additional inspection needed."

        at_max = any(r["pass_number"] >= max_passes_allowed for r in zone_results)
        if at_max:
            return (
                f"Maximum inspection passes ({max_passes_allowed}) reached. "
                "Proceeding to final report."
            )

        return "No zones require re-inspection. Proceeding to final report."
