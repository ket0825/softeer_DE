#!/usr/bin/env python3
# python shebang을 사용하여 리눅스 환경에서 실행할 수 있도록 함

import sys
import json

# 표준 입력에서 한 줄씩 읽기
for line in sys.stdin:
    # 공백 제거 및 소문자 변환
    line = line.strip().lower()
    
    review = json.loads(line)
    try:        
        
        item_id = review.get('parent_asin')
        rating = review.get('rating')
    except:
        continue
    else:
        print(f"{item_id}\t{rating}")