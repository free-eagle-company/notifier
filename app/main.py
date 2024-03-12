import os
import requests
from fastapi import FastAPI, APIRouter, Body, Response, status

SERVER_HOST = os.environ.get("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.environ.get("SERVER_PORT", 1234))
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

app = FastAPI(
    title="Send messages", openapi_url="/openapi.json"
)

api_router = APIRouter()
headers = {
    "Content-Type": "application/json"
}


@app.post('/post-message')
async def post_message_to_channel(message: str = Body(...)):
    response = requests.post(DISCORD_WEBHOOK_URL, json={"content": message}, headers=headers)
    if response.status_code != 204:
        print("Error sending message to Discord channel:", response.json())
        return Response(status_code=response.status_code)
    else:
        print("Message sent successfully to Discord channel!")
        return Response(status_code=status.HTTP_200_OK)


@app.get('/health-check')
async def health_check():
    return Response(status_code=status.HTTP_200_OK)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
