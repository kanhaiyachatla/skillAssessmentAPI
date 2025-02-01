import google.generativeai as genai
from dotenv import load_dotenv
import os
from fastapi import HTTPException

def configure():
    try:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("API Key not found")
        genai.configure(api_key=api_key)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "statusCode": 404,
                "errorCode": "GenAI connection Failed.",
                "message": "Something went wrong, please try again "+ str(e)
            }
        )
    

def get_gemini_response(prompt):
    try:
        configure()
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "statusCode": 404,
                "errorCode": "GenAI Generation Failed.",
                "message": "Something went wrong, please try again "+ str(e)
            }
        )