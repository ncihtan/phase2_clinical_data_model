# External Data Sources

The External Data Sources provided in this directory can be used to search for permissible values within an Ontology or Standard. The following information explains how these files were obtained.

## CL (Cell Type Ontology): CL _codes_human.tsv

| Data Source | Download Name | Last Update |
|-------------|---------------|------------|
| https://github.com/obophenotype/cell-ontology/releases/tag/v2025-02-13 | human-view.tsv | Mar. 11, 2025 |

Processing (via Jupyter Notebook):
- Extracted code from end of url provided in "?x" in format "CL:#######"
- Changed order of columns to "code", "?label", "?x"
- Renamed columns to "Permissible Value", "Label" and "URL"

## MONDO.tsv

| Data Type |  Data Source | Download Name | Last Update |
|-----------|-------------|---------------|------------|
| mondo terms, NCIT, ICD-10-CM and ICD-9 mappings |https://www.ebi.ac.uk/ols4/downloads |mappings_sssom.tsv.gz | Mar. 7, 2025 |
| ICD-O-3.1 mappings | https://evsexplore.semantics.cancer.gov/evsexplore/mappings | ICDO_TO_NCI_MORPHOLOGY: Version 2017-12-2 | Mar. 11, 2025 |

Processing (via Jupyter Notebook):
- Decompress mappings_sssom.tsv.gz 
- Find mondo.ols.sssom.tsv
- Process mondo.ols.sssom.tsv to 
    - remove header;
    - retain only subject_id, subject_label, object_label;
    - explode object_label and retain only NCIT, ICD-10-CM and ICD-9 mappings; 
    - rename "subject_id" and "subject_label" as "Permissible Value", "Label"; and
    - add ICD-O-3.1 mapping from ICDO_TO_NCI_MORPHOLOGY file.

## UBERON: uberon_organ-tissue.tsv

| Data Source | Download Name | Last Update |
|-------------|---------------|------------|
| https://www.ebi.ac.uk/ols4/downloads |mappings_sssom.tsv.gz | Mar. 7, 2025 |

Processing:
- Decompress mappings_sssom.tsv.gz 
- Find uberon.ols.sssom.tsv
- Use the following code to:
    - remove header;
    - extract unique subject_id (code) values and "subject_label"; and
    - relabel as "Permissible Value" and "Label".

``` {bash}
echo -e "Permissible Value\tLabel" > uberon_organ-tissue.tsv
egrep -v "^#|^subject_id" uberon.ols.sssom.tsv | cut -f1,5 | sort -u >> uberon_organ-tissue.tsv
```
