FROM pmallozzi/ltltools

ENV GIT_SSL_NO_VERIFY=1

RUN git clone https://github.com/pierg/crome.git --branch master --single-branch
WORKDIR /home/crome

RUN pip3 install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/home/crome/src:/home/crome/web:/home/crome/examples:/home/crome/casestudies"

WORKDIR /home/crome/web/backend

ENTRYPOINT [ "flask" ]
CMD ["run", "--host=0.0.0.0", "--port=5000"]
