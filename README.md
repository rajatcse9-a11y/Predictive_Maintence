# 🔧 Predictive Maintenance System

An end-to-end Machine Learning project that predicts potential machine failures using operational and sensor data. The goal is to support proactive maintenance, reduce unexpected downtime, and improve equipment reliability.

## 🚀 Project Overview

Unexpected machine failures can lead to production downtime and increased maintenance costs. This project uses machine learning to analyze machine operating conditions and identify potential failures before they occur.

The project includes data preprocessing, feature engineering, model training, model evaluation, and an interactive Streamlit application for making predictions.

## ✨ Features

* Data preprocessing and cleaning
* Exploratory data analysis
* Feature engineering
* Machine learning model training
* Model evaluation using classification metrics
* Predictive maintenance predictions
* Interactive Streamlit user interface
* FastAPI backend for model inference
* Docker configuration included for future containerization

## 🛠️ Tech Stack

* **Language:** Python
* **Machine Learning:** Scikit-learn
* **Data Processing:** Pandas, NumPy
* **Visualization:** Matplotlib, Seaborn
* **API:** FastAPI
* **Frontend:** Streamlit
* **Model Storage:** Joblib / Pickle (depending on the implementation)
* **Containerization:** Docker, Docker Compose

## 📁 Project Structure

```text
Predictiv_Maintence/
│
├── api/
│   └── ...
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   └── ...
│
├── src/
│   └── ...
│
├── streamlit_app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

*Note: Update this structure to match your actual project files before publishing.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Predictiv_Maintence
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit application

```bash
streamlit run streamlit_app.py
```

Open the local URL displayed in your terminal.

### 5. Run the FastAPI backend

If your FastAPI application is located at `api/main.py`, run:

```bash
uvicorn api.main:app --reload
```

Open the API documentation at:

```text
http://127.0.0.1:8000/docs
```

*Adjust the command if your FastAPI entry point has a different filename or location.*

## 📊 Model Evaluation

Model performance should be evaluated using appropriate classification metrics, such as:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion matrix

For predictive maintenance, recall is particularly important because missing an actual machine failure can be costly.

*Add your actual evaluation results after running the final model.*

## 🔮 Future Improvements

* Improve model performance through hyperparameter tuning
* Add monitoring for incoming machine sensor data
* Implement model versioning and experiment tracking
* Deploy the application to a cloud platform
* Add automated model retraining and monitoring

## 👨‍💻 Author

**Rajat Maurya**

Aspiring Applied ML Engineer | Machine Learning | Deep Learning | FastAPI

* GitHub: https://github.com/rajatcse9-a11y
* Portfolio: https://rajat-portfol342.netlify.app/#skills
* LinkedIn: https://www.linkedin.com/in/rajat-maurya-6a6b72354

## 📄 License

This project is available for educational and portfolio purposes. Add a LICENSE file if you want to specify the terms under which others may use or distribute the code.
