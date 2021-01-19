import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import json
from util import get_path
import time


def get_driver(url):
    # get new webpage given as a parameter. capabilities are necessary to sniff the logs
    # again the path of the browser driver is necessary
    capabilities = DesiredCapabilities.EDGE
    capabilities['loggingPrefs'] = {'performance': 'ALL'}
    capabilities['edgeOptions'] = {'w3c': False}
    driver = webdriver.Edge("msedgedriver.exe", capabilities=capabilities)
    driver.get(url)
    return driver


def process_browser_log_entry(entry):
    # reformat entry in json
    response = json.loads(entry['message'])['message']
    return response


def process_logs(logs):
    # it returns just network logs, where sought url can be
    for entry in logs:
        log = json.loads(entry['message'])['message']
        if (
                "Network.response" in log["method"]
                or "Network.request" in log["method"]
                or "Network.webSocket" in log["method"]
        ):
            yield log  # returns itarable without storing info in memory


def find_urls(log):
    for entry in log:
        if 'url' in entry:
            return log['url']


def extract_urls_vtt(url_list, vtt_list, log):
    if log is not None and '.ts' in log:
        url = log.split('.ts')[0]
        url += '.ts'
        url_list.append(url)
    if log is not None and '.vtt' in log:
        vtt = log.split('.vtt')[0]
        vtt += '.vtt'
        vtt_list.append(vtt)

    return url_list, vtt_list


def website_logs(webpage, counter):
    # open new webpage
    driver = get_driver(webpage)
    # wait for 5 seconds to allow time for the requests
    time.sleep(5)
    # sniff performance logs, that include json files
    browser_logs = driver.get_log('performance')

    logs = process_logs(browser_logs)
    urls = []
    vtt = []

    for log in logs:
        urls_request = None
        try:
            urls_request = find_urls(log['params']['request'])
        except KeyError:
            pass
        urls, vtt = extract_urls_vtt(urls, vtt, urls_request)
    print('url and vtt lists', urls, vtt)

    if len(vtt) > 0:
        with open(get_path(counter, r'\audio_to_text\subtitles', 'subtitles{}.txt'), 'w') as sub:
            rsp = requests.get(vtt[0])
            print("downloading subtitles in .txt format")
            sub.write(rsp.text)
    else:
        print('No subtitles found for this videos')
    driver.quit()

    if len(urls[0]) > 0:
        strindex = urls[0].index('segment')
        loc = strindex + len('segment')
        # url = urls[0].replace('segment1', 'segment{}')
        url = urls[0][:loc] + '{}' + urls[0][loc + 1:]
        print('The url for the first segment of page ', counter, 'was successfully found.')
        return url
    else:
        print('No url containing videos')
        return None
