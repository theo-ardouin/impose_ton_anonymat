#!/bin/bash

set -e

CONNECTION_STRING="$1"
REMOTE_PATH="$2"

if [ ! "$2" ]; then
    echo "Usage: $0 <user@domain> <remote-path>" > /dev/stderr
    exit 1
fi

# Copy required files
rsync -v -a -z -P --exclude-from=scripts/rsync_exclude.txt * "${CONNECTION_STRING}:${REMOTE_PATH}"

# Run remotely
ssh "${CONNECTION_STRING}" bash <<EOF
set -e
cd ${REMOTE_PATH}
sed -e 's:REMOTE_PATH:${REMOTE_PATH}:g' infra/systemd/impose.service > /tmp/impose.service
make init
EOF

echo "Installation complete."
echo 'Finalize deployment with "sudo make deploy" remotely.'
