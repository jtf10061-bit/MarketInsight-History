import os
from pathlib import Path
from dotenv import load_dotenv
from azure.cosmos import CosmosClient

load_dotenv(Path(__file__).parent.parent.parent / ".env")

client = CosmosClient(
    os.getenv("COSMOS_ENDPOINT"),
    os.getenv("COSMOS_KEY")
)

database = client.get_database_client(os.getenv("COSMOS_DATABASE"))
container = database.get_container_client(os.getenv("COSMOS_CONTAINER"))