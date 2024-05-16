import streamlit as st
from utils import *
import base64

def setup():
    # Set page config (optional)
    st.set_page_config(page_title="Refine Resume", page_icon=":gear:")  # Set title and icon

    # Add logo (replace 'logo.png' with your logo image filename)
    with open("refineresume.png", "rb") as file:
        logo_data = file.read()
        st.sidebar.image(logo_data, width=200)

    # Add title in sidebar
    st.sidebar.title("Refine Resume")

    # Add input field for LinkedIn username
    linkedin_username = st.sidebar.text_input("Enter your LinkedIn Username")
    
    # Additional content in the main area can be added here
    st.write("Refine Resume is a streamlit application designed to help users extract key information from their existing resume and format it into a structured and professional document suitable for various job applications.")
    get_profile_btn = st.sidebar.button("Get Profile")
    generate_pdf_btn = st.sidebar.button("Generate PDF")
    
    if get_profile_btn:
        # Call function to scrape profile data
        profile_data = scrape_linkedin_profile(linkedin_username)
        print(profile_data)
        #f = open('example_linkedin_response.json')
        #profile_data = json.load(f)
        
        details_to_pdf_builder = parse_profile_data(profile_data)
        st.session_state.details_to_pdf_builder = details_to_pdf_builder
        
    if generate_pdf_btn:
        if st.session_state.details_to_pdf_builder != None:
            temp_filename = generate_pdf(st.session_state.details_to_pdf_builder)
            with open(temp_filename, 'rb') as f:
                pdf_data = f.read()

            base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
            
            pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'

            # Displaying File
            st.markdown(pdf_display, unsafe_allow_html=True)
            
            # Create downloadable link with HTML and base64 data
            download_link = f"<a href='data:application/octet-stream;base64,{base64_pdf}' download='my_app.pdf'>Download PDF</a>"
            st.markdown(download_link, unsafe_allow_html=True)
        else:
            st.spinner('Wait for it...')
            


def parse_profile_data(profile_data):
    # Display profile data in editable boxes
    name = st.text_input("Name", value=profile_data.get("Basic Details").get("name", ""))
    user_title = st.text_input("Title", value=profile_data.get("Basic Details").get("title", ""))
    phone_number = st.text_input("Phone Number", value=profile_data.get("Basic Details").get("phone_number", ""))
    email_address = st.text_input("Email Address", value=profile_data.get("Basic Details").get("email_address", ""))
    linkedin_url = st.text_input("LinkedIn URL", value=profile_data.get("Basic Details").get("linkedin_url", ""))
    user_summary = st.text_area("Summary", value=profile_data.get("Basic Details").get("summary", ""))

    # Display work experience
    st.subheader(f"Work Experience 1")
    exp_title_1 = st.text_input("Title", value=profile_data.get("Work Experience Details", [])[0].get("Title", ""))
    exp_company_1 = st.text_input("Company", value=profile_data.get("Work Experience Details", [])[0].get("Company", ""))
    exp_duration_1 = st.text_input("Duration", value=profile_data.get("Work Experience Details", [])[0].get("Duration", ""))
    exp_summary_1 = st.text_area("Summary", value=profile_data.get("Work Experience Details", [])[0].get("Summary", ""))

    st.subheader(f"Work Experience 2")
    exp_title_2 = st.text_input("Title", value=profile_data.get("Work Experience Details", [])[1].get("Title", ""))
    exp_company_2 = st.text_input("Company", value=profile_data.get("Work Experience Details", [])[1].get("Company", ""))
    exp_duration_2 = st.text_input("Duration", value=profile_data.get("Work Experience Details", [])[1].get("Duration", ""))
    exp_summary_2 = st.text_area("Summary", value=profile_data.get("Work Experience Details", [])[1].get("Summary", ""))


    # Display education
    st.subheader(f"Education 1")
    edu_course_name_1 = st.text_input("Course Name", value=profile_data.get("Education Details", [])[0].get("Course", ""))
    edu_university_1 = st.text_input("University", value=profile_data.get("Education Details", [])[0].get("Institute", ""))
    edu_duration_1 = st.text_input("Duration", value=profile_data.get("Education Details", [])[0].get("Duration", ""))
    edu_summary_1 = st.text_area("Summary", value=profile_data.get("Education Details", [])[0].get("Summary", ""))
    
    st.subheader(f"Education 2")
    edu_course_name_2 = st.text_input("Course Name", value=profile_data.get("Education Details", [])[1].get("Course", ""))
    edu_university_2 = st.text_input("University", value=profile_data.get("Education Details", [])[1].get("Institute", ""))
    edu_duration_2 = st.text_input("Duration", value=profile_data.get("Education Details", [])[1].get("Duration", ""))
    edu_summary_2 = st.text_area("Summary", value=profile_data.get("Education Details", [])[1].get("Summary", ""))
    

    # Enhance summary using GPT
    enhanced_summaries = enhance_summaries_using_gpt(user_summary,exp_summary_1, exp_summary_2, edu_summary_1, edu_summary_2)
    details_to_pdf_builder = {
        "name" : name, 
        "title" : user_title,
        "phone_number" : phone_number,
        "email_address" : email_address,
        "linkedin_url" : linkedin_url,
        "summary" : enhanced_summaries.get("Summary", user_summary),
        "experiences" : [
            {
                "title": exp_title_1,
                "company": exp_company_1,
                "duration": exp_duration_1,
                "summary": enhanced_summaries.get("Work Experience 1", exp_summary_1)
            },
            {
                "title": exp_title_2,
                "company": exp_company_2,
                "duration": exp_duration_2,
                "summary": enhanced_summaries.get("Work Experience 2", exp_summary_2)
            },
        ],
        "education" : [
            {
                "course": edu_course_name_1,
                "university": edu_university_1,
                "duration": edu_duration_1,
                "summary":  enhanced_summaries.get("Education Summary 1", edu_summary_1)
            },
            {
               "course": edu_course_name_2,
               "university": edu_university_2,
               "duration": edu_duration_2,
               "summary":  enhanced_summaries.get("Education Summary 2", edu_summary_2)
            }
        ]
    }
    
    return details_to_pdf_builder

if __name__ == "__main__":
    setup()

