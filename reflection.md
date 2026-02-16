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

During implementation, I made several key enhancements. I added automatic registration using `__post_init__()` in Pet and Task classes so objects register themselves with their parents, eliminating manual tracking errors. I added `Owner.get_all_tasks()` to aggregate tasks from all pets, providing a clean interface for the Scheduler to retrieve all tasks in one call. I also added input validation to the Task class that raises ValueError for negative durations or invalid priorities (not 1-5), preventing bugs from bad data. Finally, I added a `scheduled_time` attribute to Task to support conflict detection, allowing the system to identify overlapping tasks. These changes made the system more robust and user-friendly while maintaining the original UML architecture.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers three main constraints: available time (Owner's daily minutes for pet care), task priority (1 being highest/critical to 5 being lowest/optional), and task duration (minutes required per task). I prioritized these constraints in order of importance: priority first (ensuring critical tasks like medication and feeding are never skipped), then duration (to fit tasks within the time limit). The available time constraint is a hard limit—tasks that don't fit are moved to the conflicts list rather than being scheduled. This approach ensures pet health and safety take precedence over completing the maximum number of tasks.


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

I used Claude as a collaborative partner throughout the project for design, implementation, and testing. During the design phase, Claude helped me brainstorm class structures and generate Mermaid.js UML diagrams by analyzing the pet care scheduling problem. For implementation, the AI scaffolded class stubs with proper dataclasses and type hints, and explained advanced Python concepts like lambda functions and list comprehensions. During testing, Claude generated 26 comprehensive test cases covering edge cases I hadn't considered, such as zero available time and back-to-back tasks. The most helpful prompts were specific and referenced my code directly, like "Based on my `#file:pawpal_system.py`, what edge cases should I test?" and "How can I make this code more Pythonic while keeping it readable?"


**b. Judgment and verification**

When implementing filtering methods, Claude suggested a highly compact list comprehension combining multiple conditions into one function: `return [t for t in self.tasks if (not pet or t.pet.name==pet) and (status is None or t.completed==status) and ...]`. I rejected this suggestion because while technically correct and "Pythonic," it sacrificed readability—the nested conditions were hard to understand at a glance and the function tried to do too many things at once. Instead, I created separate, focused methods like `filter_by_pet()` and `filter_by_completion()` that each had a single, clear purpose. I evaluated this by asking myself, "If I came back to this code in 6 months, would I immediately understand what it does?" The separate methods passed this test, and they were also easier to test and maintain. This experience taught me that "clever" code isn't always better—clarity and maintainability matter more than brevity.


---

## 4. Testing and Verification

**a. What you tested**

I created 26 automated tests covering core functionality (task creation, completion tracking, pet/owner management), sorting algorithms (priority, duration, multi-criteria), filtering methods (by pet, status, priority, type), conflict detection (time overlaps, pet resource conflicts), edge cases (empty collections, zero time available), and performance (100+ tasks). These tests are important because they verify the greedy scheduling algorithm works correctly, ensure conflict detection catches real problems without false positives, validate that edge cases don't crash the system, and prove the system performs well at scale. The comprehensive test suite acts as living documentation of expected system behavior and prevents regressions when making changes.


**b. Confidence**

I am highly confident that my scheduler works correctly because all 26 tests pass consistently in just 0.19 seconds, with zero failures or errors. The tests cover real-world scenarios like overlapping tasks, empty pets, perfect time utilization, and invalid inputs, giving me strong assurance the system handles both normal usage and edge cases gracefully. Edge cases I would test next include recurring task automation (daily reset logic), task dependencies (enforcing "feed before medication" relationships), time-of-day preferences (morning walks), concurrent schedule modifications by multiple users, and very long multi-day tasks. These additional tests would validate complex real-world scenarios beyond typical single-owner, single-day scheduling.


---

## 5. Reflection

**a. What went well**

I'm most satisfied with the conflict detection system, which successfully identifies real scheduling problems like overlapping tasks and same-pet conflicts without producing false positives for valid sequential tasks. The CLI-first development approach was excellent—by building and testing the backend through `main.py` before touching the UI, I caught bugs early and ensured the core logic was solid, so when I connected it to Streamlit, everything worked immediately. The comprehensive test suite (26 tests, 100% pass rate, 0.19s execution) gives me confidence the system is reliable and production-ready.

**b. What you would improve**

If I had another iteration, I would add recurring task automation so daily tasks automatically reset to incomplete each day instead of requiring manual reset. I would also improve the time slot assignment algorithm to let users specify preferred times (e.g., "morning walk between 7-9 AM") instead of just scheduling everything sequentially from 8:00 AM. Finally, I would refactor the Scheduler class, which currently has 27 methods, into separate classes (TaskSorter, TaskFilter, ConflictDetector) following the Single Responsibility Principle to make each component easier to test and maintain.

**c. Key takeaway**

The most important thing I learned is that AI is a powerful collaborator, but the human is still the architect. Claude could generate code quickly and suggest solutions I hadn't considered, but I had to make design decisions about which algorithms to use, evaluate trade-offs between competing approaches, ensure maintainability by rejecting overly clever code, and verify correctness through testing. The AI was like having an expert pair programmer, but I was the lead architect who decided what classes the system needed, which features mattered most, and what "good enough" looked like for an MVP. Working with AI taught me to be more intentional about my decisions—because Claude could implement any approach I described, I had to think carefully about which approach was right, considering maintainability, readability, and user experience. The key skill isn't writing code; it's knowing what code to write and why.
