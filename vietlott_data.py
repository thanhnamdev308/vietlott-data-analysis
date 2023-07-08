"""Vietlott data analysis
This is python code to analyze Vietlott data
"""

from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver
from datetime import datetime
import pandas

# Init Chrome to collect data
webdriver.chrome.driver = r"E:\setup\selenium\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome()

###
# STEP 1: Get the current draw result.
###
current_result_link = "https://vietlott.vn/vi/trung-thuong/ket-qua-trung-thuong/655"
driver.get(current_result_link)

current_result_html = driver.page_source

# make BeautifulSoup
soup = BeautifulSoup(current_result_html, "html.parser")

# prettify the html
prettyHTML = soup.prettify()

# save the prettified html to a file
with open("current_result.html", "w", encoding="utf-8") as file:
    file.write(prettyHTML)

# Find the draw code and draw date
current_draw_code = soup.find('h5').find('b').get_text()
current_draw_date = soup.find('h5').find_all('b')[1].get_text()

# Find the list of numbers
current_lottery_number = [int(span.get_text()) for span in soup.find_all(
    'span', {'class': 'bong_tron small'})]

print(f"Current draw:\t\t{current_draw_code}")
print(f"Draw date:\t\t{current_draw_date}")
print(f"Current numbers:\t{current_lottery_number}")

###
# STEP 2: Get all history draw result and save it to csv.
###

CURRENT_DRAW = int(current_draw_code[1:])


class LotteryNumber:
    """
    A class represent a draw result
    Example of a declaration:
    my_lottery = LotteryNumber(901, '07/07/2023', [4, 8, 15, 16, 23, 42])
    """

    def __init__(self, code, date, numbers):
        self.code = code
        self.date = datetime.strptime(date, '%d/%m/%Y')
        self.numbers = numbers


# Get all Lottery result links
result_links = []
for i in range(1, CURRENT_DRAW + 1):
    link = f"https://vietlott.vn/vi/trung-thuong/ket-qua-trung-thuong/655?id={i:05}&nocatche=1#00001"
    result_links.append(link)

# Loop to get the data into a list of LotteryNumber objects
file_index = 1
result_data = []
for link in result_links:
    driver.get(link)

    result_html = driver.page_source

    # make BeautifulSoup
    soup = BeautifulSoup(result_html, "html.parser")

    # Find the draw code and draw date
    draw_code = soup.find('h5').find('b').get_text()
    draw_date = soup.find('h5').find_all('b')[1].get_text()
    # Find the list of numbers
    lottery_number = [int(span.get_text()) for span in soup.find_all(
        'span', {'class': 'bong_tron small'})]

    # prettify the html
    prettyHTML = soup.prettify()

    # save the prettified html to a file
    with open(f"html/{file_index}.html", "w", encoding="utf-8") as file:
        file.write(prettyHTML)

    # Add to the result_data list
    result_data.append(LotteryNumber(
        int(draw_code[1:]), draw_date, lottery_number))

    # Log to console
    print("Findind results:")
    print(f"Draw:\t\t{draw_code}")
    print(f"Draw date:\t{draw_date}")
    print(f"Numbers:\t{lottery_number}")

    # Create a list of dictionaries containing the data from the result_data list
    data = [{'code': lottery.code,
            'date': lottery.date.strftime('%d/%m/%Y'),
             'number 1': lottery.numbers[0],
             'number 2': lottery.numbers[1],
             'number 3': lottery.numbers[2],
             'number 4': lottery.numbers[3],
             'number 5': lottery.numbers[4],
             'number 6': lottery.numbers[5], } for lottery in result_data]

    # Create a DataFrame from the data
    df = pandas.DataFrame(data)

    # Write the DataFrame to a CSV file
    df.to_csv('result_data.csv', index=False)
    
    # Increase file_index
    file_index += 1

###
# STEP 3: Analyze the data.
###

# Exit Chrome
driver.quit()
