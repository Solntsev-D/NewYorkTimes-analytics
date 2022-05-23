from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import json

url_list = [
    'https://www.nytimes.com/search?dropmab=true&query=&sections=World%7Cnyt%3A%2F%2Fsection%2F70e865b6-cc70-5181-84c9-8368b3a5c34b&sort=best',
    'https://www.nytimes.com/search?dropmab=true&query=&sections=U.S.%7Cnyt%3A%2F%2Fsection%2Fa34d3d6c-c77f-5931-b951-241b4e28681c&sort=best',
    'https://www.nytimes.com/search?dropmab=true&query=&sections=New%20York%7Cnyt%3A%2F%2Fsection%2F39480374-66d3-5603-9ce1-58cfa12988e2&sort=best',
    'https://www.nytimes.com/search?dropmab=true&query=&sections=Sports%7Cnyt%3A%2F%2Fsection%2F4381411b-670f-5459-8277-b181485a19ec&sort=best'
]

index = 0
for url in url_list:
    index += 1
    driver = webdriver.Chrome(executable_path=r"C:\PyProjects\NewYorkTimes-analytics\chromedriver\chromedriver.exe")
    try:
        driver.get(url=url)
        driver.maximize_window()
        time.sleep(1)

        i = 0
        while i < 2:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            sm_button = driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[2]/div[2]/div/button')
            sm_button.click()
            i = i+1

        titles_articles = driver.find_elements(By.CSS_SELECTOR, 'h4.css-2fgx4k')
        release_dates = driver.find_elements(By.CSS_SELECTOR, 'span.css-17ubb9w')
        locations = driver.find_elements(By.CSS_SELECTOR, 'p.css-myxawk')
        urls_articles = driver.find_elements(By.TAG_NAME, 'a')

        for i in range(0, len(titles_articles)):
            data = {
                'Date: ': release_dates[i].text,
                'Type:': locations[i].text,
                'Title:': titles_articles[i].text,
                'Url:': urls_articles[i].get_attribute('href')
            }
            if index == 1:
                filename = 'world_section'+str(i)+'.json'
                with open(filename, 'w') as f:
                    json.dump(data, f)

            elif index == 2:
                filename = 'ua_section'+str(i)+'.json'
                with open(filename, 'w') as f:
                    json.dump(data, f)

            elif index == 3:
                filename = 'newyork_section'+str(i)+'.json'
                with open(filename, 'w') as f:
                    json.dump(data, f)

            elif index == 4:
                filename = 'sport_section'+str(i)+'.json'
                with open(filename, 'w') as f:
                    json.dump(data, f)

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()
