import os

import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "Vaz12511251"),
        database=os.getenv("DB_NAME", "radancy_ads"),
    )


def test_staging_row_count():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM stg_bing_ads")
    count = cursor.fetchone()[0]

    assert count == 12497

    cursor.close()
    connection.close()


def test_rejected_rows():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM rejected_bing_ads")
    rejected_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM data_quality_results")
    issue_count = cursor.fetchone()[0]

    assert rejected_count == 12
    assert issue_count == 12

    cursor.close()
    connection.close()


def test_warehouse_counts():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM dim_campaign")
    campaigns = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM dim_ad")
    ads = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM fact_ad_performance")
    fact_rows = cursor.fetchone()[0]

    assert campaigns == 53
    assert ads == 483
    assert fact_rows == 12485

    cursor.close()
    connection.close()


def test_no_orphan_fact_records():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM fact_ad_performance f
        LEFT JOIN dim_ad a
            ON f.ad_key = a.ad_key
        WHERE a.ad_key IS NULL
        """
    )

    orphan_count = cursor.fetchone()[0]

    assert orphan_count == 0

    cursor.close()
    connection.close()