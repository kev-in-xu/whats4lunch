import re
from datetime import datetime
from flask import render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
import webbrowser
import threading

# figure out where the dining information comes from

from flask import Flask
app = Flask(__name__)
urlList = ["https://dining.columbia.edu/content/faculty-house-0",
           "https://dining.columbia.edu/content/jjs-place-0",
           "https://dining.columbia.edu/chef-mikes",
           "https://dining.columbia.edu/content/john-jay-dining-hall",
           "https://dining.columbia.edu/content/ferris-booth-commons-0",
           "https://dining.columbia.edu/content/grace-dodge-dining-hall-0"]

run_real_test = True

## show only the relevatn ones for meal times
## Next step is to create a savefile with information so I don't need to access the website every time
## Final step is to figure out whethert there's a way to run the code autonomously every time someone writes it
## Or, maybe it just writes it the first time someone opens the site in the day* which could be me!


## DESIGN:
## bold the meal title
## figure out why it's duplicated
## make 

if (run_real_test):
    

    meals_list = []
    # Gets html from each url and parses for menu items
    for url in urlList:
        webdriver_path = '/chromedriver_mac64/chromedriver'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # Set the browser in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        
        print("requesting " + str(url))
        requested=datetime.now()
        driver.get(url)
        received=datetime.now()
        print("time taken " + str(received-requested))

        # Use Selenium to interact with the page, find elements, and extract information
        try:
            containers = driver.find_elements(By.CLASS_NAME, 'container')
            meals = ""

            for container in containers:
                try:
                    station = container.find_element(By.CLASS_NAME, 'station-title').text.strip()
                    meals = meals + "\n" + station + "\n"
                    station_meals = container.find_element(By.CLASS_NAME, 'meal-items')
                    menu_items = station_meals.find_elements(By.CLASS_NAME, 'meal-item')

                    for item in menu_items:
                        item_name = item.find_element(By.CLASS_NAME, 'meal-title').text.strip()
                        meals = meals + item_name + "\n"
        
                except:
                    continue

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        finally:
            # Close the browser window
            print("done")
            driver.quit()
            if not meals:
                meals = "No data on menu items"
            meals_list.append(meals)
else:
    meals_list = ['Item: BBQ Salmon\nItem: Crispy Corn Nuggets\nItem: Jasmine Rice\nItem: Green Beans & Carrots\nItem: Mac & Cheese\nItem: Bulgur Wheat Pilaf\n', 
                  'Item: Fried Items\nItem: Cheeseburger\nItem: Turkey Burger\nItem: Beyond Burger\nItem: Black Bean Burger\nItem: Crispy Chicken Sandwich\nItem: Grilled Chicken\n', 
                  'Item: Protein\nItem: Cheese\nItem: Toppings\nItem: Dressings\nItem: Southwest Chipotle Chicken\nItem: Southwest Chipotle Tempeh\nItem: Italian Beef\nItem: Tricolor Potato, Beans, Quinoa, and Vegan Cheese\n', 
                  'Item: Grilled Cilantro Lime Pork Chops\nItem: Sweet Cinnamon Plantain\nItem: Millet\nItem: Roasted Carrots & Broccoli\nItem: Black Beans\nItem: Cilantro Lime Chicken\nItem: Roasted Carrots & Broccoli\nItem: Sweet Cinnamon Plantain\nItem: Cilantro Lime Chicken\nItem: Roasted Carrots & Broccoli\nItem: Sweet Cinnamon Plantain\nItem: Mindful Chicken Fajita (with tortillas)\nItem: Roasted Carrots & Broccoli\nItem: Plantains\n', 
                  'Item: Cheese Blintz\nItem: Scrambled Eggs\nItem: Potato Pancakes\nItem: Pork Sausage\nItem: Sausage Gravy\nItem: Biscuits\nItem: Asparagus with Cherry Tomatoes\nItem: Tofu Scramble\nItem: Beyond Sausage\nItem: Cheese Blintz\nItem: Scrambled Eggs\nItem: Potato Pancakes\nItem: Pork Sausage\nItem: Sausage Gravy\nItem: Biscuits\nItem: Popcorn Tofu Bowl\nItem: Cheese Pizza\nItem: Vegan Cheese Pizza\nItem: Chickpea Chana Masala\nItem: Basmati Rice\nItem: Vegetable Medley\nItem: Baked Haddock Fish with Red Curry Sauce\nItem: Pesto Mashed Potatoes\nItem: Farro Pilaf\nItem: Steamed Cabbage\nItem: Chickpea Chana Masala\nItem: Basmati Rice\nItem: Vegetable Medley\nItem: Fried Rice Bar\n', 
                  'Item: Fresh Mozzarella, Tomato, Basil\nItem: Vegan Mozzarella, Tomato, Basil\nItem: Beef Pepperoni\nItem: Italian Jackfruit\n', 
                  'No data on menu items']



@app.route("/")
def home():
    if (meals_list[0].find("Salmon") != -1):
        FacHouseMsg = "Fac House has salmon today!"
    else:
        FacHouseMsg = "Fac House has nothing good today :("

    ChefMikesList = ["Chef Mike's Grandma Special", "Pastrami", "Chicken Parmagiana", "Beef Reuben"]
    ChefMikesMsg = "Chef Mike's has nothing good today :("
    
    for meal in ChefMikesList:
        if (meals_list[2].find(meal) != -1):
            ChefMikesMsg = "Chef Mike's has " + meal + " today !"
            break
    
    FerrisList = ["Popcorn Chicken", "Grilled Cheese", "Quesedilla"]
    FerrisMsg = "Ferris has nothing good today :("

    for meal in FerrisList:
        if (meals_list[4].find(meal) != -1):
            FerrisMsg = "Ferris has " + meal + " today!"
            break
        ## Something to consider is what if they have multiple good things i want
    
    return render_template(
        "home.html",
        date=datetime.now(),
        FacHouse = meals_list[0],
        JJs = meals_list[1],
        ChefMikes = meals_list[2],
        JohnJay = meals_list[3],
        Ferris = meals_list[4],
        GraceDodge = meals_list[5],
        FacHouseMsg = FacHouseMsg,
        FerrisMsg = FerrisMsg,
        ChefMikesMsg = ChefMikesMsg
        )

# New functions
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


if __name__ == "__main__":
    # Define the arguments for app.run() in a tuple
    #run_args = ({'host': '127.0.0.1', 'port': 5000},)

    # Start the server in a separate thread with specified arguments
    #server_thread = threading.Thread(target=app.run, kwargs={'debug': False, 'use_reloader': False}, args=run_args)
    server_thread = threading.Thread(target=app.run)
    server_thread.start()

    # Open the browser after a delay (adjust as needed)
    delay_seconds = 1
    def open_browser():
        testSite = "http://127.0.0.1:5000"
        webbrowser.open(testSite, new=2, autoraise=True)
    browser_thread = threading.Timer(delay_seconds, open_browser)
    browser_thread.start()

"""
next step is to iterate through the URLs and create individual variables
containing the text I want to add to the screens
Then, create the tabular format in dining.html
"""