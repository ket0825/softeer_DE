#!/usr/bin/env python3

import sys

current_item_id = None
current_rating_sum = 0
count = 0

# 표준 입력에서 한 줄씩 읽기 (맵퍼에서 정렬된 결과)
for line in sys.stdin:
    # 공백 제거
    line = line.strip()
    
    # 탭으로 구분된 입력에서 단어와 카운트 추출
    item_id, rating = line.split('\t', 1)
    
    # 카운트를 정수로 변환
    try:
        rating = float(rating)
    except ValueError:
        # 카운트가 숫자가 아니면 무시
        continue        
    if current_item_id == item_id:
        current_rating_sum += rating
        count += 1
    else:
        # 일단 평균 평점 출력 이후, 새로운 단어에 대한 초기화
        if current_item_id:
            print(f"{current_item_id}\t{count}\t{(current_rating_sum / count):.1f}")
        current_item_id = item_id
        current_rating_sum = rating
        count = 1

# 마지막 단어 처리
if current_item_id:
    print(f"{current_item_id}\t{count}\t{(current_rating_sum / count):.1f}")