FROM ubuntu

ADD metahash.sh /
ADD metahash.py /
ADD mhutils.py /
ADD hub.py /
ADD temp.py /
ADD co.py /
ADD heater.py /
ADD keys /keys
ADD static /static
ADD run.sh /

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip dnsutils xxd
RUN pip3 install flask fabulous dnspython requests

ENTRYPOINT python3 temp.py & python3 co.py & python3 heater.py & python3 hub.py