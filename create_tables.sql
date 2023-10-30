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
    password TEXT NOT NULL,
);
