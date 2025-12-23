import requests
import json
import os
from requests.auth import HTTPBasicAuth

# === Configuration ===
domain = "jcautomation.talentlms.com"
api_key = "ETbFWMe1RE4b8M2jpn6p24P9AchBM9"
output_file = os.path.abspath("user_course_status.json")  # Save in current directory

# === Helper Function ===
def get_data(url, label):
    try:
        response = requests.get(url, auth=HTTPBasicAuth(api_key, ''))
        response.raise_for_status()
        print(f"✅ Retrieved {label}")
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching {label} from {url}: {e}")
        return None

# === Step 1: Get all users ===
users_url = f"https://{domain}/api/v1/users"
users = get_data(users_url, "users")

if not users or not isinstance(users, list):
    print("⚠️ No users returned. Exiting.")
    exit(1)

print(f"📊 Users found: {len(users)}")

# === Step 2: Get courses per user ===
user_course_data = []

for user in users:
    user_id = user.get('id')
    if not user_id:
        continue

    user_courses_url = f"https://{domain}/api/v1/users/id:{user_id}/courses"
    user_data = get_data(user_courses_url, f"courses for user {user_id}")

    if not user_data or "courses" not in user_data:
        print(f"⚠️ No course data for user {user_id}")
        continue

    courses = user_data["courses"]

    for course in courses:
        if not isinstance(course, dict):
            continue
        user_course_data.append({
            'user_id': user.get('id'),
            'name': user.get('name', 'N/A'),
            'email': user.get('email', 'N/A'),
            'course_id': course.get('id'),
            'course_title': course.get('name', 'N/A'),
            'progress': course.get('completion_percentage', '0'),
            'completion_status': course.get('completion_status', 'unknown')
        })

print(f"📦 Total user-course records collected: {len(user_course_data)}")

# === Step 3: Save to JSON ===
if user_course_data:
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(user_course_data, f, indent=2)
        print(f"💾 JSON file saved to: {output_file}")
    except Exception as e:
        print(f"❌ Failed to save file: {e}")
else:
    print("⚠️ No user-course data to save.")
