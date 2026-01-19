# 🚀 Getting Started Guide - Nepal Telco Churn Prediction

## Installation & Setup

### Option 1: Quick Start (Recommended)

#### Linux/macOS:
```bash
cd /home/sahajgyawali45/abc/telco_churn
chmod +x quickstart.sh
./quickstart.sh
```

Then run:
```bash
python main.py --both
```

#### Windows:
```bash
cd C:\path\to\telco_churn
quickstart.bat
```

Then run:
```bash
python main.py --both
```

---

### Option 2: Manual Setup

1. **Navigate to project:**
   ```bash
   cd /home/sahajgyawali45/abc/telco_churn
   ```

2. **Activate virtual environment:**
   ```bash
   # Linux/macOS
   source tf_venv/bin/activate
   
   # Windows
   tf_venv\Scripts\activate.bat
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run application:**
   ```bash
   python main.py --both
   ```

---

### Option 3: Docker Setup

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Or build manually:**
   ```bash
   docker build -t telco-churn-predictor .
   docker run -p 8000:8000 -p 8501:8501 telco-churn-predictor
   ```

---

## 🌐 Accessing the Application

### Streamlit Web UI
```
http://localhost:8501
```

**Features:**
- Single customer predictions
- Batch CSV processing
- Analytics dashboard
- Prediction history
- Data export

### FastAPI REST API
```
http://localhost:8000/docs
```

**Available Endpoints:**
- `GET /` - Health check
- `GET /health` - Detailed health
- `POST /predict` - Single prediction
- `POST /batch-predict` - Batch predictions
- `GET /info` - System information

### Alternative API Documentation
```
http://localhost:8000/redoc
```

---

## 📊 Using the Application

### Single Customer Prediction

1. **Open Streamlit UI** → `http://localhost:8501`
2. **Select "Single Prediction"** from navigation
3. **Fill in customer details:**
   - Demographics (name, gender, age, dependents)
   - Financial (salary)
   - Service usage (tenure, calls, SMS, data)
   - Provider info (province, telecom provider)
4. **Click "Predict Churn Risk"**
5. **Review results:**
   - Risk gauge chart
   - Churn prediction
   - Risk level
   - Recommendations

### Batch Prediction

1. **Prepare CSV file** with columns:
   ```
   name,gender,age,num_dependents,estimated_salary,calls_made,
   sms_sent,data_used,tenure_months,province,provider
   ```

2. **Select "Batch Prediction"** in UI
3. **Upload CSV file**
4. **Click "Predict All Customers"**
5. **View results:**
   - Statistics summary
   - Results table
   - Comparison charts
6. **Download results as CSV**

### Analytics Dashboard

1. **Select "Analytics Dashboard"**
2. **View key metrics:**
   - Total predictions made
   - Churn rate %
   - Average risk level
   - High-risk count
3. **Analyze charts:**
   - Risk distribution
   - Churn predictions
   - Probability histogram

### Prediction History

1. **Select "Prediction History"**
2. **Filter by:**
   - Risk level (LOW, MEDIUM, HIGH)
   - Prediction (CHURN, RETAIN)
3. **Download history as CSV**
4. **Clear history when needed**

---

## 🔌 API Usage Examples

### Using cURL

**Single Prediction:**
```bash
curl -X POST "http://localhost:8000/predict" \
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

**Health Check:**
```bash
curl http://localhost:8000/health
```

**System Info:**
```bash
curl http://localhost:8000/info
```

### Using Python

```python
import requests
import json

# Single prediction
url = "http://localhost:8000/predict"
customer = {
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
}

response = requests.post(url, json=customer)
result = response.json()

print(f"Churn Prediction: {result['churn_prediction']}")
print(f"Probability: {result['churn_probability']}%")
print(f"Risk Level: {result['risk_level']}")
print(f"\nRecommendations:")
for rec in result['recommendations']:
    print(f"  • {rec}")
```

### Using JavaScript/Node.js

```javascript
const fetch = require('node-fetch');

const customer = {
  name: "Ram Kumar",
  gender: "Male",
  age: 35,
  num_dependents: 2,
  estimated_salary: 50000,
  calls_made: 45,
  sms_sent: 30,
  data_used: 1500,
  tenure_months: 24,
  province: "Bagmati",
  provider: "Ncell"
};

fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(customer)
})
.then(response => response.json())
.then(data => {
  console.log(`Churn: ${data.churn_prediction}`);
  console.log(`Probability: ${data.churn_probability}%`);
  console.log(`Risk: ${data.risk_level}`);
})
.catch(error => console.error('Error:', error));
```

---

## 🔧 Command-Line Options

```bash
python main.py --help
```

**Options:**
```
--ui              Run Streamlit UI only
--api             Run FastAPI backend only
--both            Run both UI and API (default)
--host HOST       API host (default: 0.0.0.0)
--port PORT       API port (default: 8000)
```

**Examples:**
```bash
# Run both (default)
python main.py

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

## 📁 Project Structure

```
telco_churn/
├── main.py                          # Application runner
├── requirements.txt                 # Dependencies
├── Dockerfile                       # Docker configuration
├── docker-compose.yml               # Docker Compose
├── config.ini                       # Configuration
├── quickstart.sh                    # Linux/macOS setup
├── quickstart.bat                   # Windows setup
│
├── README.md                        # Original project README
├── APP_README.md                    # Comprehensive app guide
├── IMPLEMENTATION_SUMMARY.md        # What was built
├── QUICKSTART_GUIDE.md              # This file
│
├── src/
│   ├── __init__.py
│   ├── ui.py                       # Streamlit UI (506 lines)
│   ├── model.py                    # FastAPI backend (217 lines)
│   ├── model_service.py            # ML service (340 lines)
│   └── predmodel.py                # Data models (50 lines)
│
├── model/
│   ├── Churnpred_ann.keras         # Trained model
│   ├── scaler.pkl                  # Feature scaler
│   └── train_columns.pkl           # Column list
│
├── data/
│   ├── telecom_churn_raw.csv
│   ├── cleaned_churn_data.csv
│   └── churn_predictions_all_models.csv
│
└── notebook/
    ├── 01_data_cleaning.ipynb
    ├── 02_eda.ipynb
    └── modeltraining.ipynb
```

---

## ⚠️ Troubleshooting

### Issue: Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Use different port
python main.py --api --port 9000

# Or kill existing process (macOS/Linux)
lsof -i :8000
kill -9 <PID>
```

### Issue: Module Not Found

**Error:** `ModuleNotFoundError: No module named 'tensorflow'`

**Solution:**
```bash
# Reinstall requirements
pip install --upgrade -r requirements.txt
```

### Issue: Model File Not Found

**Error:** `Model not found at model/Churnpred_ann.keras`

**Solution:**
- Ensure model file exists in `model/` directory
- App will use fallback model if missing
- Check file permissions

### Issue: Connection Refused

**Error:** `Cannot connect to API at http://localhost:8000`

**Solution:**
```bash
# Start API first
python main.py --api

# Wait 3-5 seconds, then start UI
python main.py --ui

# Or run both together
python main.py --both
```

### Issue: Memory Error

**Solution:**
- Close other applications
- Batch process in smaller chunks
- Use API instead of UI for batch jobs

---

## 📊 CSV File Format

### Sample Input CSV

```csv
name,gender,age,num_dependents,estimated_salary,calls_made,sms_sent,data_used,tenure_months,province,provider
Ram Kumar,Male,35,2,50000,45,30,1500,24,Bagmati,Ncell
Sita Sharma,Female,28,1,45000,60,50,2000,18,Gandaki,Nepal Telecom
Arjun Singh,Male,42,3,65000,25,15,800,48,Karnali,Ncell
Priya Patel,Female,31,0,55000,70,100,3000,12,Lumbini,Nepal Telecom
```

### Column Descriptions

| Column | Type | Range | Description |
|--------|------|-------|-------------|
| name | string | - | Customer name |
| gender | string | Male/Female | Customer gender |
| age | integer | 18-100 | Customer age |
| num_dependents | integer | 0-10 | Number of dependents |
| estimated_salary | float | 0+ | Monthly salary in NPR |
| calls_made | integer | 0+ | Monthly calls |
| sms_sent | integer | 0+ | Monthly SMS |
| data_used | float | 0+ | Monthly data in MB |
| tenure_months | integer | 0-72 | Months as customer |
| province | string | See list | Nepal province |
| provider | string | Ncell/Nepal Telecom | Telecom provider |

### Valid Provinces

- Bagmati
- Gandaki
- Karnali
- Koshi
- Lumbini
- Madhesh
- Sudurpashchim

---

## 🔐 Security Notes

- ✅ Input validation via Pydantic
- ✅ No sensitive data in logs
- ✅ CORS configured for API
- ✅ Error messages sanitized
- ✅ Type hints throughout

---

## 📈 Performance Tips

1. **For single predictions:** Use UI or `/predict` endpoint
2. **For batch processing:** Use CSV upload (100+ customers)
3. **For automation:** Use API directly
4. **For analytics:** Use dashboard

---

## 💡 Tips & Tricks

### Export Predictions
1. Make predictions
2. Go to "Prediction History"
3. Click "📥 Download History"

### Filter Predictions
1. In "Prediction History"
2. Select risk level and prediction type
3. Apply filters

### View Recommendations
1. Make prediction
2. Scroll to "💡 Retention Recommendations"
3. View AI-powered insights

### Monitor Health
1. Visit `http://localhost:8000/health`
2. Check model_loaded status
3. Verify API is responsive

---

## 🎯 Typical Workflow

1. **Start Application**
   ```bash
   python main.py --both
   ```

2. **Make Predictions**
   - Single: UI Single Prediction
   - Batch: UI Batch Prediction

3. **Analyze Results**
   - UI Analytics Dashboard
   - View recommendations
   - Track trends

4. **Export Data**
   - Download CSV results
   - Use for reporting
   - Integration with other systems

---

## 📞 Need Help?

1. Check **APP_README.md** for detailed documentation
2. Review **IMPLEMENTATION_SUMMARY.md** for architecture
3. Check **config.ini** for configuration options
4. Review error messages in terminal logs

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Model files exist in `model/` directory
- [ ] Application starts without errors
- [ ] UI accessible at http://localhost:8501
- [ ] API accessible at http://localhost:8000/docs
- [ ] Health check passing
- [ ] Can make a test prediction
- [ ] Can download results

---

**Enjoy your professional churn prediction application!** 🇳🇵✨
