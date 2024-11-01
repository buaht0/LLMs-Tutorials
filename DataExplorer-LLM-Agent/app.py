# Packages
import streamlit as st
import data_helper


if "dataload" not in st.session_state:
    st.session_state.dataload = False

def activate_dataload():
    st.session_state.dataload = True


st.set_page_config(page_title="Data Explorer", layout='wide')
st.image('./img/app_banner.jpg', use_column_width=True)
st.title("Data Explorer")
st.divider()
st.sidebar.subheader("Upload Your Data")
st.sidebar.divider()
loaded_file = st.sidebar.file_uploader("Select the CSV file you want to upload", type='csv')
load_data_btn = st.sidebar.button(label='Upload', on_click=activate_dataload, use_container_width=True)

col_prework, col_dummy, col_interaction = st.columns([4, 1, 7])

if st.session_state.dataload:
    @st.cache_data
    def summarize():
        loaded_file.seek(0)
        data_summary = data_helper.summarize_data(data_file=loaded_file)
        return data_summary

    data_summary = summarize()

    with col_prework:
        st.info('DATA SUMMARY')
        st.subheader('Data Sample')
        st.write(data_summary['initial_data_sample'])
        st.divider()
        st.subheader('Variables')
        st.write(data_summary['column_descriptions'])
        st.divider()
        st.subheader('Missing Values')
        st.write(data_summary['missing_values'])
        st.divider()
        st.subheader('Duplicate Values')
        st.write(data_summary['duplicate_values'])
        st.divider()
        st.subheader('Essential Metrics')
        st.write(data_summary['essential_metrics'])
    with col_dummy:
        st.empty()
    with col_interaction:
        st.info('Data Interaction')
        variable_of_interest = st.text_input(label='Which variable do you want to analyze?')
        examine_btn = st.button(label='Review')
        st.divider()

        @st.cache_data
        def explore_variable(data_file, variable_of_interest):
            data_file.seek(0)
            dataframe = data_helper.get_dataframe(data_file=data_file)
            st.bar_chart(data=dataframe, y=[variable_of_interest])
            st.divider()
            data_file.seek(0)
            trend_response = data_helper.analyze_trend(data_file=loaded_file, variable_of_interest=variable_of_interest)
            st.success(trend_response)
            return

        if variable_of_interest or examine_btn:
            explore_variable(data_file=loaded_file, variable_of_interest=variable_of_interest)

        free_question = st.text_input(label='What would you like to know about the dataset?')
        ask_btn = st.button(label='Ask')
        st.divider()


        @st.cache_data
        def answer_question(data_file, question):
            data_file.seek(0)
            AI_Response = data_helper.ask_question(data_file=loaded_file, question=free_question)
            st.success(AI_Response)
            return
        
        if free_question or ask_btn:
            answer_question(data_file=loaded_file, question=free_question)
