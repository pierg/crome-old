FROM pmallozzi/ltltools:latest

ENV GIT_SSL_NO_VERIFY=1
RUN git clone https://github.com/pierg/crome.git --branch master --single-branch


WORKDIR /home/crome


# Preparing the environment
RUN conda env create --file environment.yml
# Include Spot Python library manually
RUN cp -R /home/dependencies/spot/* /miniconda/envs/crome-env/lib/python3.10/site-packages
RUN conda init bash
RUN exec bash



ENV PYTHONPATH "${PYTHONPATH}:/home/crome/src:/home/crome/casestudies:/home/crome/config"

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
