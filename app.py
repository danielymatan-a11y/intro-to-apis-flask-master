import os

from dotenv import load_dotenv
from flask import Flask, flash, render_template, redirect, request, url_for

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")

TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


def get_sent_messages():
    messages = []
    return messages


def send_message(to, body):
    # TODO: implement Twilio sending here
    pass


@app.route("/", methods=["GET"])
def index():
    messages = get_sent_messages()
    return render_template("index.html", messages=messages)


@app.route("/add-compliment", methods=["POST"])
def add_compliment():
    sender = request.values.get("sender", "Someone")
    receiver = request.values.get("receiver", "Someone")
    compliment = request.values.get("compliment", "wonderful")
    to = request.values.get("to")

    body = f"{sender} says: {receiver} is {compliment}. See more compliments at {request.url_root}"
    send_message(to, body)
    flash("Your message was successfully sent")
    return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
