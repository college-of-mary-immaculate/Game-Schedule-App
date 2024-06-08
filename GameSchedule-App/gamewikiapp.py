from databaserapp import DataBase  # Importing the DataBase class from databaserapp.py
from widget_generator import WidgetGenerator
import tkinter as tk
from datetime import date , datetime


class GameScheduleUI:
    def __init__(self):
        self.__window = tk.Tk()
        #self.__window.resizable(False,False)
        self.__window.state("zoomed")
        self.__window.title("Horizon | Gaming ")
        self.__window["background"] = "#666769"
        
        self.__widget = WidgetGenerator()
        self.__datab = DataBase()

        self.__width = 1350
        self.__height = 1000
        self.__window.geometry(f"{self.__width}x{self.__height}")
        self.__game_data = self.__datab.get_data()
        self.main_page_url = self.__datab.get_page_url()
        self.frame =[]
        
    def test(self):
        for url , game_detail in self.__game_data.items():
            if url == "https://rawg.io/":
                for i ,(game ,detail) in enumerate(game_detail.items()):
                    if str(date.today()) < detail["Release Date"]:
                        print(i,game,"-",detail["Release Date"])

    def edit_distance(self,string1, string2):
        m, n = len(string1), len(string2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if string1[i - 1] == string2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j],dp[i][j - 1],dp[i - 1][j - 1])  
        return dp[m][n]

    def find_game(self,event,text,page_link,where_origin):
        game_name = text.get()
        if game_name != "":
            closest_match = []
            threshold = len(game_name) // 2

            for url , game_detail in self.__game_data.items():
                if url == page_link:
                    for game,detail in game_detail.items():
                        if url == "https://rawg.io/":
                            if str(date.today()) < detail["Release Date"] and where_origin == "upcoming" or where_origin == "available" and str(date.today()) > detail["Release Date"]:
                                edit_distance = self.edit_distance(game_name.lower(),game.lower())
                                if game_name.lower() in game.lower():
                                    closest_match.append(game)
                                elif edit_distance <= threshold:
                                    closest_match.append(game)
                        else:
                            edit_distance = self.edit_distance(game_name.lower(),game.lower())
                            if game_name.lower() in game.lower():
                                closest_match.append(game)
                            elif edit_distance <= threshold:
                                closest_match.append(game)
    
            if len(closest_match) == 0:
                closest_match.append(f"Game: {game_name}")
                closest_match.append("Not Found")
              
            self.show_games_list(page_link,closest_match,where_origin)
            
        elif game_name == "":
            self.show_games_list(page_link,None,where_origin)

    def show_games_list(self,page_name,searched,where):
        self.__widget.clear_frames(self.frame)
        upper_frame = self.__widget.create_frame_pack(None,"#32213A",None,None,"flat",0,"top","x",None)
        self.frame.append(upper_frame)
        not_just_logo = self.__widget.create_img(upper_frame,100,20,None,r"assets\app_logo.png",False,"grid","e",None,0,0,(50,210),None,None)
        not_just_logo.bind("<Button-1>",lambda event:self.show_home())

        self.__widget.create_label_grid(upper_frame,f"{"\u2B55"} Search",15,None,"w","#32213A","white",None,None,None,0,2,None,"w",None,20,None)

        search = self.__widget.create_entry_grid(upper_frame,15,None,None,70,0,1,None,"w",(40,20),20)
        search.bind("<Return>",lambda event, game_name = search,url = page_name: self.find_game(event,game_name,url,where))
     
        left_frame = self.__widget.create_frame_pack(None,"#383B53",None,None,"flat",None,"left","y",None)
        self.frame.append(left_frame)
        button_platform_frame = self.__widget.create_frame_grid(left_frame,"#383B53",325,395,"flat",None,"e",0,0,None,None,None,None,"grid")
        self.__widget.create_label_grid(button_platform_frame,f"Popular By Platforms {"\U00002B50"}",15,None,"w","#383B53","white",None,20,None,0,0,None,None,(20,0),20,None)
        platform_button_name = ["PC","PS5","XBOX","IOS","ANDROID"]
        image_path = [r"assets\pc_unselected_icons.jpg",
                    r"assets\ps5_unselected_icons.jpg",
                    r"assets\xbox_unselected_icons.jpg",
                    r"assets\ios_unselected_icons.jpg",
                    r"assets\android_unselected_icons.jpg"]
        
        i = 1
        for image_name,main_url , plat_name in zip(image_path,self.main_page_url[1:],platform_button_name):
            self.__widget.create_button_grid(button_platform_frame,image_name,f"{plat_name}","left","white","#383B53",None,15,"flat","w",223,None,i,0,None,None,2,lambda url = main_url : self.show_games_list(url,searched=None,where = "platform"))
            i+=1

        img = r"assets\unselected_upcoming_page.jpg"
        upcoming_button_frame = self.__widget.create_frame_grid(left_frame,"#32213A",325,230,"flat",None,"e",1,0,None,None,None,None,"grid")
        home_page = self.__widget.create_img(upcoming_button_frame,325,231,None,img,False,"grid",None,None,0,0,None,None,None)
        home_page.bind("<Enter>",lambda event ,image = home_page,image_path = img: self.__widget.enter_official_hover(event,image,image_path))
        home_page.bind("<Leave>",lambda event ,image = home_page,original_img = img: self.__widget.leave_official_hover(event,image,original_img))
        home_page.bind("<Button-1>",lambda event: self.show_games_list("https://rawg.io/",searched=None,where = "upcoming"))

        widgets = self.__widget.create_table("#666769",page_name)
        for widget in widgets:
            self.frame.append(widget)
        
        for url,game_detail in self.__game_data.items():
            if searched:
                if url == page_name: 
                    self.show_searched_games(widgets[0],widgets[1],game_detail,url,searched,where)
            else:
                if url == page_name and where == "upcoming" or url == page_name and where == "available":
                    self.show_game_schedule_releases(widgets[0],widgets[1],game_detail,url,where)
                elif url == page_name and where == "platform":
                    self.show_popular_games(widgets[0],widgets[1],game_detail,url,where)
  
    def change_date(self,date):
        months = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",7: "Jul", 8: "Aug", 9: "Sept", 10: "Oct", 11: "Nov", 12: "Dec"}

        date_obj = datetime.strptime(date,"%Y-%m-%d")

        month_number = date_obj.month
        month = months[month_number]
        formatted_date = date_obj.strftime(f"{month} %d, %Y")

        return formatted_date

    def show_searched_games(self,canvas,frame,game_detail,url,searched,where):
        if len(searched) == 2 and searched[1] == "Not Found":
            i = 4
            not_found_cell = self.__widget.create_cell(i,canvas,frame,"404","not_found")
            self.__widget.create_img(not_found_cell,765,270,None,r"assets\404_lol.jpg",False,"grid","w",None,0,0,None,None,None)
            self.__widget.create_cell(i+1,canvas,frame,"bottomspace","searched")
        else:
            i = 1
            for game ,detail in game_detail.items():
                        for searched_games in searched:
                            if game == searched_games:
                                cell = self.__widget.create_cell(i,canvas,frame,"List","searched")
                                self.frame.append(cell)
                                img_frame = self.__widget.create_frame_grid(cell,"#383B53",440,220,"flat",None,"w",0,0,None,None,None,None,"pack")
                                img = self.__widget.create_img(img_frame,440,234,"#32213A",rf"{detail["Image"]}",False,"pack",None,None,None,None,None,None,None)

                                short_game_info = self.__widget.create_frame_grid(cell,"#383B53",440,140,"flat",None,"W",1,0,None,None,None,None,"grid")
                                self.__widget.create_label_grid(short_game_info,game,16,None,"w","#383B53","white","left",30,None,0,0,2,"w",(10,0),(7,0),300)
                                self.__widget.create_label_grid(short_game_info,f"______________",12,None,"w","#383B53","white","left",20,None,1,0,2,"w",(12,0),(0,0),200)
                                self.__widget.create_label_grid(short_game_info,f"Release Date:",11,None,"w","#383B53","white","left",20,None,2,0,None,"w",(12,0),(0,0),200)

                                date = self.change_date(detail["Release Date"])
                                if date == "Sept 05, 2025":
                                    date_text = "To Be Announced"
                                else:
                                    date_text = date
                                self.__widget.create_label_grid(short_game_info,date_text,11,None,"w","#383B53","#FFD100","left",20,None,3,0,None,"w",(12,0),(0,0),200)
                                view_button = self.__widget.create_img(short_game_info,126,40,"yellow",r"assets\searched_veiw_more_unselected.jpg",False,"grid","e",None,2,1,(110,0),None,2)
                                view_button.bind("<Enter>",lambda event: self.__widget.view_button_search_enter(event))
                                view_button.bind("<Leave>",lambda event ,image = r"assets\searched_veiw_more_unselected.jpg": self.__widget.view_button_search_leave(event,image))
                                view_button.bind("<Button-1>",lambda event, game_name = game,game_detail = detail,page_name = url: self.show_game_description(game_name,game_detail,page_name,where)) 
                                i +=1
            self.__widget.create_cell(i+2,canvas,frame,"bottomspace","searched")

    def show_game_schedule_releases(self,canvas,frame,game_detail,url,where):
        i = 3
        for game ,detail in game_detail.items():
                if where == "upcoming" and str(date.today()) < detail["Release Date"] or where == "available" and str(date.today()) > detail["Release Date"]:
                    cell = self.__widget.create_cell(i,canvas,frame,"List","show_all")
                    self.frame.append(cell)
                    top = self.__widget.create_label_pack(cell,None,0,"left","#32213A",None,25,2,None,None,"w",None,None,None)
                    
                    img = self.__widget.create_img(cell,221,150,"#32213A",rf"{detail["Image"]}",True,"pack",None,None,None,None,None,None,None)
                    label_name = self.__widget.create_label_pack(cell,game,18,"left","#32213A","white",None,None,None,None,"w",10,None,210)
                    
                    self.__widget.create_button_pack(cell,None,False,"View more +","#9E6200","#D1CAA1","bottom",10,"flat",35,None,None,None,lambda game_description = detail,game_name = game,back = url: self.show_game_description(game_name,game_description,back,where))
                    cell.bind("<Enter>",lambda event ,frame = cell,label = label_name,image = img ,top_label = top,release_date = detail["Release Date"]: self.__widget.enter_hover_frame(event,frame,label,release_date,image,top_label))
                    cell.bind("<Leave>",lambda event ,frame =cell, label = label_name,image = img,top_label = top: self.__widget.leave_hover_frame(event,frame,label,image,top_label))   
                    i +=1
        self.__widget.create_cell(i+2,canvas,frame,"bottomspace","show_all")
    
    def show_popular_games(self,canvas,frame,game_detail,url,where):
        i = 3
        for game ,detail in game_detail.items():
            cell = self.__widget.create_cell(i,canvas,frame,"List","show_all")
            self.frame.append(cell)
            top = self.__widget.create_label_pack(cell,None,0,"left","#32213A",None,25,2,None,None,"w",None,None,None)
            img = self.__widget.create_img(cell,221,150,"#32213A",rf"{detail["Image"]}",True,"pack",None,None,None,None,None,None,None)
            label_name = self.__widget.create_label_pack(cell,game,18,"left","#32213A","white",None,None,None,None,"w",10,None,210)
            
            self.__widget.create_button_pack(cell,None,False,"View more +","#9E6200","#D1CAA1","bottom",10,"flat",35,None,None,None,lambda game_description = detail,game_name = game,back = url: self.show_game_description(game_name,game_description,back,where))
            cell.bind("<Enter>",lambda event ,frame = cell,label = label_name,image = img ,top_label = top,release_date = detail["Release Date"]: self.__widget.enter_hover_frame(event,frame,label,release_date,image,top_label))
            cell.bind("<Leave>",lambda event ,frame =cell, label = label_name,image = img,top_label = top: self.__widget.leave_hover_frame(event,frame,label,image,top_label))   
            i +=1
        self.__widget.create_cell(i+2,canvas,frame,"bottomspace","show_all")
            
    def show_game_description(self,game_name,game_detail,back,wheres): 
        self.__widget.clear_frames(self.frame)
        self.__window.title("Horizon | Game Info Paradise")
        left_frame = self.__widget.create_frame_pack(None,"#383B53",600,None,"flat",None,"left","y","grid")
    
        self.frame.append(left_frame)

        image_frame = self.__widget.create_frame_grid(left_frame,"#383B53",600,400,"flat",0,"e",0,0,2,None,None,None,"grid")
        self.frame.append(image_frame)

        #self.__widget.create_label_grid(image_frame,None,10,None,None,None,None,50,1,0,0,2,None,None,None,None)
        self.__widget.create_img(image_frame,600,285,"#383B53",rf"{game_detail["Image"]}",False,"grid","w",2,1,0,None,None,None)
        self.__widget.create_label_grid(image_frame,f"{game_name}",28,None,"w","#383B53","white","left",23,None,2,0,2,"w",(15,0),(0,30),570)
        
        statistic_frame = self.__widget.create_frame_grid(left_frame,"#2E1B5B",400,250,"flat",None,"w",1,0,None,2,(20,3),(20,0),"grid")
        
        cell_width = 225
        cell_height = 30

        max_bar_width = cell_width - 40
        max_value = max(game_detail["Rating"].values())

        total_ratings = 0
        for i ,(text , rating_value) in enumerate(game_detail["Rating"].items()):
            if text == "Exceptional":
                pady = (20,0)
            else:
                pady = 2
            total_ratings+=rating_value
            self.__widget.create_label_grid(statistic_frame,f"{text}",12,None,"w","#2E1B5B","white","left",15,2,i,0,None,"w",14,pady,None)
            self.__widget.create_cell_bar_graph(statistic_frame,text,max_bar_width,max_value,cell_width,cell_height,rating_value,i,pady,"#2E1B5B")
        
        self.__widget.create_label_grid(statistic_frame,"Ratings",12,None,"w","#2E1B5B","white","left",15,2,i+1,0,None,"w",14,None,None)
        self.__widget.create_label_grid(statistic_frame,f"{total_ratings}",12,None,"center","#2E1B5B","white","left",20,2,i+1,1,None,"w",14,None,None)
    
        wishlist_frame = self.__widget.create_frame_grid(left_frame,"#2E1B5B",150,170,"flat",None,"w",1,1,None,None,(5,5),(13,0),"pack")
        self.__widget.create_label_pack(wishlist_frame,"\U0001F381",40,None,"#2E1B5B","white",10,0,None,None,None,0,0,None)
        self.__widget.create_label_pack(wishlist_frame,"Wishlist",12,None,"#2E1B5B","white",10,0,None,None,"center",2,(15,0),None)
        self.__widget.create_label_pack(wishlist_frame,f"{game_detail["Wishlist"]}",16,None,"#2E1B5B","white",10,0,None,None,"center",2,(15,0),None)
        
        button_back_frame = self.__widget.create_frame_grid(left_frame,"green",160,50,"flat",3,None,2,1,None,None,(0,10),(0,8),"pack")

        if wheres == "home":
            self.__widget.create_button_pack(button_back_frame,r"assets\closed_back.jpg",True,None,"white","#32213A","left",10,"flat",400,70,None,None,lambda: self.show_home())
        else:
            self.__widget.create_button_pack(button_back_frame,r"assets\closed_back.jpg",True,None,"white","#32213A","left",10,"flat",400,70,None,None,lambda: self.show_games_list(back,searched = None,where=wheres))
      
        right_frame = self.__widget.create_frame_pack(None,"#666769",760,None,"flat",None,"left","y","grid")
        self.frame.append(right_frame)

        header_frame = self.__widget.create_frame_grid(right_frame,"#2E1B5B",765,115,"flat",0,"w",0,0,3,None,None,None,"grid")
        # . . . ..  . . .. . . ..  . .  . . 
        left_part = self.__widget.create_frame_grid(header_frame,"#2E1B5B",390,115,"flat",0,"w",0,0,None,None,None,None,"grid")
        self.__widget.create_img(left_part,90,80,"#2E1B5B",r"assets\popular_icon.jpg",False,"grid","w",None,0,0,(20,0),(15,0),2)
        self.__widget.create_label_grid(left_part,f"{game_detail["Popularity"]:,}",40,None,"w","#2E1B5B","white","left",None,None,0,1,None,"w",(30,0),(15,0),None)
        self.__widget.create_label_grid(left_part,f"POPULARITY",10,None,"w","#2E1B5B","white","left",None,None,1,1,None,"w",(30,0),None,None)
        # . . . . .. . .. .. .. .. . .. .. .
        release = game_detail["Release Date"]
        dates = datetime.strptime(release,"%Y-%m-%d")
        release_date = dates.strftime("%B %d, %Y")
        if dates.month in [9,11,12]:
            font_s = 23
        else:
            font_s = 27
        
        if dates.year == 2025:
            formatted_date = "To Be Announced"
        else:
            formatted_date = release_date
        if str(date.today()) > release:
            release_text = "RELEASED DATE"
        else:
            release_text = "RELEASE DATE"

        righ_part = self.__widget.create_frame_grid(header_frame,"#32213A",390,115,"flat",0,"w",0,1,None,None,None,None,"grid")
        self.__widget.create_label_grid(righ_part,f"{formatted_date}",font_s,None,"w","#32213A","white","left",None,None,0,1,2,"w",(30,0),(25,0),None)
        self.__widget.create_label_grid(righ_part,f"{release_text}",10,None,"w","#32213A","#BF932A","left",None,None,1,1,None,"w",(30,0),(10,15),None)
        self.__widget.create_label_grid(righ_part,f"{"\U0001F5D3"}",14,None,"w","#32213A","#BF932A","left",None,None,1,2,None,"w",(0,300),(0,10),None)

        publisher_frame = self.__widget.create_frame_grid(right_frame,"#383B53",235,70,"flat",0,None,1,0,None,None,(20,0),(20,0),"grid")
        self.__widget.create_label_grid(publisher_frame,"Publisher:",10,None,"w","#383B53","#D4C57B","left",None,None,0,0,None,"w",(15,0),(5,0),None)

        if len(game_detail["Publisher"]) >= 17:
            font_size = 10
        elif len(game_detail["Publisher"]) <=16:
            font_size = 14
    
        self.__widget.create_label_grid(publisher_frame,f"{game_detail["Publisher"]}",font_size,"underline","e","#383B53","white","left",None,None,1,0,None,"e",(15,0),None,None)
    
        official = official_website_frame = self.__widget.create_frame_grid(right_frame,"#383B53",235,230,"flat",0,None,2,0,None,2,(20,0),(10,0),"grid")
        if str(date.today()) < game_detail["Release Date"]:
            image_path = r"assets\cart1_unselected_unreleased_icon.jpg"
        else:
            image_path = r"assets\cart2_unselected_released_icon.jpg"
        
        original_image_path = image_path
        image_cart = self.__widget.create_img(official_website_frame,160,175,None,image_path,False,"grid",None,None,0,0,45,(20,0),None)
        official.bind("<Enter>",lambda event = official,image = image_cart,img_path = image_path: self.__widget.enter_official_hover(event,image,img_path))
        official.bind("<Leave>",lambda event = official,image = image_cart,origin = original_image_path: self.__widget.leave_official_hover(event,image,origin))
        official.bind("<Button-1>",lambda event, official_web = game_detail["Official Link Website"]:self.__widget.on_click_official(official_web))
        image_cart.bind("<Button-1>",lambda event,official_web = game_detail["Official Link Website"]:self.__widget.on_click_official(official_web))
        
        platform_frame = self.__widget.create_frame_grid(right_frame,"#32213A",230,310,"flat",0,None,1,1,None,3,(15,5),(20,0),"grid")
        platform_text = game_detail["Platform"]
        
        platform_icon = self.__widget.create_frame_grid(platform_frame,"#BF932A",300,30,"flat",None,"w",0,0,None,None,None,None,"grid")
        self.__widget.create_img(platform_icon,35,30,None,r"assets\platform_icon.jpg",None,"grid","e",None,0,0,(50,0),None,None)
        self.__widget.create_label_grid(platform_icon,"Platforms",13,None,"e","#BF932A","white","left",None,None,0,1,None,"e",None,None,None)
        for i , text in enumerate(platform_text[:9],1):
            self.__widget.create_label_grid(platform_frame,f"{text}",10,None,None,"#32213A","#D1CAA1","left",None,None,i,0,2,"w",(15,0),(7,0),None)
        
        chart_ahievement = game_detail["Achievements"]
        if len(chart_ahievement) == 1 or len(chart_ahievement) == 2:
            parts1 = chart_ahievement[0].split()
            hash_icon1 = parts1[0][0]
            number1 = parts1[0][1:]

            text1 = " ".join(parts1[1:])
        else:
            parts1 =""
            hash_icon1 = ""
            number1 = ""
            text1 = ""

        achievement1_frame = self.__widget.create_frame_grid(right_frame,"#666769",200,70,"flat",0,"e",1,2,None,None,None,(20,0),"grid")
        self.__widget.create_label_grid(achievement1_frame,f"{hash_icon1} {number1}",20,None,"e","#666769","#FFD700","right",None,None,0,0,None,"e",(20,0),None,None)
        self.__widget.create_label_grid(achievement1_frame,f"{text1}",15,"underline","e","#666769","#FFD700","right",None,None,1,0,None,"e",(20,0),None,None)
        achievement1_frame.grid_propagate(False)

        if len(chart_ahievement) == 2:
            parts2 = chart_ahievement[1].split()
            hash_icon2 = parts2[0][0]
            number2 = parts2[0][1:]

            text2 = " ".join(parts2[1:])
        else:
            hash_icon2 = ""
            number2 = ""
            text2 = ""
        
        achievement2_frame = self.__widget.create_frame_grid(right_frame,"#666769",200,70,"flat",0,"e",2,2,None,None,None,(10,0),"grid")
        self.__widget.create_label_grid(achievement2_frame,f"{hash_icon2} {number2}",20,None,"e","#666769","#9FDAFF","right",None,None,0,0,None,"e",(20,0),None,None)
        self.__widget.create_label_grid(achievement2_frame,f"{text2}",15,"underline","e","#666769","#9FDAFF","right",None,None,1,0,None,"e",(20,0),None,None)

        genre_frame = self.__widget.create_frame_grid(right_frame,"#32213A",240,145,"flat",0,None,3,2,None,None,None,(10,0),"grid")
        self.__widget.create_label_grid(genre_frame,"Genre",12,None,None,"#5E17EB","white","center",25,None,0,0,2,None,None,None,None)
        genre = game_detail["Genre"]
        for i,  game_genere in enumerate(genre,2):
                if i % 2 == 0:
                    padx = (0,100)
                    color = "#BF932A"
                else:
                    padx = (5,10)
                    color = "#D1CAA1"
                self.__widget.create_label_grid(genre_frame,f"{game_genere}",10,None,None,"#32213A",color,"center",10,None,i//2,i%2,2,None,padx,(10,0),None)
        
        about_frame = self.__widget.create_frame_grid(right_frame,"#383B53",735,260,"flat",0,"w",4,0,3,None,(25,0),(15,0),"grid")
        left_about_frame = self.__widget.create_frame_grid(about_frame,"#383B53",360,260,"flat",0,"w",0,0,None,None,None,None,"grid")

        self.__widget.create_label_grid(left_about_frame,"About",14,"bold","w","#383B53","#D1CAA1","left",400,None,0,0,None,"w",(10,0),(13,0),None)
        self.__widget.create_label_grid(left_about_frame,f"{game_detail["Description"]}",12,None,"w","#383B53","#D1CAA1","left",400,None,1,0,None,"w",(10,0),None,320)
        
        right_developers_frame = self.__widget.create_frame_grid(about_frame,"#2E1B5B",420,260,"flat",0,"w",0,1,None,None,None,None,"grid")
        self.__widget.create_label_grid(right_developers_frame,"Developers",12,None,"e","#2E1B5B","white","right",15,None,0,0,2,"e",(10,100),(13,10),None)

        list_names = game_detail["Developers"]
        if len(list_names) == 0:
                index = 2 
                self.__widget.create_label_grid(right_developers_frame,"No Information Yet . .",11,None,"w","#2E1B5B","#D7DA5E","left",30,None,index//2,index%2,None,None,(50,0),(5,0),None)
        else:
            for i , name_text in enumerate(list_names[:14],2):
                if len(list_names) <= 3:
                    font_size = 9
                else:
                    font_size = 9
                text = name_text
                index = i
                if i % 2 == 0:
                    padx = (0,0) #left column
                else:
                    padx = (0,0) #right column
                self.__widget.create_label_grid(right_developers_frame,f"{text}",font_size,None,"e","#2E1B5B","#D7DA5E","right",21,None,index//2,index%2,None,"e",padx,(5,0),None)

    def get_newly_released_game(self):
        newly_released = []
        for url , game_detail in self.__game_data.items():
            if url == "https://rawg.io/":
                for game , detail in game_detail.items():
                    if str(date.today()) > detail["Release Date"]:
                        newly_released.append(game)
        return newly_released[-1]

    def get_near_release_game(self):
        near_release = []
        for url , game_detail in self.__game_data.items():
            if url == "https://rawg.io/":
                for game , detail in game_detail.items():
                    if str(date.today()) < detail["Release Date"]:
                        near_release.append(game)
        return near_release[0]
        
    def show_home(self): 
        self.__widget.clear_frames(self.frame)
        self.__window.title("Horizon | Home")

        new_released_game = self.get_newly_released_game()
        near_release = self.get_near_release_game()

        for url , game_detail in self.__game_data.items():
            if url == "https://rawg.io/":
                for game , detail in game_detail.items():
                    if game == new_released_game:
                        ilink = url
                        game_data = detail
                        newly_game_release_date = self.change_date(detail["Release Date"])
                        newly_game_name = game
                        newly_game_image = detail["Image"]
                        official_website = detail["Official Link Website"]
                    elif game == near_release:
                        jlink = url
                        game_data_upcoming = detail
                        near_release_date = self.change_date(detail["Release Date"])
                        near_game_name = game
                        near_game_image = detail["Image"]
                    
        top_bar = self.__widget.create_frame_grid(None,"#32213A",1400,40,"flat",0,"w",0,0,None,None,None,None,"pack")
        self.frame.append(top_bar)
        door = self.__widget.create_img(top_bar,140,30,None,r"assets\app_logo.png",False,"pack","ew",None,None,None,(0,0),5,None)
        door.bind("<Button-1>",lambda event: self.about_us(event))

        middle_bar = self.__widget.create_frame_grid(None,"#666769",1400,620,"flat",None,"w",1,0,None,None,None,None,"grid")
        self.frame.append(middle_bar)

        released_banner = self.__widget.create_frame_grid(middle_bar,"#000B26",1270,335,"flat",0,"w",0,0,None,None,(25,0),(15,0),"grid")#716,300
        self.__widget.create_frame_grid(middle_bar,"black",4,335,"flat",None,"w",0,1,None,None,(17,0),(15,0),None)

        image_banner = self.__widget.create_frame_grid(released_banner,"yellow",710,335,"flat",None,"w",0,0,None,None,None,None,"grid")
        self.__widget.create_img(image_banner,725,365,None,rf"{newly_game_image}",False,"grid",None,None,0,0,None,None,None)
 
        description_banner = self.__widget.create_frame_grid(released_banner,"#000B26",560,335,"flat",None,"w",0,1,None,None,None,None,"grid")
        notification = self.__widget.create_frame_grid(description_banner,"#000B26",560,70,"flat",None,"w",0,0,None,None,None,None,"grid")
        self.__widget.create_img(notification,100,50,None,r"assets\new_notification.jpg",False,"grid","w",None,0,0,(20,0),(15,0),None)
        self.__widget.create_label_grid(notification,f"{newly_game_release_date}",19,None,None,"#000B26","#BF932A",None,None,None,0,1,None,None,(35,0),(10,0),None)

        game_name_banner = self.__widget.create_frame_grid(description_banner,"#000B26",560,140,"flat",None,"w",1,0,None,None,None,None,"grid")
        self.__widget.create_label_grid(game_name_banner,newly_game_name,25,None,"w","#000B26","white","left",500,None,0,0,None,"w",(20,0),(10,0),300)

        button_banner = self.__widget.create_frame_grid(description_banner,"#000B26",520,120,"flat",None,"w",2,0,None,None,(20,0),None,"grid")
        where_to_get = self.__widget.create_img(button_banner,160,55,None,r"assets\get_button.jpg",False,"grid","w",None,0,0,(70,0),(20,0),None)
        where_to_get.bind("<Button-1>",lambda event: self.__widget.on_click_official(official_website))
        
        view = self.__widget.create_img(button_banner,162,55,None,r"assets\view_button.jpg",False,"grid","w",None,0,1,(65,0),(20,0),None)
        view.bind("<Button-1>",lambda event: self.show_game_description(newly_game_name,game_data,ilink,wheres="home"))
        
        release_banner = self.__widget.create_frame_grid(middle_bar,"#666769",1270,230,"flat",None,"w",1,0,None,None,(25,0),(15,0),"grid")

        platform_buttons = self.__widget.create_frame_grid(release_banner,"#666769",396,175,"flat",None,"w",0,0,None,None,None,20,"grid")

        images = [r"assets\pc_platform.jpg",r"assets\ps5_platform.jpg",r"assets\xbox_platform.jpg",r"assets\apple_platform.jpg",r"assets\android_platform.jpg"]
        page_url = ["https://rawg.io/games/pc","https://rawg.io/games/playstation5","https://rawg.io/games/xbox-one","https://rawg.io/games/ios","https://rawg.io/games/android"]
        
        footer = self.__widget.create_frame_grid(None,"#000B26",1400,40,"flat",None,"w",2,0,None,None,None,None,"grid")
        platform_name = self.__widget.create_label_grid(footer,"PLATFORMS",17,None,"center","#000B26","white","left",20,None,0,0,None,"nsew",(80,0),(1,0),None)
        self.__widget.create_label_grid(footer,"RELEASES",17,None,"center","#000B26","white","left",None,None,0,1,None,"nsew",(170,0),(1,0),None)
        self.frame.append(footer)

        i = 0
        for img , page_url in zip(images,page_url):
            if i % 3 == 0:
                padx = (30,20) #Left Side
            elif i % 3 == 1:
                padx = 40 #Middle
            elif i % 3 == 2:
                padx = (20,10) #right side
            if i == 0 or i == 1 or i == 2:
                pady = (0,27)
            button_platforms = self.__widget.create_img(platform_buttons,75,75,None,img,False,"grid","w",None,i//3,i%3,padx,pady,None)
            button_platforms.bind("<Button-1>",lambda event,url = page_url,search = None:self.show_games_list(url,search,where="platform"))
            button_platforms.bind("<Enter>",lambda event,image = img,plat_label = platform_name: self.__widget.home_platform_button_enter(event,image,plat_label))
            button_platforms.bind("<Leave>",lambda event,original_image = img,plat_label = platform_name: self.__widget.home_platform_button_leave(event,original_image,plat_label))
            i +=1
          
        self.__widget.create_frame_grid(release_banner,"black",4,230,"flat",None,"w",0,1,None,None,26,None,None)

        schedule_buttons = self.__widget.create_frame_grid(release_banner,"#666769",246,230,"flat",None,"w",0,2,None,None,(0,13),None,"grid")

        upcoming = self.__widget.create_frame_grid(schedule_buttons,"#666769",246,90,"flat",None,"w",0,0,None,None,None,(0,25),"grid")
        upcoming_games = self.__widget.create_img(upcoming,249,90,None,r"assets\unselected_upcoming_games.jpg",False,"grid","w",None,0,0,None,None,None) #Bind This
        upcoming_games.bind("<Button-1>",lambda event,url = "https://rawg.io/",search = None: self.show_games_list(url,search,where="upcoming"))

        available = self.__widget.create_frame_grid(schedule_buttons,"#666769",246,90,"flat",None,"w",1,0,None,None,None,(25,0),"grid")
        available_games = self.__widget.create_img(available,249,90,None,r"assets\unselected_available_games.jpg",False,"grid","w",None,0,0,None,None,None) #Bind This
        available_games.bind("<Button-1>",lambda event,url = "https://rawg.io/",search = None: self.show_games_list(url,search,where="available"))


        release_game_banner = self.__widget.create_frame_grid(release_banner,"#060035",560,220,"flat",None,"e",0,3,None,None,None,(0,10),"grid")

        img_release = self.__widget.create_frame_grid(release_game_banner,"#060035",280,220,"flat",None,"w",0,0,None,None,None,None,"grid")
        self.__widget.create_img(img_release,350,220,None,rf"{near_game_image}",False,"grid","W",None,0,0,None,None,None)

        img_release_description = self.__widget.create_frame_grid(release_game_banner,"#060035",280,220,"flat",None,"w",0,1,None,None,None,None,"grid")
        notification_soon = self.__widget.create_frame_grid(img_release_description,"#060035",265,45,"flat",None,"w",0,0,None,None,(10,0),None,"grid")
        self.__widget.create_img(notification_soon,100,37,None,r"assets\soon_notification.jpg",False,"grid","W",None,0,0,None,(9,0),None)
        self.__widget.create_label_grid(notification_soon,f"{near_release_date}",13,None,None,"#060035","#BF932A",None,None,None,0,1,None,None,(30,0),(7,0),None)

        img_release_game_name = self.__widget.create_frame_grid(img_release_description,"#060035",280,100,"flat",None,"w",1,0,None,None,(10,0),(2,0),"grid")
        self.__widget.create_label_grid(img_release_game_name,near_game_name,18,None,"w","#060035","white","left",500,None,0,0,None,"w",None,(10,0),270)

        view_more = self.__widget.create_frame_grid(img_release_description,"#060035",280,40,"flat",None,"w",2,0,None,None,(10,0),(20,0),"grid")
        view_more_button = self.__widget.create_img(view_more,100,40,None,r"assets\view_more_home_unselected.jpg",False,"grid","W",None,0,0,(100,0),(2,0),None)
        view_more_button.bind("<Button-1>",lambda event:self.show_game_description(near_game_name,game_data_upcoming,jlink,wheres="home"))
        view_more_button.bind("<Enter>",lambda event: self.__widget.home_view_more_enter(event))
        view_more_button.bind("<Leave>",lambda event:self.__widget.home_view_more_leave(event))
        
        self.__widget.create_frame_grid(middle_bar,"black",4,230,"flat",None,"w",1,1,None,None,(17,0),(15,0),None)

    def about_us(self,event):
        self.__widget.clear_frames(self.frame)
        gif_frame = self.__widget.create_frame_pack(None,None,1000,1000,None,0,None,"both","grid")
        self.__widget.create_img_gif(gif_frame,r"assets\about_us_bg_image.gif",self.__window)

        self.__window.title("Horizon | About Us")

        about_us_header = self.__widget.create_frame_grid(gif_frame,"#000B26",230,42,"flat",0,"w",0,0,None,None,167,(18,0),"grid")
        self.__widget.create_img(about_us_header,230,43,None,r"assets\about_us_banner.jpg",False,"grid","w",None,0,0,None,2,None)

        self.__widget.create_frame_grid(gif_frame,"#8C52FF",276,6,"flat",0,"w",1,0,None,None,167,None,None)

        app_about = self.__widget.create_frame_grid(gif_frame,"#000B26",276,274,"flat",5,"w",2,0,None,None,167,(13,0),"grid")
        self.__widget.create_img(app_about,163,32,None,r"assets\horizon_meow.jpg",None,"grid","w",None,0,0,20,(10,0),None)
        self.__widget.create_img(app_about,240,150,None,r"assets\app_description.jpg",False,"grid","w",None,1,0,(12,0),(8,0),None)

        self.__widget.create_frame_grid(gif_frame,"#8C52FF",276,6,"flat",0,"w",3,0,None,None,167,(15,0),None)

        developer_header = self.__widget.create_frame_grid(gif_frame,"#000B26",415,51,"flat",5,"w",4,0,None,None,32,(14,0),"grid")
        self.__widget.create_img(developer_header,170,30,None,r"assets\app_developer_header1.jpg",False,"grid","w",None,0,0,10,4,None)
        self.__widget.create_img(developer_header,130,30,None,r"assets\app_developer_header2.jpg",False,"grid","w",None,0,1,(12,0),4,None)

        developer_names = self.__widget.create_frame_grid(gif_frame,"#000B26",415,225,"flat",5,"w",5,0,None,None,32,(12,0),"grid")
        self.__widget.create_img(developer_names,67,67,None,r"assets\developer_rey.jpg",False,"grid","w",None,0,0,(30,0),(15,0),None)
        self.__widget.create_img(developer_names,155,20,None,r"assets\dev1_name.jpg",False,"grid","w",None,0,1,(20,0),(16,0),None)

        self.__widget.create_img(developer_names,67,67,None,r"assets\developer_vince.jpg",False,"grid","w",None,1,0,(30,0),(35,0),None)
        self.__widget.create_img(developer_names,210,20,None,r"assets\dev2_name.jpg",False,"grid","w",None,1,1,(20,0),(36,0),None)
        
    def run(self):
        self.__widget.change_window_icon(self.__window)
        self.show_home()
        self.__window.mainloop()
        #self.test()
            
if __name__ == "__main__":
    app = GameScheduleUI()
    app.run()
