class JEEMainModel:
    def __init__(self, db_client):
        self.collection = db_client.get_collection("jee_main_answer_sheet_urls")
    
    def save_url(self, datetime_key, url) -> bool:
        """
        Save a URL to MongoDB with datetime as key.
        For the limited set of datetime keys, this method will create a document for each key
        where the value is a list of URLs that gets appended to when new URLs are added.
        If the URL already exists for the given datetime key, no update is performed.
        
        Args:
            datetime_key (str): The datetime key (format: 'Test Date - Test Time')
            url (str): The URL to save
            
        Returns:
            str: The URL that was passed in
        """
        # First check if the URL already exists for this datetime key
        existing_doc = self.collection.find_one({"datetime": datetime_key})
        
        # If document exists and URL is already in the list, just return the URL without updating
        if existing_doc and "urls" in existing_doc and url in existing_doc["urls"]:
            return False
            
        # Otherwise, update the document with the new URL
        # Use upsert=True to create the document if it doesn't exist
        # $addToSet ensures no duplicate URLs in the list
        result = self.collection.update_one(
            {"datetime": datetime_key},
            {"$addToSet": {"urls": url}},
            upsert=True
        )

        # Return the URL
        return True