import sqlite3

# This function uses habits.db by default but can also connect to other databases, such as the test database
def get_connection(db_name='habits.db'):
    return sqlite3.connect(db_name)

# Creates the table to store habit data
def create_table():
    conn = get_connection() 
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            periodicity TEXT CHECK(periodicity IN ('daily', 'weekly')) NOT NULL,
            creation_date TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            date_completed TEXT,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Creates the table to store completion dates
def create_completion_table():
    con = get_connection() #
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            date_completed TEXT,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
    ''')
    con.commit()
    con.close()

