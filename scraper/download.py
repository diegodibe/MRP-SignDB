import requests
from util import get_path


def download(url, counter):
    with open(get_path(counter, r'\videos', 'video{}.ts'), "ab") as f:
        i = 1
        status = 200
        while status == 200:
            rsp = requests.get(url.format(i))
            status = rsp.status_code

            if status == 404:
                print('Last video segment: ', i - 1, '.ts')
            else:
                print("downloading {}.ts".format(i))
            f.write(rsp.content)
            i += 1
