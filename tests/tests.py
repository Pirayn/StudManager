import requests  
from lxml import html


STARTING_URL = 'http://localshost:8080/'
filename = "frontTests.py"


class PageElementFinder(object):
    """Visual elements finder"""
    def __init__(self):
        self.TotalElementList = []

    def FindElementsById(self, PageUrl, ParsedBody):
        """Returns list of elements from current page"""
        try:
            FreshElementList = map(lambda element_id: PageUrl+element_id, ParsedBody.xpath('//@id'))
            self.TotalElementList += FreshElementList
            return FreshElementList
        except:
            return "Error! Smth wrong with parsed body"

    def GetParsedBodyByUrl(self, PageUrl):
        try:
            response = requests.get(PageUrl)
            self.ParsedBody = html.fromstring(response.content)
            return self.ParsedBody
        except:
            return "Error! Check connection"

    def GetUrlList(self, BaseUrl, IncludeLevel):
        """Return list of all GET urls up to IncludeLevel (0 for full search)"""
        try:
            UrlList = [BaseUrl, 'http://localshost:8080/add']
            if IncludeLevel == 0:
                return UrlList
            else:
                return UrlList[0:IncludeLevel]
        except:
            return "Error! Check base url list and IncludeLevel value"


class TestParser(object):
    """Class for working with tests file"""
    def __init__(self):
        self.ParsedTestList = []
        self.TotalElemtList = []
        self.TotalAssertsCount = 0
        self.TotalElementsCount = 0
        self.AverageAssertsPerTest = 0
        self.AverageAssertsPerElement = 0
        self.ElementsUnderCoverageCount = 0
        self.TestsCount = 0

    def ParseTest(self, filename):
        """Returns total info from tests file"""
        try:
            f = open(filename)
            RawList = []
            for line in f:
                if line.startswith('def'):
                    RawList.append(line[line.find("def"):-2])
                if line.__contains__('assert'):
                    nums = line.find('assert')
                    RawList.append(line[nums:nums+6])
                if line.__contains__('find_element_by_id'):
                    RawList.append(line[line.find("(\"")+2:line.find("\")")])
                if line.__contains__("driver.get(\"http"):
                    RawList.append(line[line.find("(\"")+2:line.find("\")")])
            ParsedTestList = []
            for el in RawList:
                if el.__contains__('def Test'):
                    ParsedTestList.append(RawList[:RawList.index(el)])
                    RawList = RawList[RawList.index(el):]
            ParsedTestList.append(RawList)
            ParsedTestList = ParsedTestList[1:]
            for i in ParsedTestList:
                i.insert(1, str(i.count('assert')))
                ParsedTestList[ParsedTestList.index(i)] = filter(lambda x: x != 'assert', i)
            for i in ParsedTestList:
                for j in i[3:]:
                    i.append(i[2]+j)
                    i.remove(j)
                i.remove(i[2])
            self.ParsedTestList = ParsedTestList
            return self.ParsedTestList
        except:
            return "Error! Check check ur tests file!"

    def GetElementList(self):
        """Returns all element ids from tests file"""
        for i in self.ParsedTestList:
            for j in i[2:]:
                if j not in self.TotalElemtList:
                    self.TotalElemtList.append(j)
        self.TestsCount = len(self.TotalElemtList)
        self.TotalElementsCount = len(self.ParsedTestList[2:])
        return self.TotalElemtList

    def GetAssertsCount(self):
        """Returns total asserts count"""
        self.TotalAssertsCount = 0
        for el in self.ParsedTestList:
            self.TotalAssertsCount += int(el[1])
        self.AverageAssertsPerTest = self.TotalAssertsCount / self.TestsCount



tef = TestParser()
tef.ParseTest(filename)
print tef.ParsedTestList
print tef.GetElementList()




