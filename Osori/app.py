from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# 감성 사전
emotional_feature = {
    '행복': ['좋', '좋다', '최고', '행복', '기쁘다', '기쁘', '기쁨', '신', '신난다', '신나'],
    '슬픔': ['슬픔', '슬프', '슬프다', '우울', '우울하다', '눈물', '외로움', '외롭', '외롭다'],
    '분노': ['화', '화나', '짜증', '분노', '열', '열받']
}
atomsphere_feature = {
    '잔잔': ['잔잔', '잔잔하다', '잔잔한', '조용', '조용한', '차분', '차분한', '차분하다'],
    '몽환': ['몽환', '몽환적인', '몽환적이다', '몽롱', '몽롱한', '몽롱하다'],
    '경쾌': ['경쾌한', '경쾌하다', '신나는', '신난다', '신나']
}
genre_feature = ['재즈', '힙합', '발라드', '랩', '클래식', '알앤비', '인디', '댄스', '뉴에이지', '록', '팝', 'OST', 'EDM', '트로트', '블루스', '컨트리',
                 '레게']
situation_feature = ['드라이브', '운동', '헬스', '여행']
negative_word_emotion = ['안', '않', '못', '없', '아닌', '아니']


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


def temporary_song_list():
    songs = ["24KGolden Mood audio", "IU 금요일에 만나요 audio", "IU 금요일에 만나요 audio"]
    return songs


# 컨트롤러
@app.route('/chat', methods=['POST'])
def chat():
    param = request.get_json()
    text = param['content']
    res = preprocessing(text)
    keywords = get_feature_keywords(genre_feature, res)
    print('키워드 : ', keywords)
    play_list = temporary_song_list()
    return jsonify({'playlist': play_list})


app.run(host='127.0.0.1', port=5000)
