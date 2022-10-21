PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS id;
DROP TABLE IF EXISTS play;
DROP TABLE IF EXISTS secret;
DROP TABLE IF EXISTS correct;

CREATE TABLE user( 
    user_id VARCHAR(50) NOT NULL PRIMARY KEY, 
    user_pass VARCHAR(50) NOT NULL, 
    UNIQUE(user_id)
);

CREATE TABLE id(
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(50),
    secret_word_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES user(user_id),
    FOREIGN KEY (secret_word_id) REFERENCES secret(secret_word_id)
);	    

CREATE TABLE play(
    play_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    guessed_word VARCHAR(5),
    cr_lt_cr_pl VARCHAR(10),
    cr_lt_wr_pl VARCHAR(10)
    FOREIGN KEY (game_id) REFERENCES id(game_id),
);

CREATE TABLE secret(
    secret_word_id INTEGER PRIMARY KEY AUTOINCREMENT,
    secret_word VARCHAR(5)
);

CREATE TABLE correct(
    correct_word_id INTEGER PRIMARY KEY AUTOINCREMENT,
    correct_word VARCHAR(5)
);
COMMIT;
