from datetime import datetime, timedelta
import time
import sqlite3

# This function displays all created habits
def get_all_habits():
    from main import post_action_menu
    con = sqlite3.connect("habits.db")
    cursor = con.cursor()

    cursor.execute("SELECT name FROM habits")
    habits = cursor.fetchall()

    if not habits:
        print("📭 No habits currently being tracked.")
    else:
        print("\n📋 Currently tracked habits:")
        for habit in habits:
            print(f"- {habit[0]}")

    con.close()
    time.sleep(2)
    post_action_menu()
    
def get_habits_by_periodicity():
    from main import post_action_menu
    con = sqlite3.connect("habits.db")
    cursor = con.cursor()

    periodicity = input("Enter periodicity to filter by (daily/weekly): ").strip().lower()
    while periodicity not in ['daily', 'weekly']:
        periodicity = input("Invalid input! Please enter 'daily' or 'weekly': ").strip().lower()

    cursor.execute("SELECT name FROM habits WHERE periodicity = ?", (periodicity,))
    habits = cursor.fetchall()

    if not habits:
        print(f"😶 No habits found with periodicity '{periodicity}'.")
    else:
        print(f"\n📋 Habits with periodicity '{periodicity}':")
        for habit in habits:
            print(f"- {habit[0]}")

    con.close()
    time.sleep(2)
    post_action_menu()

# This function calculates the longest streak and belongs to the 'Analytics Menu'
def calculate_longest_streak(dates, periodicity):
    if not dates:
        return 0

    dates = sorted(datetime.strptime(d, "%Y-%m-%d").date() for d in dates)

    if periodicity == 'daily':
        expected_gap = timedelta(days=1)
    else:
        expected_gap = timedelta(weeks=1)

    longest = current = 1

    for i in range(1, len(dates)):
        gap = dates[i] - dates[i - 1]

        if gap == expected_gap:
            current += 1
        elif gap < expected_gap:
            # allow same-day duplicates (can happen by mistake), ignore
            continue
        else:
            # if the gap is too big, reset current streak
            longest = max(longest, current)
            current = 1

    longest = max(longest, current)
    return longest

def get_longest_streaks_all():
    from main import post_action_menu
    import sqlite3
    con = sqlite3.connect("habits.db")
    cursor = con.cursor()

    cursor.execute("SELECT id, name, periodicity FROM habits")
    habits = cursor.fetchall()

    if not habits:
        print("😶 No habits found.")
        con.close()
        return

    print("\n📊 Longest streaks for all habits:")
    for habit_id, name, periodicity in habits:
        cursor.execute("SELECT date_completed FROM completions WHERE habit_id = ?", (habit_id,))
        dates = [row[0] for row in cursor.fetchall()]
        longest_streak = calculate_longest_streak(dates, periodicity)
        print(f"- {name}: {longest_streak} {'day' if periodicity == 'daily' else 'week'}(s)")

    con.close()
    time.sleep(3)
    post_action_menu()
    
# This function checks the longest streak for a specific habit
def get_longest_streak_for_habit():
    from main import post_action_menu
    import sqlite3
    con = sqlite3.connect("habits.db")
    cursor = con.cursor()

    cursor.execute("SELECT id, name, periodicity FROM habits")
    habits = cursor.fetchall()

    if not habits:
        print("😶 No habits found.")
        con.close()
        return

    print("\n📋 Habits:")
    for idx, habit in enumerate(habits, start=1):
        print(f"{idx}. {habit[1]}")

    choice = input("Enter habit number or name to check longest streak: ").strip()
    habit_id = None
    periodicity = None

    if choice.isdigit():
        index = int(choice)
        if 1 <= index <= len(habits):
            habit_id, _, periodicity = habits[index - 1]
    else:
        for h_id, h_name, per in habits:
            if h_name.lower() == choice.lower():
                habit_id = h_id
                periodicity = per
                break

    if habit_id is None:
        print("❌ Habit not found. Try again.")
        con.close()
        return

    cursor.execute("SELECT date_completed FROM completions WHERE habit_id = ?", (habit_id,))
    dates = [row[0] for row in cursor.fetchall()]

    longest_streak = calculate_longest_streak(dates, periodicity)

    print(f"🏆 Longest streak for '{choice}': {longest_streak} {'day' if periodicity == 'daily' else 'week'}(s)")
    con.close()
    time.sleep(2)
    post_action_menu()

# This function is related to option 2 of the main menu to display the current streak
def calculate_current_streak(dates, periodicity):
    if not dates:
        return 0

    dates = sorted(datetime.strptime(d, "%Y-%m-%d").date() for d in dates)
    today = datetime.today().date()

    # Daily or weekly expected gaps
    if periodicity == 'daily':
        expected_gap = timedelta(days=1)
    else:
        expected_gap = timedelta(weeks=1)

    streak = 1
    for i in range(len(dates) - 1, 0, -1):
        if dates[i] - dates[i - 1] == expected_gap:
            streak += 1
        else:
            break

    # Don't reset if the user still has time to complete the habit today
    last_completion = dates[-1]

    if periodicity == 'daily':
        # If last completion was yesterday, streak continues until end of today
        if today - last_completion > timedelta(days=1):
            return 0
    else:
        # If last completion was more than a week ago, reset
        if today - last_completion > timedelta(weeks=1):
            return 0

    return streak


def calculate_streak(habit_id, periodicity, completions):
    """
    Calculate the current streak for a habit.
    :param habit_id: int
    :param periodicity: 'daily' or 'weekly'
    :param completions: list of date strings 'YYYY-MM-DD' sorted descending (newest first)
    :return: int (number of consecutive periods)
    """
    if not completions:
        return 0

    today = datetime.now().date()
    streak = 0

    if periodicity == 'daily':
        expected_date = today
        for c_date_str in completions:
            c_date = datetime.strptime(c_date_str, "%Y-%m-%d").date()
            if c_date == expected_date:
                streak += 1
                expected_date -= timedelta(days=1)
            elif c_date < expected_date:
                break
    elif periodicity == 'weekly':
        expected_year, expected_week, _ = today.isocalendar()
        for c_date_str in completions:
            c_date = datetime.strptime(c_date_str, "%Y-%m-%d").date()
            year, week, _ = c_date.isocalendar()
            if year == expected_year and week == expected_week:
                streak += 1
                prev_week_date = c_date - timedelta(weeks=1)
                expected_year, expected_week, _ = prev_week_date.isocalendar()
            elif (year < expected_year) or (year == expected_year and week < expected_week):
                break
    else:
        streak = 0

    return streak