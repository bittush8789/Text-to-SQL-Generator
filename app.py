from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai


#Configuring Google API key
load_dotenv()
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

## laod the model
model=genai.GenerativeModel('gemini-pro')


def main():
    st.markdown(
        """
            <div style="text-align:center;">
            <h1>SQL Query Generator </h1>
            <h3> I can generate SQL queries for you!</h3>
            </div>
    """,
        unsafe_allow_html=True,
    )
    text_input = st.text_area("Enter your Query here in plain English")
    submit = st.button("Generate SQL Query")

    if submit:
        with st.spinner("Generating SQL Query...."):
            template = """
                Create a SQL query snippet using the below text:

                ```
                {text_input}

                ```
                I just want a SQL Query.
            """
            formatted_template = template.format(text_input=text_input)

            
            response = model.generate_content(formatted_template)
            sql_query = response.text
            
            sql_query = sql_query.strip().lstrip("```sql").lstrip("````")

            expected_output= """
                What would be the expected response of this SQL query snippet:
                ```
                {sql_query}
                ```
                Provide sample tabular Response with no explanation:

            """
            expected_output_formatted=expected_output.format(sql_query=sql_query)
            eoutput=model.generate_content(expected_output_formatted)
            eoutput=eoutput.text
            

            explanation= """
                Explain this sql Query: 
                ```
                {sql_query}
                ```
                Please provide with simplest of explanation:
            """
        explanation_formatted=explanation.format(sql_query=sql_query)
        explanation=model.generate_content(explanation_formatted)
        explanation=explanation.text
        
        with st.container():
            st.success("SQL Query Generated Successfully! Here is Query Below:")
            st.code(sql_query,language="sql")

            st.success("Expected Output of this SQL Query will be:")
            st.markdown(eoutput)

            st.success("Explanation of this SQL Query")
            st.markdown(explanation)
            
            

main()