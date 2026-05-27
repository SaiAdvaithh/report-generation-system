# Report Generation System

A FastAPI-based report generation system that creates telemetry and compliance reports using PostgreSQL, InfluxDB, and React.

## Features

* FastAPI backend architecture
* React frontend dashboard
* Telemetry data handling with InfluxDB
* PDF report generation
* CSV export support
* Authentication and role-based access support
* Report templates and charts
* Modular backend structure

## Tech Stack

### Backend

* FastAPI
* PostgreSQL
* InfluxDB
* Python

### Frontend

* React.js
* CSS

## Project Structure

```bash
report-generation-system/
│
├── backend/
│   ├── app/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── repository/
│   │   ├── services/
│   │   ├── pdf/
│   │   └── templates/
│   ├── simulator/
│   └── main.py
│
├── frontend/
│   └── report-dashboard/
│
└── requirements.txt
```

## Frontend UI

<img width="1163" height="661" alt="Screenshot 2026-05-28 000255" src="https://github.com/user-attachments/assets/51d5b18e-7e6d-4c04-8f9e-af35299125dd" />

The frontend provides a simple report generation dashboard where users can:

* Select report date range
* Enter container and company details
* Upload company logo and signature
* Generate downloadable reports

## Backend Setup

```bash
cd backend
pip install -r ../requirements.txt
uvicorn main:app --reload
```

Backend runs on:

```bash
http://localhost:8000
```

## Frontend Setup

```bash
cd frontend/report-dashboard
npm install
npm start
```

Frontend runs on:

```bash
http://localhost:3000
```

## API Documentation

FastAPI Swagger Docs:

```bash
http://localhost:8000/docs
```

## Future Improvements

* Advanced analytics dashboard
* Better UI styling
* Authentication enhancements
* Docker deployment
* Cloud storage integration
* Real-time telemetry visualization

## Author

N Sai Advaith
