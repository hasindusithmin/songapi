import re
import json
from enum import Enum
from fastapi import FastAPI,HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


description = '''
![music](https://songapi.deta.dev/static/music.gif)

Using this **API**, you can download almost **1,350 songs**.

Also, it can be used for your **PET projects**.(You can create a mobile/web application to download songs.)
'''

# Create app instance 
app = FastAPI(
    title="SongAPI",
    description=description,
    license_info={
        'name':'Contribute to SongAPI',
        'url':'https://github.com/hasindusithmin/songapi'
    },
    contact={
        "name": "Hasindu Sithmin",
        "url": "https://hasindusithmin.github.io/",
        "email": "hasindusithmin64@gmail.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# ROOT 
@app.get('/')
def redirect_to_doc():
    # should be redirect to api documention
    return RedirectResponse('/docs')

class Keys(Enum):
    SONG = 'song'
    SINGER = 'singer'

# route:/find-all 
@app.get('/find-all')
async def find_all(sort:Keys=Keys.SONG,reverse:bool=False):
    with open('resource.json','r') as fp:
        resource =  json.load(fp)
        return sorted(resource,key=lambda k:k[sort.value],reverse=reverse)

# route: /singers 
@app.get('/find-singers')
async def find_singers():
    with open('resource.json','r') as fp:
        resource =  json.load(fp)
        return sorted(set([r['singer'] for r in resource]))

# route: /find-songsby-singer 
@app.get('/find-songsby-singer/{singer}')
async def find_songsby_singer(singer:str):
    with open('resource.json','r') as fp:
        resource =  json.load(fp)
        return list(
            filter(
                lambda obj:obj['singer'].lower() == singer.lower(),
                resource
            )
        )
            
        

# define alphabet List 
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# route: /find-songsby-letter 
@app.get('/find-songsby-letter/{char}')
async def find_song_by_letter(char:str):
    # check if the string contains only letters (a-zA-Z).
    if char not in alphabet:
        raise HTTPException(status_code=400,detail='string should contain only alphabets')
    # if the string contains only letters (a-zA-Z).
    with open('resource.json','r') as fp:
        resource =  json.load(fp)
        return list(
            filter(
                lambda obj:obj['song'].startswith(char.upper()),
                resource
            )
        )

# route: /find-singersby-letter 
@app.get('/find-singersby-letter/{char}')
async def find_singers_by_letter(char:str):
    # check if the string contains only letters (a-zA-Z).
    if char not in alphabet:
        raise HTTPException(status_code=400,detail='string should contain only alphabets')
    # if the string contains only letters (a-zA-Z).
    with open('resource.json','r') as fp:
        resource =  json.load(fp)
        return list(
            filter(
                lambda obj:obj['singer'].startswith(char.upper()),
                resource
            )
        )
        
# route /search-song
@app.get('/search-song/{quotes}')
async def search_song(quotes:str):
    with open('resource.json','r') as fp:
        resource =  json.load(fp)
        result =  list(
            filter(
                lambda obj:re.search(f'^{quotes.capitalize()}',obj['song']),
                resource
            )
        )
        if len(result) == 0:
            raise HTTPException(status_code=404)
        return result

# route /search-song
@app.get('/search-singer/{quotes}')
async def search_singer(quotes:str):
    with open('resource.json','r') as fp:
        resource =  json.load(fp)
        result =  list(
            filter(
                lambda obj:re.search(f'^{quotes.capitalize()}',obj['singer']),
                resource
            )
        )
        if len(result) == 0:
            raise HTTPException(status_code=404)
        return result