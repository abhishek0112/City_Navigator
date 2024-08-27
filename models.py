import sqlite3
def init_db():
    conn=sqlite3.connect('city_navigator.db')
    c=conn.cursor()
    
    #create table
    
    #for buses
    c.execute('''
    CREATE TABLE IF NOT EXISTS buses (
        location TEXT NOT NULL,
        time TEXT NOT NULL,
        destination TEXT NOT NULL
    )
    ''')

    
    #for trains
    c.execute('''
    CREATE TABLE IF NOT EXISTS trains (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT NOT NULL,
        train_num TEXT NOT NULL,
        time TEXT NOT NULL,
        platform TEXT NOT NULL,
        destination TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

if __name__=='__main__':
    init_db()