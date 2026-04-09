CREATE VIEW masked_card_view AS
SELECT card_holder_name, 
       CONCAT('****-****-****-', RIGHT(CAST(AES_DECRYPT(card_num_enc, 'verysecretkey') AS CHAR), 4)) AS card_display
FROM credit_cards;

CREATE VIEW audit_log_view AS
SELECT card_id, user_id, expiry_date FROM credit_cards;
