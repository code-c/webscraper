import pandas as pd
import numpy as mp
import matplotlib
import matplotlib.pyplot as plt
from selenium import webdriver


#scrape the datatable entriesd and enter them into a pandas dataframe
def web_table_to_dict():
    new_dictionary = {"Date":[],"Stage":[],"Flow":[]}

    # this is a very buggy approach but this is a demo so what the hey
    # web_table_element='/html/body/table/tbody/tr/td[1]/table/tbody/tr[2]/td[1]' notice the change of the ending to add /td[1]
    # there a three columns so we iterate from [1,3] and from row [2, 209] (skipping the first row) assuming that its fixed we should be good.
    # I also despise nest for loops but these are small tasks so what the hey eh
    #this is also a test to see if the data type is transfered through
    table_row = ".//td"
    web_table_rows = browser.find_elements_by_xpath(table_row)
    print(len(web_table_rows))

    try:
        for web_table_row in web_table_rows:
            #check to see if the string contains '-' or '|' and not do anything with those
            if ("Data" not in web_table_row.text):

                if "/" in web_table_row.text:
                    #store the date as a string
                    new_dictionary["Date"].append(web_table_row.text)
                    #print(new_dictionary)
                elif "ft" in web_table_row.text:
                    #remove the postfix 'ft'
                    element_stage = web_table_row.text[:-2]
                    #append as a float
                    new_dictionary["Stage"].append(float(element_stage))
                    #print(new_dictionary)
                elif "kcfs" in web_table_row.text:
                    #remove the postfix 'kcfs'
                    element_flow = web_table_row.text[:-4]
                    #append as a float
                    new_dictionary["Flow"].append(float(element_flow))
                    #print(new_dictionary)

    except Exception as e:
        print("Error: %s" % e)

    return new_dictionary




river_dataUrl  = 'https://water.weather.gov/ahps2/hydrograph_to_xml.php?gage=dovm1&output=tabular&time_zone=est'

chrome_path = r'/Volumes/Macintosh HD/Users/codiecottrell/Documents/webscraper/chromedriver' #path from 'which chromedriver'
browser = webdriver.Chrome(executable_path=chrome_path)

browser.get(river_dataUrl)

#browser.find_element_by_xpath('//*[@id="redirect"]/table[4]/tbody/tr/td[1]/table/tbody/tr[4]/td/a').click()

dictionary = web_table_to_dict()
print(dictionary)

river_data = pd.DataFrame.from_dict(dictionary)

pd.to_datetime(river_data.Date, format="%m/%d %H:%M")

#dates = matplotlib.dates.date2num(river_data.Date)

plt.plot(river_data.Date, river_data.Stage, linestyle='-', color='b')
plt.gcf().autofmt_xdate()

























plt.show()
