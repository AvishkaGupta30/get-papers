import argparse
import csv
import re
from typing import List, Dict, Any
from Bio import Entrez, Medline


Entrez.email = "pinkkygupta1@gmail.com"

def search_pubmed(query: str, retmax: int = 20) -> List[str]:
    handle = Entrez.esearch(db="pubmed", term=query, retmax=retmax)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

def fetch_details(id_list: List[str]) -> List[Dict[str, Any]]:
    ids = ",".join(id_list)
    handle = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="text")
    records = list(Medline.parse(handle))
    handle.close()
    return records

def is_non_academic(affiliation: str) -> bool:
    non_academic_keywords = ["pharma", "biotech", "inc", "ltd", "llc", "company", "corporation", "industries"]
    academic_keywords = ["university", "college", "institute", "hospital", "school", "dept", "laboratory", "centre", "center"]
    affil_lower = affiliation.lower()
    return any(word in affil_lower for word in non_academic_keywords) and not any(word in affil_lower for word in academic_keywords)

def extract_info(record: Dict[str, Any]) -> Dict[str, str]:
    pmid = record.get("PMID", "")
    title = record.get("TI", "").replace("\n", " ")
    title = title[:100] + "..." if len(title) > 100 else title
    date = record.get("DP", "")

    authors = record.get("AU", [])
    affiliations = record.get("AD", "")
    if isinstance(affiliations, list):
        affiliations = " | ".join(affiliations)

    author_name = "N/A"
    company_affil = "N/A"
    email = "N/A"

    if affiliations:
        affils = affiliations.split("|")
        for affil in affils:
            affil = affil.strip()
            if is_non_academic(affil):
                company_affil = affil
                match = re.search(r"[A-Z][a-z]+ [A-Z][a-z]+", affil)
                if match:
                    author_name = match.group(0)
                email_match = re.search(r"[\w\.-]+@[\w\.-]+", affil)
                if email_match:
                    email = email_match.group(0)
                break

    return {
        "PubMed ID": pmid,
        "Title": title,
        "Publication Date": date,
        "Non-academic Author": author_name,
        "Company Affiliation": company_affil,
        "Corresponding Author Email": email
    }

def save_to_csv(data: List[Dict[str, str]], filename: str):
    fieldnames = ["PubMed ID", "Title", "Publication Date", "Non-academic Author", "Company Affiliation", "Corresponding Author Email"]
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description="Fetch and filter PubMed research papers.")
    parser.add_argument("--query", required=True, help="Search query for PubMed")
    parser.add_argument("--file", help="Output CSV filename")
    parser.add_argument("--debug", action="store_true", help="Enable debug messages")
    args = parser.parse_args()

    if args.debug:
        print(f"Searching for query: {args.query}")

    ids = search_pubmed(args.query)
    records = fetch_details(ids)

    if args.debug:
        print(f"Found {len(records)} records")

    results = []
    for record in records:
        info = extract_info(record)
        if info["Company Affiliation"] != "N/A":
            results.append(info)

    if args.file:
        save_to_csv(results, args.file)
        if args.debug:
            print(f"Results saved to {args.file}")
    else:
        for row in results:
            print(row)

if __name__ == "__main__":
    main()
