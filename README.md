# 🧪 Wafer Fault Detection using Machine Learning

This project focuses on detecting faults in semiconductor wafers using machine learning. It includes a trained model along with a production-ready API built using **Flask**, allowing seamless integration into manufacturing systems.

---

## 📌 Problem Statement

In the semiconductor industry, wafer defects can lead to catastrophic failures and high financial losses. This project aims to automatically classify wafers as **faulty** or **non-faulty** using historical sensor data, improving inspection efficiency and product quality.

---

## 🎯 Objectives

- Analyze sensor readings to understand patterns in faulty wafers
- Build and evaluate ML models for fault classification
- Perform **hyperparameter tuning** to maximize performance
- Create a lightweight **Flask API** for real-time inference
- Test endpoints using **Postman** and ensure cross-origin accessibility with **CORS**

---

## 📂 Dataset

- Multivariate time-series sensor data from wafers
- Target variable: `0` (Good wafer) or `1` (Faulty wafer)

> For reproducibility, you may refer to the [SECOM Dataset](https://archive.ics.uci.edu/ml/datasets/SECOM) from UCI ML Repository.

---

## 🛠️ Tech Stack

- **Language:** Python 3.x  
- **Libraries Used:**
  - `pandas`, `numpy` – Data processing  
  - `matplotlib`, `seaborn` – Visualization  
  - `scikit-learn` – ML modeling & evaluation  
  - `GridSearchCV` – Hyperparameter tuning  
  - `Flask` – API development  
  - `flask-cors` – Cross-Origin Resource Sharing  
  - `Postman` – API testing

---

## 🧠 Model Used

After evaluating multiple models, **Random Forest** gave the best performance.

| Model         | Test AUC Score |
|---------------|----------------|
| Random Forest | **0.918** ✅     |
| XGBoost       | ~0.89           |

> Final model was selected after **hyperparameter tuning** using `GridSearchCV`.

---

## ✅ Results

- **Test AUC Score:** 0.918  
- **Confusion Matrix:**
  ![confusion matrix](assets/confusion_matrix.png)

---

## 🚀 API Deployment

The model is exposed via a **Flask REST API** to allow integration into external systems.

### 🔧 How to Use the API:

1. Run the Flask server:
   ```bash
   python app.py
