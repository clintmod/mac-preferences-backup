from os import path, listdir
from config import get_dotfiles_backup_dir, get_dotfile_excludes, get_home_dir, get_user
from utils import execute_shell, ensure_files_owned_by_user


def backup():
    print ''
    print 'Backuping up dotfiles...'
    # build file list
    home_dir = get_home_dir()
    excludes = get_dotfile_excludes()
    files = get_dot_files(home_dir, excludes)
    dest = get_dotfiles_backup_dir()
    command = ['cp', '-a', '-v'] + files + [dest]
    output = execute_shell(command)
    if output is not None:
        print output


def restore():
    print ''
    print 'Restoring dotfiles...'
    source = get_dotfiles_backup_dir()
    dest = get_home_dir()
    files = get_dot_files(source)
    command = ['sudo', 'cp', '-a', '-v'] + files + [dest]
    output = execute_shell(command)
    if output is not None:
        print output
    ensure_files_owned_by_user(get_user(), files)


def get_dot_files(home_dir, excludes=None):
    if excludes is None:
        excludes = []
    files = []
    for f in listdir(home_dir):
        full_file_path = path.join(home_dir, f)
        if path.isfile(full_file_path) and f[0] == '.' and f not in excludes:
            files.append(full_file_path)
    return files
