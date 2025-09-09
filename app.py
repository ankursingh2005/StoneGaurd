import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import io
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Set page configuration
st.set_page_config(
    page_title="NephroCare AI - Kidney Stone Management",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1E90FF;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #4682B4;
        margin-bottom: 1rem;
    }
    .highlight {
        background-color: #F0F8FF;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .doctor-card {
        background-color: #E6F2FF;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .prediction-positive {
        color: #FF4500;
        font-weight: bold;
    }
    .prediction-negative {
        color: #32CD32;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# App header
st.markdown('<h1 class="main-header">🧊 NephroCare AI</h1>', unsafe_allow_html=True)
st.markdown("### Advanced Kidney Stone Recurrence Prediction and Management System")

# Initialize session state
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {}
if 'reports_uploaded' not in st.session_state:
    st.session_state.reports_uploaded = False
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

# Sidebar for navigation
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/kidney.png", width=80)
    st.title("Navigation")
    app_page = st.radio("Go to", ["Patient Input", "Report Analysis", "Results & Recommendations", "Doctor Connect", "Health Tracker"])

    st.markdown("---")
    st.info("""
    **Disclaimer:** This application is for educational purposes only.
    Always consult healthcare professionals for medical advice.
    """)

# Mock database of doctors (in a real app, this would be a proper database)
doctors_db = [
    {"name": "Dr. Sarah Johnson", "specialty": "Nephrology", "experience": "15 years", "hospital": "City General Hospital", "rating": 4.8},
    {"name": "Dr. Michael Chen", "specialty": "Urology", "experience": "12 years", "hospital": "University Medical Center", "rating": 4.7},
    {"name": "Dr. Emily Rodriguez", "specialty": "Urological Surgery", "experience": "18 years", "hospital": "Regional Healthcare", "rating": 4.9},
    {"name": "Dr. James Wilson", "specialty": "Nephrology", "experience": "14 years", "hospital": "Metropolitan Hospital", "rating": 4.6},
    {"name": "Dr. Lisa Patel", "specialty": "Dietetics & Nutrition", "experience": "10 years", "hospital": "Wellness Center", "rating": 4.7}
]

# Food recommendations based on stone type
diet_recommendations = {
    "calcium_oxalate": {
        "avoid": ["Spinach", "Rhubarb", "Nuts", "Wheat bran", "Beets", "Tea", "Chocolate"],
        "consume": ["Calcium-rich foods with meals", "Citrus fruits", "Magnesium-rich foods", "Moderate protein"]
    },
    "uric_acid": {
        "avoid": ["Organ meats", "Anchovies", "Sardines", "High-purine foods", "Alcohol"],
        "consume": ["Low-purine diet", "Plenty of fluids", "Fruits and vegetables", "Low-fat dairy"]
    },
    "struvite": {
        "avoid": ["Foods that promote UTIs", "High-phosphorus foods"],
        "consume": ["Cranberry juice", "Probiotics", "Antibiotics as prescribed"]
    },
    "cystine": {
        "avoid": ["High-methionine foods", "Excessive protein"],
        "consume": ["High fluid intake", "Alkalinizing foods", "Specific medications"]
    }
}

# Patient Input Page
if app_page == "Patient Input":
    st.markdown('<h2 class="sub-header">Patient Information</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.session_state.patient_data['name'] = st.text_input("Full Name")
        st.session_state.patient_data['age'] = st.number_input("Age", min_value=1, max_value=100, value=30)
        st.session_state.patient_data['gender'] = st.selectbox("Gender", ["Male", "Female", "Other"])
        st.session_state.patient_data['weight'] = st.number_input("Weight (kg)", min_value=20, max_value=200, value=70)
        st.session_state.patient_data['height'] = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)

    with col2:
        st.session_state.patient_data['previous_operations'] = st.number_input("Number of previous kidney stone operations", min_value=0, max_value=10, value=1)
        st.session_state.patient_data['last_operation'] = st.date_input("Date of last operation", value=datetime.now() - timedelta(days=180))
        st.session_state.patient_data['family_history'] = st.selectbox("Family history of kidney stones", ["None", "One relative", "Multiple relatives"])
        st.session_state.patient_data['water_intake'] = st.slider("Daily water intake (glasses)", min_value=1, max_value=15, value=5)
        st.session_state.patient_data['diet'] = st.selectbox("Primary diet type", ["Mixed", "Vegetarian", "High-protein", "High-salt", "Other"])

    # Medical history
    st.markdown("### Medical History")
    medical_col1, medical_col2 = st.columns(2)

    with medical_col1:
        st.session_state.patient_data['hypertension'] = st.checkbox("Hypertension")
        st.session_state.patient_data['diabetes'] = st.checkbox("Diabetes")
        st.session_state.patient_data['uti_history'] = st.checkbox("Recurrent UTIs")

    with medical_col2:
        st.session_state.patient_data['kidney_disease'] = st.checkbox("Chronic Kidney Disease")
        st.session_state.patient_data['medications'] = st.text_input("Current medications")

    # Lifestyle factors
    st.markdown("### Lifestyle Factors")
    lifestyle_col1, lifestyle_col2 = st.columns(2)

    with lifestyle_col1:
        st.session_state.patient_data['activity_level'] = st.selectbox("Physical activity level",
                                                                     ["Sedentary", "Lightly active", "Moderately active", "Very active"])
        st.session_state.patient_data['smoking'] = st.selectbox("Smoking status", ["Never", "Former", "Current"])

    with lifestyle_col2:
        st.session_state.patient_data['alcohol'] = st.selectbox("Alcohol consumption",
                                                              ["None", "Occasional", "Moderate", "Heavy"])
        st.session_state.patient_data['stress_level'] = st.slider("Stress level (1-10)", min_value=1, max_value=10, value=5)

# Report Analysis Page
elif app_page == "Report Analysis":
    st.markdown('<h2 class="sub-header">Upload Medical Reports</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.info("Please upload clear images of your medical reports")
        xray_image = st.file_uploader("X-Ray Image", type=['png', 'jpg', 'jpeg'])
        ct_scan_image = st.file_uploader("CT Scan Image", type=['png', 'jpg', 'jpeg'])

    with col2:
        ultrasound_image = st.file_uploader("Ultrasound Image", type=['png', 'jpg', 'jpeg'])
        lab_report = st.file_uploader("Lab Report (PDF or image)", type=['pdf', 'png', 'jpg', 'jpeg'])

    if st.button("Analyze Reports"):
        if xray_image or ct_scan_image or ultrasound_image or lab_report:
            with st.spinner("Analyzing your reports with our AI engine..."):
                # Simulate processing time
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    # Simulate analysis process
                    time.sleep(0.02)
                    progress_bar.progress(percent_complete + 1)

                # Store mock analysis results
                st.session_state.reports_uploaded = True
                st.session_state.analysis_complete = True

                # Generate mock stone data
                stone_sizes = [random.uniform(2, 15) for _ in range(random.randint(1, 3))]
                st.session_state.patient_data['stone_sizes'] = stone_sizes
                st.session_state.patient_data['largest_stone'] = max(stone_sizes)
                st.session_state.patient_data['stone_count'] = len(stone_sizes)
                st.session_state.patient_data['stone_locations'] = random.sample([
                    "Right kidney upper pole", "Left kidney lower pole",
                    "Right ureter", "Left ureter", "Bladder"
                ], len(stone_sizes))

                # Predict stone type based on patient factors
                stone_types = ["Calcium Oxalate", "Uric Acid", "Struvite", "Cystine"]
                weights = [0.7, 0.15, 0.1, 0.05]  # Probability weights
                st.session_state.patient_data['stone_type'] = random.choices(stone_types, weights=weights)[0]

                # Calculate recurrence risk
                risk_factors = 0
                if st.session_state.patient_data['previous_operations'] > 1:
                    risk_factors += 2
                if st.session_state.patient_data['family_history'] != "None":
                    risk_factors += 1
                if st.session_state.patient_data['water_intake'] < 6:
                    risk_factors += 1
                if st.session_state.patient_data['diet'] in ["High-protein", "High-salt"]:
                    risk_factors += 1

                recurrence_risk = min(90, 30 + (risk_factors * 15))
                st.session_state.patient_data['recurrence_risk'] = recurrence_risk

                # Determine if surgery is needed
                surgery_needed = st.session_state.patient_data['largest_stone'] > 6 or any(
                    "ureter" in location for location in st.session_state.patient_data['stone_locations']
                )
                st.session_state.patient_data['surgery_needed'] = surgery_needed

            st.success("Analysis complete! Navigate to the Results page to see your report.")
        else:
            st.warning("Please upload at least one medical report to analyze.")

# Results & Recommendations Page
elif app_page == "Results & Recommendations":
    st.markdown('<h2 class="sub-header">Analysis Results & Recommendations</h2>', unsafe_allow_html=True)

    if not st.session_state.analysis_complete:
        st.warning("Please upload and analyze your medical reports first on the Report Analysis page.")
    else:
        # Display patient summary
        st.markdown("### Patient Summary")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Name", st.session_state.patient_data.get('name', 'Not provided'))
            st.metric("Age", st.session_state.patient_data.get('age', 'Not provided'))

        with col2:
            st.metric("Previous Operations", st.session_state.patient_data.get('previous_operations', 0))
            risk_level = "High" if st.session_state.patient_data.get('recurrence_risk', 0) > 50 else "Medium" if st.session_state.patient_data.get('recurrence_risk', 0) > 30 else "Low"
            st.metric("Recurrence Risk", f"{st.session_state.patient_data.get('recurrence_risk', 0)}%", risk_level)

        with col3:
            stone_status = "Surgery Recommended" if st.session_state.patient_data.get('surgery_needed', False) else "Can Pass Naturally"
            status_color = "red" if st.session_state.patient_data.get('surgery_needed', False) else "green"
            st.metric("Treatment Status", stone_status)
            st.metric("Stone Type", st.session_state.patient_data.get('stone_type', 'Unknown'))

        # Stone visualization
        st.markdown("### Stone Analysis")
        fig = go.Figure()

        if 'stone_sizes' in st.session_state.patient_data:
            for i, (size, location) in enumerate(zip(
                st.session_state.patient_data['stone_sizes'],
                st.session_state.patient_data['stone_locations']
            )):
                fig.add_trace(go.Bar(
                    x=[f"Stone {i+1}"],
                    y=[size],
                    name=f"{location} ({size:.1f}mm)",
                    hovertemplate=f"Location: {location}<br>Size: {size:.1f}mm<extra></extra>"
                ))

            fig.update_layout(
                title="Kidney Stone Sizes and Locations",
                xaxis_title="Stones",
                yaxis_title="Size (mm)",
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

        # Treatment recommendations
        st.markdown("### Treatment Recommendations")

        if st.session_state.patient_data.get('surgery_needed'):
            st.warning("""
            **Surgical intervention recommended** based on stone size and location.
            Options may include:
            - Extracorporeal Shock Wave Lithotripsy (ESWL)
            - Ureteroscopy
            - Percutaneous Nephrolithotomy (PCNL)
            """)
        else:
            st.success("""
            **Natural passage possible** with conservative management:
            - Increased water intake (3-4L daily)
            - Medical expulsive therapy
            - Pain management
            - Activity and positional techniques
            """)

        # Diet recommendations
        st.markdown("### Personalized Diet Plan")

        stone_type_key = st.session_state.patient_data.get('stone_type', '').lower().replace(' ', '_')
        if stone_type_key in diet_recommendations:
            rec = diet_recommendations[stone_type_key]

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Foods to Avoid")
                for food in rec['avoid']:
                    st.write(f"• {food}")

            with col2:
                st.markdown("#### Foods to Consume")
                for food in rec['consume']:
                    st.write(f"• {food}")
        else:
            st.info("General kidney stone prevention diet:")
            st.write("""
            - Drink 2.5-3L of water daily
            - Limit sodium intake to <2300mg/day
            - Consume moderate amounts of animal protein
            - Include citrus fruits and juices
            - Ensure adequate calcium from food sources
            """)

        # Prevention strategies
        st.markdown("### Recurrence Prevention Strategies")

        prevention_col1, prevention_col2, prevention_col3 = st.columns(3)

        with prevention_col1:
            st.markdown("**Hydration**")
            st.write(f"Target: {max(8, st.session_state.patient_data.get('water_intake', 5) + 3)} glasses daily")
            st.progress(min(1.0, (st.session_state.patient_data.get('water_intake', 5) / 12)))

        with prevention_col2:
            st.markdown("**Diet Modification**")
            if st.session_state.patient_data.get('diet') in ['High-protein', 'High-salt']:
                st.error("Modify current diet")
                st.write("Reduce protein/salt intake")
            else:
                st.success("Diet appears balanced")
                st.write("Maintain current patterns")

        with prevention_col3:
            st.markdown("**Monitoring**")
            st.write("Follow-up imaging recommended in:")
            st.metric("", "6 months" if st.session_state.patient_data.get('recurrence_risk', 0) > 50 else "12 months")

# Doctor Connect Page
elif app_page == "Doctor Connect":
    st.markdown('<h2 class="sub-header">Connect with Specialist Doctors</h2>', unsafe_allow_html=True)

    st.info("Based on your condition, we recommend these specialists:")

    for i, doctor in enumerate(doctors_db):
        with st.container():
            st.markdown(f'<div class="doctor-card">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 3, 1])

            with col1:
                st.image("https://img.icons8.com/color/96/000000/doctor-male.png", width=80)

            with col2:
                st.subheader(doctor['name'])
                st.write(f"**Specialty:** {doctor['specialty']}")
                st.write(f"**Experience:** {doctor['experience']}")
                st.write(f"**Hospital:** {doctor['hospital']}")

            with col3:
                st.write(f"**Rating:** {doctor['rating']}/5.0")
                if st.button("Book Consultation", key=f"doc_{i}"):
                    st.success(f"Consultation request sent to {doctor['name']}!")

            st.markdown('</div>', unsafe_allow_html=True)

    # Telemedicine option
    st.markdown("---")
    st.markdown("### Virtual Consultation")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Schedule a video consultation with available specialists:")
        appointment_date = st.date_input("Preferred Date", min_value=datetime.now().date())
        appointment_time = st.selectbox("Preferred Time", ["9:00 AM", "11:00 AM", "2:00 PM", "4:00 PM", "6:00 PM"])

        if st.button("Schedule Virtual Visit"):
            st.success(f"Virtual consultation scheduled for {appointment_date} at {appointment_time}")

    with col2:
        st.write("**Upload additional documents for your consultation:**")
        additional_docs = st.file_uploader("Medical records", type=['pdf', 'jpg', 'png'], accept_multiple_files=True)
        if additional_docs:
            st.info(f"{len(additional_docs)} files ready for consultation")

# Health Tracker Page
elif app_page == "Health Tracker":
    st.markdown('<h2 class="sub-header">Kidney Health Monitoring</h2>', unsafe_allow_html=True)

    st.markdown("### Daily Health Log")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Today's Input**")
        water_intake = st.slider("Water intake (glasses)", 0, 15, st.session_state.patient_data.get('water_intake', 5), key='daily_water')
        pain_level = st.slider("Pain level (0-10)", 0, 10, 0)
        medication_taken = st.checkbox("Taken prescribed medication today")
        symptoms = st.multiselect("Symptoms experienced",
                                 ["Back pain", "Abdominal pain", "Frequent urination",
                                  "Blood in urine", "Nausea", "Fever", "None"])

    with col2:
        st.write("**Diet Log**")
        protein_intake = st.selectbox("Protein consumption", ["Low", "Moderate", "High"])
        sodium_intake = st.selectbox("Sodium consumption", ["Low", "Moderate", "High"])
        oxalate_foods = st.multiselect("High-oxalate foods consumed",
                                      ["Spinach", "Nuts", "Beets", "Tea", "Chocolate", "Berries", "None"])
        citrus_intake = st.checkbox("Consumed citrus fruits/juices today")

    if st.button("Save Daily Entry"):
        st.success("Daily health data saved successfully!")

    st.markdown("---")
    st.markdown("### Health Progress Dashboard")

    # Generate sample progress data
    dates = pd.date_range(end=datetime.today(), periods=30, freq='D')
    water_data = [random.randint(4, 10) for _ in range(30)]
    pain_data = [random.randint(0, 7) for _ in range(30)]

    tab1, tab2, tab3 = st.tabs(["Hydration", "Symptoms", "Risk Trends"])

    with tab1:
        fig = px.line(x=dates, y=water_data, title="Daily Water Intake", labels={'x': 'Date', 'y': 'Glasses of Water'})
        fig.add_hline(y=8, line_dash="dash", line_color="green", annotation_text="Target")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig = px.bar(x=dates, y=pain_data, title="Daily Pain Level", labels={'x': 'Date', 'y': 'Pain Level (0-10)'})
        fig.add_hline(y=3, line_dash="dash", line_color="orange", annotation_text="Concern Level")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        risk_trend = [max(10, min(90, st.session_state.patient_data.get('recurrence_risk', 30) + random.randint(-5, 5))) for _ in range(30)]
        fig = px.line(x=dates, y=risk_trend, title="Recurrence Risk Trend", labels={'x': 'Date', 'y': 'Risk Percentage'})
        fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Low Risk")
        fig.add_hline(y=50, line_dash="dash", line_color="orange", annotation_text="Medium Risk")
        fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="High Risk")
        st.plotly_chart(fig, use_container_width=True)

    # Reminders and alerts
    st.markdown("### Health Reminders")
    reminder_col1, reminder_col2, reminder_col3 = st.columns(3)

    with reminder_col1:
        st.info("**Next Doctor Visit**")
        st.write("Scheduled in 30 days")
        st.button("Reschedule", key="reschedule")

    with reminder_col2:
        st.warning("**Lab Tests Due**")
        st.write("Urine analysis needed")
        st.button("Order Test", key="order_test")

    with reminder_col3:
        st.error("**Medication Refill**")
        st.write("Due in 5 days")
        st.button("Request Refill", key="request_refill")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>NephroCare AI - Advanced Kidney Stone Management System</p>
        <p>For educational purposes only | Always consult healthcare professionals for medical advice</p>
    </div>
""", unsafe_allow_html=True)