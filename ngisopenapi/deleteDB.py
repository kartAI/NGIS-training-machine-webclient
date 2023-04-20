import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def delete_data():
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            host=os.getenv('db_host'),
            database=os.getenv('db_name'),
            user=os.getenv('db_user'),
            password=os.getenv('db_pass')
        )

        cur = conn.cursor()
        cur.execute("DELETE FROM kasp")
        conn.commit()
        print("Data was successfully deleted.")

    except Exception as e:
        print(f"Error connecting to database: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

delete_data()
