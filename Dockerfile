FROM pmallozzi/ltltools:web

RUN mkdir /home/crome
COPY . /home/crome/
WORKDIR /home/crome

ENV GIT_SSL_NO_VERIFY=1

RUN pip3 install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/home/crome/src:/home/crome/examples:/home/crome/casestudies"

ENTRYPOINT ["./entrypoint.sh"]
