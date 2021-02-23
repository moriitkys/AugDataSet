class ConfigParameters():
    def __init__(self):
        self.img_size = [224, 224]
        self.control_warning_datasize = True

        self.dataset_type_all = {'rgb':'_c.png', 
                                'd':'_d.png', 
                                't':'_t.png', 
                                'mask':'_c_mask.png'}
        self.augmentation_type_all = {'rv':'reverse', 
                            'gc':'gamma_correction', 
                            'pn':'pepper_noise', 
                            'co':'cut_out', 
                            'df':'deformation'}

        self.manual_masking_color = [36, 28, 237]# Red color in Paint(Windows)

        # key extentions
        self.key_pmd_drfb_drp = "_c_raw.png"
        self.key_pmd_drfb_fbp = "_c_raw_redmask.png"
        self.key_pmd_mmd = "_whitemask.png"
        self.key_pmd_mmcd = "_mask_prep"
        self.key_pmd_cmd = "_raw/"
        self.key_for_ads = self.dataset_type_all["mask"] # "_c_mask.png"

        self.list_crop_target_extention = ["_c_raw.png", 
        "_d_raw.png", 
        "_d_raw.csv", 
        "_c_raw_mask.png", 
        "_t_raw.png", 
        "_t_raw.csv"]
        # self.list_crop_target_extention = ["_c_raw.png", "_d_raw.png", "_d_raw.csv", "_c_raw_mask.png"]

        # If you use my dataset, you can't change crop_area
        self.crop_area = [[155, 13], [608, 346]]# xmin, ymin, xmax, ymax






