from fastapi import HTTPException, Response
import json

CORS_CONFIG = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["*"],
}


def validate_input_resume(input_resume):
    if not any(input_resume.filename.endswith(ext) for ext in [".docx",'.pdf']):
        raise HTTPException(
            status_code=404,
            detail={
                "statusCode": 404,
                "errorCode": "INPUT_ERROR",
                "message": "Invalid input resume format"
            }
        )
    
def preprocess_text(text):
    return text.replace("\n", " ")

def return_exception(e):
    raise HTTPException(
        status_code=404,
        detail={
            "statusCode": 404,
            "errorCode": "Exception Occured",
            "message": "Something went wrong, please try again "+ str(e)
        }
    )


def clean_docx_file(input_text):
    sentences = input_text.split("\n")
    encountered_sentences = set()
    unique_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and sentence not in encountered_sentences:
            unique_sentences.append(sentence)
            encountered_sentences.add(sentence)

        cleaned_text = "\n".join(unique_sentences)
    return cleaned_text


