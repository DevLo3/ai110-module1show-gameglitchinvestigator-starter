---
name: Known bugs and intentional glitches in Game Glitch Investigator
description: Documents the deliberate and accidental bugs seeded in this starter project for students to find and fix
type: project
---

This is a CodePath AI110 teaching project. The app is a Streamlit number-guessing game with intentional bugs for students to investigate.

**Bug 1 (FIXED): Inverted hint messages in check_guess**
- File: `app.py`, function `check_guess`, lines ~37-47
- Root cause: The human-facing hint strings were swapped. "Too High" returned "Go HIGHER!" and "Too Low" returned "Go LOWER!" — exact opposite of correct guidance.
- Fix: Swap the message strings so "Too High" → "Go LOWER!" and "Too Low" → "Go HIGHER!"
- Both the main `try` branch and the `except TypeError` fallback had the same inversion.

**Bug 2 (noted, not fixed): attempts initialized to 1 instead of 0**
- File: `app.py`, line 97
- The `FIXME` comment is already in the code: `st.session_state.attempts = 1` should be `0`

**Bug 3 (noted): Hard difficulty range is wrong**
- File: `app.py`, line 10
- `get_range_for_difficulty("Hard")` returns `(1, 50)` but Hard should logically be a wider range than Normal (1, 100), not narrower in a confusing way.

**Architectural note: logic_utils.py is a stub**
- All functions in `logic_utils.py` raise `NotImplementedError` — they are meant to be filled in as a refactoring exercise (moving logic from `app.py` into `logic_utils.py`).
- The actual working implementations currently live in `app.py`.

**Why:** This is an AI110 educational project where students learn to identify and fix bugs in AI-generated code.
**How to apply:** When asked to fix bugs here, check this list first. When fixing, apply minimal targeted changes and document what was found.
