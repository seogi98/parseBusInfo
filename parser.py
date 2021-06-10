from bs4 import BeautifulSoup
import requests
import time
import heapq
import openpyxl

# 여기에 신청한 본인의 key를 넣어야 합니다!
key = ''

numOfRows = '10000'
pageNo = '1'
naek = []
data = []
# 도시 목록을 가져온다.
def findCityList():
    queryParams = 'ServiceKey='+key+'&numOfRows=' + numOfRows + '&pageNo='+pageNo
    url = 'http://openapi.tago.go.kr/openapi/service/ExpBusInfoService/getExpBusTrminlList?serviceKey='+key+'&numOfRows=1000&pageNo=1'
    req = requests.get(url)
    print(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    my_content = soup.select('body > items > item > terminalId')
    for content in my_content:
        naek.append(content.text)


# # 도시목록 end


def convert(strT):
    hour = int(strT[-4:-2])
    min = int(strT[-2:])
    date = int(strT[-8:-4])
    return hour*60+min
    
def sub(str1, str2):
    t1 = convert(str1)
    t2 = convert(str2)
    return t2-t1

def busInfoFind():
    for i in naek:
        # 터미널 코드 => 이름 찾기
        depTerminalId = 'NAEK010' # 출발 서울 경부
        # depTerminalId  = 'NAEK020 # 센트럴
        arrTerminalId = i # 도착
        depPlandTime = '20201122' #날짜
        busGradeId = ''
        queryParams = 'ServiceKey='+key+'&depTerminalId='+depTerminalId + '&arrTerminalId='+arrTerminalId+'&depPlandTime='+depPlandTime+'&numOfRows=1000&pageNo=1'
        url = 'http://openapi.tago.go.kr/openapi/service/ExpBusInfoService/getStrtpntAlocFndExpbusInfo?'+queryParams
        # print(url)
        req = requests.get(url)
        html = req.text
        row_index = 1
        soup = BeautifulSoup(html, 'html.parser')
        my_content = []
        # 츨발시간
        my_content = soup.select('body > items > item > depPlandTime')
        # 목적지 이름
        arrPlaceNm = []
        arrPlaceNm = soup.select('body > items > item > arrPlaceNm')
        j = 0
        ans = []
        avg = 0
        for content in my_content:
            if convert(content.text)<convert('202011120500'):
                continue
            if j == 0:
                pre = content.text
                j = j+1
                continue
            tmp  = sub(pre,content.text)
            ans.append(tmp)
            avg += tmp
            pre = content.text
            j = j+1
        if arrPlaceNm:
            if ans:
                # 이름 , 배차횟수 , 최소 , 최대 , 평균
                heapq.heappush(data,(arrPlaceNm[0].text,j,min(ans),max(ans),avg/(j-1)))
                # print(arrPlaceNm[0].text)
                # print('최소 = '+str(min(ans)))
                # print('최대 = '+str(max(ans)))
                # print('평균 = '+str(avg/(j-1)))
            else :
                heapq.heappush(data,(arrPlaceNm[0].text,j,0,0,0))

    heapq.heapify(data)

def printData():
    print(data)

def excelInput():
    wb = openpyxl.Workbook()
    sheet1 = wb.active
    for i in range(1,len(data)):   
        for j in range(5):
            sheet1.cell(row = i,column = j+1,value = data[i][j])
    wb.save('고속버스.xlsx')


findCityList()
busInfoFind()
excelInput()
printData()