import sqlite3
import os

DB_PATH = "founders.db"

def init_db():
    """Initializes the SQLite database and creates the founders table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS founders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            skills TEXT NOT NULL,
            pitch TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def add_dummy_data():
    """Populates the database with some example profiles so we have people to match with."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if data already exists to avoid duplicates
    cursor.execute("SELECT COUNT(*) FROM founders")
    if cursor.fetchone()[0] == 0:
        dummy_founders = [
            ("Sarah Jenkins", "Business/Marketing", "B2B Sales, Growth Hacking, GTM Strategy", "I excel at taking deep tech products and translating them into massive enterprise contracts."),
            ("David Chen", "Technical/Software", "React, Node.js, AWS Architecture", "I build highly scalable web applications for B2C consumer startups."),
            ("Elena Rodriguez", "Operations/Finance", "Fundraising, Financial Modeling, Supply Chain", "Experienced operator who has scaled hardware manufacturing lines from prototype to mass production."),
            ("Marcus Thorne", "Design/Product", "UI/UX, Figma, User Research", "I design intuitive interfaces for complex enterprise software that users actually love to use.")
        ]
        
        cursor.executemany("INSERT INTO founders (name, role, skills, pitch) VALUES (?, ?, ?, ?)", dummy_founders)
        conn.commit()
    
    conn.close()

def get_all_founders():
    """Retrieves all founder profiles from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, role, skills, pitch FROM founders")
    rows = cursor.fetchall()
    
    conn.close()
    
    # Convert to a list of dictionaries for easier use in Python
    founders = []
    for row in rows:
        founders.append({
            "name": row[0],
            "role": row[1],
            "skills": row[2],
            "pitch": row[3]
        })
        
    return founders

def add_founder(name, role, skills, pitch):
    """Adds a new founder (the user) to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO founders (name, role, skills, pitch) VALUES (?, ?, ?, ?)", (name, role, skills, pitch))
    
    conn.commit()
    conn.close()

# Initialize the DB when this file is imported
init_db()
add_dummy_data()
