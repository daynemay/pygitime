from collections import namedtuple
import os
import git
import logging
import time


PROJECT_ROOT = '.'
SECONDS_BETWEEN_CHECKS = 2
TIMESLOT_LENGTH_IN_MINUTES = 15
LAST_CHECK = 0
TIMESLOTS = []
LOG = logging.getLogger()


Work = namedtuple('Work', 'branch,file_name')


def _should_skip(dir_or_file_name):
    # TODO: maybe should be "matches .gitignore"
    return dir_or_file_name == '.git'


def _update_last_check():
    global LAST_CHECK
    LAST_CHECK = int(time.time())


def _wait_for_next_check():
    time.sleep(SECONDS_BETWEEN_CHECKS)


def _get_changes_by_recency(project_root):
    files = [os.path.join(directory, file)
             for directory, _, files in os.walk(PROJECT_ROOT)
             for file in files
             if not _should_skip(file) and not _should_skip(directory)]
    files.sort(key=os.path.getmtime, reverse=True)
    modified_times = (os.stat(file).st_mtime for file in files)
    return files, modified_times


def _set_up_timeslots():
    minutes_in_a_day = 24 * 60
    timeslot_count = int(minutes_in_a_day / TIMESLOT_LENGTH_IN_MINUTES)
    return [set() for _ in range(timeslot_count)]


def _find_timeslot(time):
    seconds = time % (24 * 60 * 60)  # TODO: handle timezone
    return int((seconds / 60) % TIMESLOT_LENGTH_IN_MINUTES)


def _assign_timeslot(branch, file, modified_time):
    work = Work(branch=branch, file=file)
    timeslot = _find_timeslot(modified_time)
    if work not in TIMESLOTS[timeslot]:
        TIMESLOTS[timeslot].add(work)
        return True


def _get_current_branch(project_root):
    repo = git.repo.Repo(project_root)
    return repo.active_branch.name


def start_tracking_time():
    global TIMESLOTS
    TIMESLOTS = _set_up_timeslots()
    _update_last_check()

    while True:
        files, modified_times = _get_changes_by_recency(PROJECT_ROOT)
        branch = _get_current_branch(PROJECT_ROOT)

        for file, modified_time in zip(files, modified_times):
            if modified_time < LAST_CHECK:
                break
            _assign_timeslot(branch, file, modified_time)

        _update_last_check()
        _wait_for_next_check()

def query_timeslots():
    print("TODO: Query timeslots here")

