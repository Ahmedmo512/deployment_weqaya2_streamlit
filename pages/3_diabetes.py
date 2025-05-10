import streamlit as st
import numpy as np
import pandas as pd
import joblib
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load model
st.set_page_config(page_title="Disease Dashboard")
st.title("🩺 Disease & Prediabetes Risk Prediction Dashboard")
@st.cache_resource
def load_model():
    return joblib.load(r"models/random_forest_model.pkl")

model = load_model()

# load data
data = pd.read_csv('data/diabetes.csv')

# Sidebar navigation
menu = st.sidebar.radio("Navigate", [ "📋 Predict", "📊 Visualizations"])


# Prediction tab
if menu == "📋 Predict":
    st.subheader("🧾 Enter Patient Information")

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        with col1:
            HighBP = st.selectbox("High Blood Pressure", ['No', 'Yes'])
            HighChol = st.selectbox("High Cholesterol", ['No', 'Yes'])
            CholCheck = st.selectbox("}holesterol check in 5 years?", ['No', 'Yes'])
            BMI = st.slider("Body Mass Index (BMI)", 0, 45, 25)
            Smoker = st.selectbox("Smoker (Have you smoked at least 100 cigarettes in your entire life?)", ['No', 'Yes'])
            Stroke = st.selectbox("History of Stroke", ['No', 'Yes'])
            HeartDiseaseorAttack = st.selectbox("Heart Disease/Attack", ['No', 'Yes'])
            PhysActivity = st.selectbox("Physical activity in past 30 days (not including job)", ['No', 'Yes'])
            Fruits = st.selectbox("Eats Fruits", ['No', 'Yes'])
            Veggies = st.selectbox("Eats Vegetables", ['No', 'Yes'])

        with col2:
            HvyAlcoholConsump = st.selectbox("Heavy Alcohol (adult men having more than 14 drinks per week and adult women having more than 7 drinks per week)", ['No', 'Yes'])
            AnyHealthcare = st.selectbox("Has Healthcare Coverage", ['No', 'Yes'])
            NoDocbcCost = st.selectbox("Cost Prevents Doctor Visit", ['No', 'Yes'])
            GenHlth = st.slider("General Health (1=Excellent to 5=Poor)", 1, 5)
            MentHlth = st.slider("how many days during the past 30 days was your mental health not good?", 0, 30)
            PhysHlth = st.slider("how many days during the past 30 days was your physical health not good?", 0, 30)
            DiffWalk = st.selectbox("Difficulty Walking", ['No', 'Yes'])
            Sex = st.selectbox("Sex", ['Female', 'Male'])
            Age = st.slider("Age Group Code (level 1 >> 18:24 (Each level increases by 4 years) )", 1, 13)

        submitted = st.form_submit_button("🔍 Predict")

    if submitted:
        # Convert inputs to binary
        def bin(x): return 1 if x == 'Yes' else 0
        sex_val = 1 if Sex == 'Male' else 0

        features = np.array([[bin(HighBP), bin(HighChol), bin(CholCheck), BMI, bin(Smoker), bin(Stroke),
                              bin(HeartDiseaseorAttack), bin(PhysActivity), bin(Fruits), bin(Veggies),
                              bin(HvyAlcoholConsump), bin(AnyHealthcare), bin(NoDocbcCost), GenHlth,
                              MentHlth, PhysHlth, bin(DiffWalk), sex_val, Age]])

        prediction = model.predict(features)[0]

        st.subheader("Prediction Result")
        if prediction == 0:
            st.success("✅ Low Risk: No signs of diabetes or prediabetes.")
            st.image("https://static.vecteezy.com/system/resources/thumbnails/003/780/944/small_2x/businessman-standing-with-good-health-word-balloon-healthy-lifestyle-concept-vector.jpg", width=600)

        elif prediction == 1:
            st.warning("⚠ Moderate Risk: Prediabetes likely.")
            st.image("https://i.ytimg.com/vi/uKNft5xAk0E/maxresdefault.jpg", width=600)
        else:
            st.error("🚨 High Risk: Diabetes detected.")
            st.image("https://www.shutterstock.com/shutterstock/photos/2392588533/display_1500/stock-vector-diabetes-concept-tiny-characters-with-medical-equipment-blood-glucose-level-test-doctors-check-2392588533.jpg", width=600)


# Visualizations tab (placeholder)
elif menu == "📊 Visualizations":
    st.subheader("📊 Health Risk Visualizations")

    @st.cache_resource
    def get_fig_BMI(data):
        fig = px.scatter(data, x='BMI', y='Diabetes_012', trendline="ols",
                         title="Relationship between BMI and Diabetes",
                         color_discrete_sequence=["#ff7f0e"])
        fig.update_layout(title=dict(font=dict(size=20, color='blue'), x=0.5, xanchor='center', pad=dict(t=20)),
                          xaxis_title="BMI ", yaxis_title="Diabetes Risk Probability")
        return fig

    @st.cache_resource
    def get_fig_Age(data):
        fig = px.scatter(data, x='Age', y='Diabetes_012', trendline="ols",
                         title="Relationship between Age and Diabetes",
                         color_discrete_sequence=["#ff7f0e"])
        fig.update_layout(title=dict(font=dict(size=20, color='blue'), x=0.5, xanchor='center', pad=dict(t=20)),
                          xaxis_title="Age", yaxis_title="Diabetes Risk Probability")
        return fig

    @st.cache_resource
    def get_fig_PhysHlth(data):
        fig = px.scatter(data, x='PhysHlth', y='Diabetes_012', trendline="ols",
                         title="Relationship between PhysHlth and Diabetes",
                         color_discrete_sequence=["#ff7f0e"])
        fig.update_layout(title=dict(font=dict(size=20, color='blue'), x=0.5, xanchor='center', pad=dict(t=20)),
                          xaxis_title="Physical Health", yaxis_title="Diabetes Risk Probability")
        return fig
    @st.cache_resource
    def get_fig_GenHlth(data):
        fig = px.scatter(data, x='GenHlth', y='Diabetes_012', trendline="ols",
                         title="Relationship between GenHlth and Diabetes",
                         color_discrete_sequence=["#ff7f0e"])
        fig.update_layout(title=dict(font=dict(size=20, color='blue'), x=0.5, xanchor='center', pad=dict(t=20)),
                          xaxis_title="Genral Health", yaxis_title="Diabetes Risk Probability")
        return fig
    @st.cache_resource
    def get_fig_MentHlth(data):
        fig = px.scatter(data, x='MentHlth', y='Diabetes_012', trendline="ols",
                         title="Relationship between MentHlth and Diabetes",
                         color_discrete_sequence=["#ff7f0e"])
        fig.update_layout(title=dict(font=dict(size=20, color='blue'), x=0.5, xanchor='center', pad=dict(t=20)),
                          xaxis_title="Mental Health", yaxis_title="Diabetes Risk Probability")
        return fig



    risk_factor = st.sidebar.selectbox('Select Risk Factor', ['BMI', 'Age','Physical Health', 'Mental Health','Genral Health'])
    con = st.sidebar.button('Confirm')

    if con:
        if risk_factor == 'BMI':
            st.plotly_chart(get_fig_BMI(data), use_container_width=True)
            st.write("As Body Mass Index (BMI) increases, the likelihood of diabetes generally rises.")
        elif risk_factor == 'Age':
            st.plotly_chart(get_fig_Age(data), use_container_width=True)
            st.write("Older age groups show a higher probability of having diabetes or prediabetes.")
        elif risk_factor =='Physical Health':
            st.plotly_chart(get_fig_PhysHlth(data),use_container_width=True)
            st.write(" More days of poor physical health are associated with increased diabetes risk.")
        elif risk_factor =='Mental Health':
            st.plotly_chart(get_fig_MentHlth(data),use_container_width=True)
            st.write(" More days of poor Mental health are associated with increased diabetes risk.")
        else:
            st.plotly_chart(get_fig_GenHlth(data), use_container_width=True)
            st.write("Self-rated general health (on a scale from excellent to poor) strongly correlates with diabetes presence.")
