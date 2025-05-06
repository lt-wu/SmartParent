import base64
import requests
from PIL import Image
from typing import Any, Dict, List, Optional
import email.parser

class OrchestratorAgent:
    def __init__(self, api_key: str):
        """
        Initialize the OrchestratorAgent with the provided API key.
        """
        self.api_key = api_key

    def analyze_image(self, image_path: str, image_question: str) -> str:
        """
        Analyze an image using the GPT-4o model and return the response.

        Args:
            image_path (str): Path to the image file.
            image_question (str): Question to ask about the image.

        Returns:
            str: Response from the GPT-4o model.
        """
        try:
            # Encode the image in base64
            with open(image_path, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

            # Prepare the payload for the API
            payload = {
                "messages": [
                    {"role": "user", "content": [{"type": "image", "image": encoded_image}]},
                    {"role": "user", "content": [{"type": "text", "text": image_question}]},
                ],
                "temperature": 0.7,
                "top_p": 0.95,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "max_tokens": 800,
                "stop": None,
            }

            # Send the request
            response = requests.post(
                url='https://cast-southcentral-nprd-apim.azure-api.net/cragmm/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview',
                headers={
                    'api-key': self.api_key,
                    'Content-Type': 'application/json'
                },
                json=payload
            )

            # Extract the response content
            out = response.json()['choices'][0]['message']['content']
            print("\n****** LLM Image Output ******\n", out, "\n")
            return out

        except Exception as e:
            print(f"Error analyzing image: {e}")
            return "Error analyzing image."

    def ask_llm(self, query: str, context: str, image: Optional[str] = None) -> str:
        """
        Ask the GPT-4o model a question, optionally including image analysis.

        Args:
            query (str): The main query to ask.
            context (str): Additional context for the query.
            image (Optional[str]): Path to the image to analyze (if applicable).

        Returns:
            str: Response from the GPT-4o model.
        """
        try:
            # Include image analysis if an image path is provided
            if image:
                image_info = self.analyze_image(image, "Please describe the image.")
                query = f"Image Description: {image_info}\n{context}\n{query}"

            # Prepare the payload for the query
            payload = {
                "messages": [
                    {"role": "user", "content": [{"type": "text", "text": query}]},
                ],
                "temperature": 0.7,
                "top_p": 0.95,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "max_tokens": 800,
                "stop": None,
            }

            # Send the request
            response = requests.post(
                url='https://cast-southcentral-nprd-apim.azure-api.net/cragmm/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview',
                headers={
                    'api-key': self.api_key,
                    'Content-Type': 'application/json'
                },
                json=payload
            )

            # Extract the response content
            out = response.json()['choices'][0]['message']['content']
            print("\n****** LLM Output ******\n", out, "\n")
            return out

        except Exception as e:
            print(f"Error querying LLM: {e}")
            return "Error querying LLM."

    def batch_generate_response(
        self,
        queries: List[str],
        images: List[Image.Image],
        message_histories: List[List[Dict[str, Any]]],
    ) -> List[str]:
        """
        Generate responses for a batch of queries.

        Args:
            queries (List[str]): List of queries to process.
            images (List[Image.Image]): List of images to analyze.
            message_histories (List[List[Dict[str, Any]]]): List of message histories for each query.

        Returns:
            List[str]: List of responses for each query.
        """
        responses = []

        # Process each query and image pair
        for query, image, history in zip(queries, images, message_histories):
            try:
                # Extract the image path
                image_path = image.filename if hasattr(image, "filename") else None
                if not image_path:
                    raise ValueError("Image object does not have a valid file path.")

                # Generate the context from message history
                context = "\n".join(
                    f"{msg['role'].capitalize()}: {msg['content']}" for msg in history
                )

                # Ask the LLM and get a response
                response = self.ask_llm(query, context=context, image=image_path)
                responses.append(response)

            except Exception as e:
                print(f"Error processing query '{query}': {e}")
                responses.append(f"Error processing query: {query}")

        return responses

if __name__ == "__main__":
    api_key = ##
    agent = OrchestratorAgent(api_key)  # Remove 'search_pipeline'

    query = f"""
        
        What are important dates and all the events during 2025 year, their respective start times, and end times from the email? 
        Please format the response according to the following template, don't show "," in subject and description, 
        all the dates are scheduled in 2025, 
        if don't have time in the conetxt just set 12:00:00 am for both starttime and endtime
        if don't have end time in the conetxt just set end time = start time

        data:
        [
        {{
            "subject": "Event Subject",
            "start_date": "YYYY-MM-DDTHH:MM:SS",
            "end_date": "YYYY-MM-DDTHH:MM:SS",
            "description": "Brief description of the event"
        }},
        {{
            "subject": "Event Subject",
            "start_date": "YYYY-MM-DDTHH:MM:SS",
            "end_date": "YYYY-MM-DDTHH:MM:SS",
            "description": "Brief description of the event"
        }}

        """

    # query = f"""
    #     What are the important points, main events, their respective start times, and end times from the email?  
    #     """
    
    images = [Image.open("./data/out1.jpg")]
    images = [
        Image.open("./data/out5.jpg")
    ]
    message_histories = [[{"role": "user", "content": "Hint: School event"}]]
    for image in [images]:
        response = agent.batch_generate_response([query], image, message_histories)
        print(f"Question: {query}\n***Final Answer***: {response}\n")
