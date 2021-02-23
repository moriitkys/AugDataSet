# --- Tools and parameters ---
import os
import sys
import numpy as np
import cv2
import glob
import random
import matplotlib.pyplot as plt
import shutil
from distutils import dir_util
import itertools
import tkinter
from tkinter import messagebox


class AugDataSet():
    '''
    This class generates augmented dataset especially for Deep Lerning
    Usage:
    import mylib.augdataset_rgb as augdataset
    aug_dataset = augdataset.AugDataSet(flags_aug_type = flags_aug_type,
                                        aug_scale_factor = aug_scale_factor,
                                        gc_ratio = gc_ratio,
                                        img_size = config_param.img_size,
                                        control_warning_datasize = config_param.control_warning_datasize)
    for path_selected_folder in list_selected_folders:
        aug_dataset.do_augmentation(path_selected_folder = path_selected_folder,
                                    dataset_type = dataset_type)
    '''

    def __init__(self, flags_aug_type={},
                 aug_scale_factor=1,
                 gc_ratio=0.5,
                 img_size=[224, 224],
                 control_warning_datasize=True):  # [img_width, img_hight]
        self.dataset_category = ""
        self.do_reverse = flags_aug_type["rv"]
        self.do_gamma_correction = flags_aug_type["gc"]
        self.do_add_noise = flags_aug_type["pn"]
        self.do_cut_out = flags_aug_type["co"]
        self.do_deformation = flags_aug_type["df"]
        # self.aug_scale_factor is the inflation scale factor for deformation.(1~100)
        self.aug_scale_factor = aug_scale_factor
        # self.gc_ratio is the gamma correction ratio (The bigger, the more bright images are.)
        self.gc_ratio = gc_ratio
        self.img_size = img_size
        self.save_rgb2gray = False
        self.class_folder = "1"
        self.control_warning_datasize = control_warning_datasize

        # self.aug_whole_factor is used for how large augmented data size is
        # If you change augmentation process, change how to count (under)
        self.aug_whole_factor = 1
        for flag in flags_aug_type:
            if flags_aug_type[flag]:
                if flag == "df":
                    self.aug_whole_factor = self.aug_whole_factor * \
                        (self.aug_scale_factor+1)
                else:
                    self.aug_whole_factor = self.aug_whole_factor * 2

        pathc = os.getcwd()
        self.pathc = pathc.replace("\\", '/')
        self.pathc = self.pathc.replace("/mylib", "")
        # print(self.pathc)

        self.img_input_folder = pathc + '/dataset/'+self.class_folder
        self.img_output_folder = '/dataset_aug'

        self.imgs = glob.glob(self.img_input_folder + '/*')
        self.imgs_dir_lists = []
        self.dataset_type = {}

        self.n = 0

        self.f = None

    def horizontalFlip(self, img):
        img = img[:, ::-1, :]
        return img

    def gammaCorrection(self, img_pair, specific_process_targets):
        img_pair_out = []
        img = img_pair[0]
        rows, cols, ch = img.shape
        for i, key in enumerate(self.dataset_type):
            if key in specific_process_targets:
                image = img_pair[i]
                # self.gc_ratio is the gamma correction ratio (The bigger, the more bright images are.)
                if np.random.uniform(0, 10) < int(self.gc_ratio*10):
                    imggc = image*1.3
                else:
                    imggc = image*0.7
                img_pair_out.append(imggc)
            else:
                imggc = img_pair[i]
                img_pair_out.append(imggc)
        return img_pair_out

    def addNoise(self, img_pair, specific_process_targets):
        img_pair_out = []
        img = img_pair[0]
        rows, cols, ch = img.shape
        # white noise
        pts_x_white = np.random.randint(0, cols-1, int(rows/10))
        pts_y_white = np.random.randint(0, rows-1, int(rows/10))

        # black noise
        pts_x_black = np.random.randint(0, cols-1, int(rows/10))
        pts_y_black = np.random.randint(0, rows-1, int(rows/10))

        for i, key in enumerate(self.dataset_type):
            if key in specific_process_targets:
                imgpn = img_pair[i]
                imgpn = cv2.cvtColor(imgpn, cv2.COLOR_BGR2RGB)
                imgpn[(pts_y_white, pts_x_white)] = (255, 255, 255)
                imgpn[(pts_y_black, pts_x_black)] = (0, 0, 0)
                imgpn = cv2.cvtColor(imgpn, cv2.COLOR_RGB2BGR)
            else:
                imgpn = img_pair[i]
            img_pair_out.append(imgpn)
        return img_pair_out

    def cutOut(self, img_pair, specific_process_targets):
        img_pair_out = []
        img = img_pair[0]  # Image sizes are all assumed to be the same
        # rows is height, cols is width
        rows, cols, ch = img.shape
        # In python3, these should be int()
        rn1 = random.randint(0, int(cols))
        rn2 = random.randint(0, int(rows))
        w = random.randint(0, int(cols/4))
        h = random.randint(0, int(rows/4))
        for i, key in enumerate(self.dataset_type):
            if key in specific_process_targets:
                c_val = np.random.randint(0, 255)
                imgco = img_pair[i]
                cv2.rectangle(imgco, (rn1, rn2), (rn1 + w, rn2 + h),
                              (c_val, c_val, c_val), -1)
            else:
                c_val = 0
                imgco = img_pair[i]
                cv2.rectangle(imgco, (rn1, rn2), (rn1 + w, rn2 + h),
                              (c_val, c_val, c_val), -1)
            img_pair_out.append(imgco)
        # self.imgSave(imgco)
        return img_pair_out

    def homographyTrans(self, img_pair):
        img_pair_out = []
        img = img_pair[0]  # Image sizes are all assumed to be the same
        # rows is height, cols is width
        rows, cols, ch = img.shape
        # In python3, these should be int()
        rn1 = random.randint(0, int(cols/10))
        rn2 = random.randint(0, int(cols/10))
        rn3 = random.randint(int(cols*9/10), cols)
        rn4 = random.randint(int(cols*9/10), cols)
        rn5 = random.randint(0, int(rows/10))
        rn6 = random.randint(0, int(rows/10))
        rn7 = random.randint(int(rows*9/10), rows)
        rn8 = random.randint(int(rows*9/10), rows)
        for i, key in enumerate(self.dataset_type):
            pts1 = np.float32([[rn1, rn5], [rn3, rn6], [rn2, rn7], [rn4, rn8]])
            pts2 = np.float32([[0, 0], [cols, 0], [0, rows], [cols, rows]])

            M = cv2.getPerspectiveTransform(pts1, pts2)
            dst = cv2.warpPerspective(img_pair[i], M, (cols, rows))
            img_pair_out.append(dst)

        # self.imgSave(dst)
        return img_pair_out

    def loadImage(self, dir_input):
        self.imgs_dir_lists = []
        for key in self.dataset_type:
            self.imgs_dir_lists.append(sorted(glob.glob(dir_input + '/*' +
                                                        self.dataset_type[key])))
        # Check for the number of image pairs
        # print(self.imgs_dir_lists)
        if len(self.imgs_dir_lists) > 1:
            imgs_pairs = list(itertools.combinations(self.imgs_dir_lists, 2))
            # print(imgs_pairs)
            for imgs_pair in imgs_pairs:
                # print(imgs_pair)
                if len(imgs_pair[0]) != len(imgs_pair[1]):
                    messagebox.showerror(
                        'Error エラー', 'Some images are not paired.')

    def saveImage(self, img_pair, dir_input, dir_output):
        '''
        saveImage must be called after loadImage.
        Because self.imgs_c (and etc) must be update
        '''
        self.n += 1

        for i, key in enumerate(self.dataset_type):
            filename = dir_output + "/img_" + \
                str(self.n).zfill(5) + self.dataset_type[key]
            size = (self.img_size[1], self.img_size[0])
            img = img_pair[i].copy()
            cv2.resize(img, size)
            cv2.imwrite(filename, img)
        self.f.write(dir_output + "/img_" +
                     str(self.n).zfill(5) + self.dataset_type["rgb"]+'\n')

        # cv2.imwrite(filename1, img_c)
        # cv2.imwrite(filename2, cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY))
        # cv2.imwrite(filename3, d)
        # cv2.imwrite(filename4, t)
        # if self.save_rgb2gray == True:
        #    cv2.imwrite(filename5, cv2.cvtColor(
        #        img.astype('uint8'), cv2.COLOR_RGB2GRAY))

    def do_augmentation(self, path_selected_folder, dataset_type):
        '''
        Input: dataset_folder_name(images), dataset_type(dictionary)
        Output: augmented images, name list of images(rgb only) for mask-rcnn

        Program Flow
        1, Load images in an input dir
        2, Save images into an output dir
        3, Load saved images in the output dit and augmentations, 
           then save augmented images into the output dir and save the path name into list.txt
        4, Repeat flow 3 (reverse, gammma correction, )

        points
        - images of the pair must be named (must be checked)
        - What the dataset type is (rgb, rgb-mask, rgbd, ...)
        - Images must be loaded from the saved directory after an extension
        '''
        print("Now executing augmentation :" + path_selected_folder)
        self.n = 0
        self.dataset_type = dataset_type

        list_source_imgs = os.listdir(
            path_selected_folder)

        # Check Dataset Volume
        volume = 0
        for img in list_source_imgs:
            for key in self.dataset_type:
                if self.dataset_type[key] in img:
                    volume += 1
        print("The number of data after augmentation is ",
              int(volume*self.aug_whole_factor))
        if volume*self.aug_whole_factor > 5000 and self.control_warning_datasize:
            tki_volume_confirm = tkinter.Tk()
            # tki_volume_confirm.withdraw()
            # The number of expanded data exceeds 5000.
            # Is the capacity of the PC sufficient? (Do you want to continue the expansion?)
            ret_volume_confirm = messagebox.askyesno(
                '確認', '拡張後データ数が5000を超えます。PCの容量は十分ですか？（拡張を続行しますか？）')
            if ret_volume_confirm:
                tki_volume_confirm.destroy()
            else:
                tki_volume_confirm.destroy()
                print("exit this program")
                sys.exit()
            # tki_volume_confirm.mainloop()

        dir_input = path_selected_folder
        dir_output = path_selected_folder + "_aug"
        if os.path.exists(dir_output):
            tki_folder_confirm = tkinter.Tk()
            tki_folder_confirm.withdraw()
            ret_folder_confirm = messagebox.askyesno(
                '確認', '_augフォルダがあります。_augフォルダ内を消去してよろしいですか？')
            if ret_folder_confirm:
                if os.path.exists(dir_output):
                    shutil.rmtree(dir_output)
                # make_dataset.do_augmentation(dataset_folder_name = "dataset")
                os.makedirs(dir_output)
                tki_folder_confirm.destroy()
            else:
                tki_folder_confirm.destroy()
            # tki3.mainloop()
        else:
            os.makedirs(dir_output)

        self.f = open(dir_output + '/list.txt', 'w')

        # --- Save loaded images (Always run regardless of flags) ---
        dir_input = path_selected_folder
        dir_output = path_selected_folder + "_aug"

        self.loadImage(dir_input)  # Update self.imgs_dir_lists

        for cnt in range(len(self.imgs_dir_lists[0])):
            img_pair = []
            for i in range(len(self.imgs_dir_lists)):
                image = cv2.imread(self.imgs_dir_lists[i][cnt])
                img_pair.append(image)
            self.saveImage(img_pair, dir_input, dir_output)

        # --- Save reversed images ---
        if self.do_reverse == True:
            dir_input = path_selected_folder + "_aug"  # NOT object_class_number_path
            dir_output = path_selected_folder + "_aug"

            self.loadImage(dir_input)  # Update self.imgs_dir_lists

            for cnt in range(len(self.imgs_dir_lists[0])):
                img_pair = []
                for i in range(len(self.imgs_dir_lists)):
                    image = cv2.imread(self.imgs_dir_lists[i][cnt])
                    image_rev = self.horizontalFlip(image)
                    img_pair.append(image_rev)
                self.saveImage(img_pair, dir_input, dir_output)

        # --- Save gamma corrected images ---
        if self.do_gamma_correction == True and 'rgb' in self.dataset_type:
            dir_input = path_selected_folder + "_aug"  # NOT object_class_number_path
            dir_output = path_selected_folder + "_aug"

            self.loadImage(dir_input)  # Update self.imgs_dir_lists

            for cnt in range(len(self.imgs_dir_lists[0])):
                img_pair = []
                specific_process_targets = ["rgb", "d", "t"]
                for i, key in enumerate(self.dataset_type):
                    image = cv2.imread(self.imgs_dir_lists[i][cnt])
                    img_pair.append(image)
                img_pair_out = self.gammaCorrection(
                    img_pair, specific_process_targets)
                self.saveImage(img_pair_out, dir_input, dir_output)

        # --- Save noised images ---
        if self.do_add_noise == True:
            dir_input = path_selected_folder + "_aug"  # NOT object_class_number_path
            dir_output = path_selected_folder + "_aug"

            self.loadImage(dir_input)  # Update self.imgs_dir_lists

            for cnt in range(len(self.imgs_dir_lists[0])):
                img_pair = []
                specific_process_targets = ["rgb", "d", "t"]
                for i, key in enumerate(self.dataset_type):
                    image = cv2.imread(self.imgs_dir_lists[i][cnt])
                    img_pair.append(image)
                img_pair_out = self.addNoise(
                    img_pair, specific_process_targets)
                self.saveImage(img_pair_out, dir_input, dir_output)

        # --- Save cut-out images ---
        if self.do_cut_out == True:
            dir_input = path_selected_folder + "_aug"  # NOT object_class_number_path
            dir_output = path_selected_folder + "_aug"

            self.loadImage(dir_input)  # Update self.imgs_dir_lists

            for cnt in range(len(self.imgs_dir_lists[0])):
                img_pair = []
                specific_process_targets = ["rgb"]
                for i, key in enumerate(self.dataset_type):
                    image = cv2.imread(self.imgs_dir_lists[i][cnt])
                    img_pair.append(image)
                img_pair_out = self.cutOut(
                    img_pair, specific_process_targets)
                self.saveImage(img_pair_out, dir_input, dir_output)

        # --- Save deformed images ---
        if self.do_deformation == True:
            dir_input = path_selected_folder + "_aug"  # NOT object_class_number_path
            dir_output = path_selected_folder + "_aug"

            self.loadImage(dir_input)  # Update self.imgs_dir_lists

            for cnt in range(len(self.imgs_dir_lists[0])):
                img_pair = []
                for i, key in enumerate(self.dataset_type):
                    image = cv2.imread(self.imgs_dir_lists[i][cnt])
                    img_pair.append(image)
                for _ in range(int(self.aug_scale_factor)):
                    img_pair_out = self.homographyTrans(img_pair)
                    self.saveImage(img_pair_out, dir_input, dir_output)

            # self.f.close()
