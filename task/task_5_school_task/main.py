import csv
import sys


def read_robots(robots_path: str) -> list[list]:
    """Read and validate robot records from a CSV file.

    Args:
        robots_path: Path to the robots CSV file.

    Returns:
        A list of four aligned lists: [robot_ids, battery_levels, max_loads, zones].
    """
    robot_ids = []
    battery_levels = []
    max_loads = []
    zones = []

    with open(robots_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row

        for row in reader:
            robot_id = row[0]
            battery_level = int(row[1])
            max_load = float(row[2])
            zone = row[3]

            # Validate battery level is an integer in range 0 to 100
            if not (0 <= battery_level <= 100):
                print(f"Warning: Robot {robot_id} has invalid battery level ({battery_level}).", file=sys.stderr)
                continue

            # Validate max_load is a non-negative number
            if max_load < 0:
                print(f"Warning: Robot {robot_id} has invalid max load ({max_load}).", file=sys.stderr)
                continue

            # Validate zone contains only uppercase letters
            if not zone or not zone.isupper() or not zone.isalpha():
                print(f"Warning: Robot {robot_id} has invalid zone ({zone}).", file=sys.stderr)
                continue

            robot_ids.append(robot_id)
            battery_levels.append(battery_level)
            max_loads.append(max_load)
            zones.append(zone)

    return [robot_ids, battery_levels, max_loads, zones]


def read_destinations(destinations_path: str) -> list[list]:
    """Read and validate destination records from a CSV file.

    Args:
        destinations_path: Path to the destinations CSV file.

    Returns:
        A list of two aligned lists: [destination_ids, zones].
    """
    destination_ids = []
    zones = []

    with open(destinations_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row

        for row in reader:
            destination_id = row[0]
            zone = row[1]

            # Validate zone contains only uppercase letters
            if not zone or not zone.isupper() or not zone.isalpha():
                print(f"Warning: Destination {destination_id} has invalid zone ({zone}).", file=sys.stderr)
                continue

            destination_ids.append(destination_id)
            zones.append(zone)

    return [destination_ids, zones]


def read_packages(packages_path: str) -> list[list]:
    """Read and validate package records from a CSV file.

    Args:
        packages_path: Path to the packages CSV file.

    Returns:
        A list of two aligned lists: [package_ids, weights].
    """
    package_ids = []
    weights = []

    with open(packages_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row

        for row in reader:
            package_id = row[0]
            weight = float(row[1])

            # Validate weight is a non-negative number
            if weight < 0:
                print(f"Warning: Package {package_id} has invalid weight ({weight}).", file=sys.stderr)
                continue

            package_ids.append(package_id)
            weights.append(weight)

    return [package_ids, weights]


def read_tasks(tasks_path: str, destination_ids: list[str], package_ids: list[str]) -> list[list]:
    """Read and validate task records from a CSV file.

    Args:
        tasks_path: Path to the tasks CSV file.
        destination_ids: List of valid destination IDs for reference validation.
        package_ids: List of valid package IDs for reference validation.

    Returns:
        A list of five aligned lists: [task_ids, source_ids, target_ids, task_package_ids, statuses].
    """
    task_ids = []
    source_ids = []
    target_ids = []
    task_package_ids = []
    statuses = []

    with open(tasks_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row

        for row in reader:
            task_id = row[0]
            source_id = row[1]
            target_id = row[2]
            package_id = row[3]
            status = row[4]

            # Validate that referenced IDs exist in their respective tables
            if source_id not in destination_ids:
                print(f"Warning: Task {task_id} has invalid source_id ({source_id}).", file=sys.stderr)
                continue

            if target_id not in destination_ids:
                print(f"Warning: Task {task_id} has invalid target_id ({target_id}).", file=sys.stderr)
                continue

            if package_id not in package_ids:
                print(f"Warning: Task {task_id} has invalid package_id ({package_id}).", file=sys.stderr)
                continue

            # Validate status is one of the accepted values
            if status not in ('pending', 'complete'):
                print(f"Warning: Task {task_id} has invalid status ({status}).", file=sys.stderr)
                continue

            task_ids.append(task_id)
            source_ids.append(source_id)
            target_ids.append(target_id)
            task_package_ids.append(package_id)
            statuses.append(status)

    return [task_ids, source_ids, target_ids, task_package_ids, statuses]


def is_task_executable(task_id: str, package_ids: list[str], package_weights: list[float],
                       robot_ids: list[str], max_loads: list[float], robot_zones: list[str],
                       destination_ids: list[str], destination_zones: list[str],
                       task_ids: list[str], source_ids: list[str], target_ids: list[str],
                       task_package_ids: list[str]) -> bool:
    """Determine whether a task can be executed by at least one robot.

    A task is executable if there exists a robot in the same zone as both
    the source and target, with sufficient load capacity for the package.

    Args:
        task_id: The ID of the task to check.
        package_ids: List of all package IDs.
        package_weights: List of weights aligned with package_ids.
        robot_ids: List of all robot IDs.
        max_loads: List of max loads aligned with robot_ids.
        robot_zones: List of zones aligned with robot_ids.
        destination_ids: List of all destination IDs.
        destination_zones: List of zones aligned with destination_ids.
        task_ids: List of all task IDs.
        source_ids: List of source destination IDs aligned with task_ids.
        target_ids: List of target destination IDs aligned with task_ids.
        task_package_ids: List of package IDs aligned with task_ids.

    Returns:
        True if the task is executable, False otherwise.
    """
    # Look up this task's source, target and package
    task_index = task_ids.index(task_id)
    source_id = source_ids[task_index]
    target_id = target_ids[task_index]
    package_id = task_package_ids[task_index]

    # Look up the zone for the source and target destinations
    source_zone = destination_zones[destination_ids.index(source_id)]
    target_zone = destination_zones[destination_ids.index(target_id)]

    # Look up the weight of the package to be delivered
    package_weight = package_weights[package_ids.index(package_id)]

    # Check if any robot shares the zone and can carry the package
    for i in range(len(robot_ids)):
        same_zone = robot_zones[i] == source_zone and robot_zones[i] == target_zone
        sufficient_load = max_loads[i] >= package_weight
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


def main(robots_path: str, destinations_path: str, packages_path: str,
         tasks_path: str, report_path: str) -> None:
    """Load all CSV data, check task feasibility, and write a report.

    Args:
        robots_path: Path to the robots CSV file.
        destinations_path: Path to the destinations CSV file.
        packages_path: Path to the packages CSV file.
        tasks_path: Path to the tasks CSV file.
        report_path: Path to write the feasibility report.

    Returns:
        None
    """
    # Read and validate all data from CSV files
    robot_ids, battery_levels, max_loads, robot_zones = read_robots(robots_path)
    destination_ids, dest_zones = read_destinations(destinations_path)
    package_ids, weights = read_packages(packages_path)
    task_ids, source_ids, target_ids, task_package_ids, statuses = read_tasks(
        tasks_path, destination_ids, package_ids
    )

    # Check executability for each task
    results = []
    for task_id in task_ids:
        result = is_task_executable(
            task_id, package_ids, weights,
            robot_ids, max_loads, robot_zones,
            destination_ids, dest_zones,
            task_ids, source_ids, target_ids, task_package_ids
        )
        results.append(result)

    # Write the feasibility report using task IDs paired with results
    write_feasibility_report(report_path, task_ids, results)


if __name__ == '__main__':
    main('robots.csv', 'destinations.csv', 'packages.csv', 'tasks.csv', 'feasibility_report.txt')





