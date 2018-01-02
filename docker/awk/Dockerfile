FROM ubuntu:14.04

USER root
RUN apt-get update && apt-get install -y --force-yes \
    gawk

USER ubuntu
ENV HOME /home/ubuntu

WORKDIR ${HOME}
