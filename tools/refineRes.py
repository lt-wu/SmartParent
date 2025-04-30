import requests
from datetime import datetime

# Get the current date and time
current_date = datetime.now()

# Extract the current day name
formatted_date = current_date.strftime("%Y-%m-%d")

print(f"Today's date is {formatted_date}")

def refineRes(api_key: str, q: str, text: str) -> str:
    print(formatted_date)
    """
    Ask GPT-4o to ansnwer question based on the provided text in JSON format.

    Args:
        api_key (str): API key for accessing GPT-4o.
        text (str): The text to summarize.

    Returns:
        str: JSON-formatted response from GPT-4o.
    """
    # Prepare the system and user prompts
    system_prompt = "You are a helpful assistant."
    user_prompt = f"""
    Answer {q} based on '.

    Text:
    \"\"\"{text}\"\"\"
    if {q} is related day, time please find current date  {formatted_date} first, then answer questionn don't assume any information.

    """

    # Prepare the payload for GPT-4o
    payload = {
        "messages": [
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
            {"role": "user", "content": [{"type": "text", "text": user_prompt}]},
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "max_tokens": 800,
        "stop": None,
    }

    # Send the request to GPT-4o
    response = requests.post(
            url='https://cast-southcentral-nprd-apim.azure-api.net/cragmm/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview',
            headers={
                'api-key': api_key,
                'Content-Type': 'application/json'
            },
            json=payload
        )

    # Check if the response is successful
    if response.status_code != 200:
            raise Exception(f"Failed to connect to GPT-4o API. Status code: {response.status_code}. Response: {response.text}")

    # Extract the JSON response from GPT-4o
    gpt_response = response.json()['choices'][0]['message']['content']
    print("\n****** GPT-4o Response ******\n", gpt_response, "\n")

    # Clean and validate the response
    return gpt_response
  