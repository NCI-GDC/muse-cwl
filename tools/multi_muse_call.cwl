#!/usr/bin/env cwl-runner

cwlVersion: v1.0

class: CommandLineTool

requirements:
  - class: InlineJavascriptRequirement
  - class: DockerRequirement
    dockerPull: quay.io/ncigdc/multi_muse_call:1.3

inputs:
  ref:
    type: File
    inputBinding:
      position: 2
      prefix: -f
    secondaryFiles:
      - '.fai'
      - '^.dict'

  region:
    type: File
    inputBinding:
      position: 3
      prefix: -r

  tumor_bam:
    type: File
    inputBinding:
      position: 4
      prefix: -t
    secondaryFiles:
      - '.bai'

  normal_bam:
    type: File
    inputBinding:
      position: 5
      prefix: -n
    secondaryFiles:
      - '.bai'

  thread_count:
    type: int
    inputBinding:
      position: 6
      prefix: -c

outputs:
  output_file:
    type: File
    outputBinding:
      glob: 'multi_muse_call_merged.MuSE.txt'

baseCommand: ['python', '/bin/multi_muse_call.py']
