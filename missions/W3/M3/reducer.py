#!/usr/bin/env python3

import sys

current_word = None
current_count = 0
word = None

# 표준 입력에서 한 줄씩 읽기 (맵퍼에서 정렬된 결과)
for line in sys.stdin:
    # 공백 제거
    line = line.strip()
    
    # 탭으로 구분된 입력에서 단어와 카운트 추출
    word, count = line.split('\t', 1)
    
    # 카운트를 정수로 변환
    try:
        count = int(count)
    except ValueError:
        # 카운트가 숫자가 아니면 무시
        continue
    
    # 하둡이 맵퍼 출력을 정렬하기 때문에, 같은 단어는 연속해서 입력됨
    if current_word == word:
        current_count += count
    else:
        if current_word:
            # 새 단어를 만나면 이전 단어의 결과 출력
            print(f"{current_word}\t{current_count}")
        # 새 단어로 초기화
        current_word = word
        current_count = count

# 마지막 단어 처리
if current_word == word:
    print(f"{current_word}\t{current_count}")