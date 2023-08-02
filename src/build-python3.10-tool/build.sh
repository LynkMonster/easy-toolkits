#!/bin/bash
set -x

DIR=$1

OPENSSL_PKG=./openssl-1.1.1.tar.gz
OPENSSL_DIR="$DIR/openssl-1.1.1"

PY_PKG=./Python-3.10.11.tgz
PY_DIR="$DIR/Python-3.10.11"

LIBSSL=/usr/lib64/libssl.so.1.1
LIBCRYPTO=/usr/lib64/libcrypto.so.1.1

sudo yum update -y
sudo yum -y groupinstall "Development tools"
sudo yum install libdb4-devel \
     ncurses-libs \
     ncurses-devel \
     bzip2-devel  \
     readline-devel \
     zlib-devel \
     gdbm-devel \
     xz-devel \
     sqlite-devel  \
     tk-devel \
     libpcap-devel \
     openssl-devel \
     libffi-devel \
     libuuid-devel

tar zxvf $OPENSSL_PKG -C "$DIR" .
tar zxvf $PY_PKG -C "$DIR" .

cd "$OPENSSL_DIR" && sudo ./config shared --prefix=/usr/local/openssl-1.1.1 --openssldir=/usr/local/openssl-1.1.1
sudo make && make install


if [ ! -f "$LIBSSL" ]; then
    ln -s /usr/local/openssl-1.1.1/lib/libssl.so.1.1 /usr/lib64/libssl.so.1.1
fi

if [ ! -f "$LIBCRYPTO" ]; then
  ln -s /usr/local/openssl-1.1.1/lib/libcrypto.so.1.1 /usr/lib64/libcrypto.so.1.1
fi

cd "$PY_DIR" && sudo ./configure --prefix=/usr/local/python3.10 --with-openssl=/usr/local/openssl-1.1.1
sudo make && make install

ln -s /usr/local/python3.10/bin/python3.10 /usr/bin/python3
ln -s /usr/local/python3.10/bin/pip3 /usr/bin/pip3
