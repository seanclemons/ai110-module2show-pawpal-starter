# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

PawPal+ includes intelligent algorithms to make pet care planning easier and more efficient:

### 🔄 **Flexible Sorting Options**

Sort your tasks multiple ways to find the best schedule:
- **By Priority**: Critical tasks (medication, feeding) scheduled first
- **By Duration**: Quick tasks first to maximize completion count
- **Smart Combo**: Priority + duration for optimal balance
- **By Pet**: Group all tasks for each pet together
```python

## 🧪 Testing PawPal+

### Running Tests

PawPal+ includes a comprehensive test suite to ensure reliability and correctness.

# Run all tests
python -m pytest
Test suite includes **26 automated tests** that verify:

- **Core functionality**: Task creation, completion tracking, pet/owner management, and input validation
- **Sorting algorithms**: Tasks sorted correctly by priority, duration, and multi-criteria combinations
- **Filtering methods**: Filtering by pet, completion status, priority level, and task type
- **Conflict detection**: Identifying overlapping tasks, same-pet conflicts, and validating sequential tasks
- **Edge cases**: Empty collections, zero available time, perfect time fits, and invalid inputs
- **Performance**: System handles 100+ tasks efficiently in under 1 second

**Test Results**: ✅ 26/26 passing in 0.19s

**Confidence Level**: 5 stars