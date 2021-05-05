FROM pmallozzi/ltltools

RUN git clone https://github.com/pierg/crome.git --branch dev --single-branch
WORKDIR /home/crome

# Installing NodeJS
ENV NPM_CONFIG_LOGLEVEL info
ENV NODE_VERSION 14.16.0

RUN export PLATFORM=$(if [ "$TARGETPLATFORM" = "linux/amd64" ] ; then echo "x64"; else echo "arm64"; fi) \
  buildDeps='xz-utils curl ca-certificates gnupg2 dirmngr' \
  && set -x \
  && apt-get update && apt-get upgrade -y && apt-get install -y $buildDeps --no-install-recommends \
  && rm -rf /var/lib/apt/lists/* \
  && set -ex \
  && for key in \
    4ED778F539E3634C779C87C6D7062848A1AB005C \
    94AE36675C464D64BAFA68DD7434390BDBE9B9C5 \
    1C050899334244A8AF75E53792EF661D867B9DFA \
    71DCFD284A79C3B38668286BC97EC7A07EDE3FC1 \
    8FCCA13FEF1D0C2E91008E09770F7A9A5AE15600 \
    C4F0DFFF4E8C1A8236409D08E73BC641CC11F4C8 \
    C82FA3AE1CBEDC6BE46B9360C43CEC45C17AB93C \
    DD8F2338BAE7501E3DD5AC78C273792F7D83545D \
    A48C2BEE680E841632CD4E44F07496B3EB3C1762 \
    108F52B48DB57BB0CC439B2997B01419BD92F80A \
    B9E2F5981AA6E0CD28160D9FF13993A75599653C \
  ; do \
  gpg --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys "$key" || \
  gpg --keyserver hkp://ipv4.pool.sks-keyservers.net --recv-keys "$key" || \
  gpg --keyserver hkp://pgp.mit.edu:80 --recv-keys "$key" ; \
  done \
  && curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-$PLATFORM.tar.xz" \
  && curl -SLO --compressed "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc" \
  && gpg --batch --decrypt --output SHASUMS256.txt SHASUMS256.txt.asc \
  && grep " node-v$NODE_VERSION-linux-$PLATFORM.tar.xz\$" SHASUMS256.txt | sha256sum -c - \
  && tar -xJf "node-v$NODE_VERSION-linux-$PLATFORM.tar.xz" -C /usr/local --strip-components=1 \
  && rm "node-v$NODE_VERSION-linux-$PLATFORM.tar.xz" SHASUMS256.txt.asc SHASUMS256.txt \
  && apt-get purge -y --auto-remove $buildDeps \
  && ln -s /usr/local/bin/node /usr/local/bin/nodejs



RUN pip3 install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/home/crome/src:/home/crome/examples:/home/crome/casestudies"

ENTRYPOINT ["./entrypoint.sh"]
