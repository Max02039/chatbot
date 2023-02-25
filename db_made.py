import sqlite3
import os

PATH = os.path.abspath(__file__ + '/..')

con = sqlite3.connect(os.path.join(PATH, "db.db"))

cursor = con.cursor()

def get_all():
    all = cursor.execute("SELECT * FROM users;")
    all = cursor.fetchall()
    return all

def get_all_ses():
    end_id_session = cursor.execute("SELECT num_sessions FROM users;")
    end_id_session = cursor.fetchall()
    return end_id_session

def create_table():
    sql = '''
    DROP TABLE users;
    CREATE TABLE users (
        id int,
        idtwo int,
        num_sessions int PRIMARY KEY
    );'''
    cursor.execute(sql)
    con.commit()

def create_session(us_id1, us_id2):
    id = get_all_ses()
    if len(id) == 0:
        id = 1
    else:
        id = id[-1][-1] + 1
    sql = f'''
        INSERT INTO users
        VALUES ({us_id1}, {us_id2}, {id});'''
    cursor.execute(sql)
    con.commit()

if __name__ == '__main__':
    create_table()

def del_session(us_id):
    ses = f'''SELECT * FROM users WHERE id = {us_id} OR idtwo = {us_id};'''
    result = cursor.execute(ses).fetchone()
    a = f'''DELETE FROM users WHERE id = {us_id} OR idtwo = {us_id};'''
    cursor.execute(a)
    con.commit()
    if result[0] == us_id:
        return result[1]
    else:
        return result[0]

def take_info():
    pass