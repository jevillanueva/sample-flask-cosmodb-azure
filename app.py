from flask import Flask, render_template, request, url_for, Response
from models.counter import addVisitorRoot, viewVisitorRoot
from http import HTTPStatus
from twilio.twiml.messaging_response import MessagingResponse
import asyncio
import os
from  directLineAPI import DirectLineAPI
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    TurnContext
)
from botbuilder.schema import Activity
from bot import EchoBot
bot = EchoBot()
SETTINGS = BotFrameworkAdapterSettings(os.getenv("MicrosoftAppId",""),os.getenv("MicrosoftAppPassword",""))
ADAPTER = BotFrameworkAdapter(SETTINGS)
LOOP = asyncio.get_event_loop()

botDirectLine = DirectLineAPI(os.getenv("MicrosoftDirectLineToken",""))
app = Flask(__name__)
secretBot = os.getenv("BotSecretID","Secret")
@app.route("/")
def hello():
    addVisitorRoot()
    views = viewVisitorRoot()
    return "<h1 style='color:blue'>Hello There! Views: {0}</h1> <iframe src='https://webchat.botframework.com/embed/flask-sample-mongo-bot?s={1}'  style='min-width: 400px; width: 100%; min-height: 500px;'></iframe>".format(views,secretBot)


@app.route("/api/messages", methods=["POST"])
def messages() -> Response:
    print ("HERE")
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    print (body)
    activity = Activity().deserialize(body)
    print (activity)
    auth_header = request.headers["Authorization"] if "Authorization" in request.headers else ""

    async def aux_func(turn_context):
        await bot.on_turn(turn_context)

    try:
        task = LOOP.create_task(
            ADAPTER.process_activity(activity, auth_header, aux_func)
        )
        LOOP.run_until_complete(task)
        return Response(status=HTTPStatus.CREATED)
    except Exception as exception:
        raise exception

GOOD_BOY_URL = "https://images.unsplash.com/photo-1518717758536-85ae29035b6d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80"
@app.route("/whatsapp", methods=["POST"])
def reply_whatsapp():
    response = MessagingResponse()
    print ('#'*30)
    values = request.values
    print (values)
    num_media = int(values.get("NumMedia"))
    bodyText = values.get("Body")
    latitude = values.get("Latitude",None)
    longitude = values.get("Longitude",None)
    if not num_media:
        #No contiene media data.
        if latitude is not None or longitude is not None:
            #Contiene gps
            msg = response.message("Thanks for you Position")
        else:
            #Contiene solo texto
            botDirectLine.send_message(bodyText)
            botresponse = botDirectLine.get_message()
            msg = response.message(botresponse)
    else:
        msg = response.message("Thanks for the image. Here's one for you!")
        msg.media(GOOD_BOY_URL)
    print ('#'*30)
    print (msg)
    print (response)
    return str(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0')