class: CommandLineTool
cwlVersion: v1.0
id: muse_sump
requirements:
  - class: InlineJavascriptRequirement
  - class: DockerRequirement
    dockerPull: docker.osdc.io/ncigdc/muse:1.0-96322a3
doc: |
  Run MuSE sump function.

inputs:

  dbsnp:
    type: File
    inputBinding:
      position: 2
      prefix: -D
    secondaryFiles:
      - '.tbi'

  call_output:
    type: File
    inputBinding:
      position: 3
      prefix: -I

  exp_strat:
    type: string
    default: 'E'
    doc: E or G. E should be used for WXS and G for WGS.
    inputBinding:
      position: 4
      prefix: '-'
      separate: False

  output_base:
    type: string
    inputBinding:
      position: 5
      prefix: -O

outputs:
  MUSE_OUTPUT:
    type: File
    outputBinding:
      glob: $(inputs.output_base)

baseCommand: ['/muse/muse_v1.0', 'sump']
