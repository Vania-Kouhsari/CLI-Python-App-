from database import create_table
from analysis import (
    get_all_habits,
    get_habits_by_periodicity,
    get_longest_streaks_all,
    get_longest_streak_for_habit,
    calculate_current_streak,
    calculate_streak
)
from habits import Habit
from datetime import datetime
import sqlite3
import time
import sys
from database import get_connection

# This exists in case of testing
IS_TEST_MODE = 'unittest' in sys.modules

def main_menu():
    while True:
        print("\n💡 Habit Tracker Menu")
        print("1. Create a new habit")
        print("2. View all habits")
        print("3. Delete a habit")
        print("4. Mark habit as completed")
        print("5. Habit analytics")
        print("6. Exit")

        choice = input("Select an option (1-6): ")

        if choice == "1":
            create_habit()
        elif choice == "2":
            view_habits()
        elif choice == "3":
            delete_habit()
        elif choice == "4":
            mark_completed()
        elif choice == "5":
            analytics_menu()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")
            time.sleep(2)

# Creating a new habit
def create_habit():
    name = input("Enter habit name: ")

    conn = get_connection()   
    cursor = conn.cursor()

    # Check if the habit already exists
    cursor.execute("SELECT * FROM habits WHERE name = ?", (name,))
    if cursor.fetchone():
        print("⚠ A habit with this name already exists.")
        conn.close()
        time.sleep(2)
        return
    
    description = input("Enter description: ")

    # Ask for periodicity until it's valid
    while True:
        periodicity = input("Enter periodicity (daily/weekly): ").lower()
        if periodicity in ["daily", "weekly"]:
            break
        else:
            print("❌ Invalid input. Please enter 'daily' or 'weekly'.")

    new_habit = Habit(name, description, periodicity)

    cursor.execute('''
        INSERT INTO habits (name, description, periodicity, creation_date)
        VALUES (?, ?, ?, ?)
    ''', (new_habit.name, new_habit.description, new_habit.periodicity, new_habit.creation_time))

    conn.commit()
    conn.close()
    print("✅ Habit created!")
    time.sleep(2)
    post_action_menu()

# Viewing all habits that exist
def view_habits():
    con = get_connection()  
    cursor = con.cursor()

    cursor.execute("SELECT id, name, periodicity, creation_date FROM habits")
    habits = cursor.fetchall()

    if not habits:
        print("😶 No habits found.")
    else:
        print("\n📋 Your Habits with Streaks:")
        for idx, habit in enumerate(habits, start=1):
            habit_id = habit[0]
            name = habit[1]
            periodicity = habit[2]
            creation_date = habit[3]

            # Get all completion dates for habits
            cursor.execute("""
                SELECT date_completed FROM completions WHERE habit_id = ? ORDER BY date_completed DESC
            """, (habit_id,))
            completions = [row[0] for row in cursor.fetchall()]

            streak = calculate_streak(habit_id, periodicity, completions) 

            print(f"{idx}. {name} | Period: {periodicity} | Created: {creation_date} | Current Streak: {streak}")
        time.sleep(2)
        post_action_menu()

    con.close()

def delete_habit():
    con = get_connection() 
    cursor = con.cursor()

    cursor.execute("SELECT id, name FROM habits")
    habits = cursor.fetchall()

    if not habits:
        print("😶 No habits to delete.")
        con.close()
        return

    print("\nSelect the habit to delete:")
    # Always start habit IDs from 1
    for idx, habit in enumerate(habits, start=1):
        print(f"{idx}. {habit[1]}")

    habit_id = None
    while habit_id is None:
        choice = input("Enter habit number or name to delete: ").strip()

        # Try to match by number
        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(habits):
                habit_id = habits[index - 1][0]  

        # If not found by number, try by name 
        if habit_id is None:
            for h_id, h_name in habits:
                if h_name.lower() == choice.lower():
                    habit_id = h_id
                    break

        if habit_id is None:
            print("❌ No habit found with that number or name. Please try again.")

    # Delete the habit from the database
    cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    con.commit()
    con.close()
    print("🗑 Habit deleted!")
    time.sleep(2)
    post_action_menu()

# Marking a habit as completed
def mark_completed():
    con = get_connection()   
    cursor = con.cursor()

    cursor.execute("SELECT id, name FROM habits")
    habits = cursor.fetchall()

    if not habits:
        print("😶 No habits to mark completed.")
        con.close()
        return

    print("\nSelect the habit to mark as completed:")

    for idx, habit in enumerate(habits, start=1):
        print(f"{idx}. {habit[1]}")

    habit_id = None
    while habit_id is None:
        choice = input("Enter habit number or name: ").strip()

        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(habits):
                habit_id = habits[index - 1][0]  
        # If not found by index, try name
        if habit_id is None:
            for h_id, h_name in habits:
                if h_name.lower() == choice.lower():
                    habit_id = h_id
                    break

        if habit_id is None:
            print("❌ No habit found with that number or name. Try again.")

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT * FROM completions WHERE habit_id = ? AND date_completed = ?
    """, (habit_id, today))
    if cursor.fetchone():
        print("⚠ Habit already marked as completed for today.")
        con.close()
        time.sleep(2)
        return

    cursor.execute("""
        INSERT INTO completions (habit_id, date_completed) VALUES (?, ?)
    """, (habit_id, today))

    con.commit()
    con.close()
    print(f"✅ Habit marked as completed for {today}!")
    time.sleep(2)
    post_action_menu()

# Displays the habit analytics sub menu (option 5 in the main menu)
def analytics_menu():
    while True:
        print("\n📊 Analytics Menu")
        print("1. List all habits")
        print("2. List habits by periodicity")
        print("3. Show longest streak for all habits")
        print("4. Show longest streak for a specific habit")
        print("5. Go back to main menu")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            get_all_habits()
        elif choice == "2":
            get_habits_by_periodicity()
        elif choice == "3":
            get_longest_streaks_all()
        elif choice == "4":
            get_longest_streak_for_habit()
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice, try again.")

# This menu is displayed after each taken action providing a simpler use
def post_action_menu():
    if IS_TEST_MODE:
        return
    while True:
        print("\nWhat do you want to do next?")
        print("1. Go back menu")
        print("2. Exit program")

        choice = input("Enter 1 or 2: ").strip()

        if choice == "1":
            return  # Call main menu again
        elif choice == "2":
            print("👋 Goodbye!")
            sys.exit()
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    create_table()  # Ensures tables exist
    main_menu()     # Starts the CLI