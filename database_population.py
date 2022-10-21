import sqlite3
import json

connect_db = sqlite3.connect('var/wordle.db')
connect = connect_db.cursor()

json_file_secret = open('share/secret.json')
json_data_s = json.load(json_file_secret)

for i in json_data_s:
    connect.execute("INSERT INTO secret (secret_word) VALUES(?)" , (i,))
json_file_secret.close()

json_file_correct = open('share/correct.json')
json_data_c = json.load(json_file_correct)

for i in json_data_c:
    connect.execute("INSERT INTO correct (correct_word) VALUES(?)" , (i,))
json_file_correct.close()

connect_db.commit()
