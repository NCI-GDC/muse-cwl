#!/usr/bin/env cwl-runner

cwlVersion: v1.0

class: CommandLineTool

requirements:
  - class: InlineJavascriptRequirement
  - class: ShellCommandRequirement
  - class: ResourceRequirement
  
inputs:
  call_outputs:
    type:
      type: array
      items: File
    inputBinding:
      position: 1

  output_base:
    type: string

outputs:
  merged_file:
    type: File
    outputBinding:
      glob: $(inputs.output_base + '.MuSE.txt')

baseCommand: ['awk']
arguments:
  - valueFrom: 'FNR==1 && NR !=1 {while (/^#/) getline;} 1 {print}'
    position: 0
    shellQuote: true
stdout: $(inputs.output_base + '.MuSE.txt')
