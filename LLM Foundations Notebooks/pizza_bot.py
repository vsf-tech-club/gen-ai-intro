import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_completion_from_messages(messages, model="gemini-1.5-pro", temperature=0):
    model = genai.GenerativeModel(model_name=model)
    chat = model.start_chat()
    
    for msg in messages:
        response = chat.send_message(msg['content'])
    return response.text

def main():
    context = [{
        'role':'system', 
        'content': """
You are OrderBot, an automated service to collect orders for a pizza restaurant. \
Respond to this first message with exactly: "Hello! Welcome to Pizza World! How can I help you today?"

After that, collect the order, \
and then ask if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.

The menu includes \
pepperoni pizza  12.95, 10.00, 7.00 \
cheese pizza   10.95, 9.25, 6.50 \
eggplant pizza   11.95, 9.75, 6.75 \
fries 4.50, 3.50 \
greek salad 7.25 \
Toppings: \
extra cheese 2.00, \
mushrooms 1.50 \
sausage 3.00 \
canadian bacon 3.50 \
AI sauce 1.50 \
peppers 1.00 \
Drinks: \
coke 3.00, 2.00, 1.00 \
sprite 3.00, 2.00, 1.00 \
bottled water 5.00 \
"""}]

    print("Initializing...")
    print("-" * 50)
    
    # Get initial greeting
    response = get_completion_from_messages(context)
    print("\nAssistant:", response)
    
    while True:
        user_message = input("\nYou: ")
        
        if user_message.lower() in ['quit', 'exit', 'bye']:
            print("\nThank you for visiting Pizza World!")
            break
            
        context.append({'role': 'user', 'content': user_message})
        response = get_completion_from_messages(context)
        print("\nAssistant:", response)
        context.append({'role': 'assistant', 'content': response})

if __name__ == "__main__":
    main()