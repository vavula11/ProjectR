USE radancy_ads;


-- ---------------------------------------------------------
-- Campaign dimension
-- ---------------------------------------------------------

DROP TABLE IF EXISTS fact_ad_performance;
DROP TABLE IF EXISTS dim_ad;
DROP TABLE IF EXISTS dim_campaign;


CREATE TABLE dim_campaign (
    campaign_key INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(100) NOT NULL,
    campaign_name VARCHAR(255) NOT NULL,
    campaign_status VARCHAR(100),
    UNIQUE KEY uq_campaign (
        account_number,
        campaign_name
    )
);


-- ---------------------------------------------------------
-- Ad dimension
-- ---------------------------------------------------------

CREATE TABLE dim_ad (
    ad_key INT AUTO_INCREMENT PRIMARY KEY,
    campaign_key INT NOT NULL,
    ad_group_id VARCHAR(100),
    ad_group VARCHAR(255),
    ad_id VARCHAR(100),
    ad_title TEXT,
    ad_type VARCHAR(100),
    ad_status VARCHAR(100),
    FOREIGN KEY (campaign_key)
        REFERENCES dim_campaign(campaign_key),

    UNIQUE KEY uq_ad (
        campaign_key,
        ad_group_id,
        ad_id
    )
);


-- ---------------------------------------------------------
-- Advertising performance fact
-- ---------------------------------------------------------

CREATE TABLE fact_ad_performance (
    performance_key BIGINT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    ad_key INT NOT NULL,
    device_type VARCHAR(100),
    device_os VARCHAR(100),
    network VARCHAR(100),
    delivered_match_type VARCHAR(100),
    bid_match_type VARCHAR(100),
    top_vs_other VARCHAR(100),
    impressions INT,
    clicks INT,
    spend DECIMAL(18,4),
    avg_position DECIMAL(10,4),
    conversions DECIMAL(18,4),
    assists DECIMAL(18,4),

    FOREIGN KEY (ad_key)
        REFERENCES dim_ad(ad_key)
);