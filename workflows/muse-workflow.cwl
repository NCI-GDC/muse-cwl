#!/usr/bin/env cwl-runner

cwlVersion: v1.0

class: Workflow

requirements:
  - class: InlineJavascriptRequirement
  - class: StepInputExpressionRequirement

inputs:
  - id: ref
    type: File
  - id: region
    type: string
  - id: tumor_bam
    type: File
  - id: normal_bam
    type: File
  - id: prefix
    type: string
  - id: dbsnp
    type: File
  - id: exp_strat
    type: string

outputs:
  - id: output_vcf
    type: File
    outputSource: muse_sump/output_file

steps:
  - id: muse_call
    run: ../tools/muse_call.cwl
    in:
      - id: ref
        source: ref
      - id: region
        source: region
      - id: tumor_bam
        source: tumor_bam
      - id: normal_bam
        source: normal_bam
      - id: output_base
        source: prefix
    out:
      - id: output_file

  - id: muse_sump
    run: ../tools/muse_sump.cwl
    in:
      - id: dbsnp
        source: dbsnp
      - id: call_output
        source: muse_call/output_file
      - id: exp_strat
        source: exp_strat
      - id: output_base
        source: prefix
        valueFrom: $(self + '.MuSE.vcf')
    out:
      - id: output_file
