FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev wget

RUN cd /bin/ && wget http://bioinformatics.mdanderson.org/Software/MuSE/MuSEv1.0rc_submission_c039ffa && chmod +x MuSEv1.0rc_submission_c039ffa
ADD multi_muse_call.py /bin/

ENV multi_muse_call v1.0
