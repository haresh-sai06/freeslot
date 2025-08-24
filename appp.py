import pandas as pd
from datetime import datetime

# Load your timetable CSV
df = pd.read_csv("civil_timetable.csv").fillna("")

# If Department column is missing, add it (for Civil)
if "Department" not in df.columns:
    df["Department"] = "CIVIL"

# If Classroom column is missing, add it
if "Classroom" not in df.columns:
    df["Classroom"] = "W309"

# Define slots
SLOTS = {
    "S1": ("08:50", "09:40"),
    "S2": ("09:40", "10:30"),
    "S3": ("10:45", "11:35"),
    "S4": ("11:35", "12:25"),
    "S5": ("13:30", "14:20"),
    "S6": ("14:20", "15:10"),
    "S7": ("15:10", "16:00"),
    "S8": ("16:00", "16:35"),
}

def get_slot(time_str):
    """Find slot ID for given time."""
    t = datetime.strptime(time_str, "%H:%M").time()
    for slot, (start, end) in SLOTS.items():
        if datetime.strptime(start, "%H:%M").time() <= t <= datetime.strptime(end, "%H:%M").time():
            return slot, start, end
    return None, None, None

def check_slots(day, query_time):
    """Check all classrooms at given time/day and return which are free/occupied."""
    slot, start, end = get_slot(query_time)
    if not slot:
        return f"{query_time} is not in any teaching slot (maybe break/lunch)."

    # Filter timetable
    subset = df[(df["Day"].str.lower() == day.lower()) & (df["Slot"] == slot)]

    if subset.empty:
        return f"No timetable entries found for {day} {query_time} ({slot})."

    response = f"At {query_time} ({slot}, {day}, {start}-{end}):\n"
    for _, row in subset.iterrows():
        dept = row["Department"]
        classroom = row["Classroom"]
        subject = row["Subject"]
        if subject == "":
            response += f"- {dept} {classroom} is FREE ✅\n"
        else:
            faculty = row.get("Faculty", "")
            response += f"- {dept} {classroom} is OCCUPIED ❌ ({subject}, {faculty})\n"
    return response

# ----------------------
# Example interaction
# ----------------------
day = input("Enter the day (e.g., Wednesday): ")
time_input = input("Enter the time (HH:MM, e.g., 11:00): ")

print(check_slots(day, time_input))
