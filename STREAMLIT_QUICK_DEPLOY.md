# Streamlit Cloud Deployment Quick Steps

## 🚀 Quick Deployment (5 minutes)

### Step 1: GitHub Setup
```bash
# Ensure your repo is public on GitHub
# Make sure all changes are committed
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### Step 2: Go to Streamlit Cloud
1. Visit: **https://share.streamlit.io**
2. Sign up/Sign in with GitHub
3. Click **"Create app"** or **"New app"**

### Step 3: Connect Your Repository
- **Repository**: Gyawalisahaj/telco-churn-prediction
- **Branch**: main
- **Main file path**: `src/ui.py`

### Step 4: Deploy
- Click **"Deploy"**
- Wait 2-5 minutes for build to complete
- Your app will be live! 🎉

---

## Your App URL will be:
`https://<username>-telco-churn.streamlit.app/`

OR

`https://telco-churn-prediction-<randomstring>.streamlit.app/`

---

## ✅ Pre-Deployment Checklist

- [ ] GitHub repository is **PUBLIC**
- [ ] All files are **committed and pushed** to GitHub
- [ ] Model file exists: `model/Churnpred_ann.keras`
- [ ] Data files exist: `data/cleaned_churn_data.csv`
- [ ] `requirements.txt` is up to date
- [ ] `.streamlit/config.toml` exists
- [ ] All imports in `src/ui.py` use **relative paths**

---

## 🔧 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Private repo error | Make repository PUBLIC on GitHub |
| Module not found | Check requirements.txt has all packages |
| File not found | Ensure file is in GitHub (not in .gitignore) |
| App crashes | Check Streamlit logs in dashboard |
| Slow load | Model is large; Streamlit Cloud has limited resources |

---

## 📊 After Deployment

- Monitor your app in the [Streamlit Cloud Dashboard](https://share.streamlit.io)
- Check logs if there are issues
- Updates auto-deploy when you push to GitHub
- Free tier: 1 GB RAM, auto-sleeps after 7 days of inactivity

---

## 🎯 Next Steps

After successful deployment:
1. Test all features of your app
2. Share the link with stakeholders
3. Monitor performance and error logs
4. Make updates by pushing to GitHub (auto-redeploys)

---

**Questions?** Check [Streamlit Docs](https://docs.streamlit.io/)
