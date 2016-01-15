To submit a new workflow or tool description please make a pull request against this repository.

###single cwl-tool usage:
MuSE call usage:  cwl-runner /path/to/tools/muse_call.cwl.yaml --tumor_bam_path /path/to/tumor.bam --normal_bam_path /path/to/normal.bam --reference_fasta_name /path/to/ref --reference_fasta_fai /path/to/ref.fai --Parallel_Block_Size number(default = 50000000) --thread_count number(default = 8) --uuid uuid

MuSE sump wxs usage:  cwl-runner /path/to/tools/muse_sump_wxs.cwl.yaml --muse_call_output_path /path/to/muse_call/merged_output --dbsnp_known_snp_sites /path/to/dbsnp.bgz --uuid uuid  

MuSE sump wgs usage:  cwl-runner /path/to/tools/muse_sump_wgs.cwl.yaml --muse_call_output_path /path/to/muse_call/merged_output --dbsnp_known_snp_sites /path/to/dbsnp.bgz --uuid uuid

###cwl-workflow usage:
MuSE for WXS: cwl-runner --debug /path/to/muse-wxs-workflow.cwl.yaml --tumor_bam_path /path/to/tumor.bam --normal_bam_path /path/to/normal.bam --reference_fasta_name /path/to/ref --reference_fasta_fai /path/to/ref.fai --dbsnp_known_snp_sites /path/to/dbsnp.bgz --Parallel_Block_Size number(default = 50000000) --thread_count number(default = 8) --uuid uuid

MuSE for WGS: cwl-runner --debug /path/to/muse-wgs-workflow.cwl.yaml --tumor_bam_path /path/to/tumor.bam --normal_bam_path /path/to/normal.bam --reference_fasta_name /path/to/ref --reference_fasta_fai /path/to/ref.fai --dbsnp_known_snp_sites /path/to/dbsnp.bgz --Parallel_Block_Size number(default = 50000000) --thread_count number(default = 8) --uuid uuid
