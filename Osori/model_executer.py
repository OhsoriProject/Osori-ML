import numpy as np
import copy

all_tags_fs = open(r'./crolled_melon_all_tags.txt', 'r')
all_tags_arr = all_tags_fs.read().split(',')

test_playlist_tags_fs = open(r'./crolled_melon_playlist_tags_test.txt', 'r')
# print(len(all_tags_arr))

model = np.load('./model.npy')


def get_simillar_tags(input_tag=None):
    # 태그를 input하면 가장 유사한 태그를 가져온다.
      if(input_tag == None):
        while True:
          input_str = input()
          flag = False
          if(input_str == 'quit'):
            break;
          for idx, x in enumerate(model):
            if all_tags_arr[idx] == input_str:
              # 여기서 상위 3개의 유사 태그를 찾는다.
              # x는 input_str의 array이다.
              max_score = [0,0,0,0,0]
              max_idx = [-1,-1,-1,-1,-1]
              for i in range(3):
                for idx_score, score in enumerate(x):
                  if score > max_score[i]:
                    if i>0 and max_score[i-1] <= score:
                      continue
                    max_score[i] = score
                    max_idx[i] = idx_score
              pass
              # print('유사한 태그는')
              if max_idx[0] != -1:
                flag = True
                print(all_tags_arr[idx], "=> ", end='')
                for i in range(5):
                  if max_idx[i] == -1:
                    break
                  print(all_tags_arr[max_idx[i]], end=' ')
                print()
              # print(all_tags_arr[idx],"=> ",all_tags_arr[max_idx[0]],
              # all_tags_arr[max_idx[1]], all_tags_arr[max_idx[2]],
              # all_tags_arr[max_idx[3]], all_tags_arr[max_idx[4]])
              # x의 최대값의 index가 있어야함
              # print(all_tags_arr[idx],"=> ", all_tags_arr[np.argmax(x)])


          if flag == False:
            print("찾는 태그가 없습니다.")
      else:
        input_str = input_tag
        ref_tags_arr = []
        for idx, x in enumerate(model):
            if all_tags_arr[idx] == input_str:
                max_score = [0, 0, 0, 0, 0]
                max_idx = [-1, -1, -1, -1, -1]
                for i in range(3):
                    for idx_score, score in enumerate(x):
                        if score > max_score[i]:
                            if i > 0 and max_score[i - 1] <= score:
                                continue
                            max_score[i] = score
                            max_idx[i] = idx_score
                pass
                for i in range(3):
                    if max_idx[i] == -1:
                        break
                    ref_tags_arr.append(all_tags_arr[max_idx[i]])

        return ref_tags_arr


def test_similar_tags():
    number_of_test_playlist = 26888;
    total_number_of_answer = 0;
    line = None
    while True:
        line = test_playlist_tags_fs.readline().strip()
        if (line == ''):
            break;
        playlist_line_arr = line.split(',')
        searched_tags_arr = get_simillar_tags(playlist_line_arr[0])
        playlist_line_length = len(playlist_line_arr)
        correct_count = 0
        for i in range(1, playlist_line_length):
            if playlist_line_arr[i] in searched_tags_arr:
                total_number_of_answer += 1

    print("정확도: ", total_number_of_answer / number_of_test_playlist)


# get_simillar_tags();
# test_similar_tags();


all_tags_fs.close()
