def transfer_geojson(fname):

    import json
    import os
    import psycopg2

# Connect to the PostgreSQL database
    conn = None
    try:
        conn = psycopg2.connect(
            host="postgresql-dev-kartai.postgres.database.azure.com",
            database="kartai_bachelor_2023",
            user="kartai_bachelor_2023@postgresql-dev-kartai",
            password="Io4$7M1e"
        )

    # Open the GeoJSON file
        with open("C:\\temp\\" + fname) as f:
            geojson = json.load(f)

    # Create a cursor
        cur = conn.cursor()

    # Loop over the features in the GeoJSON
        for feature in geojson["features"]:
        # Get the feature's properties and geometry
            properties = feature["properties"]
            geometry = feature["geometry"]

        # Insert the feature into the database
            cur.execute(
            "INSERT INTO mytable (properties, geometry) VALUES (%s, ST_GeomFromGeoJSON(%s))",
                (json.dumps(properties), json.dumps(geometry))
            )

    # Commit the changes
        conn.commit()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
    # Close the cursor and the connection
        if cur:
            cur.close()
        if conn:
            conn.close()

    # Check if the file was transferred correctly and delete it if so
        if conn and conn.closed:
            try:
                os.remove("C:\\temp\\" + fname)
            except Exception as e:
                print(f"An error occurred while deleting the file: {e}")
        print("Done")