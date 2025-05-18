from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables
load_dotenv()

# Get API key securely
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY not found in .env")

# Initialize Groq client
client = Groq(api_key=api_key)

# Initialize FastAPI app
app = FastAPI()

# Request body schema
class Schema(BaseModel):
    query: str

# Load the system prompt from prompt.txt
with open("app/template/prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

@app.get("/")
def root():
    return {"message": "This is text translator API"}  


@app.post("/translate")
async def translate(data: Schema):
    try:
        # Construct prompt for multilingual translation
        prompt = f"Translate the following sentence to Hindi only:\n\n\"{data.query.strip()}\""

        # API call
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=512,
            top_p=1,
            stream=False
        )

        # Extract translated text
        translated_text = completion.choices[0].message.content.strip() if completion.choices else ""

       
        return translated_text

    except Exception as e:
        raise HTTPException(status_code=500, detail="Translation failed. Please try again.")
