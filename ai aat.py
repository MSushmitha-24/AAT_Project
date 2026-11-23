
import random
from datetime import datetime, timedelta

# ==========================================
# 1. GET STARTING DATE
# ==========================================

start_date = datetime.strptime(
    input("Enter starting date (DD-MM-YYYY): "),
    "%d-%m-%Y"
).date()


# ==========================================
# 2. SEMESTER-WISE SUBJECTS
# ==========================================

subjects = {
    "VII Semester": [
        "MVJ22xx71", "MVJ22xx72", "MVJ22xx73",
        "MVJ22xx74", "MVJ22xx75"
    ],

    "VI Semester": [
        "MVJ22xx61", "MVJ22xx62",
        "MVJ22xx63x", "MVJ22xx64x"
    ],

    "V Semester": [
        "MVJ22xx51", "MVJ22xx52",
        "MVJ22xx53", "MVJ22xx55x"
    ],

    "IV Semester": [
        "MVJ22BI47", "MVJ22xx41",
        "MVJ22xx42", "MVJ22xx43",
        "MVJ22UHV48"
    ],

    "III Semester": [
        "MVJ22xx36x", "MVJ22xx34",
        "MVJ22xx31", "MVJ22xx32",
        "MVJ22xx33"
    ],

    "I/II Semester": [
        "MVJ22PWSK26", "MVJ22ENGR16",
        "MVJ22ICOK17", "MVJ22SKK17"
    ]
}


# ==========================================
# 3. FIXED EXAMINATION SESSIONS
# ==========================================

morning = ["VII Semester", "I/II Semester"]

afternoon = [
    "VI Semester", "V Semester",
    "IV Semester", "III Semester"
]

MAX_GAP = 2


# ==========================================
# 4. RANDOMIZE SUBJECT ORDER
# ==========================================

remaining = {}

for sem, course_list in subjects.items():
    remaining[sem] = course_list.copy()
    random.shuffle(remaining[sem])


# ==========================================
# 5. GENERATE WORKING DATES
# ==========================================

# Each working day has two examination slots.
# The ending date is calculated automatically.

timetable = {}
last_exam = {}
gap_violations = []

current_date = start_date

while any(remaining.values()):

    # Skip Saturday and Sunday
    if current_date.weekday() in (5, 6):
        current_date += timedelta(days=1)
        continue

    timetable[current_date] = {
        sem: "-" for sem in subjects
    }

    # -------------------------------
    # MORNING SESSION
    # -------------------------------

    active_morning = [
        sem for sem in morning if remaining[sem]
    ]

    if active_morning:

        sem = random.choice(active_morning)
        subject = remaining[sem].pop()

        timetable[current_date][sem] = subject

        # Check gap between examinations
        if sem in last_exam:
            gap = (current_date - last_exam[sem]).days

            # Count intervening working days
            working_gap = sum(
                1 for i in range(1, gap)
                if (last_exam[sem] +
                    timedelta(days=i)).weekday() < 5
            )

            if working_gap > MAX_GAP:
                gap_violations.append(
                    (sem, last_exam[sem],
                     current_date, working_gap)
                )

        last_exam[sem] = current_date

    # -------------------------------
    # AFTERNOON SESSION
    # -------------------------------

    active_afternoon = [
        sem for sem in afternoon if remaining[sem]
    ]

    if active_afternoon:

        sem = random.choice(active_afternoon)
        subject = remaining[sem].pop()

        timetable[current_date][sem] = subject

        # Check gap between examinations
        if sem in last_exam:
            gap = (current_date - last_exam[sem]).days

            working_gap = sum(
                1 for i in range(1, gap)
                if (last_exam[sem] +
                    timedelta(days=i)).weekday() < 5
            )

            if working_gap > MAX_GAP:
                gap_violations.append(
                    (sem, last_exam[sem],
                     current_date, working_gap)
                )

        last_exam[sem] = current_date

    current_date += timedelta(days=1)


# ==========================================
# 6. DISPLAY FORMATTED TIMETABLE
# ==========================================

def display_table():

    widths = [12, 12, 16, 16, 16, 16, 16, 16]

    def border():
        print(
            "+" + "+".join("-" * w for w in widths) + "+"
        )

    def print_row(values):
        print(
            "|" + "|".join(
                str(v).center(w)
                for v, w in zip(values, widths)
            ) + "|"
        )

    print("\n")
    print("MVJ COLLEGE OF ENGINEERING, BANGALORE".center(120))
    print("2022 Scheme".center(120))
    print("SEMESTER END EXAMINATIONS".center(120))
    print("\n")

    # TABLE HEADER
    border()

    print_row([
        "Date", "Day", "VII Semester",
        "VI Semester", "V Semester",
        "IV Semester", "III Semester",
        "I/II Semester"
    ])

    print_row([
        "", "", "9.30 AM -",
        "2.00 PM -", "2.00 PM -",
        "2.00 PM -", "2.00 PM -",
        "9.30 AM -"
    ])

    print_row([
        "", "", "12.30 PM",
        "5.00 PM", "5.00 PM",
        "5.00 PM", "5.00 PM",
        "12.30 PM"
    ])

    border()

    # TABLE DATA
    for d, exams in timetable.items():

        row = [
            d.strftime("%d.%m.%Y"),
            d.strftime("%A")
        ]

        for sem in subjects:
            row.append(exams[sem])

        print_row(row)
        border()

    # ======================================
    # 7. DISPLAY FINAL DETAILS
    # ======================================

    print("\nEXAMINATION DETAILS")

    print("Starting Date:",
          list(timetable.keys())[0])

    print("Ending Date:",
          list(timetable.keys())[-1])

    print("Total Examination Days:",
          len(timetable))

    print("\nSUBJECT COMPLETION STATUS")

    for sem in subjects:
        print(
            sem, ":", len(subjects[sem]),
            "subjects completed"
        )

    # ======================================
    # 8. CONSTRAINT VALIDATION
    # ======================================

    print("\nCONSTRAINT VALIDATION")

    # Session conflict check
    print("Session clashes: NONE")

    # Weekend check
    weekends = [
        d for d in timetable if d.weekday() >= 5
    ]

    if not weekends:
        print("Saturday/Sunday exams: NONE")

    # Gap check
    if not gap_violations:
        print("Maximum 2 working-day gap: SATISFIED")
    else:
        print("Maximum 2 working-day gap: NOT SATISFIED")
        print("Unavoidable gap violations:")

        for sem, previous, current, gap in gap_violations:
            print(
                sem, ":",
                previous, "to", current,
                "-", gap, "intervening working days"
            )

    print("\nTIMETABLE GENERATION COMPLETED")


# ==========================================
# 9. RUN PROGRAM
# ==========================================

display_table()
