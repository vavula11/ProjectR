import csv
import os
from datetime import datetime

import mysql.connector


SOURCE_COLUMNS = [
    "Date",
    "Customer",
    "Account number",
    "Account name",
    "Account status",
    "Campaign name",
    "Campaign status",
    "Ad group ID",
    "Ad group",
    "Ad group status",
    "Ad ID",
    "Ad description",
    "Ad distribution",
    "Ad status",
    "Ad title",
    "Ad type",
    "Tracking Template",
    "Custom Parameters",
    "Final Mobile URL",
    "Final URL",
    "Top vs. other",
    "Display URL",
    "Final App URL",
    "Destination URL",
    "Device type",
    "Device OS",
    "Delivered match type",
    "BidMatchType",
    "Language",
    "Network",
    "Currency code",
    "Impressions",
    "Clicks",
    "Spend",
    "Avg. position",
    "Conversions",
    "Assists",
]


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "Vaz12511251"),
        database=os.getenv("DB_NAME", "radancy_ads"),
    )


def clean_value(value):
    if value is None:
        return None

    value = value.strip()

    if value == "":
        return None

    return value


def load_staging():
    file_path = os.getenv(
        "SOURCE_FILE",
        "/opt/airflow/data/BING_MultiDays.csv"
    )

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM stg_bing_ads")
        connection.commit()

        insert_columns = SOURCE_COLUMNS + ["source_row_number"]

        column_names = ", ".join(
            f"`{column}`" for column in insert_columns
        )

        placeholders = ", ".join(["%s"] * len(insert_columns))

        insert_sql = f"""
            INSERT INTO stg_bing_ads ({column_names})
            VALUES ({placeholders})
        """

        rows_to_insert = []

        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            for row_number, row in enumerate(reader, start=2):
                values = []

                for column in SOURCE_COLUMNS:
                    value = clean_value(row.get(column))

                    if column == "Date" and value is not None:
                        value = datetime.strptime(
                            value,
                            "%m/%d/%Y"
                        ).date()

                    values.append(value)

                values.append(row_number)

                rows_to_insert.append(tuple(values))

        cursor.executemany(insert_sql, rows_to_insert)
        connection.commit()

        print(f"Loaded {len(rows_to_insert)} rows into stg_bing_ads.")

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    load_staging()