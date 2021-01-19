import os


def input_checking():
    input_is_correct = False
    while not input_is_correct:
        try:
            val = input('y/n ')
            if val != 'y' and val != 'n':
                raise ValueError
            input_is_correct = True
        except ValueError:
            print('Invalid input, please insert again.')
    if val == 'y':
        return True
    elif val == 'n':
        return False


def get_path(counter, n_dir, output):
    # create a new directory (if it doesn't exist yet) and return path
    ROOT_DIR = os.path.abspath(os.curdir)
    path = ROOT_DIR + n_dir
    try:
        os.mkdir(path)
    except OSError:
        pass
    return os.path.join(path, output.format(counter))
