import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def explain_decision(sugar, salt, sat_fat, calories, label):
    health_status = "unhealthy" if label == 1 else "healthy"

    prompt = f"""
You are a nutrition expert AI. Explain like a human.

Food nutritional values:
- Sugar: {sugar} g
- Salt: {salt} g
- Saturated Fat: {sat_fat} g
- Calories: {calories}

The machine-learning model classified this food as **{health_status}**.

Respond with:
1. A clear explanation WHY the food is {health_status}.
2. What health risks it may cause.
3. What better alternative foods the user can choose.
4. If unhealthy, give a healthier version of this food.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
