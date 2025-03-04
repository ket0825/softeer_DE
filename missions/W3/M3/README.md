# Documentation
- Comprehensive documentation that guides users through compiling, running, and verifying the MapReduce job.
- Clear instructions on handling HDFS operations related to the input and output files.
    - Include steps for uploading the input file to HDFS and retrieving the output file.
- Document how to interpret the output and verify the results.

## Source
- [The just steward by Richard Dehan](https://www.gutenberg.org/ebooks/75518) copied 3 times to `sample_ebook.txt` in `missions/W3/M3` directory.

## Config
- To maximize the data parallelism (data locality), the block size should be set to 1MB.
- block size: 128MB -> 1MB

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
hdfs dfs -put /users/hduser/sample_ebook.txt /users/hduser
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
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar -files mapper.py,reducer.py -mapper "python3 mapper.py" -reducer "python3 reducer.py" -input /users/hduser/sample_ebook.txt -output /tmp/output
```

## Job 확인
- yarn UI: `http://localhost:8088`에서 확인 가능
- 상세한 application log를 확인하기 위해서는 datanode 자체의 port도 host에서 접근 가능해야 함.

## Output
```bash
...
“information    3
“plain  6
“project        15
“right  3
```

## Download
```bash
hdfs dfs -get /tmp/output .
# 혹은
# hdfs dfs -getmerge /tmp/output merged_output.txt
```