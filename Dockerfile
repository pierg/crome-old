FROM pmallozzi/ltltools

RUN mkdir /home/crome/
COPY . /home/crome/
WORKDIR /home/crome

RUN pip3 install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/home/crome/src"

ENTRYPOINT ["./entrypoint.sh"]
