 
import struct, random
from utils import color_util

def clamp(minvalue, value, maxvalue):
    return max(minvalue, min(value, maxvalue))

def opt(name, var_type, value=None, description="", sane_low=None, sane_high=None):
    opts = { name: {"type":var_type}}
    if not value is None :
        opts[name]["default"] = value
    if description:
        opts[name]["description"] = description
    if not sane_low is None:
        opts[name]["sane_low"] = sane_low
    if not sane_high is None:
        opts[name]["sane_high"] = sane_high
    return opts

def merge_dicts(list_dicts):
    merged = {}
    for dic in list_dicts:
        for k, v in dic.items():
            merged[k] = v
    return merged

def set_options_on_obj(gen_obj, options):
    ignored = {}
    if "print_options" in dir(gen_obj):
        print("Setting the following options: ")
        merged = merge_dicts(gen_obj.print_options())
        for key, values in merged.items():
            safe_name = key.replace("-", "_")
            class_type = values["type"]
            simple_type = not class_type in [str] and not class_type.__class__.__name__ == "str"
            
            target_value = ""
            if "default" in values:
                target_value = values["default"]
            if key in options:
                print(f"  {safe_name}:{options[key]}")
                target_value = options[key]

            if simple_type:
                setattr(gen_obj, safe_name, class_type(target_value))
            else:
                if class_type == "color":
                    if target_value == "random":
                        target_value = color_util.random_hex()
                setattr(gen_obj, safe_name, target_value)

        for k, v in options.items():
            if k not in merged:
                ignored[k] = options[k]
    if ignored:
        print("The following options were passed but unused:")
        for key, value in ignored.items():
            print(f"   {key}:{value}")

def random_position(w, h):
    return (random.randrange(0, w), random.randrange(0, h))

def sum_tuples(*argv):
    total = []
    for tup in argv:
        if not total:
            total = list(tup)
            continue
        for i in range(len(tup)):
            total[i] += tup[i]

    return tuple(total)