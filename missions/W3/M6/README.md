## Config
- block size: 128MB -> 64MB

## Docker image build

```bash
# In project root
docker buildx build --load -t hadoop-base -f missions/W3/M6/Dockerfile .
```

## Docker compose

```bash
docker compose -f missions/W3/M6/docker-compose.yaml up
```

## Upload to HDFS (all_categories.txt를 읽고 HDFS에 각 카테고리별로 업로드하는 함수)

```bash
python3.10 insert_reviews_to_hdfs.py
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

## MapReduce 실행 (*.jsonl 파일을 읽음)

```bash
docker exec -it namenode /bin/bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar -files mapper.py,reducer.py -mapper "python3 mapper.py" -reducer "python3 reducer.py" -input /users/hduser/amazon_reviews_input/*.jsonl -output /tmp/output4
```

## Job 확인
- yarn UI: `http://localhost:8088`에서 확인 가능
- 상세한 application log를 확인하기 위해서는 datanode 자체의 port도 host에서 접근 가능해야 하는데, nodemanager의 로그는 컨테이너 내부에 있기 때문에 컨테이너 내부에서 확인해야 함(8042 포트로 접근해도 실패).

## Output
```bash
b0cdcpt7kd      2       4.0
b0cdgcc384      1       3.0
b0cdh5th82      75      4.3
b0cdnz7f2v      283     4.4
b0cdq8km21      20      4.0
b0cfgcvvhx      14      4.8
b0cfzkj4ky      2       5.0
b0chgdt817      2       3.5
```

## Download
```bash
hdfs dfs -get /tmp/output4 .
# 혹은
# hdfs dfs -getmerge /tmp/output2 merged_output.txt
```