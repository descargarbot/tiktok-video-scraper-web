# tiktok video scraper (web)
<div align="center">
  
![DescargarBot](https://www.descargarbot.com/v/download-github_tiktok.png)
  
[![TikTok](https://img.shields.io/badge/on-descargarbot?logo=github&label=status&color=green
)](https://github.com/descargarbot/tiktok-video-scraper-web/issues "TikTok Web")
</div>

<h2>dependencies</h2>
<code>Python 3.9+</code>
<code>requests</code>
<br>
<br>
<h2>install dependencies</h2>
<ul>
<li><h3>requests</h3></li>
  <code>pip install requests</code><br>
  <code>pip install -U 'requests[socks]'</code>
  <br>
<br>
</ul>
<h2>use case example</h2>

    #import the class TikTokVideoScraperWeb
    from tiktok_video_scraper_web import TikTokVideoScraperWeb

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
    
  or you can use the CLI
  <br><br>
  <code>python3 tiktok_video_scraper_web.py TIKTOK_URL</code>
<br><br>
<h2>online</h2>
<ul>
  ⤵
  <li> web 🤖 <a href="https://descargarbot.com" >  DescargarBot.com</a></li>
  <li> <a href="https://t.me/xDescargarBot" > Telegram Bot 🤖 </a></li>
  <li> <a href="https://discord.gg/gcFVruyjeQ" > Discord Bot 🤖 </a></li>
</ul>


