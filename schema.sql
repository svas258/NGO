DROP TABLE IF EXISTS posts;

CREATE TABLE posts ( 
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      NGO_NAME TEXT NOT NULL,
      contact_No INTEGER NOT NULL,
      email VARCHAR NOT NULL
);
