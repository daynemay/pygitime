from collections import defaultdict, namedtuple
from datetime import datetime
import os
import git
import logging
import time
import pytz

# TODO: Handle timezone properly
# TODO: _should_skip should maybe reference .gitignore


PROJECT_ROOT = '.'
SECONDS_BETWEEN_CHECKS = 2
TIMESLOT_LENGTH_IN_MINUTES = 15
LAST_CHECK = 0
LOG = logging.getLogger()
WORK = set()


Work = namedtuple('Work', 'date,timeslot,branch,filename')


def _should_skip(dir_or_file_name):
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
    # TODO: Only get the modified time once here!
    files.sort(key=os.path.getmtime, reverse=True)
    modified_times = (os.stat(file).st_mtime for file in files)
    return files, modified_times


def timeslot_from_timestamp(time):
    minutes = (time % (24 * 60 * 60)) / 60  # TODO: handle timezone
    return int(minutes / TIMESLOT_LENGTH_IN_MINUTES)


def _determine_timeslot(modified_time):
    modified_date = date_from_timestamp(modified_time)
    timeslot = timeslot_from_timestamp(modified_time)
    return modified_date, timeslot


def _record_work(work_date, timeslot, branch, file):
    work = Work(date=work_date, timeslot=timeslot, branch=branch, filename=file)
    if work not in WORK:
        print('Adding', work)
        WORK.add(work)


def _get_current_branch(project_root):
    return git.repo.Repo(project_root).active_branch.name


def date_from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp, tz=pytz.utc).date()


def start_tracking_time():
    _update_last_check()

    while True:
        files, modified_times = _get_changes_by_recency(PROJECT_ROOT)
        branch = _get_current_branch(PROJECT_ROOT)

        for file, modified_time in zip(files, modified_times):
            if modified_time < LAST_CHECK:
                break
            work_date, timeslot = _determine_timeslot(modified_time)
            _record_work(work_date, timeslot, branch, file)

        _update_last_check()
        _wait_for_next_check()


def query_timeslots():
    print("TODO: Query timeslots here")


if __name__ == '__main__':
    start_tracking_time()
