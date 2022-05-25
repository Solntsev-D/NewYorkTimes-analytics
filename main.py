from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
import json
import time

url_list = {
    'https://www.nytimes.com/search?dropmab=true&query=&sections=World%7Cnyt%3A%2F%2Fsection%2F70e865b6-cc70-5181-84c9-8368b3a5c34b&sort=best': 'World',
    'https://www.nytimes.com/search?dropmab=true&query=&sections=U.S.%7Cnyt%3A%2F%2Fsection%2Fa34d3d6c-c77f-5931-b951-241b4e28681c&sort=best': 'U.S.',
    'https://www.nytimes.com/search?dropmab=true&query=&sections=New%20York%7Cnyt%3A%2F%2Fsection%2F39480374-66d3-5603-9ce1-58cfa12988e2&sort=best': 'NewYork',
    'https://www.nytimes.com/search?dropmab=true&query=&sections=Sports%7Cnyt%3A%2F%2Fsection%2F4381411b-670f-5459-8277-b181485a19ec&sort=best': 'Sports'
}

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
        Categories = driver.find_elements(By.CSS_SELECTOR, 'p.css-myxawk')
        urls_articles = driver.find_elements(By.TAG_NAME, 'a')

        for i in range(0, len(titles_articles)):
            release_date = release_dates[i].text
            if 'ago' in release_date:
                release_date = str(date.today())
            data = {
                'Date: ': release_date,
                'Category:': Categories[i].text,
                'Title:': titles_articles[i].text,
                'Url:': urls_articles[i].get_attribute('href')
            }

            filename = url_list[url] + '.json'
            with open(filename, 'a') as f:
                f.write(json.dumps(data, indent=4))

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()
