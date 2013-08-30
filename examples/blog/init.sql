CREATE TABLE post (id INTEGER PRIMARY KEY, title TEXT, content TEXT, created_on datetime default current_timestamp, writer_id INTEGER);
CREATE TABLE writer (id INTEGER PRIMARY KEY, username VARCHAR(60), password VARCHAR(256), full_name VARCHAR(256));

INSERT INTO writer (username, password, full_name) VALUES ('zedshaw', 'hackme', 'Zed Shaw');

