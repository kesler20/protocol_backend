


class JsonDatabaseInterface(object):        
    '''Interface which allows to store dictionaries as json'''
        
    def __init__(self, filename: str) -> None:
        self.filename = filename
    
    def createResource(self) -> None:
        '''signature description'''
        pass
    
    def readResource(self) -> dict:
        '''signature description'''
        pass
    
    def deleteResource(self) -> None:
        '''signature description'''
        pass
    
    def updateResource(self) -> None:
        '''signature description'''
        pass


'''

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



'''