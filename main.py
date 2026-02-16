"""
PawPal+ Demo Script
Demonstrates the core functionality of the pet care scheduling system.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    print("\n🐾 Welcome to PawPal+ Demo! 🐾\n")
    
    # Step 1: Create an Owner
    print("Creating owner...")
    sarah = Owner(name="Sarah", available_time=180)  # 3 hours per day
    print(f"✓ {sarah.name} created with {sarah.available_time} minutes available per day\n")
    
    # Step 2: Create Pets
    print("Registering pets...")
    max_dog = Pet(
        name="Max",
        species="Dog",
        age=5,
        owner=sarah,
        special_needs=["Arthritis medication", "Slow walks only"]
    )
    
    whiskers = Pet(
        name="Whiskers",
        species="Cat",
        age=3,
        owner=sarah
    )
    
    print(f"✓ {max_dog.get_info()}")
    print(f"✓ {whiskers.get_info()}")
    print(f"✓ Total pets registered: {len(sarah.pets)}\n")
    
    # Step 3: Create Tasks (at least 3 with different durations)
    print("Adding tasks...")
    
    # High priority tasks
    task1 = Task(
        name="Give Max arthritis medication",
        task_type="medication",
        duration=5,
        priority=1,  # Highest priority
        pet=max_dog
    )
    
    task2 = Task(
        name="Feed Max breakfast",
        task_type="feeding",
        duration=15,
        priority=1,
        pet=max_dog
    )
    
    task3 = Task(
        name="Feed Whiskers breakfast",
        task_type="feeding",
        duration=10,
        priority=1,
        pet=whiskers
    )
    
    # Medium priority tasks
    task4 = Task(
        name="Morning walk with Max",
        task_type="walk",
        duration=30,
        priority=2,
        pet=max_dog
    )
    
    task5 = Task(
        name="Play session with Whiskers",
        task_type="enrichment",
        duration=20,
        priority=3,
        pet=whiskers
    )
    
    # Lower priority tasks
    task6 = Task(
        name="Brush Max's coat",
        task_type="grooming",
        duration=25,
        priority=4,
        pet=max_dog
    )
    
    task7 = Task(
        name="Clean Whiskers' litter box",
        task_type="cleaning",
        duration=10,
        priority=3,
        pet=whiskers
    )
    
    task8 = Task(
        name="Evening walk with Max",
        task_type="walk",
        duration=30,
        priority=2,
        pet=max_dog
    )
    
    # Count total tasks
    all_tasks = sarah.get_all_tasks()
    print(f"✓ Added {len(all_tasks)} tasks")
    for task in all_tasks:
        print(f"  - {task.name} ({task.duration} min, priority {task.priority})")
    
    print()
    
    # Step 4: Create Scheduler and Generate Plan
    print("Initializing scheduler and generating daily plan...\n")
    scheduler = Scheduler(owner=sarah)
    scheduler.generate_daily_plan()
    
    # Step 5: Display Today's Schedule
    print(scheduler.get_plan_summary())
    
    # Additional Summary Stats
    print(f"{'='*60}")
    print(f"📊 SCHEDULING SUMMARY")
    print(f"{'='*60}")
    print(f"Total tasks: {len(all_tasks)}")
    print(f"Tasks scheduled: {len(scheduler.daily_plan)}")
    print(f"Tasks in conflict: {len(scheduler.conflicts)}")
    print(f"Time efficiency: {scheduler.calculate_total_time()}/{sarah.get_available_time()} minutes ({scheduler.calculate_total_time()/sarah.get_available_time()*100:.1f}%)")
    print(f"{'='*60}\n")
    
    # Show which pets are involved
    scheduled_pets = set(task.pet.name for task in scheduler.daily_plan)
    print(f"🐾 Pets in today's schedule: {', '.join(scheduled_pets)}")
    print()


if __name__ == "__main__":
    main()