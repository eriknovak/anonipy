---
draft: true
date: 2024-07-15
authors: [eriknovak]
description: >
  The overview of the implemented strategies.
categories:
  - Overview
---

# Strategies Overview

In this post, we will show an overview of the implemented  strategies. The strategies delegate how the original text will be anonymized given the extracted `named entities`. They output the anonymized text and the list of replacements that were made to the original text.

All strategies and their API references are available in the  [strategies][anonipy.anonymize.strategies] module. What follows is the presentation of the different strategies `anonipy` provides.

<!-- more -->




## Pre-requisites



## Strategies

All following strategies are available in the [strategies][anonipy.anonymize.strategies] module.


### Redacted Strategy



### Masking Strategy




### Pseudonymization Strategy




## Conclusion

The strategies are used to anonymize the text in combination with the extracted `named entities`. The strategies are used to replace and anonymize the text as well as provide the list of replacements that were made to the original text.


!!! info "Under construction"