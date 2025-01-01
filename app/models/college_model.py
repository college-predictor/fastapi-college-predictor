from app.config.database import MongoDB

class CollegeModel:
    def __init__(self, db_client: MongoDB):
        self.collection2024 = db_client.get_collection("collegesList2024")
        self.collection2023 = db_client.get_collection("collegesList2023")
        self.collection2022 = db_client.get_collection("collegesList2022")
        self.collection2021 = db_client.get_collection("collegesList2021")
        self.collection2020 = db_client.get_collection("collegesList2020")
        self.collection2019 = db_client.get_collection("collegesList2019")
        self.collection2018 = db_client.get_collection("collegesList2018")
        self.collection2017 = db_client.get_collection("collegesList2017")
        self.collection2016 = db_client.get_collection("collegesList2016")

    def get_colleges(self, criteria: dict, year):
        if year==2024:
            return list(self.collection2024.find(criteria, {"_id": 0}))
        if year==2023:
            return list(self.collection2023.find(criteria, {"_id": 0}))
        if year==2022:
            return list(self.collection2022.find(criteria, {"_id": 0}))
        if year==2021:
            return list(self.collection2021.find(criteria, {"_id": 0}))
        if year==2020:
            return list(self.collection2020.find(criteria, {"_id": 0}))
        if year==2019:
            return list(self.collection2019.find(criteria, {"_id": 0}))
        if year==2018:
            return list(self.collection2018.find(criteria, {"_id": 0}))
        if year==2017:
            return list(self.collection2017.find(criteria, {"_id": 0}))
        if year==2016:
            return list(self.collection2016.find(criteria, {"_id": 0}))
