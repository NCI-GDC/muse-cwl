###This branch is supposed to be installed on slurm cluster controller node by salt.
####1. Create slurm bash scripts.

```
python /path/to/this/repo/branch/slurm/get_tn_pairs.py \
--config /path/to/your/GDC/postgres/config/file/ \
--outdir /path/to/desired/output/dir/
```

This code takes your GDC postgres credentials to get completed cocleaned tumor and normal pair information, and generate slurm bash script based on template.sh
Please manually add your GDC postgres credentials in template.sh (e.g. "username" and "password") before running the python code.
All reference files are pre-stated on all slurm workers.

####2. Put your slurm bash scripts into slurm cluster controller node.

Please ask administrant to get ip address of controller node.

####3. Make a for loop to run sbatch.
```
>for i in *.sh;
>do
>sbatch $i
>done
```
