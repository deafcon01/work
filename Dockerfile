FROM ocdr/dkube-datascience-tf-gpu:v1.12
USER root
RUN mkdir -p /home/dkube/work
WORKDIR /home/dkube/work
RUN apt install -y vim libsm6 libxext6 libxrender-dev unzip
RUN pip3 install opencv-python json2xml lxml contextlib2

