def transfer_geojson(fname):

    import json
    import os
    import psycopg2

    # Connect to the PostgreSQL database
    print("Connecting to database")

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
        # Check rows of data before insertion
        cur.execute("SELECT COUNT(*) FROM mytable")
        row_count_before = cur.fetchone()[0]

        # Open the GeoJSON file
        with open(os.getenv('f_path') + fname) as f:
            geojson = json.load(f)
        print("Inserting data")
        # Loop over the features in the GeoJSON
        for feature in geojson["features"]:
            # Get the feature's properties and geometry
            properties = feature["properties"]
            geometry = feature["geometry"]

            
            cur.execute(
                "INSERT INTO kasp (properties, geom, id) VALUES (%s, ST_Transform(ST_SetSRID(ST_GeomFromGeoJSON(%s), 5972), 3857), DEFAULT)",
                (json.dumps(properties), json.dumps(geometry))
)
            
            '''
            # Insert the feature into the database
            cur.execute(
                "INSERT INTO mytable (properties, geom) VALUES (%s, ST_Transform(ST_SetSRID(ST_GeomFromGeoJSON(%s), 5972), 3857))",
                (json.dumps(properties), json.dumps(geometry))
            )
            '''
            
        # Commit the changes
        conn.commit()

        # Check if the data was inserted successfully
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM mytable")
        row_count_after = cur.fetchone()[0]
        if row_count_after > row_count_before:
            print("Data was successfully inserted.")
        else:
            print("Data insertion failed.")

    except Exception as e:
        print("Error connecting to database, data was not inserted.")
    finally:
        # Close the cursor and the connection
        if cur:
            cur.close()
        if conn:
            conn.close()

    # Check if the file was transferred correctly and delete it if so
    try:
        print("Deleting the geojson file...")
        os.remove(os.getenv('f_path') + fname)
    except Exception as e:
        print(f"An error occurred while deleting the file: {e}")
    print("Done")