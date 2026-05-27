# Report Generation System

A container report generation system built using React and Python for generating telemetry-based reports with company details, uploaded logos, signatures, and compliance information.

## Features

* Generate container reports using selected date ranges
* Upload company logo and signature
* Telemetry-based report generation
* PDF report creation
* Compliance and statistics calculation
* Modular backend architecture
* Interactive React frontend

## Tech Stack

### Frontend

* React.js
* Axios
* React Signature Canvas
* CSS

### Backend

* Python
* FastAPI
* InfluxDB
* ReportLab / PDF utilities
* CORS Middleware

## Project Structure

```bash
report-generation-system/
│
├── backend/
│   ├── app/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── pdf/
│   │   ├── repository/
│   │   ├── services/
│   │   ├── simulator/
│   │   └── templates/
│   └── main.py
│
├── frontend/
│   └── report-dashboard/
│
└── requirements.txt
```

## Frontend Dashboard

<img width="1163" height="661" alt="Screenshot 2026-05-28 000255" src="https://github.com/user-attachments/assets/51d5b18e-7e6d-4c04-8f9e-af35299125dd" />

The frontend dashboard allows users to:

* Select report date range
* Enter company and facility details
* Add auditor, reviewer, and approver information
* Upload logo and signature files
* Generate downloadable reports

## Running the Frontend

```bash
cd frontend/report-dashboard
npm install
npm start
```

Frontend runs at:

```bash
http://localhost:3000
```

## Running the Backend

```bash
cd backend
uvicorn main:app --reload
```

Backend runs at:

```bash
http://localhost:8000
```

```

## Future Improvements

- Improved dashboard UI
- Real-time telemetry visualization
- Authentication system
- Docker deployment
- Cloud integration

## Author

N Sai Advaith

```

