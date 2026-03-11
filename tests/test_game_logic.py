from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug fix: swapped hint messages ---

def test_hint_says_lower_when_guess_too_high():
    # When guess > secret, message must say "Lower", not "Higher"
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"
    assert "Lower" in message, f"Expected 'Lower' in message, got: {message}"


def test_hint_says_higher_when_guess_too_low():
    # When guess < secret, message must say "Higher", not "Lower"
    outcome, message = check_guess(20, 50)
    assert outcome == "Too Low"
    assert "Higher" in message, f"Expected 'Higher' in message, got: {message}"


# --- Bug fix: type-switching caused string comparisons on even attempts ---

def test_integer_comparison_not_string():
    # 9 < 42 numerically (Too Low), but "9" > "42" as strings (would say Too High)
    outcome, message = check_guess(9, 42)
    assert outcome == "Too Low", "String comparison would incorrectly return Too High"
    assert "Higher" in message


def test_two_digit_vs_single_digit_ordering():
    # "10" < "9" as strings, but 10 > 9 numerically
    outcome, message = check_guess(10, 9)
    assert outcome == "Too High"
    assert "Lower" in message
