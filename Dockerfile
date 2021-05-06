FROM pmallozzi/ltltools:web

RUN git clone https://github.com/pierg/crome.git --branch dev --single-branch
WORKDIR /home/crome


RUN pip3 install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/home/crome/src:/home/crome/examples:/home/crome/casestudies"

ENTRYPOINT ["./entrypoint.sh"]
