DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    username VARCHAR(32) PRIMARY KEY,
    first_name VARCHAR(32),
    last_name VARCHAR(32),
    email VARCHAR(64),
    password CHAR(128) NOT NULL,
    salt CHAR(128) NOT NULL ,
    creation_date TIMESTAMPTZ NOT NULL DEFAULT current_timestamp
);
DROP TABLE IF EXISTS user_roles;
CREATE TABLE user_roles (
    username VARCHAR(32) REFERENCES users(username) ON DELETE CASCADE ,
    role VARCHAR(32),
    PRIMARY KEY (username, role)
);