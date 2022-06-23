from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
from datetime import datetime
import json
import time

def DateConversion(release_date): #Функция для преобразования даты к виду, который можно сделать типом datetime
    months = { #Словарь, где ключ - краткое название месяца, а значение - его номер
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
        }

    if "ago" in release_date or "now" in release_date: #Проверяем есть ли значения, у которых в дате записано "5 min ago" или "just now"
        release_date = str(date.today()) #Записываем в дату сегодняшнее число
        return release_date

    else: 
        for word in months:
            if word in release_date: #Смотрим какой из месяцев записан в дате
                month = months[word] #Присваиваем ему соответствующий номер месяца
                
        day = [int(day) for day in str.split(release_date) if day.isdigit()] #День равен целочисленной чисти даты
        
        release_date = "2022" + "-" + str(month) + "-" + str(day[0]) #Формируем конечный вид даты
        return release_date
    
def CheckDuplicates(df, column_name): #Функция, которая ищет и удаляет строки-дубликаты
    if any(df[column_name].duplicated()) == True: #Проверяем есть ли строки-дубликаты
        return df.drop_duplicates(column_name) #Если есть - удаляем
    else: return df

url_list = { #Словарь в котором ключ - ссылка на сайт со статьями в определённом временном диапозоне, значение - название секции
        'https://www.nytimes.com/search?dropmab=true&endDate=20220531&query=&sections=World%7Cnyt%3A%2F%2Fsection%2F70e865b6-cc70-5181-84c9-8368b3a5c34b&sort=newest&startDate=20220101': 'world1',
    'https://www.nytimes.com/search?dropmab=true&endDate=20220430&query=&sections=World%7Cnyt%3A%2F%2Fsection%2F70e865b6-cc70-5181-84c9-8368b3a5c34b&sort=newest&startDate=20220101': 'world2',
    'https://www.nytimes.com/search?dropmab=true&endDate=20220331&query=&sections=World%7Cnyt%3A%2F%2Fsection%2F70e865b6-cc70-5181-84c9-8368b3a5c34b&sort=newest&startDate=20220101': 'world3',
    'https://www.nytimes.com/search?dropmab=true&endDate=20220228&query=&sections=World%7Cnyt%3A%2F%2Fsection%2F70e865b6-cc70-5181-84c9-8368b3a5c34b&sort=newest&startDate=20220101': 'world4',
    'https://www.nytimes.com/search?dropmab=true&endDate=20220531&query=&sections=U.S.%7Cnyt%3A%2F%2Fsection%2Fa34d3d6c-c77f-5931-b951-241b4e28681c&sort=newest&startDate=20220101': 'us1',
    'https://www.nytimes.com/search?dropmab=true&endDate=20220430&query=&sections=U.S.%7Cnyt%3A%2F%2Fsection%2Fa34d3d6c-c77f-5931-b951-241b4e28681c&sort=newest&startDate=20220101': 'us2',
    'https://www.nytimes.com/search?dropmab=true&endDate=20220331&query=&sections=U.S.%7Cnyt%3A%2F%2Fsection%2Fa34d3d6c-c77f-5931-b951-241b4e28681c&sort=newest&startDate=20220101': 'us3',
    'https://www.nytimes.com/search?dropmab=true&endDate=20220228&query=&sections=U.S.%7Cnyt%3A%2F%2Fsection%2Fa34d3d6c-c77f-5931-b951-241b4e28681c&sort=newest&startDate=20220101': 'us4',
    'https://www.nytimes.com/search?dropmab=true&endDate=20220531&query=&sections=Sports%7Cnyt%3A%2F%2Fsection%2F4381411b-670f-5459-8277-b181485a19ec&sort=newest&startDate=20220101': 'sport1',
    'https://www.nytimes.com/search?dropmab=true&endDate=20220430&query=&sections=Sports%7Cnyt%3A%2F%2Fsection%2F4381411b-670f-5459-8277-b181485a19ec&sort=newest&startDate=20220101': 'sport2'
} 
for url in url_list:
    driver = webdriver.Chrome(executable_path=r"C:\PyProjects\NewYorkTimes-analytics\chromedriver\chromedriver.exe")
    try:
        driver.get(url=url)
        driver.maximize_window()
        time.sleep(1)

        i = 0
        while i < 150: #150 раз прокручиваем вниз и нажимаем кнопку "Show more", чтобы загрузить больше статей
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            sm_button = driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[2]/div[2]/div/button')
            sm_button.click()
            time.sleep(2)
            i = i+1

        titles_articles = driver.find_elements(By.CSS_SELECTOR, 'h4.css-2fgx4k') #Ищем все необходимые данные в коде страницы
        release_dates = driver.find_elements(By.CSS_SELECTOR, 'span.css-17ubb9w')
        categories = driver.find_elements(By.CSS_SELECTOR, 'p.css-myxawk')
        urls_articles = driver.find_elements(By.TAG_NAME, 'a')
        
        data = []
        for i in range(0, len(titles_articles)): #Записываем найденные данные в список из словарей Data

            release_date = DateConversion(release_dates[i].text)

            info = {
                'Date': release_date,
                'Category': categories[i].text,
                'Title': titles_articles[i].text,
                'Url': urls_articles[i].get_attribute('href')
            }
            data.append(info)

        filename = url_list[url] + '.json' #Передаём спсиок Data в .json файл.
        with open(filename, 'a') as f:
            f.write(json.dumps(data, indent=4))

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()
    
