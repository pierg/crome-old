FROM pmallozzi/ltltools

RUN git clone https://github.com/pierg/crome.git --branch master --single-branch
WORKDIR /home/crome

RUN pip3 install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/home/crome/src"

ENTRYPOINT ["./entrypoint.sh"]
