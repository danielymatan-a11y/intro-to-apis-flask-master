import os

from dotenv import load_dotenv
from flask import Flask, flash, render_template, redirect, request, url_for
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


def get_sent_messages():
    return []


def send_message(to, body):
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE_NUMBER:
        raise ValueError(
            "Missing Twilio environment variables. "
            "Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER."
        )

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=body,
        from_=TWILIO_PHONE_NUMBER,
        to=to
    )

    return message.sid


@app.route("/", methods=["GET"])
def index():
    messages = get_sent_messages()
    return render_template("index.html", messages=messages)


@app.route("/add-compliment", methods=["POST"])
def add_compliment():
    sender = request.values.get("sender", "Someone").strip()
    receiver = request.values.get("receiver", "Someone").strip()
    compliment = request.values.get("compliment", "wonderful").strip()
    to = request.values.get("to", "").strip()

    if not to:
        flash("Please enter a phone number.")
        return redirect(url_for("index"))

    body = f"{sender} says: {receiver} is {compliment}. See more compliments at {request.url_root}"

    try:
        sid = send_message(to, body)
        flash(f"Your message was successfully sent. SID: {sid}")
    except ValueError as e:
        flash(str(e))
    except TwilioRestException as e:
        flash(f"Twilio error: {e.msg}")
    except Exception as e:
        flash(f"Unexpected error: {str(e)}")

    return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
