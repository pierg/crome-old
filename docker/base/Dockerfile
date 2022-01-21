FROM pmallozzi/ltltools:base

ARG UBUNTU_VER=21.04
ARG CONDA_VER=latest
ARG OS_TYPE=x86_64
ARG PY_VER=3.9.7

FROM ubuntu:${UBUNTU_VER}

# System packages
RUN apt-get update && apt-get install -yq curl wget jq vim

# Use the above args during building https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG CONDA_VER
ARG OS_TYPE
# Install miniconda to /miniconda
RUN curl -LO "http://repo.continuum.io/miniconda/Miniconda3-${CONDA_VER}-Linux-${OS_TYPE}.sh"
RUN bash Miniconda3-${CONDA_VER}-Linux-${OS_TYPE}.sh -p /miniconda -b
RUN rm Miniconda3-${CONDA_VER}-Linux-${OS_TYPE}.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda

ARG PY_VER
#ARG TF_VER
# Install packages from conda and downgrade py (optional).
RUN conda install -c anaconda -y python=${PY_VER}

#RUN conda install -c anaconda -y \
#    tensorflow-mkl=${TF_VER} \
#    && pip install pyyaml pandas


# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH


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
