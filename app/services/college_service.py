from app.models.college_model import CollegeModel

class CollegeService:
    def __init__(self, college_model: CollegeModel):
        self.college_model = college_model

    def fetch_iit_colleges(self, adv_gen_rank=None, adv_cat_rank=None, category="OPEN", margin=0.5, gender="Gender-Neutral", state="AI"):
        criteria = {"$or": []}
        categories_to_check = ["OPEN", category] if category != "OPEN" else ["OPEN"]
        genders_to_check = ["Gender-Neutral", gender] if gender != "Gender-Neutral" else ["Gender-Neutral"]
        states_to_check = ["AI", state] if state != "AI" else ["AI"]

        for cat in categories_to_check:
            for gen in genders_to_check:
                for st in states_to_check: # iterate over states as well
                    and_conditions = [
                        {"category": cat},
                        {"gender": gen},
                        {"state": st},
                        {"college": "IIT"}
                    ]

                    rank_conditions = []

                    if adv_gen_rank is not None:
                        rank_conditions.extend([
                            {"openingRank": {"$lte": adv_gen_rank + int(adv_gen_rank * margin)}},
                            {"closingRank": {"$gte": adv_gen_rank - int(adv_gen_rank * margin)}}
                        ])

                    if adv_cat_rank is not None:
                        rank_conditions.extend([
                            {"openingRank": {"$lte": adv_cat_rank + int(adv_cat_rank * margin)}},
                            {"closingRank": {"$gte": adv_cat_rank - int(adv_cat_rank * margin)}}
                        ])

                    if rank_conditions:
                        and_conditions.extend(rank_conditions)

                    criteria["$or"].append({"$and": and_conditions})

        return self.college_model.get_colleges(criteria) if criteria["$or"] else []
    
    def fetch_nit_colleges(self, mains_gen_rank=None, mains_cat_rank=None, category="OPEN", margin=0.5, gender="Gender-Neutral", state="AI"):
        criteria = {"$or": []}
        categories_to_check = ["OPEN", category] if category != "OPEN" else ["OPEN"]
        genders_to_check = ["Gender-Neutral", gender] if gender != "Gender-Neutral" else ["Gender-Neutral"]
        states_to_check = ["AI", state] if state != "AI" else ["AI"]

        for cat in categories_to_check:
            for gen in genders_to_check:
                for st in states_to_check: # iterate over states as well
                    and_conditions = [
                        {"category": cat},
                        {"gender": gen},
                        {"state": st},
                        {"college": "NIT"}
                    ]

                    rank_conditions = []

                    if mains_gen_rank is not None:
                        rank_conditions.extend([
                            {"openingRank": {"$lte": mains_gen_rank + int(mains_gen_rank * margin)}},
                            {"closingRank": {"$gte": mains_gen_rank - int(mains_gen_rank * margin)}}
                        ])

                    if mains_cat_rank is not None:
                        rank_conditions.extend([
                            {"openingRank": {"$lte": mains_cat_rank + int(mains_cat_rank * margin)}},
                            {"closingRank": {"$gte": mains_cat_rank - int(mains_cat_rank * margin)}}
                        ])

                    if rank_conditions:
                        and_conditions.extend(rank_conditions)

                    criteria["$or"].append({"$and": and_conditions})

        return self.college_model.get_colleges(criteria) if criteria["$or"] else []
    
    def fetch_iiit_colleges(self, mains_gen_rank=None, mains_cat_rank=None, category="OPEN", margin=0.5, gender="Gender-Neutral", state="AI"):
        criteria = {"$or": []}
        categories_to_check = ["OPEN", category] if category != "OPEN" else ["OPEN"]
        genders_to_check = ["Gender-Neutral", gender] if gender != "Gender-Neutral" else ["Gender-Neutral"]
        states_to_check = ["AI", state] if state != "AI" else ["AI"]

        for cat in categories_to_check:
            for gen in genders_to_check:
                for st in states_to_check: # iterate over states as well
                    and_conditions = [
                        {"category": cat},
                        {"gender": gen},
                        {"state": st},
                        {"college": "IIIT"}
                    ]

                    rank_conditions = []

                    if mains_gen_rank is not None:
                        rank_conditions.extend([
                            {"openingRank": {"$lte": mains_gen_rank + int(mains_gen_rank * margin)}},
                            {"closingRank": {"$gte": mains_gen_rank - int(mains_gen_rank * margin)}}
                        ])

                    if mains_cat_rank is not None:
                        rank_conditions.extend([
                            {"openingRank": {"$lte": mains_cat_rank + int(mains_cat_rank * margin)}},
                            {"closingRank": {"$gte": mains_cat_rank - int(mains_cat_rank * margin)}}
                        ])

                    if rank_conditions:
                        and_conditions.extend(rank_conditions)

                    criteria["$or"].append({"$and": and_conditions})

        return self.college_model.get_colleges(criteria) if criteria["$or"] else []
    
    def fetch_gfti_colleges(self, mains_gen_rank=None, mains_cat_rank=None, category="OPEN", margin=0.5, gender="Gender-Neutral", state="AI"):
        criteria = {"$or": []}
        categories_to_check = ["OPEN", category] if category != "OPEN" else ["OPEN"]
        genders_to_check = ["Gender-Neutral", gender] if gender != "Gender-Neutral" else ["Gender-Neutral"]
        states_to_check = ["AI", state] if state != "AI" else ["AI"]

        for cat in categories_to_check:
            for gen in genders_to_check:
                for st in states_to_check: # iterate over states as well
                    and_conditions = [
                        {"category": cat},
                        {"gender": gen},
                        {"state": st},
                        {"college": "GFTI"}
                    ]

                    rank_conditions = []

                    if mains_gen_rank is not None:
                        rank_conditions.extend([
                            {"openingRank": {"$lte": mains_gen_rank + int(mains_gen_rank * margin)}},
                            {"closingRank": {"$gte": mains_gen_rank - int(mains_gen_rank * margin)}}
                        ])

                    if mains_cat_rank is not None:
                        rank_conditions.extend([
                            {"openingRank": {"$lte": mains_cat_rank + int(mains_cat_rank * margin)}},
                            {"closingRank": {"$gte": mains_cat_rank - int(mains_cat_rank * margin)}}
                        ])

                    if rank_conditions:
                        and_conditions.extend(rank_conditions)

                    criteria["$or"].append({"$and": and_conditions})

        return self.college_model.get_colleges(criteria) if criteria["$or"] else []