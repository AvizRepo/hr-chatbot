import json
import sys
from fuzzywuzzy import fuzz
import dateparser
import datetime
import os
import re

def handle_query(user_input):
    """Handles predefined HR queries using fuzzy matching."""

    qa_pairs = {
        "How many leaves do I have left?": "You have 12 casual leaves and 8 sick leaves remaining.",
        "What is the work-from-home policy?": "TechVed allows up to 10 work-from-home days per month. Additional days need manager approval.",
        "What is the procedure for applying for leave?": "To apply for leave, fill out the leave application form on the TechVed HR portal and wait for approval from your manager.",
        "When is the payroll disbursed?": "At TechVed, the payroll is disbursed on the 25th of every month."
    }

    best_match = None
    best_score = 0

    for question, answer in qa_pairs.items():
        score = fuzz.partial_ratio(user_input.lower(), question.lower())
        if score > best_score:
            best_score = score
            best_match = answer

    if best_score >= 75:
        return best_match
    else:
        return "I'm sorry, I didn't understand your question. Please try rephrasing."

def is_leave_request(user_input):
    """Determines if the input is a leave request."""
    leave_keywords = ["want to take leave", "apply for leave", "request leave", "taking leave"]
    return any(keyword in user_input.lower() for keyword in leave_keywords)

def extract_dates(text):
    """Extract start and end dates from the text using various formats."""
    date_pattern = r'(\d{4}-\d{2}-\d{2})'
    dates = re.findall(date_pattern, text)

    if len(dates) >= 2:
        return dates[0], dates[1]

    parts = text.lower().split("from")
    if len(parts) > 1:
        date_part = parts[1]
        date_parts = date_part.split("to")
        if len(date_parts) == 2:
            start_date_str = date_parts[0].strip()
            end_date_str = date_parts[1].strip()

            start_date = dateparser.parse(start_date_str)
            end_date = dateparser.parse(end_date_str)

            if start_date and end_date:
                return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

    return None, None

def handle_leave_request(user_input):
    """Handles leave request, extracts dates, confirms, and simulates submission."""

    start_date, end_date = extract_dates(user_input)

    if start_date and end_date:
        confirmation_message = f"You are requesting leave from {start_date} to {end_date}. Is this correct?"
        return {
            "response": confirmation_message,
            "leave_request": True,
            "dates": {
                "start": start_date,
                "end": end_date
            }
        }
    else:
        return "I'm sorry, I couldn't understand the dates in your leave request. Please specify the dates in format YYYY-MM-DD or as a clear date range (e.g., 'from April 20th to April 25th 2024')."

def simulate_leave_submission(start_date, end_date, user_ip):
    """Simulates leave submission by writing to a file."""
    leave_requests_file = os.path.join(os.path.dirname(__file__), '..', 'leave_requests.txt')

    with open(leave_requests_file, 'a') as f:
        f.write(f"IP Address: {user_ip}, Received Leave request from {start_date} to {end_date}\n")

    return "Your leave request has been submitted for approval."

def main():
    """Main loop to read input, process, and print output."""

    leave_request_in_progress = False
    leave_request_dates = None
    user_ip = None

    while True:
        user_input = sys.stdin.readline().strip()
        if not user_input:
            continue

        if user_input == "/start":
            leave_request_in_progress = False
            leave_request_dates = None
            continue

        if not leave_request_in_progress:
            user_ip = sys.stdin.readline().strip()

        if leave_request_in_progress:
            if "yes" in user_input.lower():
                response = simulate_leave_submission(leave_request_dates["start"], leave_request_dates["end"], user_ip)
                leave_request_in_progress = False
                leave_request_dates = None
            elif "no" in user_input.lower():
                response = "Okay, I've cancelled your leave request."
                leave_request_in_progress = False
                leave_request_dates = None
            else:
                response = "Please answer with 'yes' or 'no'."
        else:
            if is_leave_request(user_input):
                leave_response = handle_leave_request(user_input)
                if isinstance(leave_response, str):
                    response = leave_response
                else:
                    leave_request_in_progress = leave_response.get("leave_request", False)
                    leave_request_dates = leave_response.get("dates", None)
                    response = leave_response.get("response", None)
            else:
                response = handle_query(user_input)

        output = json.dumps({"response": response})
        sys.stdout.write(output + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()