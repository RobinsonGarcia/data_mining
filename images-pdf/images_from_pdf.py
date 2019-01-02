#### Extract images from pdf files using pdfimages (linux)

# This script takes a list of pdf files and extracts all images within each file to a folder specified by the user. It also gives the option to compact the output folder and remove it after it has been compated.

#--> compressing folders/files with tar: https://www.howtogeek.com/248780/how-to-compress-and-extract-files-using-the-tar-command-on-linux/
#--> basic command: tar -czvf archive.tar.gz /usr/local/something

import os
import sys
import logging
import argparse 
import shutil

#HELPER FUNCTIONS 
#--> set a logger to keep track of all relevant activities
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

#--> Parse arguments
def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p','--paths_txt',help='Set the path a txt file containing paths to pdf files')
    parser.add_argument('-o','--output_folder',help='Set the path to output folder (location where all images will be saved at)')
    parser.add_argument('-z','--tar_files',help='choose "y" to create compacted.tar.z',default='y')
    parser.add_argument('-d','--delete',help='choose "y" to DELETE all extracted images and keep only the compacted file',default='y')

    args = vars(parser.parse_args())

    #-->Parse arguments
    txt = args['paths_txt']
    save_to = args['output_folder']

    if os.path.exists(save_to):
        print('--cant create an output folder: folder already exists')
        sys.exit()
    else:
        os.system('mkdir '+save_to)
        print('--created new folder {}'.format(save_to))

    zip_ = args['tar_files'] 
    remove = args['delete']
    return txt,save_to,zip_,remove

#-->Read file txt containing paths to pdf files:
def read_lines(txt):
    #-->Read file txt containing paths to pdf files:
    f = open(txt,'r')
    lines = f.readlines()
    f.close()

    #-->Remove '\n' 
    lines = [line[:-1] for line in lines]
    return lines

#EXTRACT IMAGES
#-->Extract images from pdf gien a list of paths to pdf's
def imgs_from_pdf(lines,save_to):
    #--> Extract images from pdf
    for t,l in enumerate(lines):
        logging.info('--extracting images from {}'.format(l))
        os.system("pdfimages -j '"+l+"' "+save_to+"/image"+str(t))
        logging.info('--Extracted %d images from %d of %d reports'%(len(os.listdir(save_to)),t,len(lines)))

        #--> computes the size of the output folder in Gb 
        size = get_size(save_to)
        logging.info('--total size {}Gb'.format(size))
    return size



#--> split files into jpg and others (interested only on jpg's)
def split_jpg_others(save_to):
    imgs = os.listdir(save_to)
    os.system('mkdir '+save_to+'/jpg')
    os.system('mkdir '+save_to+'/others')
    dic = {'jpg':[],'others':[]}
    tot = len(imgs)
    count = 0
    for img in imgs:

        if img[-3:]=='jpg':
            dic['jpg'].append(os.path.join(save_to,'jpg',img))
            shutil.move(os.path.join(save_to,img),os.path.join(save_to,'jpg'))

        else:
            dic['others'].append(os.path.join(save_to,'others',img))
            shutil.move(os.path.join(save_to,img),os.path.join(save_to,'others'))
        count+=1

    logging.info("--found %d jpg's and %d others"%(len(dic['jpg']),len(dic['others'])))
    return dic



#--> Create a file filenames_jpg.txt and filenames_others.txt that stores the path to each image and return the total number of images created
def create_filenames(save_to,dic):
    logging.info('--creating filename_jpg.txt and creating filename_others.txt')

    for k in dic.keys():
        filenames = dic[k]
        f = open(save_to+'/filenames_'+k+'.txt','w')
        for path in filenames:
            f.write(path+'\n')
            f.close()
            logging.info('--'+save_to+'/filenames_'+k+'.txt successifuly created!')

    n_images = (len(dic['jpg']),len(dic['others']))

    return n_images

#--> Compact images and save to a file named compacted.tar.gz:
def compact(src,zip_,remove):

    if not zip_: zip_ = input("--would you like to compact the output_folder? (y/n): ")
    if not remove: remove = input("--would you like to keep only the compacted file and DELETE the output folder? (y/n): ") 

    if zip_=='y':
        logging.info('--starting tar -czf')
    if remove=='n':
        os.system('tar -czf compacted.tar.gz '+src)
        compacted_size = os.path.getsize('compacted.tar.gz')
        logging.info('--image files saved at %s and %s'%('compacted.tar.gz',src))
    if remove=='y':
        os.system('tar -czf compacted.tar.gz '+src+' && rm -rf '+src)
        compacted_size = os.path.getsize('compacted.tar.gz')
        logging.info('--image files saved at %s and folder %s successifully deleted'%('compacted.tar.gz',src))
    else:
        logging.error("unkown option!")

    elif zip_=='n':
        logging.info('--compacted.tar.gz not created')

    if compacted_size:
        return compacted_size/1e9
    else: 
        return None

#--> Compute the size of a folder in bytes
def get_size(folder='tmp_images'):
    size = 0
    files = os.listdir(folder)
    for f in files:
        size+= os.path.getsize(os.path.join(folder,f))
    return size/1e9



if __name__=='__main__':

    #-->Parse input arguments 
    txt,save_to,zip_,remove = parse_args()

    #-->set a logger
    set_logger(save_to+'/pdf2imgs.log')

    #-->Read file txt containing paths to pdf files:
    logging.info('--Reading file {}'.format(txt))
    lines = read_lines(txt)

    #--> Extract imgs and save them to save_to
    logging.info('--Starting to extract images')
    size = imgs_from_pdf(lines,save_to)

    #--> split files into jpg and others (interested only on jpg's)
    logging.info('Starting to split files into jpg and others')
    dic = split_jpg_others(save_to) 

    #--> Create a files filenames_jpg.txt and filenames_others.txt 
    logging.info('--Creating filenames txt (jpg/others)')
    n_images = create_filenames(save_to,dic) 

    #--> Compact all jpg files from save_to/jpg to a file compacted_jpg.tar.gx
    compacted_size = compact(save_to,zip_,remove)

    #--> Summary
    logging.info('--Concluded extracting images from {}'.format(txt))
    logging.info('--A total of %d files (jpg and others) were extracted'%(n_images[0]+n_images[1]))
    logging.info('--A total of %d jpg images were extracted and saved'%(n_images[0]))
    logging.info('--A total of %d jpg others were extracted and saved'%(n_images[1]))

    if compacted_size!=None:
        logging.info('--Output folder size: %d Gb --compacted.tar.gz size: %d Gb'%(size,compacted_size))

    else:
        logging.info('--Output folder size: %d Gb'%(size))

