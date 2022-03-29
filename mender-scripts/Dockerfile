FROM ubuntu:20.04
#RUN apt update
#RUN apt install -y wget
ADD https://downloads.mender.io/mender-artifact/3.5.0/linux/mender-artifact /usr/bin/mender-artifact
#COPY ./mender-artifact /usr/bin/mender-artifact
#COPY ../ /udaan-drishti
WORKDIR /udaan-drishti/mender-scripts
RUN chmod +x /usr/bin/mender-artifact
ENTRYPOINT ["./make-drishti-artifacts.sh"]
