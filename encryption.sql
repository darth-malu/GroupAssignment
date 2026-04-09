  INSERT INTO
  credit_cards (user_id, card_holder_name, card_num_enc, cvv_enc, expiry_date)
  VALUES
  (1, 'Jane Doe', AES_ENCRYPT('4111222233334444', 'verysecretkey'), AES_ENCRYPT('123', 'verysecretkey'), '2026-04-09');
