from flask import *
from whitenoise import WhiteNoise


app = Flask(__name__, static_folder="static")
app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/", prefix="static/", index_file="index.html", autorefresh=True)

# You can change the prefix up above and get rid of this route if you just want to host static (which begs the question why you don't use something simpler like Github Pages)
@app.route('/', methods=['GET'])
def hello():
  return send_from_directory("static", "index.html")

if __name__ == "__main__":
  app.run(threaded=True, port=9000)