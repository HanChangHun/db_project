# docker build --no-cache -t db40 .

FROM postgres:lastest

RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
RUN sed -i 's/kr.archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
RUN sed -i 's/security.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
RUN sed -i 's/extras.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y sudo apt-utils build-essential python3 python3-pip python3-dev git git-core libpq-dev libsm6 libxext6 libxrender-dev curl openssl libssl-dev nginx libgl1-mesa-glx libzbar0

# Install
RUN pip3 install --upgrade pip
RUN pip3 install numpy pandas tqdm opencv-python beautifulsoup4 sqlalchemy psycopg2 PyQt5 pyzbar


RUN git clone https://github.com/HanChangHun/db_project
RUN cd db_project
RUN su postgres "createdb projectDB"
RUN python3 upload_data.py --user postgres --pwd 1234 --db projectDB --host localhost --port 5432