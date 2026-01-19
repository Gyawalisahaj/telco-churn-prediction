# Streamlit Community Cloud Deployment Guide

## Step-by-Step Deployment Instructions

### Prerequisites
1. **GitHub Account** - You need a GitHub account to deploy on Streamlit Community Cloud
2. **Git Repository** - Your project must be pushed to GitHub
3. **Streamlit Account** - Create a free account at [share.streamlit.io](https://share.streamlit.io)

---

## Step 1: Prepare Your Repository

### 1.1 Ensure your repository is public on GitHub
- Go to your GitHub repository settings
- Make sure it's set to **Public** (required for Streamlit Cloud free tier)
- The repository should contain all necessary files

### 1.2 Your project structure should look like this:
```
telco-churn-prediction/
├── main.py
├── src/
│   ├── ui.py (your Streamlit app entry point)
│   ├── model.py
│   ├── model_service.py
│   ├── predmodel.py
│   └── __init__.py
├── model/
│   └── Churnpred_ann.keras (pre-trained model)
├── data/
│   └── cleaned_churn_data.csv (or training data)
├── requirements.txt
└── config.ini
```

---

## Step 2: Update requirements.txt for Streamlit Cloud

Your `requirements.txt` is already good, but ensure these versions work with Streamlit:

```
pandas>=2.0.0
numpy>=1.24.0
tensorflow>=2.13.0
keras>=2.13.0
scikit-learn>=1.3.0
streamlit>=1.28.0
plotly>=5.17.0
joblib>=1.3.0
```

⚠️ **Note**: Remove `fastapi` and `uvicorn` from requirements.txt if you're only deploying the Streamlit UI (not the API).

---

## Step 3: Create `.streamlit/config.toml` (Optional but Recommended)

Create a new file at `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = false

[logger]
level = "info"
```

---

## Step 4: Deploy to Streamlit Community Cloud

### 4.1 Sign up and Connect GitHub
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"** button
3. Click **"Sign up with GitHub"** and authorize Streamlit
4. Or sign in if you already have an account

### 4.2 Deploy Your App
After logging in:
1. Click **"Create app"** or **"New app"**
2. Select your repository: `Gyawalisahaj/telco-churn-prediction`
3. Select the branch: `main`
4. Specify the main file path: `src/ui.py`
5. Click **"Deploy"**

---

## Step 5: Configure Secrets (if needed)

If your app uses API keys or sensitive data:

1. In Streamlit Cloud dashboard, go to your app settings
2. Click **"Secrets"**
3. Add any secrets in TOML format:
   ```toml
   API_KEY = "your-api-key"
   DB_PASSWORD = "your-password"
   ```
4. Access them in your code: `st.secrets["API_KEY"]`

---

## Step 6: Monitor Deployment

1. After clicking deploy, you'll see a console showing build progress
2. Wait for the message: **"Your app is ready!"**
3. Your app will be live at: `https://your-username-telco-churn.streamlit.app/`

---

## Troubleshooting

### Issue: "Module not found" error
**Solution**: 
- Ensure all dependencies are in `requirements.txt`
- Check that imports use relative paths: `from src.model_service import...`

### Issue: "Model file not found"
**Solution**:
- Ensure the model file `model/Churnpred_ann.keras` is committed to GitHub
- Use relative paths in code: `Path(__file__).parent / "model" / "Churnpred_ann.keras"`

### Issue: Data file not found
**Solution**:
- Ensure CSV files in `data/` folder are committed to GitHub
- Use relative paths: `pd.read_csv("data/cleaned_churn_data.csv")`

### Issue: Memory/Timeout errors
**Solution**:
- Optimize model loading (use caching with `@st.cache_resource`)
- Reduce dataset size if possible
- Check for memory leaks in your code

### Issue: "Private repository"
**Solution**:
- Make your GitHub repository public
- Or upgrade to Streamlit Teams plan for private repos

---

## Advanced: Custom Domain

After deployment, you can add a custom domain:

1. In Streamlit Cloud dashboard, go to app settings
2. Click **"Custom domain"**
3. Enter your domain and follow DNS setup instructions

---

## Key Differences: Streamlit vs Local

| Feature | Local | Streamlit Cloud |
|---------|-------|-----------------|
| Entry point | `src/ui.py` | Same file specified during deployment |
| File paths | Absolute paths OK | Must use relative paths |
| Data files | Local storage | Must be in GitHub repo |
| Model files | Local storage | Must be in GitHub repo |
| Performance | Depends on machine | Limited (free tier: 1GB RAM, 1vCPU) |

---

## Final Checklist Before Deployment

- ✅ GitHub repository is public
- ✅ All files committed and pushed to GitHub
- ✅ `requirements.txt` has all dependencies
- ✅ Model file in `model/` folder is committed
- ✅ Data files in `data/` folder are committed
- ✅ All imports use relative paths (e.g., `from src.model_service import...`)
- ✅ No hardcoded absolute paths
- ✅ `src/ui.py` is the Streamlit app entry point
- ✅ Streamlit account created at [share.streamlit.io](https://share.streamlit.io)

---

## After Deployment: Monitoring

- Check Streamlit Cloud logs regularly
- Set up email alerts for app crashes
- Monitor app usage statistics in dashboard
- Update code by pushing to GitHub (auto-redeploys)

---

## Useful Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Community Cloud Docs](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-cloud/manage-your-app/secrets-management)
- [Streamlit Performance Tips](https://docs.streamlit.io/library/advanced-features/caching)

---

**Good luck with your deployment! 🚀**
