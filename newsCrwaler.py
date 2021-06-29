import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import urllib
import pandas as pd


def maintext(url):
    main_text = ""

    raw_id = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
    soup_id = BeautifulSoup(raw_id.text, "html.parser")
    if "yna" in url:
        texts = soup_id.select_one("div.scroller01")
        for txt in texts.find_all("p")[:-2]:
            main_text += txt.text

    elif "donga" in url:
        class_ignore = ["articlePhotoC", "armerica_ban", "article_relation", "center_ban", "bestnews" ]
        texts = soup_id.select_one("div.article_txt")
        main_text = texts.text
#                main_text = article_txt.find_all("div", class_= key:lambda x: x not in class_ignore)
        filtering = []
        for txt in texts.select("script"):
            filtering.append(txt.text)
        for txt in texts.find_all("div", class_=lambda x: x in class_ignore):
            filtering.append(txt.text)
                
        for ignore in filtering:
            main_text = main_text.replace(ignore, "")
    
    elif "joins" in url:
        class_ignore = ["ab_photo photo_center ", "ab_subtitle", "ab_related_article", "" ]
        texts = soup_id.select_one("#article_body")
        main_text = texts.text
        filtering = []
        for txt in texts.select("script"):
            filtering.append(txt.text)
        for txt in texts.find_all("div", class_=lambda x: x in class_ignore):
            filtering.append(txt.text)
                
        for ignore in filtering:
            main_text = main_text.replace(ignore, "")
    
    elif "chosun" in url:
        texts = soup_id.find("body").text
        idx1 = texts.find("created_date")

        texts = texts[:idx1]
        idx2 = texts.find('content":')
        texts = texts[idx2:]
        main_text = texts
    
    elif "khan" in url:
        texts = soup_id.select("div.art_body > p.content_text")
        for txt in texts:
            main_text += txt.text
    
    elif "hani" in url:
        main_text += soup_id.select_one("div.text").text
        

    return main_text


def main(n_article, keyword):
  
    for p in range(1, n_article, 10):
        url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query="+quote(keyword)+"&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=272&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start="+str(p
                                                                                        
                                                                                        )
        raw = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
        html = BeautifulSoup(raw.text, "html.parser")
        articles = html.select("ul.list_news > li")
 
        for art in articles:
            title = art.select_one("a.news_tit")["title"]
            url = art.select_one("a.news_tit")["href"]
            idx1 = url.find("/")
            href = url[idx1+2:]
            idx2 = href.find("/")
            source = href[:idx2]
            try:
                main = maintext(url)
                if len(main) != 0:
                    data.append([source, title, main])
            except requests.exceptions.SSLError as e:
                continue
            


if __name__ == "__main__":
    n_article = 1000  # number of article to find
#    keyword = input("Enter keyword")
    keyword = "삼성생명"

    data = []
    main(n_article, keyword)

    df = pd.DataFrame(data=data, columns=['newspaper', 'title', 'maintext'])
    df.to_csv('result.csv', mode='w', index=False, encoding="utf-8-sig")