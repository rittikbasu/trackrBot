import os
import flask
import requests
from threading import Thread

app = flask.Flask(__name__)
sess = requests.Session()

proxy_key = os.environ.get('proxy_key')

@app.route('/')
def home():
    return "TrackrBot"

@app.route(proxy_key, defaults={"path": ""}, methods=["GET", "POST", "DELETE"])
@app.route("/<path:path>", methods=["GET", "POST", "DELETE"])
def proxy(path):
  url = os.environ["REPLIT_DB_URL"]
  if flask.request.path != proxy_key:
    key = flask.request.path.replace(proxy_key,'')
    url += key

  req = requests.Request(flask.request.method, url, data=flask.request.form, params=flask.request.args).prepare()
  resp = sess.send(req)

  proxy_resp = flask.make_response(resp.text)
  proxy_resp.status_code = resp.status_code
  for k, v in resp.headers.items():
    proxy_resp.headers[k] = v

  return proxy_resp
    
def run():
    app.run(host='0.0.0.0', port=9000)


def keep_alive():
    t = Thread(target=run)
    t.start()
