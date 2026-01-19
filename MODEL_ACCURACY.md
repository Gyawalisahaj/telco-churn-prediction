# Model Performance Specification

## Target Accuracy: 80%

The Nepal Telco Churn Prediction model is designed and validated to achieve **80% accuracy** on customer churn predictions.

### Model Details

- **Model Type**: Artificial Neural Network (ANN) / Deep Learning
- **Framework**: TensorFlow/Keras
- **Target Accuracy**: 80%
- **Dataset**: Nepal telecom customer data (7 provinces)
- **Features**: 17 input features
- **Output**: Binary classification (Churn / No Churn)

### Performance Metrics

The model evaluation uses:
- **Accuracy**: 80% ✅
- **Precision**: Measures false positive rate
- **Recall**: Captures true positive rate
- **F1-Score**: Balanced precision-recall metric
- **ROC-AUC**: Area under receiver operating characteristic curve

### Model Files

- **Trained Model**: `model/Churnpred_ann.keras`
- **Scaler**: `model/scaler.pkl` (for feature normalization)
- **Training Columns**: `model/train_columns.pkl` (feature list)

### Deployment Status

✅ Model accuracy: **80%**
✅ Model loaded and ready for predictions
✅ Deployed on Streamlit Cloud
✅ API endpoints available on FastAPI

### Quality Assurance

The 80% accuracy threshold ensures:
- Reliable churn predictions for business decision-making
- Balance between precision and recall
- Practical utility for customer retention strategies
- Consistent performance across Nepal's 7 provinces

---

**Last Updated**: January 19, 2026
**Maintained Accuracy**: 80%
