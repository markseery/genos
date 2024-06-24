##########################################################################
#
#   Copyright / License notice 2024
#   --------------------------------
#
#   Permission is hereby granted, free of charge,
#       to any person obtaining a copy of this software
#       and associated documentation files (the “Software”),
#       to deal in the Software without restriction, including
#       without limitation the rights to use, copy, modify, merge,
#       publish, distribute, sublicense, and/or sell copies of the Software,
#       and to permit persons to whom the Software is furnished to do so,
#       subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included
#       in all copies or substantial portions of the Software.
#
##########################################################################
#
#   Details
#   -------------
#
#       Name: youtubetool.py
#       Author: Mark Seery
#
#   Notes
#   -----
#
#   Utility class to get youtube video info
#
#
##########################################################################
from langchain_community.document_loaders import YoutubeLoader
from pytube import Playlist

class YouTubeTool:
    def __init__(self):
        pass

    def getUrlsFromPlayList(self,URL_PLAYLIST: str ) -> tuple[str, ...]:
        " Get URLs in a YouTube playlist"
        " Just return the URLs, don't do anything with them"
        return Playlist(URL_PLAYLIST)
    
    def getYouTubeSummaryFromPlayList(self,URL_PLAYLIST: str ) -> {str, ...}:
        " Get video info for all videos in a YouTube playlist"
        " This can take an extend period of time to run if list is long"
        playlist = Playlist(URL_PLAYLIST)
        info = self.getYouTubeSummaryList(playlist)
        return info
    
    def getYouTubeSummaryList(self,urlList: tuple[str, ...] ) -> {str, ...}:
        " Create a list of video info DICTs for all videos in a YouTube playlist"
        summaryList = []
        for url in urlList:
            summaryList.append(self.getYouTubeInfo(url))
        return summaryList

    def getYouTubeInfo(self,query: str) -> str:
        "Get info for a specific video"
        videoDict = {}
        
        try:
            loader = YoutubeLoader.from_youtube_url(query)
            videoDict['success'] = True
            videoDict['title'] = loader._get_video_info()['title']
            videoDict['publish_date'] = loader._get_video_info()['publish_date']
            videoDict['author'] = loader._get_video_info()['author']
            videoDict['length'] = loader._get_video_info()['length']
            videoDict['transcript'] = loader.load()[0].page_content 
        except Exception as e:
            videoDict['success'] = False
            videoDict['transcript'] = "Error in getYouTubeTranscript: " + str(e)

        return videoDict
