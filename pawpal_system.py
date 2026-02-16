"""
PawPal+ Core System
Main classes for pet care management and scheduling.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Owner:
    """Represents a pet owner with time constraints and preferences."""
    name: str
    available_time: int  # minutes per day
    preferences: Dict = field(default_factory=dict)
    pets: List['Pet'] = field(default_factory=list)
    
    def get_available_time(self) -> int:
        """Return available time in minutes."""
        return self.available_time
    
    def add_preference(self, key: str, value) -> None:
        """Add or update a preference."""
        self.preferences[key] = value
    
    def add_pet(self, pet: 'Pet') -> None:
        """Add a pet to the owner's pet list."""
        if pet not in self.pets:
            self.pets.append(pet)
    
    def get_all_tasks(self) -> List['Task']:
        """Retrieve all tasks from all pets owned by this owner."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


@dataclass
class Pet:
    """Represents a pet that needs care."""
    name: str
    species: str
    age: int
    owner: Owner
    special_needs: List[str] = field(default_factory=list)
    tasks: List['Task'] = field(default_factory=list)
    
    def __post_init__(self):
        """Automatically register this pet with its owner."""
        self.owner.add_pet(self)
    
    def add_special_need(self, need: str) -> None:
        """Add a special need or note."""
        if need not in self.special_needs:
            self.special_needs.append(need)
    
    def get_info(self) -> str:
        """Return formatted pet information."""
        needs = ", ".join(self.special_needs) if self.special_needs else "None"
        return f"{self.name} ({self.species}, {self.age} years old) - Special needs: {needs}"
    
    def add_task(self, task: 'Task') -> None:
        """Add a task to this pet's task list."""
        if task not in self.tasks:
            self.tasks.append(task)


@dataclass
class Task:
    """Represents a care task for a pet."""
    name: str
    task_type: str
    duration: int  # minutes
    priority: int  # 1=highest, 5=lowest
    pet: Pet
    recurrence: str = 'daily'
    completed: bool = False
    
    def __post_init__(self):
        """Automatically register this task with its pet."""
        self.pet.add_task(self)
        # Validate inputs
        if self.duration <= 0:
            raise ValueError("Duration must be positive")
        if not 1 <= self.priority <= 5:
            raise ValueError("Priority must be between 1 (highest) and 5 (lowest)")
    
    def mark_complete(self) -> None:
        """Mark task as completed."""
        self.completed = True
    
    def mark_incomplete(self) -> None:
        """Reset completion status."""
        self.completed = False
    
    def is_high_priority(self) -> bool:
        """Return True if priority is high (1 or 2)."""
        return self.priority <= 2
    
    def __lt__(self, other: 'Task') -> bool:
        """Enable sorting by priority (lower number = higher priority)."""
        return self.priority < other.priority


class Scheduler:
    """Manages and organizes tasks into a daily schedule."""
    
    def __init__(self, owner: Owner):
        self.owner = owner
        self.tasks: List[Task] = []
        self.daily_plan: List[Task] = []
        self.conflicts: List[Task] = []
    
    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        if task not in self.tasks:
            self.tasks.append(task)
    
    def remove_task(self, task: Task) -> None:
        """Remove a task from the scheduler."""
        if task in self.tasks:
            self.tasks.remove(task)
    
    def load_tasks_from_owner(self) -> None:
        """Load all tasks from the owner's pets into the scheduler."""
        self.tasks = self.owner.get_all_tasks()
    
    def generate_daily_plan(self) -> List[Task]:
        """
        Generate optimized daily schedule based on priority and time constraints.
        Uses a greedy algorithm: highest priority tasks first until time runs out.
        """
        # Reset plan and conflicts
        self.daily_plan = []
        self.conflicts = []
        
        # Load tasks from owner if not already loaded
        if not self.tasks:
            self.load_tasks_from_owner()
        
        # Sort tasks by priority (highest first)
        sorted_tasks = self.sort_by_priority()
        
        # Get available time
        available_time = self.owner.get_available_time()
        time_used = 0
        
        # Greedy algorithm: add tasks until time runs out
        for task in sorted_tasks:
            if time_used + task.duration <= available_time:
                self.daily_plan.append(task)
                time_used += task.duration
            else:
                self.conflicts.append(task)
        
        return self.daily_plan
    
    def check_conflicts(self) -> List[Task]:
        """Return list of tasks that couldn't fit in the schedule."""
        return self.conflicts
    
    def get_plan_summary(self) -> str:
        """Return formatted daily plan with explanations."""
        if not self.daily_plan:
            return "No tasks scheduled yet. Run generate_daily_plan() first."
        
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"📅 TODAY'S SCHEDULE FOR {self.owner.name.upper()}")
        lines.append(f"{'='*60}")
        lines.append(f"Available time: {self.owner.get_available_time()} minutes")
        lines.append(f"Scheduled: {self.calculate_total_time()} minutes")
        lines.append(f"{'='*60}\n")
        
        for i, task in enumerate(self.daily_plan, 1):
            # Priority indicator
            if task.is_high_priority():
                priority_label = "🔴 HIGH"
            elif task.priority == 3:
                priority_label = "🟡 MEDIUM"
            else:
                priority_label = "🟢 LOW"
            
            status = "✓" if task.completed else "○"
            lines.append(f"{i}. {status} [{priority_label}] {task.name}")
            lines.append(f"   Pet: {task.pet.name} | Duration: {task.duration} min | Type: {task.task_type}")
            lines.append("")
        
        # Show conflicts if any
        if self.conflicts:
            lines.append(f"\n{'='*60}")
            lines.append(f"⚠️  CONFLICTS - Tasks that couldn't fit:")
            lines.append(f"{'='*60}")
            for task in self.conflicts:
                lines.append(f"- {task.name} ({task.duration} min, priority {task.priority}) for {task.pet.name}")
            lines.append("")
        
        return "\n".join(lines)
    
    def calculate_total_time(self) -> int:
        """Calculate total time needed for all tasks in daily plan."""
        return sum(task.duration for task in self.daily_plan)
    
    def sort_by_priority(self) -> List[Task]:
        """Return tasks sorted by priority (highest first)."""
        return sorted(self.tasks, key=lambda t: t.priority)