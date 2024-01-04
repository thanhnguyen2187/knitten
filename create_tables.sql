CREATE TABLE products (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    patterns TEXT NOT NULL,
    image_url TEXT NOT NULL
);

CREATE TABLE users (
    id TEXT PRIMARY KEY,
    role TEXT NOT NULL,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
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
    id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL,
    yarn_id TEXT NOT NULL,
    yarn_count INTEGER NOT NULL,
    FOREIGN KEY (yarn_id) REFERENCES yarns (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE orders (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE order_products (
    id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    product_count INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

