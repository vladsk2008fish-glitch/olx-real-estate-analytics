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
## 🏗 Data Pipeline Architecture

```mermaid
graph TD
    A[OLX Web Scraper] -->|Raw CSV| B[Azure Blob Storage]
    B -->|Ingestion & Cleaning| C[Python Processing / dbt]
    C -->|Structured Data| D[PostgreSQL / Azure SQL]
    D -->|Semantic Layer & Analytics| E[Lightdash]