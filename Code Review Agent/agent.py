import os
import time
from google import genai
from google.genai import types
from google.genai.errors import ServerError
from models import CodeReviewReport

def review_code(source_code: str, language: str = "python") -> CodeReviewReport:
    client = genai.Client()
    
    system_prompt = f"""
    You are an elite Principal Software Engineer and Security Auditor specializing in {language}. 
    Your task is to review the provided code for:
    1. Security vulnerabilities (e.g., injection risks, unvalidated inputs, hardcoded secrets).
    2. Performance bottlenecks (e.g., O(n^2) traps, memory inefficiencies).
    3. Code style, readability, and idiomatic best practices.
    
    Provide a thorough breakdown of findings and supply a clean, fully refactored version of the code.
    """

    max_retries = 3
    delay = 2

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=f"Please review and refactor the following code:\n\n```{language}\n{source_code}\n```",
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json",
                    response_schema=CodeReviewReport,
                    temperature=0.2,
                ),
            )
            return response.parsed
        except ServerError as e:
            if attempt == max_retries - 1:
                raise e
            print(f"Server busy (503). Retrying in {delay} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(delay)
            delay *= 2