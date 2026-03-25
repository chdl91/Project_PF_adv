"""
Phase 2 OODB Query Application

This package provides an object-oriented database interface for quiz questions,
decoupled from storage format or GUI framework.

Quick Start:
    from models.loader import OODBLoader
    from models.database import QuizDatabase
    
    loader = OODBLoader(data_dir="./data")
    db = loader.load_database_from_file("DIB.json")
    
    # Query examples
    topics = db.get_all_topics()
    questions = db.questions_by_difficulty("D_H")
    q = db.get_question("Q001")

For backward compatibility with Phase 1:
    from adapters import LegacyQuizAdapter
    phase1_data = LegacyQuizAdapter.to_phase1_format(db)

For more details, see README.md
"""

__version__ = "2.0.0"
__author__ = "Project Development Team"

__all__ = [
    "models",
    "adapters",
]
