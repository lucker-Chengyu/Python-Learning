import sys
import re

# ID format: one or more uppercase letters followed by a non-negative integer with no leading zeros
VALID_ID = re.compile(r'[A-Z]+(0|[1-9][0-9]*)')


def read_to_table(path: str) -> list[dict]:
    """Read a CSV file and return its contents as a data table.

    Args:
        path: Path to the CSV file.

    Returns:
        A list of dictionaries where each dictionary represents a row,
        with CSV headers as keys. All values are stored as strings.
    """
    table = []

    with open(path, 'r') as f:
        lines = f.readlines()
        headers = lines[0].strip().split(',')

        # Map each row to a dictionary using the header as keys
        for line in lines[1:]:
            values = line.strip().split(',')
            record = {}
            for i in range(len(headers)):
                record[headers[i]] = values[i]
            table.append(record)

    return table


def read_robots(robots_path: str) -> list[dict]:
    """Read and validate robot records from a CSV file.

    Args:
        robots_path: Path to the robots CSV file.

    Returns:
        A list of valid robot record dictionaries with typed numeric fields.
    """
    table = read_to_table(robots_path)
    robots = []

    for row in table:
        robot_id = row['robot_id']

        # Validate battery level is an integer in range 0 to 100
        if not re.fullmatch(r'([0-9]|[1-9][0-9]|100)', row['battery_level']):
            print(f"Warning: Robot {robot_id} has invalid battery level ({row['battery_level']}).", file=sys.stderr)
            continue

        # Validate max_load is a non-negative number
        if not re.fullmatch(r'(0|[1-9][0-9]*)(\.([0-9]*[1-9]|0))?', row['max_load']):
            print(f"Warning: Robot {robot_id} has invalid max load ({row['max_load']}).", file=sys.stderr)
            continue

        # Validate zone contains only uppercase letters
        if not re.fullmatch(r'[A-Z]+', row['zone']):
            print(f"Warning: Robot {robot_id} has invalid zone ({row['zone']}).", file=sys.stderr)
            continue

        # Convert numeric fields to their appropriate types
        robots.append({
            'robot_id': robot_id,
            'battery_level': int(row['battery_level']),
            'max_load': float(row['max_load']),
            'zone': row['zone']
        })

    return robots


def read_destinations(destinations_path: str) -> list[dict]:
    """Read and validate destination records from a CSV file.

    Args:
        destinations_path: Path to the destinations CSV file.

    Returns:
        A list of valid destination record dictionaries.
    """
    table = read_to_table(destinations_path)
    destinations = []

    for row in table:
        destination_id = row['destination_id']

        # Validate destination ID follows the required format
        if not VALID_ID.fullmatch(destination_id):
            print(f"Warning: Destination {destination_id} has invalid id ({destination_id}).", file=sys.stderr)
            continue

        # Validate zone contains only uppercase letters
        if not re.fullmatch(r'[A-Z]+', row['zone']):
            print(f"Warning: Destination {destination_id} has invalid zone ({row['zone']}).", file=sys.stderr)
            continue

        destinations.append(row)

    return destinations


def read_packages(packages_path: str) -> list[dict]:
    """Read and validate package records from a CSV file.

    Args:
        packages_path: Path to the packages CSV file.

    Returns:
        A list of valid package record dictionaries with typed numeric fields.
    """
    table = read_to_table(packages_path)
    packages = []

    for row in table:
        package_id = row['package_id']

        # Validate weight is a non-negative number
        if not re.fullmatch(r'(0|[1-9][0-9]*)(\.([0-9]*[1-9]|0))?', row['weight']):
            print(f"Warning: Package {package_id} has invalid weight ({row['weight']}).", file=sys.stderr)
            continue

        # Convert weight to float for numeric comparison
        packages.append({
            'package_id': package_id,
            'weight': float(row['weight'])
        })

    return packages


def read_tasks(tasks_path: str, destination_ids: list[str], package_ids: list[str]) -> list[dict]:
    """Read and validate task records from a CSV file.

    Args:
        tasks_path: Path to the tasks CSV file.
        destination_ids: List of valid destination IDs for reference validation.
        package_ids: List of valid package IDs for reference validation.

    Returns:
        A list of valid task record dictionaries.
    """
    table = read_to_table(tasks_path)
    tasks = []

    for row in table:
        task_id = row['task_id']
        source_id = row['source_id']
        target_id = row['target_id']
        package_id = row['package_id']
        status = row['status']

        # Validate ID format: one or more uppercase letters followed by digits with no leading zeros
        if not VALID_ID.fullmatch(source_id):
            print(f"Warning: Task {task_id} has invalid source_id format ({source_id}).", file=sys.stderr)
            continue

        if not VALID_ID.fullmatch(target_id):
            print(f"Warning: Task {task_id} has invalid target_id format ({target_id}).", file=sys.stderr)
            continue

        if not VALID_ID.fullmatch(package_id):
            print(f"Warning: Task {task_id} has invalid package_id format ({package_id}).", file=sys.stderr)
            continue

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

        tasks.append(row)

    return tasks


def read_schedules(schedules_path: str, robot_ids: list[str], task_ids: list[str]) -> list[dict]:
    """Read and validate schedule records from a CSV file.

    Each row contains a schedule ID, a robot ID, and one or more task IDs.
    There is no header row in this file. Rows referencing invalid robot or
    task IDs are skipped with a warning.

    Args:
        schedules_path: Path to the schedules CSV file.
        robot_ids: List of valid robot IDs for reference validation.
        task_ids: List of valid task IDs for reference validation.

    Returns:
        A list of valid schedule dictionaries with keys: schedule_id, robot_id, task_ids.
    """
    schedules = []

    with open(schedules_path, 'r') as f:
        lines = f.readlines()

        for line in lines:
            row = line.strip().split(',')
            if len(row) < 2:
                continue

            schedule_id = row[0]
            robot_id = row[1]
            schedule_task_ids = row[2:]

            # Validate the assigned robot exists
            if robot_id not in robot_ids:
                print(f"Warning: Schedule {schedule_id} has invalid robot_id ({robot_id}).", file=sys.stderr)
                continue

            # Validate all task IDs in the schedule exist
            valid = True
            for tid in schedule_task_ids:
                if tid not in task_ids:
                    print(f"Warning: Schedule {schedule_id} has invalid task_id ({tid}).", file=sys.stderr)
                    valid = False
                    break
            if not valid:
                continue

            schedules.append({
                'schedule_id': schedule_id,
                'robot_id': robot_id,
                'task_ids': schedule_task_ids
            })

    return schedules


def read_distances(distances_path: str) -> list[list[float]]:
    """Read a distance matrix from a CSV file.

    The matrix has no header. Index 0 represents the origin,
    and index i represents destination D_i.

    Args:
        distances_path: Path to the distances CSV file.

    Returns:
        A 2D list of floats representing pairwise distances in km.
    """
    distances = []

    with open(distances_path, 'r') as f:
        lines = f.readlines()

        for line in lines:
            # Skip any empty rows that may appear at the end of the file
            if line.strip():
                distances.append([float(x) for x in line.strip().split(',')])

    return distances