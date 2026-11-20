#!/opt/sweetbot/venv/bin/python3

from flask import Flask
import argparse
import github
import mattermost
import upload

parser = argparse.ArgumentParser()
parser.add_argument("--auth", action="store_true",
                    help="require a valid token on POST /upload")
args, _ = parser.parse_known_args()

app = Flask(__name__)
app.config["UPLOAD_AUTH"] = args.auth
app.register_blueprint(github.bp)
app.register_blueprint(upload.bp)

# Maximum upload size: 5 MB
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

mattermost.post('I\'m back online! :wave:')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
