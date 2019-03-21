from flask import Flask, request, jsonify, render_template
from flask_ngrok import run_with_ngrok
import os
import dialogflow_v2 as dialogflow
import requests
import json
import pusher

app = Flask(__name__)
#run_with_ngrok(app)  # Start ngrok when app is run

@app.route('/')
def index():
        return render_template('index.html')


#API_KEY = 'd94c6fa8'
API_KEY = 'd94c6fa8'
project_id = 'erica-6500d'

GOOGLE_APPLICATION_CREDENTIALS={
  "type": "service_account",
  "project_id": "erica-6500d",
  "private_key_id": "b9a6ceb122dcd1b48796588525368a3938e821d1",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDyWlh5RXicSso4\ng8+egvX8zoMedULGlcUFLApsikV+LmngqPb2y67THLAeKkmxB9cx9rTMIdqulvA1\nGkfwaxSLNS55nEsM5g47KvHlpjY0Mg973AzGPH6IwYYwCKA3HPgrrbfjhKb/SkXC\nDMvQvViHxU8TyetFnjhqJgvpaPqrmEWF0wTXckSCzzu1vk8s/aQJrNIlUC0IyIxf\nuQ43DsobTJo/YlNoFVIYn9Wfy6sWdjAVjPPQF9S6Ai0h9vQaXjNgBq8ZKmWKM2JS\nP7e4IbvBCpvE7vhMU22B49TZ6joJYV079KGMMjCB6bEr0V4HG58/MEFO7bA/txrm\nRWicxbonAgMBAAECggEAJagCDT3NIsPALg3VCbUhkZlo6CeiK4cD6OzR5dGKQLPn\ngZ/fV7OIQ4c2mklJz/b+6eWCbCFqgCw1wJqHyQRqWcL2qLCvPJ7WYT0n/t3XmD6b\nB0zGs1qc8pTXS8lbU5TtvqOsae6noA0jT6Z7WMDC672trs51/wg5jczBlw/XuyeN\nZdCfp8xx55rPujaO9hpTNW1p3IR7zN6U6lxlUd3npcdBLEw9T/AEgT1ZUIAAobRT\nz0DipuKJHoxyrYOdgwsd8plRrLapWLYFE8k99J5+gEc3ifqzgMxOqPgOIFeaCqL7\nZs0FfphMTmXusSvmre0mxoyV5I6Y5y5IVcbJWtCjmQKBgQD6jQ2VzI4MftVJ3XKv\n3uCLEgdel5qwtMu1i4/Iu/LJFqI89uk/TPZdtKTq3PB1RBeXiJc+acqpqwoPgvKj\nCICy1UkrueBeRy5A+zzisMzXoQnYKjJ7pQ7lMsOz/LGba5Mv+IHKZG/rJDbMUoDs\nOyi6AehoAylImxnXagI6Ff3QpQKBgQD3n6ZMdupPZPkuofX3VB1qoMwb/i0kzpxV\nFT2eHiLhH6SiOmJcoVWyxNKncLDle1x4oikSZeT8+Y+UAY7cuxD9KvNORp5SMdCr\nIwN+BdZIiiahIfU9o+Dqn9tktPQt1Sm12q4Jnu1p4HiESKTksMbbl9nM2R3kN412\nd7vzYdm52wKBgQDnGHMPWD0tCU9xce/2h3xUyaxCc1Ma6ad7K97TJ4goMdgyowtA\nd5xFkfkLJ/4iK0wXWMUnrCxhkoEVDZL/DTinulJjIm7whncDOLhP3wMRYFfUKhem\nM/gpL0mTGeA3mmGIPY55P2p7WEuy6eY//dDywA+84C2T6ntLVVv4d5BEgQKBgQDF\ntRxsFM4D0hT6XKosbWaHShdtikW1C5nafPkTk/A5WrByLrd2SgJIl8mxktJKh3JP\nhvnQDLcGHKO8gnn0Vw+7c12L8+pYqhl3ap9RMYvjoxowsRJDwuLDshrTj38eUQHa\nht1KJTBdxrGyvOWbCmHb1qQ5YGjzXD+AhRz1t/zE3QKBgEcjX7cytaOV/Tt3px9a\n9vUQ6MOH8A5ewEZTSLYd1IN9aL//WdlL5Fnxhf6MHXhPX470e+N9vjbOMFY/Nu5j\n+1bJPyi0Z/RjQezU+9bhNVOxQAVq08+pKWf9y+AikMUskzpguBCEYuf7TabN/gwP\n0tBk7AxOGeXxOs//t0t05b9e\n-----END PRIVATE KEY-----\n",
  "client_email": "dialogflow-dbqtce@erica-6500d.iam.gserviceaccount.com",
  "client_id": "117486695336074591323",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dialogflow-dbqtce%40erica-6500d.iam.gserviceaccount.com"
}

OMDB_API_KEY=API_KEY

project_id = 'erica-6500d'
DIALOGFLOW_PROJECT_ID=project_id

#GOOGLE_APPLICATION_CREDENTIALS=Erica-b9a6ceb122dc.json
#Pusher creds
app_id = "702823"
key = "b80b905f027269656aac"
secret = "9e6eea71654fd76fea20"
cluster = "us2"

PUSHER_APP_ID=app_id
PUSHER_KEY=key
PUSHER_SECRET=secret
PUSHER_CLUSTER=cluster
# pusher_client = pusher.Pusher(
#         app_id=os.getenv('PUSHER_APP_ID'),
#         key=os.getenv('PUSHER_KEY'),
#         secret=os.getenv('PUSHER_SECRET'),
#         cluster=os.getenv('PUSHER_CLUSTER'),
#         ssl=True)
pusher_client = pusher.Pusher(
        app_id=PUSHER_APP_ID,
        key=PUSHER_KEY,
        secret=PUSHER_SECRET,
        cluster=PUSHER_CLUSTER,
        ssl=True)



#http://www.omdbapi.com/?t=Black Panther&apikey=d94c6fa8
@app.route('/get_movie_detail', methods=['POST'])
def get_movie_detail():
    data = request.get_json(silent=True)
    print("---------------------Hello Pragya-----------------------------")
    print(data)
    movie = data['queryResult']['parameters']['movie']
    print("Movie : {}", movie)
    api_key = 'd94c6fa8'

    movie_detail = requests.get('http://www.omdbapi.com/?t={0}&apikey={1}'.format(movie, api_key)).content
    movie_detail = json.loads(movie_detail)
    response = """
        Title : {0}
        Released: {1}
        Actors: {2}
        Plot: {3}
    """.format(movie_detail['Title'], movie_detail['Released'], movie_detail['Actors'], movie_detail['Plot'])

    reply = {
        "fulfillmentText": response,
    }

    print("reply: {}".format(reply))

    return jsonify(reply)

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    if text:
        text_input = dialogflow.types.TextInput(text = text, language_code = language_code)
        query_input = dialogflow.types.QueryInput(text = text_input)
        response = session_client.detect_intent(session = session, query_input=query_input)

        print('=' * 20)
        print('Text input: {}'.format(query_input))
        print('Query text: {}'.format(query_input))
        print('Response: {}'.format(response))
        # print('Detected intent: {} \n'.format(
        #     query_input.intent.display_name))
        # print('Fulfillment text: {}\n'.format(
        #     query_result.fulfillment_text))

        return response.query_result.fulfillment_text

def get_movie_detail_fail(movie):
    api_key = 'd94c6fa8'
    movie_detail = requests.get('http://www.omdbapi.com/?t={0}&apikey={1}'.format(movie, api_key)).content
    print(movie_detail)
    movie_detail = json.loads(movie_detail)
    print(movie_detail)
    response = """
            Title : {0}
            Released: {1}
            Actors: {2}
            Plot: {3}
        """.format(movie_detail['Title'], movie_detail['Released'], movie_detail['Actors'], movie_detail['Plot'])

    reply = {
        "fulfillmentText": response,
    }

    print("reply: {}".format(reply))
    return jsonify(reply)

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = 'erica-6500d'
    fulfillment_text = detect_intent_texts(project_id,"unique",message,'en')
    response_text = {"message": fulfillment_text}

    #socketId = request.form['socketId']
    # pusher_client.trigger('movie_bot', 'new_message',
    #                       {'human_message': message, 'bot_message': fulfillment_text})

    print("fulfillment_text: {}".format(fulfillment_text))
    print("response_text: {}".format(response_text))

    if len(response_text)<2:
        response_text = get_movie_detail_fail(response_text['message'])

    return jsonify(response_text)

# run Flask app
if __name__ == "__main__":
        app.run()
        #app.run(host='0.0.0.0')
