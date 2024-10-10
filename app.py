import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from black_scholes import black_scholes
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Inject custom CSS for white tones and black text
st.markdown(
    """
    <style>
    /* General body styling */
    body {
        background-color: blue; /* White background */
    }
    
    /* Custom header */
    .app-title {
        font-size: 36px;
        font-family: 'Arial', sans-serif;
        color: white; /* white text for title */
        text-align: center;
        padding-bottom: 20px;
    }
    
    /* Inputs and buttons */
    .stButton>button {
        background-color: #DDDDDD; /* Light grey button */
        color: black; /* Black text */
        padding: 12px 24px;
        font-size: 16px;
        border-radius: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #CCCCCC; /* Darker grey on hover */
    }

    .stNumberInput, .stSelectbox {
        background-color: black; /* White inputs */
        color: black; /* Black text */
        border: 2px solid #CCCCCC; /* Light grey borders */
        border-radius: 8px;
        padding: 10px;
    }

    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: white; /* White sidebar */
        color: black; /* Black text */
        font-family: 'Arial', sans-serif;
    }

    /* Custom footer styling */
    footer {
        font-size: 12px;
        color: black;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App title
st.markdown("<h1 class='app-title'>Modern Black-Scholes Option Pricer</h1>", unsafe_allow_html=True)

# Sidebar for navigation or instructions
st.sidebar.title("Navigation")
st.sidebar.markdown("This app allows you to calculate option prices using the Black-Scholes model. Choose your parameters from the inputs.")

# Heatmap function
def generate_heatmap(S, K, T, r, sigma_range, S_range, option_type='call'):
    sigma_values = np.linspace(*sigma_range, 20)  # Reduced resolution
    S_values = np.linspace(*S_range, 20)         # Reduced resolution
    
    price_matrix = np.zeros((len(S_values), len(sigma_values)))
    
    for i, S_val in enumerate(S_values):
        for j, sigma_val in enumerate(sigma_values):
            price_matrix[i, j] = black_scholes(S_val, K, T, r, sigma_val, option_type)
    
    plt.figure(figsize=(12, 8))  # Increase figure size for better clarity
    
    sns.heatmap(price_matrix, xticklabels=np.round(sigma_values, 2), yticklabels=np.round(S_values, 2), cmap='RdYlGn', annot=True)
    
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.yticks(rotation=0)  # Ensure y-axis labels are horizontal

    plt.xlabel('Volatility (σ)')
    plt.ylabel('Stock Price (S)')
    plt.title(f'{option_type.capitalize()} Option Price Heatmap')

    # Save the heatmap image to send as an email attachment
    plt.savefig('heatmap.png')
    st.pyplot(plt)

# Function to send heatmap via email
def send_email(recipient_email):
    sender_email = 'your-email@example.com'
    sender_password = 'your-password'
    
    subject = "Your Black-Scholes Option Price Heatmap"
    body = "Attached is your generated heatmap from the Black-Scholes option pricer."

    # Create email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the body text
    msg.attach(MIMEText(body, 'plain'))

    # Attach the heatmap
    with open('heatmap.png', 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= heatmap.png")
        msg.attach(part)

    # Send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        st.success(f"Email sent to {recipient_email}")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Layout with columns
col1, col2 = st.columns(2)

# User inputs for option parameters in the first column
with col1:
    st.subheader("Option Parameters")
    S = st.number_input('Stock Price (S)', value=100.0)
    K = st.number_input('Strike Price (K)', value=100.0)
    T = st.number_input('Time to Expiration (T) in years', value=1.0)
    r = st.number_input('Risk-Free Interest Rate (r)', value=0.05)
    sigma = st.number_input('Volatility (σ)', value=0.2)
    option_type = st.selectbox('Option Type', ('call', 'put'))

# Second column for action buttons
with col2:
    st.subheader("Actions")
    if st.button('Calculate'):
        price = black_scholes(S, K, T, r, sigma, option_type)
        st.success(f"The {option_type} option price is: {price}")

    # Heatmap section
    sigma_range = (0.1, 0.5)
    S_range = (50, 150)

    if st.button('Generate Heatmap'):
        generate_heatmap(S, K, T, r, sigma_range, S_range, option_type)

    # Email heatmap section
    recipient_email = st.text_input('Enter your email to receive the heatmap:')
    if st.button('Email Heatmap'):
        if recipient_email:
            send_email(recipient_email)
        else:
            st.error('Please enter a valid email address.')

# Footer
st.markdown("<footer>Made with ❤️ using Streamlit</footer>", unsafe_allow_html=True)