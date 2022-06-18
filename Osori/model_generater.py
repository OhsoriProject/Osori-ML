import numpy as np
import os

all_tags_fs = open(r'/Users/minseokkim/Osori-ML/Osori/crolled_melon_all_tags.txt', 'r')
playlist_tag_fs = open(r'/Users/minseokkim/Osori-ML/Osori/crolled_melon_playlist_tags_learn.txt', 'r')
all_tags_arr = all_tags_fs.read().split(',')
print(all_tags_arr)
# print(all_tags_arr.index('드라이브'))


# 태그의 array 만들기
cols = len(all_tags_arr)
rows = cols
# print(len(all_tags_arr))
model = np.zeros((cols,rows))
# arr = [[0 for j in range(cols)] for i in range(rows)]
print(model)


# array에 학습
line = None
while True:
  line = playlist_tag_fs.readline().strip()
  if(line == ''):
    break;
  playlist_line_arr = line.split(',')
  # print(playlist_line_arr)
  for x in playlist_line_arr:
    for y in playlist_line_arr:
      if(x != y):
        col = all_tags_arr.index(x);
        row = all_tags_arr.index(y);
        model[col][row] += 1;
        model[row][col] += 1;


np.save('./model.npy',model)


# for idx, x in enumerate(arr):
#   if(all_tags_arr[idx] == '일렉트로닉'):
#     print(all_tags_arr[idx],"=> ", all_tags_arr[np.argmax(x)])

# print(np.argmax(arr))
all_tags_fs.close()
playlist_tag_fs.close()

# print()