from fastapi import FastAPI
from contextlib import asynccontextmanager
from .routers import api_data, report
from .db.db_connect import connectDB
from fastapi.responses import HTMLResponse


app = FastAPI()

@asynccontextmanager
async def lifespan(app):
    client, _, _, _ = connectDB()
    client
    yield
    client.close()

app = FastAPI(lifespan=lifespan)

@app.get('/')
def home():
    welcome_msg = (
        "Welcome to the app!<br><br>"
        "This application features 2 main endpoints:<br>"
        "<strong>api_data</strong> - to fetch data from an external API and store it in the DB.<br>"
        "<strong>report</strong> - to view detailed report data.<br>"
    )
    return HTMLResponse(content=f"<html><body><p>{welcome_msg}</p></body></html>")

app.include_router(api_data.router)
app.include_router(report.router)

