# from requests import put


# get function

# patch 

# post 

# delete 

import sqlite3


bool_ = False

conn = sqlite3.connect('API_DATA.db')

dB = conn.cursor()
holder = dB.execute('SELECT cor_word FROM TEST2')
ans = str(holder.fetchone())
answer = ans[2:8]
print(answer)

def check_word(input):
    if input == answer: return True




while bool_ != True:

    # initial prompt for game
    game_id = dB.execute('SELECT game_id FROM TEST2')
    print('Game ID', game_id)

    trys_left = dB.execute('SELECT trys_left FROM TEST2')
    print('Trys left', trys_left.fetchone())

    cor_pos = dB.execute('SELECT cor_pos FROM TEST2')
    print('Correct Position', cor_pos.fetchone())

    cor_let = dB.execute('SELECT cor_let FROM TEST2')
    print('Correct letters', cor_let.fetchone())


    x = 'Try and guess the word: '
    y = input(x)

    if y == 'EXIT':
        break

    bool_ = check_word(y)
