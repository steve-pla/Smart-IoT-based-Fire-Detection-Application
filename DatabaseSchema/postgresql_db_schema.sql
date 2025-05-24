-- create_tables.sql

CREATE TABLE measurements (
    timestamp TIMESTAMP WITH TIME ZONE PRIMARY KEY,
    co2 DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    o2 DOUBLE PRECISION,
    no2 DOUBLE PRECISION
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
