def detect_requirement_changes(old_requirements, new_requirements):
    """
    Compare two requirement versions and identify
    added, removed, and modified requirements.
    """

    old_map = {
        requirement["id"]: requirement
        for requirement in old_requirements
    }

    new_map = {
        requirement["id"]: requirement
        for requirement in new_requirements
    }

    changes = {
        "added": [],
        "removed": [],
        "modified": []
    }

    for requirement_id, new_requirement in new_map.items():

        if requirement_id not in old_map:
            changes["added"].append(new_requirement)
            continue

        old_requirement = old_map[requirement_id]

        if old_requirement != new_requirement:
            changes["modified"].append({
                "id": requirement_id,
                "old": old_requirement,
                "new": new_requirement
            })

    for requirement_id, old_requirement in old_map.items():

        if requirement_id not in new_map:
            changes["removed"].append(old_requirement)

    return changes