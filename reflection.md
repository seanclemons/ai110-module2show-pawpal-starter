# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
Before implementation, I identified three core user actions:

1. **Add and Manage Pets**: Register pet(s) with basic info (name, species, age, special needs)
2. **Create and Prioritize Care Tasks**: Define tasks with duration, priority, and recurrence
3. **Generate Daily Schedule**: Request an optimized daily plan based on constraints and priorities

Based on these actions, I plan to design four main classes:
- **Owner**: Represents the pet owner with preferences and time constraints
- **Pet**: Represents a pet with attributes and special needs
- **Task**: Represents a care task with duration, priority, frequency, and assignment to a pet
- **Scheduler**: Contains the algorithmic logic to organize tasks into a daily plan

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

My scheduler uses a **greedy algorithm** that sorts tasks by priority and schedules them sequentially until time runs out. This means:

- **What it does**: Picks the highest priority task, then the next highest, and so on
- **What it sacrifices**: May not maximize the total number of tasks completed

**Example scenario:**
- Available time: 60 minutes
- Tasks: High-priority 50-min walk, Medium-priority 20-min feeding, Medium-priority 15-min grooming

**Greedy result**: Schedules the 50-min walk (total: 1 task, 50 min used)
**Optimal result**: Could schedule both medium tasks (total: 2 tasks, 35 min used)

**Why this tradeoff is reasonable:**

In pet care, **priority matters more than quantity**. A pet owner would rather ensure their dog gets its critical arthritis medication (5 min, high priority) than fit in three optional grooming tasks (90 min total, low priority). The greedy approach guarantees that the most important tasks never get skipped, even if it means fewer total tasks complete.

Additionally, the greedy algorithm runs in O(n log n) time (due to sorting), making it fast and predictable even with many tasks.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
