import os, json
from dotenv import load_dotenv
from groq import Groq
import urllib.parse
import re  # <--- NEW: Python's built-in text filtering tool

def generate_region_art_url(region_name, region_type, genre="Fantasy"):
    """
    Creates a bulletproof link to an AI-generated art piece
    by stripping all punctuation that crashes image servers.
    """
    raw_prompt = f"Cinematic {genre} landscape concept art of a {region_type} named {region_name} digital painting atmospheric lighting high resolution"
    
    # 1. Strip out ALL punctuation (like the apostrophe in Khyron's)
    # This keeps ONLY letters, numbers, and spaces.
    clean_prompt = re.sub(r'[^a-zA-Z0-9\s]', '', raw_prompt)
    
    # 2. Safely encode the spaces into %20
    encoded_prompt = urllib.parse.quote(clean_prompt)
    
    # 3. Use the official /prompt/ endpoint with no extra slashes
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true"


load_dotenv() 

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

system_instructions = "You are only a worldbuilding assistant," \
"you must return 'name', 'type', 'description', 'climate' and 'rules'." \
"Do not output markdown code blocks like ```json, and do not write an introduction or conclusion. Return purely the raw JSON object string."

def generate_ai_region(theme_prompt):
    completion = client.chat.completions.create(model="llama-3.1-8b-instant",
                               temperature=0.7,
                               messages=[{"role": "system", "content": system_instructions},
                                {"role": "user", "content": theme_prompt}]
                                )
    raw_content = completion.choices[0].message.content
    clean_content = raw_content.strip() 
    ai_data = json.loads(clean_content)

    return ai_data