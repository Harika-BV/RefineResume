from linkedin_user_scrape import *
import io, json, tempfile, os
from resume import PDF
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('api_key')
client = OpenAI(api_key=api_key)


def scrape_linkedin_profile(userId):
    email = os.getenv('email')
    password = os.getenv('password')
    cookie = os.getenv('cookie')

    user_details = get_user_profile_data(userId, cookie, email, password)

    return user_details

def enhance_summaries_using_gpt(user_summary,exp_summary_1, exp_summary_2, edu_summary_1, edu_summary_2):
    # Define the conversation messages
    messages = [
        {
            "role" : "system",
            "content" : "You are a resume enhancing champion"
        },
        {
            "role" : "user",
            "content" : "I will give you my resume's objective. Generate a new summary with profile centric keywords and by adding action verbs"
        },
        {
            "role" : "user",
            "content" : user_summary
        },
        {
            "role" : "user",
            "content" : "I will give you my first work experience's summary. Generate a new summary with profile centric keywords and by adding action verbs"
        },
        {
            "role" : "user",
            "content" : exp_summary_1
        },
        {
            "role" : "user",
            "content" : "I will give you my second work experience's summary. Generate a new summary with profile centric keywords and by adding action verbs"
        },
        {
            "role" : "user",
            "content" : exp_summary_2
        },
        {
            "role" : "user",
            "content" : "I will give you my first education's summary. Generate a new summary with profile centric keywords and by adding action verbs"
        },
        {
            "role" : "user",
            "content" : edu_summary_1
        },
        {
            "role" : "user",
            "content" : "I will give you my second education's summary. Generate a new summary with profile centric keywords and by adding action verbs"
        },
        {
            "role" : "user",
            "content" : edu_summary_2
        },
        {
            "role" : "user",
            "content" : "Generate enhanced output for objective, work experience summary 1,  work experience summary 2, education summary 1, education summary 2"
        }
    ]
    #Create chat completions
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )


    generated_text = completion.choices[0].message.content.replace("•", "-")
    print(generated_text)
    parsed_resume = parse_resume_string(generated_text)
    return {
        "Summary" : parsed_resume["Objective"],
        "Work Experience 1" : parsed_resume["Work Experience Summary 1"] ,
        "Work Experience 2" : parsed_resume["Work Experience Summary 2"] ,
        "Education Summary 1" : parsed_resume["Education Summary 1"] ,
        "Education Summary 2" : parsed_resume["Education Summary 2"] 
    }

def parse_resume_string(resume_string):
    sections = resume_string.split('\n\n')
    parsed_resume = {}

    for section in sections:
        if section.startswith("Objective:"):
            parsed_resume["Objective"] = section.replace("Objective:", "").strip()
        elif section.startswith("Work Experience Summary 1:"):
            parsed_resume["Work Experience Summary 1"] = section.replace("Work Experience Summary 1:", "").strip()
        elif section.startswith("Work Experience Summary 2:"):
            parsed_resume["Work Experience Summary 2"] = section.replace("Work Experience Summary 2:", "").strip()
        elif section.startswith("Skills:"):
            parsed_resume["Skills"] = section.replace("Skills:", "").strip()
        elif section.startswith("Work Experience Summary 2:"):
            parsed_resume["Work Experience Summary 2"] = section.replace("Work Experience Summary 2:", "").strip()
        elif section.startswith("Education Summary 1:"):
            parsed_resume["Education Summary 1"] = section.replace("Education Summary 1:", "").strip()
        elif section.startswith("Education Summary 2:"):
            parsed_resume["Education Summary 2"] = section.replace("Education Summary 2:", "").strip()

    return parsed_resume


def generate_pdf(profile_data):
    pdf = PDF()
    pdf.add_page()

    pdf.personal_info(profile_data.get('name',''), profile_data.get('title',''), profile_data.get('email_address',''), profile_data.get('phone_number',''), profile_data.get('linkedin_url',''))
    pdf.summary(profile_data.get('summary',''))
    
    pdf.experience(profile_data.get('experiences', []))
    pdf.education(profile_data.get('education', []))

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_filename = temp_file.name
    
    pdf.output(temp_filename)
    return temp_filename