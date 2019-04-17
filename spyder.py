import requests

def get_one_page(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/66.0.3359.181 Safari/537.36"
    }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.text

def main():
    url = 'http://maoyan.com/board'
    html = get_one_page(url)
    print(html)

if __name__=='__main__':
    main()


def parse_one_page4(html):
    soup = BeautifulSoup(html,'lxml')
    items = range(10)
    for item in items:
        yield{
            'index':soup.find_all(class_='board-index')[item].string,
            'thumb':soup.find_all(class_= 'board-img')[item].attrs['src'],
            'name':soup.find_all(name = 'p',attrs = {'class':'name'})[item].string,
            'star':soup.find_all(name = 'p',attrs = {'class':'star'})[item].string.strip()[3:],
            'time':get_release_time(soup.find_all(class_ = 'releasetime')[item].string.strip()[5:]),
            'area':get_release_time(soup.find_all(class_= 'releasetime')[item].string.strip()[5:]),
            'score':soup.find_all(name = 'i',attrs = {'class':'integer'})[item].string.strip() + soup.find_all(name = 'i',attrs = {'class':'fraction'})[item].string.strip()
        }