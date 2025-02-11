# 🚀 **Hacktiv8 - Milestone 3 Project**
**by Verren Monica**  
**Phase 2 | Batch: RMT-038**  

## 📌 **Project Overview**  
This project automates the **Extract, Transform, and Load (ETL) process** using **Apache Airflow**. The pipeline extracts sales data from **PostgreSQL**, cleans and processes it, then loads it into **Elasticsearch**. The data is then visualized in **Kibana** to generate insights into:  

📊 **Product category preferences**  
🛍️ **Customer behavior**  
⭐ **Shopping experience evaluations**  

These insights will help **Supermarket ABC** formulate strategic recommendations to **boost sales and remain competitive** against e-commerce.  

## 📖 **Background**  
Based on the sources I read, the trend of online shopping is currently experiencing rapid growth. The development of **e-commerce**, which offers the convenience of shopping from home, has become a significant concern for **supermarkets** to continuously improve their services and remain competitive.  

To stay ahead, supermarkets must understand key factors such as **customer behavior and sales trends** to refine their business strategies. By conducting this analysis, **valuable insights** can be obtained to support **data-driven decisions** that promote **business sustainability**.  

## 🎯 **Objectives**  
As a **Data Analyst at Supermarket ABC**, my goal is to prepare a **comprehensive report** that provides insights into:  
✔️ **Product category preferences**  
✔️ **Customer behavior**  
✔️ **Shopping experience evaluations**  

Additionally, I will provide **strategic recommendations** based on the findings to **increase sales and profits**, ensuring **Supermarket ABC can sustain and compete amidst intense competition from e-commerce**.  

## 📂 **Dataset Source**  
📌 [Dataset Link](https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales/data))

## ⚙️ **ETL Process (Airflow DAG)**  
This ETL process is designed to **automate data transfer from PostgreSQL to Elasticsearch**. The dataset contains **3 months of sales data** from Supermarket ABC.  
🔹 **Step 1: Fetch from PostgreSQL** – Extracts data and saves it as a `.csv` file.  
🔹 **Step 2: Data Cleaning** – Removes duplicates, normalizes column names, handles missing values, and adjusts date formats.  
🔹 **Step 3: Post to Elasticsearch** – Uploads the cleaned data for indexing and visualization.  

### 🏗 **Technology Stack**  
✅ **Docker** – Containerized the entire pipeline for seamless execution.  
✅ **Apache Airflow** – Orchestrates the ETL workflow.  
✅ **PostgreSQL** – Stores raw sales data.  
✅ **Elasticsearch** – Stores processed data for querying and visualization.  
✅ **Kibana** – Creates dashboards and visual reports.  
✅ **Great Expectations** – Ensures data quality before ingestion.  

## 📜 **Scripts**  
📌 **[P2M3_verrenmonica_DAG.py](P2M3_verrenmonica_DAG.py)** – Python script defining the **Airflow DAG** for the ETL process.  

## 📊 **Notebooks**  
📌 **[P2M3_verrenmonica_GX.ipynb](P2M3_verrenmonica_GX.ipynb)** – Performs **data validation** on the cleaned dataset using **Great Expectations (GX)** to ensure data integrity before ingestion into Elasticsearch.  

## 📌 **Conclusion & Business Impact**  
✅ **Automated ETL workflow**, reducing manual data processing efforts.  
✅ **High-quality data validation** using Great Expectations.  
✅ **Actionable insights from sales data**, enabling better decision-making for Supermarket ABC.  
✅ **Improved competitive edge** by leveraging data-driven strategies.  

## 🔗 **Let's Connect!**  
💼 [LinkedIn](https://www.linkedin.com/in/verren-monica/) 

### ✨ **Changes & Improvements:**  
✔ **Pisahkan DAG ke bagian "Scripts"** karena itu file **Python script (`.py`)**, bukan notebook.  
✔ **Buat bagian "Notebooks" khusus untuk Great Expectations** agar lebih rapi.  
✔ **Tetap menjaga flow yang profesional dan engaging.**  

Ini sudah clean & sesuai dengan workflow-mu. 🚀 Mau ada tambahan lagi? 😊
