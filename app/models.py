from pydantic import BaseModel
from typing import List

from seeder import fetch_pokemon_data


class Pokemon(BaseModel):
    """
    Represents a Pokemon.

    Attributes:
        id (int): The ID of the Pokemon.
        name (str): The name of the Pokemon.
        type (List[str]): The types of the Pokemon.
        sprite (str): The sprite URL of the Pokemon.
    """

    id: int
    name: str
    type: List[str]
    sprite: str


async def parse_pokemon_data():
    """
    Parses the fetched Pokemon data and returns a list of Pokemon objects.

    Returns:
        list: A list of Pokemon objects.
    """
    pokemon_data = await fetch_pokemon_data()
    return [
        Pokemon(
            id=pokemon["pokeID"],
            name=pokemon["pokeName"],
            type=pokemon["Type"],
            sprite=pokemon["sprite"],
        )
        for pokemon in pokemon_data
    ]
