## Config
- block size: 128MB -> 64MB

## Docker image build

```bash
# In project root
docker buildx build --load -t hadoop-base -f missions/W3/M5/Dockerfile .
```

## 데이터 확인

```bash
head -n 10 ratings.csv
```

## Docker compose

```bash
docker compose -f missions/W3/M5/docker-compose.yaml up
```

## Upload to HDFS

```bash
docker exec -it namenode /bin/bash
hdfs dfs -put /home/hduser/ratings.csv /users/hduser
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
# 평균 연산을 위한 누적합과 카운트 변수를 사용할 수 있음.
```

## MapReduce 실행

```bash
docker exec -it namenode /bin/bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar -files mapper.py,reducer.py -mapper "python3 mapper.py" -reducer "python3 reducer.py" -input /users/hduser/ratings.csv -output /tmp/output3
```

## Job 확인
- yarn UI: `http://localhost:8088`에서 확인 가능
- 상세한 application log를 확인하기 위해서는 datanode 자체의 port도 host에서 접근 가능해야 하는데, nodemanager의 로그는 컨테이너 내부에 있기 때문에 컨테이너 내부에서 확인해야 함(8042 포트로 접근해도 실패).

## Output
```bash
...
99989   3.60
99992   3.09
99994   2.96
99996   3.50
99999   3.38
```

## Download
```bash
hdfs dfs -get /tmp/output3 .
# 혹은
# hdfs dfs -getmerge /tmp/output2 merged_output.txt
```