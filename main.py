import json
from enum import Enum
from fastapi import FastAPI,HTTPException
from fastapi.responses import RedirectResponse

# Create app instance 
app = FastAPI(
    title="SongAPI"
)

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