import sys
import numpy as np
import cv2

def find_screen_quad(gray):
    """Find the bright phone-screen rectangle in the photo."""
    h, w = gray.shape
    # The screen is the large bright region; use adaptive threshold to find its border
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # threshold: screen is bright, surrounding darker
    _, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # take largest connected component of bright
    num, labels, stats, cents = cv2.connectedComponentsWithStats(th, 8)
    if num < 2:
        return None
    areas = stats[1:, cv2.CC_STAT_AREA]
    idx = np.argmax(areas) + 1
    if stats[idx, cv2.CC_STAT_AREA] < h * w * 0.2:
        return None
    x, y, cw, ch = stats[idx, cv2.CC_STAT_LEFT], stats[idx, cv2.CC_STAT_TOP], stats[idx, cv2.CC_STAT_WIDTH], stats[idx, cv2.CC_STAT_HEIGHT]
    return x, y, cw, ch

def warp_screen(img, gray):
    """Crop to the screen quad and return warped rect."""
    quad = find_screen_quad(gray)
    if quad is None:
        return None
    x, y, cw, ch = quad
    # expand slightly
    x = max(0, x - 2); y = max(0, y - 2)
    cw = min(img.shape[1] - x, cw + 4); ch = min(img.shape[0] - y, ch + 4)
    crop = img[y:y + ch, x:x + cw]
    return crop

if __name__ == '__main__':
    path = sys.argv[1]
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    q = find_screen_quad(gray)
    print('quad:', q)
    if q:
        x, y, cw, ch = q
        print('frac:', round(cw * ch / (img.shape[0] * img.shape[1]), 3))
        crop = img[y:y + ch, x:x + cw]
        cv2.imwrite(sys.argv[2], crop)
        print('saved', sys.argv[2], crop.shape[::-1])
