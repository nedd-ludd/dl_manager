#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
import re


class Import:
    def __init__(self, raw_data_file):
        self.file = raw_data_file
        self.imports_data = self.get_data()
        self.soup = 0

    def get_data(self):
        with open(self.file, "r") as html:
            self.soup = bs(html, features="html.parser")
            data_list = []
            for item in self.soup.find_all('li', attrs={'class': 'list-entry', 'class': 'list-entry alt'}):
                if bool(re.search("magnet", str(item))):
                    href = self.return_magnet_link(item)
                    description = self.return_contents(item, "description.php")
                    category = self.return_contents(item, "category:601")
                    seeds = self.return_seeds(item)
                    # data_list.append([description, href, category, seeds])
                    data_list.append(
                        {'description': description, 'href': href, 'category': category, 'seeds': seeds})
            return data_list

    def getImportsData(self):
        return self.imports_data

    def return_magnet_link(self, bs4_item):
        for tag in bs4_item.find_all('a', href=True):
            href = tag.get('href')
            if href[0:6] == 'magnet':
                return href

    def return_contents(self, bs4_item, criteria):
        for tag in bs4_item.find_all('a', href=True):
            href = tag.get('href')
            if bool(re.search(criteria, href)):
                return tag.contents[0]

    def return_seeds(self, bs4_item):
        return bs4_item.find('span', {'class': 'list-item item-seed'}).contents[0]


def main():
    fin = r".\links.html"
    links_import = Import(raw_data_file=fin)
    downloads = links_import.getImportsData()
    print(downloads)


if __name__ == "__main__":
    main()
