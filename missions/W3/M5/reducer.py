#!/usr/bin/env python3

import sys

current_movie_id = None
current_rating_sum = 0
current_rating_count = 0

# 표준 입력에서 한 줄씩 읽기 (맵퍼에서 정렬된 결과)
for line in sys.stdin:
    # 공백 제거
    line = line.strip()
    
    # 탭으로 구분된 입력에서 단어와 카운트 추출
    movie_id, rating = line.split('\t', 1)
    
    # 카운트를 정수로 변환
    try:
        rating = float(rating)
        movie_id = movie_id.strip()
    except ValueError:
        # 카운트가 숫자가 아니면 무시
        continue
    
    # 하둡이 맵퍼 출력을 정렬(sort)하기 때문에, 같은 단어는 연속해서 입력됨
    if movie_id == current_movie_id:
        current_rating_sum += rating
        current_rating_count += 1
    else:
        # 일단 평균 평점 출력 이후, 새로운 단어에 대한 초기화
        if current_movie_id:
            print(f"{current_movie_id}\t{(current_rating_sum / current_rating_count):.2f}")
        current_movie_id = movie_id
        current_rating_sum = rating
        current_rating_count = 1

if current_movie_id:
    print(f"{current_movie_id}\t{(current_rating_sum / current_rating_count):.2f}")    