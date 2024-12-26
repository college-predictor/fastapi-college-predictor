from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

class MongoDB:
    """
    MongoDB client class for connecting to the database and managing collections.
    """
    def __init__(self):
        load_dotenv()
        username = os.getenv('MONGODB_NAME')
        password = os.getenv('MONGODB_PASS')
        mongo_uri = os.getenv('MONGO_URI')
        self.uri = mongo_uri.format(username=username, password=password)
        self.client = None
        self.database = None

    def connect(self, db_name: str):
        """
        Connects to the specified database using the MongoDB URI and ServerApi.
        """
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            self.database = self.client.get_database(db_name)
            self.client.admin.command('ping')  # Test the connection
            print(f"Connected to MongoDB database: {db_name}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    def get_collection(self, collection_name: str):
        """
        Returns a specific collection from the connected database.
        """
        if self.database is None:  # Explicitly check for None
            raise ConnectionError("Database connection not established.")
        return self.database.get_collection(collection_name)

