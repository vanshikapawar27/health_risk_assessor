# 🩺 AI-Powered Personal Health Risk Assessor

A CLI-based capstone Python project that collects daily lifestyle metrics,
applies a trained Machine Learning model to predict your health risk level,
stores your history asynchronously, and generates personalized recommendations.

---

## 📌 Problem Statement

People often overlook subtle, compounding lifestyle habits — poor sleep,
sedentary behavior, high stress, bad diet — until they manifest as serious
health conditions. There is no simple, personalized, locally-run tool that
aggregates these daily signals and provides an early, evidence-based risk
assessment without requiring any cloud service or subscription.

This project solves that.

---

## 🚀 Features

| Feature | Details |
|---|---|
| 🤖 ML Risk Prediction | RandomForestClassifier trained on 3000 synthetic records |
| 📊 12 Health Metrics | BMI, sleep, steps, stress, heart rate, diet, exercise, and more |
| 💾 Async History | `asyncio` + JSON-based persistent storage |
| 📈 Trend Viewer | See your last 7 assessments in a table |
| 💡 Recommendations | Up to 6 personalized, evidence-based suggestions |
| 🎨 Rich CLI UI | Beautiful terminal output using the `rich` library |

---

## 🗂️ Project Structure

```
health_risk_assessor/
│
├── main.py           # Entry point — CLI interface and app loop
├── assessor.py       # ML model training and prediction (RandomForest)
├── data_manager.py   # Async JSON history save/load (asyncio)
├── recommender.py    # Rule-based personalized recommendation engine
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## ⚙️ Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
python main.py
```

---

## 🧠 How the ML Model Works

- **Data**: 3,000 synthetic health records generated using realistic distributions
  and risk-scoring logic based on WHO and AHA guidelines.
- **Features**: 12 lifestyle metrics (age, BMI, sleep, steps, water intake,
  stress, heart rate, diet quality, exercise, screen time, smoking, alcohol)
- **Model**: `RandomForestClassifier` (200 trees, balanced class weights)
  wrapped in a `StandardScaler` pipeline
- **Labels**: Low (0) / Medium (1) / High (2) risk
- **Output**: Predicted class + probability distribution across all three classes

---

## 🔁 Async Design

`DataManager` uses `asyncio.to_thread()` to offload file I/O to a thread pool,
preventing blocking in the async event loop. An `asyncio.Lock` ensures
thread-safe writes across concurrent calls.

---

## 📖 OOP Design

| Class | Responsibility |
|---|---|
| `HealthAssessor` | Synthetic data generation, model training, prediction |
| `DataManager` | Async file I/O, history load/save, locking |
| `Recommender` | Metric evaluation, recommendation generation |

---

## 📋 Sample Metrics Input

| Metric | Example | Good Range |
|---|---|---|
| Age | 28 | — |
| BMI | 22.5 | 18.5–24.9 |
| Sleep (hrs) | 7.5 | 7–9 |
| Steps | 9500 | ≥8000 |
| Water (ml) | 2200 | ≥2000 |
| Stress (1–10) | 4 | ≤3 |
| Heart Rate (bpm) | 72 | 60–100 |
| Diet Quality (1–10) | 7 | ≥7 |
| Exercise (mins) | 35 | ≥30 |
| Screen Time (hrs) | 5 | ≤4 |
| Cigarettes | 0 | 0 |
| Alcohol Units | 0 | 0 |

---

## 📚 References

- WHO Global Physical Activity Guidelines
- American Heart Association — Heart Rate & BMI standards
- CDC Sleep Foundation recommendations
- NHS Alcohol unit guidelines
