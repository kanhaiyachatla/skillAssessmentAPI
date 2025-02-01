import json
import time
from fastapi import FastAPI,Request,File,UploadFile,Form,Response
from serpapi import GoogleSearch
from src.helper_function import return_exception,validate_input_resume,preprocess_text
from src.fitz_text_extractor import extract_text
from src.generative_llm import get_gemini_response
from src.prompts import get_prompt_resume_summarizer,get_prompt_skill_test,get_prompt_test_results
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.get('/')
@app.get("/health_check")
async def health_check():
    return "ok"

@app.middleware("http")
async def add_x_runtime_header(request: Request, call_next):
    stime= time.time()
    response = await call_next(request)
    etime = time.time()
    response.headers["X-Runtime"] = str(etime - stime)
    return response

@app.post("/generate_summary")
async def generate_summary(input_resume: UploadFile = File(...)):
    try:
        validate_input_resume(input_resume)
        extracted_resume = extract_text(input_resume)
        preprocessed_resume = preprocess_text(extracted_resume)
        prompt = get_prompt_resume_summarizer()
        genai_response = get_gemini_response(prompt+preprocessed_resume)
        genai_response = genai_response.replace("```","")
        genai_response = genai_response.replace("JSON","")
        genai_response = genai_response.replace("json","")
        genai_response = genai_response.replace("```json","")
        json_output = json.loads(genai_response)
        return json_output
    except Exception as e:
        return_exception(e)

@app.post("/generate_skill_test")
async def generate_test(input_skills: str):
    try:
        prompt = get_prompt_skill_test()
        genai_response = get_gemini_response(prompt+input_skills)
        genai_response = genai_response.replace("```","")
        genai_response = genai_response.replace("JSON","")
        genai_response = genai_response.replace("json","")
        genai_response = genai_response.replace("```json","")
        json_output = json.loads(genai_response)
        return json_output
    except Exception as e:
        return_exception(e)


@app.post("/check_test")
async def check_test(input_test: str,profile_summary: str):
    try:
        prompt= get_prompt_test_results()
        genai_response = get_gemini_response(prompt+input_test+"\n"+profile_summary)
        genai_response = genai_response.replace("```","")
        genai_response = genai_response.replace("JSON","")
        genai_response = genai_response.replace("json","")
        genai_response = genai_response.replace("```json","")
        json_output = json.loads(genai_response)
        return json_output
    except Exception as e:
        return_exception(e)

@app.post("/jobs")
async def get_jobs(job_title: str, location: str):
    params = {
        "engine": "google_jobs",
        "q": job_title+" "+ location,
        "hl": "en",
        "api_key": "7eee66b39bc3a2fabedfc20c90fa9b891f360eb757a40ca5ed9d35390c3c1a6c"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    jobs_results = results.get("jobs_results", [])

    return {"jobs": jobs_results}
