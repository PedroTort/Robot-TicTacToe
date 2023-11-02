import cv2
import numpy as np

def process(img):
     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
     img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
     img_canny = cv2.Canny(img_blur, 0, 100)
     kernel = np.ones((2, 2))
     img_dilate = cv2.dilate(img_canny, kernel, iterations=8)
     return cv2.erode(img_dilate, kernel, iterations=2)

def convex_hull(cnt):
     peri = cv2.arcLength(cnt, True)
     approx = cv2.approxPolyDP(cnt, peri * 0.02, True)
     return cv2.convexHull(approx).squeeze()

def centers(inner, outer):
     c = inner[..., 0].argsort()
     top_lef2, top_rit2 = sorted(inner[c][:2], key=list)
     bot_lef2, bot_rit2 = sorted(inner[c][-2:], key=list)
     c1 = outer[..., 0].argsort()
     c2 = outer[..., 1].argsort()
     top_lef, top_rit = sorted(outer[c1][:2], key=list)
     bot_lef, bot_rit = sorted(outer[c1][-2:], key=list)
     lef_top, lef_bot = sorted(outer[c2][:2], key=list)
     rit_top, rit_bot = sorted(outer[c2][-2:], key=list)
     yield inner.mean(0)
     yield np.mean([top_lef, top_rit, top_lef2, top_rit2], 0)
     yield np.mean([bot_lef, bot_rit, bot_lef2, bot_rit2], 0)
     yield np.mean([lef_top, lef_bot, top_lef2, bot_lef2], 0)
     yield np.mean([rit_top, rit_bot, top_rit2, bot_rit2], 0)
     yield np.mean([top_lef, lef_top], 0)
     yield np.mean([bot_lef, lef_bot], 0)
     yield np.mean([top_rit, rit_top], 0)
     yield np.mean([bot_rit, rit_bot], 0)
    
img = cv2.imread("gabarito.png")
contours, _ = cv2.findContours(process(img), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
# cv2.imshow("cout", contours) 
# cv2.imwrite("counters.png", contours) 
inner, outer = sorted(map(convex_hull, contours), key=len)



for x, y in centers(inner, outer):
    print(f"X: {x}; X: {y}")
    cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
# cv2.imshow("result", img)
# cv2.waitKey(0)