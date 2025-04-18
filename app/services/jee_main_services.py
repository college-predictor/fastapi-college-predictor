from bs4 import BeautifulSoup
from fastapi import HTTPException
import requests
from app.models.jee_main_model import JEEMainModel
from app.config.database import MongoDB
from app.utils.jee_main_answers import JEE_MAIN_ANSWERS_FINAL
from urllib.parse import urljoin

# Connect to MongoDB
db_client = MongoDB()
db_client.connect()
jee_main_model = JEEMainModel(db_client)

# --- Extract Main Info Table ---
def extract_main_info(soup):
    info_table = soup.find("table", attrs={"border": "1"})
    info_rows = info_table.find_all("tr")
    
    main_info = {}
    for row in info_rows:
        cols = row.find_all("td")
        if len(cols) == 2:
            key = cols[0].get_text(strip=True)
            value = cols[1].get_text(strip=True)
            main_info[key] = value
    return main_info

# Function to handle Type 1 (MCQ questions)
def parse_type_A_question(soup, base_url):
    question_data = {}

    # Extract question number and image
    question_tag = soup.find('td', {'align': 'center', 'class': 'bold'})
    question_data['question_img_url'] = urljoin(base_url, question_tag.find_next('img')['src'])

    # Extract options (there are 4 options)
    options = []
    option_tags = soup.find_all('td', style="text-align: left;")
    for i, option_tag in enumerate(option_tags[0:4]):  # Skip the first one as it's the question image
        options.append(urljoin(base_url, option_tag.find('img')['src']))
    question_data["options_url"] = options

    # Extract metadata for the question
    question_data['question_type'] = soup.find('td', text="Question Type :").find_next('td').text.strip()
    question_data['question_id'] = soup.find('td', text="Question ID :").find_next('td').text.strip()
    question_data['status'] = soup.find('td', text="Status :").find_next('td').text.strip()
    question_data['chosen_option'] = soup.find('td', text="Chosen Option :").find_next('td').text.strip()

    # Extract Option IDs
    option_ids = {}
    option_ids['option_1_id'] = soup.find('td', text="Option 1 ID :").find_next('td').text.strip()
    option_ids['option_2_id'] = soup.find('td', text="Option 2 ID :").find_next('td').text.strip()
    option_ids['option_3_id'] = soup.find('td', text="Option 3 ID :").find_next('td').text.strip()
    option_ids['option_4_id'] = soup.find('td', text="Option 4 ID :").find_next('td').text.strip()

    question_data.update(option_ids)

    return question_data


# Function to handle Type 2 (Short Answer questions)
def parse_type_B_question(soup, base_url):
    question_data = {}

    # Extract question number and image
    question_tag = soup.find('td', {'align': 'center', 'class': 'bold'})
    question_data['question_img_url'] = urljoin(base_url, question_tag.find_next('img')['src'])

    # Extract metadata for the question
    question_data['question_type'] = soup.find('td', text="Question Type :").find_next('td').text.strip()
    question_data['question_id'] = soup.find('td', text="Question ID :").find_next('td').text.strip()
    question_data['status'] = soup.find('td', text="Status :").find_next('td').text.strip()

    # Check if "Given Answer" exists and add it to the data
    given_answer_tag = soup.find('td', text="Given Answer :")
    if given_answer_tag:
        question_data['given_answer'] = given_answer_tag.find_next('td').text.strip()

    return question_data

# Function to automatically identify question type
def identify_question_type(soup):
    # Check for presence of options section
    option_tags = soup.find_all('td', style="text-align: left;")
    
    if len(option_tags) >= 4:  # If we have at least 4 options, it's an MCQ
        return "MCQ"
    elif soup.find('td', text="Given Answer :"):  # If we have "Given Answer", it's an SA
        return "SA"
    else:
        return "Unknown"

def save_url_in_mongo(base_url):
    try:        
        # Fetch and parse the URL content
        response = requests.get(base_url)
        soup = BeautifulSoup(response.content, "html.parser")
        main_info = extract_main_info(soup)

        # Extract datetime information
        test_date = main_info.get("Test Date")
        test_time = main_info.get("Test Time")
        datetime_key = f"{test_date} - {test_time}"

        if not datetime_key:
            raise HTTPException(status_code=400, detail="Test Date or Test Time not found in the URL")
        
        # print(datetime_key)
        # Save URL to MongoDB
        is_url_present = jee_main_model.save_url(datetime_key, base_url)
        
        return {
            "status": "success",
            "message": "URL saved successfully",
            "datetime": datetime_key,
            "is_url_present": is_url_present
        }
    except Exception as e:
        print(f"Error: {e}")
        return HTTPException(status_code=400, detail=f"Error processing URL: {str(e)}")

def calculate_marks(base_url):
    # print(base_url)
    try:
        score_card = {
            "answered_questions": 0,
            "unanswered_questions": 0,
            "wrong_answers": 0,
            "physics_marks": 0,
            "chemistry_marks": 0,
            "maths_marks": 0,
            "total_marks": 0,
        }

        # Fetch and parse the URL content
        response = requests.get(base_url)
        soup = BeautifulSoup(response.content, "html.parser")
        main_info = extract_main_info(soup)
        # Extract datetime information
        test_date = main_info.get("Test Date")
        test_time = main_info.get("Test Time")
        datetime_key = f"{test_date} - {test_time}"
        if not datetime_key or datetime_key not in JEE_MAIN_ANSWERS_FINAL:
            return {
                "status": "error",
                "message": f"{datetime_key} test answers not found"
            }

        questions = {}
        for qpanel in soup.select("div.question-pnl"):
            qno = qpanel.select_one("td.bold").text.strip()
            
            question_type = identify_question_type(qpanel.select_one("table"))
            if question_type == "MCQ":
                questions[qno] = parse_type_A_question(qpanel.select_one("table"), base_url)
            else:
                questions[qno] = parse_type_B_question(qpanel.select_one("table"), base_url)
        data = []
        i = 0
        for k, ques in questions.items():
            info = {
                "question_number": i+1,
                "question_type": ques["question_type"],
                "question_id": ques["question_id"],
                "question_img_url": ques["question_img_url"]
            }
            answer_id = JEE_MAIN_ANSWERS_FINAL[datetime_key][ques["question_id"]]
            question_type = ques["question_type"]

            if question_type == "MCQ":
                info["option_1_url"] = ques["options_url"][0]
                info["option_2_url"] = ques["options_url"][1]
                info["option_3_url"] = ques["options_url"][2]
                info["option_4_url"] = ques["options_url"][3]
                info["chosen_option"] = ques["chosen_option"]

                # Add correct option information
                if ques["option_1_id"] == answer_id:
                    info["correct_option"] = "1"
                elif ques["option_2_id"] == answer_id:
                    info["correct_option"] = "2"
                elif ques["option_3_id"] == answer_id:
                    info["correct_option"] = "3"
                elif ques["option_4_id"] == answer_id:
                    info["correct_option"] = "4"

                if ques["chosen_option"] == "--":
                    score_card["unanswered_questions"] += 1
                    info["status"] = "Not Answered"
                else:
                    score_card["answered_questions"] += 1
                    info["status"] = "Answered"

                    selected_option_id = ""
                    chosen_option = ques["chosen_option"]
                    
                    if chosen_option == "1":
                        selected_option_id = ques["option_1_id"]
                    elif chosen_option == "2":
                        selected_option_id = ques["option_2_id"]
                    elif chosen_option == "3":
                        selected_option_id = ques["option_3_id"]
                    elif chosen_option == "4":
                        selected_option_id = ques["option_4_id"]

                    # Determine which subject this question belongs to based on question number
                    if 1 <= info["question_number"] <= 25:  # Mathematics
                        if selected_option_id == answer_id:
                            score_card["maths_marks"] += 4
                            score_card["total_marks"] += 4
                        else:
                            score_card["wrong_answers"] += 1
                            score_card["maths_marks"] -= 1
                            score_card["total_marks"] -= 1
                    elif 26 <= info["question_number"] <= 50:  # Physics
                        if selected_option_id == answer_id:
                            score_card["physics_marks"] += 4
                            score_card["total_marks"] += 4
                        else:
                            score_card["wrong_answers"] += 1
                            score_card["physics_marks"] -= 1
                            score_card["total_marks"] -= 1
                    elif 51 <= info["question_number"] <= 75:  # Chemistry
                        if selected_option_id == answer_id:
                            score_card["chemistry_marks"] += 4
                            score_card["total_marks"] += 4
                        else:
                            score_card["wrong_answers"] += 1
                            score_card["chemistry_marks"] -= 1
                            score_card["total_marks"] -= 1
            else:
                info["given_answer"] = ques["given_answer"]
                if ques["given_answer"] == "--":
                    score_card["unanswered_questions"] += 1
                    info["status"] = "Not Answered"
                else:
                    info["status"] = "Answered"
                    info["correct_answer"] = answer_id

                    score_card["answered_questions"] += 1

                    given_answer = ques["given_answer"]
                    # Determine which subject this question belongs to based on question number
                    if 1 <= info["question_number"] <= 25:  # Mathematics
                        if given_answer == answer_id:
                            score_card["maths_marks"] += 4
                            score_card["total_marks"] += 4
                        else:
                            score_card["wrong_answers"] += 1
                            score_card["maths_marks"] -= 1
                            score_card["total_marks"] -= 1
                    elif 26 <= info["question_number"] <= 50:  # Physics
                        if given_answer == answer_id:
                            score_card["physics_marks"] += 4
                            score_card["total_marks"] += 4
                        else:
                            score_card["wrong_answers"] += 1
                            score_card["physics_marks"] -= 1
                            score_card["total_marks"] -= 1
                    elif 51 <= info["question_number"] <= 75:  # Chemistry
                        if given_answer == answer_id:
                            score_card["chemistry_marks"] += 4
                            score_card["total_marks"] += 4
                        else:
                            score_card["wrong_answers"] += 1
                            score_card["chemistry_marks"] -= 1
                            score_card["total_marks"] -= 1

            data.append(info)
            i += 1

        return {
            "status": "success",
            "message": "Marks calculated successfully",
            "data": data,
            "score_card": score_card
        }
    except Exception as e:
        print(f"Error: {e}")
        return HTTPException(status_code=400, detail=f"Error processing URL: {str(e)}")