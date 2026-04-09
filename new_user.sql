-- Registering a new user
INSERT INTO users (username, password_hash, role) 
VALUES ('admin_bob', SHA2('Apt3090Password!', 256), 'Admin');
