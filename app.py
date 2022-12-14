import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC21377aaabc7c343ef854d2785a8d8a53'
    TWILIO_SYNC_SERVICE_SID = 'IS61a38e004d31e786c87884fe66b6b99d'
    TWILIO_API_KEY = 'SKfe449b6cb3b184e26a03433024693c70'
    TWILIO_API_SECRET = 'SOCnx3gA9JUO4skRlfTL74AW0DfMixrN'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    notepad_text = request.form["text"]
    
    with open("workfile.txt", "w") as f:  
        f.write(notepad_text)
    
    text_storage_path = "workfile.txt"
    
    return send_file(text_storage_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)

#TSID: AC21377aaabc7c343ef854d2785a8d8a53
#SSID: IS61a38e004d31e786c87884fe66b6b99d
#API key: SKfe449b6cb3b184e26a03433024693c70
#Secret key: SOCnx3gA9JUO4skRlfTL74AW0DfMixrN