#!/bin/bash -ex
curl -s -o python.tgz "https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz"
tar zxf python.tgz

pushd conductor_client

sed -i "s/#__version__=\"0.0.0\"/__version__=\"${RELEASE_VERSION}\"/" \
    conductor/__init__.py
echo $payload > conductor/release.json

./installers/windows/build.sh
./installers/osx/build.sh
./installers/rpm/build.sh
./installers/debian/build.sh

curl -s -u ${GITHUB_API_TOKEN} --data-binary @installers/rpm/conductor-${RELEASE_VERSION}-0.noarch.rpm -H "Content-Type:application/octet-stream" "${UPLOAD_URL}?name=conductor-${RELEASE_VERSION}-0.noarch.rpm"
curl -s -u ${GITHUB_API_TOKEN} --data-binary @installers/debian/conductor_${RELEASE_VERSION:1}.deb -H "Content-Type:application/octet-stream" "${UPLOAD_URL}?name=conductor_${RELEASE_VERSION:1}.deb"