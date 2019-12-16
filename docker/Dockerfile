FROM quay.io/jeremiahsavage/cdis_base

USER root
RUN apt-get update && apt-get install -y --force-yes \
    wget

USER ubuntu
ENV HOME /home/ubuntu

ENV muse-tool 2.0a

RUN mkdir -p ${HOME}/tools/
RUN wget http://bioinformatics.mdanderson.org/Software/MuSE/MuSEv1.0rc_submission_c039ffa \
    && chmod +x MuSEv1.0rc_submission_c039ffa \
    && mv MuSEv1.0rc_submission_c039ffa ${HOME}/tools/

WORKDIR ${HOME}
