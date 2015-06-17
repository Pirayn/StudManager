import requests  
from lxml import html


STARTING_URL = 'http://localhost:8080/'
filename = "frontTests.py"


class PageElementFinder(object):
    """Visual elements finder"""
    def __init__(self):
        self.TotalElementList = []
        self.BaseUrl = ''
        self.IncludeLvl = 0

    def FindElementsById(self, PageUrl, ParsedBody):
        """Returns list of elements from current page"""
        try:
            FreshElementList = map(lambda element_id: PageUrl+element_id, ParsedBody.xpath('//@id'))
            self.TotalElementList += FreshElementList
            return FreshElementList
        except:
            return "Error! Smth wrong with parsed body"

    def FindElementsByClass(self, PageUrl, ParsedBody):
        """Returns list of elements from current page"""
        try:
            FreshElementList = map(lambda element_id: PageUrl+element_id, ParsedBody.xpath('//@class'))
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
        self.AverageTestsPerElement = 0
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
            self.TestsCount = len(ParsedTestList)
            return self.ParsedTestList
        except:
            return "Error! Check check ur tests file!"

    def GetElementList(self):
        """Returns all element ids from tests file"""
        for i in self.ParsedTestList:
            for j in i[2:]:
                if j not in self.TotalElemtList:
                    self.TotalElemtList.append(j)
        self.TestsCount = len(self.ParsedTestList)
        self.TotalElementsCount = len(self.TotalElemtList)
        self.AverageTestsPerElement = self.TestsCount / self.TotalElementsCount
        return self.TotalElemtList

    def GetAssertsCount(self):
        """Returns total asserts count"""
        self.TotalAssertsCount = 0
        for el in self.ParsedTestList:
            self.TotalAssertsCount += int(el[1])
        self.AverageAssertsPerTest = self.TotalAssertsCount / self.TestsCount


class Comparer(object):
    def __init__(self):
        self.elementsBezTestov = []
        self.elements = []
        self.result = []
        self.tef = TestParser()
        self.tef.ParseTest(filename)
        self.tef.GetElementList()
        self.tef.GetAssertsCount()
        pef = PageElementFinder()
        s = pef.GetParsedBodyByUrl(STARTING_URL)
        d = pef.FindElementsById(STARTING_URL, s)
        for i in d:
            if i not in self.tef.TotalElemtList:
                self.elementsBezTestov.append(i)
        self.elements = d

    def GetElementsUnderCover(self, listfromtests, listfrompage):

        pass

    def GetElementsWithoutCover(self, listfromtests, listfrompage):
        pass

    def Compare(self):
        a = (len(self.elements))
        b = (len(self.elementsBezTestov))
        max = 0
        min = len(self.tef.ParsedTestList[1])
        kol = 0
        sum = 0
        a1 =  'elements on page: '+ str(a)
        a2 =  'bez testov: '+ str(b)+ ' shtuk '+ str(self.elementsBezTestov)
        a3 = 'test coverage: '+ str(100-float(b)/float(a)*100)+ '%'
        for i in self.tef.ParsedTestList:
            dl = len(i[2:])
            kol += 1
            sum += dl
            if max < dl:
                max = dl
            if min > dl:
                min = dl
        a5 = 'max: '+str(max)
        a6 = 'min: ' + str(min)
        a7 = 'avg: ' + str(float(sum)/float(kol))
        self.result = [a1, a2, a3, a5, a6, a7]

comp  = Comparer()
comp.Compare()
print comp.result[0]
print comp.result[1]
print comp.result[2]
print comp.result[3]
print comp.result[4]
print comp.result[5]

"""
tef = TestParser()
tef.ParseTest(filename)
tef.GetElementList()
tef.GetAssertsCount()
pef = PageElementFinder()
s = pef.GetParsedBodyByUrl(STARTING_URL)
print 'azaza', s
d = pef.FindElementsById(STARTING_URL, s)
elementsBezTestov = []
for i in d:
    if i not in tef.TotalElemtList:
        elementsBezTestov.append(i)



print 'Total tests count: ', tef.TestsCount
print 'ParsedTestlist: ', tef.ParsedTestList
print 'TotalElementList: ', tef.TotalElemtList
print 'TotalAssertsCount: ', tef.TotalAssertsCount
print 'TotalElementsCount: ', tef.TotalElementsCount
print 'AverageAssertsPerTest: ', tef.AverageAssertsPerTest
print 'AssertsPerElement: ', tef.AverageAssertsPerElement
print 'AverageTestsPerElement', tef.AverageTestsPerElement

a = (len(pef.TotalElementList))
b = (len(elementsBezTestov))
max = 0
min = len(tef.ParsedTestList[1])
kol = 0
sum = 0


print 'elements on page: ', a
print 'bez testov: ', b, ' shtuk ', elementsBezTestov
print 'test coverage: ', 100-float(b)/float(a)*100, '%'

for i in tef.ParsedTestList:
    dl = len(i[2:])
    kol += 1
    sum += dl
    if max < dl:
        max = dl
    if min > dl:
        min = dl

print 'max: ', max
print 'min', min
print 'avg: ', float(sum)/float(kol)

"""

