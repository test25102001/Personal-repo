def bug_update(bug_data):
    # Get or create a Bug object to put the parsed data in.
    try:
        bug = Bug.all_bugs.get(
            canonical_bug_link=bug_data['canonical_bug_link'])
    except Bug.DoesNotExist:
        bug = Bug(canonical_bug_link=bug_data['canonical_bug_link'])

    # Fill the Bug.
    for key in bug_data:
        value = bug_data[key]
        setattr(bug, key, value)

    # Save the project onto it.
    # Project name is just the TrackerModel's tracker_name, as due to the
    # way Roundup is set up, there is almost always one project per tracker.
    # This could in theory not be the case, but until we find a Roundup
    # tracker handling bugs for multiple projects, we will just support one
    # project per tracker.
    project_from_name, _ = Project.objects.get_or_create(
            name=bug_data['tracker'].tracker_name)
    # Manually save() the Project to ensure that if it was created then it has
    # a display_name.
    if not project_from_name.display_name:
        project_from_name.save()
    bug.project = project_from_name

    # Store the tracker that generated the Bug, update last_polled and save it!
    bug.last_polled = datetime.utcnow()
    bug.save()
