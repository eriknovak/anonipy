### anonipy-0.1.0 (2024-07-16)

- Add a pattern extractor named `PatternExtractor`, used to extract entities using spacy pattern matching and regex
- Add a multi extractor named `MultiExtractor`, used to extract entities using multiple extractors
- Add the `DATE_TRANSFORM_VARIANTS` constant to help with date generator
- Refine the `Entity` implementation
- Improve package documentation

**BREAKING changes:**
- Rename the `EntityExtractor` to `NERExtractor`
- Rename the input variable `output_gen` to `sub_variant` in `DateGenerator`
- Move the `regex` submodule from `anonipy.anonymize` to `anonipy.utils`

### anonipy-0.0.8 (2024-06-17)

- Add automatic date format detection support to `DateGenerator`

### anonipy-0.0.7 (2024-06-06)

- Upgrade gliner-spacy to have cleaner code
- Add function to help manual post-anonymization replacement fixing

### anonipy-0.0.6 (2024-05-31)

- Add GPU support and entity scores to `EntityExtractor`
- Standardize the function naming in strategies

### anonipy-0.0.5 (2024-05-29)

- Re-implement file reading methods + add unit tests
- Expland the test environment on all OS

### anonipy-0.0.4 (2024-05-27)

- Add unit tests
- Fix the `LANGUAGES` constant
- Refine the Entity implementation
- Update documentation

### anonipy-0.0.3 (2024-05-22)

- Add `read_json` function
- Add `write_json` function
- Add blog post on anonymizing collections of documents
- Fix the entity regex checking in `EntityExtractor`
- Reduce the number of viable suggestions used to create a substitute in `MaskLabelGenerator`
- Add the entity label to the replacements in strategies

### anonipy-0.0.2 (2024-05-22)

- Add `write_file` function
- Add blog to the documentation

### anonipy-0.0.1 (2024-05-21)

- Initial release