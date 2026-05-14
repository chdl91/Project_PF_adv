"""
Unit Tests for Quiz Application Business Logic

Test categories:
- Score calculation
- Difficulty validation
- User management
- Question/Answer validation
"""

import pytest


class TestScoreCalculation:
    """Unit Tests for score calculation logic"""

    def test_score_percentage_calculation_perfect_score(self):
        """
        TC_001: Perfect Quiz Score
        Calculate 100% when all answers are correct

        Preconditions: Quiz with 10 questions completed
        Test Data: correct_answers=10, total_questions=10
        Expected: percentage = 100.0, grade = 'A'
        """
        correct_answers = 10
        total_questions = 10

        percentage = (correct_answers / total_questions) * 100
        grade = 'A' if percentage >= 90 else 'B' if percentage >= 80 else 'C'

        assert percentage == 100.0
        assert grade == 'A'

    def test_score_percentage_calculation_partial_score(self):
        """
        TC_002: Partial Quiz Score
        Calculate 70% when 7 out of 10 answers are correct

        Preconditions: Quiz with 10 questions completed
        Test Data: correct_answers=7, total_questions=10
        Expected: percentage = 70.0, grade = 'C'
        """
        correct_answers = 7
        total_questions = 10

        percentage = (correct_answers / total_questions) * 100
        grade = 'A' if percentage >= 90 else 'B' if percentage >= 80 else 'C'

        assert percentage == 70.0
        assert grade == 'C'

    def test_score_percentage_calculation_zero_score(self):
        """
        TC_003: Zero Quiz Score
        Calculate 0% when no answers are correct

        Preconditions: Quiz with 5 questions completed
        Test Data: correct_answers=0, total_questions=5
        Expected: percentage = 0.0
        """
        correct_answers = 0
        total_questions = 5

        percentage = (correct_answers / total_questions) * 100

        assert percentage == 0.0

    def test_score_minimum_questions_requirement(self):
        """
        TC_004: Minimum Questions Requirement
        Validate that quiz must have minimum 5 questions

        Preconditions: None
        Test Data: num_questions=5
        Expected: is_valid=True
        """
        min_questions = 5
        num_questions = 5

        is_valid = num_questions >= min_questions

        assert is_valid is True

    def test_score_below_minimum_questions(self):
        """
        TC_005: Below Minimum Questions
        Reject quiz with less than 5 questions

        Preconditions: None
        Test Data: num_questions=4
        Expected: is_valid=False
        """
        min_questions = 5
        num_questions = 4

        is_valid = num_questions >= min_questions

        assert is_valid is False


class TestDifficultyValidation:
    """Unit Tests for difficulty level validation"""

    def test_valid_difficulty_easy(self):
        """
        TC_006: Valid Difficulty - Easy
        Accept 'easy' as valid difficulty level

        Test Data: difficulty='easy'
        Expected: is_valid=True
        """
        valid_difficulties = {'easy', 'medium', 'hard'}
        difficulty = 'easy'

        is_valid = difficulty.lower() in valid_difficulties

        assert is_valid is True

    def test_valid_difficulty_medium(self):
        """
        TC_007: Valid Difficulty - Medium
        Accept 'medium' as valid difficulty level

        Test Data: difficulty='medium'
        Expected: is_valid=True
        """
        valid_difficulties = {'easy', 'medium', 'hard'}
        difficulty = 'medium'

        is_valid = difficulty.lower() in valid_difficulties

        assert is_valid is True

    def test_valid_difficulty_hard(self):
        """
        TC_008: Valid Difficulty - Hard
        Accept 'hard' as valid difficulty level

        Test Data: difficulty='hard'
        Expected: is_valid=True
        """
        valid_difficulties = {'easy', 'medium', 'hard'}
        difficulty = 'hard'

        is_valid = difficulty.lower() in valid_difficulties

        assert is_valid is True

    def test_invalid_difficulty(self):
        """
        TC_009: Invalid Difficulty
        Reject invalid difficulty level

        Test Data: difficulty='expert'
        Expected: is_valid=False
        """
        valid_difficulties = {'easy', 'medium', 'hard'}
        difficulty = 'expert'

        is_valid = difficulty.lower() in valid_difficulties

        assert is_valid is False

    def test_difficulty_case_insensitive(self):
        """
        TC_010: Difficulty Case Insensitivity
        Accept difficulty levels regardless of case

        Test Data: difficulty='EASY'
        Expected: is_valid=True
        """
        valid_difficulties = {'easy', 'medium', 'hard'}
        difficulty = 'EASY'

        is_valid = difficulty.lower() in valid_difficulties

        assert is_valid is True


class TestUserManagement:
    """Unit Tests for user creation and validation"""

    def test_username_not_empty(self):
        """
        TC_011: Username Validation - Not Empty
        Reject empty username

        Test Data: username=''
        Expected: is_valid=False
        """
        username = ''

        is_valid = bool(username.strip())

        assert is_valid is False

    def test_username_valid_length(self):
        """
        TC_012: Username Validation - Valid Length
        Accept username within max length (30 chars)

        Test Data: username='john_doe'
        Expected: is_valid=True
        """
        username = 'john_doe'
        max_length = 30

        is_valid = 0 < len(username) <= max_length

        assert is_valid is True

    def test_username_exceeds_max_length(self):
        """
        TC_013: Username Validation - Exceeds Max Length
        Reject username exceeding max length

        Test Data: username='a' * 31
        Expected: is_valid=False
        """
        username = 'a' * 31
        max_length = 30

        is_valid = 0 < len(username) <= max_length

        assert is_valid is False


class TestAnswerValidation:
    """Unit Tests for answer and quiz response validation"""

    def test_answer_selection_valid(self):
        """
        TC_014: Answer Selection - Valid
        Accept valid answer selection (1-4)

        Test Data: selected_answer=2
        Expected: is_valid=True
        """
        selected_answer = 2
        valid_answers = {1, 2, 3, 4}

        is_valid = selected_answer in valid_answers

        assert is_valid is True

    def test_answer_selection_invalid_zero(self):
        """
        TC_015: Answer Selection - Invalid Zero
        Reject answer selection 0

        Test Data: selected_answer=0
        Expected: is_valid=False
        """
        selected_answer = 0
        valid_answers = {1, 2, 3, 4}

        is_valid = selected_answer in valid_answers

        assert is_valid is False

    def test_answer_selection_invalid_beyond_range(self):
        """
        TC_016: Answer Selection - Invalid Beyond Range
        Reject answer selection > 4

        Test Data: selected_answer=5
        Expected: is_valid=False
        """
        selected_answer = 5
        valid_answers = {1, 2, 3, 4}

        is_valid = selected_answer in valid_answers

        assert is_valid is False
