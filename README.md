# Email Breach Checker API

Wrapper API for checking email breaches via LeakCheck free tier.
Built with FastAPI, deployable on Railway.

---

## Deploy to Railway (Step by Step)

### Step 1 — Push to GitHub
1. Create a new GitHub repository (e.g. `breach-checker-api`)
2. Push all files in this folder to that repo:
```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/YOUR_USERNAME/breach-checker-api.git
git push -u origin main
```

### Step 2 — Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub account (free)

### Step 3 — Deploy on Railway
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Select your `breach-checker-api` repo
4. Railway will auto-detect Python and deploy

### Step 4 — Set Environment Variable
1. In Railway dashboard, go to your project
2. Click **"Variables"**
3. Add:
   ```
   API_KEY = your-secret-key-here
   ```
   Set this to any secret string you want. Users will need this to call your API.

### Step 5 — Get Your URL
1. Go to **"Settings"** → **"Networking"**
2. Click **"Generate Domain"**
3. You'll get a URL like:
   ```
   https://breach-checker-api-production.up.railway.app
   ```

---

## Your API Details

Once deployed, share these with users:

```
API URL:        https://YOUR-APP.up.railway.app/check?email={email}
API Key Header: X-API-Key
API Key:        (the key you set in Railway Variables)
```

---

## Test Your API

```bash
curl "https://YOUR-APP.up.railway.app/check?email=test@example.com" \
  -H "X-API-Key: your-secret-key-here"
```

Expected response:
```json
{
  "email": "test@example.com",
  "breached": false,
  "breach_count": 0,
  "sources": [],
  "checked_at": "2026-02-25T10:00:00"
}
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| GET | `/check?email={email}` | Check email breach |

---

## Limitations (Free Tier)

- LeakCheck free tier: **100 checks/day** tracked by IP
- For higher volume, upgrade LeakCheck to paid plan

---

## Use in SmartETL Node

In the Email Breach Checker node, select **Custom API** and fill in:

| Field | Value |
|-------|-------|
| API URL | `https://YOUR-APP.up.railway.app/check?email={email}` |
| API Key Header | `X-API-Key` |
| API Key | `your-secret-key-here` |