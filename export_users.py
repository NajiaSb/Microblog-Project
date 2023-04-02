import sqlite3
import csv

# script for exporting database contents to csv file

db_path = 'app.db'
csv_file = 'users.csv'
users_table = 'user'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute(f'SELECT username, password_hash, otp_secret FROM {users_table}')
rows = cursor.fetchall()

with open(csv_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['username', 'password', 'token'])
    csv_writer.writerows(rows)

conn.close()
