class: CommandLineTool
cwlVersion: v1.0
id: multi_muse_call
requirements:
  - class: InlineJavascriptRequirement
  - class: DockerRequirement
    dockerPull: quay.io/ncigdc/multi_muse_call:b4ccd414cfcd4669cb8d431a15de378fdec22724
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

outputs:
  output_file:
    type: File
    outputBinding:
      glob: 'multi_muse_call_merged.MuSE.txt'

baseCommand: ['python', '/opt/multi_muse_call.py']
