"""test my_api:
        create item
            create 
            get
        update item
            create 
            update
            get
        list items
            create
            list
        delete item
            create
            delete
            get
"""
import pytest
# import uuid
from my_api import fastapi
from cfg import *
from loguru import logger



@pytest.fixture()
def del_task_fixt():
    fastapi.delete_all_tasks()
    yield
    fastapi.delete_all_tasks()


# def test_site_available():
#     expect = {"message": "Hello World from Todo API"}
#     response = fastapi.get_root()

#     assert response.status_code == 200
#     data = response.json()

#     assert data == expect


@pytest.mark.usefixtures("del_task_fixt")
def test_create_task():
    payload = {"content": "go to the library", "is_done": False}
    create_task_response = fastapi.create_task(payload["content"], payload["is_done"])
    assert create_task_response.status_code == 200

    create_task_data = create_task_response.json()
    logger.info(create_task_data)
    task_id = create_task_data["task"]["task_id"]
    assert create_task_data["task"]["user_id"] == USER_ID
    assert create_task_data["task"]["content"] == payload["content"]

    get_task_response = fastapi.get_task(create_task_data["task"]["task_id"])
    assert get_task_response.status_code == 200

    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == USER_ID
    assert get_task_data["task_id"] == task_id


@pytest.mark.usefixtures("del_task_fixt")
def test_create_update_task():
    payload = {"content": "go to the gym", "is_done": False}
    create_task_response = fastapi.create_task(payload["content"], payload["is_done"])
    assert create_task_response.status_code == 200

    create_task_data = create_task_response.json()
    logger.info(create_task_data)

    task_id = create_task_data["task"]["task_id"]
    assert create_task_data["task"]["user_id"] == USER_ID 
    assert create_task_data["task"]["content"] == payload["content"]

    get_task_response = fastapi.get_task(task_id)
    assert get_task_response.status_code == 200

    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == USER_ID
    assert get_task_data["task_id"] == task_id

    new_payload = {"content": "go out and get some fresh air", "is_done": True}
    update_task_response = fastapi.update_task(new_payload["content"], task_id, new_payload["is_done"])
    assert update_task_response.status_code == 200
    update_task_data = update_task_response.json()

    assert update_task_data["updated_task_id"] == task_id

    get_task_response = fastapi.get_task(task_id)
    assert get_task_response.status_code == 200

    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["user_id"] == USER_ID
    assert get_task_data["task_id"] == task_id


@pytest.mark.usefixtures("del_task_fixt")
def test_create_list_task():
    payload = {"content": "go home", "is_done": False}
    create_task_response = fastapi.create_task(payload["content"], payload["is_done"])
    assert create_task_response.status_code == 200

    create_task_data = create_task_response.json()
    logger.info(create_task_data)
    task_id = create_task_data["task"]["task_id"]
    assert create_task_data["task"]["user_id"] == USER_ID
    assert create_task_data["task"]["content"] == payload["content"]

    get_task_response = fastapi.get_task(task_id)
    assert get_task_response.status_code == 200

    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == USER_ID
    assert get_task_data["task_id"] == task_id

    list_task_response = fastapi.list_tasks(USER_ID)
    assert list_task_response.status_code == 200

    list_task_data = list_task_response.json()
    result = [{key: value
               for key, value in task.items() if key in ["is_done", "content"]} for task in list_task_data["tasks"]]
    assert payload == result[0]



def test_create_delete_get_task():
    payload = {"content": "relax for ten mins", "is_done": False}
    create_task_response = fastapi.create_task(payload["content"], payload["is_done"])
    assert create_task_response.status_code == 200

    create_task_data = create_task_response.json()
    logger.info(create_task_data)
    task_id = create_task_data["task"]["task_id"]
    assert create_task_data["task"]["user_id"] == USER_ID
    assert create_task_data["task"]["content"] == payload["content"]

    get_task_response = fastapi.get_task(task_id)
    assert get_task_response.status_code == 200

    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == USER_ID
    assert get_task_data["task_id"] == task_id

    delete_task_response = fastapi.delete_task(task_id)
    assert delete_task_response.status_code == 200

    delete_task_data = delete_task_response.json()
    assert delete_task_data == {"deleted_task_id": task_id}

    get_task_response = fastapi.get_task(task_id)
    assert get_task_response.status_code == 404

    get_task_data = get_task_response.json()
    assert get_task_data == {"detail": f"Task {task_id} not found"}
