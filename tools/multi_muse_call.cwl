class: CommandLineTool
cwlVersion: v1.0
id: multi_muse_call
requirements:
  - class: InlineJavascriptRequirement
  - class: DockerRequirement
    dockerPull: docker.osdc.io/ncigdc/muse-tool:1.0.0-444.bd5645e
doc: |
  Multithreading on MuSE call function.

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

  timeout:
    type: int?
    inputBinding:
      position: 7
      prefix: --timeout

outputs:
  output_file:
    type: File
    outputBinding:
      glob: 'multi_muse_call_merged.MuSE.txt'

baseCommand: ['multi']
