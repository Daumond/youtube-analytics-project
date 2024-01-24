from googleapiclient.discovery import build
from dotenv import load_dotenv
import os


load_dotenv()


class Video:
    API_KEY: str = os.getenv('YOUTUBE-API')

    def __init__(self, video_id):
        self.video_id = video_id
        self.video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                               id=self.video_id).execute()
        try:
            self.title: str = self.video_response['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/watch?v={self.video_response['items'][0]['id']}'"
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            print("Could not find ID of video")
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return f'{self.title}'

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.API_KEY)


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
