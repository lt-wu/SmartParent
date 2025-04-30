from PIL import Image
import json
import numpy as np


from tools.email import create_event


def eventCreate(event_data):
    """
    Create events on Google Calendar using the summarized JSON data.
    """
    global json_res

    # Debugging: Print the raw `json_res`
    print(f"createEventFromSummary: {json_res}")

    # Ensure `pairedDataSummarizer` has been executed and data is available
    if json_res is None:
        raise ValueError("No summarized data available. Run 'pairedDataSummarizer' first.")

    # Check if `json_res` is a valid dictionary
    try:
        parsed_json = json.loads(json_res) if isinstance(json_res, str) else json_res
        print(f"Parsed JSON: {parsed_json}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        raise ValueError(f"Invalid JSON format: {json_res}")

    # Create events on Google Calendar
    if "data" not in parsed_json:
        raise ValueError("'Important_dates_or_Event' key not found in the JSON data.")

    for event in parsed_json["data"]:
        print("EVENT ", event)
        event_data = {
            "summary": event["subject"],
            "description": event["description"],
            "start": {"dateTime": event["start_date"], "timeZone": "America/Los_Angeles"},
            "end": {"dateTime": event["end_date"], "timeZone": "America/Los_Angeles"},
        }
        try:
            create_event(event_data)
        except Exception as e:
            print(f"Error creating event: {e}")

    print("All events created successfully.")
    return "All events created successfully."


