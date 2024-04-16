import re

# =====================================
# Helper functions
# =====================================


def replace_with_asterisks(match_obj):
    if match_obj.group() is not None:
        return " ".join(
            ["*" * len(chunk) for chunk in re.split(r"\s+", match_obj.group())]
        )


# =====================================
# Hardcoded annonymization functions
# =====================================


def annonymize_emails(text):
    email_address_re = (
        "[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*"
    )
    return re.sub(email_address_re, replace_with_asterisks, text)


def annonymize_phone_number(text):
    phone_number_re = (
        "[(]?[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?([0-9]{2,}[-\s\.]?){2,}([0-9]{3,})"
    )
    return re.sub(phone_number_re, replace_with_asterisks, text)


def annonymize_website(text):
    website_url_re = "((https?|ftp|smtp):\/\/)?(www.)?([a-zA-Z0-9]+\.)+[a-z]{2,}(\/[a-zA-Z0-9#\?\_\.\=\-\&]+|\/?)*"
    return re.sub(website_url_re, replace_with_asterisks, text)


# =====================================
# Huggingface annonymization functions
# =====================================


def gliner_annonymize(text, entities, tags):
    curr_idx = 0
    anon_text = ""
    for entity in entities:
        if entity["label"] in tags:
            anon_text += text[curr_idx : entity["start"]] + (
                "*" * (entity["end"] - entity["start"])
            )
            curr_idx = entity["end"]
    anon_text += text[curr_idx:]
    return anon_text
