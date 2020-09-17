import requests
from bs4 import BeautifulSoup
import pandas as pd

#Globals
home = 'https://www.setlist.fm'

def search_Setlist():
	newSearch = raw_input("Enter an Artist: ")
	urlSearch = newSearch.replace(" ", "+")
	addURL = "/search?query=" + newSearch
	currentURL = home + addURL
	page = requests.get(currentURL)
	soup = BeautifulSoup(page.content, 'html.parser')
	getDiv = soup.find("div", class_="col-xs-12 col-sm-3 col-md-12")
	if not getDiv:
		print("No Results, Try Again")
		return
	getAs = getDiv.find_all("a")
	results = []
	for a in getAs:
		results.append(a.text)
		if a.text == newSearch:
			newSearch = a.get('href')
			currentURL = home + "/" + newSearch
			return currentURL
	
def get_Artist(url):
	#newSearch = raw_input("Do you want Setlists or Stats: ")
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	currentURL = home + "/"
	getAs = soup.find("a", title="View song statistics of all setlists")
	if not getAs:
		print("No Results, Try Again")
		return 
	newSearch = getAs.get('href')
	currentURL += newSearch
	return currentURL
	
def get_Avg_Setlist(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	getUL = soup.find("ul", class_="nav nav-tabs nav-justified")
	getA = getUL.find("a", text="Avg Setlist")
	newUrl = getA.get('href')
	currentURL = str(newUrl)
	currentURL = currentURL[2:]
	newUrl = home + currentURL
	page = requests.get(newUrl)
	soup = BeautifulSoup(page.content, 'html.parser')
	getDivs = soup.find("div", class_="hidden-sml-display")
	getAs = getDivs.find_all("a")
	years = []
	print("Valid Years: ")
	for a in getAs:
		if int(a.text) > 365:
			print(a.text)
			years.append(a.text)
	getYear = raw_input("Please enter a year: ")
	print('\n')
	yearURL = ""
	if getYear in years:
		yearURL = newUrl + "?year=" + getYear;
	page=requests.get(yearURL)
	soup = BeautifulSoup(page.content, 'html.parser')
	getAs = soup.find_all("a", class_="songLabel")
	print("Average Setlist for " + getYear)
	for a in getAs:
		print(a.text)
	return

	
def find_top_played_songs(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	AllSongs = soup.find_all("a", class_="songName")
	Plays = soup.find_all("span", class_="barChart")
	songNames = [song.get_text() for song in AllSongs]
	playCounts = [int(play.get_text()) for play in Plays]
	
	songs = pd.DataFrame({
			"Song Name": songNames,
			"Play Count": playCounts
		})
	subSongs = songs[songs["Play Count"] > 100]
	print(subSongs)
	
if __name__ == '__main__':
	next = search_Setlist()
	next = get_Artist(next)
	goals = raw_input("Top Songs or Average Set? ")
	if goals.lower() == "top songs":
		find_top_played_songs(next)
	elif goals.lower() == "average set":
		get_Avg_Setlist(next)
	else:
		print("Please enter 'top songs' or 'average set'")
	
	
