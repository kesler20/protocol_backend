import os
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
from fast_prototyping.test_main import TestClassBuilder
from sql_db_interface.database_client import DatabaseClient
from sql_db_interface.database_interface import DatabaseInterface

'''
The application backend will take requrest from any client "see origins list set as *"
Nevertheless, the endpoint architecture will take the following form

/application-name/HTTP METHOD/custom

In the case of sofiaApi the custom topic will refer to the name of the Table 
of interest in lowercase
'''

# ---------------------------------------------------#
#                                                    #
#     INTIIALISE APPLICATION AND CONFIGURATIONS      #
#                                                    #
# ---------------------------------------------------#

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

client = DatabaseClient("my_routine.db")
db = DatabaseInterface(client)


@app.get("/", tags=["root"])
async def read_root():
    response = RedirectResponse(url='/docs')
    return response

# ----------------------------------- #
#                                     #
#         APPLICATIONS ENDPOINTS      #
#                                     #
# ------------------------------------#

#----------------- DRAW-UML ----------------#


@app.post('/draw-uml/CREATE')
async def handle_create_diagram(diagram=Body(...)):
    try:
        diagram = json.loads(diagram.decode())
    except:
        print(type(diagram))

    meta_data = diagram[0]
    final_class = ""
    final_js_class = ""
    final_test_class = ""
    class_names = [object["data"]['objectName'] for object in meta_data]
    for object in meta_data:
        class_name = (object["data"]['objectName'], object["data"]['comment'])
        methods = []
        properties = []
        for method in object["data"]["gridTable"]:
            if method["signature"].find("()") == -1:
                properties.append((method["signature"], method["type"]))
            else:
                methods.append(
                    (method["signature"], method["comment"], method["type"]))

        # CREATING THE PYTHON FILE
        new_class = ClassBuilder(class_name, methods, properties)
        final_class += new_class.check_types(class_names)
        final_class += new_class.build_class_name()
        final_class += new_class.build_constructor_head()
        final_class += new_class.build_constructor_body()
        final_class += new_class.build_class_methods()

        # CREATING THE JAVASCRIPT FILE
        new_js_class = JsClassBuilder(class_name, methods, properties)
        final_js_class += new_js_class.build_class_name(
            class_name[0] == class_names[0])
        final_js_class += new_js_class.build_constructor_head()
        final_js_class += new_js_class.build_constructor_body()
        final_js_class += new_js_class.build_class_methods()

        with open('file.py', "w") as f:
            f.write(final_class)

        with open('file.js', 'w') as f:
            f.write(final_js_class)

        # CREATING THE PYTHON TEST FILE
        new_class = TestClassBuilder(class_name, methods, properties)

        if class_name[0] is class_names[0]:
            final_test_class += new_class.check_types(class_names)
            final_test_class += new_class.build_initial_import()

        final_test_class += new_class.build_class_name()
        final_test_class += new_class.build_constructor_head()
        final_test_class += new_class.build_constructor_body()
        final_test_class += new_class.build_class_methods()
        final_test_class += new_class.build_tearDown()

        if class_name[0] is class_names[-1]:
            final_test_class += new_class.build_main_function_call()

        with open('test_file.py', "w") as f:
            f.write(final_test_class)

    return {"response", "files create successfully ✅"}


@app.get('/draw-uml/python_file')
async def handle_get_python_file():
    print("get python file called")
    return FileResponse("file.py", media_type="text/x-python", filename="file.py")


@app.get('/draw-uml/python_test_file')
async def handle_get_python_test_file():
    print("get python test file called")
    return FileResponse("test_file.py", media_type="text/x-python", filename="test_file.py")


@app.get('/draw-uml/javascript_file')
async def handle_get_javascript_file():
    print("get javascript file called")
    return FileResponse("file.js", media_type="text/javascript", filename="file.js")

#-------------- SOFIA API----------------#

def convert_sql_table_to_df(column_names: 'list[str]',db: DatabaseInterface, table_name: str):
    named_rows = [list(zip(column_names, row))
                  for row in db.read_all_values_from_table(table_name)]

    data_frames: 'list[pd.DataFrame]' = []
    for row_id, row in enumerate(named_rows):
        data_array = {row[0]: [row[1]] for row in named_rows[row_id]}
        df = pd.DataFrame(data=data_array)
        data_frames.append(df)

    main_df = pd.concat(data_frames)
    main_df.set_index("id", inplace=True)
    print(f"--------------{table_name}--------------------")
    print(main_df)
    return main_df

@app.get('/sofia-api/workout')
async def handle_get_javascript_file():
    column_names = ["id", "exercises_id", "session_id", "week_day"]
    main_df = convert_sql_table_to_df(column_names,db,"Workout")
    return main_df.to_json()

@app.get('/sofia-api/exercise')
async def handle_get_javascript_file():
    column_names = ["id", "reps", "sets", "weight", "name"]
    main_df = convert_sql_table_to_df(column_names,db,"Exercise")
    return main_df.to_json()


@app.get('/sofia-api/fitness')
async def handle_get_javascript_file():
    column_names = ["id", "session_id", "maintanace_calories",
                    "muscle_mass", "body_fat", "weight"]
    main_df = convert_sql_table_to_df(column_names,db,"Fitness")
    return main_df.to_json()
