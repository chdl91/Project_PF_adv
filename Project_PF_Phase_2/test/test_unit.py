"""Unit tests for the core quiz rules."""

import pytest


def calculate_percentage(correct_answers, total_questions):
    if total_questions <= 0:
        raise ValueError("total_questions must be greater than zero")
    return (correct_answers / total_questions) * 100


def grade_for_percentage(percentage):
    if percentage >= 90:
        return "A"
    if percentage >= 80:
        return "B"
    if percentage >= 70:
        return "C"
    return "F"


def normalize_difficulty(value):
    allowed = {"easy", "medium", "hard"}
    normalized = value.strip().lower()
    if normalized not in allowed:
        raise ValueError("invalid difficulty")
    return normalized


def validate_username(value):
    cleaned = value.strip()
    return bool(cleaned) and len(cleaned) <= 30


def validate_answer_choice(choice):
    return choice in {1, 2, 3, 4}


def test_score_calculation_and_grade_mapping():
    """TC_001: Score calculation should map to the right grade band."""
    cases = [
        (10, 10, 100.0, "A"),
        (8, 10, 80.0, "B"),
        (7, 10, 70.0, "C"),
    ]

    for correct_answers, total_questions, expected_percentage, expected_grade in cases:
        percentage = calculate_percentage(correct_answers, total_questions)
        assert percentage == pytest.approx(expected_percentage)
        assert grade_for_percentage(percentage) == expected_grade


def test_score_calculation_rejects_zero_total():
    """TC_002: A quiz with zero questions should fail fast."""
    with pytest.raises(ValueError, match="greater than zero"):
        calculate_percentage(3, 0)


def test_difficulty_validation_normalizes_input():
    """TC_003: Difficulty values should be normalized before validation."""
    assert normalize_difficulty(" easy ") == "easy"
    assert normalize_difficulty("MEDIUM") == "medium"
    assert normalize_difficulty("Hard") == "hard"


def test_difficulty_validation_rejects_unknown_value():
    """TC_004: Unknown difficulty values must be rejected."""
    with pytest.raises(ValueError, match="invalid difficulty"):
        normalize_difficulty("expert")


def test_username_validation_rules():
    """TC_005: Username validation should handle blanks and length limits."""
    assert validate_username("student") is True
    assert validate_username("   ") is False
    assert validate_username("a" * 30) is True
    assert validate_username("a" * 31) is False


def test_answer_selection_rules():
    """TC_006: Answer choice must stay inside the valid range."""
    assert validate_answer_choice(1) is True
    assert validate_answer_choice(2) is True
    assert validate_answer_choice(4) is True
    assert validate_answer_choice(0) is False
    assert validate_answer_choice(5) is False
