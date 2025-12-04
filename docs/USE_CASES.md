# 📋 Use Cases & User Stories

## Table of Contents
1. [User Personas](#user-personas)
2. [Use Cases](#use-cases)
3. [User Stories](#user-stories)
4. [Scenarios](#scenarios)

---

## User Personas

### 1. Sarah - CELPIP Test Taker
**Background:**
- 28 years old, software engineer
- Planning to immigrate to Canada
- Needs CLB 7 or higher
- Limited time (evenings and weekends)

**Goals:**
- Practice under realistic test conditions
- Track progress over time
- Identify weak areas
- Improve score before official exam

**Tech Comfort:** High
**Devices:** Laptop, smartphone

---

### 2. Michael - English Language Student
**Background:**
- 22 years old, university student
- Preparing for study permit application
- First time taking CELPIP
- Needs to understand test format

**Goals:**
- Learn test structure
- Practice at own pace
- Review answers to understand mistakes
- Build confidence

**Tech Comfort:** Medium
**Devices:** Tablet, laptop

---

### 3. Priya - Working Professional
**Background:**
- 35 years old, accountant
- Retaking CELPIP to improve score
- Limited study time (30 min/day)
- Previous score: CLB 6, needs CLB 8

**Goals:**
- Focus on specific skills (Reading, Writing)
- Quick practice sessions
- Compare current vs previous attempts
- Efficient use of limited time

**Tech Comfort:** Medium
**Devices:** Laptop at home

---

## Use Cases

### UC-1: Take Full Practice Test (Test Mode)

**Actor:** Sarah (Test Taker)

**Precondition:** 
- User has internet connection
- Browser supports modern features

**Main Flow:**
1. User navigates to home page
2. System prompts for email if not set
3. User enters email address
4. User clicks "Test Mode" button
5. System generates unique attempt ID
6. System starts test with Reading Part 1
7. Timer begins countdown
8. User reads passage and answers questions
9. User submits answers
10. System saves responses to JSON
11. System auto-navigates to next part
12. (Repeat steps 7-11 for all parts)
13. After final part, system shows skill score
14. User continues to next skill
15. (Repeat steps 7-14 for all skills)
16. System shows completion message
17. System marks attempt as complete
18. User returns to home page

**Postcondition:**
- Attempt recorded in JSON
- Score displayed on home page
- Button changes to "Retake Test"

**Alternative Flows:**
- 3a. User cancels email prompt → Test not started
- 6a. User clicks "Quit Test" → Returns to home, attempt incomplete
- 8a. Timer runs out → System auto-submits answers

---

### UC-2: Practice Individual Parts (Practice Mode)

**Actor:** Michael (Student)

**Precondition:** 
- User on home page

**Main Flow:**
1. User clicks "Practice Mode" button
2. System displays skill selection page
3. User selects "Reading" skill
4. System shows all reading parts (1-4)
5. User clicks "Part 2"
6. Timer starts for Part 2
7. User answers questions at own pace
8. User submits answers
9. System shows detailed results:
   - Score per question
   - User's answer vs correct answer
   - Running total
10. User can choose:
    - Next Part
    - Different Part
    - Back to skill selection

**Postcondition:**
- Session score updated
- User can freely navigate

**Alternative Flows:**
- 8a. Timer expires → Auto-submit with warning
- 10a. User goes back to test detail → Session saved

---

### UC-3: Review Test History

**Actor:** Priya (Working Professional)

**Precondition:**
- User has taken at least one test

**Main Flow:**
1. User navigates to home page
2. System loads test history from JSON
3. System displays for each test:
   - Number of attempts
   - Latest score
   - Percentage
4. User can:
   - View historical data
   - Compare attempts
   - Decide which test to retake

**Postcondition:**
- User informed of progress

**Alternative Flows:**
- 2a. No history found → Show "0 attempts"

---

### UC-4: Manage Email Address

**Actor:** Any User

**Precondition:**
- User on home page

**Main Flow:**
1. User clicks "Set Email Address" or "Change Email"
2. System displays modal popup
3. User enters/updates email
4. User clicks "Save Email"
5. System validates email format
6. System saves to session
7. System reloads page
8. System displays updated email in banner

**Postcondition:**
- Email stored in session
- Future tests tracked under this email

**Alternative Flows:**
- 5a. Invalid email → Show error message
- 2a. User presses Escape → Modal closes, no change

---

### UC-5: Retake Test for Improvement

**Actor:** Sarah (Test Taker)

**Precondition:**
- User has completed at least one full test

**Main Flow:**
1. User sees "Retake Test" button on home page
2. User reviews previous score (e.g., 35/38)
3. User clicks "Retake Test"
4. System clears current session
5. System generates new attempt ID
6. Test starts fresh from Reading Part 1
7. User completes entire test
8. System saves as new attempt
9. System updates display:
   - Attempts: 2 (incremented)
   - Latest Score: 37/38 (improved!)
10. User can compare attempts

**Postcondition:**
- New attempt in JSON
- Latest score displayed
- History preserved

---

### UC-6: Clear Session and Start Over

**Actor:** Michael (Student)

**Precondition:**
- User has active session

**Main Flow:**
1. User clicks "Clear Session" link
2. System clears all session data
3. System displays confirmation page
4. User clicks "Back to Home"
5. System shows fresh home page
6. User can set new email or continue

**Postcondition:**
- Session cleared
- Historical data preserved in JSON

**Alternative Flows:**
- Historical JSON data remains intact

---

## User Stories

### Epic 1: Test Taking

**Story 1.1:** As a test taker, I want to take a timed practice test that simulates real CELPIP conditions, so that I can prepare effectively.
- **Acceptance Criteria:**
  - ✅ Timer counts down from configured time
  - ✅ Sequential part navigation (no going back)
  - ✅ Auto-submit when time expires
  - ✅ Only "Quit" option available during test

**Story 1.2:** As a student, I want to practice individual test parts without time pressure, so that I can learn at my own pace.
- **Acceptance Criteria:**
  - ✅ Can select any part from skill page
  - ✅ Timer still runs but is informational
  - ✅ Can navigate freely between parts
  - ✅ Immediate feedback on answers

**Story 1.3:** As a user, I want to see my answers marked as correct or incorrect, so that I can learn from mistakes.
- **Acceptance Criteria:**
  - ✅ Green checkmark for correct answers
  - ✅ Red X for incorrect answers
  - ✅ Show what user selected
  - ✅ Show correct answer for comparison

---

### Epic 2: Progress Tracking

**Story 2.1:** As a working professional, I want my test results tracked by email, so that I can review my progress over time.
- **Acceptance Criteria:**
  - ✅ Email required before Test Mode
  - ✅ All attempts saved to JSON
  - ✅ Email associated with each attempt
  - ✅ Can change email anytime

**Story 2.2:** As a returning user, I want to see how many times I've taken each test, so that I can track my practice frequency.
- **Acceptance Criteria:**
  - ✅ Attempt count displayed per test
  - ✅ Latest score shown
  - ✅ Percentage calculated
  - ✅ Historical data preserved

**Story 2.3:** As a user, I want to see my improvement over multiple attempts, so that I can measure progress.
- **Acceptance Criteria:**
  - ✅ Each attempt saved separately
  - ✅ Timestamps recorded
  - ✅ Scores comparable
  - ✅ Can retake unlimited times

---

### Epic 3: User Experience

**Story 3.1:** As a user, I want a clean, modern interface, so that practice is enjoyable.
- **Acceptance Criteria:**
  - ✅ Gradient color schemes
  - ✅ Smooth animations
  - ✅ Clear visual hierarchy
  - ✅ Responsive design

**Story 3.2:** As a mobile user, I want the site to work on my phone, so that I can practice anywhere.
- **Acceptance Criteria:**
  - ✅ Responsive layouts
  - ✅ Touch-friendly buttons
  - ✅ Readable text on small screens
  - ✅ Modal adapts to screen size

**Story 3.3:** As a user, I want to easily manage my email address, so that I don't need to navigate away from the home page.
- **Acceptance Criteria:**
  - ✅ Modal popup for email entry
  - ✅ Can change email anytime
  - ✅ Clear session option
  - ✅ Visual indication of login status

---

## Scenarios

### Scenario 1: First-Time Full Test Experience

**Context:** Sarah has never used the app and wants to take her first practice test.

**Steps:**
1. Sarah opens the website
2. She sees a yellow warning: "⚠️ No email set"
3. She clicks "Set Email Address"
4. Modal pops up smoothly
5. She types: "sarah.chen@email.com"
6. Clicks "Save Email"
7. Page reloads, blue banner shows: "👤 Logged in as: sarah.chen@email.com"
8. She sees Test 1 card with two buttons
9. She clicks "🎯 Test Mode" (the red/pink gradient button)
10. Reading Part 1 starts with 16.5-minute timer
11. She reads the correspondence and answers 11 questions
12. Clicks "Next Part →"
13. System auto-navigates to Part 2
14. She completes all 4 reading parts
15. Final screen shows: "Reading Section Complete! 35/38 (92.1%)"
16. She clicks "Continue to Listening →"
17. (Only Reading is available, so test ends)
18. Back to home page
19. She sees:
    - "✅ Current Session - 35/38"
    - "📝 Attempts: 1"
    - "🏆 Latest Score: 35/38 (92.1%)"
    - Button changed to "🔄 Retake Test"

**Outcome:** Sarah successfully completed her first test, and all data is tracked.

---

### Scenario 2: Targeted Practice

**Context:** Michael struggles with "Reading for Viewpoints" (Part 4) and wants to practice just that section.

**Steps:**
1. Michael opens the site (already has email set)
2. Clicks "📚 Practice Mode" on Test 1
3. Sees 4 skills: Reading, Listening, Writing, Speaking
4. Clicks "Reading" card
5. Sees 4 parts listed
6. Clicks "Part 4: Reading for Viewpoints"
7. Timer starts: 15 minutes
8. He reads the article and response
9. Answers 10 dropdown questions
10. Clicks "Submit Answers"
11. Results show immediately:
    - "Q1: ✅ Correct - Your answer: A, Correct: A"
    - "Q2: ❌ Incorrect - Your answer: B, Correct: C"
    - ...
12. Score: "7/10 (70%)"
13. He reviews his mistakes
14. Clicks "Next Part →" to try Part 1
15. Or clicks "← Back to Test 1" to practice something else

**Outcome:** Michael practiced his weak area with immediate feedback.

---

### Scenario 3: Score Improvement Journey

**Context:** Priya took Test 1 and scored 35/38. She wants to improve and take it again.

**Attempt 1 (Week 1):**
1. First attempt: 35/38 (92.1%)
2. Main page shows: "📝 Attempts: 1, 🏆 Latest: 35/38"

**Attempt 2 (Week 2):**
1. Priya clicks "🔄 Retake Test"
2. Takes test again, more carefully
3. Scores: 37/38 (97.4%)
4. Main page updates: "📝 Attempts: 2, 🏆 Latest: 37/38 (97.4%)"
5. She's happy to see improvement!

**Attempt 3 (Week 3):**
1. Clicks "🔄 Retake Test" again
2. Aims for perfect score
3. Scores: 38/38 (100%)
4. Main page shows: "📝 Attempts: 3, 🏆 Latest: 38/38 (100%)"
5. Perfect score achieved! 🎉

**Data in JSON:**
```json
{
  "priya.patel@email.com": {
    "test_1": {
      "attempts": [
        {"total_score": 35, "completed_at": "2025-12-04"},
        {"total_score": 37, "completed_at": "2025-12-11"},
        {"total_score": 38, "completed_at": "2025-12-18"}
      ]
    }
  }
}
```

**Outcome:** Clear progress tracking motivates Priya to keep improving.

---

### Scenario 4: Email Management

**Context:** Sarah wants to switch from personal email to work email for tracking.

**Steps:**
1. Sarah logs in with "sarah.chen@email.com"
2. She notices the blue banner at top
3. Clicks "✏️ Change Email"
4. Modal appears
5. She types: "s.chen@company.com"
6. Clicks "Save Email"
7. Page reloads
8. Banner now shows: "👤 Logged in as: s.chen@company.com"
9. All future tests will be tracked under new email
10. Her old email's data remains in JSON (separate user)

**Outcome:** Sarah successfully changed her tracking email.

---

### Scenario 5: Multiple Test Selection

**Context:** Michael has practiced Test 1 multiple times and wants to try Test 2 for variety.

**Main Page View:**
```
┌─────────────────────────────────┐
│            Test 1               │
│  📝 Attempts: 5                 │  ← Well practiced
│  🏆 Latest: 37/38 (97.4%)       │
│  [📚 Practice] [🔄 Retake]      │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│            Test 2               │
│  📝 Attempts: 0                 │  ← Never taken
│  [📚 Practice] [🎯 Test Mode]   │
└─────────────────────────────────┘
```

**Steps:**
1. Michael decides to try Test 2
2. Clicks "🎯 Test Mode" on Test 2
3. Email already set, test starts immediately
4. Completes Test 2
5. Scores: 36/38
6. Returns to home page
7. Now both tests show history:
   - Test 1: 5 attempts, latest 37/38
   - Test 2: 1 attempt, latest 36/38

**Outcome:** Michael can practice multiple tests and track progress on each.

---

### Scenario 6: Session vs Persistent Data

**Context:** Understanding the difference between session and JSON storage.

**Session Data (Temporary):**
- Current test in progress
- Current session scores
- Last viewed pages
- Cleared when:
  - Browser closed
  - "Clear Session" clicked
  - Retake Test clicked

**JSON Data (Permanent):**
- All completed attempts
- User's answers per question
- Historical scores
- Timestamps
- Preserved when:
  - Session cleared
  - Browser closed
  - App restarted

**Example:**
1. User completes test: Both session AND JSON updated
2. User closes browser: Session lost, JSON intact
3. User returns: JSON shows history, session empty
4. User clicks "Clear Session": Session cleared, JSON intact
5. User takes test again: New session, new JSON entry

**Outcome:** Users understand data persistence.

---

## Edge Cases & Error Handling

### Edge Case 1: Time Expires
- **Trigger:** Timer reaches 0:00
- **Action:** Auto-submit current answers
- **Message:** "Time is up! Moving to next part..."
- **Result:** Unanswered questions marked as incorrect

### Edge Case 2: Invalid Email
- **Trigger:** User enters "notanemail"
- **Action:** Validation fails
- **Message:** "Please enter a valid email address"
- **Result:** Form not submitted, user can correct

### Edge Case 3: Network Error
- **Trigger:** Server unreachable during submit
- **Action:** JavaScript catches error
- **Message:** "An error occurred. Please try again."
- **Result:** User can retry submission

### Edge Case 4: Modal Close Without Save
- **Trigger:** User presses Escape or clicks outside
- **Action:** Modal closes
- **Message:** None
- **Result:** No changes made, original email intact

### Edge Case 5: Incomplete Test (Quit)
- **Trigger:** User clicks "✕ Quit Test" mid-exam
- **Action:** Return to home page
- **Message:** None
- **Result:** Partial attempt NOT saved, can restart

---

*Last Updated: December 2025*

