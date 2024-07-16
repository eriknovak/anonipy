import random

random.seed(42)

# ===============================================
# GLOBAL COLOR MAPPING
# ===============================================

GLOBAL_COLOR_MAPPING = {}

# ===============================================
# Color generators and functions
# ===============================================


def generate_random_color():
    return "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])


def get_label_color(label):
    if label in GLOBAL_COLOR_MAPPING:
        return GLOBAL_COLOR_MAPPING[label]
    else:
        color = generate_random_color()
        GLOBAL_COLOR_MAPPING[label] = color
        return color
