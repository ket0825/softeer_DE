## Config
- block size: 128MB -> 64MB

## Docker image build

```bash
# In project root
docker buildx build --load -t hadoop-base -f missions/W3/M3/Dockerfile .
```

## Docker compose

```bash
docker compose -f missions/W3/M3/docker-compose.yaml up
```

## Upload to HDFS

```bash
docker exec -it namenode /bin/bash
hdfs dfs -put /home/hduser/training.1600000.processed.noemoticon.csv /users/hduser
```

## mapper.py
```python
#! /usr/bin/env python3
# python shebang 필수.

# 그 외 stdin 등으로 입력을 받아 출력을 하는 코드.
```

## reducer.py
```python
#! /usr/bin/env python3
# python shebang 필수.

# 그 외 stdin 등으로 입력을 받아 출력을 하는 코드.
```

## MapReduce 실행

```bash
docker exec -it namenode /bin/bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar -files mapper.py,reducer.py -mapper "python3 mapper.py" -reducer "python3 reducer.py" -input /users/hduser/training.1600000.processed.noemoticon.csv -output /tmp/output2
```

## Job 확인
- yarn UI: `http://localhost:8088`에서 확인 가능
- 상세한 application log를 확인하기 위해서는 datanode 자체의 port도 host에서 접근 가능해야 하는데, nodemanager의 로그는 컨테이너 내부에 있기 때문에 컨테이너 내부에서 확인해야 함(8042 포트로 접근해도 실패).

## Output
```bash
negative        800000
positive        800000
```

## Download
```bash
hdfs dfs -get /tmp/output2 .
# 혹은
# hdfs dfs -getmerge /tmp/output2 merged_output.txt
```

## Log 확인 및 분석
```bash
hdfs dfs -cat /tmp/logs/hduser/bucket-logs-tfile/0001/application_1741147780718_0001/4e8c3065aed1_36075
```

- hadoop streaming으로 표준 입출력으로 Java가 아닌 Python 코드를 실행할 때, Python 코드를 작동시킬 수 있습니다.
1. Yarn에서 AM을 위한 MRAppMaster 컨테이너 할당
2. AM은 작업 초기화 및 실행 계획 설정
    - job.xml
    - 작업 split 정보
    - 필요한 Map 및 reduce 태스크 수 결정
3. AM은 RM에 Map Reduce 태스크를 위한 컨테이너 요청
4. RM이 컨테이너 할당 및 각 Map 태스크에 컨테이너 할당.
5. 태스크 런처로 컨테이너에 대해 실행 환경 변수 및 class path가 설정 (lanunch_container.sh)
6. 태스크 파일 컨테이너 내부로 복사 혹은 심볼릭 링크 생성 (job.xml, job.jar, mapper.py, reducer.py)
7. Map 태스크 실행
    - mapper.py 실행
    - 출력을 로컬 디스크에 저장
8. Map 태스크 출력 Shuffle
    - Map 출력을 정렬하고 파티션에 따라 그룹화
    - Map 출력을 Reduce 태스크로 전송
9. Reduce 태스크 실행
    - reducer.py 실행
    - Sort (Merge) 및 그룹화
    - 메모리에 다 들어가지 않으면 외부 정렬 수행 (spill to disk. **combiner 사용으로 최적화 가능!**)
10. 작업 완료 및 HDFS에 출력 저장