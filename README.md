**# Radancy Data Engineering Take-Home Challenge**



**## 1. Overview**



**This project implements a Python-based data pipeline using Apache Airflow to process the supplied `BING\_MultiDays.csv` Bing Ads dataset.**



**The pipeline performs the following steps:**



**1. Loads the raw CSV data into a MySQL staging table.**

**2. Applies data quality checks.**

**3. Separates valid and rejected records.**

**4. Loads validated data into an analytics-friendly warehouse model.**

**5. Provides SQL queries for downstream analytics.**

**6. Uses Apache Airflow to orchestrate the complete workflow.**



**The solution is designed to provide traceability from the original source data through validation and into the final warehouse tables.**



**---**



**## 2. Technology Stack**



**- Python**

**- Apache Airflow 3.3.1**

**- MySQL**

**- SQL**

**- Docker**

**- Docker Compose**

**- Pytest**



**---**



**## 3. Architecture**



**The pipeline is organized into three main processing stages.**



**```text**

**BING\_MultiDays.csv**

&#x20;       **|**

&#x20;       **v**

**load\_staging.py**

&#x20;       **|**

&#x20;       **v**

**stg\_bing\_ads**

&#x20;       **|**

&#x20;       **v**

**quality\_check.py**

&#x20;       **|**

&#x20;       **+----------------------------+**

&#x20;       **|                            |**

&#x20;       **v                            v**

**curated\_bing\_ads             rejected\_bing\_ads**

&#x20;       **|                            |**

&#x20;       **|                            v**

&#x20;       **|                   data\_quality\_results**

&#x20;       **|**

&#x20;       **v**

**load\_warehouse.py**

&#x20;       **|**

&#x20;       **+------------------+**

&#x20;       **|                  |**

&#x20;       **v                  v**

&#x20; **dim\_campaign         dim\_ad**

&#x20;       **\\                  /**

&#x20;        **\\                /**

&#x20;         **v              v**

&#x20;       **fact\_ad\_performance**



**### Configure Database Credentials**



**The project uses MySQL for the warehouse.**



**Before starting the pipeline, update `docker-compose.yml` with your local MySQL credentials:**



**```yaml**

**DB\_USER: "your\_mysql\_username"**

**DB\_PASSWORD: "your\_mysql\_password"**

**DB\_NAME: "radancy\_ads"**

