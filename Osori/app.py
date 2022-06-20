from flask import Flask, request, jsonify
import re
from selenium import webdriver
import random
from model_executer import get_simillar_tags

app = Flask(__name__)

# 감성 사전
emotion = {
  '행복':[
          '기분좋아','기분좋은데', '기분좋아서',',기분좋으니까', '기분좋을때', '기분좋다', '기분좋을',
          '좋아', '좋아서','좋은데','좋으니까', '좋을때', '좋다', '좋을',
          '행복해', '행복한데', '행복해서', '행복하니까', '행복할때', '행복한', '행복하다', '행복할'
          '설레', '설레는데', '설레서', '설레니까','설렐때','설렌다','설렐',
          '즐거워', '즐거운데', '즐거워서', '즐거우니까', '즐거울때', '즐겁다', '즐거울'
          '신나', '신나는데', '신나서', '신나니까', '신났어', '신났는데', '신났으니까', '신날때', '신난다', '신날',
          '기뻐', '기쁜데', '기뻐서', '기쁘니까', '기쁠때', '기쁘다', '기쁠',
          '사랑','행복','설렘', '즐거움', '기쁨', '기분좋음'
          ],
  '슬픔':[
          '힘들어', '힘들다', '힘든데', '힘들어서', '힘들때', '힘들', '힘든',
          '외로워', '외롭다', '외로운데', '외로워서', '외로울때', '외로울', '외로운',
          '슬퍼', '슬프다', '슬픈데', '슬퍼서', '슬플때', '슬플', '슬픈',
          '괴로워', '괴롭다', '괴로운데', '괴로워서', '괴로울때', '괴로울', '괴로운',
          '우울해', '우울하다', '우울한데', '우울해서', '우울할때', '우울할', '우울한',
          '센치해', '센치하다', '센치한데', '센치해서', '센치할때', '센치할', '센치한',
          '울적해', '울적하다', '울적한데', '울적해서', '울적할때', '울적할', '울적한',
          '안좋아', '안좋다', '안좋은데', '안좋아서', '안좋을때', '안좋을', '안좋은'
          '슬픔', '외로움', '힘듦', '괴로움', '우울', '센치', '우울함', '센치함'
          ],
  '분노':[
          '화나', '화난다', '화나는데', '화나서', '화날때', '화날', '화나는',
          '빡친다', '빡친다', '빡치는데', '빡쳐서', '빡칠때', '빡칠', '빡치는',
          '짜증나', '짜증난다', '짜증나는데', '짜증나서', '짜증날때', '짜증날', '짜증나는', '짜증난',
          '더러워', '더럽다', '더러운데', '더러워서', '더러울때', '더러울', '더러운',
          '스트레스', '분노', '짜증', '더러움', '빡침', '짜증남', '화남'
          ]
}

description = [
  '잔잔한', '몽환적인', '신나는', '분위기좋은', '감각','감각적인', '트렌디한',
  '트렌디', '세련', '세련된', '낭만적', '낭만적인', '낭만', '아련한', '애절한', '리드미컬',
  '희망찬','리듬', '비트', '추억', '달달한', '달달', '음색', '그루브', '그루비한','그루비',
  '감성', '감성적인', '도입부', '편안한', '섹시', '퇴폐', '퇴폐적인', '섹시한', '우아한',
  '웅장한', '감미로운','몽환', '레트로', '올드스쿨', '느낌있는', '느낌', '무드있는', '무드',
  '동양풍', '복고', '복고풍', '시원한', '빡센', '따뜻한', '따스한', '멜로디', '멜로디컬한', '따듯한',
  '청량한', '운치있는', '운치', '추억', '산뜻한', '달콤한', '노동요', '웃긴', '무서운', '몽롱한',
  '신비로운', '오래된', '신곡', '새로운', '인기', '최신', '옛날'
]

genre = [
  '힙합', '알앤비', '팝', '인디', '어쿠스틱', '댄스', '케이팝', '뉴에이지', '클래식', '락',
  '메탈', '헤비메탈', '록', '이디엠', '일렉', '일렉트로닉', '트로트', '월드뮤직',
  '재즈', '블루스', '컨트리', '포크', '일렉트로니카', '하우스', '클럽음악', '모던록', '하드록',
  '랩','하드코어랩', '갱스터', '소울', '국악', '국악크로스오버', '연주곡', '연주', '국내영화',
  '뮤지컬', '국내드라마', '보사노바', '라틴재즈', '오페라', '크로스오버', '현대음악', '성악',
  '합창곡', '샹송', '레게', '탱고', '플라멩코','브라질', '브라질리언', '동요', '만화',
  '자장가', '판소리', '풍물', '사물놀이', '민요', '아이돌', '남돌', '여돌', '캐롤', '캐럴',
  '피아노', '재즈피아노', '지브리', '애니', 'bgm'
]

situation = [
  '잠', '잠자기전', '여행', '드라이브', '휴가', '휴식', '술', '재택근무', '클럽', '봄',
  '여름', '피서', '가을', '겨울', '연말', '크리스마스', '새해', '명절',
  '운동', '카페', '매장', '게임', '응원', '숙면', '요가', '집중', '공부', '명상', '샤워',
  '청소', '퇴근', '하루', '지친', '파티', '힐링','배경음악', '2000년대', '2010년대',
  '80년대', '90년대', '00년대', '2000년대', '7080', '90', '새벽', '출근', '아침', '밤',
  '술집', '70년대', '과제', '지하철', '버스', '여유', '연휴', '주말', '일상', '평소',
  '페스티벌', '회상', '바다', '한강', '휴양지', '저녁', '산책', '노래방', '남자', '여자', '초여름',
  '초가을', '초겨울', '환절기', '집콕', '작업', '일', '외출', '편집샵', '새벽감성', '술',
  '비오는날', '비', '장마', '커피', '기차'
]


features = [[emotion, "emotion"], [description, "description"], [genre, "genre"], [situation, "situation"]]

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
def extract_musics(keys):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36")
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)

    if len(keys) == 1:
        url = f'https://www.melon.com/dj/djfinder/djfinder_inform.htm?djSearchType=T&djSearchKeyword=%23{keys[0]}'
    else:
        url = f'https://www.melon.com/dj/djfinder/djfinder_inform.htm?djSearchType=T&djSearchKeyword=%23{keys[0]}#params%5BdjSearchType%5D=T&params%5BdjSearchKeyword%5D=%23{keys[0]}%2C%23{keys[1]}&params%5BorderBy%5D=POP&params%5BpagingFlag%5D=Y&params%5BtagSearchType%5D=M&po=pageObj&startIndex=1'
    driver.get(url)
    playlists = driver.find_element_by_xpath('//*[@id="djPlylstList"]/div/ul').find_elements_by_tag_name('li')
    musics = []
    for pid in range(0, min([len(playlists), 4])):
        playlists[pid].click()
        p_len = len(driver.find_element_by_xpath('//*[@id="frm"]/div/table/tbody').find_elements_by_tag_name('tr'))
        lst = list(range(1, p_len + 1))
        cnt = max([int(8 / len(playlists)), 2])
        rand_num = random.sample(lst, cnt)
        for mid in rand_num:
            title = driver.find_element_by_xpath(
                f'//*[@id="frm"]/div/table/tbody/tr[{mid}]/td[5]/div/div/div[1]/span/a').text
            singer = driver.find_element_by_xpath(
                f'//*[@id="frm"]/div/table/tbody/tr[{mid}]/td[5]/div/div/div[2]/a').text
            musics.append(singer + ' ' + title + ' ' + "audio")
        driver.back()
    print('태그 : ', keys, '\n음악 : ', musics)
    return musics


# 컨트롤러
@app.route('/chat', methods=['POST'])
def chat():
    param = request.get_json()
    text = param['content']
    res = preprocessing(text)
    keywords = {}
    rand_arr = []
    idx = 0
    for feature in features:
        keywords[feature[1]] = get_feature_keywords(feature[0], res)
        if idx == 2:
            idx += 1
            continue
        if len(keywords[feature[1]]) != 0:
            rand_arr.append(idx)
        idx += 1
    print('키워드 : ', keywords)
    play_list = []

    rand_combi = -1 if len(rand_arr) < 2 else random.sample(rand_arr,2)

    all_tags = []
    if rand_combi != -1:
        rand_keyword1 = keywords[features[rand_combi[0]][1]]
        rand_keyword2 = keywords[features[rand_combi[1]][1]]
        rand_k1 = random.randint(0,len(rand_keyword1)-1)
        rand_k2 = random.randint(0,len(rand_keyword2)-1)
        play_list.extend(extract_musics([rand_keyword1[rand_k1],rand_keyword2[rand_k2]]))
    for keyword in keywords.keys():
        if len(keywords[keyword]) == 0:
            continue
        if keyword == 'genre':
            if len(keywords['genre']) > 2:
                rand_genre = random.sample(list(range(0,len(keywords['genre'])-1)),2)
                play_list.extend(extract_musics([keywords['genre'][rand_genre[0]],keywords['genre'][rand_genre[1]]]))
            else:
                play_list.extend(extract_musics(keywords['genre']))
            continue
        if rand_combi != -1:
            if keyword != features[rand_combi[0]][1] and keyword != features[rand_combi[1]][1]:
                rand_key = random.randint(0,len(keywords[keyword])-1)
                tags = get_simillar_tags(keywords[keyword][rand_key])
                print('대상 키워드 : ', keywords[keyword][rand_key], ' / 추출 태그 : ', tags)
                rand_k3 = random.randint(0, len(tags) - 1)
                play_list.extend(extract_musics([keywords[keyword][rand_key],tags[rand_k3]]))
        rand_all_key = random.randint(0, len(keywords[keyword]) - 1)
        all_tags.extend(get_simillar_tags(keywords[keyword][rand_all_key]))
        all_tags.append(keywords[keyword][rand_all_key])
        print(all_tags)

    if len(all_tags) != 0:
        if len(all_tags) == 1:
            play_list.extend(extract_musics([all_tags[0]]))
        else:
            rand_tags_num = random.sample(list(range(0, len(all_tags))), 2)
            play_list.extend(extract_musics([all_tags[rand_tags_num[0]],all_tags[rand_tags_num[1]]]))

    return jsonify({'playlist': play_list})


app.run(host='127.0.0.1', port=5001)
