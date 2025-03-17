#project_python_2
#project written in python for a search medicine app
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import time
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from AppOpener import open
import requests
from bs4 import BeautifulSoup
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from rembg import remove
from PIL import Image
import easyocr
from pylab import rcParams
from IPython.display import Image as new

#With Builder.Loader_string we gonna create our pages of teh app
#MyScreenManager will manage the screen
#after we create each page,for the moment they are only 2 SearchPage and MenuPage so the user will search with the appp and manage
#it's functionality
#inside the pages we gonna use the Boxlayout library to specify our buttons about size and position 
#with the Button library we gonna add the buttons and make them funtional for the next page,for the camera interaction,to save the photos locally,if we stay in the same page
#and we use the same button we stay in the same page and search for the medicine that we want to find,we also put a text on the buttons so they can be clear (all of these in SearchPage)
#in the second page (MenuPage) we create Labels that will assist the user about the app functionality,we give the user the opportunity to return back to the previous page
#we let the user to search photos from the gallery or the file manager
#all of them only with kivy language style not python way
Builder.load_string("""
<MyScreenManager>:
    SearchPage:
        name: "search"
    MenuPage:
        name: "menu"
    ResultPage:
        name: "result"

<SearchPage>:
    BoxLayout:
                          
        orientation: 'vertical'                
        TextInput:
            id: text_user
            hint_text:'Give the name of medicine'
            size_hint_x: 0.6
            size_hint_y: 0.1
            multiline: False 
        Label:
            text: "type a medicine"
            id:label
            size_hint_y: None
            height: '48dp'
        Button:
            text: "Search"
            id: button_search
            size_hint_x: 0.2
            size_hint_y: 0.1
            pos_hint_x: 0.1
            pos_hint_y: 0.1
            on_press: root.search_data()
            on_release:
                app.root.current = "result"
            
        Button:
            text: "Menu"
            size_hint_x: 0.2
            size_hint_y: 0.1
            pos_hint_x: 0.2
            pos_hint_y: 0.2
            on_release:
                app.root.current = "menu"
                    
        Camera:
            id: camera
            resolution: (640, 480)
            play: False
        ToggleButton:
            text: 'Play'
            on_press: camera.play = not camera.play
            size_hint_y: None
            height: '48dp'
        Button:
            text: 'save locally'
            size_hint_y: None
            height: '48dp'
            on_press: root.locally()
        Button:
            text: "search the taken photo"
            size_hint_y: None
            height: '48dp'
            on_press: 
                root.search_photo()
                app.root.current = "result"
            

<MenuPage>:
    
    BoxLayout:
        
        orientation: 'vertical'
                    
        Label:
            text: 'photos from drive'
            size_hint_center_x: 0.25
            size_hint_center_y: 0.17
            pos_hint_center_x: 0.13         
            pos_hint_center_y: 0.15
        Button:
            text: 'drive'
            size_hint_y: None
            height: '48dp'
            on_press: 
                root.explorer()
                app.root.current = "result"                                  
                                       
        Label:
            text: 'information for the medicine'
            size_hint_center_x: 0.3
            size_hint_center_y: 0.2
            pos_hint_center_x: 0.2           
            pos_hint_center_y: 0.2
                    
                    
        Label:
            text: "where it's been used"
            size_hint_center_x: 0.3
            size_hint_center_y: 0.2
            pos_hint_center_x: 0.2           
            pos_hint_center_y: 0.2
        
        Label:
            text: 'side effects'
            size_hint_center_x: 0.3
            size_hint_center_y: 0.2
            pos_hint_center_x: 0.2           
            pos_hint_center_y: 0.2

        Button:
            text: "Search"
            size_hint_center_x: 0.5
            size_hint_center_y: 0.5
            pos_hint_center_x: 0.4           
            pos_hint_center_y: 0.4
            on_release:
                app.root.current = "search"
                    
<ResultPage>:
    BoxLayout:
        Label:
            text: ""
            id: medicine_results
        Button:
            text: "show results"
            size_hint_x: 0.2
            size_hint_y: 0.1
            pos_hint_x: 0.2
            pos_hint_y: 0.2
            on_press: root.med_results()
        Button:
            text: "back"
            size_hint_x: 0.2
            size_hint_y: 0.1
            pos_hint_x: 0.2
            pos_hint_y: 0.2
            on_release:
                app.root.current = "search"    
            
                       
    """
)
#we create the label_results and it will be global in order to transfer the data from the def search to the next page without returning them,in order to avoid the error that it occurs
label_results=""
photo="IMG_{}.png"
date=""
data_ocr_transfer=""
folder=""
#we create our classes were we use the Screeen library in order to use our screen
class SearchPage(Screen):
    #We create a function named locally to capture the images and give them the names
    #according to their captured time and date and storing the locally.
    def locally(self):
        global folder
        folder=askdirectory()
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("{}/IMG_{}.png".format(folder,timestr))
        global date
        date=timestr
    #the second function named search_data is created to search the medicine that the user typed 
    def search_data(self):
        #the medicine takes the data that are stored in the Textinput
        medicine=self.ids['text_user']
        user= medicine.text
        #we take our global label_results
        global label_results
        if user == "":
            #we change the text of the label if the user search accidentaly an empty textinput
            txt='No medicine was given'
            error_handling=self.ids.label
            error_handling.text=txt
            label_results=txt
        else:
            url=("https://www.galinos.gr/web/drugs/main/drugs/{}".format(user))
            #we format the data to the url in order to search the medicine
            r = requests.get(url)
            if r.status_code == 200:
                #we do an api request to the website
                htmldata=r.text
                #with htmldata we take the results from the request and we make them a text
                soup = BeautifulSoup(htmldata, 'html.parser') 
                s_1 = soup.find('div', class_='container-lg my-4')
                copy_data=""
                data_1=""
                for data_1 in s_1.find_all("p"):  
                    copy_data+=data_1.get_text()
                label_results=str(copy_data)
            else:
                #we change the text of the lebel if the respond is different from 200
                txt='maybe you mistyped the medicine'
                error_handling=self.ids.label
                error_handling.text=txt
                label_results=txt
    def search_photo(self):
        #with the search_photo function we crop the current photo that we took
        global folder
        path=folder
        global photo
        global date
        photo="{}/IMG_{}.png".format(path,date)
        image_input=Image.open(photo)
        outpout=remove(image_input)
        output_path="{}/photo_sample.png".format(path)
        outpout.save(output_path)
        #we open the new croped photo for the letter recognition
        rcParams['figure.figsize'] = 8,16
        Reader = easyocr.Reader(['en'])
        new(output_path)
        output_photo = Reader.readtext(output_path)
        global data_ocr_transfer
        global label_results
        data_ocr_transfer=output_photo[0][1]
        url=("https://www.galinos.gr/web/drugs/main/drugs/{}".format(data_ocr_transfer))
        #we format the data to the url in order to search the medicine
        r = requests.get(url)
        if r.status_code == 200:
            #we do an api request to the website
            htmldata=r.text
            #with htmldata we take the results from the request and we make them a text
            soup = BeautifulSoup(htmldata, 'html.parser') 
            s_1 = soup.find('div', class_='container-lg my-4')
            copy_data=""
            data_1=""
            for data_1 in s_1.find_all("p"):  
                copy_data+=data_1.get_text()
            label_results=str(copy_data)
        else:
            label_results="The data from the photo must be unclear,or a problem with the search"
           
class ResultPage(Screen):
    def med_results(self):
        #we show the data with a specific way in oreder to avoid failure in the app,we won't use any library,we want full managment by us
        results=self.ids.medicine_results
        copy=""
        start=0
        end=60
        number=len(label_results)
        n=0
        #every 60 characters we change a new line
        if number==60:
            while n <= number//60:
                n+=1
                for i in range(start,end):
                    copy+=label_results[i]
                copy+="\n"
                start+=60
                end+=60
        elif number <60:
            for i in range(0,len(label_results)):
                copy+=label_results[i]
        elif number>60 and number%60!=0:
            while n < number//60:
                n+=1
                for i in range(start,end):
                    copy+=label_results[i]
                copy+="\n"
                start+=60
                end+=60
            end=n*60
            for i in range (end,len(label_results)):
                copy+=label_results[i]
        elif number>60 and number%60==0:
            while n <= number//60:
                n+=1
                for i in range(start,end):
                    copy+=label_results[i]
                copy+="\n"
                start+=60
                end+=60
        #we put the new whole copy string to the label
        results.text=copy
               
class MenuPage(Screen):
    #with the function explorer we open the app named explorer so the user will search for the photo
    def explorer(self):
        filename = askopenfilename()
        folder=askdirectory()
        #the filename returns the path of a file and more specificaly the path of the photo for the letter recognition
        if filename =="":
            pass
        else:
            #we crop the photo that was given
            image_input=Image.open(filename)
            outpout=remove(image_input)
            output_path="{}/photo_sample.png".format(folder)
            outpout.save(output_path)
            #we open the new croped photo for the letter recognition
            rcParams['figure.figsize'] = 8,16
            Reader = easyocr.Reader(['en'])
            new(output_path)
            output_photo = Reader.readtext(output_path)
            global data_ocr_transfer
            data_ocr_transfer=output_photo[0][1]
            global label_results
            url=("https://www.galinos.gr/web/drugs/main/drugs/{}".format(data_ocr_transfer))
            #we format the data to the url in order to search the medicine
            r = requests.get(url)
            if r.status_code == 200:
                #we do an api request to the website
                htmldata=r.text
                #with htmldata we take the results from the request and we make them a text
                soup = BeautifulSoup(htmldata, 'html.parser') 
                s_1 = soup.find('div', class_='container-lg my-4')
                copy_data=""
                data_1=""
                for data_1 in s_1.find_all("p"):  
                    copy_data+=data_1.get_text()
                label_results=str(copy_data)
            else:
                label_results="The data from the photo must be unclear,or a problem with the search"


#we create our class which will manage the screen for the pages from before
class MyScreenManager(ScreenManager):
    pass        

#we create our app's class with the App library to create our app functional and ready to be used
class MyApp(App):
    #we build our app 
    def build(self):
        return MyScreenManager()
    
#we run our app
if __name__=="__main__":
    MyApp().run()
