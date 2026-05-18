
---

# 🐍 Big Snek Quiz - Advanced Programming Project

> 🚧 Replace the screenshot with one that shows your main screen.

[UI Showcase](docs/ui-images/ui_user_menu.png)

---

This project is intended to:

- Practice the complete process from **application requirements analysis to implementation**
- Apply advanced **Python** concepts in a browser-based application (NiceGUI)
- Demonstrate **data validation**, a clean architecture (presentation / application logic / persistence), and **database access via ORM**
- Produce clean, well-structured, and documented code (incl. tests)
- Prepare students for **teamwork and professional documentation**
- Use this repository as a starting point by importing it into your own GitHub account  
- Work only within your own copy — do not push to the original template  
- Commit regularly to track your progress

---

# 🍕 TEMPLATE for documentation

> 🚧 Please remove the paragraphs marked with "🚧". These are comments for preparing the documentation.

---

## � Documentation & Resources

- [UI Screenshots & Images](docs/ui-images/) - Visual documentation and UI mockups
- [Architecture Diagrams](docs/architecture-diagrams/) - System design and architecture
- [Design Decisions](Project_PF_Phase_2/DESIGN_DECISIONS.md) - Key design decisions and rationale

---

## �📝 Application Requirements

---

### Problem *Added from Phase 1*

> We learn a lot of material in this semester that is crucial to our further education. This can be overwhelming or even frightening. The material is spread over various Moodles / Inside FHNW, which is chaotic.

---

### Scenario *Added  from Phase 1*

> To enhance the learning process we aim to crate a catalouge of questions which will be presented as a quiz to prepare for our assesment exams. The quiz will be asking questions from one subject and split into chapters. The type of questions will be mulitple choice. The Answers will be validated and give an indication of right or wrong. At the end of the quiz, the user will be given a score.

---

## User Stories

### 1. View Quiz Menu
**As a user, I want to be able to choose between Digital Business (DIB) Quizes and Principles of Management (POM) Quizes**  
**Description:** The application displays a menu and choice of quizes for the user to select
**Inputs:**  The user can choose between two types of quizes
**Outputs:** Confirmation of choice (internally calling selected quiz) 
**Why:** Enables an easy entry point and selection of the desired subject area.
**Role affected:** Users (students) who want to start a quiz.
**Benefit:** Faster orientation, fewer mistakes, and a clear starting point for quiz workflows.

### 2. Select and run a quiz 
**As a user, I want to be able to quiz my knowledge in DIB or POM**  
**Description:** The application displays a collection of quiz questions and the a multiple choice selection of answers  
**Inputs:**  Choice of an answer (Four choices) 
**Outputs:** Confirmation of choice and correction if incorrect (internally: "list[attempt_answers]) 
**Why:** Core functionality for knowledge checking and reinforcement.
**Role affected:** Learners practicing and repeating exam material.
**Benefit:** Immediate feedback on knowledge level, supports focused learning and self-assessment.

### 3. Select the difficulty of quiz 
**As a user, I want to select the difficulty of the previously selected subject in order to challenge and improve my current knowledge**  
**Description:** The application displays a menu with three possible difficulties (Easy, Medium and Hard) and a choice for a random selection of questions for the user to select and proceed with
**Inputs:**  Choice of difficulty option (Three choices plus random choice)
**Outputs:** Confirmation of choice (internally calling the next step in quiz_setup)
**Why:** Allows adjusting difficulty to the learner's level and goals.
**Role affected:** Users who want easier or more challenging material.
**Benefit:** Improved motivation, appropriate challenge, and personalized training.

### 4. Select the individual topics within the subject itself
**As a user, I want to select the topic within the previously selected subject and quiz my knowledge in the selected topics only in order to focus my learning goals and possible weaknesses**  
**Description:** The application displays available topics within the database in a menu, including a random option of questions 
**Inputs:**  Choice of a single topic 
**Outputs:** Confirmation of choice (internally calling the next step in quiz_setup)
**Why:** Enables targeted practice of specific topic areas.
**Role affected:** Learners with specific knowledge gaps or learning goals.
**Benefit:** More efficient use of study time by focusing on weaknesses.

### 5. Select the amount of questions the user can complete in their attempt
**As a user, I want to select the amount of questions I can attempt in my quiz**  
**Description:** The application displays an option to select an amount of questions
**Inputs:**  Choice of a number of questions (minimum of 5 questions)
**Outputs:** Confirmation of choice (internally calling the next step in quiz_setup)
**Why:** Allows flexible time planning and adjustment to available study time.
**Role affected:** Users with varying availability or attention span.
**Benefit:** Higher user satisfaction through control over quiz length and duration.

### 6. Quit and return to main menu 
**As a user, I want to able to return to the menu at anytime in order to restart my quiz setup and the quiz itself**  
**Description:** At all times, during the quiz setup and the quiz attempt itself, the user has the possibility to return to the starting menu
**Inputs:**  User has a return choice
**Outputs:** Confirmation of choice (internally, stop attempt and return to )
**Why:** Necessary safety feature for interruptions and accidental actions.
**Role affected:** All users, especially those with time constraints or technical issues.
**Benefit:** Prevents data loss, improves UX, and gives users control over the flow.

### 7. Point Counter
**As a user, I want a point counter/final grade/percentage presented, in order to check my performance.**  
**Description:** The application displays the results of the finished attempt and shows the score (correct questions out of total), grade and percentage.
**Inputs:**  internally recognizing the users choice and adding to counter if correct choice has been selected
**Outputs:** internally calling the results.csv and creating a new entry with achieved score, date, time, final grade and percentage reached 
**Why:** Measurable results are central for tracking learning progress and evaluation.
**Role affected:** Learners who want to check their performance; instructors (optional).
**Benefit:** Clear performance overview enabling reflection and targeted improvement.

### 8. Scoreboard (Arcade Format)
**As a User, I want to be able to see my score in a scoreboard with other local users in order to compare my final attempt score with previous attempts**  
**Description:** Once an attempt is complete, the user is able to view their score and input a user name into a scoreboard
**Inputs:**  Username entry ("str" and limited characters, excluding special characters)
**Outputs:** Confirmation of choice (internally: results.csv)
**Why:** A competitive element that motivates repeated practice.
**Role affected:** Users who seek motivation through comparison; community-oriented features.
**Benefit:** Increases motivation, engagement, and encourages repeated practice.

### 9. Admin Login
**As an Admin, I want to be able to login to a separate Admin Panel with a password in order to manage to data**  
**Description:** To gain entry into the Admin Panel, a correct answer must be entered.  
**Inputs:**  Admin Password (Hardcoded) and input from admin user
**Outputs:** -
**Why:** Protects administrative functions from unauthorized access.
**Role affected:** Administrators (instructors/maintainers) with elevated privileges.
**Benefit:** Ensures integrity of the question database and prevents unwanted changes.

### 10. Admin - Add questions
**As an Admin, I want to be able to add questions, in order to keep the quiz relevant.**  
**Description:** In the form of an Admin Panel, the Admin has the ability to add questions, including assigning them to a subject, topic and difficulty. 
**Inputs:**  Input from admin user
**Outputs:** New Question is added to the database
**Why:** Allows updating and expanding the question pool.
**Role affected:** Administrators / content owners.
**Benefit:** Keeps the quiz up-to-date, supports course alignment and quality control.

### 11. Admin - Remove questions
**As an Admin, I want to be able to remove questions, in order to keep the quiz relevant.**  
**Description:** In the form of an Admin Panel, the Admin has the ability to delete questions from the database.
**Inputs:**  Input from admin user
**Outputs:** (Confirmation of deletion)
**Why:** Removing outdated or incorrect questions is necessary for data quality.
**Role affected:** Administrators with moderation privileges.
**Benefit:** Clean, reliable question pool and avoidance of incorrect learning content.

### 12. Admin - Confirmation of deletion
**As an Admin, I want to receive a confirmation before permanently deleting a question**  
**Description:** After having selected the Question ID and chosen "Delete", the admin must receieve a confirmation that this was correctly chosen.  
**Inputs:**  Input from admin user 
**Outputs:** Confirmation of deletion
**Why:** Prevents accidental deletion through an extra confirmation step.
**Role affected:** Administrators performing delete actions.
**Benefit:** Protects against data loss and enables controlled changes.

### Use cases

![UML Use Case Diagram]

**Use cases**
## Main Use Cases

- Show Menu
- Select Subject 
- Select Parameters for Quiz
   - Select Topic(s)
   - Select Difficulty
   - Select Number of Questions
- Answer Questions
   - Receive an Explanation if incorrect answer was made
- Show result 
   - Grade 
   - Points 
   - Percentage
- See the Scoreboard at the end of an attempt
- Return to Menu at any point in time
- As an Admin, have the ability to add questions
- As an Admin, have the ability to remove questions


**Actors**
- User (Attempts Quiz)
- Admin (Manage questions for the quiz)

---

### Mockups

> 🚧 Add screenshots of the wireframe mockups you chose to implement.

[View UI Images & Mockups](docs/ui-images/ui_login.png)
[View UI Images & Mockups](docs/ui-images/ui_user_menu.png)
[View UI Images & Mockups](docs/ui-images/ui_start_quiz.png)
[View UI Images & Mockups](docs/ui-images/ui_question_and_answers.png)
[View UI Images & Mockups](docs/ui-images/ui_question_and_answers_correction.png)
[View UI Images & Mockups](docs/ui-images/ui_scoreboard.png)
[View UI Images & Mockups](docs/ui-images/ui_admin_login.png)
[View UI Images & Mockups](docs/ui-images/ui_admin_panel.png)
[View UI Images & Mockups](docs/ui-images/ui_admin_add_question.png)
[View UI Images & Mockups](docs/ui-images/ui_admin_delete_question.png)
[View UI Images & Mockups](docs/ui-images/ui_admin_confirmation_delete.png)

---

## 🏛️ Architecture

Software Architecture (Layers)
┌─────────────────────┐
│   GUI Layer         │  ← Nice GUI
├─────────────────────┤
│   quiz.py (CLI)     │  ← User interface
├─────────────────────┤
│  Services (Folder)  │  ← Core quiz logic (reusable)
│                     │  ← Database operations
├─────────────────────┤
│  SQLModel + SQLite  │  ← Data persistence
└─────────────────────┘

## 🧪 Tests

The repository now includes a separate `test/` folder for pytest-based checks.

Install the dev dependency and run the suite with:

```bash
pip install -r requirements-dev.txt
pytest
```

The starter tests avoid the live database and use in-memory or temporary SQLite files instead.

User Story Flow (Now with Subject Selection)

┌──────────────────────────────────────────────────────────────────┐
│                    MAIN MENU                                     │
├──────────────────────────────────────────────────────────────────┤
│  1. User Mode (Stories 1-7)                                      │
│  2. Admin Mode (Story 8)                                         │
│  3. Exit                                                         │
└──────────────────────────────────────────────────────────────────┘
        │                                         │
        ▼                                         ▼
    ┌──────────────────────┐       ┌────────────────────────────┐
    │   USER MODE          │       │     ADMIN MODE             │
    ├──────────────────────┤       ├────────────────────────────┤
    │ 1. Select Subject    │       │ 1. Add Question (S8)       │
    │    (Story 1)         │       │    - Select subject/topic  │
    │    DIB or POM        │       │    - Question text         │
    │                      │       │    - 4 Answers             │
    │ 2. Select Topic      │       │    - Correct answer        │
    │    (Story 4)         │       │    - Explanation           │
    │    (from selected    │       │    - Difficulty            │
    │     subject)         │       │                            │
    │                      │       │ 2. Remove Question (S8)    │
    │ 3. Select Difficulty │       │    - Select Question ID    │
    │    (Story 3)         │       │    - Confirmation of       │
    │    Easy/Medium/Hard  │       │      Termination           │
    │                      │       │                            │
    │ 4. Run Quiz          │       │ 3. Return to Main          │
    │    (Story 2)         │       │                            │
    │    - Display Q&A     │       │ 4. Exit                    │
    │    - Validate answer │       │                            │
    │    - Show results    │       │                            │
    │                      │       │                            │
    │ 5. View Scoreboard   │       │                            │
    │    (Story 7)         │       │                            │
    │    - Top scores      │       │                            │
    │                      │       │                            │
    │ 6. Exit              │       │                            │
    │                      │       │                            │
    │ (S1-S7)              │       │                            │
    └──────────────────────┘       └────────────────────────────┘


Database Schema (Hierarchical Structure)

Subject (subject areas)
├─ subject_id (primary key)
└─ subject_name (e.g., "Digital Business", "Principles of Management")

Topic (topics within subjects)
├─ topic_id (primary key)
├─ topic_name (e.g., "Digitalization", "Leadership")
└─ subject_id (foreign key → Subject)

Question (quiz questions)
├─ question_id
├─ topic_id (foreign key → Topic)
├─ question_text
├─ correct_answer (foreign key → Answer.answer_id)
└─ difficulty ("easy", "medium", "hard")

Answer (possible answers for each question)
├─ answer_id
├─ question_id (foreign key → Question)
└─ answer_text

User (quiz results & admin accounts)
├─ user_id (primary key)
├─ user_name (max 30 chars)
├─ user_score
├─ user_timestamp
└─ admin_status (boolean)

 

### Software Architecture

> 🚧 Insert your UML class diagram(s). Split into multiple diagrams if needed.

![UML Class Diagram] -> Diagrams.md

**Layers / components:**
- UI (NiceGUI pages/components, browser as thin client)
- Application logic (controllers + domain/services)
- Persistence (SQLite + ORM entities + repositories/queries)

**Design decisions (examples):**          #Composite Pattern
- Organize code using **MVC**:
   - **Model:** domain + ORM entities (e.g. "domain.models.Question")
   - **View:** NiceGUI UI components/pages 
   - **Controller:** event handlers and coordination logic between UI, services, and persistence (e.g.`quiz_service.py` )
- Separate UI (`app/main.py`) from domain logic (e.g. ``) and persistence (e.g. `models.py`, `db.py`)
- Use and interaction of modules to minimize dependencies, by minimizing cohesion and maximizing coupling
- Keep business rules testable without starting the UI

**Design patterns used (examples):**
- MVC (Model–View–Controller)
- Repository/DAO for database access (e.g. `queries.py`)
- Strategy for business rules (e.g. discount calculation)
- Adapter for external services (e.g. invoice generation backend)

---

### 🗄️ Database and ORM

> 🚧 Describe the database and your ORM entities. Ideally, a diagram documents the database and it is described together with the ORM entities.

![ER Diagram] -> Diagrams.md

**ORM and Entities (example):** In our project, data is persisted in an SQLite database and mapped to Python entities using SQLModel (ORM). The core entities are Subject, Topic, Question, Answer, User, and QuizResult. 
The relationship chain:

                     Subject -> Topic -> Question -> Answer 

ensures hierarchical quiz data integrity: each Topic belongs to one Subject, each Question belongs to one Topic, and each Answer belongs to one Question. 
In addition, Question.correct_answer references a valid Answer entry. User-related data is managed through User (account/admin information) and QuizResult (stored scores and attempt results).

---

## ✅ Project Requirements

---

> 🚧 Requirements act as a contract: implement and demonstrate each point below.

Each app must meet the following criteria in order to be accepted (see also the official project guidelines PDF on Moodle):

1. Using NiceGUI for building an interactive web app
2. Data validation in the app
3. Using an ORM for database management

---

### 1. Browser-based App (NiceGUI)

> 🚧 In this section, document how your project fulfills each criterion.

The application interacts with the user via the browser. Users can:

- Login through a username of their choice
- Select "Start Quiz"
- Select the parameters of their quiz, including subject, topic, difficulty and number of questions
- End their quiz at any time and still receive a grading based on achieved progress
- View their score and compare it to previous and other users in "View Scoreboard"

- Admins can log in through a (hardcoded) password
- Admins have access to the Admin Panel and can manage questions (Add and Remove)
- The added or removed questions are linked to the database.

**Architecture note (per SS26 guidelines):** the browser is a thin client; UI state + business logic live on the server-side NiceGUI app.

---

### 2. Data Validation

The application validates all user input to ensure data integrity and a smooth user experience.
These checks prevent crashes and guide the user to provide correct input, matching the validation requirements described in the project guidelines.

---

### 3. Database Management

All relevant data is managed via an ORM (SQLModel). This Includes, "subjects, "topics", "question", "answer", "user", and " QuizResult" and "QuizSession".

---

## ⚙️ Implementation


### Technology

- Python 3.13.5
- Environment: GitHub Codespaces
- External libraries: nicegui, sqlmodel, sqlalchemy, pytest

### Libraries Used

#Third Party Libraries 
1. sqlmodel
2. nicegui
3. pytest

#Standard Libraries and it's uses
4. os
5. sys
6. json
7. random
8. uuid
9. datetime
10. zoneinfo
11. sqlite3
12. pathlib
13. typing

---

### 📂 Repository Structure

PROJECT_PF_ADV/
├─ .devcontainer
│  ├─ devcontainer.json
│  └─ Dockerfile 
├─ .pytest_cache
├─ .venv
├─ .vscode
├─ .docs
│  ├─ architecture-diagrams
│  │  └─ DIAGRAMS.md
│  └─ ui-images
│     ├─ FIGMA_DESIGN_SPEC.md
│     ├─ ui_admin_add_question.png
│     ├─ ui_admin_confirmation_delete.png
│     ├─ ui_admin_delete_question.png
│     ├─ ui_admin_login.png
│     ├─ ui_admin_panel.png
│     ├─ ui_login.png
│     ├─ ui_question_and_answers_correction.png
│     ├─ ui_question_and_answers.png
│     ├─ ui_scoreboard.png
│     ├─ ui_start_quiz.png
│     └─ ui_user_menu.png
│
├─ Project_PF (Phase 1)             #Previous Semester's Project (Autumn 2025)
│  ├─ devcontainer
│  │   └─ devcontainer.json
│  │   └─ Dockerfile
│  ├─ Data
│  │   └─ DIB.json
│  │   └─ POM.json
│  ├─ Pictures
│  │   └─ application.arcitecture_v1.jpg
│  ├─ .gitignore
│  ├─ main.py
│  ├─ quiz.py
│  ├─ README.md
│  └─ requirements.txt
│
├─ Project_PF (Phase 2)  
│  ├─ data_access             
│  │  ├─ __pycache__
│  │  ├─ __init__.py
│  │  ├─ db.py
│  │  ├─ question_dao.py
│  │  ├─ score_dao.py
│  │  ├─ subject_dao.py
│  │  └─ user_dao.py
│  ├─ DB
│  │  ├─ Legacy Files
│  │  │  ├─ DIB.json
│  │  │  └─ POM.json
│  │  ├─ check_db.py
│  │  ├─ db_converter.py
│  │  └─ quiz.db
│  ├─ domain
│  │  ├─ __pycache__
│  │  ├─ __init__.py
│  │  └─ models.py
│  ├─ services
│  │  ├─ __pycache__
│  │  ├─ __init__.py
│  │  ├─ question_service.py
│  │  ├─ quiz_session_service.py
│  │  ├─ score_service.py
│  │  ├─ subject_session_service.py
│  │  └─ user_service.py
│  ├─ test
│  │  ├─ __pycache__
│  │  ├─ conftest.py
│  │  ├─ pytest.ini
│  │  ├─ test_database.py
│  │  ├─ test_integration.py
│  │  └─ test_unit.py
│  ├─ ui
│  │  ├─ __pycache__
│  │  ├─ __init__.py
│  │  ├─ cli.py
│  │  └─  gui.py
│  ├─ __main__.py                   # entrypoint
│  ├─ class.md
│  └─ DESIGN_DECISIONS.md
├─ README.md
├─ requirements-dev.txt
└─ requirements.txt

---

### How to Run

> 🚧 Adjust to your project.

### 1. Project Setup
- Python 3.13 (or the course version) is required
- Create and activate a virtual environment:
   - **macOS/Linux:**
      ```bash
      python3 -m venv .venv
      source .venv/bin/activate
      ```
   - **Windows:**
      ```bash
      python -m venv .venv
      .venv\Scripts\Activate
      ```
- Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt #specifically for Pytesting
   ```

### 2. Configuration
- E.g., setup of parameters or environment variables

### 3. Launch
- Start the NiceGUI app in __main__.py by running the programm as a Python File. 
   

### 4. Usage (document as steps)

> 🚧 Describe the usage of the main functions

Doing a Quiz:
1. Login with a Username of your choice
2. Select "Start Quiz"
3. Set Parameters including what subject, which topics, difficulty and number of questions (minimum of 5).
4. Start Attempt 
5. Once the Attempt has been completed, either by answering all the questions or quitting the quiz beforehand, the user is shown their results, including their achieved points, percentage and grade. 
6. The user may compare their score to previous attempts or other users in "View Scoreboard". 

> 🚧 Add UI screenshots of the main screens (or a short video link):

[View UI Images & Mockups](docs/ui-images/ui_user_menu.png)
[View UI Images & Mockups](docs/ui-images/ui_start_quiz.png)
[View UI Images & Mockups](docs/ui-images/ui_question_and_answers.png)
[View UI Images & Mockups](docs/ui-images/ui_scoreboard.png)

---

## 🧪 Testing

> 🚧 Explain what you test and how to run tests.

**Test Protocoll**

### TC_001 - Score calculation and grade mapping

| **Field** | **Details** |
|-----------|-----------|
| **Test type** | Unit |
| **Preconditions** | Pytest environment available |
| **Test steps** | Run the score helper with multiple cases |
| **Actions Taken** | Calculate percentage and grade for each case |
| **Test data/input** | 10/10, 8/10, 7/10 |
| **Expected result** | Percentages and grades match the thresholds |
| **Actual result** | Matches all expected values |
| **Status** | ✅ pass |
| **Comments** | Covers several grade bands in one test |

---

### TC_002 - Score calculation rejects zero total

| **Field** | **Details** |
|-----------|-----------|
| **Test type** | Unit |
| **Preconditions** | Pytest environment available |
| **Test steps** | Call score calculation with zero total questions |
| **Actions Taken** | Verify the helper raises an error |
| **Test data/input** | 3 correct, 0 total |
| **Expected result** | ValueError is raised |
| **Actual result** | ValueError raised with the expected message |
| **Status** | ✅ pass |
| **Comments** | Boundary validation for invalid quiz setup |

---

### TC_003 - Difficulty normalization

| **Field** | **Details** |
|-----------|-----------|
| **Test type** | Unit |
| **Preconditions** | Pytest environment available |
| **Test steps** | Pass formatted difficulty values into the helper |
| **Actions Taken** | Normalize and compare the result |
| **Test data/input** | easy, MEDIUM, Hard |
| **Expected result** | Values normalize to easy, medium, hard |
| **Actual result** | Values normalized correctly |
| **Status** | ✅ pass |
| **Comments** | Uses multiple assertions in one test |

---

### TC_004 - Difficulty rejects unknown value

| **Field** | **Details** |
|-----------|-----------|
| **Test type** | Unit |
| **Preconditions** | Pytest environment available |
| **Test steps** | Pass an unsupported difficulty value |
| **Actions Taken** | Verify the helper rejects it |
| **Test data/input** | expert |
| **Expected result** | ValueError is raised |
| **Actual result** | ValueError raised |
| **Status** | ✅ pass |
| **Comments** | Negative validation case |

---

### TC_005 - Username validation rules

| **Field** | **Details** |
|-----------|-----------|
| **Test type** | Unit |
| **Preconditions** | Pytest environment available |
| **Test steps** | Check valid, blank, and too-long usernames |
| **Actions Taken** | Evaluate trim and length rules |
| **Test data/input** | student, blank string, 31 chars |
| **Expected result** | Valid names pass, invalid names fail |
| **Actual result** | Validation behaves as expected |
| **Status** | ✅ pass |
| **Comments** | Covers whitespace and length edge cases |

---

### TC_006 - Answer selection rules

| **Field** | **Details** |
|-----------|-----------|
| **Test type** | Unit |
| **Preconditions** | Pytest environment available |
| **Test steps** | Check several answer choices |
| **Actions Taken** | Compare against the valid answer range |
| **Test data/input** | 1, 2, 4, 0, 5 |
| **Expected result** | Choices 1-4 pass, others fail |
| **Actual result** | Valid range enforced |
| **Status** | ✅ pass |
| **Comments** | Compact range validation test |

---

### TC_007 - Persist question with answers

| **Field** | **Details** |
|-----------|-----------|
| **Test type** | DB |
| **Preconditions** | In-memory SQLite session and seeded subject/topic fixture |
| **Test steps** | Create a question, add four answers, mark the correct one, read it back |
| **Actions Taken** | Persist one question with one correct answer and three distractors |
| **Test data/input** | Question: What is AI?, 4 answers |
| **Expected result** | Question and all answers are stored; correct answer link is correct |
| **Actual result** | All rows persisted and linked correctly |
| **Status** | ✅ pass |
| **Comments** | Checks both persistence and relationship integrity |

---

### TC_008 - Filter by difficulty and topic

| **Field** | **Details** |
|-----------|-----------|
| **Test type** | DB |
| **Preconditions** | In-memory SQLite session and seeded subject/topic fixture |
| **Test steps** | Insert several questions across topics and difficulties, then query a subset |
| **Actions Taken** | Select only medium AI questions and sort them |
| **Test data/input** | Mixed AI and IoT questions |
| **Expected result** | Only the matching AI medium questions are returned in order |
| **Actual result** | Query returns exactly the expected rows |
| **Status** | ✅ pass |
| **Comments** | Exercises a multi-condition query |

---

### TC_009 - Save result and scoreboard order

| **Field** | **Details** |
|-----------|-----------|
| **Test type** | DB |
| **Preconditions** | In-memory SQLite session and seeded subject/topic fixture |
| **Test steps** | Insert multiple quiz results, then query by score descending |
| **Actions Taken** | Persist results for multiple users and calculate the average |
| **Test data/input** | Scores 9, 8, 5 |
| **Expected result** | Results ordered by score; average is correct |
| **Actual result** | Ordering and average match expectations |
| **Status** | ✅ pass |
| **Comments** | Slightly more complex than a simple save test |

---

### TC_010 - Quiz workflow mixed answers

| **Field** | **Details** |
|-----------|-----------|
| **Test type** | Integration |
| **Preconditions** | In-memory DB with subject/topic support |
| **Test steps** | Create questions, answer most of them correctly, save result |
| **Actions Taken** | Simulate a quiz run with one wrong answer |
| **Test data/input** | 5 questions, 4 correct answers |
| **Expected result** | Final score is stored as 4/5 |
| **Actual result** | Score stored as 4/5 |
| **Status** | ✅ pass |
| **Comments** | Uses a helper to seed question/answer data |

---

### TC_011 - Admin update and delete

| **Field** | **Details** |
|-----------|-----------|
| **Test type** | Integration |
| **Preconditions** | In-memory DB with subject/topic support |
| **Test steps** | Create a question, update its difficulty, verify the update, then delete everything |
| **Actions Taken** | Change question difficulty and remove question plus answers |
| **Test data/input** | One question with four answers |
| **Expected result** | Updated question is queryable; delete removes question and answers |
| **Actual result** | Update and delete both succeed |
| **Status** | ✅ pass |
| **Comments** | Combines update, query, and cleanup in one flow |

---

### TC_012 - Scoreboard orders attempts

| **Field** | **Details** |
|-----------|-----------|
| **Test type** | Integration |
| **Preconditions** | In-memory DB with quiz result support |
| **Test steps** | Insert several quiz attempts and order them by score |
| **Actions Taken** | Build a mini scoreboard from multiple attempts |
| **Test data/input** | Attempts: 9, 8, 7 |
| **Expected result** | Results are sorted from highest to lowest |
| **Actual result** | Scoreboard order is correct |
| **Status** | ✅ pass |
| **Comments** | Covers duplicate user attempts and leaderboard ranking |

---

**Run:**
```bash
pytest Project_PF_Phase_2/test/test_unit.py
pytest Project_PF_Phase_2/test/test_database.py
pytest Project_PF_Phase_2/test/test_integration.py
```


---



## 👥 Team & Contributions

---

| Name              | Role     | Contribution                               |
|-------------------|----------|--------------------------------------------|
| Steven            | Junior   | 1) User Stories and Use Cases
| Joggi             | Dev      | 2) ER Diagram Continuation
|                   |          | 3) Initial set-up of NiceGUI
|                   |          | 4) Initial set-up of Pytest
|                   |          | 5) Documentation and overhaul README
|                   |          | 6) Proofreading and added comments for structure
|                   |          | 7)  
|                   |          |  
| Noe               | Dev      | 1) User Stories and Use Cases
| Brönnimann        |          | 2) ER Diagram Continuation
|                   |          | 3) Continuation of NiceGUI
|                   |          | 4) Configuration of Pytest
|                   |          | 5) Definition of Tescases 
|                   |          | 6) NiceGUI Logic Overhaul
|                   |          | 7) Troubelshooting of code 
|                   |          | 
| Christian         | Senior   | 1) User Stories and User Story Flow
| Lehmann           | Dev      | 2) Created the db.converter
|                   |          | 3) Created the quiz_engine.py
|                   |          | 4) Created the quiz_service.py
|                   |          | 5) Restructured the Database into classes
|                   |          | 6) Major Overhaul of Code and Restructure 
|                   |          | 7) Overall Troubleshooting of code


---

## 🚀 Further Improvements

The following features and enhancements are candidates for future development:

### ER Adaptations (Test Class)

**Description:** Extend the Entity-Relationship model to include a dedicated `TestCase` class for tracking and managing automated test metadata.

**Proposed Implementation:**
- Create a `TestCase` entity to store test metadata (ID, name, type, status, execution timestamp)
- Link `TestCase` records to quiz questions for traceability
- Enable tracking of test coverage across the question database
- Support reporting on test execution history and trends

**Benefits:**
- Improved test visibility and traceability
- Better data-driven insights into quiz quality
- Support for historical test analysis

---

### Add and Remove Topics

**Description:** Implement admin functionality to dynamically manage quiz topics without requiring database schema changes.

**Proposed Implementation:**
- Add UI screens in the Admin Panel for topic creation with naming validation
- Implement topic deletion with cascading rules (delete topics and orphaned questions)
- Add confirmation dialogs to prevent accidental removal
- Support bulk operations for managing multiple topics
- Include validation to prevent duplicate topic names within a subject


**Benefits:**
- Course content stays current without developer involvement
- Flexible curriculum adaptation
- Reduced maintenance burden on administrators

---

### Add and Remove Subjects

**Description:** Implement admin functionality to manage quiz subjects (e.g., add new courses or remove outdated ones).

**Proposed Implementation:**
- Create subject management screens in the Admin Panel
- Subject creation with validation (non-empty name, uniqueness check)
- Subject deletion with comprehensive cascade rules (delete all dependent topics, questions, and results)
- Support subject archiving as an alternative to permanent deletion
- Include audit logging for subject changes


**Benefits:**
- Full curriculum management without code changes
- Support for multi-course deployments
- Historical data preservation through archiving
- Scalable to accommodate institutional growth

---

## 🤝 Contributing

---

> 🚧 This is a template repository for student projects.  
> 🚧 Do not change this section in your final submission.

- Use this repository as a starting point by importing it into your own GitHub account
- Work only within your own copy — do not push to the original template
- Commit regularly to track your progress

---

## 📝 License

---

This project is provided for **educational use only** as part of the Advanced Programming module.

[MIT License](LICENSE)
