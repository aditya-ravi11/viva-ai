"""Post-session multi-criteria eval pipeline.

Runs async (target 45-90s after session end). Pulls all turns + editor
events + audio chunks, calls the fine-tuned Qwen2.5-7B model on Modal,
fuses prosody features (openSMILE eGeMAPS + filler-word density + pace +
pause distribution) into the eval prompt, persists per-criterion scores
with rationale + evidence quotes.

Criteria graded: technical_correctness, process, structure, clarity,
confidence, code_process.

Resume narrative target: per-criterion MAE + Spearman vs hand labels,
head-to-head vs Claude Haiku zero-shot baseline.
"""

# TODO(M2): implement
