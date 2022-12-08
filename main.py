
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


