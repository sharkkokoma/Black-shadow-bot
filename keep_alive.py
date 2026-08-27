# 🌐 Keep-Alive Server — ដើម្បីអោយ UptimeRobot ping រក្សា bot ដំណើរការ 24/7
from flask import Flask
from threading import Thread
import config

app = Flask(__name__)


@app.route("/")
def home():
    return "🖤 BLACK SHADOW Bot Online ✅"


def _run():
    app.run(host="0.0.0.0", port=config.PORT)


def keep_alive():
    t = Thread(target=_run)
    t.daemon = True
    t.start()
    print(f"🌐 Keep-alive server ដំណើរការនៅ port {config.PORT}")
