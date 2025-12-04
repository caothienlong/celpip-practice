# 🎨 UI/UX Design Guide

## Table of Contents
1. [Design Philosophy](#design-philosophy)
2. [Color Palette](#color-palette)
3. [Visual Components](#visual-components)
4. [User Flows](#user-flows)
5. [Responsive Design](#responsive-design)

---

## Design Philosophy

### Core Principles
- **Clarity**: Clear visual hierarchy and intuitive navigation
- **Consistency**: Unified design language across all pages
- **Accessibility**: Easy to read, use, and understand
- **Modern**: Clean gradients and smooth animations
- **Purposeful**: Every element serves a function

---

## Color Palette

### Primary Colors
```css
/* Purple Gradient - Main Theme */
#667eea → #764ba2  /* Used for: Headers, main actions, branding */

/* Pink/Red Gradient - Test Mode */
#f093fb → #f5576c  /* Used for: Test Mode, urgent actions */

/* Green Gradient - Success */
#a8e6cf → #56cc9d  /* Used for: Completion badges, success states */

/* Purple/Pink - Retake */
#fbc2eb → #a18cd1  /* Used for: Retake buttons */
```

### Neutral Colors
```css
/* Backgrounds */
#ffffff  /* White - Cards, modals */
#f8f9fa  /* Light gray - Passages, question containers */
#f0f0f0  /* Gray - Disabled states */

/* Text */
#333333  /* Dark gray - Primary text */
#666666  /* Medium gray - Secondary text */
#999999  /* Light gray - Disabled text */

/* Borders */
#e0e0e0  /* Light border */
#667eea  /* Accent border (focused inputs) */
```

### Status Colors
```css
/* Info */
#f0f7ff  /* Background */
#667eea  /* Border/Text */

/* Warning */
#fff3cd  /* Background */
#ffc107  /* Border/Text */

/* Error */
#ffebee  /* Background */
#f44336  /* Border/Text */

/* Success */
#e8f5e9  /* Background */
#4caf50  /* Border/Text */
```

---

## Visual Components

### 1. Test Cards (Main Page)

```
┌─────────────────────────────────────┐
│              1                      │  ← Large gradient number
│       Practice Test 1               │  ← Title
│  ✅ Current Session - 37/38        │  ← Status badge (green)
│                                     │
│  ┌──────────────────────────────┐  │
│  │ 📝 Attempts: 3               │  │  ← History box
│  │ 🏆 Latest Score: 37/38       │  │
│  │              (97.4%)         │  │
│  └──────────────────────────────┘  │
│                                     │
│  [📚 Practice Mode]                │  ← Purple gradient
│  [🔄 Retake Test]                  │  ← Purple/pink gradient
└─────────────────────────────────────┘
```

**States:**
- **Not Started**: Gray background, no history box
- **In Progress**: Session badge shows current score
- **Completed**: Green badge + history box
- **Template**: Gray badge, disabled Test Mode button

**Hover Effects:**
- Card lifts up (`translateY(-5px)`)
- Border changes to accent color
- Shadow intensifies

---

### 2. Email Management

#### Warning Banner (No Email)
```
┌─────────────────────────────────────────┐
│  ⚠️ No email set                        │
│      📧 Set Email Address               │  ← Link to modal
│  Setting your email will enable test    │
│  result tracking and history.           │
└─────────────────────────────────────────┘
```
- Yellow background (#fff3cd)
- Orange border (#ffc107)
- Prominent call-to-action

#### Info Banner (Email Set)
```
┌─────────────────────────────────────────┐
│  👤 Logged in as: user@example.com      │
│      ✏️ Change Email  |  ✕ Clear Session│
└─────────────────────────────────────────┘
```
- Blue background (#f0f7ff)
- Blue border (#667eea)
- Shows current email

#### Email Modal
```
┌────────────────────────────────────┐
│  📧 Set Email Address          ✕  │
│                                    │
│  Enter your email to track test   │
│  results and progress              │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ your.email@example.com       │ │  ← Input field
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │       Save Email             │ │  ← Purple gradient
│  └──────────────────────────────┘ │
└────────────────────────────────────┘
```
- Centered on screen
- Semi-transparent black overlay
- Smooth animations (fade-in + slide-down)
- Closes on Escape or outside click

---

### 3. Mode Buttons

#### Practice Mode Button
```css
Background: Linear gradient (Purple #667eea → #764ba2)
Padding: 12px 20px
Border-radius: 10px
Box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3)

Hover: translateY(-2px) + stronger shadow
```

#### Test Mode Button
```css
Background: Linear gradient (Pink #f093fb → Red #f5576c)
Padding: 12px 20px
Border-radius: 10px
Box-shadow: 0 3px 10px rgba(245, 87, 108, 0.3)

Hover: translateY(-2px) + stronger shadow
```

#### Retake Test Button
```css
Background: Linear gradient (Pink #fbc2eb → Purple #a18cd1)
Padding: 12px 20px
Border-radius: 10px
Box-shadow: 0 3px 10px rgba(161, 140, 209, 0.3)

Hover: translateY(-2px) + stronger shadow
```

---

### 4. Test Interface

#### Timer Display
```
┌─────────────┐
│   ⏰ 16:30  │  ← Large, centered
└─────────────┘

States:
- Normal: Blue (#667eea)
- Warning (<60s): Red (#f5576c) + pulse animation
```

#### Progress Bar (Test Mode Only)
```
▓▓▓▓▓▓▓▓░░░░░░░░ 25%
Part 1/4 - Reading
```
- Gradient fill matches mode color
- Shows current part / total parts
- Smooth transitions

#### Question Layout
```
Side-by-Side (Desktop):
┌─────────────────┬─────────────────┐
│   📧 Message    │  ❓ Questions   │
│                 │                 │
│   Passage text  │  1. Question?   │
│   goes here...  │  [Dropdown ▼]   │
│                 │                 │
│                 │  2. Question?   │
│                 │  [Dropdown ▼]   │
└─────────────────┴─────────────────┘

Stacked (Mobile):
┌───────────────────────────────────┐
│          📧 Message               │
│   Passage text goes here...       │
└───────────────────────────────────┘
┌───────────────────────────────────┐
│        ❓ Questions               │
│   1. Question? [Dropdown ▼]       │
│   2. Question? [Dropdown ▼]       │
└───────────────────────────────────┘
```

#### Dropdown Questions
```
1. What is the main purpose?
   [Select an answer ▼                    ]

States:
- Default: Gray border (#e0e0e0)
- Focused: Blue border (#667eea)
- Answered: Green background + border (#4caf50)
```

---

### 5. Results Display

#### Practice Mode (Per Part)
```
┌──────────────────────────────────────┐
│          Results                     │
│                                      │
│  Your Score: 10/11 (90.9%)          │
│  ✅ 10 correct   ❌ 1 incorrect      │
│                                      │
│  Q1: ✅ Correct                      │
│      Your answer: A                  │
│      Correct answer: A               │
│                                      │
│  Q2: ❌ Incorrect                    │
│      Your answer: B                  │
│      Correct answer: C               │
│                                      │
│  Running Total: 10/11 points         │
│                                      │
│  [Next Part →]                       │
└──────────────────────────────────────┘
```

#### Test Mode (End of Skill)
```
┌──────────────────────────────────────┐
│    Reading Section Complete!         │
│                                      │
│            37/38                     │  ← Large score
│                                      │
│  You got 37 out of 38 correct       │
│           (97.4%)                    │
│                                      │
│  [Continue to Listening →]           │
└──────────────────────────────────────┘
```

---

## User Flows

### Flow 1: First-Time User - Test Mode

```
1. Home Page
   ↓
2. No email banner displayed
   ↓
3. User clicks "Set Email Address"
   ↓
4. Modal opens
   ↓
5. User enters email
   ↓
6. Click "Save Email"
   ↓
7. Page reloads with email banner
   ↓
8. User clicks "🎯 Test Mode"
   ↓
9. Test starts at Reading Part 1
   ↓
10. Complete Part 1 → Auto-navigate to Part 2
    ↓
11. Complete Part 2 → Auto-navigate to Part 3
    ↓
12. Complete Part 3 → Auto-navigate to Part 4
    ↓
13. Complete Part 4 → Show Reading final score
    ↓
14. Click "Continue to Listening"
    ↓
    ... (repeat for each skill)
    ↓
15. Complete all skills → "🎉 Test Complete!"
    ↓
16. Click "Back to Home"
    ↓
17. Main page shows:
    - "✅ Current Session - 37/38"
    - "📝 Attempts: 1"
    - "🏆 Latest Score: 37/38 (97.4%)"
    - Button changed to "🔄 Retake Test"
```

### Flow 2: Returning User - Practice Mode

```
1. Home Page (email already set)
   ↓
2. User clicks "📚 Practice Mode"
   ↓
3. Test detail page shows 4 skills
   ↓
4. User clicks "Reading Part 2"
   ↓
5. Test Part 2 loads with timer
   ↓
6. User answers questions
   ↓
7. Click "Submit Answers"
   ↓
8. Results shown immediately (per question)
   ↓
9. Running total displayed
   ↓
10. User can:
    - Go to Next Part
    - Go back to Test detail
    - Jump to any part
```

### Flow 3: Retake Test

```
1. Home Page (completed test shown)
   ↓
2. User clicks "🔄 Retake Test"
   ↓
3. Session cleared (new attempt_id created)
   ↓
4. Test starts fresh from Reading Part 1
   ↓
5. Complete entire test (sequential)
   ↓
6. New attempt saved to JSON
   ↓
7. Main page updates:
    - "📝 Attempts: 2" (incremented)
    - "🏆 Latest Score: 38/38" (new score)
```

### Flow 4: Change Email

```
1. Home Page (logged in)
   ↓
2. User clicks "✏️ Change Email"
   ↓
3. Modal opens with current email
   ↓
4. User enters new email
   ↓
5. Click "Save Email"
   ↓
6. Page reloads
   ↓
7. New email displayed
   ↓
8. Future tests tracked under new email
```

---

## Responsive Design

### Breakpoints

```css
/* Desktop */
@media (min-width: 1024px) {
    - Side-by-side layouts
    - Grid: 3 columns
    - Full features
}

/* Tablet */
@media (min-width: 768px) and (max-width: 1023px) {
    - Side-by-side layouts
    - Grid: 2 columns
    - Slightly smaller fonts
}

/* Mobile */
@media (max-width: 767px) {
    - Stacked layouts
    - Grid: 1 column
    - Larger touch targets
    - Simplified navigation
}
```

### Mobile Adaptations

1. **Test Cards**: Stack vertically, full width
2. **Questions**: Passage above, questions below
3. **Buttons**: Full width, larger padding
4. **Modal**: 95% width, more padding
5. **Timer**: Larger, more prominent
6. **Dropdowns**: Wider for easier touch

---

## Animations

### Page Transitions
- **Fade-in**: 0.3s ease
- **Slide-down**: 0.3s ease (modals)
- **Smooth scroll**: Navigation between sections

### Interactive Elements
- **Hover lift**: `translateY(-2px)`, 0.3s
- **Button press**: `translateY(0)`, 0.1s
- **Modal backdrop**: Fade-in 0.3s
- **Timer warning**: Pulse 1s infinite

### Loading States
- **Saving**: Button text changes to "Saving..."
- **Processing**: Button disabled, gray background
- **Auto-navigate**: Smooth page transition

---

## Accessibility

### Features
- ✅ High contrast ratios (WCAG AA compliant)
- ✅ Large, readable fonts (minimum 16px)
- ✅ Clear focus indicators (blue border)
- ✅ Keyboard navigation (Tab, Enter, Escape)
- ✅ Descriptive labels and placeholders
- ✅ Error messages with clear instructions

### Keyboard Shortcuts
- `Tab`: Navigate between elements
- `Enter`: Submit forms, click buttons
- `Escape`: Close modal
- `Arrow keys`: Navigate dropdowns

---

## Icon Usage

### Emojis as Icons
```
📚 - Practice Mode, Reading
🎯 - Test Mode, Goals
🔄 - Retake, Refresh
👤 - User, Profile
📧 - Email
✏️ - Edit
✕ - Close, Clear
⚠️ - Warning
✅ - Success, Complete
❌ - Error, Incorrect
🏆 - Score, Achievement
📝 - Attempts, Notes
⏰ - Timer, Clock
📊 - Diagram, Stats
📰 - Article, News
💬 - Message, Comment
```

---

## Best Practices

### Do's ✅
- Use consistent spacing (multiples of 5px)
- Maintain gradient directions (135deg)
- Keep animations subtle and purposeful
- Provide clear feedback on actions
- Use white space effectively
- Test on multiple screen sizes

### Don'ts ❌
- Don't mix too many colors
- Don't use animations longer than 0.5s
- Don't hide important actions
- Don't use small touch targets (<44px)
- Don't rely on color alone for meaning
- Don't create more than 3 levels of hierarchy

---

## Future Enhancements

### Potential Improvements
1. **Dark Mode**: Alternative color scheme
2. **Custom Themes**: User-selectable colors
3. **Print Styles**: Clean printable results
4. **Reduced Motion**: Respect user preferences
5. **High Contrast**: Enhanced accessibility mode
6. **Font Size Controls**: User-adjustable text size

---

*Last Updated: December 2025*

