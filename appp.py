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


def parse_time(tstr):
    """Convert messy time strings like 'S8.50am' or '9.40 am' to datetime.time"""
    tstr = tstr.lower().replace("s", "").replace(".", ":").strip()
    tstr = tstr.replace(" ", "")
    # Ensure am/pm format is valid
    try:
        return datetime.strptime(tstr, "%I:%M%p").time()
    except:
        return None


def get_csv_slot_range(slot_str):
    """Extract start and end times from CSV slot string"""
    try:
        parts = slot_str.split("-")
        start = parse_time(parts[0])
        end = parse_time(parts[1])
        return start, end
    except:
        return None, None


def get_slot_from_csv(query_time_str, day):
    """Find which slot (row) matches the query time for that day"""
    qtime = datetime.strptime(query_time_str, "%H:%M").time()
    day_subset = df[df["Day"].str.lower() == day.lower()]

    for idx, row in day_subset.iterrows():
        start, end = get_csv_slot_range(row["Slot"])
        if not start or not end:
            continue
        if start <= qtime <= end:
            return row, start, end
    return None, None, None


def check_slots(day, query_time):
    """Check all classrooms at given time/day and return free/occupied status"""
    row, start, end = get_slot_from_csv(query_time, day)
    if row is None:
        return f"{query_time} is not in any teaching slot (maybe break/lunch)."

    dept = row["Department"]
    classroom = row["Classroom"]
    subject = row["Subject"]
    faculty = row.get("Faculty", "")

    if subject == "" or subject.lower() == "break":
        return f"At {query_time} ({day}, {start}-{end}):\n- {dept} {classroom} is FREE ✅"
    else:
        return f"At {query_time} ({day}, {start}-{end}):\n- {dept} {classroom} is OCCUPIED ❌ ({subject}, {faculty})"


# ----------------------
# Example interaction
# ----------------------
day = input("Enter the day (e.g., Wednesday): ")
time_input = input("Enter the time (HH:MM, e.g., 11:00): ")

print(check_slots(day, time_input))
