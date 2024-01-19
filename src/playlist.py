import datetime
import os
import isodate

from dotenv import load_dotenv
from googleapiclient.discovery import build
from typing import List

from src.video import Video


load_dotenv()


class PlayList:

    api_key: str = os.getenv('YOUTUBE-API')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist_videos = PlayList.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                     part='contentDetails ,snippet',
                                                                     maxResults=50,
                                                                     ).execute()
        self.title = self.playlist_videos['items'][0]['snippet']['title'].split('.')[0]
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id
        self.video_ids: List[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = Video.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                id=self.video_ids).execute()

    @property
    def total_duration(self):

        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            video_duration = isodate.parse_duration(iso_8601_duration)
            total_duration += video_duration
        return total_duration

    def show_best_video(self):

        best_like = 0
        for video in self.video_response['items']:
            video_id = video['id']
            like_count = video['statistics']['likeCount']
            if int(like_count) > best_like:
                best_video_url = 'https://youtu.be/' + video_id
        return best_video_url
