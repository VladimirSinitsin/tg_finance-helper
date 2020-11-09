CREATE TABLE Budget(
    id INT IDENTITY PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    money INT
);

CREATE TABLE Category(
    codename VARCHAR(32) PRIMARY KEY
);

CREATE TABLE Product(
    codename VARCHAR(32) PRIMARY KEY,
    category_codename VARCHAR(32),
    FOREIGN KEY(category_codename) REFERENCES Category(codename)
);

CREATE TABLE Cost(
    id IDENTITY PRIMARY KEY,
    price INT,
    created DATATIME,
    product_codename VARCHAR(32),
    FOREIGN KEY(product_codename) REFERENCES Product(codename)
);