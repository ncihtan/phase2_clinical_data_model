import subprocess
import os.path
import json

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

    with open(file_path, "r") as file:
        data = json.load(file)
        dataElement = data["DataElement"]
        valueDomain = dataElement["ValueDomain"]
        if "PermissibleValues" in valueDomain:
            permissibleValues = valueDomain["PermissibleValues"]
            if len(permissibleValues) > 0:
                out_path = "permissible_values/%s.tsv" % id
                print("Writing to:  %s" % out_path)
                out = open(out_path, "w")
                out.write("PERMITTED_VALUE\tDESCRIPTION\tDEFINITION\n")
                for permitted in permissibleValues:
                    value = permitted["value"]
                    description = permitted["valueDescription"]
                    definition = permitted["ValueMeaning"]["definition"]
                    out.write("%s\t%s\t%s\n" % (value, description, definition.strip()))
                out.close()
