import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
# load all the environment variables
load_dotenv()
import google.generativeai as genai
## configure API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Function to retrieve query from the sql database
def read_query(sql,db):
    conn=sqlite3.connect(db)
    cursor=conn.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    conn.commit()
    conn.close()
    return rows

# Function to load Google Gemini Model and provide query as response
def get_response(que):
# Define Prompt
    prompt="""
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENTS and has the following columns - NAME, CLASS, Marks, Company\n\nFor example,\nExample 1 - How many entries of records are present?,
    the SQL command will be something like this:SELECT COUNT(*) FROM STUDENTS;
    \nExample 2 - Tell me all the students studying in MCOM class?,
    the SQL command will be something like this:SELECT * FROM STUDENTS WHERE CLASS="MCOM"; 
    Only return SQL query. Do not add explanation"""
    model=genai.GenerativeModel(model_name="gemini-2.5-flash")
    response=model.generate_content(f"{prompt}  \n  {que}")
    return response.text.strip()

 
def page_home():
    st.markdown("""
        <style>
            .stApp {
              background-color: #2E2E2F;
            }
            h1, h2, h3 {
             color: #4CAF50 !important;
            }
            .main-title {
                text-align: center;
                font-size: 2.5em;
                color: #4CAF50 !important;
            }
            .sub-title {
                text-align: center;
                font-size: 1.5em;;
                color: #4CAF50 !important;
            }

            .offerings  {
                padding: 20px;
                color: white !important;
            }
            .offerings h2 {
                colour: #4CAF50;
            }
            .offerings ul {
                list-style-type: none;
                padding: 0;
            }

            .offerings li {
                font-size: 18px;
                margin-bottom: 10px;
            }

            .custom-sidebar {
                background-color: #2E2E2E;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 class='main-title'>Welcome to IntelliSQL</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-title'>Revolutionizing Database Querying with Advanced LLM Capabilities.</h2>",unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.image("https://static.vecteezy.com/system/resources/previews/066/829/737/non_2x/data-warehouse-icon-concept-in-blue-color-vector.jpg")

    with col2:
        st.markdown("""
        <div class='offerings'>
            <h2>Wide Range of Offerings</h2>
            <ul>
                <li>💡 Intelligent Query Assistance</li>
                <li>📊 Data Visualization Insights</li>
                <li>⚡ Efficient Data Retrieval</li>
                <li>🚀 Performance Optimization</li>
                <li>💬 Syntax Suggestions</li>
                <li>📈 Trend Analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
# Function to Render About Page
def page_about():
    st.markdown("""
        <style>
            .stApp {
             background-color: #2E2E2F;
            }
            html,body, [class*="css"] {
            color: white !important;  /* White color for body text */
            }
            h1{
                color: #4CAF50 !important;
            }
            p{
                font-size: 20px;
                line_height: 1.6;
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='color: #4CAF50;'>About IntelliSQL</h1>",unsafe_allow_html=True)
    st.markdown("<div class='content'>",unsafe_allow_html=True)
    st.markdown("""<p>IntelliSQL is an innovative project aimed at revolutionizing database querying using advanced language model capabilities.Powered by cutting-edge LLM(Large Language Model) architecture,this system offers users an intelligent platform for interacting with SQL databases effortlessly and intuitively.</p>""",unsafe_allow_html=True)
    st.markdown("</div>",unsafe_allow_html=True)
    st.image("https://download.logo.wine/logo/Oracle_SQL_Developer/Oracle_SQL_Developer-Logo.wine.png")
# Intelligent Query Assistance Page
def page_intelligent_query_assistance():
    st.markdown("""
        <style>
            .stApp {
              background-color: #2E2E2F;
            }
            h1{
                color: #4CAF50 !important;
            }
            h6{
                color: white !important;
            }
            .tool-input {
                margin-bottom: 20px;
                color: white !important;  /* White color for body text */
            }
            .response {
                margin-top: 20px;
                color: #FFFF00 !important;  /* Yellow color for output */
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>Intelligent Query Assistance</h1>",unsafe_allow_html=True)
    st.write("""
        IntelliSQL enhances the querying process by providing intelligent assistance to users, whether they are novice or experienced users.""",unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<div class='tool-input'>", unsafe_allow_html=True)
        que = st.text_input("Enter Your Query:", key="sql_query")
        submit = st.button("Get Answer",key="submit_button",help="Click to retrieve the SQL data")
        st.markdown("</div>", unsafe_allow_html=True)

        if submit and que:
            try:
                response=get_response(que)
                st.write(f"**Generated SQL Query:** '<span style='color: #FFFF00;'>{response}</span>'", unsafe_allow_html=True)
                response = read_query(response, "data.db")
                st.markdown("<div class='response'>", unsafe_allow_html=True)
                st.subheader("The Response is:")
                st.table(response)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.subheader("Error:")
                st.error(f"An error occurred: {e}")

    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/9850/9850877.png")
# Intialaize and control the IntelliSQL Application
def main():
    st.set_page_config(
        page_title="IntelliSQL",
        page_icon="✨",
        layout="wide"
    )
    st.sidebar.title("Navigation")
    st.sidebar.markdown("<style>.sidebar .sidebar-content {background-color: #2E2E2E;color: white;}</style>",unsafe_allow_html=True)
    pages = {
        "Home": page_home,
        "About": page_about,
        "Intelligent Query Assistance": page_intelligent_query_assistance,
    }
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]
    page()
if __name__ == "__main__":
        main()
