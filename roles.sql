-- 1. Create the Roles
CREATE ROLE 'admin_role', 'merchant_role', 'auditor_role';

-- 2. Define Privileges for Admin (Full access to tables)
GRANT ALL PRIVILEGES ON credit_card_vault.* TO 'admin_role';

-- 3. Define Privileges for Merchants (Can see masked data and add new cards)
GRANT SELECT ON credit_card_vault.masked_card_view TO 'merchant_role';
GRANT INSERT ON credit_card_vault.credit_cards TO 'merchant_role';

-- 4. Define Privileges for Auditors (Read-only access to the audit view)
GRANT SELECT ON credit_card_vault.audit_log_view TO 'auditor_role';
GRANT SELECT ON credit_card_vault.user_access_levels TO 'auditor_role';

-- 5. Assign a Role to a specific Database User
-- Note: Replace 'bob_db_user' with the actual database username
CREATE USER 'bob_admin'@'localhost' IDENTIFIED BY 'BobSecurePass123!';
GRANT 'admin_role' TO 'bob_admin'@'localhost';
SET DEFAULT ROLE 'admin_role' FOR 'bob_admin'@'localhost';
