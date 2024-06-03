import streamlit as st

# Set the title of the app
st.title("Addition of Two Numbers")

# Get user input for the first number
num1 = st.number_input("Enter the first number:", value=0)

# Get user input for the second number
num2 = st.number_input("Enter the second number:", value=0)

# Add the two numbers
result = num1 + num2

# Display the result
st.write("The result of the addition is:", result)