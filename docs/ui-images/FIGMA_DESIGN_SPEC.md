# Quiz Application UI/UX Design Guide for Figma

## Project Overview
**Application Name:** Quiz Platform  
**Framework:** nicegui (Python-based UI)  
**Purpose:** Educational quiz application with user and admin modes  
**Color Scheme:** Modern, accessible design with blue and orange accents

---

## Design System

### Color Palette
- **Primary Blue:** #007ACC (main actions, headers)
- **Light Blue:** #E1F5FF (backgrounds, highlights)
- **Orange:** #FF9800 (secondary actions, alerts)
- **Light Orange:** #FFF3E0 (admin section background)
- **Dark Gray:** #333333 (text)
- **Light Gray:** #F5F5F5 (backgrounds)
- **White:** #FFFFFF (cards, modals)
- **Success Green:** #4CAF50 (correct answers)
- **Error Red:** #F44336 (incorrect answers)

### Typography
- **Font Family:** Segoe UI / Roboto (system fonts)
- **Heading (H1):** 32px, bold, #333
- **Heading (H2):** 24px, bold, #333
- **Body:** 14px, regular, #555
- **Small Text:** 12px, regular, #888

### Spacing & Layout
- **Base Unit:** 8px
- **Padding Standard:** 16px
- **Border Radius:** 4px
- **Container Max Width:** 1200px
- **Mobile Breakpoint:** 768px

---

## Core Screens

### 1. Login/Register Screen
**Purpose:** User authentication and account creation  
**Layout:** Centered single-column

**Components:**
- Application logo/title at top
- Welcome message
- Username input field (text input, placeholder: "Enter username")
- "Login / Create Account" button (primary blue, full width)
- Information message showing if returning user or new user
- Display of admin/user access level (red text for admin, blue for user)

**Dimensions:** 400px wide form on desktop, full screen mobile

---

### 2. Main Menu Screen (User Mode)
**Purpose:** Select quiz parameters  
**Layout:** Card-based grid

**Components:**
- Header: "Welcome, [Username]!" with user profile indicator
- "Select a Subject" section with buttons for each subject
- "Select Difficulty" section with radio buttons (Easy / Medium / Hard / All)
- "Number of Questions" input field (numeric, default: 10)
- "Start Quiz" button (large, prominent, primary blue)
- "View My Scores" button (secondary)
- "View Top Scores" button (secondary)
- Logout button (top right, small)

**Flow Diagram:**
```
Login → Main Menu → Subject Selection → Difficulty → Start Quiz
```

---

### 3. Quiz Screen
**Purpose:** Display questions and collect answers  
**Layout:** Full screen, centered content

**Components:**

**Header Bar:**
- Question counter: "Question 2 of 10"
- Progress bar (visual indicator)
- Current score display: "Score: 1/1"
- Time elapsed (optional)

**Question Card:**
- Large question text area
- Visual distinction for question
- Difficulty badge (Easy/Medium/Hard) in orange

**Answer Options:**
- 4 clickable answer buttons (or variable number)
- Each button shows answer text
- On hover: button background changes
- On click: 
  - Correct answer: Green background, checkmark icon
  - Incorrect answer: Red background, X icon
- Disabled after selection until "Next" clicked

**Action Buttons:**
- "Next Question" button (enabled after answer selection)
- Optional: "Exit Quiz" button (confirmation modal)

**Responsive:**
- Stack vertically on mobile
- Answer buttons take full width on mobile

**Color States:**
- Default: Light gray background
- Hover: Slightly darker
- Selected correct: Green (#4CAF50)
- Selected incorrect: Red (#F44336)
- Disabled: Light gray, 50% opacity

---

### 4. Quiz Results Screen
**Purpose:** Show quiz completion summary  
**Layout:** Card-based, centered

**Components:**
- Large result heading: "Quiz Complete!"
- Final score display (prominent, large font): "8 out of 10"
- Percentage display: "80%"
- Grade badge (if applicable): "Very Good"
- Result breakdown:
  - Correct answers: 8
  - Incorrect answers: 2
  - Time taken: [duration]
- Difficulty level taken
- Subject name

**Action Buttons:**
- "Retake Quiz" (primary)
- "Try Another Subject" (secondary)
- "View All Scores" (tertiary)
- "Main Menu" or "Logout"

---

### 5. Scores Leaderboard Screen
**Purpose:** Display user scores and top performers  
**Layout:** Table-based

**Components:**
- Header: "Your Recent Scores" or "Top Scores"
- Table columns:
  - Rank (for top scores)
  - Username
  - Subject
  - Score
  - Date/Time
  - View Details link

**Filters:**
- Subject dropdown
- Time period (Last week / Last month / All time)
- Sort by (Score / Date)

**Styling:**
- Header row: Dark blue background, white text
- Alternating row colors (white, light gray)
- Hover state: Light blue background
- Current user row: Highlighted with orange border

---

### 6. Admin Dashboard Screen
**Purpose:** Manage quiz content  
**Layout:** Multi-section dashboard

**Styling:**
- Background: Light orange (#FFF3E0)
- Admin indicator badge: Top right

**Components:**

**Navigation Tabs:**
- Subjects
- Topics
- Questions
- Users/Results

**Tab 1 - Subjects:**
- List of all subjects in table format
- Columns: Subject Name, Topics Count, Questions Count, Actions
- Action buttons: Edit, Delete (with confirmation)
- "Add New Subject" button (primary)

**Tab 2 - Topics:**
- Filter by Subject dropdown
- Table: Topic Name, Subject, Questions Count, Actions
- "Add New Topic" button

**Tab 3 - Questions:**
- Filter by Subject and Topic dropdowns
- Table: Question ID, Question Text (truncated), Difficulty, Topics, Actions
- "Add New Question" button (modal form)

**Tab 4 - Users/Results:**
- Table: Username, Total Quizzes, Average Score, Last Quiz Date
- Optional: Detailed analytics chart

**Modal Forms:**
- Input fields match database schema
- Form validation visual feedback
- Submit/Cancel buttons

---

### 7. Add/Edit Question Modal
**Purpose:** Create or modify quiz questions  
**Layout:** Centered modal, 600px width

**Components:**
- Modal title: "Add New Question"
- Subject dropdown (required)
- Topic dropdown (required, filtered by subject)
- Question text area (required, max 255 chars)
- Difficulty dropdown (easy/medium/hard)
- Answer options section:
  - 4 input fields for answers
  - Radio button to select correct answer
  - "Add another answer" button
- Form buttons: Save, Cancel
- Validation messages (red text below fields)

---

## Navigation Structure

### User Mode Flow
```
Login/Register 
  ↓
Main Menu
  ├→ Select Subject → Select Difficulty → Start Quiz
  │    ↓
  │    Quiz Screen (loop through questions)
  │    ↓
  │    Results Screen
  │    ├→ Retake Quiz (restart)
  │    ├→ Try Another Subject (back to Main Menu)
  │    └→ View Scores (Leaderboard)
  │
  ├→ View My Scores (Leaderboard)
  └→ View Top Scores (Leaderboard)
```

### Admin Mode Flow
```
Login/Register (as admin)
  ↓
Admin Dashboard
  ├→ Manage Subjects (CRUD operations)
  ├→ Manage Topics (CRUD operations)
  ├→ Manage Questions (CRUD operations)
  └→ View Users & Results (analytics)
```

---

## Component Specifications

### Input Fields
- **Text Input:** Border-bottom only (material design style)
- **Placeholder:** Gray, italic
- **Focus:** Blue underline, blue label
- **Error:** Red underline, red error message below
- **Disabled:** Gray background, 50% opacity

### Buttons
- **Primary Button:** Blue background, white text, full width on mobile
- **Secondary Button:** White background, blue border, blue text
- **Tertiary Button:** Gray text, no border
- **Hover State:** Slightly darker shade
- **Active/Pressed:** Darker shade with slight shadow
- **Disabled:** Gray, 50% opacity, no hover effect

### Cards
- **Background:** White
- **Border:** None (uses shadow)
- **Shadow:** Subtle (0 2px 4px rgba(0,0,0,0.1))
- **Padding:** 16px
- **Border Radius:** 4px
- **Hover:** Subtle shadow increase

### Progress Indicators
- **Progress Bar:** Full width, segmented or continuous
- **Color:** Blue gradient
- **Height:** 4px
- **Background:** Light gray

### Badges
- **Difficulty Easy:** Light green background, green text
- **Difficulty Medium:** Light orange background, orange text
- **Difficulty Hard:** Light red background, red text
- **Admin:** Light blue background, blue text, top-right corner

---

## Responsive Design

### Desktop (1200px+)
- Full sidebar navigation (optional)
- 2-3 column layouts
- Large buttons and inputs
- Answer options in grid

### Tablet (768px - 1199px)
- Simplified navigation
- Single column for forms
- Stacked layouts
- Full-width buttons

### Mobile (<768px)
- Hamburger menu (if applicable)
- Full-screen single column
- Large touch targets (48px minimum)
- Stacked components
- Minimal padding/spacing
- Fullscreen modals

---

## Accessibility Considerations

- Minimum contrast ratio 4.5:1 for text
- Focus indicators visible (outline or underline)
- All interactive elements keyboard accessible
- Form labels associated with inputs
- Error messages linked to fields
- Color not used as only indicator (use icons/text too)
- Touch targets minimum 48px × 48px on mobile

---

## Interaction Patterns

### Answer Selection
1. User clicks answer button
2. Button disabled, visual feedback (green or red)
3. Explanation appears (optional)
4. "Next Question" button enables
5. Progress bar updates

### Form Submission
1. User fills form
2. Validation on blur/change
3. Submit button disabled until valid
4. Loading spinner during submit
5. Success/error message

### Modal Workflows
1. User triggers modal
2. Modal centered, content scrollable if needed
3. Backdrop slightly darkened
4. Keyboard: Escape to close, Tab to navigate
5. Focus trapped in modal

---

## Implementation Notes for nicegui

### Colors Implementation
```python
# Use these hex values directly in nicegui
primary_blue = '#007ACC'
light_blue = '#E1F5FF'
success_green = '#4CAF50'
error_red = '#F44336'
```

### Component Mapping
- **Text Inputs** → `ui.input()`
- **Buttons** → `ui.button()`
- **Cards** → `ui.card()`
- **Tables** → `ui.table()`
- **Select/Dropdown** → `ui.select()`
- **Radio** → `ui.radio()`
- **Progress** → `ui.linear_progress()`
- **Modals** → `ui.dialog()`

### Layout Strategy
- Use `ui.row()` / `ui.column()` for layouts
- CSS classes for responsive styling
- Tailwind CSS compatible
- Dark mode support (optional)

---

## Design File Structure (Figma)

### Pages
1. **Design System** - Colors, typography, component styles
2. **Login** - All login/register variations
3. **User Mode** - Main menu, quiz, results, leaderboard
4. **Admin Mode** - Dashboard, modals, forms
5. **Components** - Reusable buttons, inputs, cards
6. **Prototypes** - Interaction flows, user journeys

### Components (Reusable)
- Primary Button (variants: default, hover, active, disabled)
- Secondary Button (same variants)
- Text Input (variants: default, focus, error, disabled)
- Card (variants: default, with shadow)
- Badge (variants: difficulty levels, admin)
- Answer Option (variants: default, hover, correct, incorrect)

---

## Next Steps

1. **Import to Figma** - Create a new Figma file from this spec
2. **Create Components** - Build reusable component library
3. **Design Screens** - Design each screen based on specifications
4. **Prototype Links** - Connect screens with interactions
5. **Export** - Export as assets/icons for nicegui
6. **Development** - Translate Figma designs to nicegui code
