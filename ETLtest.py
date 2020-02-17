import struct
from PIL import Image
#Here we read the database as indicated by the ETL
def read_record_ETL8B2(f):
    s = f.read(512)
    r = struct.unpack('>2H4s504s', s)
    i1 = Image.frombytes('1', (64, 63), r[3], 'raw')
    return r + (i1,)



filename = 'ETL8B2C1'
id_category = -1
new_img = Image.new('1', (64*16, 64*10))

with open(filename, 'r') as f:
    
    for i in range(160):
        id_category=id_category+1
        f.seek((id_category * 160 + 1) * 512)
        r = read_record_ETL8B2(f)
        new_img.paste(r[-1], (64*(i%16), 64*(i/16)))

iI = Image.eval(new_img, lambda x: not x)
fn = 'ETL8B2_{:03d}.png'.format(id_category)
iI.save(fn, 'PNG')