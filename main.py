import argparse, glob, os, shutil, sys

#Create the parser to retrieve user arguments
parser = argparse.ArgumentParser()
parser.add_argument('filename_mask', 
                     help='file name mask, ex: temp.*',
                     type=str)
parser.add_argument('source_folder', 
                     help='source folder abs path',
                     type=str)
parser.add_argument('destination_folder', 
                     help='destination folder abs path',
                     type=str)


def retrieve_files(source_folder,filename_mask='*'):
    """
    Retrieve file path names from arguments
    source_folder: source folder abs path
    filename_mask: mask filter for match files
               ex: *.csv, filename.*., /*/*.csv
    """
    all_files = []
    for root, dirs, files in os.walk(source_folder):
        files = glob.glob(os.path.join(root, filename_mask))
        for f in files :
            all_files.append(os.path.abspath(f))
    return all_files

def copy_files(file_list, destination_folder):
    """
    Copy files matched by mask inside a destination folder.
    If the destination folder doesn't exists, he are created.
    file_list: list of files to copy
    destination_folder: destination folder abs path
    """
    #create folder if not exists
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)

    for file in file_list:
        try:
            shutil.copy(file,destination_folder)
        except IOError as e:
            print('Unable to copy file {}. {}'.format(file,e))
        except:
            print('Unexpected error: {}'.format(sys.exc_info()))

def log_builder(all_files, cp_files):
    """
    A simple log builder to explain the execution of the script.
    all_files: all files inside source folder
    cp_files: all files able to be copied for the destination folder
    """
    br = '-'* 70
    nc_files = list(set(all_files) - set(cp_files))
    with open('log.txt','w') as log:
        log.write('log file: \n')
        log.write('all files: \n')
        log.write('\n'.join(all_files))
        log.write('\n'+br+'\n')
        log.write('copied files: \n')
        log.write('\n'.join(cp_files))
        log.write('\n'+br+'\n')
        log.write('not copied files: \n')
        log.write('\n'.join(nc_files))
    print('done')

if __name__ == '__main__':
    args = parser.parse_args()
    all_files = retrieve_files(args.source_folder)
    cp_files = retrieve_files(args.source_folder, args.filename_mask)
    copy_files(cp_files, args.destination_folder)
    log_builder(all_files, cp_files)
