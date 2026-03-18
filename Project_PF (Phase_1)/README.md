# FHNW Big Study Quiz

This project is intended to:

- Train students on the subjects of the assesments modules through quizzes
- Apply basic **Python** programming concepts learned in the Programming Foundations module
- Practice the complete process from **problem analysis to implementation**
- Demonstrate the use of **console interaction, data validation, and file processing**
- Produce clean, well-structured, and documented code
- Prepare students for **teamwork and documentation** in later modules  
- Developing project planning skills

# 🍕 TEMPLATE for documentation

## 📝 Analysis

**Problem**
> We learn a lot of material in this semester that is crucial to our further education. This can be overwhelming or even frightening. The material is spread over various Moodles / Inside FHNW, which is chaotic.

**Scenario**
> To enhance the learning process we aim to crate a catalouge of questions which will be presented as a quiz to prepare for our assesment exams. The quiz will be asking questions from one subject and split into chapters. The type of questions will be mulitple choice. The Answers will be validated and give an indication of right or wrong and will also show an explanation. At the end of the quiz, the user will be given a score.


**User stories:**
1. As a user, I want to answer different questions, in order to support my studies for the test.
2. As a user, I want a point counter/final grade/percentage presented, in order to check my performance.
3. As an Admin, I want to add and remove questions, in order to keep the quiz relevant.

**Use cases:**
- Answer Questions (from POM.json and DIB.json)
- Show Grade / Points / Percentage (to results.csv)
- Return to Menu at any point in time
- 


---

## ✅ Project Requirements

Each app must meet the following three criteria in order to be accepted (see also the official project guidelines PDF on Moodle):

1. Interactive app (console input)
2. Data validation (input checking)
3. File processing (read/write)

---

### 1. Interactive App (Console Input)

The application interacts with the user via the console. Users can:
- Answer Questions
- Choose chapters (E.g.: Subject)
- Receive a point total
- Return to the menu
- Stop the quiz


### 2. Data Validation

- The data validation is performed in quiz.py on line 123. 
- Comparing the user input of [1,2,3,4] with the listed "correct_answer" in either DIB.json or POM.json
- Additionally, the validation function will issue an explanation to the user as to why their input was incorrect. The "correct_text" and "explanation" handles this. 
- Set Failsafes incase elements are missing in the databanks 
- 

### 3. File Processing
| Input file  | Our databanks (DIB.json and POM.json) are 
|             | read on startup of the programm
|-------------------------------------------------------------------------|
| Output file | The results.csv is the output
|-------------------------------------------------------------------------|
| Explanation | The individual questions are read from the input file
|             | compared with the user's input (choice of answers) and 
|             | then validated and a result is created as an output. 

## ⚙️ Implementation
- application architecture path: 
chdl91/Project_PF/Pictures/application.arcitecture_v1.jpg

### Technology
- Python 3.11.14
- Environment: GitHub Codespaces
- No external libraries

### 📂 Repository Structure
PROJECT_PF
    - .devcontainer
        - devcontainer.json
        - Dockerfile
    - Data
        - DIB.json
        - POM.json
    - Pictures
        - application.arcitecture_v1.jpg
    - .gitignore
    - main.py
    - quiz.py
    - README.md
    - requirements.txt
    - (results.csv)

### How to Run
1) Open Repository in Github Codespacces
2) Open the Terminal
3) Run: python3 main.py



## 👥 Team & Contributions

| Name              | Role     | Contribution                               |
|-------------------|----------|--------------------------------------------|
| Steven Joggi  	| Support  | 1) Added further imports and file_path to the databanks
|                   |          | 2) Proofreading and added comments for structure
|                   |          | 3) Added counter.py and begun work on the validation
|                   |          | 4) Added Timer including "signal"
|                   |          | 5) Added call in main.py for quiz.py
|                   |          | 6) Added the requirements.txt
|                   |          | 7) Continuation of README.md 
|                   |          |  
| Noe Brönnimann 	| VP 	   | 1) Added databank json loader and file.close()
|                   |          | 2) Correction of Steven's code (counter.py & validation)
|                   |          | 3) Added the Application Architecture_v1 in Pictures
|                   |          | 4) Created start menu with input choices
|                   |          | 5) Created .gitignore with help of Phillip Gachnang
|                   |          | 6) Added results.csv 
|                   |          | 7) Added Timestamp and fix for UTC+0 time
|                   |          | 
| Christian Lehmann | Master   | 1) Creation of DIB.json and POM.json (Databank)
|                   |          | 2) Creation of quiz.py 
|                   |          | 3) Expanded the size of questions in the databank
|                   |          | 4) Overall Troubleshooting of Noe's and Steven's code
|                   |          | 5) Added validation method and correct scoring
|                   |          | 6) First Version of README.md 
|                   |          | 7) Improvement of results.csv


## 🤝 Contributing

> 🚧 This is a template repository for student projects.  
> 🚧 Do not change this section in your final submission.

- Use this repository as a starting point by importing it into your own GitHub account.  
- Work only within your own copy — do not push to the original template.  
- Commit regularly to track your progress.

## 📝 License

This project is provided for **educational use only** as part of the Programming Foundations module.  
[MIT License](LICENSE)
