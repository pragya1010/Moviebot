from flask import Flask, request, jsonify, render_template
from flask_ngrok import run_with_ngrok
import os
import dialogflow_v2 as dialogflow
import requests
import json
import pusher

app = Flask(__name__)


# run_with_ngrok(app)  # Start ngrok when app is run

@app.route('/')
def index():
    return render_template('index.html')



API_KEY = 'XXXX'
project_id = 'erica-6500d'

GOOGLE_APPLICATION_CREDENTIALS = {
XXXX
}

OMDB_API_KEY = API_KEY

project_id = 'XXX'
DIALOGFLOW_PROJECT_ID = project_id

# GOOGLE_APPLICATION_CREDENTIALS=Erica-b9a6ceb122dc.json
# Pusher creds
app_id = "XXXX"
key = "XXXXX"
secret = "XXXX"
cluster = "XXX"



# http://www.omdbapi.com/?t=Black Panther&apikey=d94c6fa8
@app.route('/get_movie_detail', methods=['POST'])
def get_movie_detail():
    data = request.get_json(silent=True)
    print("---------------------Hello Pragya-----------------------------")
    print(data)
    movie = data['queryResult']['parameters']['movie']
    print("Movie : {}", movie)
    api_key = 'XXXXX'

    movie_detail = requests.get('http://www.omdbapi.com/?t={0}&apikey={1}'.format(movie, api_key)).content
    movie_detail = json.loads(movie_detail)
    response = """
        Title : {0}
        Released: {1}
        Actors: {2}
        Plot: {3}
        
    """.format(movie_detail['Title'], movie_detail['Released'], movie_detail['Actors'], movie_detail['Plot'])
    response2 =movie_detail['Poster']

    reply = {
        "fulfillmentText": response,
        "poster": movie_detail['Poster']
        
    }

    print("reply: {}".format(reply))

    return jsonify(reply)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    if text:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)

        print('=' * 20)
        print('Text input: {}'.format(query_input))
        print('Query text: {}'.format(query_input))
        print('Response: {}'.format(response))
        # print('Detected intent: {} \n'.format(
        #     query_input.intent.display_name))
        # print('Fulfillment text: {}\n'.format(
        #     query_result.fulfillment_text))

        return response.query_result.fulfillment_text


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = 'YOUR PROJECT ID'
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = {"message": fulfillment_text}
    

    # socketId = request.form['socketId']
    # pusher_client.trigger('movie_bot', 'new_message',
    #                       {'human_message': message, 'bot_message': fulfillment_text})

    print("fulfillment_text: {}".format(fulfillment_text))
    print("response_text: {}".format(response_text))

    return jsonify(response_text)


# run Flask app
if __name__ == "__main__":
    app.run()
    # app.run(host='0.0.0.0')
