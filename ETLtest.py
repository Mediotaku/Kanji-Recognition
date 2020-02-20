import struct
from PIL import Image
#This test is working on Python 2.7.17

#Here we read the database as indicated by the ETL
def read_record_ETL8B2(f):
    s = f.read(512)
    r = struct.unpack('>2H4s504s', s)
    i1 = Image.frombytes('1', (64, 63), r[3], 'raw')
    return r + (i1,)


#Here we get the data using read_record with the correct parameters
#categories-> classes
#writers-> examples per class
def get_ETL8B2(categories, writers):
    filename = 'ETL8B2C1'
    #Creating one kanji image, then we will create a dataset for keras with them
    new_img = Image.new('1', (64, 64))

    iter(categories)

    for id_category in categories:
        with open(filename, 'r') as f:
            f.seek((id_category * 160 + 1) * 512) #In case of ETL8B2C1 dataset
            for i in range(writers):
                r = read_record_ETL8B2(f)
                new_img.paste(r[-1], (0,0))
                #Image.eval applies a function to each pixel of the given image
                iI = Image.eval(new_img, lambda x: not x)
                #Formating id_category and i into string to create 
                #a filename for every writer from each class (avoiding overwrite)
                fn = 'ETL8B2_{:s}.png'.format(str(id_category)+str(i))
                iI.save(fn, 'PNG')

get_ETL8B2(range(0,12),5)
