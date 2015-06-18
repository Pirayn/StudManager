"""
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
"""
import requests
import re
from lxml import html
PageUrl = 'http://localhost:8080/'
response = requests.get(PageUrl)
ParsedBody = html.fromstring(response.content)
FreshElementList = map(lambda element_id: PageUrl+element_id, ParsedBody.xpath('//@class'))
print list(set(FreshElementList))