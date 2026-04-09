  SELECT card_holder_name, 
        CAST(AES_DECRYPT(card_num_enc, 'verysecretkey') AS CHAR) AS card_number,
        CAST(AES_DECRYPT(cvv_enc, 'verysecretkey') AS CHAR) AS cvv
  FROM credit_cards;
