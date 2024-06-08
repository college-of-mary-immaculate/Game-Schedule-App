import tkinter as tk
from PIL import Image,ImageTk
import webbrowser


class WidgetGenerator:
    def __init__(self): 
        self.__photos = [] #For instance of Photo

    def change_window_icon(self,root):
        icon_image = Image.open(r"horizon_icon.ico")
        resized_icon = icon_image.resize((48,48))
        icon = ImageTk.PhotoImage(resized_icon)
        root.iconphoto(True,icon)


    def create_label_pack(self,frame,text,font_size,justify,bg,fg,width,height,side,fill,anchor,x,y,wraplength):
        label = tk.Label(frame,text=text,font=("Verdana",font_size),fg=fg,justify=justify,width=width,height=height,bg=bg,wraplength=wraplength)
        label.pack(side=side,fill=fill,anchor=anchor,padx=x,pady=y)
        return label
    
    def create_label_grid(self,frame,text,font_size,style,anchor,bg,fg,justify,width,height,row,column,colspan,sticky,x,y,wrap):
        if style:
            label = tk.Label(frame,text=text,font=("Verdana",font_size,style),fg=fg,anchor=anchor,justify=justify,width=width,height=height,bg=bg,wraplength=wrap)
        else:
            label = tk.Label(frame,text=text,font=("Verdana",font_size),fg=fg,anchor=anchor,justify=justify,width=width,height=height,bg=bg,wraplength=wrap)

        label.grid(row = row,column=column,columnspan= colspan,sticky=sticky,padx=x,pady=y)
        return label
    
    def create_button_pack(self,frame,image_name,border,text,fg,bg,side,font_size,relief,width,height,x,y,command_function):
        if image_name:
            img = Image.open(image_name)
            resize_img = img.resize((80,25))
            image = ImageTk.PhotoImage(resize_img)
            self.__photos.append(image)
            original_image = image
        else:
            image = None

        if border:
            w = 50
            color = "#9D7DE6"
        else:
            w = 0
            color = None

        button = tk.Button(frame,image = image,highlightbackground=color,highlightthickness=w,text=text,fg=fg,bg=bg,relief=relief,font=("Verdana",font_size),width = width,height=height,command=command_function)
        button.pack(side=side,padx=x,pady=y)
        
        if image_name:
            button.bind("<Enter>",lambda event = button: self.hover_button_enter_pack(event))
            button.bind("<Leave>",lambda event = button,images = original_image: self.hover_button_leave_pack(event,images))
        return button

    def hover_button_enter_pack(self,event):
        image = r"assets\open_back.jpg"
        image_icon = Image.open(image)
        resized_selected_img = image_icon.resize((80,25))
        open_image = ImageTk.PhotoImage(resized_selected_img)
        self.__photos.append(open_image)
        event.widget["image"] = open_image

    def hover_button_leave_pack(self,event,original_image):
        event.widget["image"] = original_image

    def create_button_grid(self,frame,image_name,text,compound,fg,bg,sticky,font_size,relief,anchor,width,height,row,column,colspan,x,y,command_function):
        if image_name:
            unselected_img = Image.open(image_name)
            resized_unselected_image = unselected_img.resize((50,50))
            unselected_img_image = ImageTk.PhotoImage(resized_unselected_image)
            self.__photos.append(unselected_img_image)
            image = unselected_img_image
            original_image = unselected_img_image
            padx_img = 50
        else:
            image = image_name #None
            padx_img = None
        button = tk.Button(frame,image=image,text=text,compound=compound,fg=fg,bg=bg,relief=relief,font=("Verdana",font_size),anchor=anchor,width = width,height=height,padx=padx_img,command=command_function)
        button.grid(sticky=sticky,row = row , column = column, columnspan=colspan,padx=x,pady=y)
        if image_name:
            button.bind("<Enter>",lambda event = button,button_text=text: self.hover_button_enter(event,button_text))
            button.bind("<Leave>",lambda event = button,origin_img = original_image: self.hover_button_leave(event,origin_img))
        return button
    
    def hover_button_enter(self,event,text):

        platform = {"PC":r"assets\pc_selected_icons.jpg","PS5":r"assets\ps5_selected_icons.jpg","XBOX":r"assets\xbox_selected_icons.jpg","IOS":r"assets\ios_selected_icons.jpg","ANDROID":r"assets\android_selected_icons.jpg"}
        for platform , img in platform.items():
            if text == platform:
                image = img  
        image_icon = Image.open(image)
        resized_selected_img = image_icon.resize((50,50))
        selected_img = ImageTk.PhotoImage(resized_selected_img)
        self.__photos.append(selected_img)

        event.widget["foreground"] = "#32213A"
        event.widget["background"] = "#D1CAA1"
        event.widget["image"] = selected_img

    def hover_button_leave(self,event,image):
        event.widget["foreground"] = "white"
        event.widget["image"] = image
        event.widget["background"] = "#383B53"

    def create_entry_pack(self,frame,font_size,bg,justify,width,x,y):
        entry = tk.Entry(frame,font=(None,font_size),justify=justify,bg=bg,width=width)
        entry.pack(padx=x,pady=y)
        return entry
    
    def create_entry_grid(self,frame,font_size,bg,justify,width,row,column,colspan,sticky,x,y):
        entry = tk.Entry(frame,font=(None,font_size),justify=justify,bg=bg,width=width)
        entry.grid(row = row,column = column,columnspan= colspan,sticky = sticky,padx=x,pady=y)
        return entry
    
    def clear_frames(self,frames):
        for frame in frames:
            frame.destroy()
    
    def enter_official_hover(self,event,image,image_path):
        if r"assets\cart1_unselected_unreleased_icon.jpg" == image_path:
            image_cart = r"assets\cart1_selected_unreleased_icon.jpg"
            size = (160,175)
        else:
            image_cart = r"assets\cart2_selected_released_icon.jpg"
            size = (160,175)
        if r"assets\unselected_upcoming_page.jpg" == image_path:
            image_cart = r"assets\selected_upcoming_page.jpg"
            size = (325,231)
            

        image_icon = Image.open(image_cart)
        resized_selected_img = image_icon.resize(size)
        selected_img = ImageTk.PhotoImage(resized_selected_img)
        self.__photos.append(selected_img)

        image["image"] = selected_img

    def leave_official_hover(self,event,image,origin):
        image_origin = Image.open(origin)
        if r"assets\unselected_upcoming_page.jpg" == origin:
            resized_origin = image_origin.resize((325,231))
        else:
            resized_origin = image_origin.resize((160,175))
        original_photo = ImageTk.PhotoImage(resized_origin)
        self.__photos.append(original_photo)
        image["image"] = original_photo
        
    def on_click_official(self,url): #Official Website Link
        webbrowser.open_new(url)
        
    def create_img(self,frame,width,height,bg,file_path,border,layout,sticky,colspan,row,column,x,y,rspan):
        image = Image.open(file_path)
        if border:
            border_width = 20
            border_color = "#383B53"
            calculate_border_width = image.width + 2 * border_width #calculate for border width
            calculate_border_hieght = image.height + 2 * border_width
            bordered_image = Image.new(image.mode,(calculate_border_width,calculate_border_hieght),border_color)
            bordered_image.paste(image,(border_width,border_width))
            resized_image = bordered_image.resize((width,height)) #With Border
        else:
            resized_image = image.resize((width,height)) #Without Border

        photo = ImageTk.PhotoImage(resized_image)
        self.__photos.append(photo)
        

        photo_label = tk.Label(frame,image=photo,bg=bg,borderwidth=0)
        if layout == "pack":
            photo_label.pack(padx=x,pady=y)
        elif layout == "grid":
            photo_label.grid(sticky=sticky,row=row,column = column ,columnspan=colspan,rowspan=rspan,padx=x,pady=y) #Table Frame Header
        
        return photo_label

    def create_frame_pack(self,another_frame,bg,width,height,relief,borderwidth,side,fill,propagate):
        if borderwidth:
            color = "#8C52FF"
        else:
            color = None
        frame = tk.Frame(another_frame,bg=bg,width=width,height=height,relief = relief,highlightbackground=color,borderwidth=borderwidth)
        frame.pack(side=side,fill=fill)
        if propagate == "pack":
            frame.pack_propagate(False)
        elif propagate == "grid":
            frame.grid_propagate(False)
        return frame
    
    def create_frame_grid(self,another_frame,bg,width,height,relief,borderwidth,sticky,row,column,colspan,rspan,x,y,propagate):
        if borderwidth:
            color = "#9D7DE6"
        else:
            color = None
        frame = tk.Frame(another_frame,bg=bg,width=width,height=height,relief=relief,highlightthickness=borderwidth,highlightbackground=color,highlightcolor=color)
        frame.grid(sticky=sticky,row=row,column=column,columnspan=colspan,rowspan=rspan,padx=x,pady=y)
        if propagate == "pack":
            frame.pack_propagate(False)
        elif propagate == "grid":
            frame.grid_propagate(False)
        return frame

    def view_button_search_enter(self,event):
        image = r"assets\searched_veiw_more_selected.jpg"
        image_icon = Image.open(image)
        resized_selected_img = image_icon.resize((126,40))
        img = ImageTk.PhotoImage(resized_selected_img)
        self.__photos.append(img)
        event.widget["image"] = img

    def view_button_search_leave(self,event,image):
        image_icon = Image.open(image)
        resized_selected_img = image_icon.resize((126,40))
        original_img = ImageTk.PhotoImage(resized_selected_img)
        self.__photos.append(original_img)
        event.widget["image"] = original_img


    def create_table(self,canva_bg,url):
        canvas = tk.Canvas(bg="#383B53",highlightbackground="#666769")
        scrollbar = tk.Scrollbar(orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left",fill="both",expand=True)
        scrollbar.pack(side="right",fill="both")

        table_frame = tk.Frame(canvas,bg=canva_bg,width=100,height=100)
        banner = {"https://rawg.io/":r"assets\upcoming_banner.jpg","https://rawg.io/games/pc":r"assets\pc_banner.jpg","https://rawg.io/games/playstation5":r"image/ps5_banner.jpg","https://rawg.io/games/xbox-one":r"assets\xbox_banner.jpg","https://rawg.io/games/ios":r"assets\ios_banner.jpg","https://rawg.io/games/android":r"assets\android_banner.jpg"}
        for banner_image,image_url in banner.items():
            if url == banner_image and banner_image == "https://rawg.io/":
                image = image_url
                padx = (57,0)
            elif url == banner_image:
                image = image_url
                padx = (50,0)
                
        self.create_img(table_frame,970,180,"#666769",f"{image}",False,"grid","ns",3,None,None,padx,(20,0),None)
       
        widget = [canvas,table_frame,scrollbar]
        return widget
    

    def create_cell(self,index,canvas,table_frame,reason,type): 
        if index % 3 == 1: # Middle cell Padx
            padx = 10
        elif index % 3 == 0: #Left cell Padx
            padx=(100,70)
        elif index % 3 == 2: # Right cell padx
            padx=(70,145)
        
        table_element = {"show_all":{"List":{"cell_width":220,"cell_height":330,"cell_bg":"#32213A","padx":padx,"pady":25,"row_index":index // 3,"column_index":index % 3},"bottomspace":{"cell_width":220,"cell_height":25,"cell_bg":"#666769","padx":padx,"pady":25,"row_index":index // 3,"column_index":index % 3}},
                         "searched":{"List":{"cell_width":440,"cell_height":380,"cell_bg":"#32213A","padx":(290,200),"pady":25,"row_index":index,"column_index":0},"bottomspace":{"cell_width":400,"cell_height":25,"cell_bg":"#666769","padx":(290,200),"pady":25,"row_index":index,"column_index":0}},
                         "not_found":{"404":{"cell_width":765,"cell_height":270,"cell_bg":"#32213A","padx":(175,200),"pady":(30,70),"row_index":index,"column_index":0},"bottomspace":{"cell_width":400,"cell_height":30,"cell_bg":"#666769","padx":(175,200),"pady":(30,70),"row_index":index,"column_index":0}}
                         }
        
        cell_appearance = table_element[type][reason]

        cell_frame = tk.Frame(table_frame,width=cell_appearance["cell_width"],height=cell_appearance["cell_height"],bg=cell_appearance["cell_bg"],relief=None)
        cell_frame.grid(row=cell_appearance["row_index"],column=cell_appearance["column_index"],padx=cell_appearance["padx"],pady=cell_appearance["pady"]) #Calculating the Example: lets say the index is 0 ( index // 0 = 0 ,column 0 % 3 = 0 so grid(0,0)) 3 can be represented as how many cell in a line
        if type == "show_all":
            cell_frame.propagate(False)
        else:
            cell_frame.grid_propagate(False)

        table_frame_id = canvas.create_window((0,0),window=table_frame,anchor="nw")
      
        table_frame.update_idletasks()  # Update table_frame to calculate cell size
        canvas.config(scrollregion=canvas.bbox("all"))  # Update canvas scroll region
        return cell_frame

    def enter_hover_frame(self,event, frame,label,date,image,top):
        frame["height"] += 72
        frame["background"] = "#383B53"
        label.config(bg="#383B53")
        image["background"] = "#383B53"
        top["height"] -=1
        if date == "2025-09-05":
            release_date = "TBA"
        else:
            release_date = date
        self.date_label = self.create_label_pack(frame,f"____________________\n\nRelease Date:\n{release_date}",10,"left","#383B53","white",None,None,None,None,"w",12,(0,0),None)
        

    def leave_hover_frame(self, event,frame,label,image,top):
        frame["height"] -= 72
        frame["background"] = "#32213A"
        label.config(bg="#32213A")
        image["background"] =  "#32213A"
        top["height"] +=1
        self.date_label.destroy()

    def create_cell_bar_graph(self,frame,text,max_width,max_value,cell_width,cell_height,value,index,pady,canva_bg):
        if text == "Exceptional":
            fill_color = "#32620E"
        elif text == "Recommended":
            fill_color = "#5E17EB"
        elif text == "Meh":
            fill_color = "#C85103"
        elif text == "Skip":
            fill_color = "#FF0000"

        canvas_graph = tk.Canvas(frame,width = cell_width,height=cell_height,borderwidth=0,highlightbackground=canva_bg,relief="flat",bg=canva_bg)
        canvas_graph.grid(row=index,column=1,padx=5,pady=pady)

        if value !=0:
            bar_width = (value / max_value) * max_width
        else:
            bar_width = 0

        x0 = cell_width - bar_width - 10 #padx 0
        y0 = (cell_height - 20) / 2 #pady 0
        x1 = x0 + bar_width 
        y1 = y0 + 20
        canvas_graph.create_rectangle(x0,y0,x1,y1,fill=fill_color,outline="")
        canvas_graph.create_text(cell_width / 2,(y0 + y1) / 2,font=("Verdana",13),text=value,anchor="center",fill="white")

        return canvas_graph

    def create_img_gif(self,frame,img,root_name):
        label_gif = tk.Label(frame,bg="white",border=0,highlightthickness=0)
        label_gif.pack()
        
        self.gif_global_root = root_name

        gif_image = img
        gif_frames = self.get_frames(rf"{gif_image}")

        self.gif_global_root.after(100,self.play_gif,label_gif,gif_frames)

        return label_gif

    def get_frames(self,img):
        with Image.open(img) as gif:
            index = 0
            frames = []
            while True:
                try:
                    resized_gif = gif.resize((1360,700))
                    gif.seek(index)
                    frame = ImageTk.PhotoImage(resized_gif)
                    frames.append(frame)
                except EOFError:
                    break
                index +=1
            return frames
        
    def play_gif(self,label,frames):
        total_delay = 50
        delay_frames = 30
        for frame in frames:
            self.gif_global_root.after(total_delay,self.next_frame,frame,label,frames)
            total_delay +=delay_frames
        self.gif_global_root.after(total_delay,self.next_frame,frame,label,frames,True)

    def next_frame(self,frame,label,frames,restart=False):
        if restart:
            self.gif_global_root.after(1,self.play_gif,label,frames)
            return
        label.config(image=frame)

    def home_platform_button_enter(self,event,image,platform):

        home_plat_icons = {r"assets\pc_platform.jpg":{"image":r"assets\pc_platform_selected.jpg","name":"PC"},
                           r"assets\ps5_platform.jpg":{"image":r"assets\ps5_platform_selected.jpg","name":"PLAYSTATION 5"},
                           r"assets\xbox_platform.jpg":{"image":r"assets\xbox_platform_selected.jpg","name":"XBOX"},
                           r"assets\apple_platform.jpg":{"image":r"assets\ios_platform_selected.jpg","name":"IOS"},
                           r"assets\android_platform.jpg":{"image":r"assets\android_platform_selected.jpg","name":"ANDROID"}
                           }
     
        img = home_plat_icons[image]["image"]
        text = home_plat_icons[image]["name"]
        image_icon = Image.open(img)
        resized_selected_img = image_icon.resize((75,75))
        img_plat = ImageTk.PhotoImage(resized_selected_img)
        self.__photos.append(img_plat)

        event.widget["image"] = img_plat
        platform["text"] = text

    def home_platform_button_leave(self,event,original_image,platform):
        image_icon = Image.open(original_image)
        resized_selected_img = image_icon.resize((75,75))
        img_plat = ImageTk.PhotoImage(resized_selected_img)
        self.__photos.append(img_plat)

        event.widget["image"] = img_plat
        platform["text"] = "PLATFORM"

    def home_view_more_enter(self,event):
        img = r"assets\view_button_home_selected.jpg"
        image_icon = Image.open(img)
        resized_selected_img = image_icon.resize((100,40))
        img_view_icon = ImageTk.PhotoImage(resized_selected_img)
        self.__photos.append(img_view_icon)

        event.widget["image"] = img_view_icon

    def home_view_more_leave(self,event):
        img = r"assets\view_more_home_unselected.jpg"
        image_icon = Image.open(img)
        resized_selected_img = image_icon.resize((100,40))
        img_view_icon = ImageTk.PhotoImage(resized_selected_img)
        self.__photos.append(img_view_icon)

        event.widget["image"] = img_view_icon


if __name__ == "__main__":
    widget = WidgetGenerator()
  