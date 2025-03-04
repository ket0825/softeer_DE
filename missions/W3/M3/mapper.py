#!/usr/bin/env python3
# python shebang을 사용하여 리눅스 환경에서 실행할 수 있도록 함

import sys

# 표준 입력에서 한 줄씩 읽기
for line in sys.stdin:
    # 공백 제거 및 소문자 변환
    line = line.strip().lower()
    
    # 공백을 기준으로 단어 분리
    words = line.split()
    
    # 각 단어마다 (단어, 1) 출력
    for word in words:
        # 탭으로 구분된 key-value 쌍 출력 (하둡 스트리밍 표준 포맷)
        print(f"{word}\t1")