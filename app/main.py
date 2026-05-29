from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Mini SIEM API")

logs = []
alerts = []


class LogEntry(BaseModel):
    ip_address: str
    username: str
    action: str
    status: str


@app.get("/")
def home():
    return {"message": "Mini SIEM Running"}


@app.post("/logs")
def ingest_log(log: LogEntry):
    log_entry = log.dict()
    log_entry["timestamp"] = str(datetime.now())

    logs.append(log_entry)

    # Simple alert detection
    if log.status.lower() == "failed":
        alerts.append({
            "alert": "Failed Login Attempt",
            "ip": log.ip_address,
            "user": log.username,
            "time": str(datetime.now())
        })

    return {
        "message": "Log received",
        "log": log_entry
    }


@app.get("/logs")
def get_logs():
    return logs


@app.get("/alerts")
def get_alerts():
    return alerts