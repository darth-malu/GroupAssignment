   -- Create the project database
   CREATE DATABASE credit_card_vault;
   USE credit_card_vault;
 
   -- Table for authentication (SHA-2 storage)
   CREATE TABLE users (
       user_id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50) NOT NULL UNIQUE,
       password_hash VARCHAR(255) NOT NULL,
       role ENUM('Merchant', 'Admin', 'Auditor') NOT NULL
   );
 
   -- The Vault (AES storage for Sensitive/Confidential data)
   CREATE TABLE credit_cards (
       card_id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT,
       card_holder_name VARCHAR(100), -- Public Info
       card_num_enc VARBINARY(255),    -- Sensitive Info (Encrypted)
       cvv_enc VARBINARY(255),         -- Confidential Info (Encrypted)
       expiry_date DATE,
       FOREIGN KEY (user_id) REFERENCES users(user_id)
   );
