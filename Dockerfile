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

# Use conda-pack to create a standalone enviornment in /nuc:
RUN conda-pack -n nuc -o $TEMP_TAR && \
    mkdir /nuc && \
    cd /nuc && \
    tar xf $TEMP_TAR && \
    rm $TEMP_TAR 

# put nuc in same path it'll be in final image, so now fix up paths
RUN /nuc/bin/conda-unpack
# Debian as the base image since the conda env also includes Python
FROM debian:buster as runtime


RUN apt-get update && apt-get -y install cron

# Copy hello-cron file to the cron.d directory

# Copy /nuc from the previous stage:
COPY --from=build /nuc /nuc
COPY --from=build /app /app
COPY --from=build daily-cron /etc/cron.d/daily-cron
# activate the 
ENV PATH=/nuc/bin:$PATH


# EXPOSE 80
# Behind a TLS Termination Proxy
# If you are running your container behind a TLS Termination Proxy (load balancer) like Nginx or Traefik, 
# add the option --proxy-headers, this will tell Uvicorn to trust the headers sent by that proxy telling 
# it that the application is running behind HTTPS, etc.
# CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
HEALTHCHECK --interval=21s --timeout=3s --start-period=10s CMD curl --fail http://localhost:8080/ping || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]