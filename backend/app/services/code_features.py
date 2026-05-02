"""Process-feature extraction from editor_events.

Features:
- time_to_first_keystroke (after question end)
- edit_churn_ratio (chars deleted / chars added)
- burst_pattern (kps over time; thinking <=2, typing >=5)
- pause_during_typing_count (pauses >4s mid-typing)
- tab_switches, paste_count (integrity flags - surfaced, do not fail user)
- final_code_run_result (sandboxed test execution)

Composite process_score = weighted z-scores against thresholds.
Hand-tuned from a 20-session pilot; replaced with learned thresholds at >=100 sessions.
"""

# TODO(M3): implement
