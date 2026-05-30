import pandas as pd
import psycopg2
from psycopg2 import sql

#Configurations
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "customer_segmentation",
    "user": "sensitive information, type yours",
    "password": "sensitive information, type yours",
}

#Logins
def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def setup_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id              INTEGER PRIMARY KEY,
            gender          VARCHAR(10),
            ever_married    VARCHAR(5),
            age             INTEGER,
            graduated       VARCHAR(5),
            profession      VARCHAR(50),
            work_experience FLOAT,
            spending_score  VARCHAR(10),
            family_size     FLOAT,
            var_1           VARCHAR(20),
            segmentation    VARCHAR(5)   
        );
    """)

    # segmentation description
    cur.execute("""
        CREATE TABLE IF NOT EXISTS segments (
            segment_code    VARCHAR(5) PRIMARY KEY,
            segment_name    VARCHAR(50),
            description     TEXT
        );
    """)

    cur.execute("""
        INSERT INTO segments VALUES
            ('A', 'Premium',    'Aukštos vertės klientai – didelės pajamos, aktyvūs pirkėjai'),
            ('B', 'Established','Stabili grupė – vidutinės pajamos, reguliarūs pirkimai'),
            ('C', 'Potential',  'Augimo potencialas – jauni, dar formuojasi įpročiai'),
            ('D', 'Budget',     'Taupūs klientai – žemos išlaidos, jautrūs kainai')
        ON CONFLICT DO NOTHING;
    """)

    conn.commit()

    #Data uploading
    train = pd.read_csv("train.csv")
    test  = pd.read_csv("test.csv")

    # Suvienodinti stulpeliai
    test["Segmentation"] = None

    df = pd.concat([train, test], ignore_index=True)
    df.columns = [c.lower() for c in df.columns]
    df = df.drop_duplicates(subset="id")

    # delete of the old entry
    cur.execute("TRUNCATE customers;")

    inserted = 0
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO customers
                (id, gender, ever_married, age, graduated, profession,
                 work_experience, spending_score, family_size, var_1, segmentation)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (id) DO NOTHING;
        """, (
            int(row["id"]),
            row["gender"]          if pd.notna(row["gender"])          else None,
            row["ever_married"]    if pd.notna(row["ever_married"])    else None,
            int(row["age"])        if pd.notna(row["age"])             else None,
            row["graduated"]       if pd.notna(row["graduated"])       else None,
            row["profession"]      if pd.notna(row["profession"])      else None,
            float(row["work_experience"]) if pd.notna(row["work_experience"]) else None,
            row["spending_score"]  if pd.notna(row["spending_score"])  else None,
            float(row["family_size"]) if pd.notna(row["family_size"]) else None,
            row["var_1"]           if pd.notna(row["var_1"])           else None,
            row["segmentation"]    if pd.notna(row["segmentation"])    else None,
        ))
        inserted += 1

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    setup_database()
