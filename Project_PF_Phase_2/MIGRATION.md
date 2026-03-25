# Migration Guide: Phase 1 → Phase 2

## Overview

This guide helps you convert Phase 1 quiz data (flat JSON arrays) to Phase 2 OODB format (normalized with explicit relationships).

---

## Before vs After

### Phase 1 Format (Flat Array)

```json
[
  {
    "topic": "Digitalization",
    "question": "What best describes 'Digitalization'?",
    "answers": {
      "1": "Converting analog...",
      "2": "The broad socio-economic...",
      "3": "A pricing model...",
      "4": "A pricing model... (repeated)"
    },
    "correct_answer": 2,
    "explanation": "'Digitalization' is defined as: ...",
    "difficulty": "easy",
    "id": "Q001"
  },
  ...  // More questions, ~ 200+ entries
]
```

**Problems:**
- Topic names repeat 20-50 times
- Difficulty values repeat hundreds of times
- Answers are embedded in each question
- Hard to filter or query efficiently
- Relationships are implicit

---

### Phase 2 Format (OODB Normalized)

```json
{
  "schema_version": "2.0",
  "objects": {
    "difficulties": [
      {"id": "D_E", "name": "easy", "weight": 1.0},
      {"id": "D_M", "name": "medium", "weight": 2.0},
      {"id": "D_H", "name": "hard", "weight": 3.0}
    ],
    "topics": [
      {
        "id": "T_Digitalization",
        "name": "Digitalization",
        "description": "..."
      },
      ...
    ],
    "questions": [
      {
        "id": "Q001",
        "topic_id": "T_Digitalization",
        "text": "What best describes 'Digitalization'?",
        "difficulty_id": "D_E",
        "correct_choice_id": "Q001_C2",
        "explanation": "..."
      },
      ...
    ],
    "choices": [
      {
        "id": "Q001_C1",
        "question_id": "Q001",
        "label": "1",
        "text": "Converting analog..."
      },
      {
        "id": "Q001_C2",
        "question_id": "Q001",
        "label": "2",
        "text": "The broad socio-economic..."
      },
      ...
    ]
  }
}
```

**Benefits:**
- No duplication (topic stored once, referenced many times)
- Explicit relationships (foreign keys)
- Smaller file size (when gzipped)
- Easier to query, filter, validate
- Natural OOP mapping

---

## Automatic Migration

### Using Python Script (Recommended)

```python
import json
from pathlib import Path
from adapters import LegacyQuizAdapter
from models.loader import OODBLoader

# Load Phase 1 JSON
phase1_file = Path("../Project_PF (Phase_1)/Data/DIB.json")
with open(phase1_file) as f:
    legacy_data = json.load(f)

# Convert to OODB
db = LegacyQuizAdapter.from_phase1_format(legacy_data)

# Save as Phase 2 format
loader = OODBLoader()
loader.save_database_to_file(db, "DIB_migrated.json")

print("✅ Migration complete!")
```

---

## Manual Verification Checklist

After migration, verify:

- [ ] All topics present
  ```python
  original_topics = set(q["topic"] for q in phase1_data)
  migrated_topics = set(t.name for t in db.get_all_topics())
  assert original_topics == migrated_topics
  ```

- [ ] All questions present
  ```python
  assert len(db.get_all_questions()) == len(phase1_data)
  ```

- [ ] No duplicate choices
  ```python
  choices_per_q = [len(q.choices) for q in db.get_all_questions()]
  assert all(c == 4 for c in choices_per_q)  # Each question has 4 choices
  ```

- [ ] Correct answers match
  ```python
  for q in db.get_all_questions():
      assert q.get_correct_choice() is not None
      assert q.get_correct_answer_number() in ["1", "2", "3", "4"]
  ```

- [ ] Difficulty values valid
  ```python
  valid_difficulties = {"easy", "medium", "hard"}
  for d in db.difficulties.values():
      assert d.name in valid_difficulties
  ```

---

## Common Issues & Solutions

### Issue 1: Object IDs Not Unique

**Problem**: Topic IDs clash (e.g., multiple "T_Digitalization")

**Solution**: Use unique ID generator
```python
import uuid

topic_ids = {}
for topic_name in unique_topics:
    topic_ids[topic_name] = f"T_{uuid.uuid4().hex[:8]}"
```

### Issue 2: Answers Not Mapping Correctly

**Problem**: Phase 1 has 3 answers in some questions, 5 in others

**Solution**: Validate and normalize before migration
```python
min_answers = min(len(q.get("answers", {})) for q in phase1_data)
max_answers = max(len(q.get("answers", {})) for q in phase1_data)
print(f"Answer count range: {min_answers} to {max_answers}")

# If not all 4, pad or warn
for q in phase1_data:
    while len(q["answers"]) < 4:
        q["answers"][str(len(q["answers"]) + 1)] = "No answer"
```

### Issue 3: Difficulty Spelling Inconsistencies

**Problem**: Phase 1 has "Easy", "EASY", "easy" all mixed

**Solution**: Normalize before migration
```python
for q in phase1_data:
    q["difficulty"] = q["difficulty"].lower().strip()
```

### Issue 4: Missing Explanations or Topics

**Problem**: Some questions lack explanation or topic

**Solution**: Fill with defaults
```python
for q in phase1_data:
    if not q.get("explanation"):
        q["explanation"] = "See course materials for more information."
    if not q.get("topic"):
        q["topic"] = "Uncategorized"
```

---

## File Structure After Migration

```
Project_PF_Phase_2/
├── data/
│   ├── DIB.json              ← New OODB format (migrated from Phase 1)
│   ├── POM.json              ← New OODB format (migrated from Phase 1)
│   └── DIB_backup_phase1.json ← (optional) Keep original for safety
├── models/
├── adapters/
└── ...
```

---

## Testing the Migration

### Verify Phase 1 Compatibility

After migration, Phase 1 quizzes should work unchanged via adapter:

```python
from models.loader import OODBLoader
from adapters import LegacyQuizAdapter

# Load new OODB
loader = OODBLoader()
db = loader.load_database_from_file("DIB.json")

# Convert back to Phase 1 format
phase1_converted = LegacyQuizAdapter.to_phase1_format(db)

# Run original Phase 1 quiz.py with converted data
from quiz import run_quiz
result = run_quiz(phase1_converted)
print(f"Quiz completed: {result[0]}/{result[1]} correct")
```

---

## Data Quality Improvements to Make During Migration

Consider adding during migration:

### 1. **Timestamps**
```python
question.created_at = "2026-03-25"
question.updated_at = "2026-03-25"
```

### 2. **Tags for Better Filtering**
```python
# Add tags based on content analysis
if "capital" in question.text.lower():
    question.tags.append("geography")
```

### 3. **Difficulty Revision**
```python
# Review and potentially adjust difficulty
# based on answer patterns
if question.text.startswith("In the context of"):
    question.difficulty_id = "D_M"  # Upgrade slightly
```

### 4. **Metadata**
```python
topic.metadata = {
    "course": "BUSN 101",
    "chapter": 3,
    "section": "Advanced Topics"
}
```

---

## Rollback Plan

If something goes wrong:

```bash
# Backup original
cp data/DIB.json data/DIB_phase2.json

# Restore Phase 1 version
cp <path-to-phase1>/DIB.json data/DIB_phase1_backup.json

# Re-migrate (or use legacy adapter for queries)
from adapters import LegacyQuizAdapter
db = LegacyQuizAdapter.from_phase1_format(legacy_data)
```

---

## Timeline

- **Phase 1**: Keep original flat JSON for reference
- **Phase 2**: New OODB format, backward-compatible via adapter
- **Phase 3**: Deprecate Phase 1 data types entirely

---

## Questions?

Refer to:
- `../Project_PF (Phase_1)/Data/DIB.json` - Original format
- `models/loader.py` - Migration logic
- `adapters/legacy.py` - Backward compatibility code
- `example.py` - Running migrated data
