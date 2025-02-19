
import streamlit as st
import pandas as pd
from pandasai.llm.openai import OpenAI
import openai
import os
import matplotlib.pyplot as plt
import matplotlib
import pandasai
from pandasai import llm 
from pandasai import SmartDataframe

def app():
    matplotlib.use('Agg')
    
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] > .main {
            background: linear-gradient(45deg, #f3f2f7, #e0e0e0);
        }
        .icon {
            font-size: 1.5em;
            vertical-align: middle;
            margin-right: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    """Main function to run the Streamlit app."""

    def chat_with_csv(df, prompt):
        """Function to interact with a CSV using AI.

        Args:
            df (pd.DataFrame): The data from a CSV file.
            prompt (str): The user's question or prompt.

        Returns:
            result: The AI's response.
                """
        OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']
        openai.api_key = OPENAI_API_KEY


        llm = OpenAI(api_token=OPENAI_API_KEY)
        #pandas_ai = llm(llm,save_charts_path="exports/charts/temp_chart.png")
        #result = pandas_ai.run(df, prompt=prompt)
        os.makedirs("exports/charts", exist_ok=True)
        dfsmart = SmartDataframe(
            df,
            config={
                "llm": llm,
                "save_charts": True,
                "save_charts_path": "exports/charts"  # Use a directory instead of a file name
            }
        )
        print("w hnaya" )
        result2=dfsmart.chat(prompt)
        print(result2)
        #st.image(result.get('value'))
        return result2

    # Displaying a subheader and a custom welcome message
    st.subheader("Welcome User!")
    st.markdown(
        '''<div style="text-align:center;">
            <p style="font-size:40px;font-weight:bold;color:#5C4DB1;">🔮 DataSage </p>
            <p style="font-size:18px;color:#888888;">Unravel the mysteries of your CSV data with the power of AI. 
            Simply upload, ask, and let DataSage provide insights.</p>
           </div>''',
        unsafe_allow_html=True
    )

    # Creating a container for the main content of the app
    container = st.container()

    # Defining the content to be displayed in the container
    with container:
        # Creating a styled container for the file uploader
        st.markdown('<div style="border: 2px solid #E0E0E0; border-radius: 10px; padding: 20px;">', unsafe_allow_html=True)
        
        # File uploader allowing users to upload CSV files
        input_csv = st.file_uploader("📤 Upload your CSV file", type=['csv'])

        # If a CSV file is uploaded, display a preview of the data and the chat interface
        if input_csv is not None:
            col1, col2 = st.columns([1, 1])

            # Displaying a preview of the uploaded CSV file in the left column
            with col1:
                st.info("📄 Preview of Uploaded CSV")
                data = pd.read_csv(input_csv)
                st.dataframe(data)

            # Chat interface allowing users to ask questions about the data in the right column
            with col2:
                st.markdown("## 🤖 Chat with DataSage")
                input_text = st.text_area("What would you like to know?", height=100)
                
                # If the "Ask DataSage" button is pressed, process the user's input and generate a response
                if st.button("Ask DataSage"):
                    if input_text:
                        st.info(f"Your Query: *{input_text}*")
                        with st.spinner("Generating response..."):
                            result = chat_with_csv(data, input_text)
                            print("WLH HNA EMCHI N3ETIZ")

                            #fig = plt.gcf()
                            #if fig.get_axes():
                            #    st.pyplot(fig)
                            #st.write(result)

                           # print(result['value'])

                           
                            print(result)
                            if isinstance(result, pd.DataFrame):
                                st.dataframe(result)
                            elif isinstance(result, (int, float)):
                                st.success(result)
                            elif isinstance(result, str):
                                if result.endswith('.png') and os.path.exists(result):
                                    st.image(result)
                                else:
                                    st.success(result)
                            else:
                                st.warning("Unexpected response type.")


                    else:
                        st.warning("Please enter a prompt.")
