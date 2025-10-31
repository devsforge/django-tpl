-- maintenance role and database creation queries
CREATE ROLE django WITH LOGIN PASSWORD 'django';
CREATE DATABASE django OWNER django;
