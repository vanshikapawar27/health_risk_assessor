"""
assessor.py — ML Model for Health Risk Assessment
====================================================
Uses a RandomForestClassifier trained on synthetic health data.
Predicts Low / Medium / High risk based on lifestyle inputs.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import warnings

warnings.filterwarnings("ignore")


class HealthAssessor:
    """
    Trains and uses an ML pipeline to assess personal health risk.

    Risk Labels:
        0 → Low
        1 → Medium
        2 → High
    """

    LABEL_MAP = {0: "Low", 1: "Medium", 2: "High"}
    FEATURE_ORDER = [
        "age", "bmi", "sleep_hours", "steps", "water_ml",
        "stress_level", "heart_rate", "diet_quality",
        "exercise_mins", "screen_hours", "smoking", "alcohol_units"
    ]

    def __init__(self):
        self.model = self._build_and_train()

    def _generate_synthetic_data(self, n=3000):
        """
        Generate realistic synthetic health data with label logic
        based on medical guidelines (WHO, AHA).
        """
        np.random.seed(42)
        data = []

        for _ in range(n):
            age           = np.random.randint(18, 75)
            bmi           = np.random.uniform(16, 42)
            sleep         = np.random.uniform(3, 10)
            steps         = np.random.randint(500, 18000)
            water         = np.random.randint(500, 4000)
            stress        = np.random.randint(1, 10)
            hr            = np.random.randint(45, 120)
            diet          = np.random.randint(1, 10)
            exercise      = np.random.randint(0, 120)
            screen        = np.random.uniform(1, 12)
            smoking       = np.random.randint(0, 20)
            alcohol       = np.random.randint(0, 10)

            # Risk scoring based on known health guidelines
            risk_score = 0

            # BMI
            if bmi < 18.5 or bmi > 30:   risk_score += 2
            elif bmi > 25:                risk_score += 1

            # Sleep
            if sleep < 6 or sleep > 9:   risk_score += 2
            elif sleep < 7:               risk_score += 1

            # Steps
            if steps < 3000:             risk_score += 2
            elif steps < 7000:           risk_score += 1

            # Water
            if water < 1200:             risk_score += 2
            elif water < 1800:           risk_score += 1

            # Stress
            if stress >= 8:              risk_score += 3
            elif stress >= 6:            risk_score += 2
            elif stress >= 4:            risk_score += 1

            # Heart rate
            if hr > 100 or hr < 50:      risk_score += 2
            elif hr > 90:                risk_score += 1

            # Diet
            if diet <= 3:                risk_score += 2
            elif diet <= 5:              risk_score += 1

            # Exercise
            if exercise == 0:            risk_score += 2
            elif exercise < 20:          risk_score += 1

            # Screen time
            if screen > 8:               risk_score += 1

            # Smoking
            risk_score += min(smoking // 3, 4)

            # Alcohol
            risk_score += min(alcohol // 2, 3)

            # Age factor
            if age > 55:                 risk_score += 1

            # Assign label
            if risk_score <= 5:    label = 0   # Low
            elif risk_score <= 11: label = 1   # Medium
            else:                  label = 2   # High

            data.append([age, bmi, sleep, steps, water, stress,
                         hr, diet, exercise, screen, smoking, alcohol, label])

        data = np.array(data)
        X = data[:, :-1]
        y = data[:, -1].astype(int)
        return X, y

    def _build_and_train(self):
        """Build and train a RandomForest pipeline."""
        X, y = self._generate_synthetic_data()
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(
                n_estimators=200,
                max_depth=12,
                min_samples_split=5,
                class_weight="balanced",
                random_state=42
            ))
        ])

        pipeline.fit(X_train, y_train)

        # Print model accuracy on training
        y_pred = pipeline.predict(X_test)
        print("\n[Model Training Complete]")
        print(classification_report(y_test, y_pred,
                                    target_names=["Low", "Medium", "High"]))

        return pipeline

    def predict(self, inputs: dict) -> tuple[str, dict]:
        """
        Predict health risk from user input dict.

        Returns:
            risk_label: str — "Low", "Medium", or "High"
            risk_proba: dict — probability for each class
        """
        features = np.array([[inputs[f] for f in self.FEATURE_ORDER]])
        label_idx = self.model.predict(features)[0]
        proba = self.model.predict_proba(features)[0]

        risk_label = self.LABEL_MAP[label_idx]
        risk_proba = {
            "Low": proba[0],
            "Medium": proba[1],
            "High": proba[2]
        }
        return risk_label, risk_proba
