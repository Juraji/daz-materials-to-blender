import json
from collections import defaultdict, OrderedDict

# PBRSkin from lib: \\data\\DAZ 3D\\Built-in Content\\Daz Iray PBRSkin\\PBRSkin.dsf
# Iray Uber and Translucent shader from scene save file (using said shaders)

SOURCE_FILE = ""
TARGET_FILE = ""
MAT_INDEX = 0

if __name__ == '__main__':
    with open(SOURCE_FILE) as f:
        dson = json.load(f)

    channels = dson["material_library"][MAT_INDEX]["extra"][1]["channels"]
    mapped_channels = defaultdict(list)

    for channel in channels:
        c_group = channel["group"]

        mapped_channel = {
            "id": channel["channel"]["id"],
            "type": channel["channel"]["type"],
            "uses_map": "mappable" in channel["channel"] and channel["channel"]["mappable"],
            "default_value": None if not "value" in channel["channel"] else channel["channel"]["value"],
        }

        # We are all just floats
        if mapped_channel["type"] == "float_color":
            mapped_channel["type"] = "color"
        elif mapped_channel["type"] == "int":
            mapped_channel["type"] = "float"
        elif mapped_channel["type"] == "image":
            mapped_channel["uses_map"] = True

        if mapped_channel["type"] == "enum":
            mapped_channel["enum_opts"] = channel["channel"]["enum_values"]

        mapped_channels[c_group].append(mapped_channel)

    if "diffuse" in dson["material_library"][0]:
        diffuse = dson["material_library"][0]["diffuse"]
        mapped_channels["/Base/Diffuse"].insert(0, {
            "id": "diffuse",
            "type": "color",
            "uses_map": True,
            "default_value": [1, 1, 1],
        })

    sorted_channels = OrderedDict(sorted(mapped_channels.items()))

    with open(TARGET_FILE, "w") as f:
        f.write(json.dumps(sorted_channels, indent=4))
