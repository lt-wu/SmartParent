from PIL import Image
import json
import os
import re
import faiss
import numpy as np


from tools.get_llm_config import get_llm_config
from tools.model import OrchestratorAgent

from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")

api_key = os.getenv("AZURE_OPENAI_API_KEY")
global parsed_email_data

def read_emails():
    agent = OrchestratorAgent(api_key)

    images = [Image.open("./data/out1.jpg")]
    message_histories = [[{"role": "user", "content": "Hint: School event"}]]


    query = f"""
        
        What are important dates and all the events during 2025 year, their respective start times, and end times from the email? 
        Please format the response according to the following template, don't show "," in subject and description, all the dates are scheduled in 2025:

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
        ]

        """

    # query = f"""
    #     What are the important points, main events, their respective start times, and end times from the email?  
    #     """
    
    response = agent.batch_generate_response([query], images, message_histories)
    parsed_email_data = response

    return parsed_email_data
