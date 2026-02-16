import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .conflict-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🐾 PawPal+")
st.markdown("**Your intelligent pet care scheduling assistant**")

with st.expander("📖 How It Works", expanded=False):
    st.markdown("""
**PawPal+** uses smart scheduling algorithms to organize your pet care tasks:

1. **Add your information**: Enter your name and available time
2. **Register your pets**: Add one or more pets with their details
3. **Create tasks**: Define care tasks with duration and priority (1=highest, 5=lowest)
4. **Choose algorithm**: Select how to prioritize tasks
5. **Generate schedule**: Create an optimized daily plan with conflict detection

**Features:**
- 🔄 Multiple sorting strategies (priority, duration, smart combo)
- 🔍 Advanced filtering (by pet, status, priority, type)
- ⚠️ Automatic conflict detection
- 📊 Real-time efficiency metrics
""")

st.divider()

# Initialize session state
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pets" not in st.session_state:
    st.session_state.pets = []
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None
if "schedule_generated" not in st.session_state:
    st.session_state.schedule_generated = False

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
        step=15,
        help="How many minutes per day can you dedicate to pet care?"
    )

if st.button("Create/Update Owner Profile", type="primary"):
    st.session_state.owner = Owner(name=owner_name, available_time=available_time)
    st.session_state.pets = []
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)
    st.session_state.schedule_generated = False
    st.success(f"✅ Owner profile created: {owner_name} with {available_time} minutes available")

# Section 2: Pet Management
st.divider()
st.subheader("🐾 Your Pets")

if st.session_state.owner:
    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Rabbit", "Other"])
    with col3:
        age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)
    
    special_needs = st.text_input("Special needs (optional)", placeholder="e.g., Medication, Slow walks")
    
    if st.button("➕ Add Pet"):
        needs_list = [need.strip() for need in special_needs.split(",")] if special_needs else []
        pet = Pet(
            name=pet_name,
            species=species,
            age=age,
            owner=st.session_state.owner,
            special_needs=needs_list
        )
        st.session_state.pets.append(pet)
        st.session_state.schedule_generated = False
        st.success(f"✅ Added {pet_name} the {species}")
    
    # Display current pets
    if st.session_state.owner.pets:
        st.markdown("**Current Pets:**")
        for pet in st.session_state.owner.pets:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"🐾 {pet.get_info()}")
                with col2:
                    st.caption(f"{len(pet.tasks)} task(s)")
    else:
        st.info("💡 No pets added yet. Add one above to get started!")
else:
    st.warning("⚠️ Please create an owner profile first")

# Section 3: Task Management
st.divider()
st.subheader("📋 Care Tasks")

if st.session_state.owner and st.session_state.owner.pets:
    # Select which pet this task is for
    pet_names = [pet.name for pet in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Task for which pet?", pet_names, key="task_pet_select")
    selected_pet = next(pet for pet in st.session_state.owner.pets if pet.name == selected_pet_name)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        task_name = st.text_input("Task name", value="Morning walk", key="task_name_input")
    with col2:
        task_type = st.selectbox(
            "Task type", 
            ["feeding", "walk", "medication", "grooming", "enrichment", "cleaning"],
            key="task_type_select"
        )
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=5, max_value=240, value=20, step=5, key="task_duration")
    
    col4, col5 = st.columns(2)
    with col4:
        priority = st.slider("Priority", min_value=1, max_value=5, value=2, help="1 = Highest, 5 = Lowest", key="task_priority")
    with col5:
        recurrence = st.selectbox("Recurrence", ["daily", "weekly", "once"], key="task_recurrence")
    
    if st.button("➕ Add Task"):
        try:
            task = Task(
                name=task_name,
                task_type=task_type,
                duration=duration,
                priority=priority,
                pet=selected_pet,
                recurrence=recurrence
            )
            st.session_state.schedule_generated = False
            st.success(f"✅ Added task: {task_name} (Priority {priority}, {duration} min)")
        except ValueError as e:
            st.error(f"❌ Error creating task: {str(e)}")
    
    # Display all tasks with filtering
    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        st.markdown("---")
        st.markdown("**Task List & Filters**")
        
        # Filter controls
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_pet = st.selectbox("Filter by pet", ["All"] + pet_names, key="filter_pet")
        with col2:
            filter_status = st.selectbox("Filter by status", ["All", "Incomplete", "Completed"], key="filter_status")
        with col3:
            filter_priority = st.selectbox("Filter by priority", ["All", "High (1-2)", "Medium (3)", "Low (4-5)"], key="filter_priority")
        
        # Apply filters
        filtered_tasks = all_tasks
        if filter_pet != "All":
            scheduler = Scheduler(owner=st.session_state.owner)
            scheduler.load_tasks_from_owner()
            filtered_tasks = scheduler.filter_by_pet(filter_pet)
        
        if filter_status == "Incomplete":
            filtered_tasks = [t for t in filtered_tasks if not t.completed]
        elif filter_status == "Completed":
            filtered_tasks = [t for t in filtered_tasks if t.completed]
        
        if filter_priority == "High (1-2)":
            filtered_tasks = [t for t in filtered_tasks if t.priority <= 2]
        elif filter_priority == "Medium (3)":
            filtered_tasks = [t for t in filtered_tasks if t.priority == 3]
        elif filter_priority == "Low (4-5)":
            filtered_tasks = [t for t in filtered_tasks if t.priority >= 4]
        
        # Display filtered tasks
        st.markdown(f"**Showing {len(filtered_tasks)} of {len(all_tasks)} tasks**")
        
        for task in filtered_tasks:
            priority_emoji = "🔴" if task.priority <= 2 else "🟡" if task.priority == 3 else "🟢"
            status_emoji = "✅" if task.completed else "⭕"
            
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"{status_emoji} {priority_emoji} **{task.name}** - {task.pet.name} ({task.duration} min, P{task.priority}, {task.task_type})")
            with col2:
                if st.button("Toggle", key=f"toggle_{id(task)}"):
                    if task.completed:
                        task.mark_incomplete()
                    else:
                        task.mark_complete()
                    st.rerun()
    else:
        st.info("💡 No tasks added yet. Create some tasks above!")
        
elif st.session_state.owner and not st.session_state.owner.pets:
    st.warning("⚠️ Please add at least one pet first")
else:
    st.warning("⚠️ Please create an owner profile and add pets first")

# Section 4: Generate Schedule
st.divider()
st.subheader("🗓️ Generate Daily Schedule")

if st.session_state.owner and st.session_state.owner.get_all_tasks():
    
    # Algorithm selection
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"**Ready to schedule {len(st.session_state.owner.get_all_tasks())} tasks for {st.session_state.owner.name}**")
    with col2:
        sort_method = st.selectbox(
            "Scheduling algorithm",
            ["priority", "duration", "priority_duration"],
            format_func=lambda x: {
                "priority": "🎯 Priority First",
                "duration": "⏱️ Shortest First", 
                "priority_duration": "🧠 Smart Combo"
            }[x],
            help="Choose how to prioritize tasks"
        )
    
    # Algorithm explanation
    with st.expander("ℹ️ Algorithm Explanations"):
        st.markdown("""
**🎯 Priority First**: Schedules highest priority tasks first (1→5). Best for ensuring critical tasks never get skipped.

**⏱️ Shortest First**: Schedules quickest tasks first. Maximizes number of completed tasks.

**🧠 Smart Combo**: Sorts by priority, then duration within each priority. Best balance of importance and efficiency.
""")
    
    generate_button = st.button("🚀 Generate Schedule", type="primary")
    
    if generate_button:
        # Generate the schedule
        scheduler = st.session_state.scheduler
        scheduler.load_tasks_from_owner()
        scheduler.generate_daily_plan(sort_method=sort_method)
        
        # Assign time slots for conflict detection
        scheduler.assign_time_slots(start_time=480)  # 8:00 AM
        
        st.session_state.schedule_generated = True
        
        # Check for conflicts
        warnings = scheduler.get_conflict_warnings()
        
        # Display conflicts FIRST if any exist
        if warnings:
            st.markdown("---")
            st.markdown("### ⚠️ Conflicts Detected")
            for warning in warnings:
                st.warning(warning)
            
            st.info("💡 **Tip**: Increase your available time, reduce task durations, or mark some tasks as lower priority to resolve conflicts.")
        
        # Display the schedule
        st.markdown("---")
        st.success(f"✅ Schedule generated using **{sort_method.replace('_', ' + ').title()}** algorithm!")
        
        # Stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Tasks Scheduled", len(scheduler.daily_plan))
        with col2:
            st.metric("Time Used", f"{scheduler.calculate_total_time()} min")
        with col3:
            efficiency = (scheduler.calculate_total_time() / st.session_state.owner.available_time * 100) if st.session_state.owner.available_time > 0 else 0
            st.metric("Efficiency", f"{efficiency:.1f}%")
        with col4:
            st.metric("Conflicts", len(scheduler.conflicts), delta=f"-{len(scheduler.conflicts)}" if len(scheduler.conflicts) > 0 else "0", delta_color="inverse")
        
        # Display schedule as table
        st.markdown("### 📅 Today's Schedule")
        
        schedule_data = []
        for i, task in enumerate(scheduler.daily_plan, 1):
            priority_label = "🔴 High" if task.is_high_priority() else "🟡 Med" if task.priority == 3 else "🟢 Low"
            status = "✅" if task.completed else "⭕"
            
            if task.scheduled_time:
                start_time = scheduler._format_time(task.scheduled_time)
                end_time = scheduler._format_time(task.scheduled_time + task.duration)
                time_slot = f"{start_time} - {end_time}"
            else:
                time_slot = "Not scheduled"
            
            schedule_data.append({
                "#": i,
                "Time": time_slot,
                "Task": task.name,
                "Pet": task.pet.name,
                "Type": task.task_type.title(),
                "Duration": f"{task.duration} min",
                "Priority": priority_label,
                "Status": status
            })
        
        st.dataframe(schedule_data, use_container_width=True, hide_index=True)
        
        # Display conflicts if any
        if scheduler.conflicts:
            st.markdown("---")
            st.markdown("### 📋 Tasks That Didn't Fit")
            
            conflict_data = []
            for task in scheduler.conflicts:
                priority_label = "🔴 High" if task.is_high_priority() else "🟡 Med" if task.priority == 3 else "🟢 Low"
                conflict_data.append({
                    "Task": task.name,
                    "Pet": task.pet.name,
                    "Duration": f"{task.duration} min",
                    "Priority": priority_label,
                    "Reason": "Not enough time remaining"
                })
            
            st.dataframe(conflict_data, use_container_width=True, hide_index=True)
        
        # Export schedule option
        st.markdown("---")
        if st.button("📄 View Text Summary"):
            st.text(scheduler.get_plan_summary())

else:
    st.info("👆 Add an owner, pets, and tasks above to generate a schedule")

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🐾 PawPal+ © 2024")
with col2:
    st.caption("Built with Streamlit & Python")
with col3:
    st.caption("✅ 26 tests passing")