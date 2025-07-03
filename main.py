from extractors.employee_extractor import extract_employees
from extractors.group_extractor import extract_groups
from extractors.organization_extractor import extract_organizations
from extractors.role_extractor import extract_roles
from extractors.access_rights_extractor import extract_access_rights

if __name__ == "__main__":
    extract_organizations()
    employee_groups_map = extract_groups()
    extract_employees(employee_groups_map)
    extract_roles()
    extract_access_rights()
