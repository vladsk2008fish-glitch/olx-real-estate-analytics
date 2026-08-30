# Łódź Real Estate Data & Analytics Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon%20Cloud-4169E1?style=flat&logo=postgresql&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-Core-FF694B?style=flat&logo=dbt&logoColor=white)
![Lightdash](https://img.shields.io/badge/Lightdash-BI-C8F7C5?style=flat)
![Git](https://img.shields.io/badge/Git-GitHub-181717?style=flat&logo=github&logoColor=white)

End-to-end data pipeline for collecting, storing, transforming, and visualizing real estate rental market data in Łódź, Poland.

This project demonstrates an automated ETL (Extract, Transform, Load) workflow with cloud integration (Neon PostgreSQL Cloud), data modeling using **dbt Core**, and visual exploratory analytics via an interactive **Lightdash** BI dashboard.

---

## 🏗 Architecture & Data Flow

```mermaid
graph TD
    A[OLX Web Scraper - Requests / BeautifulSoup] -->|Raw Payload| B[Neon Cloud PostgreSQL]
    B -->|Transformation & Outlier Cleaning| C[dbt Core Models]
    C -->|Semantic Layer & Metrics| D[Lightdash BI Engine]
    D -->|Interactive Charts & KPIs| E[Rental Market Dashboard]