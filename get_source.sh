#!/bin/bash
set -e

VER=$(basename "$(pwd)" | sed 's/.*-//')
SRC_DIR=$(dirname "$0")/source
ARCHIVE="lame-${VER}.tar.gz"
DIR="lame-${VER}"
URL="https://downloads.sourceforge.net/project/lame/lame/${VER}/${ARCHIVE}"

mkdir -p "$SRC_DIR"
cd "$SRC_DIR"

if [ ! -f "$ARCHIVE" ]; then
    echo "📦 Downloading $ARCHIVE"
    wget "$URL"
else
    echo "✅ Archive already exists: $ARCHIVE"
fi

if [ ! -d "$DIR" ]; then
    echo "📂 Extracting $ARCHIVE"
    tar -xzf "$ARCHIVE"
else
    echo "✅ Source directory already exists: $DIR"
fi

