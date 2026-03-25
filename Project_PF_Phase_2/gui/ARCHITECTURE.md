# Web GUI Architecture Guide (Phase 2 → Phase 3)

## Overview

This guide explains **best practices** for integrating a web GUI with the Phase 2 OODB core, without building the GUI yet. It's a roadmap for when you're ready to add frontend and API layers.

---

## Architecture Principles

### 1. **Separation of Concerns**

The Phase 2 OODB should **never depend on GUI code**.

```
GUI (React/Vue)
    ↓ HTTP REST
API (FastAPI/Flask)
    ↓ imports
Core Models (Phase 2, no UI code)
    ↓ imports
Data (JSON, SQL, etc.)
```

**Why?** 
- Core logic is testable without a web server
- Can swap GUI frameworks without rewriting models
- Can support multiple clients (web, CLI, mobile API)

### 2. **Stateless API Design**

All quiz state lives in the client or a results database, not in the API server.

```python
# Good (stateless)
POST /api/quiz/submit-answer
{
  "question_id": "Q001",
  "user_answer": 2,
  "session_id": "user-session-123"
}
→ Checks answer, returns result, stores in DB

# Bad (stateful)
GET /api/quiz/next-question  # What quiz? Which user?
```

### 3. **Lean API + Fat Client**

Move logic to client where possible (cheaper, faster, less load):

```python
# Move to client
- Form validation (required fields, type checks)
- Local filtering (show only hard questions)
- UI state (selected answer, scrolling position)

# Keep on server
- Authentication & authorization
- Scoring logic (prevent cheating)
- Persistent results storage
- Sensitive computations
```

---

## Recommended Tech Stack

### Frontend (3 options, ordered by recommendation)

#### **Option A: Vue 3 + Vite** (Recommended for teams familiar with JS)
- **Why**: Gentle learning curve, fast dev experience, good docs
- **Setup**: `npm create vite@latest my-quiz -- --template vue`
- **State**: Pinia (Vue's Vuex successor)
- **HTTP**: axios or fetch API

```javascript
// Example Pinia store
import { defineStore } from 'pinia'

export const useQuizStore = defineStore('quiz', {
  state: () => ({
    currentQuestion: null,
    userAnswers: [],
    timeRemaining: 60,
  }),
  actions: {
    async fetchQuestion(topicId) {
      this.currentQuestion = await api.get(`/questions/${topicId}`)
    },
    submitAnswer(answer) {
      this.userAnswers.push(answer)
      api.post('/results/submit', { answer })
    }
  }
})
```

#### **Option B: React 18 + Vite** (Recommended for JSX lovers)
- **Why**: Largest ecosystem, more job market
- **State**: Zustand or TanStack Query
- **Setup**: `npm create vite@latest my-quiz -- --template react`

#### **Option C: Svelte** (Recommended for simplicity)
- **Why**: Smallest bundle size, least boilerplate
- **Trade-off**: Smaller community

### Backend (2 options)

#### **Option A: FastAPI** (Recommended - modern, fast)
```python
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Load OODB once on startup
from models.loader import OODBLoader
loader = OODBLoader()
quiz_db = loader.load_database_from_file("DIB.json")

@app.get("/api/topics")
def get_topics():
    return [{"id": t.id, "name": t.name} for t in quiz_db.get_all_topics()]

@app.get("/api/questions")
def get_questions(topic_id: str, difficulty: str = None):
    questions = quiz_db.questions_by_topic(topic_id)
    if difficulty:
        questions = [q for q in questions if q.difficulty_id == f"D_{difficulty[0].upper()}"]
    return [
        {
            "id": q.id,
            "text": q.text,
            "choices": [{"id": c.id, "label": c.label, "text": c.text} for c in q.choices],
            "difficulty": difficulty
        }
        for q in questions
    ]

@app.post("/api/answers/check")
def check_answer(question_id: str, choice_id: str):
    question = quiz_db.get_question(question_id)
    is_correct = question.correct_choice_id == choice_id
    return {
        "is_correct": is_correct,
        "correct_answer": question.get_correct_answer_number(),
        "explanation": question.explanation
    }

# Serve static files (React/Vue build)
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
```

#### **Option B: Flask** (If you prefer lightweight)
```python
from flask import Flask, jsonify
from models.loader import OODBLoader

app = Flask(__name__)
loader = OODBLoader()
quiz_db = loader.load_database_from_file("DIB.json")

@app.route('/api/topics', methods=['GET'])
def get_topics():
    return jsonify([{"id": t.id, "name": t.name} for t in quiz_db.get_all_topics()])

# ... similar routes
```

---

## API Route Design

### Core Quiz Routes

```
GET  /api/topics                      → List[Topic]
GET  /api/topics/{id}                 → Topic with questions
GET  /api/questions                   → List[Question] (all)
GET  /api/questions?topic_id=T_DIB    → Questions filtered by topic
GET  /api/questions?difficulty=easy   → Questions filtered by difficulty
GET  /api/questions/{id}              → Single Question with choices
POST /api/answers/check               → { question_id, choice_id } → { correct, explanation }

POST /api/sessions                    → Create quiz session (returns session_id)
POST /api/sessions/{id}/submit        → Submit answer, score response
GET  /api/sessions/{id}/results       → Quiz results
```

### Admin Routes (Future)

```
POST /api/admin/questions             → Create question
PUT  /api/admin/questions/{id}        → Update question
DELETE /api/admin/questions/{id}      → Delete question
GET  /api/admin/analytics             → Quiz statistics
GET  /api/admin/users                 → User activity
```

---

## Frontend Component Structure

```
src/
├── components/
│   ├── QuizContainer.vue          # Main quiz flow
│   ├── QuestionDisplay.vue        # Single question + choices
│   ├── ResultsScreen.vue          # Final score and review
│   ├── TopicSelector.vue          # Topic/difficulty picker
│   └── Timer.vue                  # Question timer
├── pages/
│   ├── Home.vue
│   ├── Quiz.vue
│   └── Results.vue
├── stores/
│   └── quizStore.js               # Pinia store (state + actions)
├── api/
│   └── client.js                  # HTTP client (axios/fetch)
└── App.vue
```

### Example Component (Vue 3 + TypeScript)

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useQuizStore } from '@/stores/quizStore'
import QuestionDisplay from '@/components/QuestionDisplay.vue'

const store = useQuizStore()
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  await store.fetchQuestion()
  loading.value = false
})

const submitAnswer = async (choice_id: string) => {
  const result = await store.checkAnswer(choice_id)
  if (result.is_correct) {
    store.score += 1
    setTimeout(() => store.fetchQuestion(), 1500)
  }
}
</script>

<template>
  <div class="quiz-container">
    <QuestionDisplay 
      v-if="store.currentQuestion && !loading"
      :question="store.currentQuestion"
      @answer="submitAnswer"
    />
    <div v-if="loading" class="loading">Loading...</div>
  </div>
</template>

<style scoped>
.quiz-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
```

---

## Deployment Strategy

### Development
```bash
# Terminal 1: Backend
cd Project_PF_Phase_2
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

### Production
```bash
# Build frontend
cd frontend && npm run build

# Copy dist to backend static folder
cp -r dist/* ../backend/static/

# Run backend (serves frontend automatically)
uvicorn main:app --host 0.0.0.0 --port 8000
```

Or use Docker:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

---

## Caching Strategy (Future)

```python
# Cache frequently accessed data
from functools import lru_cache

@lru_cache(maxsize=1)
def get_all_topics():
    return quiz_db.get_all_topics()

# OR use Redis for distributed cache
import redis

cache = redis.Redis(host='localhost', port=6379)

@app.get('/api/topics')
def get_topics():
    cached = cache.get('topics')
    if cached:
        return json.loads(cached)
    topics = [t for t in quiz_db.get_all_topics()]
    cache.setex('topics', 3600, json.dumps(topics))  # 1 hour
    return topics
```

---

## Testing Strategy

### Backend (Unit Tests)
```python
# tests/test_oodb.py
from models.loader import OODBLoader
from models.database import QuizDatabase

def test_load_questions():
    loader = OODBLoader()
    db = loader.load_database_from_file("DIB.json")
    assert len(db.get_all_questions()) > 0

def test_correct_answer():
    loader = OODBLoader()
    db = loader.load_database_from_file("DIB.json")
    q = db.get_question("Q001")
    assert q.get_correct_answer_number() is not None
```

### Frontend (Component Tests with Vitest)
```javascript
// tests/QuestionDisplay.spec.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import QuestionDisplay from '@/components/QuestionDisplay.vue'

describe('QuestionDisplay', () => {
  it('renders choices', () => {
    const question = {
      id: 'Q001',
      text: 'Test?',
      choices: [
        { id: 'Q001_C1', label: '1', text: 'Option 1' },
        // ...
      ]
    }
    const wrapper = mount(QuestionDisplay, { props: { question } })
    expect(wrapper.text()).toContain('Option 1')
  })
})
```

---

## Security Considerations

1. **Prevent Cheating**: Never send correct answer to client before submission
   ```python
   # Bad
   return { "question": "...", "correct_answer": 2, "choices": [...] }
   
   # Good
   return { "question": "...", "choices": [...] }  # No correct_answer
   POST /check-answer { question_id, choice_id } → { is_correct }
   ```

2. **Rate Limiting**: Prevent rapid-fire answer submissions
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   
   @app.post('/api/answers/check')
   @limiter.limit("10/minute")
   def check_answer(...):
       pass
   ```

3. **CORS**: Allow only your frontend domain
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourquizapp.com"],
       allow_methods=["GET", "POST"],
   )
   ```

---

## Performance Tips

1. **Lazy load questions**: Don't send all choicesall at once
2. **Compress responses**: gzip by default in FastAPI
3. **Debounce client requests**: Wait 500ms before sending answer check
4. **Index database**: If using SQL, index `topic_id`, `difficulty_id`
5. **Pagination**: Don't load 1000 questions at once

---

## Migration Timeline

**Month 1**: Core API (GET endpoints) + simple React form  
**Month 2**: Scoring logic, session management, results  
**Month 3**: Admin panel for managing questions  
**Month 4**: Caching, performance optimization, analytics  

---

## Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **Vue 3**: https://vuejs.org/
- **Pinia**: https://pinia.vuejs.org/
- **REST best practices**: https://restfulapi.net/
- **API security**: https://owasp.org/www-project-api-security/

---

**You now have a clear roadmap to extend Phase 2 with a beautiful, scalable GUI!**
