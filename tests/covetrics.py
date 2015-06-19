import requests
import re
from lxml import html


STARTING_URL = 'http://localhost:8080/'
#filename = "/Users/artem/Desktop/StudManager/tests/frontTests.py"


class PageElementFinder(object):
    """Visual elements finder"""
    def __init__(self):
        self.TotalElementList = []
        self.BaseUrl = ''
        self.IncludeLvl = 0
        self.UrlList = []

    def FindElements(self):
        """Returns list of elements from current page"""
        if self.UrlList:
            for PageUrl in self.UrlList:
                response = requests.get(PageUrl)
                self.ParsedBody = html.fromstring(response.content)
                FreshElementList = map(lambda element_id: PageUrl+element_id, self.ParsedBody.xpath('//@id'))
                self.TotalElementList += FreshElementList
                FreshElementList = map(lambda element_id: PageUrl+element_id, self.ParsedBody.xpath('//@class'))
                self.TotalElementList += list(set(FreshElementList))
        else:
            return "UrlList is empty"

    def GetUrlList(self, BaseUrl, IncludeLevel):
        """Return list of all GET urls up to IncludeLevel (0 for full search)"""
        try:
            IncludeLevel -= 1
            self.UrlList = [BaseUrl, 'http://localhost:8080/add/']
            if IncludeLevel == 0:
                return self.UrlList
            else:
                return self.UrlList[0:IncludeLevel]
        except:
            return "Error! Check base url list and IncludeLevel value"


class TestParser(object):
    """Class for working with tests file"""
    def __init__(self):
        self.ParsedTestList = []
        self.TotalElemetList = []

    def ParseTests(self, file):
        """Returns total info from tests file"""
        f = open(file)
        ParsedTestList = []
        ElementInTestsList = []
        cur = -1
        host = ''
        for line in f:
            if ('def Test') in line:
                ParsedTestList.append([line[line.find("def Test"):-2], 0, 0, 0])
                cur += 1
            if ("driver.get(\"http") in line:
                host = line[line.find("(\"")+2:line.find("\")")]
            if (("find_element_by_id") or ('find_elemnt_by_class')) in line:
                element = host + line[line.find("(\"")+2:line.find("\")")]
                ElementInTestsList.append(element)
                ParsedTestList[cur].append(element)
            if (ParsedTestList and re.match('.', line)):
                ParsedTestList[cur][1] += 1
            if ("assert") in line:
                ParsedTestList[cur][2] += 1
            if (("if ") or ("case :")) in line:
                ParsedTestList[cur][3] += 1
        self.ParsedTestList = ParsedTestList
        self.TotalElemetList = ElementInTestsList


class Comparer(object):
    def __init__(self):
        self.UncoveredElements = []
        self.TestCoverage = 0

    def Compare(self, AppElements, TestsElemets, ParsedTests):
        self.UncoveredElements = list(set(AppElements)-set(TestsElemets))

#pageEls = PageElementFinder()
#pageEls.GetUrlList(STARTING_URL, 2)
#pageEls.FindElements()
#print pageEls.TotalElementList
#testEls = TestParser()
#testEls.ParseTests(filename)
#comp = Comparer()
#comp.Compare(pageEls.TotalElementList, testEls.TotalElemetList, testEls.ParsedTestList)
#for s in pageEls.TotalElementList:
#    print s
#print comp.UncoveredElements



