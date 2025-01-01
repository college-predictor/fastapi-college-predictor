# sample_data.py

sample_colleges = [
    # IIT Colleges
    {
        "id": 1,
        "courseName": "Computer Science",
        "courseType": "B.Tech",
        "collegeType": "IIT",
        "collegeName": "Indian Institute of Technology Delhi",
        "instituteCode": 101,
        "state": "Delhi",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 5,
        "closingRank": 250,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "12 LPA",
        "nirfRanking": 3,
        "placementRating": 4.5,
        "collegeLifeRating": 4.2,
        "campusRating": 4.7,
        "aiSummary": "IIT Delhi is renowned for its excellent academic environment and robust placement opportunities, offering state-of-the-art facilities and a vibrant campus life.",
        "contactInfo": {
            "phone": "+91-11-12345678",
            "email": "admissions@iitd.ac.in",
            "address": "Hauz Khas, New Delhi, Delhi 110016"
        }
    },
    {
        "id": 2,
        "courseName": "Electrical Engineering",
        "courseType": "B.Tech",
        "collegeType": "IIT",
        "collegeName": "Indian Institute of Technology Bombay",
        "instituteCode": 102,
        "state": "Maharashtra",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 10,
        "closingRank": 300,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "14 LPA",
        "nirfRanking": 2,
        "placementRating": 4.7,
        "collegeLifeRating": 4.3,
        "campusRating": 4.8,
        "aiSummary": "IIT Bombay offers a dynamic learning environment with cutting-edge research facilities and a strong emphasis on innovation and entrepreneurship.",
        "contactInfo": {
            "phone": "+91-22-87654321",
            "email": "admissions@iitb.ac.in",
            "address": "Powai, Mumbai, Maharashtra 400076"
        }
    },
    {
        "id": 3,
        "courseName": "Mechanical Engineering",
        "courseType": "B.Tech",
        "collegeType": "IIT",
        "collegeName": "Indian Institute of Technology Kanpur",
        "instituteCode": 103,
        "state": "Uttar Pradesh",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 15,
        "closingRank": 350,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "13 LPA",
        "nirfRanking": 4,
        "placementRating": 4.4,
        "collegeLifeRating": 4.1,
        "campusRating": 4.6,
        "aiSummary": "IIT Kanpur is celebrated for its rigorous academic programs and extensive research opportunities, fostering a culture of excellence and innovation.",
        "contactInfo": {
            "phone": "+91-512-2345678",
            "email": "admissions@iitk.ac.in",
            "address": "IIT Kanpur, Uttar Pradesh 208016"
        }
    },
    {
        "id": 4,
        "courseName": "Civil Engineering",
        "courseType": "B.Tech",
        "collegeType": "IIT",
        "collegeName": "Indian Institute of Technology Madras",
        "instituteCode": 104,
        "state": "Tamil Nadu",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 20,
        "closingRank": 400,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "11 LPA",
        "nirfRanking": 5,
        "placementRating": 4.3,
        "collegeLifeRating": 4.0,
        "campusRating": 4.5,
        "aiSummary": "IIT Madras provides a vibrant campus life with excellent infrastructure and a strong focus on research and development in various engineering disciplines.",
        "contactInfo": {
            "phone": "+91-44-12345678",
            "email": "admissions@iitm.ac.in",
            "address": "Chennai, Tamil Nadu 600036"
        }
    },
    {
        "id": 5,
        "courseName": "Chemical Engineering",
        "courseType": "B.Tech",
        "collegeType": "IIT",
        "collegeName": "Indian Institute of Technology Kharagpur",
        "instituteCode": 105,
        "state": "West Bengal",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 25,
        "closingRank": 450,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "10 LPA",
        "nirfRanking": 6,
        "placementRating": 4.2,
        "collegeLifeRating": 3.9,
        "campusRating": 4.4,
        "aiSummary": "IIT Kharagpur is known for its sprawling campus and diverse academic programs, providing students with ample opportunities for research and professional growth.",
        "contactInfo": {
            "phone": "+91-322-2345678",
            "email": "admissions@iitkgp.ac.in",
            "address": "Kharagpur, West Bengal 721302"
        }
    },

    # NIT Colleges
    {
        "id": 6,
        "courseName": "Computer Science",
        "courseType": "B.Tech",
        "collegeType": "NIT",
        "collegeName": "National Institute of Technology Tiruchirappalli",
        "instituteCode": 201,
        "state": "Tamil Nadu",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 300,
        "closingRank": 1200,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "8 LPA",
        "nirfRanking": 15,
        "placementRating": 4.0,
        "collegeLifeRating": 3.8,
        "campusRating": 4.1,
        "aiSummary": "NIT Trichy offers a balanced academic curriculum with strong industry connections, ensuring good placement opportunities and a supportive campus environment.",
        "contactInfo": {
            "phone": "+91-431-2345678",
            "email": "admissions@nitt.edu",
            "address": "National Institute of Technology, Tiruchirappalli, Tamil Nadu 620015"
        }
    },
    {
        "id": 7,
        "courseName": "Electrical Engineering",
        "courseType": "B.Tech",
        "collegeType": "NIT",
        "collegeName": "National Institute of Technology Karnataka",
        "instituteCode": 202,
        "state": "Karnataka",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 350,
        "closingRank": 1300,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "7.5 LPA",
        "nirfRanking": 18,
        "placementRating": 3.9,
        "collegeLifeRating": 3.7,
        "campusRating": 4.0,
        "aiSummary": "NIT Karnataka provides comprehensive engineering education with a focus on practical skills and industry readiness, fostering a collaborative campus culture.",
        "contactInfo": {
            "phone": "+91-80-23456789",
            "email": "admissions@nita.ac.in",
            "address": "National Institute of Technology, Surathkal, Karnataka 575025"
        }
    },
    {
        "id": 8,
        "courseName": "Mechanical Engineering",
        "courseType": "B.Tech",
        "collegeType": "NIT",
        "collegeName": "National Institute of Technology Warangal",
        "instituteCode": 203,
        "state": "Telangana",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 400,
        "closingRank": 1400,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "7 LPA",
        "nirfRanking": 20,
        "placementRating": 3.8,
        "collegeLifeRating": 3.6,
        "campusRating": 3.9,
        "aiSummary": "NIT Warangal is distinguished by its strong engineering programs and vibrant student life, offering numerous opportunities for personal and professional development.",
        "contactInfo": {
            "phone": "+91-870-2345678",
            "email": "admissions@nitrw.ac.in",
            "address": "National Institute of Technology, Warangal, Telangana 506004"
        }
    },
    {
        "id": 9,
        "courseName": "Civil Engineering",
        "courseType": "B.Tech",
        "collegeType": "NIT",
        "collegeName": "National Institute of Technology Rourkela",
        "instituteCode": 204,
        "state": "Odisha",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 450,
        "closingRank": 1500,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "6.5 LPA",
        "nirfRanking": 22,
        "placementRating": 3.7,
        "collegeLifeRating": 3.5,
        "campusRating": 3.8,
        "aiSummary": "NIT Rourkela offers a supportive academic environment with a focus on research and innovation, preparing students for successful careers in engineering.",
        "contactInfo": {
            "phone": "+91-661-2345678",
            "email": "admissions@nitrkl.ac.in",
            "address": "National Institute of Technology, Rourkela, Odisha 769008"
        }
    },
    {
        "id": 10,
        "courseName": "Chemical Engineering",
        "courseType": "B.Tech",
        "collegeType": "NIT",
        "collegeName": "National Institute of Technology Calicut",
        "instituteCode": 205,
        "state": "Kerala",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 500,
        "closingRank": 1600,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "6 LPA",
        "nirfRanking": 25,
        "placementRating": 3.6,
        "collegeLifeRating": 3.4,
        "campusRating": 3.7,
        "aiSummary": "NIT Calicut is known for its excellent academic standards and vibrant campus life, providing students with ample opportunities for growth and development.",
        "contactInfo": {
            "phone": "+91-498-2345678",
            "email": "admissions@nitsc.ac.in",
            "address": "National Institute of Technology, Calicut, Kerala 673601"
        }
    },

    # IIIT Colleges
    {
        "id":11,
        "courseName": "Computer Science",
        "courseType": "B.Tech",
        "collegeType": "IIIT",
        "collegeName": "International Institute of Information Technology Hyderabad",
        "instituteCode": 301,
        "state": "Telangana",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 600,
        "closingRank": 2000,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "9 LPA",
        "nirfRanking": 30,
        "placementRating": 4.1,
        "collegeLifeRating": 3.9,
        "campusRating": 4.2,
        "aiSummary": "IIIT Hyderabad specializes in information technology and engineering, offering cutting-edge research opportunities and strong industry partnerships.",
        "contactInfo": {
            "phone": "+91-40-23456789",
            "email": "admissions@iiit.ac.in",
            "address": "IIIT Hyderabad, Gachibowli, Hyderabad, Telangana 500032"
        }
    },
    {
        "id":12,
        "courseName": "Electronics and Communication",
        "courseType": "B.Tech",
        "collegeType": "IIIT",
        "collegeName": "International Institute of Information Technology Bangalore",
        "instituteCode": 302,
        "state": "Karnataka",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 650,
        "closingRank": 2100,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "8.5 LPA",
        "nirfRanking": 32,
        "placementRating": 4.0,
        "collegeLifeRating": 3.8,
        "campusRating": 4.1,
        "aiSummary": "IIIT Bangalore focuses on advanced studies in information technology and electronics, providing students with state-of-the-art facilities and research opportunities.",
        "contactInfo": {
            "phone": "+91-80-23456789",
            "email": "admissions@iiitb.ac.in",
            "address": "IIIT Bangalore, Electronic City, Bangalore, Karnataka 560100"
        }
    },
    {
        "id":13,
        "courseName": "Information Technology",
        "courseType": "B.Tech",
        "collegeType": "IIIT",
        "collegeName": "International Institute of Information Technology Delhi",
        "instituteCode": 303,
        "state": "Delhi",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 700,
        "closingRank": 2200,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "8 LPA",
        "nirfRanking": 35,
        "placementRating": 3.9,
        "collegeLifeRating": 3.7,
        "campusRating": 4.0,
        "aiSummary": "IIIT Delhi offers a vibrant academic atmosphere with a strong emphasis on research and innovation in information technology and related fields.",
        "contactInfo": {
            "phone": "+91-11-23456789",
            "email": "admissions@iiitd.ac.in",
            "address": "IIIT Delhi, Okhla, New Delhi, Delhi 110025"
        }
    },
    {
        "id":14,
        "courseName": "Software Engineering",
        "courseType": "B.Tech",
        "collegeType": "IIIT",
        "collegeName": "International Institute of Information Technology Pune",
        "instituteCode": 304,
        "state": "Maharashtra",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 750,
        "closingRank": 2300,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "7.5 LPA",
        "nirfRanking": 38,
        "placementRating": 3.8,
        "collegeLifeRating": 3.6,
        "campusRating": 3.9,
        "aiSummary": "IIIT Pune provides comprehensive education in software engineering with a focus on practical skills, research, and industry collaboration.",
        "contactInfo": {
            "phone": "+91-20-23456789",
            "email": "admissions@iiitp.ac.in",
            "address": "IIIT Pune, Aundh, Pune, Maharashtra 411007"
        }
    },
    {
        "id":15,
        "courseName": "Data Science",
        "courseType": "B.Tech",
        "collegeType": "IIIT",
        "collegeName": "International Institute of Information Technology Bangalore",
        "instituteCode": 302,
        "state": "Karnataka",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 800,
        "closingRank": 2400,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "7 LPA",
        "nirfRanking": 40,
        "placementRating": 3.7,
        "collegeLifeRating": 3.5,
        "campusRating": 3.8,
        "aiSummary": "IIIT Bangalore offers specialized programs in data science, equipping students with the necessary skills to excel in the rapidly evolving tech industry.",
        "contactInfo": {
            "phone": "+91-80-23456789",
            "email": "admissions@iiitb.ac.in",
            "address": "IIIT Bangalore, Electronic City, Bangalore, Karnataka 560100"
        }
    },

    # GFTI Colleges
    {
        "id":16,
        "courseName": "Computer Engineering",
        "courseType": "B.Tech",
        "collegeType": "GFTI",
        "collegeName": "Government Funded Technical Institute Mumbai",
        "instituteCode": 401,
        "state": "Maharashtra",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 900,
        "closingRank": 2500,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "6.5 LPA",
        "nirfRanking": 50,
        "placementRating": 3.5,
        "collegeLifeRating": 3.3,
        "campusRating": 3.6,
        "aiSummary": "GFIT Mumbai provides quality technical education with a focus on practical learning and industry readiness, ensuring students are well-prepared for their careers.",
        "contactInfo": {
            "phone": "+91-22-34567890",
            "email": "admissions@gfti-mumbai.ac.in",
            "address": "GFTI Mumbai, Andheri, Mumbai, Maharashtra 400058"
        }
    },
    {
        "id":17,
        "courseName": "Electrical Engineering",
        "courseType": "B.Tech",
        "collegeType": "GFTI",
        "collegeName": "Government Funded Technical Institute Delhi",
        "instituteCode": 402,
        "state": "Delhi",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 950,
        "closingRank": 2600,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "6 LPA",
        "nirfRanking": 52,
        "placementRating": 3.4,
        "collegeLifeRating": 3.2,
        "campusRating": 3.5,
        "aiSummary": "GFIT Delhi offers robust engineering programs with a strong emphasis on foundational knowledge and practical applications, preparing students for diverse career paths.",
        "contactInfo": {
            "phone": "+91-11-34567890",
            "email": "admissions@gfti-delhi.ac.in",
            "address": "GFTI Delhi, Rohini, Delhi 110085"
        }
    },
    {
        "id":18,
        "courseName": "Mechanical Engineering",
        "courseType": "B.Tech",
        "collegeType": "GFTI",
        "collegeName": "Government Funded Technical Institute Chennai",
        "instituteCode": 403,
        "state": "Tamil Nadu",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 1000,
        "closingRank": 2700,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "5.5 LPA",
        "nirfRanking": 55,
        "placementRating": 3.3,
        "collegeLifeRating": 3.1,
        "campusRating": 3.4,
        "aiSummary": "GFIT Chennai focuses on delivering comprehensive mechanical engineering education with ample opportunities for hands-on learning and industry exposure.",
        "contactInfo": {
            "phone": "+91-44-34567890",
            "email": "admissions@gfti-chennai.ac.in",
            "address": "GFTI Chennai, Tambaram, Chennai, Tamil Nadu 600045"
        }
    },
    {
        "id":19,
        "courseName": "Civil Engineering",
        "courseType": "B.Tech",
        "collegeType": "GFTI",
        "collegeName": "Government Funded Technical Institute Kolkata",
        "instituteCode": 404,
        "state": "West Bengal",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 1050,
        "closingRank": 2800,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "5 LPA",
        "nirfRanking": 58,
        "placementRating": 3.2,
        "collegeLifeRating": 3.0,
        "campusRating": 3.3,
        "aiSummary": "GFIT Kolkata offers solid civil engineering programs with a focus on sustainable development and infrastructure planning, preparing students for real-world challenges.",
        "contactInfo": {
            "phone": "+91-33-34567890",
            "email": "admissions@gfti-kolkata.ac.in",
            "address": "GFTI Kolkata, Salt Lake, Kolkata, West Bengal 700091"
        }
    },
    {
        "id":20,
        "courseName": "Chemical Engineering",
        "courseType": "B.Tech",
        "collegeType": "GFTI",
        "collegeName": "Government Funded Technical Institute Pune",
        "instituteCode": 405,
        "state": "Maharashtra",
        "gender": "Gender-Neutral",
        "quota": "AI",
        "category": "OPEN",
        "openingRank": 1100,
        "closingRank": 2900,
        "profileImage": "https://placehold.co/300x300",
        "avgPkg": "4.5 LPA",
        "nirfRanking": 60,
        "placementRating": 3.1,
        "collegeLifeRating": 2.9,
        "campusRating": 3.2,
        "aiSummary": "GFIT Pune provides a strong foundation in chemical engineering with an emphasis on practical skills and industry-oriented training, ensuring graduates are workforce-ready.",
        "contactInfo": {
            "phone": "+91-20-34567890",
            "email": "admissions@gfti-pune.ac.in",
            "address": "GFTI Pune, Hinjewadi, Pune, Maharashtra 411057"
        }
    }
]









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
        self.uri = mongo_uri.format(username=username, password=password, db_name="college-predictor-dev")
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
        if self.database is None:
            raise ConnectionError("Database connection not established.")
        return self.database.get_collection(collection_name)

    def drop_collection(self, collection_name: str):
        """
        Drops the specified collection from the database.
        """
        if self.database is None:
            raise ConnectionError("Database connection not established.")
        self.database.drop_collection(collection_name)
        print(f"Dropped collection: {collection_name}")

    def insert_sample_data(self, collection_name: str, data: list):
        """
        Inserts sample data into the specified collection.
        """
        collection = self.get_collection(collection_name)
        collection.insert_many(data)
        print(f"Inserted {len(data)} documents into the collection '{collection_name}'.")


if __name__ == "__main__":
    db_client = MongoDB()
    db_name = "college-predictor-dev"
    collection_to_drop = "collegesList"
    collection_to_create = "collegesList"

    try:
        db_client.connect(db_name)
        db_client.drop_collection(collection_to_drop)
        db_client.insert_sample_data(collection_to_create, sample_colleges)
    except Exception as e:
        print(f"An error occurred: {e}")





criteria = {'$or': [{'$and': [{'category': 'OPEN'}, {'gender': 'Gender-Neutral'}, {'collegeType': 'IIT'}, {'openingRank': {'$lte': 550}}, {'closingRank': {'$gte': 450}}, {'$or': [{'quota': 'AI'}, {'state': 'Maharashtra'}]}]}]}
