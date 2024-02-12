import cv2
import os

in_dir = os.path.join(os.getcwd(), '..', 'images')
out_dir = os.path.join(os.getcwd(), '..', 'png')
img_ext = ['.png', '.jpg', '.jpeg', '.bmp', '.webp']

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for filename in os.listdir(in_dir):
    img_in_path = os.path.join(in_dir, filename)

    if os.path.isfile(img_in_path) and filename.lower().endswith(tuple(img_ext)):
        new_filename = f'{os.path.splitext(filename)[0]}.png'
        img_out_path = os.path.join(out_dir, new_filename)

        if not os.path.exists(img_out_path):
            img = cv2.imread(img_in_path)
            cv2.imwrite(img_out_path, img)
            print(f'CONVERTED - {filename} to {new_filename} in {out_dir}')
        else:
            print(f'SKIPPING - {filename} already exists at {out_dir}')
