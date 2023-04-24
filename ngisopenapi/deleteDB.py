import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Function to delete all rows from the 'kasp' table
def delete_data():
    # Initialize connection and cursor objects as None
    conn = None
    cur = None
    try:
        # Connect to the PostgreSQL database using environment variables
        conn = psycopg2.connect(
            host=os.getenv('db_host'),
            database=os.getenv('db_name'),
            user=os.getenv('db_user'),
            password=os.getenv('db_pass')
        )

        # Create a cursor object
        cur = conn.cursor()
        # Execute the DELETE query on the 'kasp' table
        cur.execute("DELETE FROM kasp")
        # Commit the changes
        conn.commit()
        print("Data was successfully deleted.")

    except Exception as e:
        print("Error connecting to database")
    finally:
        # Close the cursor and the connection
        if cur:
            cur.close()
        if conn:
            conn.close()

# Call the delete_data function
delete_data()
