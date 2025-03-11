# Extract Diseases from NCI Thesaurus
# Diseases are defined as any descendent of C2991


def node_descends_from(node_id, ancestor_id, parent_map):
    """Determines if node_id descends from ancestor_id."""
    parent_id = parent_map[node_id]
    while parent_id is not None and parent_id != ancestor_id:
        node_id = parent_id
        if node_id in parent_map:
            parent_id = parent_map[node_id]
        else:
            parent_id = None
    if parent_id == ancestor_id:
        return True
    else:
        return False


# First Pass
parent_map = {}
nci_path = "external/nci_thesarus.txt"
out_path = "external/ncit_diagnosis.tsv"

fd = open(nci_path)
for line in fd:
    parts = line.split("\t")
    id = parts[0]
    parent_id = parts[2]
    parent_id_list = parent_id.split("|")
    for parent_id in parent_id_list:
        parent_map[id] = parent_id

# Second Pass
fd = open(nci_path)
out = open(out_path, "w")
print("Writing to:  %s" % out_path)
out.write("Permitted_Value\tParent_ID\tLabel\tDescription\tCategory\n")
for line in fd:
    parts = line.split("\t")
    id = parts[0]
    parent_id = parts[2]
    label = parts[3]
    description = parts[4]
    category = parts[7]
    if node_descends_from(id, "C2991", parent_map):
        out.write(
            "%s\t%s\t%s\t%s\t%s\n" % (id, parent_id, label, description, category)
        )
fd.close()
out.close()
print("Please convert the file to excel manually")
