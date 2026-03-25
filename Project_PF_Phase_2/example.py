"""
Phase 2 Starter Example: Load OODB and run with Phase 1 code or standalone.

This file demonstrates the most common usage patterns.
"""

from adapters import LegacyQuizAdapter
from models.database import QuizDatabase
from models.loader import OODBLoader
import sys
from pathlib import Path

# Add Phase 2 to Python path
sys.path.insert(0, str(Path(__file__).parent))


def print_database_summary():
    """Load and print a summary of the quiz database."""
    print("\n" + "="*60)
    print("PHASE 2 OODB QUIZ DATABASE")
    print("="*60)

    loader = OODBLoader(data_dir=Path(__file__).parent / "data")
    db = loader.load_database_from_file("DIB.json")

    summary = db.summary()
    print(f"\n📊 Database Summary:")
    print(f"   Topics: {summary['topics_count']}")
    print(f"   Questions: {summary['questions_count']}")
    print(f"   Answers: {summary['choices_count']}")
    print(f"\n📚 Topics:")
    for topic in summary['topics']:
        print(f"   - {topic['name']} ({topic['question_count']} questions)")

    return db


def explore_question_object(db: QuizDatabase):
    """Show how to navigate OODB objects."""
    print("\n" + "="*60)
    print("OBJECT NAVIGATION EXAMPLE")
    print("="*60)

    # Get a question
    question = db.get_question("Q001")
    if not question:
        print("Question Q001 not found")
        return

    print(f"\n❓ Question: {question.text}")

    # Get topic via relationship
    topic = db.get_topic(question.topic_id)
    print(f"📂 Topic: {topic.name if topic else 'Unknown'}")

    # Get difficulty via relationship
    diff = db.get_difficulty(question.difficulty_id)
    print(f"🎯 Difficulty: {diff.name if diff else 'Unknown'}")

    # List choices
    print(f"\n📋 Choices:")
    for choice in question.choices:
        is_correct = choice.id == question.correct_choice_id
        mark = "✓ CORRECT" if is_correct else "  "
        print(f"   [{mark}] {choice.label}. {choice.text}")

    print(f"\n💡 Explanation: {question.explanation}")


def show_backward_compatibility(db: QuizDatabase):
    """Show how Phase 1 code works with Phase 2 data."""
    print("\n" + "="*60)
    print("BACKWARD COMPATIBILITY: Phase 1 Format")
    print("="*60)

    # Convert to Phase 1 format
    phase1_questions = LegacyQuizAdapter.to_phase1_format(db)

    print(
        f"\n✅ Successfully converted {len(phase1_questions)} questions to Phase 1 format")

    # Show a sample
    if phase1_questions:
        sample = phase1_questions[0]
        print(f"\n📄 Sample (Phase 1 format):")
        print(f"   Topic: {sample['topic']}")
        print(f"   Question: {sample['question']}")
        print(f"   Difficulty: {sample['difficulty']}")
        print(f"   Answers:")
        for num, text in sample['answers'].items():
            mark = " ✓" if int(num) == sample['correct_answer'] else ""
            print(f"      {num}.{mark} {text}")
        print(f"\n   This format is compatible with Phase 1 quiz.py!")


def demo_queries(db: QuizDatabase):
    """Show example queries."""
    print("\n" + "="*60)
    print("EXAMPLE QUERIES")
    print("="*60)

    # By topic
    topic = db.get_topic("T_Digitalization")
    if topic:
        print(f"\n🔍 Questions in '{topic.name}':")
        for q in topic.questions[:3]:  # First 3
            print(f"   - {q.text[:60]}...")

    # By difficulty
    hard_questions = db.questions_by_difficulty("D_H")
    print(f"\n🔍 Hard questions: {len(hard_questions)}")
    if hard_questions:
        print(f"   - {hard_questions[0].text[:60]}...")

    # By tags
    tagged = db.questions_by_tags(["definitions"])
    print(f"\n🔍 Questions with tag 'definitions': {len(tagged)}")


def main():
    """Run all demonstrations."""
    print("\n🚀 Phase 2 Starter Example")
    print("This demonstrates loading and using the OODB quiz database.\n")

    try:
        # Main demo
        db = print_database_summary()
        explore_question_object(db)
        show_backward_compatibility(db)
        demo_queries(db)

        print("\n" + "="*60)
        print("✨ All examples completed successfully!")
        print("="*60)
        print("\n📖 Next steps:")
        print("   1. Check README.md for architecture overview")
        print("   2. See gui/ARCHITECTURE.md for GUI roadmap")
        print("   3. Use LegacyQuizAdapter to integrate with Phase 1 code")
        print("   4. Build out REST API and frontend (Phase 3)")
        print()

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("Make sure data files exist in the data/ directory")


if __name__ == "__main__":
    main()
