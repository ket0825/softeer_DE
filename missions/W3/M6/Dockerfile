# ubuntu-20.04 base.
FROM eclipse-temurin:8-jdk-focal

# 필수 패키지 설치
# DEBIAN_FRONTEND=noninteractive: apt-get install 시 interactive 설정을 무시하고 설치 진행 (모두 yes로 설정)
RUN apt-get update -y \
    && export DEBIAN_FRONTEND=noninteractive && apt-get install -y --no-install-recommends \
        sudo \
        curl \
        ssh \
    && apt-get clean
# 계정 생성과 동시에 홈 디렉토리에 생성
# hduser 계정 및 패스워드 설정
# 파이프라인 |을 사용하여 바로 useradd 명령어의 인수로 전달
# hduser 계정에 sudo 권한 부여
# hduser가 명령 수행 시 패스워드를 물어보지 않도록 설정 (/etc/sudoers 파일에 hduser 계정에 대한 NOPASSWD 설정 추가)
# /usr/bin 디렉토리에 python3 바이너리를 python으로 링크
RUN useradd -m hduser && echo "hduser:supergroup" | chpasswd && adduser hduser sudo && echo "hduser     ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && cd /usr/bin/ && sudo ln -s python3 python

WORKDIR /home/hduser
USER hduser
# 
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && chmod 0600 ~/.ssh/authorized_keys
ENV HADOOP_VERSION=3.3.3
ENV HADOOP_HOME=/home/hduser/hadoop-${HADOOP_VERSION}

RUN curl -sL --retry 3 \
  "http://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz" \
  | gunzip \
  | tar -x -C /home/hduser/ \
 && rm -rf ${HADOOP_HOME}/share/doc

ENV HDFS_NAMENODE_USER=hduser
ENV HDFS_DATANODE_USER=hduser
ENV HDFS_SECONDARYNAMENODE_USER=hduser

ENV YARN_RESOURCEMANAGER_USER=hduser
ENV YARN_NODEMANAGER_USER=hduser

RUN sudo apt-get install -y software-properties-common \
    && sudo add-apt-repository -y ppa:deadsnakes/ppa \
    && sudo apt-get update -y \
    && sudo apt-get install -y python3.10 python3.10-dev python3.10-distutils python3.10-venv python3-setuptools

# Python 3.10용 pip 설치
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.10 get-pip.py \
    && rm get-pip.py

# Python 심볼릭 링크 설정 및 pip 심볼릭 링크 추가
RUN cd /usr/bin/ \
    && sudo rm -rf python \
    && sudo ln -s python3.10 python \
    && sudo ln -s pip3.10 pip \
    && sudo apt-get clean \
    && sudo rm -rf /var/lib/apt/lists/* \
    && sudo rm -rf /tmp/*

# datasets 패키지 설치 (이전 위치에서)
RUN python -m pip install --no-cache-dir datasets

COPY missions/W3/M6/ssh_config /etc/ssh/ssh_config
ENV JAVA_HOME=/opt/java/openjdk/
RUN echo "export JAVA_HOME=/opt/java/openjdk/" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

COPY missions/W3/M6/entrypoints/ /home/hduser/
COPY missions/W3/M6/hadoop-configs/* $HADOOP_HOME/etc/hadoop/

ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin
ENV LD_LIBRARY_PATH=$HADOOP_HOME/lib/native

EXPOSE 50070 50075 50010 50020 50090 8020 9000 9864 9870 10020 19888 8088 8030 8031 8032 8033 8040 8042 22

USER root
RUN echo "export JAVA_HOME=/opt/java/openjdk" > /etc/profile.d/java.sh && \
    echo "export PATH=\${JAVA_HOME}/bin:\${PATH}" >> /etc/profile.d/java.sh && \
    chmod +x /etc/profile.d/java.sh && \
    echo "PermitUserEnvironment yes" >> /etc/ssh/sshd_config && \
    mkdir -p /home/hduser/.ssh && \
    echo "JAVA_HOME=/opt/java/openjdk" >> /home/hduser/.ssh/environment && \
    chown -R hduser:hduser /home/hduser/.ssh && \
    chmod 600 /home/hduser/.ssh/environment

USER hduser
WORKDIR /usr/local/bin
WORKDIR /home/hduser

COPY missions/W3/M6/*.py /home/hduser/
COPY missions/W3/M6/*.txt /home/hduser/

# YARNSTART=0 will prevent yarn scheduler from being launched
ENV YARNSTART=1

# docker run -d -it\
#     -p 9864:9864 \
#     -p 9870:9870 \
#     -p 8088:8088 \
#     -p 9000:9000 \
#     --mount type=volume,source=hadoop_namenode,target=/hadoop/dfs/name \
#     --mount type=volume,source=hadoop_datanode,target=/hadoop/dfs/data \
#     --hostname hadoop-single \
#     sample-hadoop-standalone /bin/bash

