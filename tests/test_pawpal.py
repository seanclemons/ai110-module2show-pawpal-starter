"""
PawPal+ Test Suite
Tests for core functionality of the pet care scheduling system.
"""

import pytest
from pawpal_system import Owner, Pet, Task, Scheduler


# Test 1: Task Completion
def test_task_completion():
    """Verify that calling mark_complete() changes the task's status."""
    # Arrange: Create test data
    owner = Owner(name="Test Owner", available_time=60)
    pet = Pet(name="Fluffy", species="Cat", age=2, owner=owner)
    task = Task(
        name="Feed cat",
        task_type="feeding",
        duration=10,
        priority=1,
        pet=pet
    )
    
    # Act: Mark task as complete
    assert task.completed == False  # Initially not completed
    task.mark_complete()
    
    # Assert: Check status changed
    assert task.completed == True
    
    # Also test mark_incomplete
    task.mark_incomplete()
    assert task.completed == False


# Test 2: Task Addition
def test_task_addition_to_pet():
    """Verify that adding a task to a Pet increases that pet's task count."""
    # Arrange: Create owner and pet
    owner = Owner(name="Test Owner", available_time=120)
    pet = Pet(name="Rex", species="Dog", age=5, owner=owner)
    
    # Act: Check initial task count
    initial_count = len(pet.tasks)
    assert initial_count == 0  # Pet starts with no tasks
    
    # Add first task
    task1 = Task(
        name="Walk dog",
        task_type="walk",
        duration=30,
        priority=2,
        pet=pet
    )
    
    # Assert: Task count increased
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
    
    # Assert: Task count increased again
    assert len(pet.tasks) == 2
    assert task2 in pet.tasks


# Bonus Test 3: Scheduler Priority Sorting
def test_scheduler_priority_sorting():
    """Verify that scheduler sorts tasks by priority correctly."""
    # Arrange
    owner = Owner(name="Test Owner", available_time=200)
    pet = Pet(name="Buddy", species="Dog", age=3, owner=owner)
    
    # Create tasks with different priorities (intentionally out of order)
    task_low = Task(name="Grooming", task_type="grooming", duration=20, priority=4, pet=pet)
    task_high = Task(name="Medication", task_type="medication", duration=5, priority=1, pet=pet)
    task_medium = Task(name="Walk", task_type="walk", duration=30, priority=3, pet=pet)
    
    scheduler = Scheduler(owner=owner)
    scheduler.generate_daily_plan()
    
    # Assert: Tasks should be ordered by priority
    assert scheduler.daily_plan[0].priority == 1  # Highest priority first
    assert scheduler.daily_plan[1].priority == 3
    assert scheduler.daily_plan[2].priority == 4  # Lowest priority last


# Bonus Test 4: Scheduler Time Constraint
def test_scheduler_respects_time_constraint():
    """Verify that scheduler doesn't exceed available time."""
    # Arrange: Owner with limited time
    owner = Owner(name="Busy Owner", available_time=60)
    pet = Pet(name="Spot", species="Dog", age=4, owner=owner)
    
    # Create tasks that total more than 60 minutes
    task1 = Task(name="Task 1", task_type="feeding", duration=30, priority=1, pet=pet)
    task2 = Task(name="Task 2", task_type="walk", duration=40, priority=2, pet=pet)
    task3 = Task(name="Task 3", task_type="play", duration=20, priority=3, pet=pet)
    
    scheduler = Scheduler(owner=owner)
    scheduler.generate_daily_plan()
    
    # Assert: Total scheduled time should not exceed available time
    total_time = scheduler.calculate_total_time()
    assert total_time <= owner.available_time
    
    # Assert: Some tasks should be in conflicts
    assert len(scheduler.conflicts) > 0
    assert len(scheduler.daily_plan) < 3  # Not all tasks fit


# Bonus Test 5: Task Priority Validation
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


# Bonus Test 6: Owner Gets All Tasks from Multiple Pets
def test_owner_gets_all_tasks_from_multiple_pets():
    """Verify that owner can retrieve all tasks from all their pets."""
    # Arrange
    owner = Owner(name="Multi-Pet Owner", available_time=200)
    dog = Pet(name="Rex", species="Dog", age=5, owner=owner)
    cat = Pet(name="Whiskers", species="Cat", age=3, owner=owner)
    
    # Add tasks to different pets
    task1 = Task(name="Walk dog", task_type="walk", duration=30, priority=2, pet=dog)
    task2 = Task(name="Feed dog", task_type="feeding", duration=15, priority=1, pet=dog)
    task3 = Task(name="Feed cat", task_type="feeding", duration=10, priority=1, pet=cat)
    
    # Act
    all_tasks = owner.get_all_tasks()
    
    # Assert
    assert len(all_tasks) == 3
    assert task1 in all_tasks
    assert task2 in all_tasks
    assert task3 in all_tasks