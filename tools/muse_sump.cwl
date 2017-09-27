#!/usr/bin/env cwl-runner

cwlVersion: v1.0

class: CommandLineTool

requirements:
  - class: InlineJavascriptRequirement
  - class: ShellCommandRequirement
  - class: DockerRequirement
    dockerPull: quay.io/ncigdc/muse-tool:2.0a

inputs:

  - id: dbsnp
    type: File
    inputBinding:
      position: 2
      prefix: -D
    secondaryFiles:
      - '.tbi'

  - id: call_output
    type: File
    inputBinding:
      position: 3
      prefix: -I

  - id: exp_strat
    type: string
    default: 'E'
    doc: E or G. E should be used for WXS and G for WGS.
    inputBinding:
      position: 4
      prefix: '-'
      separate: False

  - id: output_base
    type: string
    inputBinding:
      position: 5
      prefix: -O

outputs:
  - id: output_file
    type: File
    outputBinding:
      glob: $(inputs.output_base)

baseCommand: ['/home/ubuntu/tools/MuSEv1.0rc_submission_c039ffa', 'sump']
