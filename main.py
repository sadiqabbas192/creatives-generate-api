from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

def get_brand_data(brand_id=None, brand_name=None):

    try:
        with open("brands.json", "r") as f:
            data = json.load(f)
            
        brands = data.get("all_brands", [])
        
        for brand in brands:
            # Check by ID if provided
            if brand_id is not None:
                if str(brand.get("brand_id")) == str(brand_id):
                    return brand
            
            # Check by Name if provided
            if brand_name is not None:
                if brand.get("brand_name", "").lower() == brand_name.lower():
                    return brand
                    
        return None
    except FileNotFoundError:
        print("Error: brands.json not found.")
        return None
    except Exception as e:
        print(f"Error reading brands.json: {e}")
        return None

def llm_chatbot(user_query, brand_id=None, brand_name=None):

    # 1. Retrieve Brand Data
    brand_data = get_brand_data(brand_id=brand_id, brand_name=brand_name)
    
    if not brand_data:
        return "Error: Brand not found."
    
    # 2. Serialize Brand Context for Prompt
    brand_context_str = json.dumps(brand_data, indent=2)
    
    # 3. Load Prompts
    try:
        with open("prompts/llm-gemini/user.txt", "r", encoding="utf-8") as f:
            user_prompt_template = f.read()
        
        with open("prompts/llm-gemini/system.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()
    except FileNotFoundError as e:
        return f"Error: Prompt file not found - {e}"

    # 4. Inject Variables into User Prompt
    user_prompt = user_prompt_template.replace("{{brand_context}}", brand_context_str)
    user_prompt = user_prompt.replace("{{user_query}}", str(user_query))

    # 5. Call Gemini API
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY not found in environment variables."

    try:
        from google.genai import types
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-09-2025",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json"
            )
        )
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"

if __name__ == "__main__":
    # Test 1: Simple Request
    print("--- Test 1: Under Armour - Simple Request ---")
    query1 = "create a new year post"
    response1 = llm_chatbot(user_query=query1, brand_name="Under Armour")
    print('query', - query1)
    print('---------------------------------------------')
    print("\n[LLM Response]:\n")
    print(response1)
    
    # # Test 2: Specific Visual Request
    # print("\n\n--- Test 2: Nike - Specific Visual Request ---")
    # query2 = "create a new year post with a caption new year new will and logo on top right corner use color red black and white with a nice athletic in the background"
    # response2 = llm_chatbot(user_query=query2, brand_id=2)
    # print("\n[LLM Response]:\n")
    # print(response2)

    # # Test 3: Complex Request with Comparison
    # print("\n\n--- Test 3: Under Armour - Complex Request ---")
    # query3 = "create a new year post also suggest caption for it logo on top left corner use colors red black and white use image provided to get a better understanding of how other poster are made for it"
    # response3 = llm_chatbot(user_query=query3, brand_name="Under Armour")
    # print("\n[LLM Response]:\n")
    # print(response3)


