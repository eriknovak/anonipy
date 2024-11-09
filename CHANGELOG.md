### anonipy-0.2.0 (2024-11-09)

**Breaking Changes:**

- Change Python support between v3.9 and v3.12.
- Change default `model_name` for `LLMLabelGenerator` to be `HuggingFaceTB/SmolLM2-1.7B-Instruct` (for ease of use)

**New Features:**

- Enable CPU utilization for `LLMLabelGenerator`
- Enable changing the input parameters for `LLMLabelGenerator` (`model_name` and `use_gpu`)
- Add additional unit tests for `NERExtractor`

**Bug Fixes:**

- Fix package documentation

### anonipy-0.1.2 (2024-07-23)

**Bug Fixes:**

- Fix entity creation in `PatternExtractor`
- Fix documentation duplication

### anonipy-0.1.1 (2024-07-16)

**New Features:**

- Add `Entity` regex group selection
- Add option to ignore `Entity` regex pattern in `LLMLabelGenerator.generate`

### anonipy-0.1.0 (2024-07-16)

**Breaking Changes:**

- Rename the `EntityExtractor` to `NERExtractor`
- Rename the input variable `output_gen` to `sub_variant` in `DateGenerator`
- Rename the input variable `entity_prefix` to `add_entity_attrs` in `LLMLabelGenerator.generate`
- Move the `regex` submodule from `anonipy.anonymize` to `anonipy.utils`

**New Features:**

- Add a pattern extractor named `PatternExtractor`, used to extract entities using spacy pattern matching and regex
- Add a multi extractor named `MultiExtractor`, used to extract entities using multiple extractors
- Add the `DATE_TRANSFORM_VARIANTS` constant to help with date generator
- Refine the `Entity` implementation
- Improve package documentation

### anonipy-0.0.8 (2024-06-17)

**New Features:**

- Add automatic date format detection support to `DateGenerator`

### anonipy-0.0.7 (2024-06-06)

**New Features:**

- Upgrade `gliner-spacy` to have cleaner code
- Add function to help manual post-anonymization replacement fixing

### anonipy-0.0.6 (2024-05-31)

**New Features:**

- Add GPU support and entity scores to `EntityExtractor`
- Standardize the function naming in strategies

### anonipy-0.0.5 (2024-05-29)

**New Features:**

- Re-implement file reading methods + add unit tests
- Expland the test environment on all OS

### anonipy-0.0.4 (2024-05-27)

**New Features:**

- Add unit tests
- Refine the Entity implementation
- Update documentation

**Bug Fixes:**

- Fix the `LANGUAGES` constant

### anonipy-0.0.3 (2024-05-22)

**New features:**

- Add `read_json` function
- Add `write_json` function
- Add blog post on anonymizing collections of documents
- Reduce the number of viable suggestions used to create a substitute in `MaskLabelGenerator`
- Add the entity label to the replacements in strategies

**Bug Fixes:**

- Fix the entity regex checking in `EntityExtractor`

### anonipy-0.0.2 (2024-05-22)

**New Features:**

- Add `write_file` function
- Add blog to the documentation

### anonipy-0.0.1 (2024-05-21)

- Initial release
