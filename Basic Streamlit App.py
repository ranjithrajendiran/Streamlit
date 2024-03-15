
import streamlit as st



st.set_page_config(page_title="HPCL Dashboard", page_icon="data:image/png;base64,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", layout="wide")
# Load the secrets from the TOML file


def login():
    message_color = "#003323"
    text_color = "#003323"
    
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: flex-start; background-color: white;">
            <h2 style="color: {message_color};"><b>Welcome to Dashboard</b></h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        
        image_url = "https://www.pinelabs.com/img/logo.png?version=6.1.9"

        st.markdown(
            f"<div style='display: flex; justify-content: center;'><img src='{image_url}'></div>",
            unsafe_allow_html=True
        )
        with st.form("login_form"):
            username = st.text_input("Username:")
            password = st.text_input("Password:", type="password")
            login_button = st.form_submit_button("Login")

            admin_username = "admin"  # Define admin username
            admin_password = "admin123"  # Define admin password

            if login_button:
                if username == admin_username and password == admin_password:
                    st.success("Login successful!")
                    return True

                st.error("Invalid username or password. Please try again.")
                
    
            scrollable_text = f"<b style='color: {text_color}; animation: flash 1s infinite;'>Our platform, your move</b> 📈"

            st.markdown(
                f"""
                <style>
                    @keyframes flash {{
                        0%, 49%, 100% {{
                            opacity: 1;
                        }}
                        50% {{
                            opacity: 0;
                        }}
                    }}
                </style>
                <div style='white-space: nowrap; overflow: hidden; width: 100%;'>
                    <marquee scrollamount='5' direction='left'>{scrollable_text}</marquee>
                </div>
                """,
                unsafe_allow_html=True
            )

            return False




def logout():
    st.session_state.is_logged_in = False
    

def main():
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False

    if not st.session_state.is_logged_in:
        if login():
            st.session_state.is_logged_in = True
            st.rerun()
        else:
            return

        st.empty()
    st.markdown(
        """
        <style>
            .title-box {
                text-align: center;
                padding: 10px 20px;  
                background-color: #003323;  
                color: white;  
                width: 100%;  
                height: fit-content;  
            }
            .first-line {
                font-weight: bold;
                font-size: 30px;  
                color: yellow;  
                margin-bottom: 0;  
            }
            .second-line {
                font-size: 18px;  
                margin-top: 0;  
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    
    st.markdown("<div class='title-box'><p class='first-line'>HPCL Report Summary</p>", unsafe_allow_html=True)
  
 

   
if __name__ == "__main__":
    main()

      
