import requests #Tool to Request link and request for the whole code of the website
from bs4 import BeautifulSoup #WebScraping 
from PIL import Image
from io import BytesIO
import os
import json #For Storing Data
import asyncio
import aiohttp

class DataBase: #Soon Asyncio and aiohttp will dominate this class ,still learning it though
    def __init__(self):
            if os.path.exists("owo.json"): 
                with open("owo.json", "r") as json_file:
                    self.__page_cache = json.load(json_file) 
            else:
                self.__page_cache = {}
            self.__source = ["https://rawg.io/","https://rawg.io/games/pc","https://rawg.io/games/playstation5","https://rawg.io/games/xbox-one","https://rawg.io/games/ios","https://rawg.io/games/android"] #WebPages that have list of games
            self.__api_key = "7fcf04fb8f7a42b9b128d64e155802b5" #API Key for secure and safe scraping <3
            self.headers = {'Authorization': 'Bearer '+self.__api_key}
        
    def bubble_sort_games_by_date(self,games_data): 
        print("Sorting Dates . . .")
        n = len(games_data)
        for i in range(n):
            for j in range(0, n-i-1):
                if games_data[j]["release_date"] > games_data[j+1]["release_date"]:
                    games_data[j], games_data[j+1] = games_data[j+1], games_data[j] 

    def bubble_sort_games_by_popularity(self,games_data):
        print("Sorting Popularity . . .")
        n = len(games_data)
        for i in range(n):
            for j in range(0, n-i-1):
                if games_data[j]["popular"] < games_data[j+1]["popular"]:
                    games_data[j], games_data[j+1] = games_data[j+1], games_data[j]

    def date_changer(self,date): #Turning WebScraped Dates into formal formmat in order to Sort
        months = {
            "Jan": "01",
            "Feb": "02",
            "Mar": "03",
            "Apr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Aug": "08",
            "Sep": "09",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12"
        }

        month_day , year = date.split(", ") #May 1, 2024 = month_day(May 1) year(2024) it will remove the "," including the space
        month_name, day = month_day.split() # month_name(May) day(1) splitting the month_day

        numeric_month = months[month_name] #numeric_month(months[May:05] < May) = 05
        formatted_date = f"{year}-{numeric_month}-{day.zfill(2)}" #zfill for single num to put 0 at first , if day is 1 it will be add a 0 on it so = 01
        
        return formatted_date #Output: formatted_date(2024-05-01)

    def download_image(self,image_link):
        folder_path = "game_images"
        os.makedirs(folder_path, exist_ok=True)
        
        image_url = image_link["content"]
        
        if image_url:
            image_response = requests.get(image_url,headers=self.headers)
            image = Image.open(BytesIO(image_response.content))

            resized_image = image.resize((600,400))
            image_filename = os.path.join(folder_path, os.path.basename(image_url))

            resized_image.save(image_filename,quality = 90)
            return image_filename
        else:
            return "placeholder.jpg"

    def get_main_page_href(self): #Getting the main Pages that have list of Games 
        if os.path.exists("game_url.json"):
            with open("game_url.json","r") as json_file:
                game_links = json.load(json_file) 
        else:
            game_links = {} 
        
        percentage = 0 
        for url in self.__source:
            if url not in game_links: #if game_url exist and data is not on dictionary it will become true to avoid being requested with existing data and to avoid time consuming
                print(url,True) #To know what url is not on the data
                game_links[url] = {"Main page Links":[],"Game Names": [],"Game Popularity":[]} #Storing Links of games on the main pages including small thumbnail images and names
                response = requests.get(url,headers=self.headers) #Requesting the whole code of the Page inorder to scrape
                
                page_content = response.text #turning the code into a text inorder to find the specific data 
                soup = BeautifulSoup(page_content,"html.parser") #parsing the texted code on page_content
                if url == "https://rawg.io/": 
                    num_games = 45 #Taking the 45 Releases Games
                else:
                    num_games = 35 #Taking the top 35 most popular games
                href = soup.find_all('a', class_="game-card-medium__info__name")[:num_games] 
                popularity = soup.find_all(class_="game-card-button__inner")
                for link ,popular in zip(href,popularity): #Finding all div class with names "game-card-medium__info__name to get the link"
                    game_link = "https://rawg.io"+link['href'] #Along with the div class it will get its href or link through the game description
                    game_name = link.text #Getting the texted or string Game name
                    game_popularity = popular.text
                    game_links[url]["Game Names"].append(game_name)
                    game_links[url]["Main page Links"].append(game_link)
                    game_links[url]["Game Popularity"].append(game_popularity)

            if url == "https://rawg.io/":
                percentage +=25
            else:
                percentage += 15
            print(percentage,"%")
        self.save_data(game_links,"game_url.json") #Indent outside of the first for loop to know if the looping is finish then saving the earlier storage of game_links = {}
        return game_links #Output: game_links = {Along with processed data}

    def get_game_description(self):
        data = self.get_main_page_href() 
        for url , game_links in data.items(): 
            if url not in self.__page_cache: #Check if url or Gamelink is exist to avoid rewrite or doubled data of that url
                    self.__page_cache[url] = {} 
            needed_sorting_data = [] 
            for links , names , popularity in zip(game_links["Main page Links"],game_links["Game Names"],game_links["Game Popularity"]):
                if names not in self.__page_cache[url]: 
                    response = requests.get(links,headers=self.headers)  #requesting the link of game description page
                    page_content = response.text #Turning the description page into text inorder to find the data below:
                    soup = BeautifulSoup(page_content,"html.parser")
                    name_tag = soup.find("h1", itemprop="name", class_="heading heading_1 game__title")     #*GAME NAME
                    date_tag = soup.find("div", itemprop="datePublished")     #*GAME RELEASED DATE
                    genre_tag = soup.find_all("meta", itemprop="genre")     #*GAME GENRE
                    platform_tag = soup.find_all("meta",itemprop="gamePlatform")     #*GAME AVAILABLE PLATFORM
                    publisher_tag = soup.find("meta",itemprop="publisher")     #*GAME PUBLISHER
                    rating_section_tag = soup.find_all('div', class_='rating-distribution__label')     #*GAME RATINGS
                    game_description_tag = soup.find("div",class_="game__about-text")     #*GAME DESCRIPTION
                    developer_tag = soup.find_all("div",itemprop="creator")     #*GAME DEVELOPERS
                    website_tag = soup.find("div",class_="game__meta-website")     #*GAME OFFICIAL 
                    image_meta = soup.find("meta", itemprop="image")     #*GAME IMAGE
                    top_number_tag = soup.find_all("div",class_="rating-chart__number")     #*GAMING ACHIEVEMENT RATES
                    top_genre_tag = soup.find_all("a",class_="rating-chart__bottom-link")[1:]     #*GAME ACHIEVEMENT NAMES
                    wish_tag = soup.find("span",class_="btn-wishlist__title__counter")     #*GAME WISHLISTS
                    popular = int(popularity.replace(",","")) #*GAME POPULARITY

                    image_file_path = self.download_image(image_meta)

                    achievements = []
                    for number , genres in zip(top_number_tag,top_genre_tag):
                        top_number = number.text.strip()
                        top_genre = genres.text.strip()
                        achieve = top_number + " " + top_genre
                        achievements.append(achieve)


                    game_ratings = {}
                    for ratings in rating_section_tag:
                        rating_type = ratings.find("div",class_="rating__text")
                        rating_count = ratings.find("div",class_="rating-distribution__label-count")
                        if rating_count:
                            game_ratings[rating_type.text] = int(rating_count.text)
                        else:
                            game_ratings[rating_type.text] = 0

                    genre = []
                    for g in genre_tag:
                        genre.append(g["content"])

                    platform = []
                    for plat in platform_tag:
                        platform.append(plat["content"])
                    developer = []
                    for dev in developer_tag:
                        dev_tag = dev.find("meta", itemprop="name")
                        developer.append(dev_tag["content"])

                    game_name = name_tag.text.strip()

                    if wish_tag:
                        wishlist = wish_tag.text.strip()
                    else:
                        wishlist = "No Wishes"

                    if website_tag:
                        game_official_web = website_tag.text.strip()
                    else:
                        game_official_web = "None"
                        
                    if game_description_tag:
                        whole_description = game_description_tag.text.strip() 
                        cutting_description = whole_description.find(".")
                        game_short_description = whole_description[:cutting_description+1]
                    else:
                        game_short_description = "None"

                    if date_tag:
                        release_date = date_tag.text.strip()
                        game_release_date = self.date_changer(release_date)
                    else:
                        game_release_date = "2025-09-05" #!This need some fixing for the To Be Announced system

                    if publisher_tag:
                        game_publisher_name = publisher_tag["content"]
                    else:
                        game_publisher_name = "None"
                    if url == "https://rawg.io/": #the link is a sign for the Upcoming games 
                        sort_data = {"game_name":game_name,"release_date":game_release_date,"wishlist":wishlist,"popular":popular,"achievements":achievements,"image":image_file_path,"genre":genre,"platform":platform,"publisher":game_publisher_name,"rating":game_ratings,"description":game_short_description,"developers":developer,"official_link":game_official_web} #Data to Sort in Dates
                        needed_sorting_data.append(sort_data)
                        self.bubble_sort_games_by_date(needed_sorting_data)
                    else: #The else will be the most popular games 
                        sort_data = {"game_name":game_name,"release_date":game_release_date,"wishlist":wishlist,"popular":popular,"achievements":achievements,"image":image_file_path,"genre":genre,"platform":platform,"publisher":game_publisher_name,"rating":game_ratings,"description":game_short_description,"developers":developer,"official_link":game_official_web} #Data to Sort for Popularity
                        needed_sorting_data.append(sort_data)
                        self.bubble_sort_games_by_popularity(needed_sorting_data)
                    print("ok",game_name) #ok.
            for sorted_data in needed_sorting_data:
                self.__page_cache[url][sorted_data["game_name"]] = {"Release Date": sorted_data["release_date"],"Wishlist":sorted_data["wishlist"],"Popularity":sorted_data["popular"],"Achievements":sorted_data["achievements"],"Image":sorted_data["image"], "Genre":sorted_data["genre"],"Platform":sorted_data["platform"],"Publisher":sorted_data["publisher"],"Rating":sorted_data["rating"],"Description":sorted_data["description"],"Developers":sorted_data["developers"],"Official Link Website":sorted_data["official_link"]}
            print("done")  
            
    def save_data(self,dictionary,file_name): #Saving data using json
        formatted_json = json.dumps(dictionary, indent=4) #Indent to make the database readable and organized
        with open(file_name, "w") as json_file: #"w" means write
                json_file.write(formatted_json)
        return self

    def update_data(self): #*On Development
        pass

    def check_updated_date(self): #*On Development
        pass

    def get_online_data(self): 
        data = self.get_game_description() #getting all the needed data
        self.save_data(self.__page_cache,"owo.json")
        
    def get_data(self):
        return self.__page_cache #returning the data with data loaded by json
    
    def get_page_url(self):
        return self.__source

if __name__ == "__main__":
    data = DataBase()
    data.get_online_data()

#robots.txt of the website just to make sure the url of the website dont have the following: , check also game_url.json for the other url -vince
# vr - User-agent: *
# vr - Disallow: /signup
# vr - Disallow: /login
# vr - Disallow: /import
# vr - Disallow: /search
# vr - Disallow: /collections/create
# vr - Disallow: /reviews/create
# vr - Disallow: /amp/
# vr - Disallow: /settings/
# vr - Disallow: /discover/*
# vr - Disallow: /developers/*
# vr - Disallow: /publishers/*
# vr - Disallow: /tags/*
# vr - Disallow: /games/*/reddit*
# vr - Disallow: /games/*/twitch*
# vr - Disallow: /games/*/updates*
# vr - Disallow: /games/*/imgur*
# vr - Disallow: /games/*/edit*
# vr - Disallow: /@*
# vr - Disallow: /*filter=*
# vr - Disallow: /*filters=*
# vr - Disallow: /*tldr=*
# vr - Disallow: /*cache_off=

# vr - Sitemap: https://rawg.io/sitemap.xml

#-----------------------------
#* Reference: https://rawg.io/ 
#-----------------------------