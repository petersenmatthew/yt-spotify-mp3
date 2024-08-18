import json
from youtube_search import YoutubeSearch

def get_ytid(name):
    name = f"{name} (Audio)"
    results = YoutubeSearch(name, max_results=1).to_json()

    data = json.loads(results)

    video_id = data['videos'][0]['id']
    
    return(video_id)
