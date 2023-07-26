import csv
from collections import defaultdict
from itertools import groupby
from operator import itemgetter
from typing import Dict, List, Optional, Tuple


def read_csv_file(file_path: str) -> List[Dict]:
    """Load a CSV file and convert it into a list of dictionaries"""
    with open(file_path, "r") as file:
        reader = csv.reader(file, delimiter=";")
        header = next(reader)
        data = [dict(zip(header, row)) for row in reader]
    return data


def parse_mapping_file(mapping_records: List[Dict]) -> Tuple[Dict, defaultdict]:
    """Parse the mapping file records into a dictionary for efficient lookup."""
    direct_mapping = {}
    combined_mapping = defaultdict(dict)

    for record in mapping_records:
        if (
            "source_type" not in record
            or "source" not in record
            or "destination" not in record
        ):
            continue

        if "|" in record["source_type"]:
            # Case for combined mapping
            source_types = record["source_type"].split("|")
            source_values = record["source"].split("|")
            combined_mapping[tuple(source_types)][tuple(source_values)] = record[
                "destination"
            ]
        else:
            # Case for direct mapping
            direct_mapping[record["source_type"]] = {record["source"]: record["destination"]}

    return direct_mapping, combined_mapping


def apply_mappings(
    pricat_records: List[Dict], direct_mapping: Dict, combined_mapping: dict, combine_fields: Optional[Dict]
) -> List[Dict]:
    """Apply the mappings to the pricat records."""
    for record in pricat_records:
        for field in record:
            if field in direct_mapping:
                # Check if a direct mapping exists and apply it
                if record[field] in direct_mapping[field]:
                    record[field] = direct_mapping[field][record[field]]
            elif field in combined_mapping:
                # Check if a combined mapping exists and apply it
                if (field, record[field]) in combined_mapping:
                    record[field] = combined_mapping[(field, record[field])]
            else:
                # Copy unmapped fields
                record[field] = record[field]

        # Combine fields if specified
        if combine_fields:
            for new_field, fields_to_combine in combine_fields.items():
                record[new_field] = " ".join(str(record[field]) for field in fields_to_combine)

    return pricat_records


def group_records(mapped_pricat_records: List[Dict]) -> Dict:
    """Group the records into a hierarchical structure: Catalog -> Article -> Variation."""
    # Sort the records by article number for grouping
    sorted_records = sorted(mapped_pricat_records, key=itemgetter("article_number"))

    # Initialize the catalog
    catalog = {"Catalog": {"brand": sorted_records[0]["brand"], "articles": []}}

    # Group the records by article number
    for article_number, group in groupby(sorted_records, key=itemgetter("article_number")):
        variations = list(group)

        # Initialize the article
        article = {"article_number": article_number, "variations": []}

        # Add the variations to the article
        for variation in variations:
            article_variation = {}
            for key, value in variation.items():
                # Exclude brand and article_number from variations
                if key not in ("brand", "article_number"):
                    article_variation[key] = value
            article["variations"].append(article_variation)

        # Add the article to the catalog
        catalog["Catalog"]["articles"].append(article)

    # in case we also want to save the data in json file
    # with open('catalog.json', 'w') as f:
    #     json.dump(catalog, f)
    return catalog
