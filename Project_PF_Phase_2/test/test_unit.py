"""Unit tests for the core quiz rules — tests actual service class methods."""

import pytest

from services.score_service import ScoreService
from services.question_service import QuestionService
from services.user_service import UserService


def test_score_calculation_and_grade_mapping():
    """TC_001: Score calculation should map to the right grade band."""
    cases = [
        (10, 10, 100.0, 6),
        (9, 10, 90.0, 6),
        (8, 10, 80.0, 5),
        (7, 10, 70.0, 4),
        (6, 10, 60.0, 3),
        (5, 10, 50.0, 2),
        (4, 10, 40.0, 1),
    ]
    for correct, total, expected_pct, expected_grade in cases:
        pct = ScoreService.calculate_percentage(correct, total)
        assert pct == pytest.approx(expected_pct)
        assert ScoreService.calculate_grade(pct) == expected_grade


def test_score_calculation_rejects_zero_total():
    """TC_002: A quiz with zero questions should fail fast."""
    with pytest.raises(ValueError, match="greater than zero"):
        ScoreService.calculate_percentage(3, 0)


def test_difficulty_validation_normalizes_input():
    """TC_003: Difficulty values should be normalized before validation."""
    assert QuestionService.normalize_difficulty(" easy ") == "easy"
    assert QuestionService.normalize_difficulty("MEDIUM") == "medium"
    assert QuestionService.normalize_difficulty("Hard") == "hard"


def test_difficulty_validation_rejects_unknown_value():
    """TC_004: Unknown difficulty values must be rejected."""
    with pytest.raises(ValueError, match="Invalid difficulty"):
        QuestionService.normalize_difficulty("expert")


def test_username_validation_rules():
    """TC_005: Username validation should handle blanks and length limits."""
    assert UserService.validate_username("student") is True
    assert UserService.validate_username("   ") is False
    assert UserService.validate_username("a" * 30) is True
    assert UserService.validate_username("a" * 31) is False


def test_answer_selection_rules():
    """TC_006: Answer choice must stay inside the valid range (1–4)."""
    assert QuestionService.validate_answer_index(1) is True
    assert QuestionService.validate_answer_index(2) is True
    assert QuestionService.validate_answer_index(4) is True
    assert QuestionService.validate_answer_index(0) is False
    assert QuestionService.validate_answer_index(5) is False
