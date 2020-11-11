CREATE TABLE Budget(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    money INTEGER
);

CREATE TABLE Category(
    codename TEXT PRIMARY KEY
);

CREATE TABLE Product(
    codename TEXT PRIMARY KEY,
    category_codename TEXT,
    FOREIGN KEY(category_codename) REFERENCES Category(codename)
);

CREATE TABLE Cost(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    price INTEGER,
    created DATATIME,
    product_codename TEXT,
    FOREIGN KEY(product_codename) REFERENCES Product(codename)
);