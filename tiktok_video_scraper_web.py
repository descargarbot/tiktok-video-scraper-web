import requests
import re
import sys
import json

##################################################################
class TikTokVideoScraperWeb:

    def __init__(self):
        """ Initialize """

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Referer': 'https://www.tiktok.com/'
        }

        self.proxies = {
            'http': '',
            'https': '',
        }

        self.tiktok_session = requests.Session()
    
    def set_proxies(self, http_proxy: str, https_proxy: str) -> None:
        """ set proxy  """

        self.proxies['http'] = http_proxy 
        self.proxies['https'] = https_proxy
    

    def get_video_data_by_video_url(self, tiktok_url: str) -> tuple:
        """ get video url from web
            note that the url obtained is not accessible without 
            the cookies obtained in the first get and that is why
            the urls obtained from web are not shareable """

        try:
            html_tiktok_web_video = self.tiktok_session.get(tiktok_url, headers=self.headers, proxies=self.proxies).text
        except Exception as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('error getting html web video')

        matches = re.findall(
            r'<script\s+[^>]*id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>\s*(.*?)\s*</script>',
            html_tiktok_web_video,
            re.DOTALL
        )

        if matches:
            text_video_data = matches[0].strip()
        else:
            raise SystemExit('__UNIVERSAL_DATA_FOR_REHYDRATION__ error')

        try:
            json_video_data = json.loads(text_video_data)
        except json.JSONDecodeError as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('error getting json web video')

        try:
            tiktok_thumb = json_video_data['__DEFAULT_SCOPE__']['webapp.video-detail']['itemInfo']['itemStruct']['video']['dynamicCover']
            tiktok_video_url = json_video_data['__DEFAULT_SCOPE__']['webapp.video-detail']['itemInfo']['itemStruct']['video']['playAddr']
        except Exception as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('error getting html web video')

        return tiktok_video_url, tiktok_thumb


    def download(self, tiktok_video_url: str, video_id: str) -> list:
        """ download the video """

        try:
            video = self.tiktok_session.get(tiktok_video_url, headers=self.headers, proxies=self.proxies, stream=True)
        except Exception as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('error downloading video')

        
        path_filename = f'{video_id}.mp4'
        try:
            with open(path_filename, 'wb') as f:
                for chunk in video.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
        except Exception as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('error writting video')

        return [path_filename]


    def get_video_filesize(self, video_url: str) -> str:
        """ get file size of requested video """

        try:
            video_size = self.tiktok_session.head(video_url, headers=self.headers, proxies=self.proxies)
        except Exception as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('error getting video file size')

        return video_size.headers['content-length']

    def get_video_id_by_url(self, video_url: str) -> str:
        """ get video id for use as filename """

        video_url = video_url.split('?')[0]
        video_id = video_url[:-1].split('/')[-1] if video_url[-1] == '/' else video_url.split('/')[-1]

        return video_id

##################################################################

if __name__ == "__main__":

    # use case example

    # set tiktok video url
    tiktok_url = 'your tiktok video url'

    # create scraper video object
    tiktok_video = TikTokVideoScraperWeb()

    # set the proxy (optional, u can run it with ur own ip)
    #tiktok_video.set_proxies('socks5://157.230.250.185:2144', 'socks5://157.230.250.185:2144')

    # get video id from url, just for filename in web scraper
    video_id = tiktok_video.get_video_id_by_url(tiktok_url)
    
    # get video url from video id
    tiktok_video_url, video_thumbnail = tiktok_video.get_video_data_by_video_url(tiktok_url)

    # get the video filesize
    video_size = tiktok_video.get_video_filesize(tiktok_video_url)
    print(f'filesize: ~{video_size} bytes')

    # get video id for a filename
    video_id = tiktok_video.get_video_id_by_url(tiktok_url)

    # download video by url
    downloaded_video_list = tiktok_video.download(tiktok_video_url, video_id)
 
    tiktok_video.tiktok_session.close()
