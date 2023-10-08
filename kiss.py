from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from models import Search, Series, Stream, Latest
import re
app = FastAPI()

BASE_URL = "https://kissasian.lu/"


# Create a route that accepts data as input using the Pydantic model

def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup,response


@app.get("/api/search/{query}")
async def search(query: str):
    url = BASE_URL + "Search/SearchSuggest"
    params = {'type': 'drama',
              'keyword': query}
    response = requests.post(url, data=params)
    search_results = []
    soup = BeautifulSoup(response.content, 'html.parser')
    for lis in soup.findAll("a"):
        # print(lis.get("href"))
        # print(lis.get("title"))
        temp = {
            "id": lis.get("href").replace("/Drama/", ""),
            "title": lis.text,
            "url": "https://kissasian.lu" + lis.get("href")

        }
        search_model = Search(**temp)

        search_results.append(search_model)

    return {
        "query": query,
        "response_length": len(soup.findAll("a")),
        "data": search_results
    }


@app.get("/api/series_info/{query}")
async def series_info(query: str):
    url = BASE_URL + "Drama/" + query
    soup, response = get_soup(url)
    other_names = []
    genres = []
    casts = []
    eps_list = []
    if response.status_code == 200:

        for othername in (soup.find("div", class_="section group").find("p").findAll("a")):
            other_names.append(othername.text)

        for genre in soup.find("div", class_="section group").findAll("a", class_="dotUnder"):
            genres.append(genre.text)

        for ele in (soup.findAll("div", class_="actor-info")):
            casts.append(ele.text.strip())

        content_list = soup.find("ul", class_="list")
        no_eps = len(content_list.findAll('a'))
        for ele in content_list.findAll('a'):
            eps_list.append("https://kissasian.lu" + ele.get('href'))

        # print({"no_eps":no_eps, "episode_links":eps_list})

        content = {
            "title": soup.find("div", class_="heading").text,
            "img_url": BASE_URL + soup.find("div", class_="col cover").find("img").get("src"),
            "other_names": other_names,
            "genre": genres,
            "casts": casts,
            "no_eps": no_eps,
            "episode_links": eps_list

        }
        series_res = Series(**content)
        return series_res


@app.get("/api/stream/{series_id}/{ep_no}")
async def get_stream(series_id: str, ep_no: int):
    url = BASE_URL + f"Drama/{series_id}/Episode-{str(ep_no)}"
    soup, response = get_soup(url)

    if response.status_code==200:
        try:
            vidmoly_url = soup.find("iframe", {"id": "mVideo"}).attrs['src']
            vid_soup,vid_res  = get_soup(vidmoly_url)
        except:
            return "Invalid Input"
        if vid_res.status_code==200:
            pattern = r'file:"(https://[^"]+)"'

            # Use re.search() to find the first match in the text
            match = re.search(pattern, vid_res.text)

            # Check if a match was found and extract the URL
            if match:
                url_main = match.group(1)
                temp =  {"series_id":series_id,"ep_no":ep_no,"stream_url":url_main}
                stream_res = Stream(**temp)
                return stream_res

            else:
                return "Cannot find any url"


@app.get("/api/latest")
async  def latest():
    url = "https://kissasian.lu/"
    soup, response = get_soup(url)
    latest_res = []
    if response.status_code == 200:

        for ele in (soup.find("div", class_="item-list").findAll("div", class_="info")):
            ep_url = ele.find("a").get("href")
            latest_series = ele.find("a").text.strip().split("\n")
            temp = {
                "title": latest_series[0],
                "latest_ep": latest_series[1],
                "ep_url": ep_url
            }
            latest_eps = Latest(**temp)
            latest_res.append(latest_eps)

        return {
            "list_len":len(latest_res),
            "data":latest_res
        }




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
