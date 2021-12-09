FROM pmallozzi/ltltools:web

ENV GIT_SSL_NO_VERIFY=1
RUN git clone https://github.com/pierg/crome.git --branch master --single-branch

WORKDIR /home/crome/web/frontend
RUN npm run install:clean
RUN npm run build

WORKDIR /home/crome


RUN pip3 install -r requirements.txt

# Include Spot Python library manually
RUN cp -R /home/ltltools/dependencies/ubuntu/spot/PACKAGE /home/crome/venv/lib/*/site-packages



ENV PYTHONPATH "${PYTHONPATH}:/home/crome/src:/home/crome/casestudies:/home/crome/config"

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
