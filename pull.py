import subprocess
import os.path
import json

def replace_illegal_quoting(value):
    if value:
        return value.replace('"', "'")
    else:
        return value

# Pulls Data from the caDSR API
id_list = []
fd = open("config/ca_dsr.txt")
for line in fd:
    id_list.append(line.strip())


# Cache JSON Files
for id in id_list:
    url = "https://cadsrapi.cancer.gov/rad/NCIAPI/1.0/api/DataElement/" + id
    output_file = "cache/%s.json" % id

    if not os.path.exists(output_file):
        print("Downloading from:  %s" % url)
        curl_command = [
            "curl",
            "-X",
            "GET",
            url,
            "-H",
            "accept: application/json",
            "-o",
            output_file,
        ]
        subprocess.run(curl_command, check=True)
    else:
        print("Using cached results:  %s" % output_file)

# Process the Cached JSON
for id in id_list:
    file_path = "cache/%s.json" % id
    permitted_list = []

    with open(file_path, "r") as file:
        data = json.load(file)
        dataElement = data["DataElement"]
        valueDomain = dataElement["ValueDomain"]
        if "PermissibleValues" in valueDomain:
            permissibleValues = valueDomain["PermissibleValues"]
            for permitted in permissibleValues:
                value = replace_illegal_quoting(permitted["value"])
                description = replace_illegal_quoting(permitted["valueDescription"])
                definition = replace_illegal_quoting(permitted["ValueMeaning"]["definition"])
                permitted_list.append((value, description, definition.strip()))

        if len(permitted_list) > 0:
            permitted_list.sort(key=lambda x: x[0])
            out_path = "permissible_values/%s.tsv" % id
            print("Writing to:  %s" % out_path)
            out = open(out_path, "w")
            out.write("PERMITTED_VALUE\tDESCRIPTION\tDEFINITION\n")
            for permitted in permitted_list:
                (value, description, definition) = permitted
                out.write("%s\t%s\t%s\n" % (value, description, definition))
            out.close()
