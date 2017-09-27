#!/usr/bin/env cwl-runner

cwlVersion: v1.0

class: CommandLineTool

requirements:
  - class: InlineJavascriptRequirement
  - class: ShellCommandRequirement
  - class: DockerRequirement
    dockerPull: quay.io/shenglai/picard-sortvcf-tool:1.0a

inputs:
  - id: java_opts
    type: string
    default: "16G"
    doc: |
      "JVM arguments should be a quoted, space separated list (e.g. -Xmx8g -Xmx16g -Xms128m -Xmx512m)"
    inputBinding:
      position: 1
      prefix: "-Xmx"
      separate: false

  - id: nthreads
    type: int
    default: 8
    inputBinding:
      position: 2
      prefix: "-XX:ParallelGCThreads="
      separate: false

  - id: reference_dict
    type: File
    inputBinding:
      position: 5
      prefix: "SEQUENCE_DICTIONARY="
      separate: false

  - id: output_vcf
    type: string
    inputBinding:
      position: 6
      prefix: "OUTPUT="
      separate: false

  - id: input_vcf
    type: File
    inputBinding:
      prefix: "I="
      separate: false
      position: 7

outputs:
  - id: sorted_output_vcf
    type: File
    outputBinding:
      glob: $(inputs.output_vcf)
    secondaryFiles:
      - ".tbi"

baseCommand: java
arguments:
  - valueFrom: "/home/ubuntu/tools/picard-tools/picard.jar"
    prefix: "-jar"
    position: 3
  - valueFrom: "SortVcf"
    position: 4
  - valueFrom: "true"
    position: 8
    prefix: "CREATE_INDEX="
    separate: false
