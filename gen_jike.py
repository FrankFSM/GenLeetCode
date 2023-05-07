import requests
import json


def get_geektime_courses_by_api():
    url = "https://gateway-api.geekbang.org/course_api/courses/list"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    data = {
        "page": 1,
        "size": 20,
        "is_new": 0,
        "category": -1,
        "direction": -1,
        "last_id": 0
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = json.loads(response.text)
        courses = result['data']['list']

        for course in courses:
            title = course['title']
            description = course['brief']
            print(f"Title: {title}\nDescription: {description}\n")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")


if __name__ == '__main__':
    get_geektime_courses_by_api()
