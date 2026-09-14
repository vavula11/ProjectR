import os

import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "Vaz12511251"),
        database=os.getenv("DB_NAME", "radancy_ads"),
    )


def load_warehouse():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Clear tables in child-to-parent order because of foreign keys.
        cursor.execute("DELETE FROM fact_ad_performance")
        cursor.execute("DELETE FROM dim_ad")
        cursor.execute("DELETE FROM dim_campaign")

        # Load campaign dimension.
        cursor.execute(
            """
            INSERT INTO dim_campaign (
                account_number,
                campaign_name,
                campaign_status
            )
            SELECT
                b.`Account number`,
                b.`Campaign name`,
                MAX(b.`Campaign status`)
            FROM curated_bing_ads b
            GROUP BY
                b.`Account number`,
                b.`Campaign name`
            """
        )

        # Load ad dimension.
        cursor.execute(
            """
            INSERT INTO dim_ad (
                campaign_key,
                ad_group_id,
                ad_group,
                ad_id,
                ad_title,
                ad_type,
                ad_status
            )
            SELECT
                c.campaign_key,
                b.`Ad group ID`,
                MAX(b.`Ad group`),
                b.`Ad ID`,
                MAX(b.`Ad title`),
                MAX(b.`Ad type`),
                MAX(b.`Ad status`)
            FROM curated_bing_ads b
            INNER JOIN dim_campaign c
                ON c.account_number = b.`Account number`
                AND c.campaign_name = b.`Campaign name`
            GROUP BY
                c.campaign_key,
                b.`Ad group ID`,
                b.`Ad ID`
            """
        )

        # Load fact table.
        #
        # Grain:
        # Date + Ad + Device type + Device OS + Network
        # + Delivered match type + BidMatchType + Top vs. other
        cursor.execute(
            """
            INSERT INTO fact_ad_performance (
                date,
                ad_key,
                device_type,
                device_os,
                network,
                delivered_match_type,
                bid_match_type,
                top_vs_other,
                impressions,
                clicks,
                spend,
                avg_position,
                conversions,
                assists
            )
            SELECT
                b.`Date`,
                a.ad_key,
                b.`Device type`,
                b.`Device OS`,
                b.`Network`,
                b.`Delivered match type`,
                b.`BidMatchType`,
                b.`Top vs. other`,
                b.`Impressions`,
                b.`Clicks`,
                b.`Spend`,
                b.`Avg. position`,
                b.`Conversions`,
                b.`Assists`
            FROM curated_bing_ads b
            INNER JOIN dim_campaign c
                ON c.account_number = b.`Account number`
                AND c.campaign_name = b.`Campaign name`
            INNER JOIN dim_ad a
                ON a.campaign_key = c.campaign_key
                AND a.ad_group_id = b.`Ad group ID`
                AND a.ad_id = b.`Ad ID`
            """
        )

        connection.commit()

        cursor.execute("SELECT COUNT(*) FROM dim_campaign")
        campaign_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM dim_ad")
        ad_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM fact_ad_performance")
        fact_count = cursor.fetchone()[0]

        print(f"Campaigns loaded: {campaign_count}")
        print(f"Ads loaded: {ad_count}")
        print(f"Fact rows loaded: {fact_count}")

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    load_warehouse()