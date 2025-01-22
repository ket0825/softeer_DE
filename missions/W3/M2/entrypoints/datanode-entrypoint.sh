#!/bin/bash
# datanode-entrypoint.sh
# 에러 발생 시 즉시 중단
set -e
# ssh 서비스 시작
sudo service ssh start

sudo mkdir -p /hadoop/dfs/data && \
sudo chown -R hduser:hduser /hadoop && \
sudo chmod -R 755 /hadoop

echo "Current JAVA_HOME: $JAVA_HOME"
echo "Java version: $(java -version)"

# HDFS 시작
$HADOOP_HOME/sbin/start-dfs.sh

# HDFS SafeMode 해제
$HADOOP_HOME/bin/hdfs dfsadmin -safemode leave

# # namenode 로그를 계속 모니터링하면서 컨테이너 실행 유지
tail -f $HADOOP_HOME/logs/hadoop-*-datanode-*.log
# 계속 실행
# tail -f /dev/null