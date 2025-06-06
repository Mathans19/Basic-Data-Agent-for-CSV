import streamlit as st
import pandas as pd
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the Groq API key from environment variable
groq_api_key = os.getenv("GROQ_API_KEY")


# Streamlit app title
st.title('CSV Data Analyst with Groq AI')

# File upload widget for CSV
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

# Check if file is uploaded
if uploaded_file is not None:
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(uploaded_file)
    st.write(f"✅ CSV loaded successfully with {len(df)} rows and {len(df.columns)} columns.")
    st.dataframe(df.head())  # Display first few rows of the uploaded file
    
    llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama3-70b-8192") 


    # Create a prompt template
    prompt = PromptTemplate(
        input_variables=["dataframe_head", "columns", "question", "full_dataset"],
        template="""You are a data analyst.
        Here is the entire dataset:
        {full_dataset}

        The columns available are:
        {columns}

        Based on this, answer the user's question:
        {question}

        If the question is unclear, politely ask for clarification."""
    )

    # Create an LLM Chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Text input for the user to ask questions
    question = st.text_input("Ask a question about the CSV:")

    if question:
        dataframe_preview = df.head(5).to_string()  # Optionally show first 5 rows for context
        available_columns = ", ".join(df.columns)
        full_dataset = df.to_string()  # Full dataset for answering based on all rows

        # Run the question through the model chain
        response = chain.run({
            "dataframe_head": dataframe_preview,
            "columns": available_columns,
            "question": question,
            "full_dataset": full_dataset
        })
        
        # Display the answer from the model
        st.write("Answer:", response)
else:
    st.write("Please upload a CSV file to proceed.")
