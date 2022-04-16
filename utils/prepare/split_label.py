import os
import sys

import cv2 as cv
import numpy as np
from tqdm import tqdm
sys.path.append(os.getcwd())
from utils import orderConvex, shrink_poly

DATA_FOLDER = '/home/cjy/Desktop/text-detection-ctpn/data/my_data/'
OUTPUT = '/home/cjy/Desktop/text-detection-ctpn/data/dataset/mlt/'
MAX_LEN = 1200
MIN_LEN = 600

im_fns = os.listdir(os.path.join(DATA_FOLDER, "image"))
im_fns.sort()

if not os.path.exists(os.path.join(OUTPUT, "image")):
    os.makedirs(os.path.join(OUTPUT, "image"))
if not os.path.exists(os.path.join(OUTPUT, "label")):
    os.makedirs(os.path.join(OUTPUT, "label"))

for im_fn in tqdm(im_fns):
    try:
        _, fn = os.path.split(im_fn)
        bfn, ext = os.path.splitext(fn)
        if ext.lower() not in ['.jpg', '.png']:
            continue

        gt_path = os.path.join(DATA_FOLDER, "label",bfn + '.txt')
        img_path = os.path.join(DATA_FOLDER, "image", im_fn)

        img = cv.imread(img_path)
        img_size = img.shape
        im_size_min = np.min(img_size[0:2])
        im_size_max = np.max(img_size[0:2])
        im_scale = float(600) / float(im_size_min)
        if np.round(im_scale * im_size_max) > 1200:
            im_scale = float(1200) / float(im_size_max)
        new_h = int(img_size[0] * im_scale)
        new_w = int(img_size[1] * im_scale)
        new_h = new_h if new_h // 16 == 0 else (new_h // 16 + 1) * 16
        new_w = new_w if new_w // 16 == 0 else (new_w // 16 + 1) * 16

        re_im = cv.resize(img, (new_w, new_h), interpolation=cv.INTER_LINEAR)
        re_size = re_im.shape

        polys = []
        with open(gt_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            splitted_line = line.strip().lower().split(',')
            x1, y1, x2, y2, x3, y3, x4, y4 = map(float, splitted_line[:8])
            poly = np.array([x1, y1, x2, y2, x3, y3, x4, y4]).reshape([4, 2])
            poly[:, 0] = poly[:, 0] / img_size[1] * re_size[1]
            poly[:, 1] = poly[:, 1] / img_size[0] * re_size[0]
            poly = orderConvex(poly)
            polys.append(poly)
        res_polys = []
        for poly in polys:
            if np.linalg.norm(poly[0] - poly[1]) < 10 or np.linalg.norm(poly[3] - poly[0]) < 10:
                continue
            res = shrink_poly(poly)
            res = res.reshape([-1, 4, 2])
            for r in res:
                x_min = np.min(r[:, 0])
                y_min = np.min(r[:, 1])
                x_max = np.max(r[:, 0])
                y_max = np.max(r[:, 1])
                res_polys.append([x_min, y_min, x_max, y_max])
        cv.imwrite(os.path.join(OUTPUT, "image", fn), re_im)
        with open(os.path.join(OUTPUT, "label", bfn) + ".txt", "w") as f:
            for p in res_polys:
                line = ",".join(str(p[i]) for i in range(4))
                f.writelines(line + "\r\n")
    except:
        print("Error processing {}".format(im_fn))
