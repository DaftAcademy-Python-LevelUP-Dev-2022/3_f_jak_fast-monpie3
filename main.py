# Do not put any other code or imports here


class HerokuApp:
    app_url = "http://127.0.0.1:8000/"  # Fill your heroku app url here


from fastapi import FastAPI, Depends, Response, status, HTTPException, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Union

app = FastAPI()
security = HTTPBasic()

@app.get("/")
def root():
    return "Hi there!👋"
    
    
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
    
    
class Format_Details(BaseModel):
    format: str
        
    
@app.get("/info")
def check_format(format: Format_Details, response: Response, user_agent: Union[str, None] = Header(default=None)):
    json_respone  = {
    "user_agent": user_agent
    }
    html_response = """<input type="text" id=user-agent name=agent value="{user_agent}">"""
    if format.format == "html":
        return html_response 
    elif format.format == "json": 
        return json_respone     
    else: 
        response.status_code = status.HTTP_400_BAD_REQUEST
