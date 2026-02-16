"""
PawPal+ Comprehensive Test Suite
Tests for core functionality, edge cases, and algorithms.
"""

import pytest
from pawpal_system import Owner, Pet, Task, Scheduler


# ==================== FIXTURES ====================

@pytest.fixture
def basic_owner():
    """Create a basic owner for testing."""
    return Owner(name="Test Owner", available_time=120)


@pytest.fixture
def owner_with_pets(basic_owner):
    """Create owner with two pets."""
    dog = Pet(name="Max", species="Dog", age=5, owner=basic_owner)
    cat = Pet(name="Whiskers", species="Cat", age=3, owner=basic_owner)
    return basic_owner, dog, cat


# ==================== BASIC FUNCTIONALITY TESTS ====================

def test_task_completion():
    """Verify that calling mark_complete() changes the task's status."""
    owner = Owner(name="Test Owner", available_time=60)
    pet = Pet(name="Fluffy", species="Cat", age=2, owner=owner)
    task = Task(
        name="Feed cat",
        task_type="feeding",
        duration=10,
        priority=1,
        pet=pet
    )
    
    # Initially not completed
    assert task.completed == False
    
    # Mark complete
    task.mark_complete()
    assert task.completed == True
    
    # Mark incomplete
    task.mark_incomplete()
    assert task.completed == False


def test_task_addition_to_pet():
    """Verify that adding a task to a Pet increases that pet's task count."""
    owner = Owner(name="Test Owner", available_time=120)
    pet = Pet(name="Rex", species="Dog", age=5, owner=owner)
    
    # Pet starts with no tasks
    assert len(pet.tasks) == 0
    
    # Add first task
    task1 = Task(
        name="Walk dog",
        task_type="walk",
        duration=30,
        priority=2,
        pet=pet
    )
    
    assert len(pet.tasks) == 1
    assert task1 in pet.tasks
    
    # Add second task
    task2 = Task(
        name="Feed dog",
        task_type="feeding",
        duration=15,
        priority=1,
        pet=pet
    )
    
    assert len(pet.tasks) == 2
    assert task2 in pet.tasks


def test_scheduler_priority_sorting():
    """Verify that scheduler sorts tasks by priority correctly."""
    owner = Owner(name="Test Owner", available_time=200)
    pet = Pet(name="Buddy", species="Dog", age=3, owner=owner)
    
    # Create tasks with different priorities (intentionally out of order)
    task_low = Task(name="Grooming", task_type="grooming", duration=20, priority=4, pet=pet)
    task_high = Task(name="Medication", task_type="medication", duration=5, priority=1, pet=pet)
    task_medium = Task(name="Walk", task_type="walk", duration=30, priority=3, pet=pet)
    
    scheduler = Scheduler(owner=owner)
    scheduler.generate_daily_plan()
    
    # Tasks should be ordered by priority
    assert scheduler.daily_plan[0].priority == 1  # Highest priority first
    assert scheduler.daily_plan[1].priority == 3
    assert scheduler.daily_plan[2].priority == 4  # Lowest priority last


def test_scheduler_respects_time_constraint():
    """Verify that scheduler doesn't exceed available time."""
    owner = Owner(name="Busy Owner", available_time=60)
    pet = Pet(name="Spot", species="Dog", age=4, owner=owner)
    
    # Create tasks that total more than 60 minutes
    task1 = Task(name="Task 1", task_type="feeding", duration=30, priority=1, pet=pet)
    task2 = Task(name="Task 2", task_type="walk", duration=40, priority=2, pet=pet)
    task3 = Task(name="Task 3", task_type="play", duration=20, priority=3, pet=pet)
    
    scheduler = Scheduler(owner=owner)
    scheduler.generate_daily_plan()
    
    # Total scheduled time should not exceed available time
    total_time = scheduler.calculate_total_time()
    assert total_time <= owner.available_time
    
    # Some tasks should be in conflicts
    assert len(scheduler.conflicts) > 0
    assert len(scheduler.daily_plan) < 3  # Not all tasks fit


def test_task_priority_validation():
    """Verify that Task validates priority is between 1 and 5."""
    owner = Owner(name="Test Owner", available_time=60)
    pet = Pet(name="Cat", species="Cat", age=2, owner=owner)
    
    # Test invalid priority (too high)
    with pytest.raises(ValueError, match="Priority must be between 1"):
        Task(name="Invalid", task_type="feeding", duration=10, priority=6, pet=pet)
    
    # Test invalid priority (too low)
    with pytest.raises(ValueError, match="Priority must be between 1"):
        Task(name="Invalid", task_type="feeding", duration=10, priority=0, pet=pet)
    
    # Test valid priorities work
    for priority in range(1, 6):
        task = Task(name=f"Task {priority}", task_type="feeding", duration=10, priority=priority, pet=pet)
        assert task.priority == priority


def test_owner_gets_all_tasks_from_multiple_pets():
    """Verify that owner can retrieve all tasks from all their pets."""
    owner = Owner(name="Multi-Pet Owner", available_time=200)
    dog = Pet(name="Rex", species="Dog", age=5, owner=owner)
    cat = Pet(name="Whiskers", species="Cat", age=3, owner=owner)
    
    # Add tasks to different pets
    task1 = Task(name="Walk dog", task_type="walk", duration=30, priority=2, pet=dog)
    task2 = Task(name="Feed dog", task_type="feeding", duration=15, priority=1, pet=dog)
    task3 = Task(name="Feed cat", task_type="feeding", duration=10, priority=1, pet=cat)
    
    all_tasks = owner.get_all_tasks()
    
    assert len(all_tasks) == 3
    assert task1 in all_tasks
    assert task2 in all_tasks
    assert task3 in all_tasks


# ==================== SORTING TESTS ====================

def test_sort_by_duration():
    """Verify tasks are sorted by duration (shortest first)."""
    owner = Owner(name="Owner", available_time=200)
    pet = Pet(name="Pet", species="Dog", age=5, owner=owner)
    
    # Create tasks with different durations
    Task(name="Long task", task_type="walk", duration=45, priority=2, pet=pet)
    Task(name="Short task", task_type="medication", duration=5, priority=1, pet=pet)
    Task(name="Medium task", task_type="feeding", duration=20, priority=3, pet=pet)
    
    scheduler = Scheduler(owner=owner)
    scheduler.load_tasks_from_owner()
    sorted_tasks = scheduler.sort_by_duration()
    
    # Check chronological order by duration
    assert sorted_tasks[0].duration == 5
    assert sorted_tasks[1].duration == 20
    assert sorted_tasks[2].duration == 45


def test_sort_by_priority_then_duration():
    """Verify multi-criteria sorting (priority first, then duration)."""
    owner = Owner(name="Owner", available_time=200)
    pet = Pet(name="Pet", species="Dog", age=5, owner=owner)
    
    # Create tasks with same priority but different durations
    task1 = Task(name="P1 Long", task_type="walk", duration=30, priority=1, pet=pet)
    task2 = Task(name="P1 Short", task_type="medication", duration=5, priority=1, pet=pet)
    task3 = Task(name="P2 Medium", task_type="feeding", duration=20, priority=2, pet=pet)
    
    scheduler = Scheduler(owner=owner)
    scheduler.load_tasks_from_owner()
    sorted_tasks = scheduler.sort_by_priority_then_duration()
    
    # P1 tasks should come first, and within P1, shorter task first
    assert sorted_tasks[0].name == "P1 Short"  # Priority 1, 5 min
    assert sorted_tasks[1].name == "P1 Long"   # Priority 1, 30 min
    assert sorted_tasks[2].name == "P2 Medium" # Priority 2, 20 min


def test_sort_by_pet_name():
    """Verify tasks are sorted alphabetically by pet name."""
    owner = Owner(name="Owner", available_time=200)
    charlie = Pet(name="Charlie", species="Dog", age=5, owner=owner)
    bella = Pet(name="Bella", species="Cat", age=3, owner=owner)
    ace = Pet(name="Ace", species="Bird", age=1, owner=owner)
    
    Task(name="Task for Charlie", task_type="walk", duration=30, priority=2, pet=charlie)
    Task(name="Task for Bella", task_type="feeding", duration=15, priority=1, pet=bella)
    Task(name="Task for Ace", task_type="cleaning", duration=10, priority=3, pet=ace)
    
    scheduler = Scheduler(owner=owner)
    scheduler.load_tasks_from_owner()
    sorted_tasks = scheduler.sort_by_pet_name()
    
    # Should be alphabetical: Ace, Bella, Charlie
    assert sorted_tasks[0].pet.name == "Ace"
    assert sorted_tasks[1].pet.name == "Bella"
    assert sorted_tasks[2].pet.name == "Charlie"


# ==================== FILTERING TESTS ====================

def test_filter_by_pet():
    """Verify filtering tasks by specific pet."""
    owner = Owner(name="Owner", available_time=200)
    dog = Pet(name="Max", species="Dog", age=5, owner=owner)
    cat = Pet(name="Whiskers", species="Cat", age=3, owner=owner)
    
    Task(name="Walk Max", task_type="walk", duration=30, priority=2, pet=dog)
    Task(name="Feed Max", task_type="feeding", duration=15, priority=1, pet=dog)
    Task(name="Feed Whiskers", task_type="feeding", duration=10, priority=1, pet=cat)
    
    scheduler = Scheduler(owner=owner)
    scheduler.load_tasks_from_owner()
    
    max_tasks = scheduler.filter_by_pet("Max")
    
    assert len(max_tasks) == 2
    assert all(task.pet.name == "Max" for task in max_tasks)


def test_filter_by_completion():
    """Verify filtering tasks by completion status."""
    owner = Owner(name="Owner", available_time=200)
    pet = Pet(name="Pet", species="Dog", age=5, owner=owner)
    
    task1 = Task(name="Task 1", task_type="walk", duration=30, priority=2, pet=pet)
    task2 = Task(name="Task 2", task_type="feeding", duration=15, priority=1, pet=pet)
    task3 = Task(name="Task 3", task_type="grooming", duration=20, priority=3, pet=pet)
    
    # Mark some complete
    task1.mark_complete()
    
    scheduler = Scheduler(owner=owner)
    scheduler.load_tasks_from_owner()
    
    incomplete = scheduler.filter_by_completion(completed=False)
    completed = scheduler.filter_by_completion(completed=True)
    
    assert len(incomplete) == 2
    assert len(completed) == 1
    assert task1 in completed
    assert task2 in incomplete
    assert task3 in incomplete


def test_filter_by_priority():
    """Verify filtering tasks by priority range."""
    owner = Owner(name="Owner", available_time=200)
    pet = Pet(name="Pet", species="Dog", age=5, owner=owner)
    
    Task(name="High priority", task_type="medication", duration=5, priority=1, pet=pet)
    Task(name="Medium priority", task_type="walk", duration=30, priority=3, pet=pet)
    Task(name="Low priority", task_type="grooming", duration=20, priority=5, pet=pet)
    
    scheduler = Scheduler(owner=owner)
    scheduler.load_tasks_from_owner()
    
    high_priority = scheduler.filter_by_priority(min_priority=1, max_priority=2)
    
    assert len(high_priority) == 1
    assert high_priority[0].priority == 1


def test_get_high_priority_tasks():
    """Verify getting only high-priority tasks."""
    owner = Owner(name="Owner", available_time=200)
    pet = Pet(name="Pet", species="Dog", age=5, owner=owner)
    
    Task(name="Critical", task_type="medication", duration=5, priority=1, pet=pet)
    Task(name="Important", task_type="feeding", duration=15, priority=2, pet=pet)
    Task(name="Normal", task_type="walk", duration=30, priority=3, pet=pet)
    
    scheduler = Scheduler(owner=owner)
    scheduler.load_tasks_from_owner()
    
    high_priority = scheduler.get_high_priority_tasks()
    
    assert len(high_priority) == 2
    assert all(task.is_high_priority() for task in high_priority)


# ==================== CONFLICT DETECTION TESTS ====================

def test_conflict_detection_exact_same_time():
    """Verify that scheduler flags duplicate times (exact overlap)."""
    owner = Owner(name="Owner", available_time=200)
    dog = Pet(name="Max", species="Dog", age=5, owner=owner)
    cat = Pet(name="Whiskers", species="Cat", age=3, owner=owner)
    
    # Create tasks at EXACT same time
    task1 = Task(name="Walk Max", task_type="walk", duration=30, priority=2, pet=dog, scheduled_time=540)
    task2 = Task(name="Walk Whiskers", task_type="walk", duration=30, priority=2, pet=cat, scheduled_time=540)
    
    scheduler = Scheduler(owner=owner)
    scheduler.load_tasks_from_owner()
    scheduler.generate_daily_plan()
    
    conflicts = scheduler.detect_time_conflicts()
    
    assert len(conflicts) > 0
    assert any(task1 in (c[0], c[1]) and task2 in (c[0], c[1]) for c in conflicts)


def test_conflict_detection_overlap():
    """Verify detection of partially overlapping tasks."""
    owner = Owner(name="Owner", available_time=200)
    pet = Pet(name="Max", species="Dog", age=5, owner=owner)
    
    # Task 1: 9:00-9:30 (540-570)
    # Task 2: 9:15-9:45 (555-585)
    # Overlap: 9:15-9:30
    task1 = Task(name="Task 1", task_type="walk", duration=30, priority=2, pet=pet, scheduled_time=540)
    task2 = Task(name="Task 2", task_type="grooming", duration=30, priority=3, pet=pet, scheduled_time=555)
    
    scheduler = Scheduler(owner=owner)
    scheduler.load_tasks_from_owner()
    scheduler.generate_daily_plan()
    
    conflicts = scheduler.detect_time_conflicts()
    
    assert len(conflicts) > 0


def test_no_conflict_sequential_tasks():
    """Verify that back-to-back tasks don't trigger false conflicts."""
    owner = Owner(name="Owner", available_time=200)
    pet = Pet(name="Max", species="Dog", age=5, owner=owner)
    
    # Task 1: 9:00-9:30 (540-570)
    # Task 2: 9:30-10:00 (570-600)
    # No overlap - task2 starts exactly when task1 ends
    task1 = Task(name="Task 1", task_type="walk", duration=30, priority=2, pet=pet, scheduled_time=540)
    task2 = Task(name="Task 2", task_type="feeding", duration=30, priority=1, pet=pet, scheduled_time=570)
    
    scheduler = Scheduler(owner=owner)
    scheduler.load_tasks_from_owner()
    scheduler.generate_daily_plan()
    
    conflicts = scheduler.detect_time_conflicts()
    
    # Should be no conflicts
    assert len(conflicts) == 0


def test_pet_conflict_detection():
    """Verify detection of same pet doing multiple tasks simultaneously."""
    owner = Owner(name="Owner", available_time=200)
    pet = Pet(name="Max", species="Dog", age=5, owner=owner)
    
    # Same pet, overlapping times
    task1 = Task(name="Walk", task_type="walk", duration=45, priority=2, pet=pet, scheduled_time=540)
    task2 = Task(name="Medication", task_type="medication", duration=10, priority=1, pet=pet, scheduled_time=560)
    
    scheduler = Scheduler(owner=owner)
    scheduler.load_tasks_from_owner()
    scheduler.generate_daily_plan()
    
    pet_conflicts = scheduler.detect_pet_conflicts()
    
    assert len(pet_conflicts) > 0


def test_auto_time_assignment_no_conflicts():
    """Verify automatic time assignment creates conflict-free schedule."""
    owner = Owner(name="Owner", available_time=200)
    pet = Pet(name="Max", species="Dog", age=5, owner=owner)
    
    Task(name="Task 1", task_type="medication", duration=5, priority=1, pet=pet)
    Task(name="Task 2", task_type="feeding", duration=15, priority=2, pet=pet)
    Task(name="Task 3", task_type="walk", duration=30, priority=3, pet=pet)
    
    scheduler = Scheduler(owner=owner)
    scheduler.load_tasks_from_owner()
    scheduler.generate_daily_plan()
    scheduler.assign_time_slots(start_time=480)  # Start at 8:00 AM
    
    conflicts = scheduler.detect_all_conflicts()
    
    assert len(conflicts['time_conflicts']) == 0
    assert len(conflicts['pet_conflicts']) == 0


# ==================== EDGE CASE TESTS ====================

def test_empty_pet_no_tasks():
    """Verify pet with no tasks doesn't cause errors."""
    owner = Owner(name="Owner", available_time=120)
    pet = Pet(name="Max", species="Dog", age=5, owner=owner)
    
    # Pet has no tasks
    assert len(pet.tasks) == 0
    
    scheduler = Scheduler(owner=owner)
    scheduler.load_tasks_from_owner()
    scheduler.generate_daily_plan()
    
    # Should work without crashing
    assert len(scheduler.daily_plan) == 0
    assert len(scheduler.conflicts) == 0


def test_zero_available_time():
    """Verify all tasks go to conflicts when no time available."""
    owner = Owner(name="Busy Owner", available_time=0)
    pet = Pet(name="Max", species="Dog", age=5, owner=owner)
    
    Task(name="Task 1", task_type="feeding", duration=15, priority=1, pet=pet)
    Task(name="Task 2", task_type="walk", duration=30, priority=2, pet=pet)
    
    scheduler = Scheduler(owner=owner)
    scheduler.generate_daily_plan()
    
    assert len(scheduler.daily_plan) == 0
    assert len(scheduler.conflicts) == 2


def test_tasks_exactly_fill_time():
    """Verify perfect fit scenario (100% efficiency)."""
    owner = Owner(name="Owner", available_time=60)
    pet = Pet(name="Max", species="Dog", age=5, owner=owner)
    
    Task(name="Task 1", task_type="feeding", duration=20, priority=1, pet=pet)
    Task(name="Task 2", task_type="walk", duration=40, priority=2, pet=pet)
    
    scheduler = Scheduler(owner=owner)
    scheduler.generate_daily_plan()
    
    assert scheduler.calculate_total_time() == 60
    assert len(scheduler.conflicts) == 0
    assert len(scheduler.daily_plan) == 2


def test_filter_returns_empty_gracefully():
    """Verify filtering with no matches returns empty list (not error)."""
    owner = Owner(name="Owner", available_time=120)
    pet = Pet(name="Max", species="Dog", age=5, owner=owner)
    
    Task(name="Task", task_type="feeding", duration=15, priority=1, pet=pet)
    
    scheduler = Scheduler(owner=owner)
    scheduler.load_tasks_from_owner()
    
    # Filter by non-existent pet
    result = scheduler.filter_by_pet("Nonexistent")
    
    assert result == []
    assert isinstance(result, list)


def test_all_same_priority():
    """Verify sorting behavior when all tasks have same priority."""
    owner = Owner(name="Owner", available_time=200)
    pet = Pet(name="Pet", species="Dog", age=5, owner=owner)
    
    task1 = Task(name="Task 1", task_type="feeding", duration=15, priority=3, pet=pet)
    task2 = Task(name="Task 2", task_type="walk", duration=30, priority=3, pet=pet)
    task3 = Task(name="Task 3", task_type="grooming", duration=20, priority=3, pet=pet)
    
    scheduler = Scheduler(owner=owner)
    scheduler.load_tasks_from_owner()
    sorted_tasks = scheduler.sort_by_priority()
    
    # All should have priority 3
    assert all(task.priority == 3 for task in sorted_tasks)
    # Order should be stable (original order maintained)
    assert len(sorted_tasks) == 3


def test_single_long_task_doesnt_fit():
    """Verify single task too long goes to conflicts."""
    owner = Owner(name="Owner", available_time=60)
    pet = Pet(name="Max", species="Dog", age=5, owner=owner)
    
    task = Task(name="Very long task", task_type="grooming", duration=90, priority=1, pet=pet)
    
    scheduler = Scheduler(owner=owner)
    scheduler.generate_daily_plan()
    
    assert len(scheduler.daily_plan) == 0
    assert len(scheduler.conflicts) == 1
    assert scheduler.conflicts[0] == task


def test_invalid_duration():
    """Verify negative or zero duration raises error."""
    owner = Owner(name="Owner", available_time=120)
    pet = Pet(name="Max", species="Dog", age=5, owner=owner)
    
    with pytest.raises(ValueError, match="Duration must be positive"):
        Task(name="Invalid", task_type="feeding", duration=-10, priority=1, pet=pet)
    
    with pytest.raises(ValueError, match="Duration must be positive"):
        Task(name="Invalid", task_type="feeding", duration=0, priority=1, pet=pet)


# ==================== ALGORITHM PERFORMANCE TESTS ====================

def test_many_tasks_performance():
    """Verify scheduler handles many tasks efficiently."""
    import time
    
    owner = Owner(name="Owner", available_time=500)
    pet = Pet(name="Pet", species="Dog", age=5, owner=owner)
    
    # Create 100 tasks
    for i in range(100):
        Task(
            name=f"Task {i}",
            task_type="walk",
            duration=10,
            priority=(i % 5) + 1,
            pet=pet
        )
    
    scheduler = Scheduler(owner=owner)
    
    start_time = time.time()
    scheduler.generate_daily_plan()
    end_time = time.time()
    
    # Should complete in less than 1 second
    assert end_time - start_time < 1.0
    assert len(scheduler.daily_plan) > 0