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
    scheduled_time: Optional[int] = None  # Start time in minutes from midnight (e.g., 540 = 9:00 AM)
    
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
    
    # ==================== SORTING METHODS ====================
    
    def sort_by_priority(self) -> List[Task]:
        """Return tasks sorted by priority (highest first)."""
        return sorted(self.tasks, key=lambda t: t.priority)
    
    def sort_by_duration(self) -> List[Task]:
        """Return tasks sorted by duration (shortest first)."""
        return sorted(self.tasks, key=lambda t: t.duration)
    
    def sort_by_duration_desc(self) -> List[Task]:
        """Return tasks sorted by duration (longest first)."""
        return sorted(self.tasks, key=lambda t: t.duration, reverse=True)
    
    def sort_by_priority_then_duration(self) -> List[Task]:
        """
        Return tasks sorted by priority first, then by duration.
        For same priority, shorter tasks come first.
        """
        return sorted(self.tasks, key=lambda t: (t.priority, t.duration))
    
    def sort_by_pet_name(self) -> List[Task]:
        """Return tasks sorted alphabetically by pet name."""
        return sorted(self.tasks, key=lambda t: t.pet.name)
    
    # ==================== FILTERING METHODS ====================
    
    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return only tasks for a specific pet."""
        return [task for task in self.tasks if task.pet.name == pet_name]
    
    def filter_by_completion(self, completed: bool = False) -> List[Task]:
        """
        Return tasks filtered by completion status.
        completed=True returns completed tasks, False returns incomplete tasks.
        """
        return [task for task in self.tasks if task.completed == completed]
    
    def filter_by_priority(self, min_priority: int = 1, max_priority: int = 5) -> List[Task]:
        """
        Return tasks within a priority range.
        Example: filter_by_priority(1, 2) returns only high-priority tasks.
        """
        return [task for task in self.tasks if min_priority <= task.priority <= max_priority]
    
    def filter_by_task_type(self, task_type: str) -> List[Task]:
        """Return only tasks of a specific type (feeding, walk, medication, etc.)."""
        return [task for task in self.tasks if task.task_type == task_type]
    
    def get_high_priority_tasks(self) -> List[Task]:
        """Return only high-priority tasks (priority 1-2)."""
        return [task for task in self.tasks if task.is_high_priority()]
    
    # ==================== SCHEDULING ALGORITHM ====================
    
    def generate_daily_plan(self, sort_method: str = "priority") -> List[Task]:
        """
        Generate optimized daily schedule based on priority and time constraints.
        
        Args:
            sort_method: How to sort tasks before scheduling
                - "priority" (default): highest priority first
                - "duration": shortest tasks first
                - "priority_duration": priority first, then duration
        """
        # Reset plan and conflicts
        self.daily_plan = []
        self.conflicts = []
        
        # Load tasks from owner if not already loaded
        if not self.tasks:
            self.load_tasks_from_owner()
        
        # Sort tasks based on method
        if sort_method == "duration":
            sorted_tasks = self.sort_by_duration()
        elif sort_method == "priority_duration":
            sorted_tasks = self.sort_by_priority_then_duration()
        else:  # default: "priority"
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
    
    # ==================== CONFLICT DETECTION ====================
    
    def detect_time_conflicts(self) -> List[tuple]:
        """
        Detect tasks that overlap in time.
        Returns list of tuples: (task1, task2, conflict_reason)
        """
        conflicts = []
        
        # Only check tasks with scheduled times
        scheduled_tasks = [t for t in self.daily_plan if t.scheduled_time is not None]
        
        for i, task1 in enumerate(scheduled_tasks):
            for task2 in scheduled_tasks[i+1:]:
                # Calculate end times
                task1_end = task1.scheduled_time + task1.duration
                task2_end = task2.scheduled_time + task2.duration
                
                # Check for overlap: task1 starts before task2 ends AND task2 starts before task1 ends
                if (task1.scheduled_time < task2_end and task2.scheduled_time < task1_end):
                    reason = f"Time overlap: both scheduled between {self._format_time(max(task1.scheduled_time, task2.scheduled_time))} and {self._format_time(min(task1_end, task2_end))}"
                    conflicts.append((task1, task2, reason))
        
        return conflicts
    
    def detect_pet_conflicts(self) -> List[tuple]:
        """
        Detect if the same pet has multiple tasks at the same time.
        Returns list of tuples: (task1, task2, conflict_reason)
        """
        conflicts = []
        scheduled_tasks = [t for t in self.daily_plan if t.scheduled_time is not None]
        
        for i, task1 in enumerate(scheduled_tasks):
            for task2 in scheduled_tasks[i+1:]:
                # Same pet can't do two things at once
                if task1.pet.name == task2.pet.name:
                    task1_end = task1.scheduled_time + task1.duration
                    task2_end = task2.scheduled_time + task2.duration
                    
                    if (task1.scheduled_time < task2_end and task2.scheduled_time < task1_end):
                        reason = f"{task1.pet.name} cannot do two tasks simultaneously"
                        conflicts.append((task1, task2, reason))
        
        return conflicts
    
    def detect_all_conflicts(self) -> Dict[str, List[tuple]]:
        """
        Run all conflict detection methods and return organized results.
        Returns dict with conflict types as keys.
        """
        return {
            'time_conflicts': self.detect_time_conflicts(),
            'pet_conflicts': self.detect_pet_conflicts()
        }
    
    def get_conflict_warnings(self) -> List[str]:
        """
        Generate user-friendly warning messages for all conflicts.
        Returns list of warning strings.
        """
        warnings = []
        all_conflicts = self.detect_all_conflicts()
        
        # Time conflicts
        for task1, task2, reason in all_conflicts['time_conflicts']:
            warnings.append(
                f"⚠️  TIME CONFLICT: '{task1.name}' and '{task2.name}' overlap\n"
                f"   {reason}"
            )
        
        # Pet conflicts
        for task1, task2, reason in all_conflicts['pet_conflicts']:
            warnings.append(
                f"⚠️  PET CONFLICT: {reason}\n"
                f"   Tasks: '{task1.name}' and '{task2.name}'"
            )
        
        return warnings
    
    def _format_time(self, minutes: int) -> str:
        """Convert minutes from midnight to HH:MM format."""
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"
    
    def assign_time_slots(self, start_time: int = 480) -> None:
        """
        Automatically assign time slots to tasks in daily_plan.
        start_time: minutes from midnight (default 480 = 8:00 AM)
        """
        current_time = start_time
        
        for task in self.daily_plan:
            task.scheduled_time = current_time
            current_time += task.duration
    
    def print_conflict_report(self) -> None:
        """Print a formatted report of all detected conflicts."""
        warnings = self.get_conflict_warnings()
        
        if not warnings:
            print("✅ No conflicts detected! All tasks are compatible.\n")
        else:
            print(f"\n{'='*70}")
            print(f"⚠️  CONFLICT DETECTION REPORT")
            print(f"{'='*70}")
            print(f"Found {len(warnings)} conflict(s):\n")
            for i, warning in enumerate(warnings, 1):
                print(f"{i}. {warning}\n")
            print(f"{'='*70}\n")