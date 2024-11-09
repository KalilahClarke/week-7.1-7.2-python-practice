from dotenv import load_dotenv
import os
import google.generativeai as genai
import random

# Load API key from .env file
load_dotenv()
api_key = os.getenv('API_KEY')

# Configure the Generative AI model if the API key is available
if api_key:
    os.environ['API_KEY'] = api_key
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None
    print("Warning: API_KEY not found. Using predefined responses instead.")

def get_financial_advice(prompt, use_ai=True, temperature=0, max_output_tokens=1000):

    if model and use_ai:
        try:
            generation_config = {
                'temperature': temperature,
                'max_output_tokens': max_output_tokens
            }
            response = model.generate_content(prompt, generation_config=generation_config)
            is_financial = check_financial_association(prompt, generation_config)
            if(is_financial):
                return response.text
            else:
                return 'This is not associated with Financial Literacy.'
        
        except Exception as e:
            print(f"Error using AI model: {e}. Switching to predefined advice.")
    
    return predefined_financial_advice(prompt)

def check_financial_association(prompt, generation_config):

    query = f"Is this prompt associated with finances: {prompt}"
    response = model.generate_content(query, generation_config=generation_config)

    # print(response.text)
    if(response.text[0:3].lower() == 'yes'):
        return True
    return False


def predefined_financial_advice(prompt):

    advice_bank = {
        "invest": [
            "Consider diversifying your portfolio with a mix of stocks and bonds.",
            "Investing in index funds can be a low-risk way to grow your wealth over time."
        ],
        "save": [
            "Setting aside a portion of your income each month in a high-yield savings account can help build an emergency fund.",
            "Automate your savings to make it easier to stay consistent with your financial goals."
        ],
        "debt": [
            "Focus on paying off high-interest debt first to reduce the total amount of interest paid.",
            "Consider consolidating your debts if you're struggling to keep track of multiple payments."
        ],
        "default": [
            "To get started, track your monthly expenses to see where your money goes.",
            "A financial advisor can help you tailor a plan specific to your income and goals."
        ]
    }
    
    # Select advice type based on keywords in the prompt
    lower_prompt = prompt.lower()
    if "invest" in lower_prompt:
        advice = random.choice(advice_bank["invest"])
    elif "save" in lower_prompt:
        advice = random.choice(advice_bank["save"])
    elif "debt" in lower_prompt:
        advice = random.choice(advice_bank["debt"])
    else:
        advice = random.choice(advice_bank["default"])
    
    return f"Financial advice: {advice}"

def main():
    print("Welcome to the financial support service!")
    
    # Initial prompt from the user
    prompt = input("What kind of financial support do you need? ").strip()
    if not prompt:
        prompt = "Provide a starting point for managing my finances."
    print()
    
    # Fetch and display the initial financial advice
    response = get_financial_advice(prompt)
    print(response)
    
    # Loop for additional queries
    while True:
        ask_another = input("Would you like to ask another question? (Yes/No): ").strip().lower()
        if ask_another != "yes":
            print("Thank you for using the financial support service!")
            break
        
        # Prompt for the next question
        prompt = input("What other financial support do you need? ").strip()
        print()
        response = get_financial_advice(prompt)
        print(response)

if __name__ == "__main__":
    main()
