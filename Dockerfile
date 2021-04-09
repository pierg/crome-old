FROM ubuntu:19.10

ENV DEBIAN_FRONTEND=noninteractive

# Istall binary files of strix and nuXmv
COPY bin/ubuntu_19_10/updated/strix /usr/local/bin
COPY bin/ubuntu_19_10/owl.jar /usr/local/bin
RUN chmod +x /usr/local/bin/strix

COPY bin/linux/nuXmv /usr/local/bin
RUN chmod +x /usr/local/bin/nuXmv


# Install keyboard-configuration separately to avoid travis hanging waiting for keyboard selection
RUN \
    apt -y update && \
    apt install -y keyboard-configuration

# Install general things
RUN \
    apt install -y \
        git \
        unzip \
        nano \
        wget \
        gnupg2 \
        tzdata



RUN apt update
RUN \
    apt install -y \
        cmake \
        make\
        libboost-dev \
        libboost-program-options-dev \
        libboost-filesystem-dev \
        libboost-iostreams-dev \
        zlib1g-dev \
        default-jre \
        openjdk-13-jdk


# Install CoGoMo dependencies
RUN \
    apt install -y \
        python3-pip \
        python3-dev


# Needed for spot
RUN wget -q -O - https://www.lrde.epita.fr/repo/debian.gpg | apt-key add -
RUN echo 'deb http://www.lrde.epita.fr/repo/debian/ stable/' >> /etc/apt/sources.list

RUN apt -y update && DEBIAN_FRONTEND=noninteractive && \
    apt install -y \
    spot \
    libspot-dev \
    spot-doc

# Installing Docker (to run strix)
RUN \
    apt install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        software-properties-common
RUN -fsSL https://download.docker.com/linux/ubuntu/gpg
RUN apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic test"
RUN apt update
RUN apt install docker-ce
RUN docker pull lazkany/strix


RUN \
    apt clean && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /home

RUN git clone -b master --single-branch https://github.com/pierg/cogomo.git

RUN python3 -m pip install --user --upgrade pip

WORKDIR /home/cogomo


RUN pip3 install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/home/cogomo:/home/cogomo/src:/home/cogomo:/home/cogomo/output:/home/cogomo/missions:/home/cogomo/src/z3"

ENTRYPOINT ["./entrypoint.sh"]
