import pandas as pd
# FastAPI imports
from fastapi import FastAPI, Body, UploadFile, Depends, BackgroundTasks, Response, status
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, StreamingResponse
from starlette.requests import Request
import json
import pickle
from fast_prototyping.main import ClassBuilder
from fast_prototyping.mainjs import JsClassBuilder
import os

app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["root"])
async def read_root():
    response = RedirectResponse(url='/docs')
    return response

###################################### ROUTER ENDPOINTS ################################

@app.post('/router/CREATE')
def handle_create_endpoint(link=Body(...)):

    final_data = []
    for li in link:
        final_data.append(li)

    with open('router_links.json', 'wb') as fp:
        pickle.dump(final_data, fp)

    with open('router_links.json', 'rb') as fp:
        data = pickle.load(fp)

    print(data)

    return {'response': 'okay'}


@app.get('/router/READ')
async def handle_router_query():
    with open('router_links.json', 'rb') as fp:
        data = pickle.load(fp)

    try:
        data = json.loads(json.dumps(data))
    except TypeError:
        data = []

    return {'response': data}

@app.post('/router/UPLOAD')
async def handle_router_upload(link=Body(...)):
    try:
        link = json.loads(link.decode())
    except:
        print(type(link))

    final_data = []
    with open('router_links.json', 'rb') as fp:
        try:
            old_data = pickle.load(fp)
        except EOFError:
            old_data = []

    for data in old_data:
        final_data.append(data)

    final_data.append(link)

    with open('router_links.json', 'wb') as fp:
        pickle.dump(final_data, fp)

    with open('router_links.json', 'rb') as fp:
        data = pickle.load(fp)

    print(link)

    return {'response': 'okay'}


@app.post('/router/DELETE')
async def handle_router_delete(name=Body(...)):
    try:
        name = json.loads(name.decode())
    except:
        print(type(name))

    final_data = []
    with open('router_links.json', 'rb') as fp:
        try:
            old_data = pickle.load(fp)
        except EOFError:
            old_data = []

    len_before = len(final_data)
    for data in old_data:
        final_data.append(data)

    final_data = list(filter(lambda lnk: lnk['title'] != name, final_data))
    len_after = len(final_data)

    with open('router_links.json', 'wb') as fp:
        pickle.dump(final_data, fp)

    with open('router_links.json', 'rb') as fp:
        data = pickle.load(fp)

    print(name)
    print(len_before - len_after)

    return {'response': 'okay'}

############################################### SOFIA - DIET ENDPOINTS ###################################


@app.post('/sofia-diet/food/CREATE')
async def handle_upload(food=Body(...)):
    try:
        food = json.loads(food.decode())
    except:
        print(type(food))

    final_data = []
    with open('sofia-diet_food.json', 'rb') as fp:
        try:
            old_data = pickle.load(fp)
        except EOFError:
            old_data = []

    for data in old_data:
        final_data.append(data)

    final_data.append(food)
    with open('sofia-diet_food.json', 'wb') as fp:
        pickle.dump(final_data, fp)

    with open('sofia-diet_food.json', 'rb') as fp:
        data = pickle.load(fp)

    print(data)

    return {'response': 'okay'}


@app.get('/sofia-diet/food/READ')
async def handle_read_food():
    with open('sofia-diet_food.json', 'rb') as fp:
        data = pickle.load(fp)

    try:
        data = json.loads(json.dumps(data))
    except TypeError:
        data = []

    return {'response': data}


@app.post('/sofia-diet/meal/CREATE')
async def handle_meal_upload(meal=Body(...)):
    try:
        meal = json.loads(meal.decode())
    except:
        print(type(meal))

    final_data = []
    with open('sofia-diet_meal.json', 'rb') as fp:
        try:
            old_data = pickle.load(fp)
        except EOFError:
            old_data = []

    for data in old_data:
        final_data.append(data)

    final_data.append(meal)
    with open('sofia-diet_meal.json', 'wb') as fp:
        pickle.dump(final_data, fp)

    with open('sofia-diet_meal.json', 'rb') as fp:
        data = pickle.load(fp)

    print(data)

    return {'response': 'okay'}


@app.get('/sofia-diet/meal/READ')
async def handle_meal_query():
    with open('sofia-diet_meal.json', 'rb') as fp:
        data = pickle.load(fp)

    try:
        data = json.loads(json.dumps(data))
    except TypeError:
        data = []

    return {'response': data}


@app.get('/sofia-diet/diet/READ')
async def handle_meal_query():
    with open('sofia-diet_diet.json', 'rb') as fp:
        data = pickle.load(fp)

    try:
        data = json.loads(json.dumps(data))
    except TypeError:
        data = []

    return {'response': data}


@app.post('/sofia-diet/diet/CREATE')
async def handle_create_diet(diet=Body(...)):
    try:
        diet = json.loads(diet.decode())
    except:
        print(type(diet))
    final_data = []
    with open('sofia-diet_diet.json', 'rb') as fp:
        try:
            old_data = pickle.load(fp)
        except EOFError:
            old_data = []

    for data in old_data:
        final_data.append(data)

    final_data.append(diet)
    with open('sofia-diet_diet.json', 'wb') as fp:
        pickle.dump(final_data, fp)

    with open('sofia-diet_diet.json', 'rb') as fp:
        data = pickle.load(fp)

    print(data)

    return {'response': 'okay '}


@app.post('/draw-uml/CREATE')
async def handle_create_diagram(diagram=Body(...)):
    try:
        diagram = json.loads(diagram.decode())
    except:
        print(type(diagram))

    meta_data = diagram[0]
    final_class = ""
    final_js_class = ""
    class_names = [object["data"]['objectName'] for object in meta_data]
    for object in meta_data:
        class_name = (object["data"]['objectName'],object["data"]['comment'])
        methods = []
        properties = []
        for method in object["data"]["gridTable"]:
            if method["signature"].find("()") == -1:
                properties.append((method["signature"], method["type"]))
            else:
                methods.append(
                    (method["signature"], method["comment"], method["type"]))

        new_class = ClassBuilder(class_name, methods, properties)
        final_class += new_class.check_types(class_names)
        final_class += new_class.build_class_name()
        final_class += new_class.build_constructor_head()
        final_class += new_class.build_constructor_body()
        final_class += new_class.build_class_methods()

        new_js_class = JsClassBuilder(class_name, methods, properties)
        final_js_class += new_js_class.build_class_name(
            class_name[0] == class_names[0])
        final_js_class += new_js_class.build_constructor_head()
        final_js_class += new_js_class.build_constructor_body()
        final_js_class += new_js_class.build_class_methods()
        os.remove('file.py')
        os.remove('file.js')
        
        with open('file.py', "w") as f:
            f.write(final_class)

        with open('file.js', 'w') as f:
            f.write(final_js_class)

    return {"response", "files create successfully ✅"}

@app.post('/draw-uml/CREATE/test')
async def handle_create_diagram(diagram=Body(...)):
    try:
        diagram = json.loads(diagram.decode())
    except:
        print(type(diagram))

    meta_data = diagram[0]
    final_class = ""
    class_names = [object["data"]['objectName'] for object in meta_data]
    for object in meta_data:
        class_name = (object["data"]['objectName'],object["data"]['comment'])
        methods = []
        properties = []
        for method in object["data"]["gridTable"]:
            if method["signature"].find("()") == -1:
                properties.append((method["signature"], method["type"]))
            else:
                methods.append(
                    (method["signature"], method["comment"], method["type"]))

        new_class = ClassBuilder(class_name, methods, properties)
        final_class += new_class.check_types(class_names)
        final_class += new_class.build_class_name()
        final_class += new_class.build_constructor_head()
        final_class += new_class.build_constructor_body()
        final_class += new_class.build_class_methods()

        with open('file.py', "w") as f:
            f.write(final_class)

    return {"response", "files create successfully ✅"}


@app.get('/draw-uml/python')
def handle_get_python_file():
    print("get python file called")
    return FileResponse("file.py", media_type="text/x-python", filename="file.py")

@app.get('/draw-uml/python_file')
def handle_get_python_file():
    print("get python file called")
    return FileResponse("file.py", media_type="text/x-python", filename="file.py")

@app.get('/draw-uml/javascript_file')
def handle_get_javascript_file():
    print("get javascript file called")
    return FileResponse("file.js", media_type="text/javascript", filename="file.js")
