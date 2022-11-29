#!/bin/sh
# Test function for the docker image
set -e

# Set the docker image name as the given parameter
DOCKER_IMAGE=$1

# Set the docker image name
IMAGE=$1
if [ -z "${IMAGE}" ]; then
    echo "Error: Provide a docker image name." && exit 1
fi

# Check that the docker image exists
echo "Checking if ${IMAGE} exists..."
docker inspect "${IMAGE}" --format="Image exists"


# Check that the docker image returns the correct output
echo "Testing $DOCKER_IMAGE..."

# Run the docker image and check that all files are created in the folder (in case with graphs)
OUTPUT_FOLDER=outputs
docker run --rm --memory="500m" -v "${PWD}"/platypus-core/tests/data:/data -v "${PWD}/${OUTPUT_FOLDER}":/${OUTPUT_FOLDER} "${DOCKER_IMAGE}" -i /data/1.tar -o /"${OUTPUT_FOLDER}" \

for value in test.tar
do
    if [ ! -f "${OUTPUT_FOLDER}/${value}" ]; then
    echo "Error: File ${OUTPUT_FOLDER}/${value} not created" && exit 1
fi
done

echo "Testing ${DOCKER_IMAGE} successful."
