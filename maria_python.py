import socket
import mariadb 

# Setup MariaDB Connection
# db_conn = mariadb.connect(user="admin_bob", password="Apt3090Password!", database="credit_card_vault")
try:
    db_conn = mariadb.connect(
        user="admin_bob",
        password="Apt3090Password!",
        host="127.0.0.1",  # Forces TCP instead of Unix Socket
        port=3306,
        database="credit_card_vault"
    )
    print("Success! Connected to MariaDB.")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")

cursor = db_conn.cursor()

# Setup TCP Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # FIX: Allow immediate reuse of the port
server.bind(('localhost', 65432))
server.listen()

while True:
    print("\nWaiting for data...")
    client_sock, addr = server.accept()
    
    # Receive data: expected format "userid,name,cardnum,cvv,expiry"
    raw_data = client_sock.recv(1024).decode()
    
    try:
        # Split the string by commas
        user_id, name, card_num, cvv, expiry = raw_data.split(',')

        # Updated SQL Query with all fields
        query = """
            INSERT INTO credit_cards (user_id, card_holder_name, card_num_enc, cvv_enc, expiry_date) 
            VALUES (?, ?, AES_ENCRYPT(?, 'verysecretkey'), AES_ENCRYPT(?, 'verysecretkey'), ?)
        """
        
        # Execute with the tuple of variables
        cursor.execute(query, (user_id, name, card_num, cvv, expiry))
        db_conn.commit()
        
        client_sock.send(b"Full record vaulted successfully.")
        print(f"Success: Record added for {name}")

    except ValueError:
        client_sock.send(b"Error: Format must be userid,name,cardnum,cvv,expiry")
        print("Received malformed data.")
    except mariadb.Error as e:
        print(f"Database error: {e}")
        client_sock.send(b"Database insertion failed.")

    client_sock.close()
