import requests
import lxml.html as html
import os 
import datetime

HOME_URL = 'https://www.elcomercio.com/'
XPATH_LINK_TO_ARTICLE = '//a[@class = "image page-link"]/@href'
XPATH_TITLE = '//div[@class = "title"]/h1/text()'
XPATH_BODY = '//div[@class = "paragraphs"]/p[not(@class)]/node()'
XPATH_BODY_A = '//div[@class = "paragraphs"]/p[not(@class)]/a/text()'
XPATH_BODY_B = '//div[@class = "paragraphs"]/p[not(@class)]/b/text()'
XPATH_BODY_I = '//div[@class = "paragraphs"]/p[not(@class)]/i/text()'

def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            
            try:
                    title = parsed.xpath(XPATH_TITLE)[0]
                    title = title.replace('\"', '')
                    title = title.replace('?', '')
                    title = title.replace('¿', '')
                    title = title.replace('\'', '')
                    
                    body = parsed.xpath(XPATH_BODY)
                    full_body = []
                    body_a = parsed.xpath(XPATH_BODY_A)
                    body_b = parsed.xpath(XPATH_BODY_B)
                    body_i = parsed.xpath(XPATH_BODY_I)
                    counted_a = 0; counted_b = 0; counted_i = 0
                    for strings in body:
                        if isinstance(strings, str) != True:
                            strings = str(strings)
                            strings = strings[9:11]
                            if strings == 'a ':
                                full_body.append(body_a[counted_a])
                                counted_a += 1
                            if strings == 'b ':
                                full_body.append(body_b[counted_b])
                                counted_b += 1
                            if strings == 'i ':
                                full_body.append(body_i[counted_i])
                                counted_i += 1
                            if strings == 'br':
                                full_body.append('\n')
                        else:
                            full_body.append(strings)
                    
            except IndexError:
                return
            
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                for p in full_body:
                    f.write(p)
                
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notice = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            links_to_notice = list(filter(lambda x: x[0] == '/', links_to_notice))
            for a in links_to_notice:
                print(a)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notice:
                parse_notice('https://www.elcomercio.com'+link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()