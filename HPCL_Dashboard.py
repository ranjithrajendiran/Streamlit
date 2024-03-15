import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import glob
from cryptography.fernet import Fernet
import paramiko


st.set_page_config(page_title="HPCL Dashboard", page_icon="data:image/png;base64,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", layout="wide")

with open(r"D:\\HPCL_Report_Summary\\Credentials\\HPCL_encryption_key.key", "rb") as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

with open(r"D:\\HPCL_Report_Summary\\Credentials\\HPCL_encrypted_credentials.txt", "rb") as cred_file:
    encrypted_username = cred_file.readline()
    encrypted_password = cred_file.readline()
    

def download_file_sftp(hostname, port, username, password, remote_file_path, local_file_path):
    try:
       
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)  

        sftp = paramiko.SFTPClient.from_transport(transport)

        try:
            sftp.stat(remote_file_path)
        except FileNotFoundError:
            print("Remote file not found.")
            return

     
        sftp.get(remote_file_path, local_file_path)
        print(f"File '{remote_file_path}' downloaded to '{local_file_path}'.")

    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
    except paramiko.SSHException as e:
        print(f"Unable to establish SSH connection: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        try:
         
            sftp.close()
            transport.close()
        except NameError:
          
            pass

hostname = 'sftp.pinelabs.com'
port = 22
username = cipher_suite.decrypt(encrypted_username).decode()
password = cipher_suite.decrypt(encrypted_password).decode()

remote_file_path = '/DATA/HPCL_Project/Project status.xlsx'

local_file_path = 'Project status.xlsx'

download_file_sftp(hostname, port, username, password, remote_file_path, local_file_path)

def load_data(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    return df

def generate_card_chart(col, user_custom_name, additional_card_background_color, card_index, calculation, font_size=24):
    col.markdown(
        f"""
        <div style="display: flex; flex-direction: column; align-items: center; width: 90%; height: 150px; border: 2px solid #b0c4de; border-radius: 10px; background-color: {additional_card_background_color}; color: #000000; margin-bottom: 10px; margin-top: 20px; {'clear: both;' if card_index % 4 == 0 else ''}">
            <p style="font-size: 17px; text-align: center; margin: 0; line-height: 50px; ">{user_custom_name}</p>
            <p style="font-size: 38px; text-align: center; margin: 0;">{calculation}</p>
        </div>
        """, unsafe_allow_html=True)



def load_credentials_from_config(directory='D:\\Streamlit\\Credentials', filename='config.json'):
    filepath = os.path.join(directory, filename)
    try:
        with open(filepath, 'r') as f:
            config_data = json.load(f)
            return config_data
    except FileNotFoundError:
        print(f"Error: {filepath} not found. Please generate usernames and passwords first.")
        return []


credentials_directory = 'D:\\Streamlit\\Credentials'
valid_credentials = load_credentials_from_config(directory=credentials_directory)
formatted_credentials = [{"username": username, "password": password} for username, password in valid_credentials]
valid_credentials = formatted_credentials

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

            if login_button:
                for user_data in valid_credentials:
                    if username == user_data["username"] and password == user_data["password"]:
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

            return False #old
        




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
  
 
    default_file_path = "D:\HPCL_Report_Summary\Project status.xlsx"

    df = load_data(default_file_path)

    if df.empty:
        st.warning("Failed to fetch data.")
        return

    image_url = "https://www.pinelabs.com/img/logo.png?version=6.1.9"
    
    st.sidebar.markdown(
    f"<div style='display: flex; justify-content: center; align-items: center; text-align: center;'><img src='{image_url}'></div>",
    unsafe_allow_html=True
)
    
    
    st.sidebar.markdown(
    """
    <style>
        .sidebar-header {
            text-align: center;
            padding: 10px;
            background-color: #003323;  
            color: yellow;  
            box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.5);  
        }
    </style>
    """,
    unsafe_allow_html=True
)
    
    
    if st.sidebar.button("🌀 Refresh", key="refresh_button", help="Click to refresh the page", use_container_width=True,type="primary"):
        st.rerun()



    st.sidebar.markdown("<h2 class='sidebar-header'>Master Filter</h2>", unsafe_allow_html=True)
    st.sidebar.markdown('')

    
    filtered_df=df.copy()
    
    selected_Zone = st.sidebar.multiselect("Select Zone", list(df["Zone"].unique()))
    selected_Region = st.sidebar.multiselect("Select Region", list(df["Region"].unique()))
    selected_State = st.sidebar.multiselect("Select State", list(df["State"].unique()))
    selected_SAP_CC = st.sidebar.multiselect("Select SAP CC", list(df["SAP CC"].unique()))
    selected_RO_NAME = st.sidebar.multiselect("Select RO NAME", list(df["RO NAME"].unique()))
    
   
    
    if selected_Zone:
        filtered_df = filtered_df[filtered_df["Zone"].isin(selected_Zone)]
    
    if selected_Region:
        filtered_df = filtered_df[filtered_df["Region"].isin(selected_Region)]
    
    if selected_State:
        filtered_df = filtered_df[filtered_df["State"].isin(selected_State)]
    
    if selected_SAP_CC:
        filtered_df = filtered_df[filtered_df["SAP CC"].isin(selected_SAP_CC)]
    
    if selected_RO_NAME:
        filtered_df = filtered_df[filtered_df["RO NAME"].isin(selected_RO_NAME)]
    
  
    st.markdown('')

    if not filtered_df.empty:
        
        scrolling_messages = []
    
        pending_sat_count = filtered_df["SAT Date"].isnull().sum()
        pending_power_on_count = filtered_df["Power on Date"].isnull().sum()
        
        formatted_message = (
            f"<span style='color: darkred; font-family: Trebuchet MS; font-size: 18px;'>"
            f"Pending SAT Count: <span style='font-weight: bold;'>{pending_sat_count}</span> | "
            f"Pending Power on Count: <span style='font-weight: bold;'>{pending_power_on_count}</span>"
            f"</span>"
        )
        
        scrolling_messages.append(formatted_message)
        
        messages_combined = " | ".join(scrolling_messages)
        
        st.markdown(f'<marquee behavior="scroll" direction="left" style="white-space: nowrap;">{messages_combined}</marquee>', unsafe_allow_html=True)
    
        predefined_card_charts = [
            
            {
                "column": "RO NAME",
                "background_color": "#20D39C",
                "custom_name": "Total Outlets",
                "calculation": filtered_df["RO NAME"].count(),
            },
            
            {
                "column": "RO NAME",
                "background_color": "#FFAA37",
                "custom_name": "Total PO Received",
                "calculation":  filtered_df["RO NAME"].count(),  # Round and convert to integer
            },
    
            {
                "column": "Power on Date",
                "background_color": "#5AE2E2",
                "custom_name": "Total Power on Done",
                "calculation": filtered_df['Power on Date'].notnull().sum()
                },
            {
                "column": "SAT Date",
                "background_color": "#78ADF9",
                "custom_name": "Total SAT Done",
                "calculation": filtered_df['SAT Date'].notnull().sum()
            },
        ]
    
        col1, col2, col3, col4 = st.columns(4)
        
        
        for i, chart_info in enumerate(predefined_card_charts):
            user_custom_name = chart_info["custom_name"]
            additional_card_background_color = chart_info["background_color"]
            calculation = chart_info["calculation"]
        
            col = [col1, col2, col3, col4][i]
            generate_card_chart(col, user_custom_name, additional_card_background_color, i + 1, calculation)
            
        st.markdown("")  
        
        custom_styles = """
            <style>
                .subheader-text {
                    font-size: 26px;
                    font-weight: bold;
                    color: #003323;  /* Change the color as needed */
                    margin-top: -30px;  /* Adjust the top margin */
                    margin-bottom: 0px;
                }
            </style>
        """
        
        st.markdown(custom_styles, unsafe_allow_html=True)
        
        st.markdown("<p class='subheader-text'>Project Summary</p>", unsafe_allow_html=True)
        filtered_df.columns =  filtered_df.columns.str.strip()
        
    
        filtered_df['SAT Call WIP'] = filtered_df['SAT Call']
    
        filtered_df.columns = filtered_df.columns.str.strip()
    
    
        columns_to_lowercase = ['Survey status', 'BOM Approval sent', 'BOM Approved', 'TPI', 'BOM Dispatch status - WFCC', 'BOM Deliverd', 'Civil  & electrical','Power On','Observation','SAT Call','SAT Call WIP','Warrenty status']
        filtered_df[columns_to_lowercase] = filtered_df[columns_to_lowercase].apply(lambda x: x.astype(str).str.lower())
    
        filtered_df['Observation'] = filtered_df['Observation'].astype(str).str.lower().str.strip()
    
        summary_filtered_df = filtered_df.groupby(['Zone', 'Region']).agg({
            'RO NAME': 'nunique',
            'SAP CC': 'count',
            'Survey status': lambda x: (x == 'completed').sum(),
            'BOM Approval sent': lambda x: (x == 'completed').sum(),
            'BOM Approved': lambda x: (x == 'completed').sum(),
            'TPI': lambda x: (x == 'completed').sum(),
            'BOM Dispatch status - WFCC': lambda x: (x == 'yes').sum() ,
            'BOM Deliverd'  :lambda x: (x == 'yes').sum() ,
            'Civil  & electrical'  :  lambda x: (x == 'completed').sum(), 
            'Power On':lambda x: (x == 'yes').sum(),
            'Observation' : lambda x: (x == 'completed').sum(),
            'SAT Call WIP' :lambda x: (x != 'yes').sum(),
            'SAT Call' :lambda x: (x == 'yes').sum(),
            'Warrenty status' : lambda x: (x == 'yes').sum(),
            
    
        }).reset_index()
    
        summary_filtered_df.rename(columns={'RO NAME': 'Outlets Awarded','SAP CC': 'PO Received','Survey status': 'Survey Done'
                                   ,'TPI':'TPI Completed','BOM Dispatch status - WFCC':'BOM Dispatched','Civil  & electrical' :'Mechanical Work done',
                                   'Power On' :'Power on Done','Observation' :'Observation completed', 'SAT Call WIP' :'SAT Call given',
                                   'SAT Call' :'SAT Done','Warrenty status' : 'Warranty status'
                                   
                                   }, inplace=True)
    
    
    
    
        st.dataframe(summary_filtered_df,hide_index=True)
        
    
        
        st.markdown("") 
        st.markdown(
           """
           <style>
               .subheader-text {
                   font-size: 28px;
                   font-weight: bold;
                   text-align: center;
                   margin-left: -20px;
               }
               .centered-chart {
                   margin: auto; 
               }
           </style>
           """,
           unsafe_allow_html=True
        )
    
        st.markdown("<p class='subheader-text'>Project Data</p>", unsafe_allow_html=True)
        
        filtered_df['SAP CC'] = filtered_df['SAP CC'].astype(str)
    
        st.dataframe(filtered_df, hide_index=True)
        
        st.markdown("") 
        st.markdown("<p class='subheader-text'>User Remarks</p>", unsafe_allow_html=True)
        st.info('Please Click Submit Button After Entering Remarks', icon="ℹ️")
        
                        
        def save_data_to_csv(data, folder='user_data', filename='user_data.csv'):
            if not os.path.exists(folder):
                os.makedirs(folder)
        
            existing_files = glob.glob(f'{folder}/user_data_*.csv')
            for file in existing_files:
                os.remove(file)
        
            data['Remarks'] = data['Remarks'].replace('', pd.NA)
        
            data = data.dropna(subset=['Remarks'])
        
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename_with_timestamp = f'{folder}/user_data_{timestamp}.csv'
            data.to_csv(filename_with_timestamp, index=False)
        
            concatenate_files(folder)
        
        def concatenate_files(folder='user_data', output_filename='merged_user_data.csv'):
            try:
                files = glob.glob(f'{folder}/user_data_*.csv')
                if files:
                    existing_data = pd.read_csv(output_filename) if os.path.exists(output_filename) else pd.DataFrame()
        
                    dfs = [existing_data] + [pd.read_csv(file).dropna(axis=1, how='all') for file in files]
        
                    merged_data = pd.concat(dfs, ignore_index=True)
        
                    merged_data.sort_values(['SAP CC', 'Last Modified Date'], ascending=[False, False], inplace=True)
                    merged_data.drop_duplicates('SAP CC', keep='first', inplace=True)
        
                    merged_data.to_csv(output_filename, index=False)
                    st.success("Remarks Updated Successfully.", icon="✅")
            except PermissionError:
                st.error("PermissionError: You do not have permission to save the merged data file. Please check file permissions.")
        def load_data_from_csv(folder='user_data', filename='user_data.csv'):
            try:
                data = pd.read_csv(f'{folder}/{filename}')
                return data
            except FileNotFoundError:
                return pd.DataFrame(columns=['SAP CC', 'Remarks', 'Last Modified Date'])
        
        
        user_data = load_data_from_csv()
        
        idf = filtered_df[['SAP CC']].copy()
        idf['Remarks'] = ''
        idf['Last Modified Date'] = 'it will be automatically captured.'
                     
        idf = st.data_editor(
            idf,
            column_config={
                "SAP CC": st.column_config.TextColumn(
                    "SAP CC",
                    help="This column is not editable",
                    disabled=True,
                ),
                "Remarks": "Remarks",
                "Last Modified Date": "Last Modified Date",
            },
            width=900,
            height=450,
            key='user_data_editor',
            hide_index=True,
        )
        
        if st.button("Submit", key="submit_button", help="Click to Save the Remarks", type="primary"):
            if idf['Remarks'].eq('').all():
                st.warning("⚠️ Please enter remarks before submitting.")
            else:
                user_data[['SAP CC', 'Remarks', 'Last Modified Date']] = idf[['SAP CC', 'Remarks', 'Last Modified Date']]
        
                user_data['Last Modified Date'] = pd.to_datetime('now').strftime('%Y-%m-%d %H:%M:%S')
        
                save_data_to_csv(user_data)
            
        st.markdown("")     
        st.sidebar.markdown("<h2 class='sidebar-header'>Remarks Table Filter</h2>", unsafe_allow_html=True)
        st.sidebar.markdown('')
        
        st.markdown("<p class='subheader-text'>Remarks Table</p>", unsafe_allow_html=True)
        def load_merged_data(filename='merged_user_data.csv'):
            try:
                data = pd.read_csv(filename)
                return data
            except FileNotFoundError:
                st.error(f"File '{filename}' not found.")
                return pd.DataFrame()
        
        merged_data1 = load_merged_data()
        filtered_data = merged_data1.copy()  # Create a copy for filtering
        
        filtered_data = filtered_data.dropna(subset=['SAP CC'])

        filtered_data['SAP CC'] = filtered_data['SAP CC'].astype('Int64').astype(str)
        
        unique_sap_cc_values = filtered_data['SAP CC'].unique()
        selected_sap_cc_values = st.sidebar.multiselect("Filter by SAP CC", unique_sap_cc_values, default=[])
        
        if selected_sap_cc_values:
            filtered_data = filtered_data[filtered_data['SAP CC'].isin(selected_sap_cc_values)]
        
        unique_last_modified_dates = filtered_data['Last Modified Date'].unique()
        selected_last_modified_dates = st.sidebar.multiselect("Filter by Last Modified Date", unique_last_modified_dates, default=[])
        
        if selected_last_modified_dates:
            filtered_data['Last Modified Date'] = pd.to_datetime(filtered_data['Last Modified Date'])
            filtered_data = filtered_data[filtered_data['Last Modified Date'].isin(selected_last_modified_dates)]
        
        
        
        st.dataframe(filtered_data.astype({'SAP CC': str}), hide_index=True,width=900,height=450)
        
        st.sidebar.info("Discover additional functionalities at the table's top-right corner, offering features such as expanding the view and effortlessly downloading the data", icon="💡")
        
        
        
        if st.sidebar.button("⏩ Logout", key="logout_button", help="Click to log out", on_click=logout, use_container_width=True,type="primary"):
            st.success("Logged out successfully.")
            st.experimental_rerun()
      
                
    else:
        flashing_warning_style = """
            <style>
                @keyframes flash {
                    0% { opacity: 1; }
                    50% { opacity: 0; }
                    100% { opacity: 1; }
                }
        
                .flashing-warning {
                    animation: flash 6s infinite; 
                }
            </style>
            
            <div style="margin-top: 20px;"></div> <!-- Empty line -->
            
            <div class="flashing-warning" style="padding: 10px; border: 1px solid #d33; border-radius: 5px; background-color: #F1C40F; color: #333333; text-align: center; ">
                <p>No data matches for the selected filter criteria!</p>
            </div>
        """
        
        st.markdown(flashing_warning_style, unsafe_allow_html=True)
   
if __name__ == "__main__":
    main()

      
