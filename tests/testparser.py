__author__ = 'artem'
f = open("frontTests.py")
RawList = []
for line in f:
    if line.startswith('def'):
        RawList.append(line[line.find("def"):-1])
    if line.__contains__('assert'):
        nums = line.find('assert')
        RawList.append(line[nums:nums+6])
    if line.__contains__('find_element_by_id'):
        RawList.append(line[line.find("(\"")+2:line.find("\")")])
    if line.__contains__("driver.get(\"http"):
        RawList.append(line[line.find("(\"")+2:line.find("\")")])

ParsedList = []
for el in RawList:
    if el.__contains__('def Test'):
        ParsedList.append(RawList[:RawList.index(el)])
        RawList = RawList[RawList.index(el):]
ParsedList.append(RawList)

ParsedList = ParsedList[1:]

for i in ParsedList:
    i.insert(1, str(i.count('assert')))
    ParsedList[ParsedList.index(i)] = filter(lambda x: x != 'assert', i)

for i in ParsedList:
    for j in i[3:]:
        i.append(i[2]+j)
        i.remove(j)
    i.remove(i[2])

print ParsedList




