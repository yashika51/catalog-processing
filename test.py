from collections import defaultdict

from utils import (apply_mappings, group_records, parse_mapping_file,
                   read_csv_file)


# Unit tests
def test_read_csv_file():
    data = read_csv_file("raw_files/pricat.csv")
    assert isinstance(data, list)
    if data:
        assert isinstance(data[0], dict)


def test_parse_mapping_file():
    # Test data
    mappings = [
        {
            "source": "winter",
            "destination": "Winter",
            "source_type": "season",
            "destination_type": "season",
        }
    ]
    direct_mapping, combined_mapping = parse_mapping_file(mappings)
    assert isinstance(direct_mapping, dict)
    assert isinstance(combined_mapping, defaultdict)
    assert direct_mapping["season"]["winter"] == "Winter"


def test_apply_mappings_unmapped_field():
    pricat_records = [{"season": "winter", "unmapped_field": "value"}]
    direct_mapping = {"season": {"winter": "Winter"}}
    combined_mapping = defaultdict(dict)
    mapped_records = apply_mappings(
        pricat_records, direct_mapping, combined_mapping, None
    )
    assert "unmapped_field" in mapped_records[0]
    assert mapped_records[0]["unmapped_field"] == "value"


def test_apply_mappings():
    pricat_records = [{"season": "winter"}]
    direct_mapping = {"season": {"winter": "Winter"}}
    combined_mapping = defaultdict(dict)
    mapped_records = apply_mappings(
        pricat_records, direct_mapping, combined_mapping, None
    )
    assert mapped_records[0]["season"] == "Winter"


# Integration test
def test_catalog_creation():
    pricat_records = read_csv_file("test_files/test_pricat.csv")
    mappings = read_csv_file("test_files/test_mappings.csv")

    direct_mapping, combined_mapping = parse_mapping_file(mappings)
    mapped_pricat_records = apply_mappings(
        pricat_records, direct_mapping, combined_mapping, None
    )
    catalog = group_records(mapped_pricat_records)

    assert isinstance(catalog, dict)
    assert "Catalog" in catalog
