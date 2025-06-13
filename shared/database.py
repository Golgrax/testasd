import mysql.connector
import hashlib

# --- IMPORTANT: CONFIGURE YOUR DATABASE CONNECTION HERE ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Test1234!',
    'database': 'pup_shop'
}
# ---------------------------------------------------------

def get_db_connection():
    """Establishes a connection to the database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def hash_password(password):
    """Hashes a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def initialize_database():
    """Creates tables if they don't exist and populates with initial data."""
    conn = get_db_connection()
    if not conn:
        print("Could not initialize database. Connection failed.")
        return

    cursor = conn.cursor()
    
    # --- Table Definitions ---
    tables = {}
    tables['users'] = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            address1 TEXT,
            address2 TEXT,
            contact_no1 VARCHAR(50),
            contact_no2 VARCHAR(50)
        ) ENGINE=InnoDB
    """
    
    tables['products'] = """
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            image_url VARCHAR(255),
            stock INT NOT NULL DEFAULT 0,
            sold_count INT NOT NULL DEFAULT 0
        ) ENGINE=InnoDB
    """

    # Add more tables like orders, order_items, cart_items as needed for full functionality

    for table_name, table_description in tables.items():
        try:
            print(f"Creating table {table_name}: ", end='')
            cursor.execute(table_description)
            print("OK")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # --- Initial Data Population (for demonstration) ---
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        print("Populating products table with initial data...")
        products_to_add = [
            ('PUP Minimalist Baybayin Lanyard', 'Coquette style lanyard with Baybayin script.', 140.00, '/static/images/product_lanyard.jpg', 100, 50),
            ('PUP Iskolar TOTE BAG', 'Durable and stylish tote bag for every Iskolar ng Bayan.', 160.00, '/static/images/product_tote.jpg', 150, 25),
            ('PUP Jeepney Signage', 'A decorative replica of the iconic PUP jeepney signage.', 20.00, '/static/images/product_jeepney.jpg', 200, 110),
            ('PUP STUDY WITH STYLE Shirt', 'Premium quality shirt with the Obelisk silhouette.', 450.00, '/static/images/product_shirt.jpg', 80, 15)
        ]
        insert_query = "INSERT INTO products (name, description, price, image_url, stock, sold_count) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.executemany(insert_query, products_to_add)
        conn.commit()
        print("Initial products added.")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    # This allows you to run this file directly to set up the DB
    print("Initializing database schema and data...")
    initialize_database()
    print("Database initialization complete.")