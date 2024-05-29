import os
from os.path import join
import shutil
import time
from datetime import datetime
import schedule
import threading

def runContinuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

def autoTransferFiles(source, destination):
    for file in os.listdir(source):
        # check if file is not hidden
        if not file.startswith('.'):
            # get time in seconds and convert to datetime object
            modification_time = datetime.fromtimestamp(os.path.getmtime(join(source, file)))
            current_time = datetime.fromtimestamp(time.time())

            # get time difference in seconds
            delta = current_time - modification_time
            sec = delta.total_seconds()

            # get time difference in hours
            hours = sec / (60 * 60)

            # add file if new or modified in the last 24 hours
            if hours < 24:
                shutil.move(source + '/' + file, destination)
                print (file + ' was successfully transferred.')


if __name__ == "__main__":
    # run auto transfer of files in the background
    stop_run_continuously = runContinuously()

    # run job AFTER and every 24 hours since the program started
    schedule.every(24).hours.do(autoTransferFiles, source="", destination="")

    # run scheduled jobs right away when program is started regardless of the schedule
    schedule.run_all()

    # stop auto transfer of files in the background
    # stop_run_continuously.set()