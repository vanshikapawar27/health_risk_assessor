"""
recommender.py — Personalized Health Recommendations
======================================================
Generates targeted advice based on the user's weakest health metrics
and their overall risk level.
"""


class Recommender:
    """Rule-based recommendation engine for health improvements."""

    def generate(self, inputs: dict, risk_label: str) -> list[str]:
        """
        Generate up to 5 personalized recommendations based on weak metrics.

        Args:
            inputs: dict of user health inputs
            risk_label: "Low", "Medium", or "High"

        Returns:
            List of recommendation strings
        """
        recs = []

        # Sleep
        if inputs["sleep_hours"] < 6:
            recs.append("🛌 You're severely sleep-deprived. Aim for 7–9 hours. Poor sleep raises cortisol and cardiovascular risk.")
        elif inputs["sleep_hours"] < 7:
            recs.append("🛌 Try to get at least 7 hours of sleep. Even one extra hour can lower stress hormones significantly.")

        # BMI
        if inputs["bmi"] > 30:
            recs.append("⚖️ Your BMI indicates obesity. A 5–10% weight reduction can dramatically cut your risk of diabetes and heart disease.")
        elif inputs["bmi"] > 25:
            recs.append("⚖️ You're in the overweight range. Combining 30 min daily walks with a balanced diet can help normalize BMI.")
        elif inputs["bmi"] < 18.5:
            recs.append("⚖️ You're underweight. Consider consulting a dietitian to ensure you're meeting caloric and nutrient needs.")

        # Steps
        if inputs["steps"] < 3000:
            recs.append("🚶 You're very sedentary today. Walking just 30 minutes (≈3000 steps) reduces cardiovascular disease risk by 19%.")
        elif inputs["steps"] < 7000:
            recs.append("🚶 Try to hit 8,000–10,000 steps daily. Small breaks and short walks throughout the day add up quickly.")

        # Water
        if inputs["water_ml"] < 1200:
            recs.append("💧 You're significantly dehydrated. Drink at least 2L (2000ml) of water daily to maintain kidney and cognitive function.")
        elif inputs["water_ml"] < 1800:
            recs.append("💧 Increase water intake to at least 2L/day. Carry a reusable bottle as a constant reminder.")

        # Stress
        if inputs["stress_level"] >= 8:
            recs.append("🧘 Your stress level is dangerously high. Practice 10-minute deep breathing or meditation daily — it lowers cortisol by up to 20%.")
        elif inputs["stress_level"] >= 6:
            recs.append("🧘 Elevated stress detected. Try journaling, reducing caffeine, or a short evening walk to unwind.")

        # Heart rate
        if inputs["heart_rate"] > 100:
            recs.append("❤️ Your resting heart rate is elevated (>100 bpm). This may indicate stress, dehydration, or overexertion. Consult a doctor if persistent.")
        elif inputs["heart_rate"] < 50:
            recs.append("❤️ Very low resting heart rate detected. While common in athletes, consult a doctor if you feel dizzy or fatigued.")

        # Diet
        if inputs["diet_quality"] <= 3:
            recs.append("🥗 Your diet quality is poor. Aim to include vegetables, whole grains, and lean protein in at least 2 meals today.")
        elif inputs["diet_quality"] <= 5:
            recs.append("🥗 There's room to improve your diet. Reducing processed food and adding one more serving of vegetables can make a real difference.")

        # Exercise
        if inputs["exercise_mins"] == 0:
            recs.append("🏃 No exercise today. Even 15–20 minutes of brisk walking counts and significantly boosts mood and metabolism.")
        elif inputs["exercise_mins"] < 20:
            recs.append("🏃 Aim for 30+ minutes of moderate activity per day as recommended by the WHO.")

        # Smoking
        if inputs["smoking"] > 0:
            recs.append(f"🚭 You smoked {inputs['smoking']} cigarette(s) today. Every cigarette increases cardiovascular and cancer risk. Consider a cessation program.")

        # Alcohol
        if inputs["alcohol_units"] > 4:
            recs.append("🍺 High alcohol consumption detected. More than 14 units/week raises liver, heart, and cancer risk. Try tracking and setting weekly limits.")
        elif inputs["alcohol_units"] > 2:
            recs.append("🍺 Moderate alcohol detected. Try alcohol-free days each week to give your liver recovery time.")

        # Screen
        if inputs["screen_hours"] > 8:
            recs.append("📵 Excessive screen time can disrupt melatonin and sleep. Use the 20-20-20 rule: every 20 min, look 20 feet away for 20 seconds.")

        # High-risk summary
        if risk_label == "High" and len(recs) < 3:
            recs.append("🔴 Your overall risk is High. Please consider scheduling a health check-up with your doctor soon.")

        return recs[:6]  # Limit to 6 most important
