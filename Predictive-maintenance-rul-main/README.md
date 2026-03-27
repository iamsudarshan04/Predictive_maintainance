PROJECT VISIT LINK : https://predictive-maintenance-rul-production.up.railway.app/

# Predictive Maintenance – Remaining Useful Life (RUL) Prediction

![ML Pipeline](./readme.md/MLpipeline.jpeg)

## Project Overview
This project focuses on **predictive maintenance** by estimating the **Remaining Useful Life (RUL)** of turbofan jet engines using sensor and operating condition data.  
The goal is to predict how many operational cycles an engine can continue before failure, enabling timely maintenance and preventing unexpected breakdowns.

The project is built step by step, starting from data understanding and feature engineering to baseline model evaluation, following a **professional machine learning workflow**.

---

## Problem Statement
Aircraft engines degrade over time due to continuous operation.  
Using historical sensor data, this project aims to:

- Model engine degradation behavior
- Predict the remaining number of cycles before failure (RUL)
- Validate whether engine condition snapshots can be used to estimate RUL

This is formulated as a **supervised regression problem**, where the target variable is numerical.

---

## Dataset
**NASA Turbofan Jet Engine Degradation Dataset (FD001)**

### Files Used
- `train_FD001.txt`  
  Contains full run-to-failure data for multiple engines.  
  This file is used to compute true RUL values and train models.

### Dataset Characteristics
- Multiple engines
- Each engine runs for several cycles until failure
- Each cycle contains:
  - Engine ID
  - Cycle number
  - 3 operating settings
  - 21 sensor readings

---

## Project Workflow

### 1. Data Understanding & Preparation
- Loaded raw text data using pandas
- Assigned meaningful column names
- Understood engine-cycle structure
- Treated each engine-cycle row as a **snapshot** of engine condition

### 2. RUL Target Creation

![RUL Creation Process](./readme.md/RUL_creation.jpeg)

Since the dataset does not directly provide RUL for training data:

- For each engine, the last cycle represents failure
- RUL was computed as:

```
RUL = max_cycle_of_engine − current_cycle
```

This transformed raw data into a **labeled dataset** suitable for supervised learning.

### 3. Feature Engineering

#### Sensor Analysis
- Visualized sensor behavior across operational cycles  
- Identified sensors showing **consistent degradation trends**  
- Avoided flat or noisy sensors  

#### Selected Features
- A subset of degradation-relevant sensors  
- All 3 operating settings  

These features were combined to form the **feature matrix (X)**.

### 4. Feature Matrix and Target Variable
- **X (features):**
  - Selected sensor values  
  - Operating settings  
- **y (target):**
  - Remaining Useful Life (RUL)  

Each row in X represents one engine snapshot, and the corresponding value in y represents the remaining life for that snapshot.

### 5. Train–Test Split
- Split data into training and testing sets (80/20)  
- Ensured alignment between features and target  
- Prevented data leakage  

### 6. Baseline Model – Linear Regression

A **Linear Regression model** was trained to establish a baseline.

**Purpose:**
- Validate whether engineered features contain predictive signal  
- Provide a reference point for more complex models  

#### Evaluation Metrics
- **MAE (Mean Absolute Error):** average prediction error in cycles  
- **RMSE (Root Mean Squared Error):** penalizes large errors  

#### Results
- MAE ≈ **35 cycles**  
- RMSE ≈ **45 cycles**  

**Conclusion:**  
The baseline model learns meaningful patterns, but linear assumptions limit accuracy.

### 7. Advanced Model – XGBoost Regressor
To capture non-linear degradation behavior:

- Trained an **XGBoost regression model**  
- Compared performance with baseline  
- Observed improved error metrics  

This model was selected as the **final predictive model**.

### 8. Model Serialization
To prepare for deployment:

- Saved the trained XGBoost model using `joblib`  
- Saved the ordered list of feature columns  
- Ensured consistency between training and inference  

These serialized artifacts enable model reuse without retraining.

---

## Deployment

![Deployment Architecture](./readme.md/deployment.jpeg)

### API Service
The trained model was deployed as a **FastAPI service**, transforming it into a usable system.

#### API Features
- Loads trained model and feature configuration  
- Accepts engine condition snapshots via JSON  
- Performs real-time RUL prediction  
- Returns both:
  - Predicted RUL (numerical)
  - Risk classification (Low / Medium / High)

![Risk Classification Logic](./readme.md/RCL.jpeg)

![End-to-End System](./readme.md/endtoend.jpeg)

### Endpoint
**POST** `/predict`

**Request Body:**
```json
{
  "sensor_readings": [...],
  "operating_settings": [...]
}
```

**Response:**
```json
{
  "predicted_rul": 85,
  "risk_level": "Low"
}
```

---

## Unique Value Proposition
- End-to-end ML system (not notebook-only)
- Snapshot-based inference suitable for real-world use
- Clean separation between model development and model usage
- Ready for cloud deployment and frontend integration

---

## Tools & Technologies Used
- **Programming:** Python
- **Data Processing:** pandas, NumPy
- **Machine Learning:** scikit-learn, XGBoost
- **Visualization:** Matplotlib
- **API Framework:** FastAPI, Uvicorn
- **Model Persistence:** Joblib
- **Development:** Jupyter Notebook
- **Version Control:** Git & GitHub

---

## Project Structure
```
├── frontend/           # Frontend application
├── models/            # Trained models and artifacts
├── notebooks/         # Jupyter notebooks for exploration
├── MLpipeline.jpeg    # ML pipeline diagram
├── RCL.jpeg          # Risk classification diagram
├── RUL_creation.jpeg # RUL creation process
├── deployment.jpeg   # Deployment architecture
├── endtoend.jpeg     # End-to-end system flow
├── app.py            # FastAPI application
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

---

## Key Learning Outcomes
- Understanding predictive maintenance and RUL modeling
- Feature selection through degradation analysis
- Baseline vs advanced model comparison
- Regression evaluation metrics (MAE, RMSE)
- Model serialization and dependency management
- API-based ML deployment

---

## Getting Started

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running the API
```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation
Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Author
**Shadya Panneerselvam**

---

## License
This project is open source and available for educational purposes.
