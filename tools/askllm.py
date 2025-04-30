import requests
import json
import re

def ask_gpt4o_to_summarize(api_key: str, text: str) -> str:
    """
    Ask GPT-4o to summarize the provided text in JSON format.

    Args:
        api_key (str): API key for accessing GPT-4o.
        text (str): The text to summarize.

    Returns:
        str: JSON-formatted response from GPT-4o.
    """
    # Prepare the system and user prompts
    system_prompt = "You are a helpful assistant that converts text into JSON format."
    user_prompt = f"""
    Convert the following text into a JSON structure. The key for the JSON is called 'data'.

    Text to convert:
    \"\"\"{text}\"\"\"

    JSON format example:
    {{
        "data": [
            {{
                "subject": "Earth Day",
                "start_date": "2025-04-22T00:00:00",
                "end_date": "2025-04-22T23:59:59",
                "description": "Celebration of Earth Day"
            }},
            ...
        ]
    }}
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
    try:
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
        cleaned_response = clean_response(gpt_response)
        print("\n****** Cleaned Response ******\n", cleaned_response, "\n")

        # Ensure the response is valid JSON
        try:
            json_response = json.loads(cleaned_response)
            print("\n****** Final Parsed JSON ******\n", json_response, "\n")
            return json_response
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return f"Error parsing JSON: {e}"

    except Exception as e:
        print(f"Error processing GPT-4o response: {e}")
        return f"Error processing GPT-4o response: {e}"


def clean_response(response: str) -> str:
    """
    Cleans the response from GPT-4o by removing invalid prefixes, explanatory text, and markdown formatting.
    Attempts to reconstruct truncated JSON.

    Args:
        response (str): Raw response from GPT-4o.

    Returns:
        str: Cleaned response ready for JSON parsing.
    """
    try:
        # Remove markdown formatting and explanatory text
        cleaned_response = re.sub(r"```json|```", "", response).strip()

        # Attempt to fix truncated JSON by adding closing brackets if necessary
        # if not cleaned_response.endswith("]}"):
        #     cleaned_response = cleaned_response.rstrip(",]}") + "]}"
        
        return cleaned_response
    except Exception as e:
        print(f"Error cleaning response: {e}")
        return response


# Example usage
# if __name__ == "__main__":
#     api_key = '393bb6051a2b4d3492022575dd0a038f'

#     text_to_summarize = '''
#     Based on the information provided, here is a list of important dates and events formatted according to your template:

#     Important dates or Events:
#     [
#         {
#             "subject": "Eid Dress Down",
#             "start_date": "2025-04-01T00:00:00",
#             "end_date": "2025-04-01T23:59:59",
#             "description": "Eid Dress Down Day"
#         },
#         {
#             "subject": "Field Trip",
#             "start_date": "2025-04-02T00:00:00",
#             "end_date": "2025-04-02T23:59:59",
#             "description": "Field Trip Day"
#         },
#         {
#             "subject": "Spirit Day",
#             "start_date": "2025-04-03T00:00:00",
#             "end_date": "2025-04-03T23:59:59",
#             "description": "Spirit Day"
#         }
#     ]
#     '''
#     # Ask GPT-4o to summarize the text into JSON
#     json_summary = ask_gpt4o_to_summarize(api_key, text_to_summarize)

#     # Print the JSON response
#     print("\n****** Final JSON Summary ******\n", json_summary)