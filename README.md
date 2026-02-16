# PawPal+ 🐾

**An intelligent pet care scheduling assistant built with Python and Streamlit**

PawPal+ helps busy pet owners stay consistent with pet care by tracking tasks, considering constraints, and generating optimized daily schedules with smart algorithms and conflict detection.

---

## 📸 Demo

<a href="/course_images/ai110/pawpal_screenshot.png" target="_blank"><img src='/course_images/ai110/pawpal_screenshot.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

*PawPal+ Streamlit interface showing schedule generation with conflict detection*

---

## ✨ Features

### 🐾 **Multi-Pet Management**
- Track care for unlimited pets (dogs, cats, birds, rabbits, etc.)
- Store pet details: name, species, age, and special needs
- Aggregate tasks across all pets automatically

### 📋 **Smart Task Tracking**
- Define tasks with detailed attributes:
  - **Duration**: Time needed in minutes
  - **Priority**: 1 (highest/critical) to 5 (lowest/optional)
  - **Type**: Feeding, walks, medication, grooming, enrichment, cleaning
  - **Recurrence**: Daily, weekly, or one-time tasks
  - **Completion Status**: Mark tasks as done or pending

### 🧠 **Intelligent Scheduling Algorithms**

#### **Multiple Sorting Strategies**
Choose how to prioritize your tasks:
- **🎯 Priority First**: Critical tasks (medication, feeding) scheduled first - never skip important care
- **⏱️ Shortest First**: Quick tasks scheduled first - maximize number of completed tasks
- **🧠 Smart Combo**: Priority + duration optimization - best balance of importance and efficiency

#### **Advanced Filtering**
Focus on what matters with powerful filters:
- **By Pet**: View tasks for a specific pet only
- **By Status**: Show incomplete tasks or completed tasks
- **By Priority**: Filter high-priority (1-2), medium (3), or low (4-5) tasks
- **By Type**: Group similar tasks (all feedings, all walks, etc.)
- **Quick Access**: Get all high-priority tasks with one method call

### ⚠️ **Automatic Conflict Detection**
Never double-book your time:
- **Time Overlap Detection**: Identifies tasks scheduled at the same time
- **Pet Resource Conflicts**: Detects when same pet has multiple simultaneous tasks
- **Visual Warnings**: Clear, actionable messages explain conflicts
- **Smart Time Assignment**: Automatically schedules tasks sequentially to avoid conflicts
- **Helpful Tips**: Suggestions to resolve scheduling problems

### 📊 **Real-Time Analytics**
Track your scheduling efficiency:
- **Tasks Scheduled**: Count of tasks that fit in available time
- **Time Used**: Total minutes allocated to pet care
- **Efficiency Percentage**: How well you're using available time
- **Conflict Count**: Number of tasks that didn't fit

### 🎨 **Professional UI/UX**
- Clean, intuitive Streamlit interface
- Color-coded priorities (🔴 High, 🟡 Medium, 🟢 Low)
- Status indicators (✅ Completed, ⭕ Pending)
- Interactive filtering and sorting
- Data tables for easy viewing
- One-click task completion toggling

---

## 🏗️ System Architecture

### Core Classes

```
Owner → Pet → Task
  ↓
Scheduler
```

**`Owner`**: Represents pet owner with available time and preferences
- Manages multiple pets
- Aggregates all tasks across pets
- Tracks daily available time (minutes)

**`Pet`**: Represents a pet with details and special needs
- Stores pet information (name, species, age)
- Maintains list of care tasks
- Auto-registers with owner

**`Task`**: Represents a care task
- Duration, priority, type, recurrence
- Completion tracking
- Optional scheduled time for conflict detection
- Auto-registers with pet
- Input validation (priority 1-5, positive duration)

**`Scheduler`**: The "brain" that organizes tasks
- **5 Sorting Methods**: Priority, duration, smart combo, pet name, descending duration
- **5 Filtering Methods**: By pet, status, priority, type, high-priority
- **7 Conflict Detection Methods**: Time overlaps, pet conflicts, warnings, auto-assignment
- **Core Algorithm**: Greedy scheduling (O(n log n) time complexity)
- Daily plan generation with configurable strategies

### Design Patterns

- **Auto-Registration**: Tasks/Pets automatically register with parents (`__post_init__()`)
- **Aggregation**: Owner aggregates all tasks from all pets
- **Strategy Pattern**: Multiple sorting algorithms selectable at runtime
- **Validation**: Input validation prevents invalid data entry

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd pawpal-starter

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
# Launch Streamlit UI
streamlit run app.py

# Run CLI demo
python main.py

# Run tests
python -m pytest
```

---

## 📖 Usage Guide

### 1. Create Owner Profile
- Enter your name
- Set available time per day (in minutes)
- Click "Create/Update Owner Profile"

### 2. Add Pets
- Enter pet name, species, and age
- Add special needs (optional): medications, dietary restrictions, etc.
- Click "Add Pet"
- Repeat for multiple pets

### 3. Create Tasks
- Select which pet the task is for
- Enter task details:
  - **Name**: "Morning walk", "Feed breakfast", etc.
  - **Type**: feeding, walk, medication, grooming, enrichment, cleaning
  - **Duration**: Time needed in minutes (5-240)
  - **Priority**: 1 (highest) to 5 (lowest)
  - **Recurrence**: daily, weekly, once
- Click "Add Task"

### 4. Filter and View Tasks
- Use filters to focus on specific tasks:
  - Filter by pet name
  - Filter by completion status (incomplete/completed)
  - Filter by priority level (high/medium/low)
- Toggle task completion with one click

### 5. Generate Schedule
- Choose scheduling algorithm:
  - **Priority First**: For ensuring critical tasks never get skipped
  - **Shortest First**: For maximizing number of completed tasks
  - **Smart Combo**: For best balance
- Click "Generate Schedule"
- Review schedule with time slots (e.g., "08:00 - 08:30")
- Check for conflict warnings at top
- View tasks that didn't fit in "Tasks That Didn't Fit" section

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run with coverage report
python -m pytest --cov=pawpal_system --cov-report=term-missing

# Run specific test categories
python -m pytest -k "sorting"      # Only sorting tests
python -m pytest -k "conflict"     # Only conflict detection tests
python -m pytest -k "edge"         # Only edge case tests
```

### Test Coverage

**26 comprehensive tests** covering:

- ✅ **Core Functionality (7 tests)**: Task management, pet registration, validation
- ✅ **Sorting Algorithms (4 tests)**: Priority, duration, multi-criteria, alphabetical
- ✅ **Filtering Methods (5 tests)**: Pet, status, priority, type filters
- ✅ **Conflict Detection (6 tests)**: Time overlaps, pet conflicts, sequential validation
- ✅ **Edge Cases (3 tests)**: Empty collections, zero time, perfect fits
- ✅ **Performance (1 test)**: 100+ tasks in < 1 second

### Test Results

```
================================ test session starts =================================
collected 26 items

tests/test_pawpal.py ..............................                           [100%]

================================= 26 passed in 0.19s ==================================
```

**Confidence Level**: ⭐⭐⭐⭐⭐ (5/5 stars) - Production-ready with comprehensive coverage

---

## 🧠 Algorithm Details

### Greedy Scheduling Algorithm

```python
1. Load all tasks from owner's pets
2. Sort tasks by chosen method (priority/duration/smart)
3. Iterate through sorted tasks
4. Add task if it fits in remaining time
5. Otherwise, add to conflicts list
6. Return daily plan
```

**Time Complexity**: O(n log n) due to sorting  
**Space Complexity**: O(n) for storing tasks

**Trade-off**: Prioritizes critical tasks (pet health) over maximizing task count. A high-priority 60-minute walk will be scheduled over three low-priority 20-minute tasks, ensuring important care is never skipped.

### Conflict Detection

```python
1. Get all tasks with scheduled times
2. Check every pair of tasks for overlap
3. Overlap if: task1_start < task2_end AND task2_start < task1_end
4. Return list of conflicting pairs with reasons
```

**Time Complexity**: O(n²) for checking all pairs  
**Trade-off**: Simple and effective for typical pet care scenarios (< 50 tasks per day)

### Sorting Strategies

| Strategy | Best For | Example Use Case |
|----------|----------|------------------|
| Priority First | Critical tasks never skipped | Pet with daily medication |
| Shortest First | Maximize completed tasks | Busy day with many quick tasks |
| Smart Combo | Balance importance & efficiency | Normal day with mixed priorities |

---

## 📁 Project Structure

```
pawpal-starter/
├── app.py                    # Streamlit UI (polished interface)
├── pawpal_system.py          # Core logic (Owner, Pet, Task, Scheduler)
├── main.py                   # CLI demo script with algorithm tests
├── tests/
│   ├── __init__.py
│   └── test_pawpal.py        # 26 comprehensive tests
├── docs/
│   ├── architecture.md       # System design documentation
│   └── uml_final.png         # Final UML class diagram
├── reflection.md             # Design decisions and tradeoffs
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .gitignore
```

---

## 🎓 Learning Outcomes

This project demonstrates:

- ✅ **Object-Oriented Programming**: Classes, inheritance, encapsulation with Python dataclasses
- ✅ **Algorithm Design**: Sorting (5 methods), filtering (5 methods), greedy scheduling
- ✅ **System Architecture**: UML diagrams, class relationships, design patterns
- ✅ **Test-Driven Development**: 26 pytest tests with 100% pass rate
- ✅ **Web Development**: Streamlit UI with session state management
- ✅ **Data Validation**: Input validation and error handling
- ✅ **Documentation**: README, UML, code comments, docstrings
- ✅ **AI Collaboration**: Human-AI partnership throughout development

---

## 🚧 Known Limitations

These are intentional design decisions for an MVP:

- **No travel time**: Doesn't account for travel between locations (e.g., park to home)
- **No owner energy**: Doesn't track owner fatigue or energy levels
- **No time-of-day preferences**: Tasks scheduled sequentially, not at specific times (e.g., "morning walk")
- **No task dependencies**: Doesn't enforce order (e.g., "feed before medication")
- **Single-day planning**: Doesn't optimize across multiple days
- **No recurring automation**: Daily tasks don't auto-reset (future enhancement)

---

## 🔮 Future Enhancements

Potential improvements:

- 📅 **Recurring Task Automation**: Daily reset of completed tasks
- ⏰ **Time-of-Day Preferences**: Morning walks, evening feeding slots
- 🔗 **Task Dependencies**: Enforce ordering (feed → medication)
- 📍 **Location Tracking**: Travel time between activities
- 📊 **Analytics Dashboard**: Track completion rates over time
- 🔔 **Reminders**: Push notifications for upcoming tasks
- 📱 **Mobile App**: Native iOS/Android version
- 👥 **Multi-User**: Shared pet custody scheduling
- 🌐 **Calendar Integration**: Sync with Google Calendar, iCal
- 💾 **Cloud Sync**: Save schedules across devices

---

## 🛠️ Technologies Used

- **Python 3.10+**: Core programming language
- **Streamlit**: Web UI framework
- **pytest**: Testing framework
- **Python Dataclasses**: Clean OOP implementation
- **Mermaid.js**: UML diagram generation
- **Git/GitHub**: Version control

---

## 📝 License

This is an educational project for AI-assisted software development learning.

---

## 🙏 Acknowledgments

Built as part of an AI-assisted development learning module focusing on:
- System design with UML
- CLI-first development workflow
- Algorithm implementation and optimization
- Human-AI collaboration patterns
- Test-driven development
- Professional documentation

**Special thanks to**:
- Anthropic's Claude for AI assistance throughout development
- Streamlit team for the excellent UI framework
- Python community for comprehensive libraries and tools

---

## 📧 Contact

**Project Link**: [Your GitHub Repository URL]

**Developer**: [Your Name]

---

**Made with 🐾 and ❤️ by [Your Name]**

*PawPal+ - Because every pet deserves consistent, quality care*