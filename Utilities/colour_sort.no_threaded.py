
import os
import cv2
import numpy as np
from PIL import Image,ImageFile,ImageOps
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
from tqdm import tqdm
import pandas as pd
import hashlib
from traceback_with_variables import activate_by_import
from concurrent.futures import ThreadPoolExecutor, as_completed
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

file_path = ""
img_types = [str(f).replace('.','') for f,u in Image.registered_extensions().items()]

img_files = [file_path+f for f 
             in os.listdir(file_path[:-1:]) 
             if os.path.isfile(file_path+f) 
             and f[-(f[::-1].find('.')):]
             in [str(f).replace('.','') for f,u 
             in Image.registered_extensions().items()]]

def main(img_files, i_f):
        img_list = []
        img_list.clear()
        img = cv2.imread(img_files[i_f])
        im_success, img_buf = cv2.imencode(str('.'+img_files[i_f][-(img_files[i_f][::-1].find('.')):]),img)
        md5_calc = str(hashlib.md5(img_buf).hexdigest())
        w,h = (32,32)
        pil_arr = cv2.cvtColor(np.array(cv2.blur(img,(40,40))), cv2.COLOR_BGR2RGB)
        img_thumb = ImageOps.contain(Image.fromarray(pil_arr),(w,h))
        img_conv = img_thumb.convert(mode="P",palette=Image.ADAPTIVE,colors=16).convert(mode="RGB")
        img_arr = np.array(img_conv).astype('uint8')
        h, w, c = img_arr.shape
        arr_list = [str(('{:02X}' * 3).format(r,g,b)) for r,g,b in img_arr.reshape(-1,3)]
        pix_list = np.array(arr_list).reshape(h,w).tolist()
        pixel_lines = []
        px = [pixel_lines.append(" ".join(str(y) for y in [x for x in pix_list]))]
        for i, line in enumerate(pixel_lines):
            pixel_lines[i] = " ".join([x for x in word_tokenize(line)])
        vectorizer = CountVectorizer(ngram_range = (4,4))
        X1 = vectorizer.fit_transform(pixel_lines) 
        features = (vectorizer.get_feature_names_out())
        vectorizer = TfidfVectorizer(ngram_range = (4,4))
        X2 = vectorizer.fit_transform(pixel_lines)
        sums = X2.sum(axis = 0)
        data1 = []
        for col, term in enumerate(features):
            data1.append( (term, sums[0,col] ))
        ranking = pd.DataFrame(data1, columns = ['term','rank'])z
        words = (ranking.sort_values('rank', ascending = False))
        f_head = [x for x in list(words.iloc[0:10,0])]
        f_name = ''.join(str(x).split(' ')[0] for x in np.unique(np.array(f_head)).tolist())
        os.rename(img_files[i_f],file_path+f_name+md5_calc+str(i_f).zfill(4)+'.'+img_files[i_f][-(img_files[i_f][::-1].find('.')):])

fl_len = len(img_files)
status_bar = tqdm(total=fl_len, desc='Images')
with ThreadPoolExecutor(8) as executor:
    futures = [executor.submit(main, img_files, i_f) for i_f in range(0,len(img_files)-1)]
    for _ in as_completed(futures):
        status_bar.update(n=1) 
