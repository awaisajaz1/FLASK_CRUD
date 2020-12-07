# pull image file from docker hub
FROM centos:7

# install package in base vm
RUN yum -y update \ 
    && yum install -y gcc libc-dev make libffi-dev openssl-dev python3-dev python3 libxml2-dev libxslt-dev wget mysql-devel python3-devel.x86_64

# Set the working directory to /app
WORKDIR /app

# Copy the current content to /app
COPY . /app

# install the dependencies
RUN pip3 --no-cache-dir install -r requirements.txt

# expose ip to external host
EXPOSE 5000

# make default execution
#ENTRYPOINT ["python3"]
CMD ["python3", "WebApplication.py"]
