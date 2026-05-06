def is_task_executable(task: dict, robots: list[dict], destinations: list[dict], packages: list[dict]) -> bool:
    """Determine whether a task can be executed by at least one robot.

    A task is executable if there exists a robot in the same zone as both
    the source and target, with sufficient load capacity for the package.

    Args:
        task: A task record dictionary.
        robots: List of valid robot record dictionaries.
        destinations: List of valid destination record dictionaries.
        packages: List of valid package record dictionaries.

    Returns:
        True if the task is executable, False otherwise.
    """
    source_id = task['source_id']
    target_id = task['target_id']
    package_id = task['package_id']

    # Look up the zone for the source and target destinations
    source_zone = next(row['zone'] for row in destinations if row['destination_id'] == source_id)
    target_zone = next(row['zone'] for row in destinations if row['destination_id'] == target_id)

    # Look up the weight of the package to be delivered
    package_weight = next(row['weight'] for row in packages if row['package_id'] == package_id)

    # Check if any robot shares the zone and can carry the package
    for robot in robots:
        same_zone = robot['zone'] == source_zone and robot['zone'] == target_zone
        sufficient_load = robot['max_load'] >= package_weight
        if same_zone and sufficient_load:
            return True

    return False


def write_feasibility_report(file_path: str, task_ids: list[str], results: list[bool]) -> None:
    """Write a task feasibility report to a text file.

    Args:
        file_path: Path to the output report file.
        task_ids: List of task IDs in order.
        results: List of booleans indicating executability for each task.

    Returns:
        None
    """
    executable_count = 0
    non_executable_count = 0
    lines = ["Task Feasibility Report\n", "\n"]

    # Write the result for each task and accumulate totals
    for task_id, result in zip(task_ids, results):
        if result:
            lines.append(f"{task_id}: executable\n")
            executable_count += 1
        else:
            lines.append(f"{task_id}: not executable\n")
            non_executable_count += 1

    lines.append("\n")
    lines.append(f"Executable tasks: {executable_count}\n")
    lines.append(f"Non-executable tasks: {non_executable_count}\n")

    with open(file_path, 'w') as f:
        f.writelines(lines)