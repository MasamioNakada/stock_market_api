from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(
    prefix="/logs",
)

@router.get("/")
async def get_logs():
    '''Get logs'''

    #read a api.txt
    with open('api.txt', 'r') as f:
        txt = f.readlines()

    txt_10 = txt[:10]

    return PlainTextResponse("".join(txt_10), status_code=200)
