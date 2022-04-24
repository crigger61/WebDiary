DROP TABLE IF EXISTS users;
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(32) UNIQUE NOT NULL ,
    first_name VARCHAR(32),
    last_name VARCHAR(32),
    email VARCHAR(64),
    password CHAR(128) NOT NULL,
    salt CHAR(128) NOT NULL ,
    creation_date TIMESTAMPTZ NOT NULL DEFAULT current_timestamp
)
