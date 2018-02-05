#!/usr/bin/env cwl-runner

cwlVersion: v1.0

class: CommandLineTool

requirements:
  - class: InlineJavascriptRequirement
  - class: DockerRequirement
    dockerPull: quay.io/ncigdc/mergemuse:1.0

inputs:
  call_outputs:
    type:
      type: array
      items: File
      inputBinding:
        prefix: --muse_call_out
    inputBinding:
      position: 1

  merged_name:
    type: string
    inputBinding:
      prefix: --merge_outname
      position: 2

outputs:
  merged_file:
    type: File
    outputBinding:
      glob: $(inputs.merged_name)

baseCommand: ['python', '/bin/MergeMuSE.py']
