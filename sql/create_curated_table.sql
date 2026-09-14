USE radancy_ads;

DROP TABLE IF EXISTS data_quality_results;
DROP TABLE IF EXISTS rejected_bing_ads;
DROP TABLE IF EXISTS curated_bing_ads;


CREATE TABLE curated_bing_ads (
    `Date` DATE,
    `Customer` VARCHAR(255),
    `Account number` VARCHAR(100),
    `Account name` VARCHAR(255),
    `Account status` VARCHAR(100),
    `Campaign name` VARCHAR(255),
    `Campaign status` VARCHAR(100),
    `Ad group ID` VARCHAR(100),
    `Ad group` VARCHAR(255),
    `Ad group status` VARCHAR(100),
    `Ad ID` VARCHAR(100),
    `Ad description` TEXT,
    `Ad distribution` VARCHAR(100),
    `Ad status` VARCHAR(100),
    `Ad title` TEXT,
    `Ad type` VARCHAR(100),
    `Tracking Template` TEXT,
    `Custom Parameters` TEXT,
    `Final Mobile URL` TEXT,
    `Final URL` TEXT,
    `Top vs. other` VARCHAR(100),
    `Display URL` TEXT,
    `Final App URL` TEXT,
    `Destination URL` TEXT,
    `Device type` VARCHAR(100),
    `Device OS` VARCHAR(100),
    `Delivered match type` VARCHAR(100),
    `BidMatchType` VARCHAR(100),
    `Language` VARCHAR(100),
    `Network` VARCHAR(100),
    `Currency code` VARCHAR(20),
    `Impressions` INT,
    `Clicks` INT,
    `Spend` DECIMAL(18,4),
    `Avg. position` DECIMAL(10,4),
    `Conversions` DECIMAL(18,4),
    `Assists` DECIMAL(18,4),
    `source_row_number` INT
);


CREATE TABLE rejected_bing_ads (
    `Date` DATE,
    `Customer` VARCHAR(255),
    `Account number` VARCHAR(100),
    `Account name` VARCHAR(255),
    `Account status` VARCHAR(100),
    `Campaign name` VARCHAR(255),
    `Campaign status` VARCHAR(100),
    `Ad group ID` VARCHAR(100),
    `Ad group` VARCHAR(255),
    `Ad group status` VARCHAR(100),
    `Ad ID` VARCHAR(100),
    `Ad description` TEXT,
    `Ad distribution` VARCHAR(100),
    `Ad status` VARCHAR(100),
    `Ad title` TEXT,
    `Ad type` VARCHAR(100),
    `Tracking Template` TEXT,
    `Custom Parameters` TEXT,
    `Final Mobile URL` TEXT,
    `Final URL` TEXT,
    `Top vs. other` VARCHAR(100),
    `Display URL` TEXT,
    `Final App URL` TEXT,
    `Destination URL` TEXT,
    `Device type` VARCHAR(100),
    `Device OS` VARCHAR(100),
    `Delivered match type` VARCHAR(100),
    `BidMatchType` VARCHAR(100),
    `Language` VARCHAR(100),
    `Network` VARCHAR(100),
    `Currency code` VARCHAR(20),
    `Impressions` INT,
    `Clicks` INT,
    `Spend` DECIMAL(18,4),
    `Avg. position` DECIMAL(10,4),
    `Conversions` DECIMAL(18,4),
    `Assists` DECIMAL(18,4),
    `source_row_number` INT
);


CREATE TABLE data_quality_results (
    `quality_id` INT AUTO_INCREMENT PRIMARY KEY,
    `source_row_number` INT NOT NULL,
    `check_name` VARCHAR(255) NOT NULL,
    `failure_reason` TEXT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
