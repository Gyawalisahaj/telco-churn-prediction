# 🚀 QUICK REFERENCE CARD

## One-Page Cheat Sheet for Nepal Telco Churn Prediction System

### 🎯 MAIN COMMAND
```bash
python main.py --both
```
Opens Streamlit UI at http://localhost:8501 and API at http://localhost:8000

---

## 🌐 ACCESS POINTS

| Service | URL | Purpose |
|---------|-----|---------|
| **UI** | http://localhost:8501 | Web interface for predictions |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **API ReDoc** | http://localhost:8000/redoc | Alternative API documentation |
| **Health Check** | http://localhost:8000/health | System status |

---

## 📋 COMMAND VARIANTS

```bash
# Both UI and API (default, recommended)
python main.py --both

# UI only
python main.py --ui

# API only
python main.py --api

# API on custom port
python main.py --api --port 9000

# Help
python main.py --help
```

---

## ⚡ QUICK START (Linux/macOS)

```bash
chmod +x quickstart.sh
./quickstart.sh
```

## ⚡ QUICK START (Windows)

```bash
quickstart.bat
```

---

## 🔌 API ENDPOINTS

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check |
| GET | `/health` | Detailed health |
| POST | `/predict` | Single prediction |
| POST | `/batch-predict` | Multiple predictions |
| GET | `/info` | System information |

---

## 📝 API PREDICTION REQUEST

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ram Kumar",
    "gender": "Male",
    "age": 35,
    "num_dependents": 2,
    "estimated_salary": 50000,
    "calls_made": 45,
    "sms_sent": 30,
    "data_used": 1500,
    "tenure_months": 24,
    "province": "Bagmati",
    "provider": "Ncell"
  }'
```

---

## 🎨 UI NAVIGATION

| Page | Features |
|------|----------|
| **Single Prediction** | Form input, visualization, recommendations |
| **Batch Prediction** | CSV upload, bulk processing, stats |
| **Analytics** | Dashboard, charts, metrics |
| **History** | Log, filters, export |

---

## 📊 CSV FORMAT

```csv
name,gender,age,num_dependents,estimated_salary,calls_made,sms_sent,data_used,tenure_months,province,provider
Ram Kumar,Male,35,2,50000,45,30,1500,24,Bagmati,Ncell
```

---

## 🇳🇵 VALID VALUES

**Provinces:**
Bagmati, Gandaki, Karnali, Koshi, Lumbini, Madhesh, Sudurpashchim

**Providers:**
Ncell, Nepal Telecom

**Gender:**
Male, Female

---

## 📚 DOCUMENTATION FILES

| File | Read For |
|------|----------|
| QUICKSTART_GUIDE.md | Getting started (5 min) |
| APP_README.md | Full documentation |
| IMPLEMENTATION_SUMMARY.md | Architecture details |
| DEPLOYMENT_CHECKLIST.md | Testing (25-point list) |
| PROJECT_INDEX.md | File reference |

---

## 🐳 DOCKER

```bash
# Build & run
docker-compose up --build

# Or manually
docker build -t churn-predictor .
docker run -p 8000:8000 -p 8501:8501 churn-predictor
```

---

## ⚙️ CONFIGURATION

See `config.ini` for:
- API settings (host, port)
- Model paths
- Risk thresholds
- Feature definitions

---

## 🔐 VALID RANGES

| Field | Min | Max |
|-------|-----|-----|
| age | 18 | 100 |
| num_dependents | 0 | 10 |
| tenure_months | 0 | 72 |
| estimated_salary | 0 | ∞ |
| calls_made | 0 | ∞ |
| sms_sent | 0 | ∞ |
| data_used | 0 | ∞ |

---

## 📊 PREDICTION OUTPUT

```json
{
  "customer_name": "Ram Kumar",
  "churn_prediction": "RETAIN",
  "churn_probability": 42.5,
  "risk_level": "MEDIUM",
  "recommendations": [
    "📉 Low engagement detected...",
    "💰 Consider affordable plans..."
  ]
}
```

---

## ⏱️ PERFORMANCE

- Single prediction: **<100ms**
- Batch (100 customers): **<2s**
- Model load: **<3s**

---

## 🆘 TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| Port in use | `python main.py --api --port 9000` |
| Module not found | `pip install -r requirements.txt` |
| Model not found | Uses fallback model automatically |
| Connection refused | Run `python main.py --both` |

---

## 📞 QUICK HELP

| Need | Location |
|------|----------|
| Installation | QUICKSTART_GUIDE.md |
| API details | APP_README.md |
| Architecture | IMPLEMENTATION_SUMMARY.md |
| Tests | DEPLOYMENT_CHECKLIST.md |
| Files | PROJECT_INDEX.md |
| Errors | DEPLOYMENT_CHECKLIST.md > Troubleshooting |

---

## ✅ VERIFICATION

Verify working:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "model_loaded": true, "version": "1.0.0"}
```

---

## 🎯 COMMON TASKS

**Make single prediction:**
1. Open http://localhost:8501
2. Fill form
3. Click "Predict Churn Risk"
4. View results & recommendations

**Batch process:**
1. Prepare CSV file
2. Open Batch Prediction
3. Upload CSV
4. Click "Predict All Customers"
5. Download results

**View analytics:**
1. Make some predictions
2. Go to Analytics Dashboard
3. View charts and metrics

**Check API:**
1. Visit http://localhost:8000/docs
2. Use Swagger UI
3. Try endpoints

---

## 🚀 STARTUP CHECKLIST

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Run `python main.py --both`
- [ ] Wait 3-5 seconds
- [ ] UI opens in browser
- [ ] API responds at /health
- [ ] Make test prediction
- [ ] Download test results

---

## 📌 KEY FILES

```
src/ui.py           → Streamlit web interface (505 lines)
src/model.py        → FastAPI REST API (216 lines)
src/model_service.py → ML service layer (242 lines)
src/predmodel.py    → Data models (55 lines)
main.py             → Application runner
```

---

## 💡 TIPS

- **Batch processing** is faster for 100+ customers
- **API** is best for integration/automation
- **UI** is best for manual analysis
- **Check health** if issues: `curl http://localhost:8000/health`
- **Export results** for further analysis
- **Read QUICKSTART_GUIDE.md** for detailed steps

---

## 🎓 LEARNING PATH

1. Read this card (1 min)
2. Run `python main.py --both` (1 min)
3. Make 1-2 test predictions (2 min)
4. Try batch upload (2 min)
5. Check API docs (2 min)
6. Read QUICKSTART_GUIDE.md (5 min)

**Total: 13 minutes to get started**

---

## 📞 SUPPORT

- **Setup issues**: QUICKSTART_GUIDE.md
- **API questions**: APP_README.md
- **Architecture**: IMPLEMENTATION_SUMMARY.md
- **Testing**: DEPLOYMENT_CHECKLIST.md
- **File reference**: PROJECT_INDEX.md

---

**Version:** 1.0.0 | **Status:** Production Ready ✅

**Remember:** Start with `python main.py --both` 🚀
