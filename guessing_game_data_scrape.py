import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
from csv import DictWriter
import io

user_agent_list = [
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
]

url = "https://ww2db.com/vehicle.php?list=a"
data_list = []

user_agent = random.choice(user_agent_list)
headers = {'User-Agent': user_agent}

def create_data():
	res = requests.get(url, headers=headers, timeout=20)
	soup = BeautifulSoup(res.content, "html.parser")

	data_table_html = soup.select('#dataTable')
	data_table_rows_html = data_table_html[0].select('tr')

	for item in data_table_rows_html:
		data = {}
		try:
			data['Name'] = item.select('a')[0].text
		except:
			data['Name'] = None
		try:
			data['Link'] = urllib.parse.urljoin('https://ww2db.com/', item.select('a')[0]['href'])
		except:
			data['Link'] = None
		try:
			data['Manufacturer'] = item.select('td')[2].text
		except:
			data['Manufacturer'] = None
		try:
			data['Role'] = item.select('td')[1].text
		except:
			data['Role'] = None
		try:
			data['Country'] = item.select('td')[3].text
		except:
			data['Country'] = None
		try:
			request = requests.get(data['Link'], headers=headers, timeout=20)
			soup = BeautifulSoup(request.content, "html.parser")
			content = soup.select('#content')
			image_link = content[0].select('.filephoto')
			image_url = urllib.parse.urljoin('https://ww2db.com', image_link[0]['src'])
			data['Picture'] = image_url
		except:
			data['Picture'] = None 
	
		data_list.append(data)
	data_list.pop(0)
	return data_list

def write_data(scraped_data):
	with io.open("data_archive.csv", "w", newline='') as file:
		headers = ["Name", "Link", "Manufacturer", "Role", "Country", "Picture"]
		csv_writer = DictWriter(file, fieldnames=headers)
		csv_writer.writeheader()
		for data in scraped_data:
			csv_writer.writerow(data)

scraped_data = create_data()
write_data(scraped_data)