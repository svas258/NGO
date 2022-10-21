
CREATE TABLE Users ( 
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      public_id INTEGER ,
      name TEXT NOT NULL,
      password VARCHAR NOT NULL,
      admin BOOLEAN NOT NULL
);
