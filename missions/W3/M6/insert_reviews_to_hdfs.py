import subprocess
import os
import time
import json

from datasets import load_dataset

def read_categories():
    with open("all_categories.txt") as f:
        return f.read().splitlines()

def insert_reviews_to_hdfs():
    categories = read_categories()
    output_dir = "amazon_reviews_data"
    hdfs_dir = "/users/hduser/amazon_reviews_input"
    
    # 로컬 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # HDFS 디렉토리 생성
    subprocess.run(f"hadoop fs -mkdir -p {hdfs_dir}", shell=True)
    
    for category in categories:
        print(f"Processing category: {category}")
        output_file = f"{output_dir}/raw_review_{category}.jsonl"
        
        try:
            # 데이터셋 로드
            dataset = load_dataset(
                "McAuley-Lab/Amazon-Reviews-2023", 
                f"raw_review_{category}", 
                trust_remote_code=True, 
                streaming=True
            )
            
            # 파일 열기
            with open(output_file, 'w') as f:
                # 처리 진행 상황 추적
                record_count = 0
                start_time = time.time()
                
                # 데이터 기록
                for record in dataset["full"]:
                    f.write(json.dumps(record) + '\n')
                    record_count += 1
                    
                    # 진행 상황 표시
                    if record_count % 10000 == 0:
                        elapsed = time.time() - start_time
                        print(f"Category {category}: Processed {record_count} records in {elapsed:.2f} seconds")
                
                print(f"Completed writing {record_count} records for {category}")
            
            # HDFS에 업로드
            print(f"Uploading {output_file} to HDFS...")
            upload_result = subprocess.run(
                f"hadoop fs -put -f {output_file} {hdfs_dir}/",
                shell=True
            )
            
            if upload_result.returncode == 0:
                print(f"Successfully uploaded {output_file} to HDFS")
                # 디스크 공간 절약을 위해 로컬 파일 삭제 (선택 사항)
                # os.remove(output_file)
            else:
                print(f"Failed to upload {output_file} to HDFS")
            
        except Exception as e:
            print(f"Error processing category {category}: {str(e)}")
            continue
        
        # API 제한 방지를 위한 짧은 대기 시간
        time.sleep(2)
    
    print("All categories processed and uploaded to HDFS")
        
        
if __name__ == "__main__":
    insert_reviews_to_hdfs()