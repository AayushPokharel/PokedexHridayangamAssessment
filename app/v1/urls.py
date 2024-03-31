from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database import get_all_pokemons

router = APIRouter()
templates = Jinja2Templates(directory="templates")


pokemon_type_colors = {
    "normal": "#A8A878",
    "fire": "#F08030",
    "water": "#6890F0",
    "electric": "#F8D030",
    "grass": "#78C850",
    "ice": "#98D8D8",
    "fighting": "#C03028",
    "poison": "#A040A0",
    "ground": "#E0C068",
    "flying": "#A890F0",
    "psychic": "#F85888",
    "bug": "#A8B820",
    "rock": "#B8A038",
    "ghost": "#705898",
    "dragon": "#7038F8",
    "dark": "#705848",
    "steel": "#B8B8D0",
    "fairy": "#EE99AC",
}


@router.get("/pokemons", response_class=HTMLResponse)
async def index(request: Request):

    pokemons = await get_all_pokemons()

    return templates.TemplateResponse(
        "v1/index.html",
        {
            "request": request,
            "pokemons": pokemons,
            "pokemon_type_colors": pokemon_type_colors,
        },
    )
