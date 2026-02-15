"""
PawPal+ Core System - Skeleton
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
    
    def get_available_time(self) -> int:
        """Return available time in minutes."""
        pass
    
    def add_preference(self, key: str, value) -> None:
        """Add or update a preference."""
        pass


@dataclass
class Pet:
    """Represents a pet that needs care."""
    name: str
    species: str
    age: int
    owner: Owner
    special_needs: List[str] = field(default_factory=list)
    
    def add_special_need(self, need: str) -> None:
        """Add a special need or note."""
        pass
    
    def get_info(self) -> str:
        """Return formatted pet information."""
        pass


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
    
    def mark_complete(self) -> None:
        """Mark task as completed."""
        pass
    
    def mark_incomplete(self) -> None:
        """Reset completion status."""
        pass
    
    def is_high_priority(self) -> bool:
        """Return True if priority is high (1 or 2)."""
        pass
    
    def __lt__(self, other) -> bool:
        """Enable sorting by priority (lower number = higher priority)."""
        pass


class Scheduler:
    """Manages and organizes tasks into a daily schedule."""
    
    def __init__(self, owner: Owner):
        self.owner = owner
        self.tasks: List[Task] = []
        self.daily_plan: List[Task] = []
        self.conflicts: List[Task] = []
    
    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        pass
    
    def remove_task(self, task: Task) -> None:
        """Remove a task from the scheduler."""
        pass
    
    def generate_daily_plan(self) -> List[Task]:
        """
        Generate optimized daily schedule based on priority and time constraints.
        Uses a greedy algorithm: highest priority tasks first until time runs out.
        """
        pass
    
    def check_conflicts(self) -> List[Task]:
        """Return list of tasks that couldn't fit in the schedule."""
        pass
    
    def get_plan_summary(self) -> str:
        """Return formatted daily plan with explanations."""
        pass
    
    def calculate_total_time(self) -> int:
        """Calculate total time needed for all tasks in daily plan."""
        pass
    
    def sort_by_priority(self) -> List[Task]:
        """Return tasks sorted by priority (highest first)."""
        pass