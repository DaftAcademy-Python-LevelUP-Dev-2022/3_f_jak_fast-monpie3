# Do not put any other code or imports here


class HerokuApp:
    app_url = "http://127.0.0.1:8000/"  # Fill your heroku app url here


from fastapi import FastAPI, Depends, Response, status, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials


app = FastAPI()
security = HTTPBasic()

@app.get("/start", response_class=HTMLResponse)
def index_start():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>The unix epoch started at 1970-01-01</h1>
        </body>
    </html>
    """


    
@app.post("/check", response_class=HTMLResponse)
def index_start(credentials: HTTPBasicCredentials = Depends(security)):
    try: 
        my_date_validated = datetime.datetime.strptime(credentials.password, "%Y-%m-%d")
        today = datetime.datetime.now()
        
        delta = (today - my_date_validated)
        
        age = int(delta.days/365.25)
        if age >= 16:
            return f"""
            <html>
                <head>
                    <title>Some HTML in here</title>
                </head>
                <body>
                    <h1>Welcome {credentials.username}! You are {age}</h1>
                </body>
            </html>
            """
        else: 
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    except ValueError:  
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    
    
