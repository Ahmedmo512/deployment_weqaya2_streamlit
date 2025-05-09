import streamlit as st
import pandas as pd 
import joblib 
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# App Title and Intro
st.title('Hypertension Prediction System ')
image_url = "https://th.bing.com/th/id/OIP.3OHMSFQptjBxVUPoNPGxsQHaFX?w=510&h=370&rs=1&pid=ImgDetMain"
st.image(image_url, caption="Early detection and prevention of hypertension is key to a healthier life.", use_container_width=True)
st.write("**Welcome to the Hypertension Prediction System!**\n"
         "This app uses machine learning to predict the likelihood of hypertension based on various health factors.\n"
         "Please enter your information below and get insights about your health risk.\n")

# Data Import and Preprocessing
df = pd.read_csv(r'data/hypertension(26k,14).csv')

# Functions for Visualizations
@st.cache_resource
def get_fig_Chest_Pain_Type(data):
    mean_risk = data.groupby("cp")["target"].mean().reset_index()
    fig = px.bar(mean_risk, x="cp", y="target",
                 title="Average Hypertension Risk by Chest Pain Type",
                 labels={"cp": "Chest Pain Type", "target": "Average Risk"},
                 color="target", color_continuous_scale="Reds")
    fig.update_layout(xaxis=dict(
        tickmode='array',
        tickvals=[0,1,2,3],
        ticktext=["Asymptomatic", "Typical Angina", "Atypical Angina", "Non-anginal Pain"]
    ))
    return fig

@st.cache_resource
def get_fig_Serum_cholestoral(data):
    fig, ax = plt.subplots()
    sns.histplot(data, x="chol", hue="target", bins=30, kde=True, ax=ax)
    ax.set_title("Cholesterol Distribution by Hypertension Risk")
    ax.set_xlabel("Serum Cholesterol (mg/dl)")
    ax.set_ylabel("Count")
    return fig

@st.cache_resource
def get_fig_Maximum_heart_rate(data):
    fig = px.box(data, x="target", y="thalach",
                 title="Heart Rate Distribution by Hypertension Risk",
                 labels={"target": "Risk (0=No, 1=Yes)", "thalach": "Max Heart Rate"},
                 color="target", color_discrete_sequence=["#2ca02c", "#d62728"])
    return fig

@st.cache_resource
def get_fig_ST_depression(data):
    fig = px.violin(data, y="oldpeak", x="target", box=True, points="all",
                    title="ST Depression Distribution by Hypertension Risk",
                    labels={"target": "Risk (0=No, 1=Yes)", "oldpeak": "ST Depression"},
                    color="target", color_discrete_sequence=["#1f77b4", "#ff7f0e"])
    return fig

# Visualization Selection
st.sidebar.subheader("Visualize Risk Factors")
risk_factor = st.sidebar.selectbox('Select a Risk Factor', ['Chest Pain Type', 'Serum Cholestoral', 'Maximum Heart Rate', 'ST Depression'])

if risk_factor == 'Chest Pain Type':
    st.plotly_chart(get_fig_Chest_Pain_Type(df), use_container_width=True)
elif risk_factor == 'Serum Cholestoral':
    st.pyplot(get_fig_Serum_cholestoral(df))
elif risk_factor == 'Maximum Heart Rate':
    st.plotly_chart(get_fig_Maximum_heart_rate(df), use_container_width=True)
else:
    st.plotly_chart(get_fig_ST_depression(df), use_container_width=True)

# Load Model and Scaler
scaler = joblib.load(r'models/scaler.pkl')
model = joblib.load(r'models/model.pkl')

# Input Form
st.subheader("Enter Your Information Below")

col1, col2 = st.columns(2)

age = col1.slider("**Age**", 10, 100, 20, help="Enter your age.")
sex = col2.selectbox("**Sex**", ["Male", "Female"], help="Select your gender.")
sex = 1 if sex == "Male" else 0

cp = col1.selectbox("**Chest Pain Type**", ["Asymptomatic", "Typical Angina", "Atypical Angina", "Non-anginal Pain"], help="Select the type of chest pain.")
cp = {"Asymptomatic": 0, "Typical Angina": 1, "Atypical Angina": 2, "Non-anginal Pain": 3}.get(cp)

trestbps = col2.slider("**Resting Blood Pressure (mm Hg)**", 80, 200, 110, help="Enter your resting blood pressure.")
chol = col1.slider("**Serum Cholesterol (mg/dl)**", 100, 600, 200, help="Enter your serum cholesterol level.")
fbs = col2.selectbox("**Fasting Blood Sugar > 120 mg/dl**", ["Yes", "No"], help="Is your fasting blood sugar greater than 120 mg/dl?")
fbs = 1 if fbs == "Yes" else 0

restecg = col1.selectbox("**Resting ECG Results**", ["Normal", "ST-T Wave Abnormality", "Severe ST-T Wave Abnormality"], help="Select your ECG result.")
restecg = {"Normal": 0, "ST-T Wave Abnormality": 1, "Severe ST-T Wave Abnormality": 2}.get(restecg)

thalach = col2.slider("**Max Heart Rate Achieved**", 60, 200, 100, help="Enter your maximum heart rate during exercise.")
exang = col1.selectbox("**Exercise Induced Angina**", ["Yes", "No"], help="Do you experience chest pain during exercise?")
exang = 1 if exang == "Yes" else 0

oldpeak = col2.slider("**ST Depression Induced by Exercise**", 0.0, 7.0, 2.0, step=0.1, help="Enter the ST depression caused by exercise.")
slope = col1.selectbox("**Slope of Peak Exercise ST Segment**", ["Upsloping", "Flat", "Downsloping"], help="Select the slope of the ST segment during exercise.")
slope = {"Upsloping": 0, "Flat": 1, "Downsloping": 2}.get(slope)

ca = col2.slider("**Number of Major Vessels Colored by Fluoroscopy**", 0, 4, 1, step=1, help="Enter the number of vessels colored by fluoroscopy.")
thal = col1.selectbox("**Myocardial Perfusion Scan**", ["Normal", "Fixed Defect", "Reversible Defect"], help="Select the result of your myocardial perfusion scan.")
thal = {"Normal": 1, "Fixed Defect": 2, "Reversible Defect": 3}.get(thal)

inputs = np.array([age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]).reshape(1, -1)
inputs = scaler.transform(inputs)

# Prediction and Result Display
result = model.predict(inputs)
neg_perc = model.predict_proba(inputs)[0][0]
pos_perc = model.predict_proba(inputs)[0][1]

# Display prediction results
if result == 1:
    result_text = "**High Risk**: You are at risk for hypertension."
    result_color = "red"
else:
    result_text = "**Low Risk**: You are not at risk for hypertension."
    result_color = "green"

perc = f"{max(neg_perc, pos_perc)*100:.2f}%"

# Warning Message
st.write("""
    **Important Reminder**:
    Hypertension is a serious health condition that should not be ignored. Please consult a doctor for a full diagnosis and treatment plan.
""")
start_text = f"""
Based on the inputs, this program estimates that the patient *{result_text}* with a **{perc}** probability.
Please note, this is just an estimation. Consult with your doctor for accurate results. We hope you're always in good health.
"""

st.write("-"*50)
end_text = """
**Important Warning:**

If you have been diagnosed with or suspect hypertension, please take immediate steps to manage your condition:

1. **Relax**: Try to stay calm and practice deep breathing exercises.
2. **Avoid Stimulants**: Limit caffeine, nicotine, and alcohol consumption.
3. **Stay Hydrated**: Drink plenty of water throughout the day.
4. **Monitor Your Blood Pressure**: Keep track of your readings using a monitor.
5. **Eat Healthily**: Prioritize fruits, vegetables, and low-sodium foods.
6. **Seek Medical Attention if Necessary**: If you experience symptoms like chest pain, dizziness, or difficulty breathing, seek medical help immediately.
"""
# Conclusion Text with Delay
def stream_data():
    for word in start_text.split(" "):
        yield word + " "
        time.sleep(0.02)

    if result == 1:
        st.error(f"⚠️ The patient is at risk of hypertension! with {perc}")
        st.image("https://media.mehrnews.com/d/2018/11/05/4/2947868.jpg", width=600)
        for word in end_text.split(" "):
            yield word + " "
            time.sleep(0.02)
    else: 
             st.success(f"✅ The patient is not at risk of hypertension with {perc}.  ")
             st.image("https://astrologer.swayamvaralaya.com/wp-content/uploads/2012/08/health1.jpg", width=600)

if st.button("**PREDICT**"):
    st.write_stream(stream_data)
