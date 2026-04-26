import numpy as np
import cv2


def gen_checkboard(patch_size):
    bright_value = np.random.randint(64, 250)
    dark_value = np.random.randint(5, 55)
    img = np.ones((patch_size, patch_size, 3), dtype=np.uint8) * bright_value
    x_range = (np.random.randint(0, patch_size//4), np.random.randint(patch_size//4*3, patch_size))
    y_range = (np.random.randint(0, patch_size//4), np.random.randint(patch_size//4*3, patch_size))
    img[y_range[0]:y_range[1]:4, x_range[0]:x_range[1]:4, :] = dark_value
    img[y_range[0]+1:y_range[1]+1:4, x_range[0]+1:x_range[1]+1:4, :] = dark_value
    img[y_range[0]+2:y_range[1]+2:4, x_range[0]+2:x_range[1]+2:4, :] = dark_value
    img[y_range[0]+3:y_range[1]+3:4, x_range[0]+3:x_range[1]+3:4, :] = dark_value
    return img

    
def write_img():
    for i in range(100):
        img_l = gen_checkboard(256)
        img_h = np.clip(img_l * 3.96, 0, 255)
        img_h = np.uint8(img_h)
        cv2.imwrite(f"res/img{i:03d}_l.png", img_l)
        cv2.imwrite(f"res/img{i:03d}_h.png", img_h)


if __name__ == "__main__":
    write_img()
    