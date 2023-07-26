from typing import Optional

from fastapi import APIRouter

from utils import (apply_mappings, group_records, parse_mapping_file,
                   read_csv_file)

api_router = APIRouter()


@api_router.get("/catalog")
def get_catalog(combine_fields: Optional[str] = None):
    pricat_records = read_csv_file('raw_files/pricat.csv')
    mappings = read_csv_file('raw_files/mappings.csv')

    # Parse the mappings
    direct_mapping, combined_mapping = parse_mapping_file(mappings)

    # Parse combine_fields
    combine_fields_dict = {}
    if combine_fields:
        fields_to_combine = combine_fields.split(',')
        new_field = "_".join(fields_to_combine)
        combine_fields_dict[new_field] = fields_to_combine

    # Apply the mappings to the pricat records
    mapped_pricat_records = apply_mappings(pricat_records, direct_mapping,
                                           combined_mapping, combine_fields_dict)

    # Group the mapped pricat records into a catalog
    catalog = group_records(mapped_pricat_records)

    return catalog
