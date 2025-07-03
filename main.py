"""
Main execution script for Verint Migration Toolkit.

This script sequentially runs all necessary data extractors to retrieve
and process configuration data from the legacy Verint instance.

Extractors:
- Organizations
- Groups
- Employees (requires groups for mapping)
- Roles
- Access Rights

This script is the entry point for orchestrating the Verint data extraction pipeline.
"""

from extractors.employee_extractor import extract_employees
from extractors.group_extractor import extract_groups
from extractors.organization_extractor import extract_organizations
from extractors.role_extractor import extract_roles
from extractors.access_rights_extractor import extract_access_rights

if __name__ == "__main__":
    # Extract all organization units
    #extract_organizations()

    # Extract group structure; map is needed for linking employees
    #employee_groups_map = extract_groups()

    # Extract employee details using group map
    #extract_employees(employee_groups_map)

    # Extract roles information
    extract_roles()

    # Extract access rights
    extract_access_rights()