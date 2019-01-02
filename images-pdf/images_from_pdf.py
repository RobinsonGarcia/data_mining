import os
import sys
import logging

#--> compressing folders/files with tar: https://www.howtogeek.com/248780/how-to-compress-and-extract-files-using-the-tar-command-on-linux/

#--> basic command: tar -czvf archive.tar.gz /usr/local/something

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

#--> Compute the size of a folder in bytes
def get_size(folder='tmp_images'):
    size = 0
    files = os.listdir(folder)
    for f in files:
        size+= os.path.getsize(os.path.join(folder,f))
    return size

if __name__=='__main__':
    set_logger('pdf2imgs.log')

    txt = sys.argv[1]

    f = open(txt,'r')
    lines = f.readlines()
    f.close()

    lines = [line[:-1] for line in lines]


    for t,l in enumerate(lines):
        logging.info('--extracting images from {}'.format(l))
        os.system("pdfimages -j '"+l+"' tmp_images/image"+str(t))
        logging.info('--Extracted %d images from %d of %d reports'%(len(os.listdir('tmp_images')),t,len(lines)))

        size = get_size()
        logging.info('--total size {}Mb'.format(size/1e6))

