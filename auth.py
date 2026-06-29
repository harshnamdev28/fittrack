import hashlib
from database import get_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup(username, password):
    hashed = hash_password(password)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        conn.close()
        return True  # signup successful
    except Exception as e:
        conn.close()
        return False  # username already taken
    


def login(username, password):
    hashed = hash_password(password)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        user_id = result[0]
        return user_id   # login successful, return their ID
    else:
        return None       # login failed
    
