from fastapi import FastAPI
from pydantic import BaseModel #Pydantic ensures the data types are correct.
from typing import Optional
import httpx

app=FastAPI()
DJANGO_API_URL = "http://127.0.0.1:8001" 

class analyze_pr_request(BaseModel):
    url:str
    pr_number:int
    github_token:Optional[str]= None

@app.post("/start_task/")
async def start_task_endpoint(task_req:analyze_pr_request ):
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
        f"{DJANGO_API_URL}/start_task/",
        data={
                "url": task_req.url,
                "pr_number": task_req.pr_number,
                "github_token": task_req.github_token,

            }
            
        )
        data1={
                "url": task_req.url,
                "pr_number": task_req.pr_number,
                "github_token": task_req.github_token,

            }
        print(data1)
        
        if response.status_code != 200:
            return {"error": "Failed to start task", "details": response.text}
        task_id = response.json().get("task_id")
        #print(task_id)
        return {"task_id": task_id, "status": "Task started"}

    

@app.get("/task_status/{task_id}/")
async def task_status_endpoint(task_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_API_URL}/task_status_view/{task_id}/")
        print("working")
        print(response)
        return response.json()
    
    return {"message": "something went wrong",}

