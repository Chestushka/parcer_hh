import requests
from bs4 import BeautifulSoup

ITEMS = 100
MAX_PAGE = 3

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru,en;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": 'hhuid=9_S0hNKJUL9XG2U4HRNHpQ--; _ym_uid=1698176278576981462; __ddg1_=1HDXlsyrVHTOUAZms7iC; cpa=%7B%22partner_name%22%3A+%22utm_term%22%2C+%22data%22%3A+%22%5Cu043f%5Cu043e%5Cu0438%5Cu0441%5Cu043a+%5Cu0432%5Cu0430%5Cu043a%5Cu0430%5Cu043d%5Cu0441%5Cu0438%5Cu0439%22%7D; cpa_deduplication_source=yandex; tmr_lvid=f00506947ffb5281039dc6129a97e477; tmr_lvidTS=1727958617135; iap.uid=883f4cbc7f4346268150f6056696fea8; _ym_d=1727958617; __zzatgib-w-hh=MDA0dBA=Fz2+aQ==; redirect_host=hh.ru; region_clarified=hh.ru; uxs_uid=71d925d0-8183-11ef-8912-3fd5c1cb5d4f; _xsrf=0427fbe4065f86c0cafeb7ed4edb558d; hhrole=anonymous; display=desktop; crypted_hhuid=F1940996A34F3B9B28F74401CAC00A8D42CFE1B5C58D3EAA525B6F49D86506FF; hhtoken=KLjucEPNq_XMA1DWdcQCJ5yKkO2x; GMT=3; _ym_isad=1; domain_sid=eg76jaIFkpiLcftL7jWnf%3A1728576288270; __ddg9_=209.58.130.207; __ddgid_=Fc6r0BLHx8fED8JV; __ddgmark_=EKENndJHObaQ7hz0; __ddg5_=8uo7uxDhuglybvJf; __ddg2_=4xZ5zS9Pv5XP07E0; device_magritte_breakpoint=xs; device_breakpoint=xs; _ym_visorc=w; regions=""; total_searches=8; tmr_detect=0%7C1728578517115; __ddg8_=fusz5HHW4geA2hcg; __ddg10_=1728578991; gsscgib-w-hh=667QeTYdb5NBKNorEGQmDq8djMEej8mRSQG/KYFD5ZQTjamtntbwb0XSoRn1kFq5fdgt69xbzecQeyrOipbosdcW0mH3P9+wfcopP0OSfk76rsVOeCzHQJ+qaDNnXs5sPXga+C2YjcZDD1UaeqeVt0KB/UJ1oIVg8a3toXJ0pL8F0muGMijqhOcguqBQvXr23l9cx8GpgYDKJM6A0Pd8C2BorJQrQYHUZh8xeb52dV2IsTLH9sCdWMXm5fWXoLqHIQ==; cfidsgib-w-hh=0MJS7zBLiVC/OJPmQ+AbF2ENZu38Zq6JbVI7Xa0fWd3Qe+Gj3kKzmxwkjUVsMQhHtqLwNLUG4MA4VHuxl1PcSwPXgkfwEoOF+oahIFIi/C2YGRQ3Mv6bFgeqS0VHpShRjCS29HGa0Gn2T8y+cSCt/1SwEOlBmuzGyEokNA==; cfidsgib-w-hh=0MJS7zBLiVC/OJPmQ+AbF2ENZu38Zq6JbVI7Xa0fWd3Qe+Gj3kKzmxwkjUVsMQhHtqLwNLUG4MA4VHuxl1PcSwPXgkfwEoOF+oahIFIi/C2YGRQ3Mv6bFgeqS0VHpShRjCS29HGa0Gn2T8y+cSCt/1SwEOlBmuzGyEokNA==; gsscgib-w-hh=667QeTYdb5NBKNorEGQmDq8djMEej8mRSQG/KYFD5ZQTjamtntbwb0XSoRn1kFq5fdgt69xbzecQeyrOipbosdcW0mH3P9+wfcopP0OSfk76rsVOeCzHQJ+qaDNnXs5sPXga+C2YjcZDD1UaeqeVt0KB/UJ1oIVg8a3toXJ0pL8F0muGMijqhOcguqBQvXr23l9cx8GpgYDKJM6A0Pd8C2BorJQrQYHUZh8xeb52dV2IsTLH9sCdWMXm5fWXoLqHIQ==; fgsscgib-w-hh=1Er4bc73fb966fb5454ec949f0bfd3fe9532eff0',
    "Origin": "https://hh.ru",
    "Priority": "u=4, i",
    "Referer": "https://hh.ru/search/vacancy?text=python&search_period=0&items_on_page=100",
    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "YaBrowser";v="24.7", "Yowser";v="2.5"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36",
}

def extract_job(html):

    title = html.find("span", {"data-qa": "serp-item__title-text"}).text
    company = html.find("span", {"data-qa": "vacancy-serp__vacancy-employer-text"}).text
    link = html.find('a', {'class': 'magritte-link___b4rEM_4-3-2 magritte-link_style_neutral___iqoW0_4-3-2 magritte-link_enable-visited___Biyib_4-3-2'})['href']
    
    salary = html.find('meta', property='og:description')
    if salary:
        salary = salary.get('content')
    if not salary:
        salary = 'Нет данных1'

    
    return {"title": title, "company": company, "salary": salary, 'link': link}

def extract_hh_jobs(last_page, url):
    jobs = []

    for page in range(last_page):

        print(f'Парсинг страницы {page}')
        result = requests.get(f"{url}&page={page}", headers=headers)
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.findAll("div", {"class": "vacancy-info--umZA61PpMY07JVJtomBA"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs

def get_jobs(keyword):
    url = f"https://hh.ru/search/vacancy?text={keyword}&search_period=0&items_on_page={ITEMS}"
    
    jobs = extract_hh_jobs(MAX_PAGE, url)
    return jobs
