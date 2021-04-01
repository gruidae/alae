#!/bin/bash

cd `dirname $0`
cd ..

if [ ! -d tmp ]; then
    # tmpディレクトリを作成
    mkdir tmp
    echo "Make Directory tmp/ in alae" >&2
fi
