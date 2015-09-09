# encoding: utf-8
import urllib2
from bs4 import BeautifulSoup
from crawlerTools.data import mitbbs
from crawlerTools.data import onePthreeC
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Crawler(object):

    support_website = {
        "mitbbs": {
            "root": "http://www.mitbbs.com",
            "boards": mitbbs.boards,
        },
        "1p3c": {
            "root": "http://www.1point3acres.com/bbs/",
            "boards": onePthreeC.boards
        }
    }

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}



    def __init__(self, website):
        try:
            self.root_url = self.support_website[website]["root"]
            self.boards = self.support_website[website]["boards"]
        except KeyError:
            print(website + " is not support")
            print("currently support website:")
            for key, val in self.support_website.items():
                print(key + " : " + val["root"])

    def _get_data(self, section, max_page, keywords):
        results = {}
        keywords = keywords if type(keywords) == list else list(keywords)
        page = 0
        while page < max_page:
            try:
                page_num = page * 100 + 1
                url = self.root_url + '/bbsdoc1/' + section + '_' + str(page_num) + '_0.html'
                req = urllib2.Request(url, headers=self.hdr)
                content = urllib2.urlopen(req).read()
                content = BeautifulSoup(content, from_encoding='GB18030')
                for link in content.findAll('a', {'class': 'news1'}):
                    new_url = self.root_url + link.get('href')
                    title = link.string
                    if title is None:
                        continue
                    for keyword in keywords:
                        if keyword in title:
                            results[title.strip(' \t\n\r')] = new_url
                            break
            except:
                print "Unexpected error:", sys.exc_info()[0]
            page += 1
        return results

    def crawl(self, sections, max_page=1, keywords=''):
        sections = sections if type(sections) == list else [sections]
        keywords = keywords.strip().split(' ')
        for section in sections:
            if section not in self.boards:
                print(section + " is not in boards")
                continue
            else:
                en_section = mitbbs.boards[section]
                results = self._get_data(en_section, max_page, keywords)
                print("/-------" + section + "---------/")
                for key, val in results.items():
                    print(key)
                    print(val)


if __name__ == "__main__":
    mit = Crawler('mitbbs')
    mit.crawl('待字闺中')