class: CommandLineTool
cwlVersion: v1.0
id: MergeMuSE
requirements:
  - class: InlineJavascriptRequirement
  - class: DockerRequirement
    dockerPull: quay.io/ncigdc/mergemuse:1.1
doc:
  Merge MuSE call outputs, when not using `multi_muse_call.cwl`.

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

baseCommand: ['python', '/opt/MergeMuSE.py']
