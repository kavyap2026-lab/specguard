from specguard.requirement_parser import load_requirements
from specguard.test_mapper import find_requirement_tests
from specguard.change_detector import detect_requirement_changes
from specguard.review_tracker import load_reviewed_requirements
from specguard.html_report import generate_html_report


OLD_REQUIREMENTS_FILE = "requirements/requirements_v1.yaml"
NEW_REQUIREMENTS_FILE = "requirements/requirements_v2.yaml"
TESTS_DIRECTORY = "tests"
REVIEW_STATUS_FILE = "config/review_status.yaml"
HTML_REPORT_FILE = "reports/specguard_report.html"


def main():

    # Load both requirement versions
    old_requirements = load_requirements(OLD_REQUIREMENTS_FILE)
    new_requirements = load_requirements(NEW_REQUIREMENTS_FILE)

    # Find requirement-to-test mappings
    requirement_map = find_requirement_tests(TESTS_DIRECTORY)

    # Compare requirement versions
    changes = detect_requirement_changes(
        old_requirements,
        new_requirements
    )

    reviewed_requirements = load_reviewed_requirements(
        REVIEW_STATUS_FILE
    )

    print("=" * 72)
    print("                         SPECGUARD")
    print("          Requirement Coverage & Change Analysis")
    print("=" * 72)

    # -------------------------------------------------
    # REQUIREMENT COVERAGE
    # -------------------------------------------------

    print("\nREQUIREMENT COVERAGE")
    print("-" * 72)

    covered = 0

    for requirement in new_requirements:

        requirement_id = requirement["id"]
        title = requirement["title"]

        tests = requirement_map.get(requirement_id, [])

        if tests:
            status = "COVERED"
            covered += 1
        else:
            status = "MISSING"

        print(
            f"{requirement_id:8} "
            f"{status:10} "
            f"{len(tests):2} test(s) | "
            f"{title}"
        )

    total = len(new_requirements)

    coverage = (covered / total * 100) if total else 0

    print("-" * 72)
    print(f"Total requirements:   {total}")
    print(f"Covered requirements: {covered}")
    print(f"Missing requirements: {total - covered}")
    print(f"Requirement coverage: {coverage:.1f}%")

    # -------------------------------------------------
    # CHANGE IMPACT ANALYSIS
    # -------------------------------------------------

    print("\nCHANGE IMPACT ANALYSIS")
    print("-" * 72)

    print(f"Added requirements:    {len(changes['added'])}")
    print(f"Removed requirements:  {len(changes['removed'])}")
    print(f"Modified requirements: {len(changes['modified'])}")

    # Display modified requirements
    for change in changes["modified"]:

        requirement_id = change["id"]

        old_description = change["old"]["description"].strip()
        new_description = change["new"]["description"].strip()

        associated_tests = requirement_map.get(
            requirement_id,
            []
        )

        print("\n" + "!" * 72)

        if requirement_id in reviewed_requirements:
            print(f"REVIEWED: {requirement_id}")
        else:
            print(f"REVIEW REQUIRED: {requirement_id}")

        print(f"\nOLD REQUIREMENT:")
        print(old_description)

        print(f"\nNEW REQUIREMENT:")
        print(new_description)

        print(
            f"\nAssociated tests: "
            f"{len(associated_tests)}"
        )

        for test in associated_tests:
            print(f"  - {test}")

        if requirement_id in reviewed_requirements:
            print("\nSTATUS: REVIEWED"
            )

        elif associated_tests:
            print("\nSTATUS: REVIEW REQUIRED")
            print(
                "WARNING: Requirement changed. "
                "Existing tests may need review."
            )

        else:
            print("\nSTATUS: REVIEW REQUIRED")
            print(
                "WARNING: Requirement changed "
                "and no associated tests were found."
            )

        print("!" * 72)

    print("\n" + "=" * 72)
    
    generate_html_report(
        requirements=new_requirements,
        requirement_map=requirement_map,
        changes=changes,
        reviewed_requirements=reviewed_requirements,
        output_file=HTML_REPORT_FILE
    )

    print(
        f"\nHTML report generated: "
        f"{HTML_REPORT_FILE}"
    )

if __name__ == "__main__":
    main()