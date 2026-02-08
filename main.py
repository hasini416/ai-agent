from fastapi import FastAPI, HTTPException, Request #for setting up the api
from fastapi.templating import Jinja2Templates #render html
from pydantic import BaseModel
from agent import run_agent #run the agen from the agent.py
# import uvicorn

#initialize the applicationa nd the template 
app = FastAPI()
templates = Jinja2Templates(directory="templates")


#define the type api going to accept 
#Request model
class AgentRequest(BaseModel):
    """Request model for agent invocation"""
    prompt: str

#Response model
class AgentResponse(BaseModel):
    """Response model for agent invocation""" 
    response: str   


#home root for seeing the website 
@app.get("/")
async def home(request: Request):
    """Serve the main html interface"""
    return templates.TemplateResponse("index.html",{"request":request})


@app.post("/agent", response_model=AgentResponse)
async def invoke_agent(request:AgentRequest):
    """
    Invoke the AI agent with a prompt.
    the agent can read and write text files based on natural language instructions.
    """

    try:
        if not request.prompt.strip():
            raise HTTPException(status_code=400,detail="Prompt cannot be empty")
        
        result = run_agent(request.prompt)
        return AgentResponse(response = result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error invoking agent : {str(e)}")
    

# uvicorn.run(app, host="0.0.0.0",port=8000)    