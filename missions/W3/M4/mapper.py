#!/usr/bin/env python3
# python shebang을 사용하여 리눅스 환경에서 실행할 수 있도록 함

import sys

# 표준 입력에서 한 줄씩 읽기
for line in sys.stdin:
    # 공백 제거 및 소문자 변환
    line = line.strip().lower()            
    
    try:
        sentiment = line.split(",")[0]
        sentiment = sentiment.strip('"')
        if sentiment not in ["0", "2", "4"]:
            continue
    except:
        continue
    
    if sentiment == "0":
        print("negative\t1")
    elif sentiment == "2":
        print("neutral\t1")
    elif sentiment == "4":
        print("positive\t1")
    else:
        continue    