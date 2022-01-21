FROM pmallozzi/ltltools:latest

ENV GIT_SSL_NO_VERIFY=1
RUN git clone https://github.com/pierg/crome.git --branch master --single-branch


WORKDIR /home/crome

## Install Dependencies
#RUN conda env create --name condaenv
#RUN conda activate condaenv
#RUN conda install --file requirements.txt
#RUN conda install -c conda-forge pygraphviz
#
#
## Include Spot Python library manually
#RUN cp -R /home/ltltools/dependencies/spot/* /home/crome/conda/lib/python*/site-packages/



ENV PYTHONPATH "${PYTHONPATH}:/home/crome/src:/home/crome/casestudies:/home/crome/config"

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
