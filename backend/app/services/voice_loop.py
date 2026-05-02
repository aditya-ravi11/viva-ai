"""Real-time voice interview loop.

Glues Deepgram streaming ASR + Claude Haiku 4.5 + Deepgram Aura TTS over
a single WebSocket connection. This is the single hardest file in v1 -
target end-of-user-speech to first-TTS-frame latency is <2.5s.

Implementation notes (Month 1):
- Maintain a server-side WS to Deepgram for audio in.
- On final ASR results, build prompt = system + cached RAG + cached resume +
  last 6 turns + current code state. Stream Claude response.
- Stream Claude tokens to Aura via sentence-level chunking
  (one TTS request per sentence to minimize TTFB).
- Audio is captured as 30s rolling chunks to R2 for post-session prosody.
"""

# TODO(M1): implement
