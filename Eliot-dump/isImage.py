#!/usr/bin/env python3

import numpy as np
import cv2 as cv


def is_mask_bouteille(self):
    img1 = cv.imread('shape_btl1.jpg', cv.IMREAD_GRAYSCALE)
    img2 = cv.imread('shape_btl2.jpg', cv.IMREAD_GRAYSCALE)
    img3 = cv.imread('shape_btl3.jpg', cv.IMREAD_GRAYSCALE)
    img4 = cv.imread('shape_btl4.jpg', cv.IMREAD_GRAYSCALE)
    assert img1 is not None, "file img1 could not be read, check with os.path.exists()"
    assert img2 is not None, "file img2 could not be read, check with os.path.exists()"
    assert img3 is not None, "file img3 could not be read, check with os.path.exists()"
    assert img4 is not None, "file img4 could not be read, check with os.path.exists()"

    ret, thresh1 = cv.threshold(img1, 127, 255,0)
    ret, thresh2 = cv.threshold(img2, 127, 255,0)
    ret, thresh3 = cv.threshold(img3, 127, 255,0)
    ret, thresh4 = cv.threshold(img4, 127, 255,0)

    msk,contours,hierarchy = cv.findContours(self.mask,2,1)
    cnt_mask = contours[0]

    im1,contours,hierarchy = cv.findContours(thresh1,2,1)
    cnt1 = contours[0]
    im2,contours,hierarchy = cv.findContours(thresh2,2,1)
    cnt2 = contours[0]
    im3,contours,hierarchy = cv.findContours(thresh3,2,1)
    cnt3 = contours[0]
    im4,contours,hierarchy = cv.findContours(thresh4,2,1)
    cnt4 = contours[0]


    ret1 = cv.matchShapes(cnt_mask,cnt1,1,0.0)
    ret2 = cv.matchShapes(cnt_mask,cnt2,1,0.0)
    ret3 = cv.matchShapes(cnt_mask,cnt3,1,0.0)
    ret4 = cv.matchShapes(cnt_mask,cnt4,1,0.0)

    if ret1 < 0.01 or ret2 < 0.01 or ret3 < 0.01 or ret4 < 0.01:
        return True
    
    return False