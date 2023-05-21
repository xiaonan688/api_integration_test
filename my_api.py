"""encapulate api"""
import requests 
from cfg import *

class FastAPI:

    def get_root(self):
        response = requests.get(HOST+ROOT_URL)
        return response
    

    def create_task(self, content:str, is_done:bool):
        payload={
        "content": content,
        "user_id": USER_ID,
        "is_done": is_done
        }
        response = requests.put(HOST+CREATE_TASK_URL, json=payload)

        return response
    

    def get_task(self, task_id:str):
        response = requests.get(HOST+GET_TASK_ID_URL+task_id)
        return response
    

    def list_tasks(self, user_id:str):
        response = requests.get(HOST+LIST_TASKS_URL+user_id)
        return response
    

    def update_task(self, content:str, task_id:str, is_done:bool):
        payload={
                "content": content,
                "user_id": USER_ID,
                "task_id": task_id,
                "is_done": is_done
                }
        response = requests.put(HOST+UPDATE_TASK_URL, json=payload)
        return response
    
    
    def delete_task(self, task_id :str):
        response = requests.delete(HOST+DELETE_TASK_URL+task_id )
        return response
    

    def delete_all_tasks(self):
        list_tasks_response = fastapi.list_tasks(USER_ID)
        if list_tasks_response.status_code == 200:
            list_tasks_data = list_tasks_response.json()
            tasks = list_tasks_data["tasks"]
            if tasks:
                task_ids = [i["task_id"] for i in tasks]
                for i in task_ids:
                    fastapi.delete_task(i)
        else:
            print("Status code exception")

fastapi = FastAPI()