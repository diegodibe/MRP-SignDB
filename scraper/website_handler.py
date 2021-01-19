from selenium import webdriver
# import Action chains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import DesiredCapabilities
from scraper.website_logs import website_logs
from scraper.download import download
import time


def get_site():
    # get specified website, driver edge(or other driver) location must be specified
    capabilities = DesiredCapabilities.EDGE
    driver = webdriver.Edge(executable_path="scraper/msedgedriver.exe", capabilities=capabilities)
    # set the main page as the page with all the videos
    driver.get("https://www.rsi.ch/play/tv/programma/telegiornale-lingua-dei-segni?id=10960556")
    return driver


def scraper():
    print('\n Scraper module running...')
    driver = get_site()

    # click load more button to have all videos in the page
    python_button = None
    while python_button is None:
        try:
            python_button = driver.find_elements_by_xpath("//button[@class='Button__StyledButton-bxxxk2-0 bdfIqV']")[0]
            ActionChains(driver).move_to_element(python_button).click(python_button).perform()
            python_button = None
        except:
            break
    
    # get all the element with the word 'segni' in it
    elements = driver.find_elements_by_partial_link_text('segni')
    # elements = driver.find_elements_by_xpath('//a[contains(@href,"nohmatikh")]') #for greek videos
    
    count = 0  # counter of elements with the word 'segni' in it
    hrefs = []
    for elem in elements:
        print('elem', elem.get_attribute("href"))
        hrefs.append(elem.get_attribute("href"))
        count += 1
    print('Videos found', count)
    
    count = 0
    for i in hrefs:
        count += 1
        # element extracted, use the element to extract url
        # print(elem.get_attribute("href"))
        url = None
        while url is None:
            print(url)
            try:
                url = website_logs(i, count)
            except:
                pass
    
        # url extracted, download
        if url is not None:
            download(url, count)
            print('video ', count, ' has been processed.')
        else:
            print('webpage ', i, 'not processed')
    
    driver.quit()
