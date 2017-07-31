#!/usr/bin/env cwl-runner

cwlVersion: v1.0

class: CommandLineTool

requirements:
  - $import: envvar-global.cwl
  - class: InlineJavascriptRequirement
  - class: DockerRequirement
    dockerPull: quay.io/ncigdc/muse-tool:2.0a

inputs:
  - id: ref
    type: File
    inputBinding:
      position: 2
      prefix: -f
    secondaryFiles:
      - '.fai'
      - '^.dict'

  - id: region
    type: string
    inputBinding:
      position: 3
      prefix: -r

  - id: tumor_bam
    type: File
    inputBinding:
      position: 4
    secondaryFiles:
      - '^.bai'

  - id: normal_bam
    type: File
    inputBinding:
      position: 5
    secondaryFiles:
      - '^.bai'

  - id: output_base
    type: string
    inputBinding:
      position: 6
      prefix: -O

outputs:
  - id: output_file
    type: File
    outputBinding:
      glob: $(inputs.output_base + '.MuSE.txt')

baseCommand: ['/home/ubuntu/tools/MuSEv1.0rc_submission_c039ffa', 'call']
