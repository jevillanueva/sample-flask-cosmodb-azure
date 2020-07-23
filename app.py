from quart import Quart, render_template, request, url_for, Response
from models.counter import addVisitorRoot, viewVisitorRoot
from http import HTTPStatus
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
app = Quart(__name__)

@app.route("/")
def hello():
    addVisitorRoot()
    views = viewVisitorRoot()
    return "<h1 style='color:blue'>Hello There! Views: {0}</h1>".format(views)


@app.route("/api/messages", methods=["POST"])
async def messages() -> Response:
    print ("HERE")
    if "application/json" in request.headers["Content-Type"]:
        body = await request.get_json()
    else:
        return Response(response="", status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    print (body)
    activity = Activity().deserialize(body)
    print (activity)
    auth_header = request.headers["Authorization"] if "Authorization" in request.headers else ""
    response = await ADAPTER.process_activity(activity, auth_header, bot.on_turn)
    if response:
        return  Response(response="",status=HTTPStatus.CREATED)
    return  Response(response="",status=HTTPStatus.OK)


if __name__ == "__main__":
    app.run(host='0.0.0.0')