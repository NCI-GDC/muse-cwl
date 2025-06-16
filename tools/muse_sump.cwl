class: CommandLineTool
cwlVersion: v1.0
id: muse_sump
requirements:
  - class: InlineJavascriptRequirement
  - class: ShellCommandRequirement
  - class: DockerRequirement
    dockerPull: docker.osdc.io/ncigdc/muse-tool:1.0.0-444.bd5645e
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

baseCommand: ['/usr/local/bin/muse', 'sump']
