from bs4 import BeautifulSoup as bs4
from itertools import zip_longest
import pandas as pd
import requests
import time
url = "https://in.linkedin.com/jobs/search?keywords="
key = ["Web developer", " front end developer", " back end developer", " ui/ux designer", " software tester", " data analyst", " data architect", " cloud engineer", " cloud architect", " network administrator", " network engineer", " network architect", " data scientist", "Content writing, logo designing", "video editing",
       "digital marketing", "social media marketing", "Networks one category", "Cloud ", "Software development ", "Systems.. Designing", "testing admin one category", "Media", "graphic designers", "logo", "poster", "graphic designs", "social mefia", "content writers", " content writers", "video editors", "digital", "social", "media and sales"]
data = {}
total_time = time.perf_counter()
time_for_parsing = 0
time_for_doenload = 0
for i in key:
    start_time = time.perf_counter()
    print(f"Key : {i} \n")
    data_url = url+i
    print(f"Link {data_url} \n")
    req_start_time = time.perf_counter()
    html = requests.get(data_url).text
    req_end_time = time.perf_counter()
    time_for_parsing += req_end_time - req_start_time
    print(
        f"Downloaded Html Time {req_end_time - req_start_time:0.4f} seconds")
    req_start_time = time.perf_counter()
    soup = bs4(html, "lxml")
    req_end_time = time.perf_counter()
    print(f" Parsing Time {req_end_time - req_start_time:0.4f} seconds")
    time_for_parsing += req_end_time - req_start_time
    links = []
    for ultag in soup.find_all('ul', {'class': 'jobs-search__results-list'}):
        for litag in ultag.find_all('li'):
            for atag in ultag.find_all('a'):
                links.append(atag.get('href'))
    req_end_time = time.perf_counter()
    data[i] = links
    print(
        f" Time Taken for Extract Data for {i} is {req_end_time - req_start_time:0.4f} seconds")
end_time = time.perf_counter()
print(f"Total Time Taken {end_time - start_time:0.4f} seconds")
print(f"Total Time Taken for Parsing {time_for_parsing:0.4f} seconds")
print(f"Total Time Taken for Downloading {time_for_doenload:0.4f} seconds")
total_time = time.perf_counter() - total_time
print(f"Total Time Taken {total_time:0.4f} seconds")
zl = list(zip_longest(*data.values()))
df = pd.DataFrame(zl, columns=data.keys())
df.to_csv('out.csv')
