#!/bin/sh

cp -r /udaan-drishti/mender-scripts /mender-scripts
cd /mender-scripts
commit=${COMMIT}
# outbound
ARTIFACT_NAME="drishti-outbound-${commit}"
#TODO: Remove hardcoded device type
DEVICE_TYPE="raspberrypi4"
OUTPUT_PATH="/artifacts/$ARTIFACT_NAME.mender"
DEST_DIR="/opt/udaan/drishti"
FILE_TREE="/udaan-drishti/"

./directory-artifact-gen -n "${ARTIFACT_NAME}" -t ${DEVICE_TYPE} -d ${DEST_DIR} -o "${OUTPUT_PATH}" ${FILE_TREE} -- -s ./ArtifactInstall_Leave_50_deploy-outbound -s ./ArtifactInstall_Leave_60_chown

# inbound
ARTIFACT_NAME="drishti-inbound-${commit}"
OUTPUT_PATH="/artifacts/$ARTIFACT_NAME.mender"

./directory-artifact-gen -n "${ARTIFACT_NAME}" -t ${DEVICE_TYPE} -d ${DEST_DIR} -o "${OUTPUT_PATH}" ${FILE_TREE} -- -s ./ArtifactInstall_Leave_50_deploy-inbound -s ./ArtifactInstall_Leave_60_chown

# inbound-internal
ARTIFACT_NAME="drishti-inbound-internal-${commit}"
OUTPUT_PATH="/artifacts/$ARTIFACT_NAME.mender"

./directory-artifact-gen -n "${ARTIFACT_NAME}" -t ${DEVICE_TYPE} -d ${DEST_DIR} -o "${OUTPUT_PATH}" ${FILE_TREE} -- -s ./ArtifactInstall_Leave_50_deploy-inbound-internal -s ./ArtifactInstall_Leave_60_chown

# outbound-internal
ARTIFACT_NAME="drishti-outbound-internal-${commit}"
OUTPUT_PATH="/artifacts/$ARTIFACT_NAME.mender"

./directory-artifact-gen -n "${ARTIFACT_NAME}" -t ${DEVICE_TYPE} -d ${DEST_DIR} -o "${OUTPUT_PATH}" ${FILE_TREE} -- -s ./ArtifactInstall_Leave_50_deploy-outbound-internal -s ./ArtifactInstall_Leave_60_chown


