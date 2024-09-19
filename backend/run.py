from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from register import register_routes
import schedule
import threading
import asyncio
import time
from datetime import datetime, timedelta
from views.mail import mail

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

register_routes(app)

async def send_mail_job():
    # Replace this with your actual mail sending logic
    await mail()

def run_send_mail_job():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_mail_job())

# Schedule the task to run every day at 15:08
schedule.every().day.at("17:18").do(lambda: threading.Thread(target=run_send_mail_job).start())

def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    import uvicorn

    # Start the scheduler in a separate thread
    threading.Thread(target=scheduler, daemon=True).start()

    # Run FastAPI
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)

