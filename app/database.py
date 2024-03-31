from decouple import config
import asyncpg

from models import parse_pokemon_data

pool = None


async def get_db_connection():
    """
    Establishes a connection to the database pool.

    Returns:
        asyncpg.pool.Pool: The database connection pool.
    """
    global pool
    pool = await asyncpg.create_pool(
        user=config("POSTGRES_USER"),
        password=config("POSTGRES_PASSWORD"),
        database=config("POSTGRES_DB"),
        host=config("POSTGRES_HOST"),
    )


async def load_db_with_pokemons():
    """
    Loads the database with Pokemon data.

    This function parses Pokemon data, checks if the 'pokemon' table exists in the database,
    creates the table if it doesn't exist, truncates the table to remove existing records,
    and inserts new Pokemon data into the table.

    Returns:
        None
    """
    seed_data = await parse_pokemon_data()

    async with pool.acquire() as conn:
        try:
            # Check if the table exists
            table_exists = await conn.fetchval(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = $1)",
                "pokemon",
            )

            if not table_exists:
                # If the table doesn't exist, create it
                await conn.execute(
                    "CREATE TABLE pokemon (id INT PRIMARY KEY, name TEXT, type TEXT[], sprite TEXT)"
                )
            else:
                # If the table exists, truncate it to remove existing records
                await conn.execute("TRUNCATE TABLE pokemon")

            for pokemon in seed_data:
                existing_pokemon = await conn.fetchrow(
                    "SELECT id FROM pokemon WHERE id = $1", pokemon.id
                )

                if existing_pokemon:
                    # If the Pokemon already exists, skip it.
                    continue

                await conn.execute(
                    "INSERT INTO pokemon (id, name, type, sprite) VALUES ($1, $2, $3, $4)",
                    pokemon.id,
                    pokemon.name,
                    pokemon.type,
                    pokemon.sprite,
                )
        finally:
            await pool.release(conn)


async def get_all_pokemons():
    """
    Retrieve all pokemons from the database.

    Returns:
        List: A list of dictionaries representing the pokemons.
    """
    async with pool.acquire() as conn:
        pokemons = await conn.fetch("SELECT * FROM pokemon")
        return pokemons
