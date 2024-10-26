from Bio import ExPASy, SwissProt
import pandas as pd

def fetch_and_parse_uniprot(ids):
    records = []

    for protein_id in ids:
        try:
            handle = ExPASy.get_sprot_raw(protein_id)
            record = SwissProt.read(handle)
            go_terms = {
                "C": [],
                "F": [],
                "P": []
            }
            for ref in record.cross_references:
                if ref[0] == "GO":
                    term_type = ref[2][0]
                    term_desc = ref[2][2:]
                    go_terms[term_type].append(term_desc)

            protein_data = {
                "ID": record.entry_name,
                "Name": record.description,
                "Organism": record.organism,
                "Cellular Component": ", ".join(go_terms["C"]),
                "Molecular Function": ", ".join(go_terms["F"]),
                "Biological Process": ", ".join(go_terms["P"])
            }
            records.append(protein_data)

        except Exception as e:
            print(f"Failed to fetch or parse the record for {protein_id}: {e}")

    return pd.DataFrame(records)

protein_ids = ["A0A1H8M005", "A0A1H8LYM5", "A0A1H8JSI3", "A0A1H8FZU7"]
df = fetch_and_parse_uniprot(protein_ids)

df_transposed = df.transpose()

df_transposed.to_csv("transposed_protein_go_data.csv", index=True)

print(df_transposed)