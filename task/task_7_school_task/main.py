import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

from reader import read_robots, read_destinations, read_packages, read_tasks
from reader import read_schedules, read_distances
from tasker import is_task_executable, check_schedule


def write_feasability_report(report_path: str, tasks: list, results: list[bool],
                             schedules: list, schedule_report: list) -> None:
    """Write a combined task and schedule feasibility report to a text file.

    Args:
        report_path: Path to the output report file.
        tasks: List of task record dictionaries.
        results: List of booleans indicating executability for each task.
        schedules: List of schedule record dictionaries.
        schedule_report: List of check_schedule results for each schedule.

    Returns:
        None
    """
    executable_count = 0
    non_executable_count = 0

    with open(report_path, "w") as file:
        file.write("Task Feasibility Report\n\n")

        # Write individual task results and accumulate totals
        for i in range(len(tasks)):
            if results[i] == True:
                file.write(tasks[i]["task_id"] + ": executable\n")
                executable_count += 1
            else:
                file.write(tasks[i]["task_id"] + ": not executable\n")
                non_executable_count += 1

        file.write("\n")
        file.write("Executable tasks: " + str(executable_count) + "\n")
        file.write("Non-executable tasks: " + str(non_executable_count) + "\n\n")

        file.write("Schedule feasibility\n\n")

        # Write schedule results with travel summary for feasible schedules
        for i in range(len(schedules)):
            schedule = schedules[i]
            result = schedule_report[i]

            if result is None:
                file.write(schedule["schedule_id"] + ": Infeasible\n")
            else:
                final_state = result[-1]
                hours = final_state[0]
                distance = final_state[1]
                battery = final_state[3]

                file.write(
                    schedule["schedule_id"] + ": Robot " + schedule["robot_id"] +
                    " completed schedule in " + format(hours, ".2f") +
                    " hours and covered " + format(distance, ".2f") +
                    " km. Battery remaining " + format(battery, ".2f") + "%.\n")


def plot_schedule_positions(schedules: list, schedule_report: list, plot_file: str) -> None:
    """Plot each feasible schedule's distance from the origin over time.

    All feasible schedules are drawn on the same figure as separate lines.
    The plot is saved to a file and not displayed interactively.

    Args:
        schedules: List of schedule dictionaries as returned by read_schedules.
        schedule_report: List of check_schedule results, one per schedule.
        plot_file: File path to save the plot to.

    Returns:
        None
    """
    plt.figure()

    for i in range(len(schedules)):
        if schedule_report[i] is not None:
            times = []
            distances_from_origin = []

            # Extract time and distance-from-origin at each recorded stop
            for row in schedule_report[i]:
                times.append(row[0])
                distances_from_origin.append(row[2])

            data = pd.DataFrame({
                "time": times,
                "distance_from_origin": distances_from_origin})

            plt.plot(
                data["time"],
                data["distance_from_origin"],
                marker="o",
                label=schedules[i]["robot_id"])

    plt.xlabel("Time (hours)")
    plt.ylabel("Distance from Origin (km)")
    plt.title("Robot Position Over Time")
    plt.legend()
    plt.grid(True)
    plt.savefig(plot_file)
    plt.close()


def main(robots_path: str, destinations_path: str, packages_path: str,
         tasks_path: str, schedules_path: str, distances_path: str,
         report_path: str, plot_file: str) -> None:
    """Load all CSV data, check feasibility, write a report, and plot results.

    Args:
        robots_path: Path to the robots CSV file.
        destinations_path: Path to the destinations CSV file.
        packages_path: Path to the packages CSV file.
        tasks_path: Path to the tasks CSV file.
        schedules_path: Path to the schedules CSV file.
        distances_path: Path to the distances CSV file.
        report_path: Path to write the feasibility report.
        plot_file: Path to save the schedule position plot.

    Returns:
        None
    """
    # Read and validate all data from CSV files
    robots = read_robots(robots_path)
    destinations = read_destinations(destinations_path)
    packages = read_packages(packages_path)

    destination_ids = []
    for destination in destinations:
        destination_ids.append(destination["destination_id"])

    package_ids = []
    for package in packages:
        package_ids.append(package["package_id"])

    tasks = read_tasks(tasks_path, destination_ids, package_ids)

    task_ids = []
    for task in tasks:
        task_ids.append(task["task_id"])

    robot_ids = []
    for robot in robots:
        robot_ids.append(robot["robot_id"])

    schedules = read_schedules(schedules_path, robot_ids, task_ids)
    distances = read_distances(distances_path)

    # Check executability for each individual task
    results = []
    for task in tasks:
        result = is_task_executable(task, robots, destinations, packages)
        results.append(result)

    # Check feasibility for every schedule
    schedule_report = []
    for schedule in schedules:
        result = check_schedule(schedule, distances, robots, destinations, packages, tasks)
        schedule_report.append(result)

    # Write the combined report and generate the position plot
    write_feasability_report(report_path, tasks, results, schedules, schedule_report)
    plot_schedule_positions(schedules, schedule_report, plot_file)


if __name__ == "__main__":
    main(
        'robots.csv',
        'destinations.csv',
        'packages.csv',
        'tasks.csv',
        'schedules.csv',
        'distances.csv',
        'feasibility_report.txt',
        'schedule_plot.png'
    )