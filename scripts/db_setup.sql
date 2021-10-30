DROP DATABASE IF EXISTS wsbots_db;
CREATE DATABASE wsbots_db;
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles  -- SELECT list can be empty for this
      WHERE  rolname = 'wsbots') THEN

      CREATE ROLE wsbots LOGIN PASSWORD 'password';
   END IF;
END
$do$;