# External Data Sources

## uberon_organ-tissue.tsv

| Data Source | Download Name | Last Update |
|-------------|---------------|------------|
| https://www.ebi.ac.uk/ols4/downloads |mappings_sssom.tsv.gz | Mar. 7, 2025 |

Processing:
- Decompress mappings_sssom.tsv.gz 
- Find uberon.ols.sssom.tsv
- Remove header, extract subject_id (code) values and , relabel as "Permissible Value" and 

``` {bash}
echo -e "Permissible Value\tLabel" > uberon_organ-tissue.tsv
egrep -v "^#|^subject_id" uberon.ols.sssom.tsv | cut -f1,5 | sort -u >> uberon_organ-tissue.tsv
```
