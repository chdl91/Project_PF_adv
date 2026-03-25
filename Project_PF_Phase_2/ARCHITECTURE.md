# Phase 1 ↔ Phase 2 Architecture Diagram

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  YOUR PROJECT STRUCTURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Project_PF_adv/                                                 │
│  │                                                                │
│  ├─ Project_PF (Phase_1)/          ← LEGACY (Reference)         │
│  │  ├── main.py                                                  │
│  │  ├── quiz.py                                                  │
│  │  └── Data/                                                    │
│  │      ├── DIB.json               ← Phase 1 Flat Format         │
│  │      └── POM.json                                             │
│  │                                                                │
│  └─ Project_PF_Phase_2/            ← NEW (Main Development)     │
│     ├── README.md                  (Start here)                  │
│     ├── MIGRATION.md               (Data conversion guide)       │
│     ├── example.py                 (Runnable demos)              │
│     │                                                             │
│     ├── models/                    (OOP Domain Layer)            │
│     │   ├── entities.py            ← Classes: Topic, Question    │
│     │   ├── database.py            ← QuizDatabase (OODB engine)  │
│     │   └── loader.py              ← JSON ↔ Objects             │
│     │                                                             │
│     ├── adapters/                  (Transformation Layer)        │
│     │   └── legacy.py              ← PHASE 1 COMPATIBILITY!     │
│     │                                                             │
│     ├── data/                      (OODB Data)                  │
│     │   ├── DIB.json               ← Phase 2 Normalized Format   │
│     │   └── POM.json                                             │
│     │                                                             │
│     └── gui/                       (Future: Web GUI Guide)       │
│         └── ARCHITECTURE.md        (REST API + Frontend design) │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Phase 1 → Phase 2 → Future

```
                  ╔════════════════════════════════════╗
                  ║      Phase 1 Legacy Code           ║
                  ║  (quiz.py, main.py, CLI)           ║
                  ╚══════════════╤═══════════════════════╝
                                 │
                    ┌────────────┘
                    │ (NO CHANGES NEEDED!)
                    ▼
        ╔═══════════════════════════════════════════════╗
        ║    LegacyQuizAdapter (adapters/legacy.py)   ║
        ║                                              ║
        ║  Converts Phase 1 flat list format      ║
        ║  ↔ Phase 2 OODB normalized format      ║
        ╚══════════════╤═════════════════════════╝
                       │
         ┌─────────────┘
         │
         ▼
╔═════════════════════════════════════════════════════════════╗
║           Phase 2: OOP Domain Models                       ║
║                                                             ║
║  ┌──────────────────┐  ┌──────────────────┐               ║
║  │ Topic            │  │ Question         │               ║
║  │ - id             │  │ - id             │               ║
║  │ - name           │  │ - topic_id  -----┼──→ Topic      ║
║  │ - description    │  │ - text           │               ║
║  │ - questions --┐  │  │ - difficulty_id  │               ║
║  └──────────────┼──┘  │ - correct_choice_id               ║
║                 │     │ - explanation    │               ║
║                 │     │ - choices  ──┐   │               ║
║                 │     └──────────────┼───┘               ║
║                 │                    │                    ║
║            ┌────┴────────────────────┼────┐              ║
║            │                         ▼    │              ║
║  ┌─────────┴──────────┐  ┌──────────────────┐            ║
║  │ Choice             │  │ Difficulty       │            ║
║  │ - id               │  │ - id             │            ║
║  │ - question_id      │  │ - name: easy/med/hard         ║
║  │ - label: 1-4       │  │ - weight: 1.0/2.0/3.0         ║
║  │ - text             │  └──────────────────┘            ║
║  └────────────────────┘                                  ║
║                                                             ║
║  Managed by: QuizDatabase (models/database.py)           ║
║  - Provides OOP queries (get_topic, questions_by_*)      ║
║  - Handles relationships (navigation, lookups)           ║
║  - Independent of storage/GUI                           ║
╚═════════════════════════════════════════════════════════════╝
         │
         │ (can support multiple clients)
         │
    ┌────┴────────────────────────┬────────────────────┐
    ▼                             ▼                    ▼
    
╔═══════════════════╗    ╔══════════════════╗  ╔══════════════════╗
║  CLI Interface    ║    ║  REST API        ║  ║  Future: GUIs    ║
║  (Phase 1)        ║    ║  (Phase 3)       ║  ║  (Phase 3+)      ║
║                   ║    ║                  ║  ║                  ║
║  quiz.py runs ────┼────│→ FastAPI/Flask   │  │ React/Vue App    ║
║  Phase 1 format   ║    │   - GET /topics  │  │  - Web UI        ║
║  (via adapter)    ║    │   - GET /quest   │  │  - Auth          ║
║                   ║    │   - POST /answer │  │  - Analytics     ║
║  + Results CSV    │    │   - JSON resp    │  │  - Admin Panel   ║
╚═══════════════════╝    ╚══════════════════╝  ╚══════════════════╝
    ▼                         ▼                      ▼
    └─────────────────────────┴──────────────────────┘
                              ▼
                    ╔════════════════════╗
                    ║  Persistence Layer ║
                    ║                    ║
                    ║ JSON files (now)   ║
                    ║ ↓ (swap out to)    ║
                    ║ SQL Database       ║
                    ║ MongoDB            ║
                    ║ Cloud API          ║
                    ╚════════════════════╝
```

---

## Phase 1 vs Phase 2 Comparison

### Data Model Differences

**Phase 1 (Flat Array)**
```
Question Q001
  ├─ topic: "Digitalization"           (string, repeated)
  ├─ difficulty: "easy"                (string, repeated)
  ├─ answers: {1: "...", 2: "...", ...}(embedded)
  ├─ correct_answer: 2                 (number)
  └─ ...

Question Q002
  ├─ topic: "Digitalization"           (repeated again)
  ├─ difficulty: "easy"                (repeated again)
  ├─ answers: {...}
  └─ ...
```

→ **Problems:** Duplication, implicit relationships, hard to query

**Phase 2 (OODB Normalized)**
```
Topic T_Digitalization (stored once)
  ├─ Question Q001
  │   ├─ topic_id: "T_Digitalization"      (reference)
  │   ├─ difficulty_id: "D_E"              (reference)
  │   ├─ correct_choice_id: "Q001_C2"     (reference)
  │   └─ choices [...]
  │
  └─ Question Q002
      ├─ topic_id: "T_Digitalization"     (same reference)
      ├─ difficulty_id: "D_E"             (same reference)
      └─ ...

Difficulty D_E (stored once)
  ├─ Referenced by 50+ questions
  └─ (not duplicated)
```

→ **Benefits:** No duplication, explicit relationships, easy to query

---

## Migration Flow

```
Phase 1 Data File (DIB.json, ~200 questions)
        │
        │ 1. Load as phase1_data
        │
        ▼
┌─────────────────────────────────┐
│ LegacyQuizAdapter               │
│ .from_phase1_format()           │
│                                 │
│ Processes:                      │
│ - Extract unique topics         │
│ - Extract unique difficulties   │
│ - Parse answers & choices       │
│ - Map correct_answer → choice   │
│ - Assign new IDs                │
└────────────────┬────────────────┘
                 │
        ▼
    QuizDatabase (OODB)
        │
        ▼
    OODBLoader.save_database_to_file()
        │
        ▼
Phase 2 Data File (DIB.json, normalized OODB format)
        │
        ├─ Smaller file size (no duplication)
        ├─ Easier to update (edit topic once, affects all Q's)
        ├─ Better for querying (explicit relationships)
        └─ Ready for GUI integration
```

---

## Class Hierarchy & Relationships

```
┌────────────────────────────────────────────────────────────┐
│                    QuizDatabase (OODB Engine)              │
├────────────────────────────────────────────────────────────┤
│ Attributes:                                                │
│  - difficulties: Dict[id, Difficulty]                      │
│  - topics: Dict[id, Topic]                                 │
│  - questions: Dict[id, Question]                           │
│  - choices: Dict[id, Choice]                               │
│                                                            │
│ Methods:                                                   │
│  + get_topic(id) → Topic                                   │
│  + get_question(id) → Question                             │
│  + questions_by_difficulty(id) → List[Question]           │
│  + questions_by_topic(id) → List[Question]                │
│  + questions_by_tags(tags) → List[Question]               │
│  + summary() → Dict                                        │
└────────────────────────────────────────────────────────────┘
         ▲
         │
    manages
         │
    ┌────┴─────────────────────────────────────┐
    │                                           │
    │                                           │
1:N │                                        1:∞ │
    │                                           │
    ▼                                           ▼
                                        
┌──────────────────┐         ┌──────────────────────┐
│ Topic            │         │ Difficulty           │
├──────────────────┤         ├──────────────────────┤
│ id: str          │         │ id: str              │
│ name: str        │         │ name: str            │
│ description: str │         │ weight: float        │
│ questions: List  │◄────┐   │                      │
└──────────────────┘     │   └──────────────────────┘
        ▲                │           ▲
        │        1:N     │           │
        │                │           │
        │            ┌───┴─────────┐ │
        │            │             │ │
        │            ▼             │ │
        │     ┌──────────────────┐ │ │
        │     │ Question         │ │ │
        │     ├──────────────────┤ │ │
        │     │ id: str          │ │ │
        │     │ topic_id: str ───┼─┘ │
        │     │ text: str        │   │
        │     │ difficulty_id ───┼───┘
        │     │ correct_choice_id│
        │     │ explanation: str │
        │     │ choices: List ───┼───┐
        │     │ tags: List       │   │
        │     │ created_at: str  │   │
        │     └──────────────────┘   │
        │             ▲              │
        │             │          1:N │
        └─────────────┼──────────────┘
                      │
                      │
                  ┌───┴──────────────┐
                  │   1:1            │
                  │                  │
                  ▼                  ▼
                                
                ┌──────────────────┐
                │ Choice           │
                ├──────────────────┤
                │ id: str          │
                │ question_id: str │
                │ label: str (1-4) │
                │ text: str        │
                └──────────────────┘
```

---

## Integration Points

### Existing Phase 1 Code
```python
from quiz import run_quiz  # Unchanged!

# Now you can:
from models.loader import OODBLoader
from adapters import LegacyQuizAdapter

db = OODBLoader().load_database_from_file("DIB.json")
legacy_data = LegacyQuizAdapter.to_phase1_format(db)

run_quiz(legacy_data)  # Works as before!
```

### Future Phase 3 (Web GUI)
```python
from fastapi import FastAPI
from models.loader import OODBLoader

app = FastAPI()
db = OODBLoader().load_database_from_file("DIB.json")

@app.get("/api/questions/{topic_id}")
def get_questions(topic_id: str):
    questions = db.questions_by_topic(topic_id)
    return [
        {
            "id": q.id,
            "text": q.text,
            "choices": [{"label": c.label, "text": c.text} for c in q.choices]
        }
        for q in questions
    ]
```

---

**Phase 2 is designed as a solid foundation that scales from CLI to Web seamlessly.**
