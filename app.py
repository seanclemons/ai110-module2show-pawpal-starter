import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+** - your intelligent pet care scheduling assistant!

This app helps you plan daily care tasks for your pets based on available time and task priorities.
"""
)

with st.expander("📖 How It Works", expanded=False):
    st.markdown(
        """
**PawPal+** uses a smart scheduling algorithm to organize your pet care tasks:

1. **Add your information**: Enter your name and available time
2. **Register your pets**: Add one or more pets with their details
3. **Create tasks**: Define care tasks with duration and priority (1=highest, 5=lowest)
4. **Generate schedule**: Click to create an optimized daily plan

The scheduler prioritizes critical tasks (medication, feeding) and fits as many tasks as possible within your available time.
"""
    )

st.divider()

# Initialize session state
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pets" not in st.session_state:
    st.session_state.pets = []
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# Section 1: Owner Setup
st.subheader("👤 Owner Information")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Your name", value="Jordan")
with col2:
    available_time = st.number_input(
        "Available time (minutes/day)", 
        min_value=30, 
        max_value=480, 
        value=180,
        step=15
    )

if st.button("Create/Update Owner Profile"):
    st.session_state.owner = Owner(name=owner_name, available_time=available_time)
    st.session_state.pets = []  # Reset pets when owner changes
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)
    st.success(f"✓ Owner profile created: {owner_name} with {available_time} minutes available")

# Section 2: Pet Management
st.divider()
st.subheader("🐾 Your Pets")

if st.session_state.owner:
    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"])
    with col3:
        age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)
    
    special_needs = st.text_input("Special needs (optional)", placeholder="e.g., Medication, Slow walks")
    
    if st.button("Add Pet"):
        needs_list = [need.strip() for need in special_needs.split(",")] if special_needs else []
        pet = Pet(
            name=pet_name,
            species=species,
            age=age,
            owner=st.session_state.owner,
            special_needs=needs_list
        )
        st.session_state.pets.append(pet)
        st.success(f"✓ Added {pet_name} the {species}")
    
    # Display current pets
    if st.session_state.owner.pets:
        st.markdown("**Current Pets:**")
        for pet in st.session_state.owner.pets:
            with st.container():
                st.markdown(f"- {pet.get_info()}")
    else:
        st.info("No pets added yet. Add one above to get started!")
else:
    st.warning("⚠️ Please create an owner profile first")

# Section 3: Task Management
st.divider()
st.subheader("📋 Care Tasks")

if st.session_state.owner and st.session_state.owner.pets:
    # Select which pet this task is for
    pet_names = [pet.name for pet in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Task for which pet?", pet_names)
    selected_pet = next(pet for pet in st.session_state.owner.pets if pet.name == selected_pet_name)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        task_name = st.text_input("Task name", value="Morning walk")
    with col2:
        task_type = st.selectbox(
            "Task type", 
            ["feeding", "walk", "medication", "grooming", "enrichment", "cleaning"]
        )
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=5, max_value=240, value=20, step=5)
    
    col4, col5 = st.columns(2)
    with col4:
        priority = st.slider("Priority", min_value=1, max_value=5, value=2, help="1 = Highest, 5 = Lowest")
    with col5:
        recurrence = st.selectbox("Recurrence", ["daily", "weekly", "once"])
    
    if st.button("Add Task"):
        task = Task(
            name=task_name,
            task_type=task_type,
            duration=duration,
            priority=priority,
            pet=selected_pet,
            recurrence=recurrence
        )
        st.success(f"✓ Added task: {task_name} (Priority {priority}, {duration} min)")
    
    # Display all tasks
    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        st.markdown("**All Tasks:**")
        for task in all_tasks:
            priority_emoji = "🔴" if task.priority <= 2 else "🟡" if task.priority == 3 else "🟢"
            st.markdown(f"{priority_emoji} **{task.name}** - {task.pet.name} ({task.duration} min, Priority {task.priority})")
    else:
        st.info("No tasks added yet. Create some tasks above!")
        
elif st.session_state.owner and not st.session_state.owner.pets:
    st.warning("⚠️ Please add at least one pet first")
else:
    st.warning("⚠️ Please create an owner profile and add pets first")

# Section 4: Generate Schedule
st.divider()
st.subheader("🗓️ Generate Daily Schedule")

if st.session_state.owner and st.session_state.owner.get_all_tasks():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**Ready to schedule {len(st.session_state.owner.get_all_tasks())} tasks for {st.session_state.owner.name}**")
    with col2:
        generate_button = st.button("🚀 Generate Schedule", type="primary")
    
    if generate_button:
        # Generate the schedule
        scheduler = st.session_state.scheduler
        scheduler.load_tasks_from_owner()
        scheduler.generate_daily_plan()
        
        # Display the schedule
        st.success(f"✅ Schedule generated! {len(scheduler.daily_plan)} tasks scheduled.")
        
        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tasks Scheduled", len(scheduler.daily_plan))
        with col2:
            st.metric("Time Used", f"{scheduler.calculate_total_time()} min")
        with col3:
            efficiency = (scheduler.calculate_total_time() / st.session_state.owner.available_time * 100)
            st.metric("Efficiency", f"{efficiency:.1f}%")
        
        # Display schedule
        st.markdown("### 📅 Today's Schedule")
        for i, task in enumerate(scheduler.daily_plan, 1):
            priority_label = "🔴 HIGH" if task.is_high_priority() else "🟡 MEDIUM" if task.priority == 3 else "🟢 LOW"
            with st.container():
                st.markdown(f"**{i}. [{priority_label}] {task.name}**")
                st.caption(f"Pet: {task.pet.name} | Duration: {task.duration} min | Type: {task.task_type}")
        
        # Display conflicts if any
        if scheduler.conflicts:
            st.warning(f"⚠️ {len(scheduler.conflicts)} task(s) couldn't fit in today's schedule")
            with st.expander("View Conflicts"):
                for task in scheduler.conflicts:
                    st.markdown(f"- **{task.name}** ({task.duration} min, Priority {task.priority}) for {task.pet.name}")
                st.info("💡 Tip: Increase your available time or reduce task durations to fit more tasks.")

else:
    st.info("👆 Add an owner, pets, and tasks above to generate a schedule")

# Footer
st.divider()
st.caption("PawPal+ © 2024 | Built with Streamlit and Python")