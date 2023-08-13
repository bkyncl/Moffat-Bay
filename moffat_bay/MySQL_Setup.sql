DROP DATABASE IF EXISTS moffat_bay;
CREATE DATABASE moffat_bay;
DROP USER IF EXISTS 'bravoteam';
CREATE USER 'bravoteam' IDENTIFIED WITH mysql_native_password BY 'Bravo123';
GRANT ALL ON moffat_bay.* TO 'bravoteam';