import streamlit as st

def main():
    st.title("Welcome to My Streamlit App")
    st.write("This is a simple Streamlit app for testing deployment.")

    # Add some interactive widgets
    st.sidebar.header("User Input")
    name = st.sidebar.text_input("Enter your name", "John Doe")
    age = st.sidebar.number_input("Enter your age", min_value=0, max_value=150, value=30)

    # Display the user input
    st.write(f"Hello, {name}! You are {age} years old.")

if __name__ == "__main__":
    main()
