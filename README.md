GDC MuSE (v1.0rc_submission_c039ffa) pipeline
---
Python Wrapper

```
/home/ubuntu/.virtualenvs/p2/bin/python slurm/gdc_muse_pipeline.py -h
```

CWL

```
/home/ubuntu/.virtualenvs/p2/bin/cwltool tools/muse_call.cwl -h
/home/ubuntu/.virtualenvs/p2/bin/cwltool workflows/muse_sump_srt.cwl -h
```
Note: The scattered outputs from muse_call would be merged in the wrapper and then pass to `workflows/muse_sump_srt.cwl`.

Docker

Dockerfiles for CWL tools could be found at `docker/`
