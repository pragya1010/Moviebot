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


# API_KEY = 'd94c6fa8'
API_KEY = 'd94c6fa8'
project_id = 'erica-6500d'

GOOGLE_APPLICATION_CREDENTIALS = {
   XXXX
}

OMDB_API_KEY = API_KEY

project_id = 'erica-6500d'
DIALOGFLOW_PROJECT_ID = project_id

# GOOGLE_APPLICATION_CREDENTIALS=Erica-b9a6ceb122dc.json
# Pusher creds
app_id = "XXXX"
key = "XXXX"
secret = "XXXX"
cluster = "XXXX" 

PUSHER_APP_ID = app_id
PUSHER_KEY = key
PUSHER_SECRET = secret
PUSHER_CLUSTER = cluster
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


# http://www.omdbapi.com/?t=Black Panther&apikey=d94c6fa8
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
    response = """Title : {0}
        Released : {1}
        Actors : {2}
        Plot : {3}
        Rotten Tomatoes Ratings :  {4}
        IMDB Ratings :  {5}
        {6}

    """.format(movie_detail['Title'],
               movie_detail['Released'], movie_detail['Actors'], movie_detail['Plot'],
               movie_detail['Ratings'][1]['Value'],
               movie_detail['imdbRating'], movie_detail['Poster'])

    reply = {
        "fulfillmentText": response,
    }
    poster = {
        "poster": movie_detail['Poster']
    }
    print("reply:-----------> {}".format(reply))

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
    project_id = 'erica-6500d'
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')

    # print("Name--->", name)
    # api_key = 'd94c6fa8'
    #
    # movie_detail = requests.get('http://www.omdbapi.com/?t={0}&apikey={1}'.format(name, api_key)).content
    # movie_detail = json.loads(movie_detail)
    #
    # print(movie_detail['Poster'])

    # socketId = request.form['socketId']
    # pusher_client.trigger('movie_bot', 'new_message',
    #                       {'human_message': message, 'bot_message': fulfillment_text})

    # response_text = {"message": fulfillment_text, "poster":movie_detail['Poster'] }

    ful = fulfillment_text.split("        ")
    details = ful[:-1]
    print(details)

    ful_txt = "        ".join(i for i in details)
    print(ful_txt)

    
    poster = ful[-1]
    print(poster)
    image_url = "<img src = '"+  poster + "';alt=\"Cinque Terre\" width=\"1000\" height=\"1000\">"
    # <img src = ${data.poster} style="height: 100px; width: 100px" >
    # <img src="http://www.hans-zimmer.com/~hybrid/powell/DRAGON3.jpg">


    # response_text = {"message": details, "poster": poster}
    if len(details) > 1:
        
        # response_text = {"message": fulfillment_text, "poster": poster, "validate": len(details)}
        response_text = {"message": ful_txt, "poster": image_url}
    else:
        response_text = {"message": fulfillment_text, "poster": ''}

    if response_text["message"] == '':
        response_text["message"] = "Sorry couldn't fetch details for it."
        
    print("fulfillment_text: {}".format(fulfillment_text))
    print("response_text----------->: {}".format(response_text))

    return jsonify(response_text)


# run Flask app
if __name__ == "__main__":
    app.run()
    # app.run(host='0.0.0.0')
