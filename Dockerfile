# Pull any base image that includes python3
FROM python:3.10

# install the toolbox runner tools
RUN pip install json2args==0.4.0

# install pandas and pandas-profiling
RUN pip install pandas==1.5.1 pandas-profiling==3.4.0

# create the tool input structure
RUN mkdir /in
COPY ./in /in
RUN mkdir /out
RUN mkdir /src
COPY ./src /src

WORKDIR /src
CMD ["python", "run.py"]