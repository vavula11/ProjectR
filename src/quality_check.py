import os

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

METRIC_COLUMNS = [
    "Impressions",
    "Clicks",
    "Spend",
    "Conversions",
    "Assists",
]

REQUIRED_COLUMNS = [
    "Date",
    "Customer",
    "Account number",
    "Campaign name",
    "Ad group ID",
    "Ad ID",
]


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "your_mysql_password"),
        database=os.getenv("DB_NAME", "radancy_ads"),
    )


def is_empty(value):
    return value is None or str(value).strip() == ""


def validate_row(row):
    issues = []

    for column in REQUIRED_COLUMNS:
        if is_empty(row[column]):
            issues.append(f"{column} is missing")

    for column in METRIC_COLUMNS:
        value = row[column]

        if value is None:
            continue

        if value < 0:
            issues.append(f"{column} cannot be negative")

    impressions = row["Impressions"]
    clicks = row["Clicks"]
    conversions = row["Conversions"]

    if impressions is not None and clicks is not None:
        if clicks > impressions:
            issues.append("Clicks cannot be greater than Impressions")

    if clicks is not None and conversions is not None:
        if conversions > clicks:
            issues.append("Conversions cannot be greater than Clicks")

    return issues


def quality_check():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    insert_columns = SOURCE_COLUMNS + ["source_row_number"]

    try:
        cursor.execute("DELETE FROM curated_bing_ads")
        cursor.execute("DELETE FROM rejected_bing_ads")
        cursor.execute("DELETE FROM data_quality_results")
        connection.commit()

        cursor.execute(
            """
            SELECT *
            FROM stg_bing_ads
            ORDER BY source_row_number
            """
        )

        rows = cursor.fetchall()

        rejected_rows = []
        valid_rows = []
        quality_results = []

        for row in rows:
            issues = validate_row(row)

            row_values = tuple(
                row[column] for column in insert_columns
            )

            if issues:
                rejected_rows.append(row_values)

                quality_results.append(
                    (
                        row["source_row_number"],
                        "Business/Required Field Validation",
                        "; ".join(issues),
                    )
                )
            else:
                valid_rows.append(row_values)

        column_names = ", ".join(
            f"`{column}`" for column in insert_columns
        )

        placeholders = ", ".join(
            ["%s"] * len(insert_columns)
        )

        curated_sql = f"""
            INSERT INTO curated_bing_ads ({column_names})
            VALUES ({placeholders})
        """

        rejected_sql = f"""
            INSERT INTO rejected_bing_ads ({column_names})
            VALUES ({placeholders})
        """

        quality_sql = """
            INSERT INTO data_quality_results (
                source_row_number,
                check_name,
                failure_reason
            )
            VALUES (%s, %s, %s)
        """

        if valid_rows:
            cursor.executemany(
                curated_sql,
                valid_rows
            )

        if rejected_rows:
            cursor.executemany(
                rejected_sql,
                rejected_rows
            )

        if quality_results:
            cursor.executemany(
                quality_sql,
                quality_results
            )

        connection.commit()

        print(f"Total staging rows: {len(rows)}")
        print(f"Valid rows: {len(valid_rows)}")
        print(f"Rejected rows: {len(rejected_rows)}")

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    quality_check()
