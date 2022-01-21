FROM pmallozzi/ltltools:latest

ENV GIT_SSL_NO_VERIFY=1
RUN git clone https://github.com/pierg/crome.git --branch master --single-branch


WORKDIR /home/crome


# Preparing the environment
RUN conda env create --file environment.yml
# Include Spot Python library manually
RUN cp -R /home/dependencies/spot/* /miniconda/envs/conda-env/lib/python*/site-packages
RUN conda init bash
RUN conda activate crome-env



ENV PYTHONPATH "${PYTHONPATH}:/home/crome/src:/home/crome/casestudies:/home/crome/config"

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
