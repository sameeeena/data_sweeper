# Imports
import streamlit as st 
import pandas as pd 
import os 
from io import BytesIO 



# setup our App
st.set_page_config(page_title="Data sweeper", layout='wide')
st.title("💽Data sweeper")
st.markdown("""<style>
            body{background-color: "lemon"}
            </style>""",unsafe_allow_html=True)

st.markdown("<p style=' font-size:24px;' 'bold;'>Transfrom your files between csv and Excel formats with built-in data cleaning and visualization!</p>",unsafe_allow_html=True)

uploaded_files = st.file_uploader("**Upload your file (CSV or Excel)**",type=["CSV","xlsx"], accept_multiple_files=True)

        
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        
    
    #Display info about the file
    st.write(f"**File Name:** {file.name}")
    st.write(f"**File Size:** {file.size/1024}")
    
    #show 5 rows of our df
    st.write("**Preview the Head of the Dataframe**")
    st.dataframe(df.head())
    
    #options for data cleaning
    st.subheader("**🛠️Data Cleaning Options**")
    if st.checkbox(f"Clean Data for {file.name}"):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"**Remove duplicates from {file.name}**"):
                df.drop_duplicates(inplace=True)
                st.write("**Duplicates Removed!**")
                
                with col2:
                    if st.button(f"**Fill missing values for {file.name}**"):
                        numeric_cols = df.select_dtypes(include=['numbers']).columns
                        df[numeric_cols] =df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("**Missing values have been filled!**")
                        
     #choose specific columns to convert
                    st.subheader("**Select Columns To Convert**")
            Columns = st.multiselect(f"**Choose Columns for {file.name}**", df.columns, default=df.columns)
            df = df[Columns]
            
            #Create Some Visualizations
            st.subheader("**📊 Data Visualization**")
            if st.checkbox (f"**Show Visualization for {file.name}**"):
                st.bar_chart (df.select_dtypes(include='number').iloc[:,:2])
                
                #Convert the file -> CSV to Excel
                st.subheader("**Conversion Options**")
                conversion_type = st.radio(f"**Convert {file.name} to:**",["CSV","Excel"], key=file.name)
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer,index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                    
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext,".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    buffer.seek(0)
                    
                    
        st.download_button(
                    label=f"**⏬ Download {file.name} as {conversion_type}**",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )


                    
        st.success("**🎉All files Processed!**")
                        