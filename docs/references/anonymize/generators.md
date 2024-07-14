---
title: Generators Module
---

# Generators Module

::: anonipy.anonymize.generators

## LLM Label Generator

!!! info "GPU Requirements"
    The `LLMLabelGenerator` utilizes the open source LLMs,    specifically the [Meta-Llama-3-8B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct) model. Because the model is quite large, we utilize quantization using the `bitsandbytes` package to reduce its size. Therefore, the `LLMLabelGenerator` requires at least 8GB GPU and CUDA drivers to be available. If these resources are not available on your machine, you can use the `MaskLabelGenerator` instead.

::: anonipy.anonymize.generators.LLMLabelGenerator

## Mask Label Generator

::: anonipy.anonymize.generators.MaskLabelGenerator

## Number Generator

::: anonipy.anonymize.generators.NumberGenerator

## Date Generator

::: anonipy.anonymize.generators.DateGenerator
