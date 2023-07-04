import requests
import time 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os 
from prefect import flow, task
from bs4 import BeautifulSoup
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from prefect.tasks import task_input_hash
from datetime import timedelta
import pandas as pd

@task()
def extract_links(location):
	with open(location) as fp:
		links = [(i+'/videos').replace('\n','') for i in fp.readlines()]
	return links

@task(log_prints=True)
def get_video_id(link):
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument("--disable-dev-shm-usage")
	chrome_prefs = {}
	chrome_options.experimental_options["prefs"] = chrome_prefs
	chrome_prefs["profile.default_content_settings"] = {"images": 2}
	video_channel_mapping = {}
	driver = webdriver.Chrome(chrome_options)
	driver.get(link)
	driver.fullscreen_window()
	time.sleep(1)
	scroll_pause_time = 2
	screen_height = driver.execute_script('return window.screen.height;')
	i=1
	while True:
		driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
		i+=1
		time.sleep(scroll_pause_time)
		scroll_height = driver.execute_script('return document.documentElement.scrollHeight;')
		if(screen_height)* i > 1.01 *scroll_height:
			break
	soup = BeautifulSoup(driver.page_source,'html.parser')
	list_of_videos = soup.find_all("a",id='video-title-link')
	list_of_videos = [i['href'].replace('/watch?v=','').split('?')[0] for i in list_of_videos]
	video_channel_mapping[link] = list_of_videos
	driver.close()
	return video_channel_mapping



@task(log_prints=True,retries=2,retry_delay_seconds=[60,120])
def get_data(API_URL,video_ids):
	dicts = {}
	for channel ,videos in video_ids.items():
		temp_list = []
		for video in videos:
			response = requests.get(API_URL+video)
			time.sleep(0.7)
			i=10
			if (response.status_code == 400):
				return -1
			while(response.status_code == 429):
				time.sleep(i)
				print(video)
				response = requests.get(API_URL + video)
			if(response.status_code == 200):
				temp_list.append({**response.json(),"channel":channel.replace('https://www.youtube.com/','').replace('@','').replace('/videos','')})

	return temp_list


@task()
def write_response_local(data):
	fpath = '/opt/prefect/data/latest.csv'
	data.to_csv(fpath)
	return fpath


@task()
def write_response_gcs(lpath,gpath):
	gcs_block = GcsBucket.load('yt-data')
	gcs_block.upload_from_path(from_path = lpath,
				to_path = gpath)
	
	return

@flow(log_prints=True)
def etlFlow():
	links_file_loc = '/opt/prefect/data/links.txt'
	links = extract_links(links_file_loc)
	print('happy to be here')
	#video_ids = get_video_ids(links)
	def req_fn(links):
		data = []
		for link in links:
			video_id = get_video_id(link)
			data += get_data('https://returnyoutubedislikeapi.com/Votes?videoId=',video_id)
		return data
	data = req_fn(links)
	df = pd.DataFrame.from_records(data)
		
		
	#data = get_data('https://returnyoutubedislikeapi.com/votes?videoId=',video_ids)
	file_loc = write_response_local(df)
	rvalue = write_response_gcs(file_loc,'results/latest.csv')
	return 0
	



if __name__ == '__main__':
	etlFlow()
