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
            html_tiktok_web_video = self.tiktok_session.get(tiktok_url, headers=self.headers, proxies=self.proxies,timeout=5).text
        except requests.exceptions.Timeout:
            print("timeout in get_video_data_by_video_url")
            raise SystemExit("timeout in get_video_data_by_video_url")
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

        video_nsfw = 0
        tiktok_video_url = []
        try:
            tiktok_thumb = json_video_data['__DEFAULT_SCOPE__']['webapp.video-detail']['itemInfo']['itemStruct']['video']['dynamicCover']
            tiktok_video_url.append(json_video_data['__DEFAULT_SCOPE__']['webapp.video-detail']['itemInfo']['itemStruct']['video']['playAddr'])

            # if the item is a photo story video-> playAddr = '', just like dynamicCover
            if tiktok_video_url[0] == '':
                tiktok_video_url = []
                raise ValueError("photo story video-> playAddr empty")
        except Exception as e:
            try:
                tiktok_thumb = json_video_data['__DEFAULT_SCOPE__']['webapp.video-detail']['itemInfo']['itemStruct']['video']['cover']
                tiktok_video_url.append(json_video_data['__DEFAULT_SCOPE__']['webapp.video-detail']['itemInfo']['itemStruct']['music']['playUrl'])
                tiktok_video_url.append(tiktok_thumb)
                video_nsfw = -2
            except Exception as e:
                print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
                raise SystemExit('error getting html web video')

        return tiktok_video_url, tiktok_thumb, video_nsfw


    def download(self, tiktok_video_url: list, video_id: str, _type: int) -> list:
        """ download the video """

        download_list = []
        count = 0

        for item in tiktok_video_url:
            try:
                video = self.tiktok_session.get(item, headers=self.headers, proxies=self.proxies)
            except Exception as e:
                print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
                raise SystemExit('error downloading video')

            if _type == 0:
                path_filename = f'{video_id}.mp4'
            else:
                if count == 0:
                    path_filename = f'{video_id}.mp3'
                else:
                    path_filename = f'{video_id}_{count}.jpeg'
            try:
                with open(path_filename, 'wb') as f:
                    for chunk in video.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()
            except Exception as e:
                print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
                raise SystemExit('error writting video')

            count = count + 1
            download_list.append(path_filename)
 
        return download_list


    def get_video_filesize(self, video_url: str) -> str:
        """ get file size of requested video """

        filesize_list = []
        for item in video_url:

            try:
                video_size = self.tiktok_session.head(item, headers=self.headers, proxies=self.proxies, timeout=5)
                filesize_list.append(video_size.headers['content-length'])
            except requests.exceptions.Timeout:
                print("timeout in get_video_filesize")
                raise SystemExit("timeout in get_video_filesize")
            except Exception as e:
                print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
                raise SystemExit('error getting video file size')

        return filesize_list

    def get_video_id_by_url(self, video_url: str) -> str:
        """ get video id for use as filename """

        video_url = video_url.split('?')[0]
        video_id = video_url[:-1].split('/')[-1] if video_url[-1] == '/' else video_url.split('/')[-1]

        return video_id

##################################################################

if __name__ == "__main__":

    # use case example

    # set tiktok video url
    tiktok_url = ''
    if tiktok_url == '':
        if len(sys.argv) < 2:
            print('you must provide a tiktok url')
            exit()
        tiktok_url = sys.argv[1]

    # create scraper video object
    tiktok_video = TikTokVideoScraperWeb()

    # set the proxy (optional, u can run it with ur own ip)
    #tiktok_video.set_proxies('socks5://157.230.250.185:2144', 'socks5://157.230.250.185:2144')

    # get video url from video id
    tiktok_video_url, video_thumbnail, video_nsfw = tiktok_video.get_video_data_by_video_url(tiktok_url)

    # get the video filesize
    video_size = tiktok_video.get_video_filesize(tiktok_video_url)
    print(f'filesize: ~{video_size} bytes')

    # get video id for a filename
    video_id = tiktok_video.get_video_id_by_url(tiktok_url)

    # if video_nsfw = 0 is a video, no matter where came from(story/feed)
    # if video_nsfw = -2 is a "carrusel" from story
    downloaded_video_list = tiktok_video.download(tiktok_video_url, video_id, video_nsfw)
 
    tiktok_video.tiktok_session.close()
