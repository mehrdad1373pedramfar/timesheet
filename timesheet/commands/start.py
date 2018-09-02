# -*- coding: utf-8 -*-
import os
import argparse

from timesheet import config
from timesheet.commands import Command
from timesheet.models import Subject, Task, DBSession
from timesheet.commands.completers import subject_completer, task_completer

__author__ = 'vahid'


class StartCommand(Command):
    name = 'start'
    description = 'Starts a task'

    @classmethod
    def add_arguments(cls):
        cls.parser.add_argument('subject', help="Subject to do something about that.").completer = subject_completer
        cls.parser.add_argument('task', nargs=argparse.REMAINDER, metavar='task', default=[], choices=[],
                                help="Task title.").completer = task_completer

    def do_job(self):
        active_task = Task.get_active_task()
        if active_task:
            print('You have an active task: %s' % active_task)
            answer = input("Do you want to terminate the currently active task ([y]/n)? ")
            if not answer or answer.lower() == 'y':
                active_task.end()
            else:
                return

        subject = Subject.ensure(self.args.subject)
        task = Task(title=' '.join(self.args.task), user = config.user if hasattr(config, 'user') else os.environ.get('USER'))
        subject.tasks.append(task)

        DBSession.commit()
        print('Started task: %s' % task)
