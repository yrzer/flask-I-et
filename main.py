


from flask import Flask, request, jsonify
from pywebpush import webpush, WebPushException
import os

app = Flask(__name__)

VAPID_PUBLIC_KEY = os.environ.get("BJKHYAsP42a0TpDNOQ50ctTokNsfPmbvmzrm06fMrx_bcBslszKi8VGWFyI2eY0cj-9DGJE0mH2Xc0nQZWnMIdU")
VAPID_PRIVATE_KEY = os.environ.get("SdKIoJi09KpdhQEPyyZH65gz7qu2W1w41O4WLkh3Qy8")
VAPID_CLAIMS = {"sub": "mailto:bqlojvscmsauqymobo@nesopf.com"}

subscribers = []  # w praktyce lepiej baza danych

@app.route("/subscribe", methods=["POST"])
def subscribe():
    subscription_info = request.json
    subscribers.append(subscription_info)
    return jsonify({"status": "subscribed"})

@app.route("/notify", methods=["POST"])
def notify():
    payload = {"title": "Nowy plan", "body": "Plan zajęć się zmienił!"}
    for sub in subscribers:
        try:
            webpush(
                subscription_info=sub,
                data=jsonify(payload).get_data(as_text=True),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS,
            )
        except WebPushException as e:
            print("Błąd przy wysyłce:", repr(e))
    return jsonify({"status": "notified"})

@app.route("/vapidPublicKey", methods=["GET"])
def get_key():
    return jsonify({"publicKey": VAPID_PUBLIC_KEY})


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome yrzer!"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
