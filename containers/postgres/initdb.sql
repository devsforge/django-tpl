-- maintenance role and database creation queries
CREATE ROLE django WITH LOGIN CREATEDB PASSWORD 'django';
CREATE DATABASE django OWNER django;
