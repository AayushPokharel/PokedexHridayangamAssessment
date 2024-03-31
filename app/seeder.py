import httpx


async def execute_query():
    """
    Executes a GraphQL query to retrieve Pokemon data from the PokeAPI.

    Returns:
        A list of Pokemon data, where each item contains the Pokemon's ID, name, types, and sprite.
    """
    graphql_query = """
    query MyQuery {
      pokemon_v2_pokemon(order_by: {id: asc}) {
        id
        name
        pokemon_v2_pokemontypes {
          slot
          pokemon_v2_type {
            name
            id
          }
        }
        pokemon_v2_pokemonsprites {
          sprites(path: "front_default")
        }
      }
    }
    """

    graphql_endpoint = "https://beta.pokeapi.co/graphql/v1beta"
    async with httpx.AsyncClient(timeout=50) as client:  # Increase timeout here
        response = await client.post(graphql_endpoint, json={"query": graphql_query})
        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("pokemon_v2_pokemon", [])
        else:
            print(f"Error: {response.status_code}")
            return []


async def fetch_pokemon_data():
    """
    Fetches Pokemon data from an external source.

    This function retrieves Pokemon data by executing a query and processing the response.
    It retries the query up to 3 times in case of a connection timeout.

    Returns:
      A list of dictionaries, where each dictionary represents a Pokemon and contains the following keys:
      - 'pokeID': The ID of the Pokemon.
      - 'pokeName': The name of the Pokemon.
      - 'Type': A list of types associated with the Pokemon.
      - 'sprite': The URL of the Pokemon's sprite image.

      If the data cannot be fetched after multiple attempts, an empty list is returned.
    """
    for attempt in range(3):  # Retry 3 times
        try:
            data = await execute_query()
            pokemon_list = []
            for pokemon in data:
                poke_id = pokemon.get("id")
                poke_name = pokemon.get("name")
                pokemon_types_dt = pokemon.get("pokemon_v2_pokemontypes", [])
                types = [ptype["pokemon_v2_type"]["name"] for ptype in pokemon_types_dt]
                sprites = pokemon.get("pokemon_v2_pokemonsprites", [])
                if sprites[0]["sprites"] == None:
                    sprite_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"
                else:
                    sprite_url = sprites[0]["sprites"]
                pokemon_list.append(
                    {
                        "pokeID": poke_id,
                        "pokeName": poke_name,
                        "Type": types,
                        "sprite": sprite_url,
                    }
                )
            return pokemon_list
        except httpx.ConnectTimeout:
            print(f"Connection timed out. Retrying... Attempt {attempt+1}")
    print("Failed to fetch data after multiple attempts.")
    return []
