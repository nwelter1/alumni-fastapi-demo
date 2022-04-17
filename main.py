from fastapi import FastAPI, Request
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name = 'static')
templates = Jinja2Templates(directory='templates')

@app.get('/')
def home():
    return {'message':'Hello World FastAPI!'}

# path parameter
@app.get('/{num}')
def add_two(num: int):
    return {'num': num+2}


# query parameters
@app.get('/items/')
def get_items(first: Optional[str] = None, detail: Optional[str] = None):
    fake_data = {
        'nate':{
            'phone': '555-5555',
            'address': '123 fake street',
            'occupation': 'Teacher',
            'languages': ['Python', 'JS', 'C++', 'TypeScript']
        },
        'brandon':{
            'phone': '555-5555',
            'address': '12345 Real Street',
            'occupation': 'Teacher',
            'languages': ['Python', 'JS', 'Java', 'TypeScript', 'Kotlin']
        }
    }
    # details = {'phone', 'address', 'occupation', 'languages'}
    # if detail not in details:
    #     return {'error':'that detail does not exist'}
    if first and detail:
        details = {'phone', 'address', 'occupation', 'languages'}
        if detail not in details:
            return {'error':'that detail does not exist'}
        return fake_data[first][detail]
    if first:
        return fake_data[first]
    if detail:
        return {'message':'Need a first name before getting detail!'}
    return {'everyone': fake_data}

@app.get('/items/{name}', response_class=HTMLResponse)
def read_info(request: Request, name: str):
    fake_data = {
            'nate':{
                'phone': '555-5555',
                'address': '123 fake street',
                'occupation': 'Teacher',
                'languages': ['Python', 'JS', 'C++', 'TypeScript', 'HTML']
            },
            'brandon':{
                'phone': '555-5555',
                'address': '12345 Real Street',
                'occupation': 'Teacher',
                'languages': ['Python', 'JS', 'Java', 'TypeScript', 'Kotlin']
            }
        }
    info = fake_data[name]
    print(info)
    return templates.TemplateResponse('index.html', {'request': request, 'name':name, 'info':info})