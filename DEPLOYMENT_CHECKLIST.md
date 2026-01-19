# ✅ Deployment Checklist & Verification Guide

## Pre-Deployment Verification

### 1. Environment Setup
- [ ] Python 3.8+ installed
- [ ] Virtual environment created (`tf_venv`)
- [ ] Virtual environment activated
- [ ] All dependencies installed from `requirements.txt`

**Command to verify:**
```bash
python --version
pip list | grep -E "fastapi|streamlit|tensorflow|pandas"
```

### 2. Project Structure
- [ ] `src/ui.py` exists (506 lines, Streamlit UI)
- [ ] `src/model.py` exists (217 lines, FastAPI backend)
- [ ] `src/model_service.py` exists (340 lines, service layer)
- [ ] `src/predmodel.py` exists (data models)
- [ ] `model/Churnpred_ann.keras` exists
- [ ] `model/scaler.pkl` exists
- [ ] `model/train_columns.pkl` exists
- [ ] `main.py` exists (runner)
- [ ] `requirements.txt` exists
- [ ] `config.ini` exists

**Command to verify:**
```bash
ls -la src/
ls -la model/
ls -la *.py *.txt *.ini *.md
```

### 3. File Integrity

- [ ] `src/ui.py` imports correctly
- [ ] `src/model.py` imports correctly
- [ ] `src/model_service.py` imports correctly
- [ ] No syntax errors in any Python file

**Command to verify:**
```bash
python -m py_compile src/ui.py src/model.py src/model_service.py src/predmodel.py main.py
```

### 4. Dependencies Check

Required packages:
- [ ] pandas (>=2.0.0)
- [ ] numpy (>=1.24.0)
- [ ] tensorflow (>=2.13.0)
- [ ] keras (>=2.13.0)
- [ ] scikit-learn (>=1.3.0)
- [ ] streamlit (>=1.28.0)
- [ ] fastapi (>=0.104.0)
- [ ] uvicorn (>=0.24.0)
- [ ] pydantic (>=2.0.0)
- [ ] plotly (>=5.17.0)
- [ ] joblib (>=1.3.0)

**Command to verify:**
```bash
pip check
```

## Functionality Testing

### 5. Model Service Initialization

**Test command:**
```bash
python -c "from src.model_service import ChurnModelService; ms = ChurnModelService(); print(f'Model Loaded: {ms.model_loaded}')"
```

Expected output:
```
✅ Model loaded successfully...
Model Loaded: True
```

### 6. API Startup

**Test command:**
```bash
python -c "from src.model import app; print('API imports successfully')"
```

Expected output:
```
API imports successfully
```

### 7. Single Prediction Test

**Python test script:**
```python
from src.model_service import ChurnModelService

service = ChurnModelService()
test_customer = {
    "name": "Test Customer",
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
}

result = service.predict(test_customer)
assert result.get("success"), f"Prediction failed: {result}"
print(f"✅ Single prediction works: {result['churn_prediction']}")
```

**Run with:**
```bash
python test_prediction.py
```

### 8. API Endpoint Testing

**Start API:**
```bash
python main.py --api &
```

**Test health endpoint (wait 3 seconds):**
```bash
sleep 3
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

**Test prediction endpoint:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test",
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

Expected response includes:
- `customer_name`: "Test"
- `churn_prediction`: "CHURN" or "RETAIN"
- `churn_probability`: number 0-100
- `risk_level`: "LOW", "MEDIUM", or "HIGH"

### 9. UI Startup Test

**Start UI:**
```bash
streamlit run src/ui.py
```

Expected:
- [ ] Page loads without errors
- [ ] "🇳🇵 Nepal Telco Churn Predictor" title visible
- [ ] Sidebar navigation visible
- [ ] No error messages in terminal

### 10. Navigation Test

In Streamlit UI:
- [ ] "Single Prediction" page loads
- [ ] "Batch Prediction" page loads
- [ ] "Analytics Dashboard" page loads
- [ ] "Prediction History" page loads
- [ ] No errors during navigation

### 11. Single Prediction Form Test

In Streamlit UI - Single Prediction:
- [ ] Can enter customer name
- [ ] Gender dropdown works
- [ ] Age input accepts values
- [ ] Dependents input works
- [ ] Salary input works
- [ ] Tenure slider works
- [ ] Calls/SMS/Data inputs work
- [ ] Province dropdown has all 7 provinces
- [ ] Provider dropdown has both options
- [ ] "Predict Churn Risk" button present
- [ ] Button is enabled

**Test data:**
```
Name: Test Customer
Gender: Male
Age: 35
Dependents: 2
Salary: 50000
Calls: 45
SMS: 30
Data: 1500 MB
Tenure: 24 months
Province: Bagmati
Provider: Ncell
```

Click "Predict Churn Risk" and verify:
- [ ] Shows "✅ Prediction Complete!"
- [ ] Displays prediction result
- [ ] Shows risk gauge chart
- [ ] Shows risk level
- [ ] Shows recommendations
- [ ] Can view profile summary

### 12. Batch Prediction Test

In Streamlit UI - Batch Prediction:
- [ ] File uploader present
- [ ] Can select CSV file
- [ ] "Predict All Customers" button present
- [ ] Shows progress bar during processing
- [ ] Displays results table
- [ ] Shows statistics (total, high-risk, avg risk)
- [ ] Shows comparison chart
- [ ] "Download Results" button works

**Test CSV:** Create `test_batch.csv`:
```csv
name,gender,age,num_dependents,estimated_salary,calls_made,sms_sent,data_used,tenure_months,province,provider
Test1,Male,35,2,50000,45,30,1500,24,Bagmati,Ncell
Test2,Female,28,1,45000,60,50,2000,18,Gandaki,Nepal Telecom
```

### 13. Analytics Dashboard Test

In Streamlit UI - Analytics Dashboard:
- [ ] Shows after making predictions
- [ ] Displays key metrics
- [ ] Shows risk distribution pie chart
- [ ] Shows churn distribution bar chart
- [ ] Shows probability histogram

### 14. Prediction History Test

In Streamlit UI - Prediction History:
- [ ] After predictions, history shows
- [ ] Can filter by risk level
- [ ] Can filter by prediction type
- [ ] Download button works
- [ ] Clear history button works

### 15. Combined Mode Test

**Start both UI and API:**
```bash
python main.py --both
```

Verify:
- [ ] API starts first (terminal shows "Starting API...")
- [ ] UI starts second (opens in browser)
- [ ] Both communicate correctly
- [ ] Can make predictions from UI
- [ ] API logs show requests

## Docker Testing

### 16. Docker Build

```bash
docker build -t telco-churn-predictor .
```

Expected:
- [ ] Build completes without errors
- [ ] Image created successfully
- [ ] Can run `docker images | grep telco`

### 17. Docker Run

```bash
docker run -p 8000:8000 -p 8501:8501 telco-churn-predictor
```

Expected:
- [ ] Container starts
- [ ] Logs show API starting
- [ ] Both ports accessible
- [ ] Can access UI at http://localhost:8501
- [ ] Can access API at http://localhost:8000/docs

### 18. Docker Compose

```bash
docker-compose up
```

Expected:
- [ ] Service starts
- [ ] Health check passes
- [ ] Can make predictions
- [ ] Logs persisted in `logs/` directory
- [ ] Model directory mounted correctly

## Performance Testing

### 19. Single Prediction Speed

**Measure time:**
```bash
time curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","gender":"Male","age":35,...}'
```

Expected: < 200ms total time

### 20. Batch Processing Speed

**Test with 100 customers:**
- [ ] Completes in < 5 seconds
- [ ] All predictions successful
- [ ] No memory leaks
- [ ] Progress bar updates

## Documentation Verification

### 21. Documentation Files

- [ ] `APP_README.md` exists (comprehensive)
- [ ] `IMPLEMENTATION_SUMMARY.md` exists (summary)
- [ ] `QUICKSTART_GUIDE.md` exists (quick start)
- [ ] `DEPLOYMENT_CHECKLIST.md` exists (this file)
- [ ] `config.ini` exists (configuration)

### 22. Code Documentation

- [ ] `src/ui.py` has docstrings
- [ ] `src/model.py` has docstrings
- [ ] `src/model_service.py` has docstrings
- [ ] All functions documented
- [ ] Complex logic explained

## Security Testing

### 23. Input Validation

Test invalid inputs:
```bash
# Invalid gender
curl -X POST "http://localhost:8000/predict" \
  -d '{"gender":"Invalid",...}'

# Age out of range
curl -X POST "http://localhost:8000/predict" \
  -d '{"age":200,...}'

# Invalid province
curl -X POST "http://localhost:8000/predict" \
  -d '{"province":"InvalidProvince",...}'
```

Expected: Clear error messages, no crashes

### 24. Error Handling

- [ ] Missing fields show validation errors
- [ ] Type mismatches handled gracefully
- [ ] Model loading failures show fallback
- [ ] API errors return proper HTTP codes

## Logging Verification

### 25. Log Output

Run application and check logs:
```bash
python main.py --both 2>&1 | tee app.log
```

Expected log messages:
- [ ] "✅ Model loaded successfully"
- [ ] "✅ Model service initialized"
- [ ] "🚀 Starting Nepal Telco Churn Prediction API..."
- [ ] Requests logged with details
- [ ] No error messages (unless expected)

## Final Checklist

### Pre-Production

- [ ] All tests pass (1-25)
- [ ] No Python errors or warnings
- [ ] Documentation complete
- [ ] Performance acceptable
- [ ] Security validated
- [ ] Logging working
- [ ] Docker builds successfully
- [ ] All files committed to git

### Deployment Ready

- [ ] Environment variables configured
- [ ] Model files backed up
- [ ] Logs directory writable
- [ ] Port 8000 & 8501 available
- [ ] Firewall rules configured
- [ ] Monitoring set up
- [ ] Backup strategy defined

## Rollback Plan

If issues occur:

1. **API Issues:**
   ```bash
   python main.py --ui
   # Use local model service instead
   ```

2. **Model Issues:**
   - Uses fallback model automatically
   - No manual intervention needed

3. **Memory Issues:**
   - Process batch requests in smaller chunks
   - Restart container

4. **Port Conflicts:**
   ```bash
   python main.py --api --port 9000
   ```

---

## Test Completion

**Date:** ________________
**Tested By:** ________________
**Result:** ☐ PASSED ☐ FAILED

**Notes:** 
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

**Sign-off:** ________________

---

**If all checks pass, application is ready for production deployment!** ✅
