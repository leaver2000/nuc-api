FROM continuumio/miniconda3 as build

# ARG PYTHON_VERSION=3.7
# ARG CONDA_PYTHON_VERSION=3
# ARG CONDA_DIR=/opt/conda
ARG TEMP_TAR=/tmp/env.tar

COPY environment.yml .

COPY app/ app/

RUN conda update -n base -c defaults conda && \
    conda env create -f environment.yml && \
    conda install -c conda-forge conda-pack

# install conda-pack

# Use conda-pack to create a standalone enviornment in /venv:
RUN conda-pack -n venv -o $TEMP_TAR && \
    mkdir /venv && \
    cd /venv && \
    tar xf $TEMP_TAR && \
    rm $TEMP_TAR 

# put venv in same path it'll be in final image, so now fix up paths
RUN /venv/bin/conda-unpack
# Debian as the base image since the conda env also includes Python
FROM debian:buster as runtime


RUN apt-get update && apt-get -y install cron

# Copy hello-cron file to the cron.d directory
COPY --from=build daily-cron /etc/cron.d/daily-cron


# Copy /venv from the previous stage:
COPY --from=build /venv /venv
COPY --from=build /app /app
# activate the 
ENV PATH=/venv/bin:$PATH


# EXPOSE 80
# Behind a TLS Termination Proxy
# If you are running your container behind a TLS Termination Proxy (load balancer) like Nginx or Traefik, 
# add the option --proxy-headers, this will tell Uvicorn to trust the headers sent by that proxy telling 
# it that the application is running behind HTTPS, etc.
# CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
HEALTHCHECK --interval=21s --timeout=3s --start-period=10s CMD curl --fail http://localhost:8080/ping || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]