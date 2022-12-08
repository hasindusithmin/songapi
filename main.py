import json
from enum import Enum
from fastapi import FastAPI
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

