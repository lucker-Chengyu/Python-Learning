from reader import read_robots, read_destinations, read_packages, read_tasks
from tasker import is_task_executable, write_feasibility_report


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
    robots = read_robots(robots_path)
    destinations = read_destinations(destinations_path)
    packages = read_packages(packages_path)

    # Pass ID lists to read_tasks for reference validation
    destination_ids = [d['destination_id'] for d in destinations]
    package_ids = [p['package_id'] for p in packages]
    tasks = read_tasks(tasks_path, destination_ids, package_ids)

    # Check executability for each task
    results = []
    for task in tasks:
        result = is_task_executable(task, robots, destinations, packages)
        results.append(result)

    # Write the feasibility report using task IDs paired with results
    task_ids = [task['task_id'] for task in tasks]
    write_feasibility_report(report_path, task_ids, results)


if __name__ == '__main__':
    main('robots.csv', 'destinations.csv', 'packages.csv', 'tasks.csv', 'feasibility_report.txt')