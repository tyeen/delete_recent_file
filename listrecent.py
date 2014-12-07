import sys
import subprocess
import alfred
from os.path import expanduser
from difflib import SequenceMatcher

SHARE_LIST_FILE_SIG = 'LSSharedFileList'

class AppItem:
    def __init__(self):
        self.app_name = ''
        self.app_plist_name = ''
        self.ratio = 0


def get_apps_holding_recent_file():
    '''
    Get the file(which is a plist file) list from ~/Library/Preferences/
    Then filter the list by whose file name containing 'LSSharedFileList'
    '''
    home_folder = expanduser('~')
    prefs_folder = home_folder + '/Library/Preferences'
    cmd = ['ls', '-A', prefs_folder]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    plist_files = out.split()

    app_items = []
    for plist in plist_files:
        if SHARE_LIST_FILE_SIG in plist:
            app_item = AppItem()
            app_item.app_plist_name = plist

            # Seperate app_name and company name from the result.
            pos = plist.find(SHARE_LIST_FILE_SIG)
            total = plist[:pos - 1]
            last_dot_pos = total.rfind('.')
            app_name = total[last_dot_pos + 1:]

            # If the first character of the app_name is not upper cased,
            # it may be not a good app_name, and we need to append company name to
            # let user know what it is.
            display_item = app_name
            if not app_name[0].isupper():
                display_item = app_name + '(' + total + ')'

            app_item.app_name = display_item

            app_items.append(app_item)

    return app_items


def show_recent_list_of_file(target_file):
    '''
    Get the recent list saved by the parameter file.
    '''
    file_path = expanduser('~') + '/Library/Preferences/' + target_file
    feedback = []

    index = 0
    res = True
    while res:
        sub_cmd = 'Print RecentDocuments:CustomListItems:' + str(index) + ':Name'
        cmd = ['/usr/libexec/PlistBuddy', '-c', sub_cmd, file_path]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        res = out != ''
        if res:
            out_arg = unicode(target_file, 'utf-8') + ' ' + unicode(out.strip(), 'utf-8')
            feedback.append(alfred.Item(
                {'arg': out_arg}, # item attribute
                unicode(out.strip(), 'utf-8'), # title
                unicode(target_file, 'utf-8') # subtitle
                )
            )
        index = index + 1
    alfred.write(alfred.xml(feedback))


def find_target_item(user_input):
    '''
    Find the target that will be deleted.
    This procedure contains two steps:
      1. Retreive an app list of apps that have recent list to let user select.
      2. After user selecting the target app, get the recent list in that app
         and let user perform the real deleting.
    '''
    app_items = get_apps_holding_recent_file()

    if not ' ' in user_input:
        # There's no space in the arguments, meaning user has not selected the target app.

        # Re-arrange the list with items that most matches user input.
        for app_item in app_items:
            if user_input != '':
                s = SequenceMatcher(None, app_item.app_name.lower(), user_input.lower())
                app_item.ratio = s.ratio()
        app_items.sort(key=lambda app_item: app_item.ratio, reverse=True)

        # Show the sorted list.
        feedback = []
        for item in app_items:
            feedback.append(alfred.Item(
                {}, # item attributes, arg, uid, etc.
                unicode(item.app_name, 'utf-8'), # title
                unicode(item.app_plist_name, 'utf-8') # subtitle
                )
            )
        alfred.write(alfred.xml(feedback))
    else:
        # User input a space, which means he/she has determined the file.
        # Time to find the recent item the user wants to delete.
        inputs = user_input.split()
        if len(inputs) <= 2:
            # Only alow to input ONE item.
            max_ratio = 0
            target = ''
            for app_item in app_items:
                s = SequenceMatcher(None, app_item.app_name.lower(), inputs[0].lower())
                r = s.ratio()
                if r > max_ratio:
                    max_ratio = r
                    target = app_item.app_plist_name

            if target != '':
                show_recent_list_of_file(target)


def main():
    input_target = ''
    if len(sys.argv) > 1 and sys.argv[1] != '':
        input_target = sys.argv[1]
    find_target_item(input_target)


if __name__ == '__main__':
    main()
