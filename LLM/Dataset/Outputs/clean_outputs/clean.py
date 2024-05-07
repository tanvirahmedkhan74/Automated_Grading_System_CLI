import json
import re
def clean_result():
    for i in range(2, 15):
        with open(f"mark_report{i}.json", "r") as file:
            data = json.load(file)

        for obj in data:
            res = obj["result"]
            print(res)
            # Remove non-numeric characters and extract the first integer
            match = re.search(r"\d+", res)
            if match:
                first_integer = int(match.group())
            else:
                first_integer = None
            obj["result"] = first_integer

        with open(f"mark_report{i}.json", "w") as file:
            json.dump(data, file, indent=4)

def clean_single_result(filename):
    with open(filename, "r") as file:
        data = json.load(file)

    for obj in data:
        res = obj["result"]
        print(res)
        # Remove non-numeric characters and extract the first integer
        match = re.search(r"\d+", res)
        if match:
            first_integer = int(match.group())
        else:
            first_integer = None
        obj["result"] = first_integer

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
clean_single_result('mark_report.json')