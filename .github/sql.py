import pandas as pd
import psycopg2
 
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "customer_segmentation",
    "user": "corneleaa",
    "password": "kornachka123",
}
 
def query(sql, title=None):
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    if title:
        print(f"\n{'='*55}")
        print(f"  {title}")
        print('='*55)
    print(df.to_string(index=False))
    return df
 
 
def run_analysis():
 
    # 1.Klientų skaičius pagal segmentą
    query("""
        SELECT
            c.segmentation                          AS segmentas,
            s.segment_name                          AS pavadinimas,
            COUNT(*)                                AS klientu_sk,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS procentai
        FROM customers c
        JOIN segments s ON c.segmentation = s.segment_code
        WHERE c.segmentation IS NOT NULL
        GROUP BY c.segmentation, s.segment_name
        ORDER BY klientu_sk DESC;
    """, "1. Klientų pasiskirstymas pagal segmentą")
 
    # 2. Vidutinis amžius ir darbo patirtis pagal segmentą
    query("""
        SELECT
            segmentation                                        AS segmentas,
            ROUND(AVG(age)::numeric, 1)                         AS vid_amzius,
            ROUND(AVG(work_experience)::numeric, 1)             AS vid_darbo_patirtis,
            ROUND(AVG(family_size)::numeric, 1)                 AS vid_seimos_dydis
        FROM customers
        WHERE segmentation IS NOT NULL
        GROUP BY segmentation
        ORDER BY segmentation;
    """, "2. Demografiniai vidurkiai pagal segmentą")
 
    # 3. Išlaidų pasiskirstymas pagal segmentą
    query("""
        SELECT
            segmentation    AS segmentas,
            spending_score  AS islaidu_lygis,
            COUNT(*)        AS kiekis
        FROM customers
        WHERE segmentation IS NOT NULL
        GROUP BY segmentation, spending_score
        ORDER BY segmentation, kiekis DESC;
    """, "3. Išlaidų lygis pagal segmentą")
 
    # 4. Top profesijos kiekviename segmente
    query("""
        SELECT
            segmentation    AS segmentas,
            profession      AS profesija,
            COUNT(*)        AS kiekis
        FROM customers
        WHERE segmentation IS NOT NULL
          AND profession IS NOT NULL
        GROUP BY segmentation, profession
        ORDER BY segmentation, kiekis DESC
        LIMIT 16;
    """, "4. Populiariausios profesijos pagal segmentą")
 
    # 5. Lyčių pasiskirstymas
    query("""
        SELECT
            segmentation    AS segmentas,
            gender          AS lytis,
            COUNT(*)        AS kiekis,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY segmentation), 1) AS procentai
        FROM customers
        WHERE segmentation IS NOT NULL
        GROUP BY segmentation, gender
        ORDER BY segmentation, kiekis DESC;
    """, "5. Lyčių pasiskirstymas pagal segmentą")
 
    # 6. Vedybinis statusas ir išsilavinimas
    query("""
        SELECT
            segmentation        AS segmentas,
            ever_married        AS susituokes,
            graduated           AS issilavinimas,
            COUNT(*)            AS kiekis
        FROM customers
        WHERE segmentation IS NOT NULL
        GROUP BY segmentation, ever_married, graduated
        ORDER BY segmentation, kiekis DESC;
    """, "6. Vedybinis statusas ir išsilavinimas pagal segmentą")
 
    # 7. Lojalumas
    query("""
        SELECT
            segmentation                                    AS segmentas,
            COUNT(*) FILTER (WHERE work_experience >= 5)   AS patyre_klientai,
            COUNT(*) FILTER (WHERE work_experience < 5)    AS nauji_klientai,
            ROUND(
                COUNT(*) FILTER (WHERE work_experience >= 5) * 100.0 / COUNT(*), 1
            )                                              AS patyre_proc
        FROM customers
        WHERE segmentation IS NOT NULL
          AND work_experience IS NOT NULL
        GROUP BY segmentation
        ORDER BY segmentation;
    """, "7.Patyrę ir nauji klientai")
 
    # 8. Amžiaus grupės pagal segmentą
    query("""
        SELECT
            segmentation AS segmentas,
            CASE
                WHEN age < 25 THEN '18-24 (Gen Z)'
                WHEN age < 35 THEN '25-34 (Millennials)'
                WHEN age < 50 THEN '35-49 (Gen X)'
                ELSE               '50+ (Boomers)'
            END          AS amziaus_grupe,
            COUNT(*)     AS kiekis
        FROM customers
        WHERE segmentation IS NOT NULL
        GROUP BY segmentation, amziaus_grupe
        ORDER BY segmentation, kiekis DESC;
    """, "8. Amžiaus grupės pagal segmentą")
 
 
if __name__ == "__main__":
    run_analysis()
 