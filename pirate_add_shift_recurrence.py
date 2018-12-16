#!/usr/bin/python

import sys
import os
from tasklib import TaskWarrior

time_attributes = ('wait', 'scheduled', 'until')

def is_new_local_recurrence_child_task(task):
    # Do not affect tasks not spun by recurrence
    if not task['parent']:
        return False

    # Newly created recurrence tasks actually have
    # modified field copied from the parent, thus
    # older than entry field (until their ID is generated)
    if (task['modified'] - task['entry']).total_seconds() < 0:
        return True

tw = TaskWarrior(data_location=os.path.dirname(os.path.dirname(sys.argv[0])))
tw.overrides.update(dict(recurrence="no", hooks="no"))

def hook_shift_recurrence(task):
    if is_new_local_recurrence_child_task(task):
        parent = tw.tasks.get(uuid=task['parent']['uuid'])
        parent_due_shift = task['due'] - parent['due']
        for attr in time_attributes:
            if parent[attr]:
                task[attr] = parent[attr] + parent_due_shift
