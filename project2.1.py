import pymysql
import requests
import urllib.request as req
import webbrowser 
from bs4 import BeautifulSoup
from datetime import datetime

global n 
n = 1

con = pymysql.connect()
cur = con.cursor()

def init():
    print("---------------------------------------------------")
    print("안녕하세요 숫자를 입력해주세요")
    print("화장실 주차장 찾기 프로그램 공주 입니다")
    print("<1> 로그인\n<2> 회원가입\n<3> 종료하기")
    print("---------------------------------------------------")
    pick = int(input())
    print("입력하신번호는 %d 입니다" %pick)
    return int(pick)

def login():
    print("-----------------------로그인화면--------------------------")
    id = input("아이디를 입력해주세요.\n")
    password = input("비밀번호를 입력해주세요.\n") 
    cur.execute("SELECT user_id,user_password from usertbl2 where user_id = '%s' AND user_password = '%s'" %(id,password))
    result = cur.fetchall()
    print(result) #test
    if len(result) < 1:
        print("로그인에 실패하였습니다. 다시시도해주세요.")
        return -1
    else :
        print("로그인 성공")
        return 0
    print("-----------------------로그인화면--------------------------")

def sign():
    print("-----------------------회원가입화면--------------------------")
    cur.execute("ALTER TABLE usertbl2 CONVERT TO CHARSET utf8;")
    id = input("아이디를 입력해주세요.\n")
    password = input("비밀번호를 입력해주세요.\n")
    addy =  input("ex.서울특별시 광진구 , ex.경기도 고양시 일산서구 입력해주세요\n")
    cur.execute("INSERT INTO `usertbl2` (`user_id`,`user_password`,`address`) VALUES ('%s','%s','%s')" %(id,password,addy))
    print("회원가입을 종료합니다.")
    print("-----------------------회원가입화면--------------------------")

def choiceBathPark():
    print("-----------------------화장실,주차장,화장실헤드라인,개인정보(수정) 선택화면--------------------------")
    print("<1> 화장실 선택\n<2> 주차장 선택\n<3> 화장실헤드라인\n<4> 개인정보수정")
    pick= int(input())
    print("입력하신번호는 %d 입니다" %pick)
    print("-----------------------화장실,주차장,화장실헤드라인,개인정보(수정) 선택화면--------------------------")
    return  int(pick)

def readyToilet():
    print("-----------------------화장실준비화면--------------------------")
    print("<1> 화장실 검색\n<2> 화장실 등록\n<3> 화장실 삭제")
    pick= int(input())
    print("입력하신번호는 %d 입니다" %pick)
    if pick  == 1:
        findToilet()
    elif pick == 2:
        enrollToilet()
    elif pick == 3:
        deleteToilet()
    print("-----------------------화장실준비화면--------------------------")

def findToilet():
    print("-----------------------화장실검색화면--------------------------")
    print("화장실은 현재 아이디 위치 기반하여 알려드립니다.")
    cur.execute("SELECT a.toil_name, a.address FROM `toiltbl2` a JOIN `usertbl2` b ON SUBSTRING(a.address, 1, 12) = SUBSTRING(b.address, 1, 12)")
    result = cur.fetchall()
    for i in range(len(result)):
         print("화장실 이름 : ", result[i][0], "\n화장실 주소 : ", result[i][1])    
    print("-----------------------화장실검색화면--------------------------")

def enrollToilet():
    print("-----------------------화장실등록화면--------------------------")
    cur.execute("ALTER TABLE toiltbl2 CONVERT TO CHARSET utf8;")
    cur.execute("SELECT MAX(id) FROM toiltbl2")
    max_id = cur.fetchone()[0]  #쿼리의 결과 집합에서 한 행(row)을 가져오는 메서드
    new_id = max_id +1
    category = input("공중화장실/사설화장실 입력해주세요.\n")
    toil_name =  input("화장실이름이나 건물이름/위치을 적어주세요.\n")
    phone_number = input("전화번호를 적어주세요.\n")
    address = input("주소(도로명)를 적어주세요. ex)서울 광진구 능동로 216\n")
    cur.execute("INSERT INTO `toiltbl2` (`id`,`category`,`toil_name`,`phone_number`,`address`) VALUES ('%s','%s','%s','%s','%s')" %(new_id,category,toil_name,phone_number,address))
    print("-----------------------화장실등록화면--------------------------")

def deleteToilet():
    print("-----------------------화장실삭제화면--------------------------")
    toil_name = input("화장실이름이나 건물이름/위치을 적어주세요.\n")
    cur.execute("DELETE FROM `toiltbl2` WHERE toil_name =  %s" %(toil_name))
    print("-----------------------화장실삭제화면--------------------------")

def readyParking():
    print("-----------------------주차장 준비화면--------------------------")
    print("<1> 주차장 검색\n<2> 주차장 등록\n<3> 주차장 삭제")
    pick= int(input())
    print("입력하신번호는 %d 입니다" %pick)
    if pick  == 1:
        findParking()
    elif pick == 2:
        enrollParking()
    elif pick == 3:
        deleteParking()
    print("-----------------------주차장 준비화면--------------------------")

def findParking():
    print("-----------------------주차장 검색화면--------------------------")
    print("주차장은 현재 아이디 위치 기반하여 알려드립니다.")
    cur.execute("SELECT a.park_name, a.address FROM `parktbl2` a JOIN `usertbl2` b ON SUBSTRING(a.address, 1, 12) = SUBSTRING(b.address, 1, 12)")
    result = cur.fetchall()
    for i in range(len(result)):
         print("주차장 이름 : ", result[i][0], " 주차장 주소 : ", result[i][1])
    print("혹시 정확한 지도(그림)을 원하시나요 ?")
    print("<1> 예.\n<2> 아니오.")
    map_num = int(input())
    if map_num == 1:
        print("지도를 보기 원하셨습니다.")
        print("주차장 이름을 정확하게 적어주세요.")
        parking_name =input()
        show_map(parking_name)
    print("-----------------------주차장 검색화면--------------------------")

def enrollParking():
    print("-----------------------주차장 등록화면--------------------------")
    cur.execute("ALTER TABLE parktbl2 CONVERT TO CHARSET utf8;")
    park_name = input("주차장이름을 입력해주세요.\n")
    address =  input("화장실 도로명주소를 입력해주세요 ex)경기도 고양시 일산동구 호수로 595.\n")
    fee = input("유료/무료/혼합 입력해주세요.\n")
    phone_number = input("전화번호를 입력해주세요 ex)031-925-9930\n")
    cur.execute("INSERT INTO `parktbl2` (`num`,`park_name`,`address`,`phone_number`) VALUES (now(),'%s','%s','%s','%s')" %(park_name,address,fee,phone_number))
    print("-----------------------주차장 등록화면--------------------------")

def deleteParking():
    print("-----------------------주차장 삭제화면--------------------------")
    toil_name = input("화장실이름이나 건물이름/위치을 적어주세요.\n")
    cur.execute("DELETE FROM `toiltbl2` WHERE toil_name =  %s" %(toil_name))
    print("-----------------------주차장 삭제화면--------------------------")

def reviseinformation():
    print("-----------------------개인정보 수정 화면--------------------------")
    cur.execute("ALTER TABLE usertbl2 CONVERT TO CHARSET utf8;")
    password = input("수정하실 패스워드를 입력하세요.")
    address = input("수정하실 주소를 입력하세요.")
    cur.execute("UPDATE SET `usertbl2` SET `user_password` =%s , `address` = %s" %(password,address))
    print("-----------------------개인정보 수정 화면--------------------------")

def readNews():
    print("-----------------------IT 헤드라인만 취급합니다.--------------------------")
    n = 1
    yyyymmdd = datetime.today().strftime("%Y%m%d")
    int(yyyymmdd)
    for page in range(1, 5):
        url = f"https://news.naver.com/main/list.naver?mode=LS2D&sid2=230&sid1=105&mid=shm&date={yyyymmdd}&page={page}" # 앞에 f 붙여줘야 변수라고 생각함 {} 이게
        openurl = req.urlopen(url)
        soup = BeautifulSoup(openurl, "html.parser")

        a_list = soup.select("div.list_body.newsflash_body>ul>li>dl>dt>a")
        for a in a_list:
            name = a.string
            if name is not None:
                name = name.strip()
                print("----%d 번째 기사 제목입니다---" %n)
                n+=1
                print(name)
    print("-----------------------IT 헤드라인만 취급합니다.--------------------------")

def show_map(parking_name): # https://www.openstreetmap.org/#map=19/위도/경도 사용할거  
    print("-----------------------지도 보는 화면--------------------------")
    parking_three = parking_name[:3]  # 첫 글자만 검사 오타방지
    cur.execute("SELECT `latitude`, `longitude` FROM `parktbl2` WHERE `park_name` LIKE %s", (f"{parking_three}%",))
    result = cur.fetchall()
    if result:
        latitude = result[0][0]
        longitude = result[0][1]
        url = f"https://www.openstreetmap.org/#map=19/{latitude}/{longitude}"
        webbrowser.open(url)
        print("지도를 열었습니다.")
    else:
        print("주차장 정보를 찾을 수 없습니다.")
    print("-----------------------지도 보는 화면--------------------------")

while True:
    init_input = init()
    if init_input == 1: # 로그인
        login_num =login()
        if login_num == -1:
            continue
        choice_num =choiceBathPark()
        if choice_num == 1:
            readyToilet()
        elif choice_num ==2:
            readyParking()
        elif choice_num ==3:
            readNews()
        elif choice_num == 4:
            reviseinformation()
        else : 
            print("1번 2번 3번 4번 중에 골라주세요.")            
    elif init_input == 2: # 회원가입
        sign()
    elif init_input == 3: # 종료하기
        print("종료하겠습니다.")
        con.commit()
        break
    else :
        print("1번 2번 3번중에 골라주세요.")
        con.commit()

con.commit()

