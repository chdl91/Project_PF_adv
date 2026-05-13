# Design Decisions

Explains the key choices made in the OOP refactor of this project.

---

## Why these 4 service classes?

Each class owns **one domain** of the application. This mirrors how you'd describe the real world:

| Class | Owns | Real-world analogy |
|---|---|---|
| `UserService` | Who is logged in | A receptionist |
| `SubjectService` | What subjects/topics exist | A librarian |
| `QuestionService` | The actual quiz content | A question bank |
| `ScoreService` | Results and rankings | A scoreboard |

If the lecturer later says "add a timer to each quiz result", you touch only `ScoreService`. If they say "add tags to questions", you touch only `QuestionService`. Nothing else changes.

---

## Why does every class get `engine` injected in `__init__`?

```python
class QuestionService:
    def __init__(self, engine):
        self.engine = engine
```

The alternative would be a **global variable** at the top of the file (which is what the original code had):

```python
ENGINE = create_engine(...)  # old approach - bad
```

The problem with a global: every class in every file automatically uses the **same, hardcoded** database. You can never test with a fake database. You can never swap it out.

With injection, the **caller decides** which database to use:

```python
# Production
db_engine = create_engine("sqlite:///DB/quiz.db")

# Testing
test_engine = create_engine("sqlite:///:memory:")

svc = QuestionService(test_engine)  # no code change needed
```

---

## Why does `QuizEngine` receive services instead of importing them?

```python
class QuizEngine:
    def __init__(self, subject_service, question_service, score_service):
```

`QuizEngine` needs to fetch questions and save results — but it shouldn't care *how* those things happen. By receiving the services as parameters, you could later pass in a `MockQuestionService` that returns fake questions for testing, without touching `QuizEngine` at all.

This is the core idea behind **"swap out easily"** — the lecturer's requirement.

---

## Why do functions return dictionaries instead of objects?

For example:

```python
def get_or_create_user(self, username) -> dict:
    return {
        "user_id": 1,
        "user_name": "Alice",
        "admin_status": False,
        "is_new": True
    }
```

**Reason 1 — Loose coupling.** If `get_or_create_user` returned a `User` SQLModel object, then `quiz.py` would need to import `User` from `DB_classes.py`. With dictionaries, `quiz.py` knows nothing about the database layer — it just gets plain data.

**Reason 2 — The GUI won't break.** When `quiz_gui.py` is built, it calls the exact same services and gets the exact same dictionaries. No changes needed to the service layer.

**Reason 3 — Dictionaries are self-documenting at call sites.** Compare:

```python
# With object — what fields does this have?
user = service.get_or_create_user("Alice")
user.???

# With dict — immediately readable
user = service.get_or_create_user("Alice")
if user["admin_status"]:
    ...
```

The tradeoff is you lose type-checking on the dict contents. A production app would use a dataclass or Pydantic model instead. For this project, dicts are the right level of complexity.

---

## Why does `QuizCLI` get all 4 services AND the engine?

```python
class QuizCLI:
    def __init__(self, user_service, subject_service, question_service, score_service, quiz_engine):
```

Each dependency is needed for a specific job:

| Dependency | Used in |
|---|---|
| `user_service` | `login()` |
| `subject_service` | `select_subject()`, `admin_mode()` (add/delete topics) |
| `question_service` | Counting available questions, `admin_mode()` (add/delete questions) |
| `score_service` | `view_scoreboard()` |
| `quiz_engine` | `run_quiz()` — the full quiz loop |

`QuizCLI` does **only** user input and display. All actual logic lives in the services and engine. A future `QuizGUI` class would have the same constructor signature, just different output methods (buttons instead of `print()`).

---

## The wiring in `__main__` — why does it matter?

```python
if __name__ == "__main__":
    db_engine    = create_engine(...)
    user_svc     = UserService(db_engine)
    subject_svc  = SubjectService(db_engine)
    question_svc = QuestionService(db_engine)
    score_svc    = ScoreService(db_engine)
    engine       = QuizEngine(subject_svc, question_svc, score_svc)
    cli          = QuizCLI(user_svc, subject_svc, question_svc, score_svc, engine)
    cli.run()
```

This one block is the **only place** where all the pieces are connected. To switch to a GUI, you change one line:

```python
# CLI
cli = QuizCLI(user_svc, subject_svc, question_svc, score_svc, engine)

# GUI (future)
gui = QuizGUI(user_svc, subject_svc, question_svc, score_svc, engine)
```

All services and the engine stay identical. This is the entire point of OOP with dependency injection — the structure forces a clean separation between *what the app does* and *how it shows it*.
