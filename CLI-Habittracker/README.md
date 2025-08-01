# 🧠 Habit Tracker (Python CLI)

A command-line habit tracking app built with Python using Object-Oriented Programming, SQLite for data persistence, and functional programming for analytics. This project allows users to track daily and weekly habits, mark completions, monitor progress, and analyze their consistency through streaks and reports.

---

## Features

-  Create, delete, and list habits
-  Support for both *daily* and *weekly* habits
-  Mark habits as completed with dates
-  Track *current* and *longest* streaks
-  Analyze habit consistency using functional programming
-  Comes with unit tests and pre-filled example data
-  Stores data locally in a SQLite database

---

##  Project Structure

habit-tracker/
│
├── main.py              # Main CLI interface
├── habits.py            # Habit class and management logic
├── database.py          # Database connection and setup
├── analysis.py          # Analytics (FP-based streaks, filters)
├── test.py              # Unit tests for core functionality
├── habits.db            # SQLite database
├── habits_test.db       # Test database
└── README.md            # This file

---

## echnologies Used

- Python 3
- SQLite3
- OOP (Object-Oriented Programming)
- FP (Functional Programming in analysis.py)
- CLI-based user interaction
- datetime, time, sqlite3 libraries

---

##  How to Run

1. *Clone the repo:*

```bash
git clone https://github.com/vania-kouhsari/CLI-Python-App 
cd CLI-Habittracker 
```
2. *Run the app*

```bash
python main.py
```

3. *Run the CLI instructions to create and manage habits*

## Analytics Features

- List all currently tracked habits
- List all habits by periodicity (daily/weekly)
- Get longest streak for each habit
- Get longest streak for a specific habit
- Get current streak for any habit

## Testing
*Run unit tests using:*

```bash
python test.py
```

App includes a separate test dataset in order keep habit data clean. You can start testing right away without needing to add habits manually.

## Final Notes

This project was developed as part of a university assignment and is designed to demonstrate:
	•	Practical OOP usage
	•	Functional programming in analytics
	•	Data persistence with SQLite
	•	CLI design and user interaction
	•	Modular code organization

Thank you for reviewing this project!