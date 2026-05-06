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

def check_schedule(schedule: dict, distances: list[list[float]], robots: list[dict],
                   destinations: list[dict], packages: list[dict],
                   tasks: list[dict]) -> list[tuple] | None:
    """Simulate a schedule and determine whether it is feasible.

    A schedule is feasible if the robot can complete all tasks and return
    to the origin without its battery dropping below 0% at any point.

    The route follows: origin -> source1 -> target1 -> source2 -> target2 -> ... -> origin.
    Travel to a source is unloaded; travel to a target carries the package.

    Args:
        schedule: A schedule dictionary with robot_id and task_ids.
        distances: 2D distance matrix where index 0 is the origin and index i is destination D_i.
        robots: List of valid robot record dictionaries.
        destinations: List of valid destination record dictionaries.
        packages: List of valid package record dictionaries.
        tasks: List of valid task record dictionaries.

    Returns:
        None if the schedule is infeasible, otherwise a list of tuples
        (time_elapsed_hours, total_distance_km, distance_from_origin_km, battery_pct)
        with one entry for the origin and one entry after each leg of travel.
    """
    robot_id = schedule['robot_id']
    task_ids_in_schedule = schedule['task_ids']

    # Look up the assigned robot
    robot = next((r for r in robots if r['robot_id'] == robot_id), None)
    if robot is None:
        return None

    robot_zone = robot['zone']
    battery = float(robot['battery_level'])

    # Build lookup dictionaries for fast access by ID
    dest_by_id = {d['destination_id']: d for d in destinations}
    pkg_by_id = {p['package_id']: p for p in packages}
    task_by_id = {t['task_id']: t for t in tasks}

    # Map destination IDs to their matrix index (index 0 is reserved for the origin)
    dest_index = {d['destination_id']: i + 1 for i, d in enumerate(destinations)}

    # Validate all destinations are in the same zone as the robot
    for tid in task_ids_in_schedule:
        task = task_by_id.get(tid)
        if task is None:
            return None

        src = dest_by_id.get(task['source_id'])
        tgt = dest_by_id.get(task['target_id'])
        if src is None or tgt is None:
            return None

        if src['zone'] != robot_zone or tgt['zone'] != robot_zone:
            return None

    # Validate the robot can carry every package in the schedule
    for tid in task_ids_in_schedule:
        task = task_by_id[tid]
        pkg = pkg_by_id.get(task['package_id'])
        if pkg is None:
            return None
        if robot['max_load'] < pkg['weight']:
            return None

    # Record the starting state at the origin before any travel
    data_points = [(0.0, 0.0, 0.0, battery)]

    current_idx = 0
    total_time = 0.0
    total_dist = 0.0

    for tid in task_ids_in_schedule:
        task = task_by_id[tid]
        src_idx = dest_index[task['source_id']]
        tgt_idx = dest_index[task['target_id']]
        pkg_weight = pkg_by_id[task['package_id']]['weight']

        # Leg 1: travel unloaded from current position to the source
        d1 = distances[current_idx][src_idx]
        battery -= d1 * 1.0
        total_time += d1 / 15.0
        total_dist += d1
        data_points.append((total_time, total_dist, distances[0][src_idx], battery))

        if battery < 0:
            return None

        # Leg 2: travel loaded from source to target
        d2 = distances[src_idx][tgt_idx]
        battery -= d2 * (1.0 + 0.5 * pkg_weight)
        total_time += d2 / 15.0
        total_dist += d2
        data_points.append((total_time, total_dist, distances[0][tgt_idx], battery))

        if battery < 0:
            return None

        current_idx = tgt_idx

    # Return to origin unloaded after all tasks are complete
    d_return = distances[current_idx][0]
    battery -= d_return * 1.0
    total_time += d_return / 15.0
    total_dist += d_return
    data_points.append((total_time, total_dist, 0.0, battery))

    if battery < 0:
        return None

    return data_points