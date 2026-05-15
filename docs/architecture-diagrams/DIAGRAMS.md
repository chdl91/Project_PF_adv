# Architecture Diagrams

All diagrams reflect the current project structure after the OOP/N-Tier refactor.
Paste any block into [mermaid.live](https://mermaid.live) to export as PNG.

---

## 01 — ER Diagram

> Shows all database tables, their fields, and relationships.
> `QuizResult` is now a separate table — quiz scores are no longer stored in `User`.

```mermaid
erDiagram
    SUBJECT {
        int subject_id PK
        string subject_name UK
    }
    TOPIC {
        int topic_id PK
        string topic_name
        int subject_id FK
    }
    QUESTION {
        int question_id PK
        int topic_id FK
        string question_text
        int correct_answer FK
        string difficulty
    }
    ANSWER {
        int answer_id PK
        int question_id FK
        string answer_text
    }
    USER {
        int user_id PK
        string user_name UK
        boolean admin_status
    }
    QUIZ_RESULT {
        int result_id PK
        string user_name
        int subject_id FK
        int score
        int total_questions
        string timestamp
    }

    SUBJECT  ||--o{ TOPIC       : "contains"
    TOPIC    ||--o{ QUESTION    : "contains"
    QUESTION ||--o{ ANSWER      : "has"
    QUESTION }o--|| ANSWER      : "correct_answer"
    USER     ||--o{ QUIZ_RESULT : "takes"
```

---

## 02 — Class Diagram

> Shows all classes across all layers and how they depend on each other.
> Calls flow downward (UI → Service → DAO → DB). Data returns upward.

```mermaid
classDiagram
    %% ── Domain models ──────────────────────────────────────────
    class Subject {
        +int subject_id
        +str subject_name
    }
    class Topic {
        +int topic_id
        +str topic_name
        +int subject_id
    }
    class Question {
        +int question_id
        +int topic_id
        +str question_text
        +int correct_answer
        +str difficulty
    }
    class Answer {
        +int answer_id
        +int question_id
        +str answer_text
    }
    class User {
        +int user_id
        +str user_name
        +bool admin_status
    }
    class QuizResult {
        +int result_id
        +str user_name
        +str subject_name
        +int score
        +int total_questions
        +str timestamp
    }

    Subject  "1" --> "many" Topic       : contains
    Topic    "1" --> "many" Question    : contains
    Question "1" --> "many" Answer      : has
    Question      -->       Answer      : correct_answer
    User     "1" --> "many" QuizResult  : takes

    %% ── Data access layer ───────────────────────────────────────
    class Database {
        +engine
        +__init__(db_path)
        +get_session()
    }
    class UserDAO {
        +find_by_name(username)
        +create(username)
    }
    class SubjectDAO {
        +get_all()
        +get_by_name(name)
        +get_topics(subject_id)
        +add_subject(name)
        +add_topic(name, subject_id)
        +delete_topic(topic_id)
        +delete_subject(subject_id)
    }
    class QuestionDAO {
        +get_by_topic(topic_id, difficulty)
        +get_answers(question_id)
        +add(topic_id, text, answers, correct_idx, difficulty)
        +delete(question_id)
    }
    class ScoreDAO {
        +save(user_name, subject_name, score, total)
        +get_top(limit)
    }

    Database <-- UserDAO     : uses
    Database <-- SubjectDAO  : uses
    Database <-- QuestionDAO : uses
    Database <-- ScoreDAO    : uses

    %% ── Service layer ───────────────────────────────────────────
    class UserService {
        +get_or_create_user(username)
    }
    class SubjectService {
        +get_all_subjects()
        +get_subject_id_by_name(name)
        +get_topics_with_ids_by_subject(name)
        +add_subject(name)
        +add_topic(topic_name, subject_id)
        +delete_topic(topic_id)
        +delete_subject(subject_id)
    }
    class QuestionService {
        +get_questions_with_answers(topic_id, difficulty)
        +add_question(topic_id, text, answers, correct_idx, difficulty)
        +delete_question(question_id)
    }
    class ScoreService {
        +save_quiz_result(username, subject, score, total)
        +get_top_scores(limit)
    }
    class QuizSessionService {
        +active_sessions Dict
        +start_quiz_session(username, subject, n, difficulty)
        +validate_answer(session_id, answer_id)
        +submit_answer(session_id, answer_id)
        +get_quiz_progress(session_id)
        +end_quiz_session(session_id)
    }

    UserDAO     <-- UserService     : uses
    SubjectDAO  <-- SubjectService  : uses
    QuestionDAO <-- QuestionService : uses
    ScoreDAO    <-- ScoreService    : uses

    SubjectService  <-- QuizSessionService : uses
    QuestionService <-- QuizSessionService : uses
    ScoreService    <-- QuizSessionService : uses

    %% ── Presentation layer ──────────────────────────────────────
    class QuizCLI {
        +run()
        +login()
        +user_mode(username)
        +admin_mode(username)
        +run_quiz(username, subject, n, difficulty)
        +view_scoreboard()
    }
    class QuizGUI {
        +run()
    }

    UserService        <-- QuizCLI : uses
    SubjectService     <-- QuizCLI : uses
    QuestionService    <-- QuizCLI : uses
    ScoreService       <-- QuizCLI : uses
    QuizSessionService <-- QuizCLI : uses

    UserService        <-- QuizGUI : uses
    SubjectService     <-- QuizGUI : uses
    QuestionService    <-- QuizGUI : uses
    ScoreService       <-- QuizGUI : uses
    QuizSessionService <-- QuizGUI : uses
```

---

## 03 — N-Tier Architecture Diagram

> Shows the four layers and the single entry point (`__main__.py`).
> Dashed arrows = planned (NiceGUI, to be implemented).

```mermaid
graph TB
    MAIN["__main__.py\n(wires all layers)"]

    subgraph UI["Presentation Layer — ui/"]
        CLI["QuizCLI\ncli.py"]
        GUI["QuizGUI\ngui.py\n(NiceGUI — planned)"]
    end

    subgraph SVC["Service Layer — services/"]
        US["UserService"]
        SS["SubjectService"]
        QS["QuestionService"]
        SCS["ScoreService"]
        QSS["QuizSessionService"]
    end

    subgraph DAL["Data Access Layer — data_access/"]
        DB["Database\ndb.py\n(Facade)"]
        UDAO["UserDAO"]
        SDAO["SubjectDAO"]
        QDAO["QuestionDAO"]
        SCDAO["ScoreDAO"]
    end

    subgraph DOM["Domain — domain/"]
        MOD["models.py\nSubject · Topic · Question\nAnswer · User · QuizResult"]
    end

    DATABASE[("SQLite\nDB/quiz.db")]

    MAIN --> CLI
    MAIN -.-> GUI

    CLI  --> US & SS & QS & SCS & QSS
    GUI  -.-> US & SS & QS & SCS & QSS

    QSS  --> SS & QS & SCS

    US   --> UDAO
    SS   --> SDAO
    QS   --> QDAO
    SCS  --> SCDAO

    UDAO  & SDAO & QDAO & SCDAO --> DB
    DB --> DATABASE

    UDAO  & SDAO & QDAO & SCDAO -. uses .-> MOD
```

---

## 04 — Sequence Diagram: Take a Quiz

> Shows the complete flow when a user takes a quiz, from login to final score.
> Key change: results are saved to `QUIZ_RESULT`, not `USER`.

```mermaid
sequenceDiagram
    actor User
    participant CLI  as QuizCLI
    participant QSS  as QuizSessionService
    participant SS   as SubjectService
    participant QS   as QuestionService
    participant SCS  as ScoreService
    participant DAO  as DAOs
    participant DB   as SQLite

    User ->> CLI : Enter username
    CLI  ->> CLI : login() → get_or_create_user()
    CLI -->> User : Welcome message

    User ->> CLI : Select subject, difficulty, # questions
    CLI  ->> QSS : start_quiz_session(username, subject, n, difficulty)

    QSS  ->> SS  : get_topics_with_ids_by_subject(subject)
    SS   ->> DAO : SubjectDAO.get_by_name() / get_topics()
    DAO  ->> DB  : SELECT Subject, Topic
    DB  -->> DAO : rows
    DAO -->> SS  : List[Topic]
    SS  -->> QSS : List[dict]

    QSS  ->> QS  : get_questions_with_answers(topic_id, difficulty)
    QS   ->> DAO : QuestionDAO.get_by_topic() / get_answers()
    DAO  ->> DB  : SELECT Question, Answer
    DB  -->> DAO : rows
    DAO -->> QS  : List[Question + Answer]
    QS  -->> QSS : List[dict]

    Note over QSS : Randomly sample n questions<br/>Store session in active_sessions{}
    QSS -->> CLI : (session_id, first_question)
    CLI -->> User : Display question + answers

    loop For each question
        User ->> CLI : Select answer (1–4)
        CLI  ->> QSS : submit_answer(session_id, answer_id)
        Note over QSS : validate_answer()<br/>update score & current_idx
        QSS -->> CLI : {is_correct, score, next_question, quiz_complete}
        CLI -->> User : Show feedback + next question
    end

    CLI  ->> QSS : end_quiz_session(session_id)
    QSS  ->> SCS : save_quiz_result(username, subject, score, total)
    SCS  ->> DAO : ScoreDAO.save(...)
    DAO  ->> DB  : INSERT INTO quizresult
    DB  -->> DAO : OK
    DAO -->> SCS : QuizResult
    SCS -->> QSS : True

    Note over QSS : Delete session from active_sessions{}
    QSS -->> CLI : {score, percentage, grade}
    CLI -->> User : Show final results + grade
```

---

## 05 — Use Case Diagram

> Shows all features available to each actor. No code changes affect this diagram.

```mermaid
graph LR
    subgraph Admin["Admin Features"]
        A1[Admin Login]
        A2[Add Subject]
        A3[Add Topic]
        A4[Add Question]
        A5[Delete Question]
        A6[Delete Topic]
        A7[Delete Subject]
    end

    subgraph User["User Features"]
        U1[Login / Register]
        U2[Select Subject]
        U3[Select Difficulty]
        U4[Take Quiz]
        U5[Answer Questions]
        U6[View Score]
        U7[View Scoreboard]
    end

    ADMIN((Admin)) --> A1 & A2 & A3 & A4 & A5 & A6 & A7
    USR((User))    --> U1 & U2 & U3 & U4 & U5 & U6 & U7
```
