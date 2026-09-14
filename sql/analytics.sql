USE radancy_ads;


-- 1. Overall advertising performance

SELECT
    SUM(impressions) AS impressions,
    SUM(clicks) AS clicks,
    SUM(spend) AS spend,
    SUM(conversions) AS conversions,
    SUM(assists) AS assists
FROM fact_ad_performance;


-- 2. Campaign performance

SELECT
    c.campaign_name,
    SUM(f.impressions) AS impressions,
    SUM(f.clicks) AS clicks,
    SUM(f.spend) AS spend,
    SUM(f.conversions) AS conversions
FROM fact_ad_performance f
JOIN dim_ad a
    ON f.ad_key = a.ad_key
JOIN dim_campaign c
    ON a.campaign_key = c.campaign_key
GROUP BY c.campaign_key, c.campaign_name
ORDER BY spend DESC;


-- 3. Click-through rate by campaign

SELECT
    c.campaign_name,

    SUM(f.clicks) * 100.0
        / NULLIF(SUM(f.impressions), 0) AS ctr

FROM fact_ad_performance f
JOIN dim_ad a
    ON f.ad_key = a.ad_key
JOIN dim_campaign c
    ON a.campaign_key = c.campaign_key

GROUP BY c.campaign_key, c.campaign_name

ORDER BY ctr DESC;


-- 4. Conversion rate by campaign

SELECT
    c.campaign_name,

    SUM(f.conversions) * 100.0
        / NULLIF(SUM(f.clicks), 0) AS conversion_rate

FROM fact_ad_performance f
JOIN dim_ad a
    ON f.ad_key = a.ad_key
JOIN dim_campaign c
    ON a.campaign_key = c.campaign_key

GROUP BY c.campaign_key, c.campaign_name

ORDER BY conversion_rate DESC;


-- 5. Spend by device

SELECT
    device_type,
    SUM(spend) AS total_spend,
    SUM(clicks) AS clicks,
    SUM(conversions) AS conversions

FROM fact_ad_performance

GROUP BY device_type

ORDER BY total_spend DESC;