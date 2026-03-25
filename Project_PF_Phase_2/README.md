# Phase 2: OODB-Based Quiz Application Architecture

## Overview

**Phase 2** builds on Phase 1 legacy code with a modern object-oriented database (OODB) structure and lays the groundwork for GUI integration.

### Key Improvements

- **Object-Oriented Design**: Questions, Topics, Choices are first-class objects with stable identities
- **Normalization**: No more duplicate topic/difficulty data in each question
- **Backward Compatible**: Phase 1 code works unchanged via `LegacyQuizAdapter`
- **GUI-Ready**: Clean separation of data, business logic, and presentation layers
- **Extensible**: Easy to add new features (filtering, analytics, persistence, caching)

---

## Directory Structure

```
Project_PF_Phase_2/
├── data/                    # OODB JSON data files
│   ├── DIB.json            # Digital Business questions (OODB format)
│   └── POM.json            # Principles of Management questions (OODB format)
├── models/                 # Core domain models and database
│   ├── __init__.py
│   ├── entities.py         # Topic, Question, Choice, Difficulty classes
│   ├── database.py         # QuizDatabase in-memory OODB
│   └── loader.py           # JSON loader/serializer
├── adapters/               # Data transformation layers
│   ├── __init__.py
│   └── legacy.py           # Phase 1 compatibility layer
├── gui/                    # Web GUI framework (future)
│   └── ARCHITECTURE.md     # GUI design guide
├── README.md              # This file
└── requirements.txt       # Python dependencies
```

---

## Core Components

### 1. Domain Models (`models/entities.py`)

**Four main entity classes:**

```python
# Difficulty level metadata
Difficulty:
  - id: str (e.g., "D_E", "D_M", "D_H")
  - name: str ("easy", "medium", "hard")
  - weight: float (1.0, 2.0, 3.0)

# A quiz question with metadata
Question:
  - id: str (e.g., "Q001")
  - topic_id: str (reference to Topic)
  - text: str (question text)
  - difficulty_id: str (reference to Difficulty)
  - correct_choice_id: str (reference to the correct Choice)
  - explanation: str
  - choices: List[Choice] (navigation property)
  - tags: List[str] (optional metadata)
  - created_at, updated_at: str (timestamps)

# A single answer choice
Choice:
  - id: str (e.g., "Q001_C1")
  - question_id: str (reference to Question)
  - label: str ("1", "2", "3", "4")
  - text: str (choice text)

# A topic/subject that groups questions
Topic:
  - id: str (e.g., "T_Digitalization")
  - name: str ("Digital Business", etc.)
  - description: str (optional)
  - questions: List[Question] (navigation property)
  - metadata: Dict[str, any]
  - created_at: str (timestamp)
```

### 2. In-Memory Database (`models/database.py`)

**QuizDatabase** provides OOP-style lookups:

```python
db = QuizDatabase()
db.add_topic(topic)
db.add_difficulty(difficulty)

# Queries
topic = db.get_topic("T_Digitalization")
question = db.get_question("Q001")
questions = db.questions_by_difficulty("D_H")
questions = db.questions_by_tags(["fundamentals", "definitions"])
```

### 3. Data Loader (`models/loader.py`)

**OODBLoader** converts JSON ↔ OOP objects:

```python
# Load from JSON
loader = OODBLoader(data_dir="./data")
db = loader.load_database_from_file("DIB.json")

# Save back to JSON
loader.save_database_to_file(db, "DIB_modified.json")
```

**OODB JSON Schema** (normalized structure):

```json
{
  "schema_version": "2.0",
  "objects": {
    "difficulties": [
      { "id": "D_E", "name": "easy", "weight": 1.0 },
      ...
    ],
    "topics": [
      { "id": "T_Digitalization", "name": "Digitalization", ... },
      ...
    ],
    "questions": [
      {
        "id": "Q001",
        "topic_id": "T_Digitalization",
        "text": "What best describes...",
        "difficulty_id": "D_E",
        "correct_choice_id": "Q001_C2",
        "explanation": "...",
        "tags": ["fundamentals"]
      },
      ...
    ],
    "choices": [
      {
        "id": "Q001_C1",
        "question_id": "Q001",
        "label": "1",
        "text": "Option 1 text"
      },
      ...
    ]
  }
}
```

### 4. Legacy Adapter (`adapters/legacy.py`)

**Converts OODB ↔ Phase 1 flat list format:**

```python
# Phase 1 format (flat list)
[
  {
    "topic": "Digital Business",
    "question": "What best describes...",
    "answers": {"1": "...", "2": "...", "3": "...", "4": "..."},
    "correct_answer": 2,
    "explanation": "...",
    "difficulty": "easy",
    "id": "Q001"
  },
  ...
]

# Convert to Phase 1 format for existing quiz.py
from adapters import LegacyQuizAdapter
phase1_data = LegacyQuizAdapter.to_phase1_format(db)
run_quiz(phase1_data)  # Phase 1 code works unchanged!
```

---

## Usage Examples

### Load and Use OODB

```python
from models.loader import OODBLoader
from models.database import QuizDatabase

# Load data
loader = OODBLoader(data_dir="./data")
db = loader.load_database_from_file("DIB.json")

# Inspect data
print(db.summary())

# Query examples
topic = db.get_topic("T_Digitalization")
print(f"Topic: {topic.name}, {topic.question_count()} questions")

hard_questions = db.questions_by_difficulty("D_H")
print(f"Found {len(hard_questions)} hard questions")

# Navigate objects
question = db.get_question("Q001")
print(f"Question: {question.text}")
print(f"Correct answer: {question.get_correct_answer_number()}")
for choice in question.choices:
    is_correct = choice.id == question.correct_choice_id
    mark = "✓" if is_correct else " "
    print(f"  [{mark}] {choice.label}. {choice.text}")
```

### Use with Phase 1 Code (Backward Compat)

```python
from models.loader import OODBLoader
from adapters import LegacyQuizAdapter
from quiz import run_quiz  # Phase 1 code unchanged

# Load OODB
loader = OODBLoader()
db = loader.load_database_from_file("DIB.json")

# Convert to Phase 1 format
phase1_data = LegacyQuizAdapter.to_phase1_format(db)

# Run with existing Phase 1 code
result = run_quiz(phase1_data)
```

### Migrate Phase 1 Data to OODB

```python
import json
from adapters import LegacyQuizAdapter
from models.loader import OODBLoader

# Load old Phase 1 JSON
with open("../Project_PF (Phase_1)/Data/DIB.json") as f:
    legacy_data = json.load(f)

# Convert to OODB
db = LegacyQuizAdapter.from_phase1_format(legacy_data)

# Save new format
loader = OODBLoader()
loader.save_database_to_file(db, "DIB_migrated.json")
```

---

## Phase 2 vs Phase 1

| Aspect | Phase 1 | Phase 2 |
|---------|---------|---------|
| **Data Structure** | Flat array | Normalized OODB graph |
| **Relationships** | Implicit (repeating values) | Explicit (ID references) |
| **Topic Storage** | Duplicated in each question | Stored once, referenced |
| **Difficulty** | String in each question | Separate Difficulty objects |
| **OOP** | Dict-based | Class-based (Topic, Question, etc.) |
| **Queries** | Manual filtering | Database methods |
| **Extensibility** | Hard (add fields everywhere) | Easy (update entities) |
| **GUI Support** | Not designed for | Built-in (clean separation) |
| **Compatibility** | ✗ | ✓ Via LegacyQuizAdapter |

---

## Future Integration: Web GUI

### Architecture (Best Practices Guide)

**See `gui/ARCHITECTURE.md` for detailed design.**

**High-level stack recommendation:**

```
┌─────────────────────────────────────────────────────┐
│            Frontend (React/Vue.js)                  │
│  - Component library, state management              │
│  - Quiz UI, results dashboard, admin panel          │
└──────────────────────────────────────────────────────┘
                        ↓ HTTP/REST ↓
┌──────────────────────────────────────────────────────┐
│        Backend API (FastAPI or Flask)                │
│  - REST endpoints for questions, topics, results     │
│  - Authentication, validation, caching               │
│  - Results export (CSV, JSON)                        │
└──────────────────────────────────────────────────────┘
                        ↓ Import ↓
┌──────────────────────────────────────────────────────┐
│    Phase 2 Core (models + adapters)                  │
│  - OODB data model, business logic                   │
│  - No GUI dependencies (testable)                    │
└──────────────────────────────────────────────────────┘
                        ↓ Load ↓
┌──────────────────────────────────────────────────────┐
│         Persistence Layer                            │
│  - JSON files, SQL database, or cloud storage        │
└──────────────────────────────────────────────────────┘
```

**Key principles:**

1. **Separation of concerns**: Core logic isolated from web framework
2. **Statelessness**: API is functional, tests don't need a server
3. **Flexible persistence**: Can swap JSON → SQL/MongoDB without changing models
4. **Caching layer**: Between API and database for performance

---

## Next Steps

### Immediate (Foundation)
- [ ] Complete migration of all Phase 1 questions to OODB format
- [ ] Test backward compatibility with Phase 1 code
- [ ] Add unit tests for loader and adapters

### Short-term (Enhancement)
- [ ] Add SQL persistence layer (SQLAlchemy)
- [ ] Create REST API skeleton (FastAPI)
- [ ] Add filtering and search capabilities
- [ ] Implement results tracking database

### Medium-term (GUI)
- [ ] Build React/Vue frontend
- [ ] Add admin panel for question management
- [ ] Implement user authentication
- [ ] Create analytics dashboard

### Long-term (Scale)
- [ ] Add caching (Redis)
- [ ] Implement deployment pipeline
- [ ] Add CI/CD testing
- [ ] Performance monitoring

---

## Dependencies

```
python>=3.8
```

No external dependencies required for core OODB functionality.
When GUI is added:
```
fastapi
uvicorn
pydantic
sqlalchemy  # if using SQL
redis  # if adding caching
```

---

## Key Files to Reference

- **Phase 1 reference**: `../Project_PF (Phase_1)/quiz.py`
- **Legacy tests**: Use Phase 1 questions with adapter to verify compatibility
- **Data schema**: See `data/DIB.json` for OODB JSON structure
- **GUI roadmap**: `gui/ARCHITECTURE.md` (coming soon)

---

**Phase 2 is designed to be a solid foundation that grows with your project.**
