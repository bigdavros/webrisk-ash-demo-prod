FROM google/cloud-sdk:slim

RUN apt update && apt install wget python3 -y
ADD webrisk-python-01 /webrisk
WORKDIR /webrisk
RUN pip3 install -r requirements.txt

EXPOSE 5000
ENTRYPOINT [ "python3" ]
CMD ["/webrisk/app.py" ]
