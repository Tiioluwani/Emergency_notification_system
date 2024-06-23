from flask import Flask, render_template, request, jsonify
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import logging
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Specify the path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), 'file.env')

# Load environment variables from .env file
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    logging.error("file.env file not found at {}".format(dotenv_path))

# Access environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_PHONE_NUMBER')

client = Client(account_sid, auth_token)

# Phone numbers
to_numbers = ['+2347047705022']  # List of recipient phone numbers


@app.route('/')
def index():
    return render_template('call.html')


@app.route('/send_notification', methods=['POST'])
def send_notification():
    if request.is_json:
        data = request.get_json()
        message = data['message']
    else:
        message = request.form.get('message', '')

    for to_number in to_numbers:
        try:
            response = VoiceResponse()
            response.say(message)
            twiml = str(response)

            # Log the TwiML response
            logging.info(f'TwiML to be sent: {twiml}')

            call = client.calls.create(
                twiml=twiml,
                to=to_number,
                from_=twilio_number
            )
            logging.info(f'Notification sent to {to_number} (Call SID: {call.sid})')
        except Exception as e:
            logging.error(f'Error sending notification to {to_number}: {e}')

    return jsonify({'Message': 'Notifications sent successfully'})


if __name__ == '__main__':
    app.run(debug=True)
