from logic_utils import check_guess
from streamlit.testing.v1 import AppTest

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# Bug #4: history entry should appear in session state after a single submit,
# not require a second submit or a checkbox toggle to trigger a rerun.
def test_history_updated_after_single_submit():
    at = AppTest.from_file("../app.py").run()
    at.text_input[0].input("50")
    at.button[0].click().run()
    assert len(at.session_state.history) == 1


# Bug #3a: clicking New Game should clear the attempt history list.
def test_new_game_clears_history():
    at = AppTest.from_file("../app.py").run()
    at.text_input[0].input("50")
    at.button[0].click().run()
    assert len(at.session_state.history) == 1
    at.button[1].click().run()  # New Game
    assert len(at.session_state.history) == 0


# Bug #3b: clicking New Game after a win or loss should reset status to
# "playing" so further guesses can be submitted.
def test_new_game_resets_status_to_playing():
    at = AppTest.from_file("../app.py").run()
    at.session_state.secret = 50  # pin secret so a guess of 50 wins
    at.text_input[0].input("50")
    at.button[0].click().run()
    assert at.session_state.status == "won"
    at.button[1].click().run()  # New Game
    assert at.session_state.status == "playing"


# Hint regression: after the st.rerun() fix for Bug #1, hints were being
# wiped before render. A warning message should be visible after one submit.
def test_hint_visible_after_single_submit():
    at = AppTest.from_file("../app.py").run()
    at.session_state.secret = 99  # ensure the guess won't accidentally win
    at.text_input[0].input("1")
    at.button[0].click().run()
    assert len(at.warning) > 0


# Bug #1: attempts was initialized to 1 instead of 0, causing the counter
# to show 1 used attempt on a fresh page load before any guess was submitted.
def test_attempts_initialized_to_zero_on_fresh_load():
    at = AppTest.from_file("../app.py").run()
    assert at.session_state.attempts == 0


# Bug #2: check_guess had its hint messages swapped — a guess that was too
# high incorrectly told the player to go higher, and vice versa.
def test_hint_message_direction_too_high():
    # guess (60) > secret (50): player should be told to go LOWER
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()


def test_hint_message_direction_too_low():
    # guess (40) < secret (50): player should be told to go HIGHER
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()
