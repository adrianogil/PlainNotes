import sublime, sublime_plugin

import datetime

import os

class CreateDailyNoteCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        note_title = datetime.datetime.now().strftime("%Y.%m.%d") + '.note'
        daily_path = "/Notes/Reports/"
        note_path = os.environ['HOME'] + daily_path + note_title

        if not os.path.isfile(note_path):
            last_day_note = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y.%m.%d") + '.note'
            note_path = os.environ['HOME'] + daily_path + last_day_note
            print("CreateDailyNoteCommand - last day: " + str(last_day_note))

            with open(note_path, 'r', encoding='utf-8') as f:
                last_day_notes_lines = f.readlines()

            todo_start_line = -1

            new_content = ""

            for i in range(0, len(last_day_notes_lines)):
                l = last_day_notes_lines[i]
                if 'ToDo:' in l:
                    todo_start_line = i
                    new_content = l
                elif todo_start_line != -1:
                    if l[0] != '_':
                        new_content = new_content + l

            with open(note_path, 'w') as f:
                for i in range(0, len(last_day_notes_lines)):
                    l = last_day_notes_lines[i]
                    if 'ToDo:' in l:
                        todo_start_line = -1
                    elif todo_start_line == -1:
                        if l[0] == '_':
                            f.write(l)
                    else:
                        f.write(l)

            sublime.set_clipboard(new_content)

        note_path = os.environ['HOME'] + daily_path + note_title
        print("CreateDailyNoteCommand  " + str(note_path))
        new_view = self.view.window().open_file(note_path)