import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import data_engine  
import prompts       

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1" 
)

def run_automation():

    print("Step 1: Fetching and calculating market data...")
    report_data = data_engine.generate_ai_report()
    
    # Check if data actually exists
    if not report_data:
        print("Error: No data received from data_engine.")
        return
    
    models_to_try = [
        "qwen/qwen3.6-plus",                                             
        "google/gemini-pro-1.5-exp",
        "mistralai/mistral-7b-instruct:free",
        "openrouter/auto"                                                
    ]
    full_prompt = prompts.CRYPTO_ANALYSIS_PROMPT.format(report_data=json.dumps(report_data, indent=2))

    for model in models_to_try:
        print(f"Trying model: {model}")

        try:
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a professional crypto researcher."},
                    {"role": "user", "content": full_prompt}
                ],
                timeout=60,
                temperature=0.2,
                max_tokens=2000 
            )
            print(f"Success with {model}!")
            
            
            final_report = response.choices[0].message.content
            print("\n--- REPORT ---")
            print(final_report)

            with open("latest_analysis.md", "w") as f:
                f.write(final_report)
                print("Report saved to latest_analysis.md")
            break  

        except Exception as e:
            print(f"{model} failed or timed out: {e}. Trying next model...")
    else:
        print("All models failed. Please check your API keys and try again later.")
  
if __name__ == "__main__":
    run_automation()
