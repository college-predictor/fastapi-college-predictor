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
        self.db_name = os.getenv('DB_NAME_PROD')
        mongo_uri = os.getenv('MONGO_URI')
        self.uri = mongo_uri.format(username=username, password=password, db_name=self.db_name)
        self.client = None
        self.database = None

    def connect(self):
        """
        Connects to the specified database using the MongoDB URI and ServerApi.
        """
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            self.database = self.client.get_database(self.db_name)
            self.client.admin.command('ping')  # Test the connection
            print(f"Connected to MongoDB database: {self.db_name}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    def get_collection(self, collection_name: str):
        """
        Returns a specific collection from the connected database.
        """
        if self.database is None:  # Explicitly check for None
            raise ConnectionError("Database connection not established.")
        print("connecting to:", collection_name)
        return self.database.get_collection(collection_name)

