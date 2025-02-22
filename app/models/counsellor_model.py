from app.config.database import MongoDB
from typing import Dict, Any

class CounsellorModel:
    def __init__(self, db_client: MongoDB):
        self.counsellor_collection = db_client.get_collection("counsellor")
        self.research_collection = db_client.get_collection("research")

    def save_counsellor_interaction(self, interaction: Dict[str, Any]) -> None:
        self.counsellor_collection.insert_one(interaction)

    def save_research(self, research: Dict[str, Any]) -> None:
        self.research_collection.insert_one(research)

    def get_research(self, research_id: str) -> Dict[str, Any]:
        return self.research_collection.find_one({"research_id": research_id}, {"_id": 0})