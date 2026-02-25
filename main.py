from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import hashlib
from datetime import datetime

app = FastAPI(
    title="Email Breach Checker API",
    description="Wrapper API for checking email breaches via LeakCheck",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# -------------------------------------------------------
# Auth — simple API key check
# -------------------------------------------------------
API_KEY = os.getenv("API_KEY", "changeme-set-your-own-key")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")
    return key

# -------------------------------------------------------
# LeakCheck Free API
# -------------------------------------------------------
LEAKCHECK_FREE_URL = "https://leakcheck.io/api/public"

def check_leakcheck(email: str) -> dict:
    try:
        resp = requests.get(
            LEAKCHECK_FREE_URL,
            params={"check": email},
            timeout=10,
        )

        if resp.status_code == 200:
            data = resp.json()
            found = data.get("found", False)
            sources = data.get("sources", [])

            return {
                "breached": found,
                "breach_count": len(sources) if found else 0,
                "sources": sources if found else [],
            }

        elif resp.status_code == 429:
            raise HTTPException(status_code=429, detail="LeakCheck rate limit reached. Try again later.")

        else:
            raise HTTPException(status_code=502, detail=f"LeakCheck API error: {resp.status_code}")

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="LeakCheck request timed out.")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Network error: {str(e)}")


# -------------------------------------------------------
# Routes
# -------------------------------------------------------
@app.get("/")
def root():
    return {
        "service": "Email Breach Checker API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "check": "/check?email={email}",
            "health": "/health",
        }
    }


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/check")
def check_email(email: str, api_key: str = Depends(verify_api_key)):
    """
    Check if an email has been in a data breach.

    Returns:
    - breached: true/false
    - breach_count: number of breaches
    - sources: list of breach source names
    """
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Invalid email format.")

    email = email.strip().lower()
    result = check_leakcheck(email)

    return {
        "email": email,
        "breached": result["breached"],
        "breach_count": result["breach_count"],
        "sources": result["sources"],
        "checked_at": datetime.utcnow().isoformat(),
    }