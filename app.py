from flask import Flask, render_template, request, url_for, Response
from models.counter import addVisitorRoot, viewVisitorRoot
import asyncio
import os
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
app = Flask(__name__)

@app.route("/")
def hello():
    addVisitorRoot()
    views = viewVisitorRoot()
    return "<h1 style='color:blue'>Hello There! Views: {0}</h1>".format(views)


@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)
    print (body)
    activity = Activity().deserialize(body)
    print (activity)
    auth_header = (
        request.headers["Authorization"] if "Authorization" in request.headers else ""
    )

    async def aux_func(turn_context):
        await bot.on_turn(turn_context)

    try:
        task = LOOP.create_task(
            ADAPTER.process_activity(activity, auth_header, aux_func)
        )
        LOOP.run_until_complete(task)
        return Response(status=201)
    except Exception as exception:
        raise exception

if __name__ == "__main__":
    app.run(host='0.0.0.0')