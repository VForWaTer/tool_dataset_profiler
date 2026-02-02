# Pull any base image that includes python3
FROM python:3.12

# install the toolbox runner tools
RUN pip install "json2args>=0.7.0"

# install tool dependencies
RUN pip install setuptools==75.2.0 pandas==2.1.4 ydata-profiling==4.18.1 pyarrow==15.0.0 sweetviz==2.3.1 scipy==1.13.0

# Build spec binary from source
RUN apt-get update && apt-get install -y golang-go git && \
    git clone https://github.com/hydrocode-de/gotap.git /tmp/gotap && \
    cd /tmp/gotap && go build -o /usr/local/bin/spec ./main.go && \
    rm -rf /tmp/gotap && \
    apt-get remove -y golang-go git && apt-get autoremove -y && apt-get clean

# create the tool input structure
RUN mkdir /in
COPY ./in /in
RUN mkdir /out
RUN mkdir /src
COPY ./src /src

WORKDIR /src
CMD ["spec", "run", "profile", "--input-file", "/in/inputs.json"]