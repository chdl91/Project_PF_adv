Topics(id, name)
"Topic_id": "T001"=PK, "topic": "Management Basics"
Questions(id, topic_id, question_text, correct_answer, explanation, difficulty)
"Question_id": "Q001" =PK,"Topic_id": "T001"=SK,"question_text": "What best describes 'Management' in management context?","correct_answer": answer_id, "explanation": "'Management' means: The pursuit of organizational goals efficiently and effectively by integrating people, resources, and processes..","difficulty": "easy"
Answers(id, question_id, answer_text)
answer_id: "A00001"=PK, question_id: "Q001", "answer_text"
Users (id, user_name, score, timestamp)
user_id, user_name, user_score, user_timestamp

"topic": "Management Basics",
    "question": "What best describes 'Management' in management context?",
    "answers": {
      "1": "Planning, organizing, leading, and controlling.",
      "2": "Interpersonal, informational, and decisional roles performed by managers.",
      "3": "Regards the organization as a system of interrelated parts.",
      "4": "The pursuit of organizational goals efficiently and effectively by integrating people, resources, and processes."
    },
    "correct_answer": 4,
    "explanation": "'Management' means: The pursuit of organizational goals efficiently and effectively by integrating people, resources, and processes..",
    "difficulty": "easy",
    "id": "Q001"