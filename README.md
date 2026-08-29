# Łódź Real Estate Data & Analytics Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-Blob%20Storage-0089D6?style=flat&logo=microsoftazure&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat&logo=mysql&logoColor=white)
![Architecture](https://img.shields.io/badge/Clean%20Code-SOLID-brightgreen?style=flat)

End-to-end data pipeline for collecting, storing, and analyzing real estate rental market data in Łódź, Poland. 

This project demonstrates an ETL (Extract, Transform, Load) workflow with cloud integration (Azure Blob Storage), relational database querying using advanced SQL techniques (window functions), and visual exploratory data analysis (EDA).

---

## Architecture & Data Flow

```text
[ Web Scraper / Data Collector ] 
               │
               ▼
   [ Azure Blob Storage ] (Raw Data Lake Layer)
               │
               ▼
   [ Python Data Processing ] (Pandas / NumPy / Clean Architecture)
               │
               ▼
   [ MySQL Database ] (Processed Relational Storage)
               │
               ▼ (Window Functions, Aggregations)
[ EDA & Data Analytics ] (Seaborn / Plotly / SQL Queries)