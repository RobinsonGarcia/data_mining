import os
import sys
import logging

def set_logger(log_path):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(stream_handler)

def scan(dir_):
    logging.info('--scanning all file extensions')
    files = {}
    for root,dirs,file_ in os.walk(dir_,topdown=False):
        for f in file_:
            files[os.path.splitext(f)[-1]]=[]

    logging.info('found %d extensions: %s'%(len(files.keys()),files.keys()))

    logging.info('quantifying number of files per extension')

    for root,dirs,file_ in os.walk(dir_,topdown=False):
        for f in file_:
            files[os.path.splitext(f)[-1]].append(os.path.join(root,f))

    for k,v in files.items():
        logging.info('file ext: %s -- total:%f '%(k,len(v)))

    return files

def write_filenames(files):
    for t in files.keys():
        logging.info('writing filenames to {}.txt'.format(t))
        f = open(t[1:]+'.txt','w')
    for i in range(len(files[t])):
        f.write(files[t][i]+'\n')
        logging.info('-- {}'.format(files[t][i]))
        f.close()

if __name__=="__main__":
    set_logger('scan.log')

    dir_ = sys.argv[1]

    files = scan(dir_)

    write_filenames(files)
