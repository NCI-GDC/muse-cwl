class: CommandLineTool
cwlVersion: v1.0
id: muse_call
requirements:
  - class: InlineJavascriptRequirement
  - class: DockerRequirement
    dockerPull: docker.osdc.io/ncigdc/muse-tool:1.0.0-444.bd5645e
doc: |
  Run MuSE call function.

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
      prefix: -l

  tumor_bam:
    type: File
    inputBinding:
      position: 4
    secondaryFiles:
      - '.bai'

  normal_bam:
    type: File
    inputBinding:
      position: 5
    secondaryFiles:
      - '.bai'

outputs:
  output_file:
    type: File
    outputBinding:
      glob: $(inputs.region.nameroot + '.MuSE.txt')

baseCommand: ['/usr/local/bin/muse', 'call']
arguments:
  - valueFrom: $(inputs.region.nameroot)
    prefix: -O
    position: 6
