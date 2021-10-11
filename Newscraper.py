from bs4 import BeautifulSoup
import requests
import time

class NewsScraper:

    def __init__(self):
        # self.siteList = ["https://politico.com"]
        self.siteConfigList = [
            {"baseURL": "https://www.politico.com",
            "linkStringsToKeep": ["www.politico.com"],
            "linkStringsToSkip": ["video", "login", "logout", "interactive", "pagesuite-professional", "/tag/", "cartoon"],
            "articleElementType": "p",
            "articleElementQualifier": {'class' : 'story-text__paragraph'},
            "elementContentToSkip": ["Image", "Photo"],
            # "articleStringsToRemove": [  # ".*EDT"#],
            "imageSelector": "[property=og:image]"
             }
            ]
        # "articleElementType": "p",
        # "elementContentToSkip": ["Image", "Photo"],
        # "articleStringsToRemove": [  # ".*EDT"#],
            # "imageSelector": "[property=og:image]"
        # )


    def main(self):
        print("Hello from Newscraper")
        for siteConfig in self.siteConfigList:
            siteLinks = self.getLinksFromPage(siteConfig)
            for link in siteLinks:
                article = self.getArticleFromLink(link, siteConfig)
                time.sleep(3)

    def getArticleFromLink(self, link, siteConfig):
        articleDict = {}
        articleElementType = siteConfig["articleElementType"]
        articleElementQualifier = siteConfig["articleElementQualifier"]
        response = requests.get(link)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        allTitles = soup.find_all('title')
        title = allTitles[0].string
        articleDict["title"] = title
        #articleElements = soup.find_all(articleElementType)
        #soup.find('p', attrs={'class' : 'lead'})
        # articleElements = soup.find_all(articleElementType, attrs={'class' : 'story-text__paragraph'})
        articleElements = soup.find_all(articleElementType, attrs= articleElementQualifier)
        articleText = ""
        for element in articleElements:
            if element.text is None:
                print(element)
            # print("element string: {0}".format(element.text))
            articleText += element.text
        print("articleText: {0}".format(articleText))


        pass


    def getRelevantLinks(self, links, linksToSkip):
        relevantLinks = []
        for link in links:
            skipLink = False
            for ignoreString in linksToSkip:
                if ignoreString in link:
                    skipLink = True
                    break
            if skipLink == True:
                continue
            else:
                relevantLinks.append(link)
        return relevantLinks

    def getLinksFromPage(self, siteConfig):
        goodLinks = []
        linksToSkip = siteConfig["linkStringsToSkip"]
        print("getting links from: {0}".format(siteConfig["baseURL"]))
        response = requests.get(siteConfig["baseURL"])
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        # links = soup.find_all("a")
        links = [a['href'] for a in soup.find_all('a', href=True)]
        tempLinks = set([ link for link in links if len(link) >= 57])
        # linksNotSkipped = [link for link in tempLinks if link not in []]
        # linksNotSkipped = [link for link in tempLinks if link not contains [aLink for aLink in linksToSkip ]]
        relevantLinks = self.getRelevantLinks(tempLinks, linksToSkip)
        return relevantLinks


if __name__ == '__main__':
    scraper = NewsScraper()
    scraper.main()
    testThing = "some text"
    print(testThing)




