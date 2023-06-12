import streamlit as st # 필요한 모듈
import numpy as np # 필요한 모듈
from itertools import permutations # 필요한 모듈
import random # 필요한 모듈

#모듈사용시 requirement.txt에 작성 


def randnum(): #각 자리수가 중복되지않는 4자리의 난수 생성 
    digits = ['0','1','2','3','4','5','6','7','8','9'] #각 자리수 
    nums=list(permutations(digits, 4)) #위 리스트에서 가능한 4개의 순열들(4자리 숫자) 을 모두 뽑은뒤 nums 에 list형태로 저장  
    random.shuffle(nums) # nums에 저장된숫자들을 무작위로 섞음
    return nums[0] #위에서 무작위로 섞은 숫자들중 첫번쨰 숫자 ( 난수 )를 리턴 

if 'number' not in st.session_state: #streamlit의 구조상 상호작용을 할때마다 새로고침되므로 변수에 저장된 값이 사라지지 않기 위해 작성 
    st.session_state.number = []  #number 변수를 빈 리스트로 초기화 
if 'i' not in st.session_state: #for문에 사용되는 변수 i 
    st.session_state.i = 0  #초기화
if 'randnums' not in st.session_state: #난수
    st.session_state.randnums = randnum() #randnums에 난수로 초기화 
if 'inputNum' not in st.session_state: #입력받은 숫자
    st.session_state.inputNum = "" #초기화
if 'inning' not in st.session_state: #시도횟수
    st.session_state.inning = 0 #초기화
if 'record' not in st.session_state: #게임 진행 기록 
    st.session_state.record = [] #초기화

def result(input,ball,strike): #입력값, ball,strike 를 매개변수로 넘겨받음 
    if(strike==4): #strike가 4일경우 
        st.write('# Victory') #승리 문자열 출력  
    elif(st.session_state.inning>=15): #시도횟수가 15회 이상일경우
        st.write('# Gameover') # 게임오버 문자열 출력
        st.write('정답은 ',str(st.session_state.randnums[0])+str(st.session_state.randnums[1])+str(st.session_state.randnums[2])+str(st.session_state.randnums[3]),' 입니다.')
        #게임의 정답을 출력 
        st.write('새로운 게임을 하시려면 F5를 눌려주세요. ') # 문자열 출력
    else:
        for i in range(st.session_state.inning+1): #게임의 진행횟수만큼 반복문 실행 
            st.session_state.record.append([]) #게임의 기록을 저장하기 위해 빈 배열 생성
            st.session_state.record[i].append([]) # 각회차마다의 정보를 기록하기위해 2차원 배열 생성
            st.session_state.record[i].append(input) #입력값
            st.session_state.record[i].append(ball) #볼
            st.session_state.record[i].append(strike) #스트라이크
            st.write(i+1,'회 입력숫자: ',st.session_state.record[i][1], st.session_state.record[i][2],' ball ',st.session_state.record[i][3],' strike ')

            #각 회차마다의 기록을 저장하여 출력 

def verify_digit(input): #입력 받은 값을 매개변수로 하여 검증   
    strike=0 #변수 초기화 
    ball=0 #초기화
    for i in range(4): #입력받은값은 문자열이므로 각 인덱스와 정답의 각 인덱스와 비교 
        if (st.session_state.randnums[i] == input[i]): #인덱스 0부터 3까지 비교 
            strike+=1 #입력숫자와 정답의 숫자와 자리가 둘다 일치할경우 strike 
        elif input[i] in st.session_state.randnums: #그렇지 않은경우 입력숫자의 각 인덱스가 정답에 있는지 확인
            ball+=1 # 숫자만 일치하는경우 이므로 ball 
    result(input,ball,strike) #검증이 끝나면 결과출력을 위해 result함수에 입력값과 ball과 strike 를 매개변수로 넘겨줌 

###################################################################################
st.write('# 숫자 야구 게임') #페이지에 문자열 출력 

if st.button('게임 규칙'): #버튼 클릭시 게임 규칙을 출력 
    st.write('숫자야구는 0부터 9까지의 각 자리의 수가 다른 네자리의 숫자를 추리하는 게임입니다.') #페이지에 문자열 출력
    st.write('1. 숫자는 맞지만 위치가 틀렸을때는 Ball') #페이지에 문자열 출력
    st.write('2. 숫자와 위치 모두 일치할 경우 Strike') #페이지에 문자열 출력
    st.write('3. 숫자와 위치 모두 틀렸을 경우 Out') #페이지에 문자열 출력
    st.write('4. 15번의 시도 후 정답을 맞히지 못한다면 Gameover 입니다.') #페이지에 문자열 출력
    st.session_state.inning-=1 #버튼 글릭시 시도횟수가 증가하는 버그 해결 
    if(st.session_state.inning<1): # 위 버그 해결후 처음 버튼클릭시 시도횟수가 -1,0 이 되는 버그 해결 
        st.session_state.inning=1 # 버그 해결 

input=st.text_input("0123부터 9876 사이의 숫자를 입력하세요 ",max_chars=4) #최대 4자리 수만 입력 
if input:  #input의 초기값은 빈 문자열 (False) 이므로 입력이 되었을때 (True) 아래의 내용 실행
    if len(input)==4 and input.isdigit() and input>='0123' and input<='9876'   :  #다음의 조건 모두 만족해야함 1.4자리의 입력 2.숫자만 입력 3.0123이상의 입력 4.9876이하의 입력 
        st.session_state.inputNum=input #입력받은값을 inputNum에 저장 
        verify_digit(input) #값을 입력받으면 검증실행 

        # st.write('정답: ',str(st.session_state.randnums[0])+str(st.session_state.randnums[1])+str(st.session_state.randnums[2])+str(st.session_state.randnums[3]))
        # st.write('입력숫자: ',st.session_state.inputNum)

        st.session_state.inning+=1 #위 수행이 끝나면 시도횟수 +1 
    else: #입력이 유효하지 않을경우 오류 출력 
        st.error('0123부터 9876 사이의 4자리 숫자만 입력하세요.') #페이지에 문자열 출력



#input>='0123' and input<='9876'이 문자열 사이에서도 정상작동 되는 이유는 문자열도 ascii 코드 값에 따라 비교연산을 하기 떄문 . 
