"""
PawPal+ Demo Script - Testing Conflict Detection
Demonstrates conflict detection with overlapping tasks.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    print("\n🐾 PawPal+ Conflict Detection Demo! 🐾\n")
    
    # Create Owner and Pets
    print("Setting up owner and pets...")
    owner = Owner(name="Alex", available_time=300)
    
    max_dog = Pet(name="Max", species="Dog", age=5, owner=owner)
    bella_dog = Pet(name="Bella", species="Dog", age=3, owner=owner)
    
    print(f"✓ Created owner: {owner.name}")
    print(f"✓ Registered pets: {', '.join(p.name for p in owner.pets)}\n")
    
    # Create Scheduler
    scheduler = Scheduler(owner=owner)
    
    print("="*70)
    print("TEST 1: NO CONFLICTS (Sequential Tasks)")
    print("="*70)
    
    # Create tasks without conflicts
    task1 = Task(name="Feed Max", task_type="feeding", duration=15, priority=1, pet=max_dog)
    task2 = Task(name="Walk Max", task_type="walk", duration=30, priority=2, pet=max_dog)
    task3 = Task(name="Feed Bella", task_type="feeding", duration=15, priority=1, pet=bella_dog)
    
    scheduler.load_tasks_from_owner()
    scheduler.generate_daily_plan(sort_method="priority")
    
    # Assign time slots starting at 8:00 AM (480 minutes from midnight)
    scheduler.assign_time_slots(start_time=480)
    
    print("\nScheduled tasks:")
    for task in scheduler.daily_plan:
        end_time = task.scheduled_time + task.duration
        print(f"  {scheduler._format_time(task.scheduled_time)}-{scheduler._format_time(end_time)}: {task.name} ({task.pet.name})")
    
    # Check for conflicts
    scheduler.print_conflict_report()
    
    # ============ TEST 2: TIME CONFLICTS ============
    print("="*70)
    print("TEST 2: TIME CONFLICTS (Same Start Time)")
    print("="*70)
    
    # Clear previous tasks
    owner.pets[0].tasks.clear()
    owner.pets[1].tasks.clear()
    
    # Create tasks with SAME start time (9:00 AM = 540 minutes)
    task1 = Task(name="Walk Max", task_type="walk", duration=30, priority=2, pet=max_dog, scheduled_time=540)
    task2 = Task(name="Walk Bella", task_type="walk", duration=30, priority=2, pet=bella_dog, scheduled_time=540)
    task3 = Task(name="Feed Max", task_type="feeding", duration=15, priority=1, pet=max_dog, scheduled_time=480)
    
    scheduler2 = Scheduler(owner=owner)
    scheduler2.load_tasks_from_owner()
    scheduler2.generate_daily_plan(sort_method="priority")
    
    print("\nScheduled tasks:")
    for task in scheduler2.daily_plan:
        if task.scheduled_time:
            end_time = task.scheduled_time + task.duration
            print(f"  {scheduler2._format_time(task.scheduled_time)}-{scheduler2._format_time(end_time)}: {task.name} ({task.pet.name})")
    
    # Check for conflicts
    scheduler2.print_conflict_report()
    
    # ============ TEST 3: PET CONFLICTS ============
    print("="*70)
    print("TEST 3: PET CONFLICTS (Same Pet, Overlapping Times)")
    print("="*70)
    
    # Clear previous tasks
    owner.pets[0].tasks.clear()
    owner.pets[1].tasks.clear()
    
    # Create overlapping tasks for the SAME pet
    task1 = Task(name="Walk Max", task_type="walk", duration=45, priority=2, pet=max_dog, scheduled_time=540)
    task2 = Task(name="Give Max medication", task_type="medication", duration=10, priority=1, pet=max_dog, scheduled_time=560)
    task3 = Task(name="Feed Bella", task_type="feeding", duration=15, priority=1, pet=bella_dog, scheduled_time=540)
    
    scheduler3 = Scheduler(owner=owner)
    scheduler3.load_tasks_from_owner()
    scheduler3.generate_daily_plan(sort_method="priority")
    
    print("\nScheduled tasks:")
    for task in scheduler3.daily_plan:
        if task.scheduled_time:
            end_time = task.scheduled_time + task.duration
            print(f"  {scheduler3._format_time(task.scheduled_time)}-{scheduler3._format_time(end_time)}: {task.name} ({task.pet.name})")
    
    # Check for conflicts
    scheduler3.print_conflict_report()
    
    # ============ TEST 4: MULTIPLE CONFLICTS ============
    print("="*70)
    print("TEST 4: MULTIPLE CONFLICTS (Complex Scenario)")
    print("="*70)
    
    # Clear previous tasks
    owner.pets[0].tasks.clear()
    owner.pets[1].tasks.clear()
    
    # Create a mess of overlapping tasks
    task1 = Task(name="Walk Max", task_type="walk", duration=30, priority=2, pet=max_dog, scheduled_time=540)
    task2 = Task(name="Walk Bella", task_type="walk", duration=30, priority=2, pet=bella_dog, scheduled_time=540)
    task3 = Task(name="Groom Max", task_type="grooming", duration=45, priority=3, pet=max_dog, scheduled_time=550)
    task4 = Task(name="Feed Max", task_type="feeding", duration=15, priority=1, pet=max_dog, scheduled_time=560)
    
    scheduler4 = Scheduler(owner=owner)
    scheduler4.load_tasks_from_owner()
    scheduler4.generate_daily_plan(sort_method="priority")
    
    print("\nScheduled tasks:")
    for task in scheduler4.daily_plan:
        if task.scheduled_time:
            end_time = task.scheduled_time + task.duration
            print(f"  {scheduler4._format_time(task.scheduled_time)}-{scheduler4._format_time(end_time)}: {task.name} ({task.pet.name})")
    
    # Check for conflicts
    scheduler4.print_conflict_report()
    
    # ============ TEST 5: AUTO TIME SLOT ASSIGNMENT ============
    print("="*70)
    print("TEST 5: AUTOMATIC TIME SLOT ASSIGNMENT (No Conflicts)")
    print("="*70)
    
    # Clear previous tasks
    owner.pets[0].tasks.clear()
    owner.pets[1].tasks.clear()
    
    # Create tasks WITHOUT scheduled times
    task1 = Task(name="Feed Max", task_type="feeding", duration=15, priority=1, pet=max_dog)
    task2 = Task(name="Walk Max", task_type="walk", duration=30, priority=2, pet=max_dog)
    task3 = Task(name="Give Max medication", task_type="medication", duration=5, priority=1, pet=max_dog)
    task4 = Task(name="Feed Bella", task_type="feeding", duration=15, priority=1, pet=bella_dog)
    task5 = Task(name="Walk Bella", task_type="walk", duration=25, priority=2, pet=bella_dog)
    
    scheduler5 = Scheduler(owner=owner)
    scheduler5.load_tasks_from_owner()
    scheduler5.generate_daily_plan(sort_method="priority_duration")
    
    # Auto-assign sequential time slots starting at 8:00 AM
    print("\nAuto-assigning time slots starting at 8:00 AM...")
    scheduler5.assign_time_slots(start_time=480)
    
    print("\nScheduled tasks:")
    for task in scheduler5.daily_plan:
        if task.scheduled_time:
            end_time = task.scheduled_time + task.duration
            print(f"  {scheduler5._format_time(task.scheduled_time)}-{scheduler5._format_time(end_time)}: {task.name} ({task.pet.name}, {task.duration} min)")
    
    # Check for conflicts (should be none!)
    scheduler5.print_conflict_report()
    
    print("="*70)
    print("🎉 All conflict detection tests completed!")
    print("="*70)


if __name__ == "__main__":
    main()