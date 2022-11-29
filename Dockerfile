# syntax=docker/dockerfile:1.2
FROM docker.io/condaforge/mambaforge:4.12.0-2 as build

# Update mamba
RUN mamba update mamba -y

# Install conda lock and conda pack
COPY environment.docker.yml ./
RUN mamba env update --file environment.docker.yml --name base

# Install conda environment on the image with conda lock
COPY conda-linux-64.lock ./

# Copy auth file to docker image and use to build conda env. Note replace with line under when buildkit is supported on bitbucket.
COPY auth.json ./
RUN conda-lock install --name fromlock --auth-file auth.json conda-linux-64.lock
#RUN --mount=type=secret,id=auth conda-lock install --name fromlock --auth-file auth.json conda-linux-64.lock

# Use conda-pack to create a standalone enviornment tarball and extract in /venv:
RUN conda-pack --name fromlock -o /tmp/env.tar && mkdir -p /venv && tar xf /tmp/env.tar -C /venv

# Cleanup prefixes from in the active environment.
RUN /venv/bin/conda-unpack

# Use a distroless runtime image.
#Note: python interpreter will be copied with conda pack from the build env, no need to have it in the runtime image
FROM gcr.io/distroless/base:debug@sha256:c2224daeb29a70a15182a13bdf7dfa3c7a0976d95967fe8d9b41ef8bdf465644 as runtime

# Force the stdout and stderr streams to be unbuffered (ie. flush immediately)
ENV PYTHONUNBUFFERED=1

# Set the workdir
WORKDIR /app

# Copy /venv from the build stage and add to path
COPY --from=build /venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy code files
COPY platypus-core/ ./

# Set the entrypoint to call the main method
ENTRYPOINT ["python", "/app/main.py"]
