import requests

url = 'https://sales-transcript-feedback.fly.dev/'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}



def start_bot(prompt:str, voice_id:str,roleplay_type):
    data = {
        "prompt": prompt,
        "voice_id": voice_id,
        "session_time": 10,
        "roleplay_type":roleplay_type,
        "difficulty_level":"Easy",
        "avatar_name":"John",
        "user_id":"test_user"
    }

    response = requests.post(url, headers=headers, json=data)

    # Print response status and content
    print("Status Code:", response.status_code)
    print("Response:", response.json())

    return response.json()


if __name__=="__main__":
    start_bot(prompt="you are a friendly assistant")
