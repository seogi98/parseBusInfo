# 고속버스 공공데이터포털 api 가져오기

# 1. 프로젝트 개요

서울 경부 , 센트럴에서 출발하는 고속버스의 배차 횟수 , 배차 시간을 구해서 저장해야할 일이 생겼기 때문에
간단한 프로젝트를 진행하였습니다. 요구사항은 다음과 같습니다.

- 서울 경부 , 센트럴에서 출발하는 고속버스 정보
- 일요일 5시 부터 24시 사이에 운행되는 버스의 수
- 버스 시간표의 배차 간격 최대, 최소, 평균값
- 가나다 순으로 액셀에 입력

첫번째로 고속버스 데이터를 가져와야 했기떄문에 공공데이터포털 api를 이용하여 데이터를 가져와야 했습니다.
또한 가져온 데이터를 액셀에 저장하여야 했기떄문에 가장 편하고 간단하게 사용할 수 있는 python을 사용 하였습니다.

# 2. 공공데이터포털 api 가져오기

[공공데이터포털 사이트](https://www.data.go.kr/)

첫번째로 공공 테이터 포털 api를 가져오기 위해선 사이트에 회원가입을 한 후에 활용신청을 하여 인증키를 받아와야 합니다. 
제공하는 일일 트래픽은 1000 이며 이 이상 사용하려면 운영계정 신청을 하여야합니다. 

인증 키를 받게되면 이제 데이터를 가져 올 수 있습니다. 데이터를 가져오기 위해서 다음을 import해야합니다.
``` py
from bs4 import BeautifulSoup
import requests
import time
```
그리고 난 후에 기본적으로 데이터를 넘겨주기 위해서 (주소 + 인증키 + 요청변수) 이러한 형식으로 
데이터를 보내야 합니다. 


# 3. API 요청 변수 확인하기

우리가 필요한 정보는 고속 버스의 정보 조회기떄문에 고속 버스 api를 사용해야 합니다. 
![캡처](https://user-images.githubusercontent.com/44061558/99324807-5b8d1c00-28b8-11eb-9869-0ba3622f6ef5.PNG)

이때 요청변수를 보내기 위해선 터미널 ID가 필요합니다. 따라서 
![캡처2](https://user-images.githubusercontent.com/44061558/99325258-48c71700-28b9-11eb-983a-e81deda8cf6e.PNG)를 통해 
터미널ID를 알 수 있습니다.

# 4. 데이터 가져오기

## 4.1 터미널 ID 가져오기

첫번째로 센트럴,서울 경부 터미널의 ID는 사이트에서 확인 할 수 있습니다.
서울 경부터미널은 NAEK010 , 센트럴은 NAEK020입니다. 코드는 서울 경부
터미널을 기준으로 설명하겠습니다. 요청변수는 다음과 같습니다.

- numOfRows = 한페이지 결과수
- pageNo = 페이지 번호
- terminalNm = 터미널명

포털에서 numOfRows사이즈를 넘겨주지않을경우 기본적으로 10개 만 출력합니다. 따라서 numOfRows = '10000' 로 넣어주고
pageNo = '1' 넣어준후 요청 변수 부분을 완성 합니다.
그후 (주소 + 인증키 + 요청변수)를 조합하여 URL을 완성합니다.

그후 우리가 필요한건 터미널 ID 이므로 'body > items > item > terminalId'부분만 선택하여서 my_content에 저장한 후 Naek배열에 모든 터미널 정보를 저장합니다.

```py
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
```

## 4.2 터미널 ID를 통해서 버스 정보 가져오기

요청 변수는 다음과 같습니다.
![캡처](https://user-images.githubusercontent.com/44061558/99324807-5b8d1c00-28b8-11eb-9869-0ba3622f6ef5.PNG)

Naek 배열에 지금 터미널의 ID가 저장 되어 있으므로
Naek 배열 요소들을 arrTerminalId에 넣어서 요청해 주면됩니다.

``` py
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
```

이때 우리가 필요한 정보는 목적지의 이름, 출발 시간이 필요하므로 다음 데이터를 가져옵니다.

``` py
# 츨발시간
my_content = soup.select('body > items > item > depPlandTime')
# 목적지 이름
arrPlaceNm = []
arrPlaceNm = soup.select('body > items > item > arrPlaceNm')
```

이때 가져온 데이터는 string형식으로 되어 있습니다. 따라서 

- string으로 되어있는 시간형식을 => 분 형식으로 바꿔주기
- 바꿔준 시간을 빼기

두 과정을 거처야지 데이터를 배차 시간을 알 수 있습니다. 가져오는 코드는 다음과 같습니다.

``` py
# 변환하기
def convert(strT):
    hour = int(strT[-4:-2])
    min = int(strT[-2:])
    date = int(strT[-8:-4])
    return hour*60+min
    
# 빼기 
def sub(str1, str2):
    t1 = convert(str1)
    t2 = convert(str2)
    return t2-t1

```

다음 코드는 데이터를 돌면서 각각의 데이터의 차이를 구하는 코드입니다.우리가 필요한 데이터는 5:00 ~ 24:00 의 데이터이므로
5:00 이전에 데이터가 들어 올 경우 데이터를 예외처리 해주고
각각의 데이터 차이를 구합니다.

그후에 data 에 (이름, 배차횟수, 최소, 최대, 평균)값을 삽입한후
heapq.heapity를 이용해서 데이터를 정렬되게 만듭니다.


``` py
for content in my_content:
    # 예외 데이터
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
```

# 5. 가져온 데이터를 액셀에 쓰기

액셀에 데이터를 쓰기 위해선 openyxl이 필요합니다.
``` py
import openpyxl
def excelInput():
    wb = openpyxl.Workbook()
    sheet1 = wb.active
    for i in range(1,len(data)):   
        for j in range(5):
            sheet1.cell(row = i,column = j+1,value = data[i][j])
    wb.save('고속버스.xlsx')
```
sheet1을 활성화 한 후에 data의 길이만큼
(1,1)부터 (len(data),5)까지 데이터를 저장합니다.



# 6. 전체 코드
``` python
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

```