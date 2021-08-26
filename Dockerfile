FROM pmallozzi/ltltools:web

ENV LISTEN_PORT 5000
EXPOSE 5000

ENV GIT_SSL_NO_VERIFY=1

RUN git clone https://github.com/pierg/crome.git --branch master --single-branch
WORKDIR /home/crome

RUN pip3 install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/home/crome/src:/home/crome/examples:/home/crome/casestudies"

ENTRYPOINT ["./entrypoint.sh"]
