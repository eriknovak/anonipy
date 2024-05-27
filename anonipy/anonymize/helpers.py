from ..definitions import Entity

# =====================================
# Entity converters
# =====================================


def convert_spacy_to_entity(entity, type, regex=".*", *args, **kwargs):
    return Entity(
        entity.text, entity.label_, entity.start_char, entity.end_char, type, regex
    )
