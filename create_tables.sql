CREATE TABLE products (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    patterns TEXT NOT NULL,
    image_url TEXT NOT NULL
);

CREATE TABLE users (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    full_name TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE yarns (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    color TEXT NOT NULL,
    price_per_unit INTEGER NOT NULL
);

CREATE TABLE product__yarn (
    product_id TEXT NOT NULL,
    yarn_id TEXT NOT NULL,
    yarn_count INTEGER NOT NULL,
    PRIMARY KEY (yarn_id, product_id),
    FOREIGN KEY (yarn_id) REFERENCES yarns (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);

