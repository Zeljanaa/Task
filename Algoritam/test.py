from PIL import Image
import re
import pytesseract
from PIL import Image

def SideCropImage(img, CROP_SIZE=100):
    width, height = img.size
    img = img.crop((CROP_SIZE, CROP_SIZE, width - CROP_SIZE, height - CROP_SIZE))
    return img

def formatText(text):
    text = re.sub(r"\W+", "", text.lower())   
    text = re.sub(r"[\n\t\r]*", "", text)
    return text
    
def sliceCropper(obj):
    leftText = obj.crop((obj.size[0] * 0.285, obj.size[1] * 0.1, obj.size[0] * 0.531, obj.size[1] * 0.9))
    rightText = obj.crop((obj.size[0] * 0.665, obj.size[1] * 0.1, obj.size[0] * 0.884, obj.size[1] * 0.9))
    leftValText = pytesseract.image_to_string(leftText)
    rightValText = pytesseract.image_to_string(rightText)
    return formatText(leftValText), formatText(rightValText)


def indexsheetParser(fpath):
    with Image.open(fpath) as im:
        mappings = [
            'officesiteid',
            'agency',
            'program',
            'programyear',
            'folderid',
            'foldertab',
            'dispositiondate',
            'disposition',
            'holdtype',
            'availabledigitally',
            'activeinactive',
            'tempperm',
            'filecode',
            'casenumber',
        ]
        
        index_dict = {} 
        width = im.size[0]
        tr = (430 / 2219)
        br = (1750 / 2219)
        im1 = SideCropImage(im)
        left = 0
        right = width
        top = tr * im.size[1]
        slicecount =  14
        blockheight = br * im.size[1]
        fr = 0.38
        extend = (blockheight-top) / slicecount 
        
        im1 = im.crop((left, top, right, blockheight))
        
        # the index sheet is slightly slanted
        im1 = im1.rotate(0.2)
        
        
        for x in range(slicecount):  
            bottom = top + extend
            im1 = im.crop((left, top, right, bottom))
            top = top + extend
            
            # right
            valImg = im1.crop((width * fr , 0, width, extend))
            # crop out the left
            valImg = valImg.crop(( valImg.size[0] * 0.01, valImg.size[1] * 0.1, valImg.size[0] * 0.805, valImg.size[1] * 0.94))
            valText = pytesseract.image_to_string(valImg)
            
            text = formatText(valText)
            
            index_dict[mappings[x]] = text.strip()
    
        tr = (1862 / 2219)
        br = (1986 / 2219)
        left = 0
        right = im.size[0]
        top = tr * im.size[1]
        bottom = br * im.size[1]
        im2 = im.crop((left, top, right, bottom))
        margin = (bottom - top) / 3
        s1 = im2.crop((left, 0, right, margin))
        s2 = im2.crop((left, margin, right, margin * 2))
        s3 = im2.crop((left, margin * 2, right, margin * 3))
        
        filelocation, drawer = sliceCropper(s1)
        binder, box = sliceCropper(s2)
        room, doc = sliceCropper(s3)
        
        index_dict['drawer'] = drawer
        index_dict['binder'] = binder
        index_dict['box'] = box
        index_dict['room'] = room
        index_dict['doc'] = doc
        index_dict['filelocation'] = filelocation
        index_dict['ver'] = '' 
        return  index_dict
    
    
    
inputfile = '1.jpg'
index_dict = indexsheetParser(inputfile)
print(index_dict)