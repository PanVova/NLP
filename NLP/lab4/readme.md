# CommonLit ETL Project

This project demonstrates a full machine learning pipeline deployment using Docker Compose, FastAPI, PostgreSQL, and Apache Airflow. The task is based on a BERT-based regression model trained on the CommonLit Readability dataset.

## 🔧 Project Structure
```
lab4/
├── docker-compose.yml
├── db/
│   └── init.sql
├── api/
│   ├── app.py
│   ├── Dockerfile
│   └── model.pt
├── airflow/
│   └── dags/
│       └── commonlit_etl.py
```

## 🚀 How to Run

### 1. Clone or unpack the project
```bash
cd lab4
```

### 2. Build and run everything with Docker Compose
```bash
docker-compose up --build
```

This will launch:
- PostgreSQL database on `localhost:5432`
- FastAPI server on `http://localhost:8000/docs`
- Airflow UI on `http://localhost:8080`

### 3. Access Airflow
1. Go to: [http://localhost:8080](http://localhost:8080)
2. Login with:
   - **Username**: `airuser`
   - **Password**: `123456`

### 4. Insert a text into the input table
```bash
docker exec -it lab4-db-1 psql -U user -d commonlit
```
Then inside the prompt:
```sql
INSERT INTO input_texts (text) VALUES ('This is a test passage about physics and comprehension.');
\q
```

### 5. Trigger the ETL DAG
- In Airflow UI, enable and run the DAG named `commonlit_etl`

### 6. Check the output
```bash
docker exec -it lab4-db-1 psql -U user -d commonlit
```
```sql
SELECT * FROM predicted_scores;
```

---

## 🧠 Task Summary

- **Input**: Table `input_texts` with text passages.
- **Model**: BERT-based regressor from lab1_commonlit.
- **API**: FastAPI exposes a `/predict` endpoint.
- **ETL**: Airflow extracts inputs, gets predictions from API, and stores results in `predicted_scores`.

---

## 📌 Requirements
- Docker
- Docker Compose
- Internet access (for first-time image & model downloading)

## ✅ Done
- [x] PostgreSQL setup with init script
- [x] FastAPI service with model loading
- [x] Dockerized environment
- [x] Airflow DAG for ETL

---

Lab4:
https://docs.google.com/document/d/1lg3JM6Hu6Lv--V3JKvCAp8QmayIPs-YrJpQUyJ6TqZI/edit?tab=t.0#heading=h.rs6ljfya5d6