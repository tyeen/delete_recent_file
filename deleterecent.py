import sys
import subprocess
from os.path import expanduser

def delete_recent_item_from_file(target_file, item):
    '''
    Delete the recent item from the list saved by the parameter file.
    '''
    file_path = expanduser('~') + '/Library/Preferences/' + target_file
    index = 0
    res = True
    while res:
        sub_cmd = 'Print RecentDocuments:CustomListItems:' + str(index) + ':Name'
        cmd = ['/usr/libexec/PlistBuddy', '-c', sub_cmd, file_path]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        res = out != ''
        if res:
            if item == out.strip():
                sub_cmd = 'Delete RecentDocuments:CustomListItems:' + str(index)
                cmd = ['/usr/libexec/PlistBuddy', '-c', sub_cmd, file_path]
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                p.communicate()

                out_msg = item.strip()
                print out_msg
                break
        index = index + 1


def delete_target(user_input):
    '''
    Delete the specified target.
    The 'target' parameter should contains two parts: target_app & target_item in the target_app.
    '''
    if not ' ' in user_input:
        return;

    inputs = user_input.split()
    if len(inputs) == 2:
        delete_recent_item_from_file(inputs[0], inputs[1])


def main():
    if len(sys.argv) >= 1 and sys.argv[1] != '':
        input_target = sys.argv[1]
        delete_target(input_target)


if __name__ == '__main__':
    main()
