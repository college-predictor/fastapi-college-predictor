from app.models.college_model import CollegeModel

class CollegeService:
    def __init__(self, college_model: CollegeModel):
        self.college_model = college_model

    def fetch_iit_colleges(self, adv_gen_rank=None, adv_cat_rank=None, category=None, margin=None, gender=None, state=None, year=None):
        if not (adv_gen_rank or adv_cat_rank):
            return []

        colleges = self.college_model.get_colleges({"collegeType": "IIT"}, year)
        # print(colleges)
        filtered_colleges = []
        for college in colleges:
            opening_rank = college.get("openingRank")
            closing_rank = college.get("closingRank")
            required_gender = college.get("gender")
            required_category = college.get("category")
            required_state = college.get("state")
            required_quota = college.get("quota")

            # Adjust ranks with margin
            adjusted_opening_rank = int(opening_rank * (1 - margin))
            adjusted_closing_rank = int(closing_rank * (1 + margin))
            
            if adv_gen_rank and required_category=="OPEN":
                if required_gender=="Gender-Neutral" or required_gender==gender:
                    if required_quota=="AI" or required_state==state:
                        if adjusted_opening_rank< adv_gen_rank <adjusted_closing_rank:
                            filtered_colleges.append(college)
            
            if adv_cat_rank and required_category==category:
                if required_gender=="Gender-Neutral" or required_gender==gender:
                    if required_quota=="AI" or required_state==state:
                        if adjusted_opening_rank< adv_cat_rank <adjusted_closing_rank:
                            filtered_colleges.append(college)
        return filtered_colleges
    
    def fetch_mains_colleges(self, mains_gen_rank=None, mains_cat_rank=None, category=None, margin=None, gender=None, state=None, year=None):
        if not (mains_gen_rank or mains_cat_rank):
            print("mains_gen_rank", mains_gen_rank, "mains_cat_rank", mains_cat_rank)
            return [[], [], []]

        colleges = self.college_model.get_colleges({"collegeType": { "$ne": "IIT" }}, year)
        # print(colleges)
        filtered_nit_colleges = []
        filtered_iiit_colleges = []
        filtered_gfti_colleges = []
        # print(mains_cat_rank)
        for college in colleges:
            # print("College type: ", college["collegeType"])
            opening_rank = college.get("openingRank")
            closing_rank = college.get("closingRank")
            required_gender = college.get("gender")
            required_category = college.get("category")
            required_state = college.get("state")
            required_quota = college.get("quota")
            college_type = college.get("collegeType")

            # Adjust ranks with margin
            adjusted_opening_rank = int(opening_rank * (1 - margin))
            adjusted_closing_rank = int(closing_rank * (1 + margin))
            
            if mains_gen_rank and required_category=="OPEN":
                if required_gender=="Gender-Neutral" or required_gender==gender:
                    if required_quota=="OS" or required_state==state:
                        if adjusted_opening_rank< mains_gen_rank <adjusted_closing_rank:
                            if college_type == "NIT":
                                # print("NIT College: ", college)
                                filtered_nit_colleges.append(college)
                            elif college_type == "IIIT":
                                filtered_iiit_colleges.append(college)
                            elif college_type == "GFTI":
                                filtered_gfti_colleges.append(college)
            
            if mains_cat_rank and required_category==category:
                if required_gender=="Gender-Neutral" or required_gender==gender:
                    if required_quota=="OS" or required_state==state:
                        if adjusted_opening_rank< mains_cat_rank <adjusted_closing_rank:
                            filtered_nit_colleges.append(college)
        return [filtered_nit_colleges, filtered_iiit_colleges, filtered_gfti_colleges]