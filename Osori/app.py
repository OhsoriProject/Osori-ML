from flask import Flask, request, jsonify
import re
from selenium import webdriver
import random

app = Flask(__name__)

# 감성 사전
emotion = {
    '행복': ['사랑', '설렘', '기분전환', '신난다', '좋아', '짱', '기분좋은', '감동', '기분좋아', '행복하다', '행복', '기쁘다', '즐겁다', '기분좋다', '좋다', '설레다',
           '기쁨', '기쁜', '행복한', '즐거운', '설레는', '신나'],
    '슬픔': ['힘들다', '외롭다', '슬프다', '슬픔', '외로움', '괴로움', '괴롭다', '우울하다', '센치하다', '울적하다', '우울', '기분안좋다', '안좋다', '힐링', '스트레스',
           '이별', '외로워', '슬퍼', '우울해', '기분안좋아', '안좋아', '울적해', '스트레스받아'],
    '분노': ['화난다', '빡쳐', '개빡친다', '좆같애', '좆같아', '지랄같아', '괴롭다', '짜증나다', '짜증', '화', '화나', '기분더러워', '더러워', '더러움', '더럽다',
           '괴로워', '짜증나', '개빡쳐'],
}

description = [
    '잔잔한', '몽환적인', '신나는', '분위기좋은', '감각', '감각적인', '트렌디한', '트렌디', '세련', '세련된', '낭만적', '낭만적인', '낭만', '아련한', '애절한', '리드미컬',
    '슬픈', '희망찬',
    '리듬', '비트', '추억', '달달한', '달달', '음색', '그루브', '그루비한', '그루비', '감성', '감성적인', '도입부', '편안한', '섹시', '퇴폐', '퇴폐적인', '섹시한',
    '우아한', '웅장한', '감미로운',
    '몽환', '레트로', '올드스쿨', '느낌있는', '느낌', '무드있는', '무드', '동양풍', '복고', '복고풍', '시원한', '빡센', '따뜻한', '따스한', '멜로디', '멜로디컬한',
    '따듯한',
    '청량한', '운치있는', '운치', '추억', '산뜻한', '달콤한', '노동요', '웃긴', '무서운', '몽롱한', '신비로운', '오래된', '신곡', '새로운'
]

genre = [
    '힙합', '알앤비', '팝', '인디', '어쿠스틱', '댄스', '케이팝', '뉴에이지', '클래식', '락',
    '메탈', '헤비메탈', '록', '이디엠', '일렉', '일렉트로닉', '트로트', '월드뮤직',
    '재즈', '블루스', '컨트리', '포크', '일렉트로니카', '하우스', '클럽음악', '모던록', '하드록', '랩',
    '하드코어랩', '갱스터', '소울', '국악', '국악크로스오버', '연주곡', '연주', '국내영화', '뮤지컬', '국내드라마', '보사노바',
    '라틴재즈', '오페라', '크로스오버', '현대음악', '성악', '합창곡', '샹송', '레게', '탱고', '플라멩코',
    '브라질', '브라질리언', '동요', '만화', '자장가', '판소리', '풍물', '사물놀이', '민요', '아이돌', '남돌', '여돌', '캐롤', '캐럴', '피아노', '재즈피아노', '지브리',
    '애니',
    'bgm'
]

situation = [
    '잠', '잠자기전', '여행', '드라이브', '휴가', '휴식', '술', '재택근무', '클럽', '봄', '여름', '피서', '가을', '겨울', '연말', '크리스마스', '새해', '명절',
    '운동', '카페', '매장', '게임', '응원', '숙면', '요가', '집중', '공부', '명상', '샤워', '청소', '퇴근', '하루', '지친', '파티',
    '배경음악', '2000년대', '2010년대', '80년대', '90년대', '00년대', '2000', '7080', '90', '새벽', '출근', '아침', '밤', '술집', '70년대',
    '과제', '지하철', '버스', '여유', '연휴', '주말', '일상', '평소', '페스티벌', '회상', '바다', '한강', '휴양지', '저녁', '산책', '노래방', '남자', '여자',
    '초여름',
    '초가을', '초겨울', '환절기', '집콕', '작업', '일', '외출', '편집샵', '새벽감성', '비오는날', '비', '장마', '커피', '기차'
]

features = [emotion, description, genre, situation]


# 문장 전처리
def preprocessing(ch):
    result = ''
    r = ch
    sentence = re.sub('([a-zA-Z])', '', r)
    sentence = re.sub('[ㄱ-ㅎㅏ-ㅣ]+', '', sentence)
    sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', sentence)
    result += sentence
    print('전처리 : ', result)
    return result


# 키워드 추출
def get_feature_keywords(feature, chat):
    key = []
    morphs = chat.split()
    print('문장 분석 : ', morphs)
    if type(feature) is dict:
        for keyword in feature.keys():
            for mo in morphs:
                if mo in feature[keyword]:
                    key.append(keyword)
    if type(feature) is list:
        for keyword in feature:
            for mo in morphs:
                if mo == keyword:
                    key.append(keyword)
    return key


# 노래 추출
def extract_musics(key1, key2):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36")
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    url = f'https://www.melon.com/dj/djfinder/djfinder_inform.htm?djSearchType=T&djSearchKeyword=%23{key1}#params%5BdjSearchType%5D=T&params%5BdjSearchKeyword%5D=%23{key1}%2C%23{key2}&params%5BorderBy%5D=POP&params%5BpagingFlag%5D=Y&params%5BtagSearchType%5D=M&po=pageObj&startIndex=1'
    driver.get(url)
    playlists = driver.find_element_by_xpath('//*[@id="djPlylstList"]/div/ul').find_elements_by_tag_name('li')
    musics = []
    for pid in range(0, 4):
        playlists[pid].click()
        p_len = len(driver.find_element_by_xpath('//*[@id="frm"]/div/table/tbody').find_elements_by_tag_name('tr'))
        lst = list(range(1, p_len + 1))
        print(p_len)
        rand_num = random.sample(lst, 2)
        for mid in rand_num:
            title = driver.find_element_by_xpath(
                f'//*[@id="frm"]/div/table/tbody/tr[{mid}]/td[5]/div/div/div[1]/span/a').text
            singer = driver.find_element_by_xpath(
                f'//*[@id="frm"]/div/table/tbody/tr[{mid}]/td[5]/div/div/div[2]/a').text
            musics.append(singer + ' ' + title + ' ' + "audio")
        driver.back()
    return musics


# 컨트롤러
@app.route('/chat', methods=['POST'])
def chat():
    param = request.get_json()
    text = param['content']
    res = preprocessing(text)
    keywords = []
    for feature in features:
        keywords.extend(get_feature_keywords(feature, res))
    print('키워드 : ', keywords)
    play_list = extract_musics(keywords[0], keywords[1])
    return jsonify({'playlist': play_list})


app.run(host='127.0.0.1', port=5000)
