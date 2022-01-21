FROM pmallozzi/ltltools:base

ENV GIT_SSL_NO_VERIFY=1
RUN git clone https://github.com/pierg/crome.git --branch master --single-branch


WORKDIR /home/crome

# Create the environment:
RUN conda env create -f environment.yml

# Activate the environment, and make sure it's activated:
RUN conda activate myenv

RUN conda install -c conda-forge pygraphviz

# Include Spot Python library manually
#RUN cp -R /home/ltltools/dependencies/ubuntu/spot/PACKAGE /home/crome/venv/lib/*/site-packages



ENV PYTHONPATH "${PYTHONPATH}:/home/crome/src:/home/crome/casestudies:/home/crome/config"

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
