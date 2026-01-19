# Streamlit Cloud Deployment Guide

## Option 1: Using `streamlit_app.py` (Recommended ⭐)

**Why this works best:**
- Streamlit Cloud automatically looks for `streamlit_app.py` as the entry point
- It properly handles sys.path for module imports
- No need to specify the main file path during deployment

### Steps:
1. Push changes to GitHub:
   ```bash
   git add src/ui.py src/model.py streamlit_app.py
   git commit -m "Add Streamlit Cloud deployment file"
   git push origin main
   ```

2. Go to https://share.streamlit.io
3. Click **"New app"**
4. Select your repository: `your-username/telco-churn-prediction`
5. Select branch: `main`
6. **Leave "Main file path" blank** (Streamlit will auto-detect `streamlit_app.py`)
7. Click **"Deploy"**

---

## Option 2: Using `src/ui.py`

If you prefer to specify the file path:

### Steps:
1. Go to https://share.streamlit.io
2. Click **"New app"**
3. Repository: `your-username/telco-churn-prediction`
4. Branch: `main`
5. Main file path: `src/ui.py`
6. Click **"Deploy"**

---

## Option 3: Using `main.py` (Not Recommended ❌)

**Why NOT to use `main.py`:**
- `main.py` is designed to run FastAPI and Streamlit in subprocesses
- Streamlit Cloud doesn't support subprocess spawning
- It will cause hanging/timeout errors

---

## Files Modified for Cloud Compatibility

✅ **`src/ui.py`** - Improved import handling with multiple fallback levels
✅ **`src/model.py`** - Enhanced import robustness
✅ **`streamlit_app.py`** - NEW cloud entry point

---

## Troubleshooting

### Still getting ImportError?
Check the app logs on Streamlit Cloud:
1. Click your app
2. Click **"Manage app"** (⋮ menu)
3. Click **"View logs"**
4. Look for import errors

### Model file not found?
- Ensure `model/Churnpred_ann.keras` is committed to Git
- The file size might cause deployment issues if >100MB
- Check `.gitignore` isn't excluding the model

### Too many dependencies?
- Streamlit Cloud has limited memory
- Remove unused packages from `requirements.txt`
- TensorFlow can be large - consider using a lighter alternative if needed

---

## Deployment Status

- **Entry Point:** `streamlit_app.py` (auto-detected) OR `src/ui.py` (explicit)
- **Main file:** `src/ui.py` (UI app)
- **Dependencies:** See `requirements.txt`
- **Model:** `model/Churnpred_ann.keras`
- **Config:** `.streamlit/config.toml`

**Ready to deploy!** ✨
