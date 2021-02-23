'''
2021/02/18 moriitkys@ROBOTAiM
Lisence: MIT
'''

import tkinter
from tkinter import ttk
from tkinter import filedialog
import glob
import os
import tkinter.font as tkFont

# https://denno-sekai.com/tkinter-pack/
# https://www.kihilog.net/python_tkinter_label/
# list box
# https://www.stjun.com/entry/2019/07/14/215812


class CreatePanel():
    '''
    This class creates UI panel for setting parameters especially for Deep Lerning
    Usage:
    import mylib.create_panel_for_mask as create_panel
    setting_panel = create_panel.CreatePanel()
    setting_panel.create_buttons()

    ~
    Notes:
    If you want to get the folder selected by this panel, 
    do as follows with Jupyter notebook etc. 
    list_selected_folders = setting_panel.list_selected_folders
    '''

    def __init__(self, 
                dataset_type_all, 
                augmentation_type_all,
                key_for_searching_foldername):
        self.tki = tkinter.Tk()
        self.tki.geometry('500x565')
        self.tki.title('Settings')

        self.var_gc_degree = tkinter.StringVar()
        self.var_df_number = tkinter.StringVar()

        self.list_selected_folders = []
        self.dict_selected_folders = {}

        self.dataset_type_all = dataset_type_all
        self.augmentation_type_all = augmentation_type_all
        self.list_selected_datatype = []
        self.flags_dataset_type = {}
        self.list_selected_augtype = []
        self.flags_aug_type = {}

        self.target_folder = os.getcwd().replace("\\", '/')
        self.target_folder = self.target_folder.replace(
            "/mylib", "") + '/DataSource/rgbdt'

        self.key_for_searching_foldername = key_for_searching_foldername

        # Prepare self.dict_object_class_number
        self.prepare_dict_object_class_number()

    
    def prepare_dict_object_class_number(self):
        # Prepare self.dict_object_class_number
        self.dict_object_class_number = {}
        list_object_class_path = glob.glob(self.target_folder + "/*")
        for object_class_path in list_object_class_path:
            object_class_path = object_class_path.replace("\\", "/")
            object_class_name = object_class_path[object_class_path.rfind(
                '/')+1:]
            list_object_class_number_path = glob.glob(
                self.target_folder + "/" + object_class_name + "/*")
            for object_class_number_path in list_object_class_number_path:
                object_class_number_path = object_class_number_path.replace(
                    "\\", "/")
                object_class_number_name = object_class_number_path[object_class_number_path.rfind(
                    '/')+1:]
                # I want to list only the folders that are the target of data expansion
                # Like "/0001", "/0002", ...
                #flag_containing_key = True
                # for ignore_key in self.config_param.key_ignore_foldername_for_mask:
                #    if ignore_key in object_class_number_path:  # Exclude if _aug, _raw, etc. are included in the path
                #        flag_containing_ignorekey = True
                for key in self.key_for_searching_foldername:
                    # Exclude if _aug, _raw, etc. are included in the path
                    for filepath in glob.glob(object_class_number_path + "/*"):
                        if key in filepath:
                            # print("false")
                            #flag_containing_key = False
                            # if flag_containing_key:
                            self.dict_object_class_number[object_class_name +
                                                          "/"+object_class_number_name] = object_class_number_path
                            break
        #print("list_object_class_path", list_object_class_path)
        #print("list_object_class_number_path", list_object_class_number_path)
        # print(self.dict_object_class_number)

    def change_parent_direstory(self,):
        self.target_folder = tkinter.filedialog.askdirectory(
            initialdir=self.target_folder)
        self.text_datasource.set(self.target_folder)
        #print("cpd", self.target_folder)

        # Update self.dict_object_class_number
        self.prepare_dict_object_class_number()

        list_object_class_number_name = [
            i for i in self.dict_object_class_number]
        self.list_object_class_number_name_tk.set(
            list_object_class_number_name)

    def select_class_number_folders(self):
        self.list_selected_folders = []
        self.dict_selected_folders = {}
        list_selected_folders_name = []
        #print(self.listbox_target_folders.curselection())
        for selected_name in self.listbox_target_folders.curselection():
            for i, key in enumerate(self.dict_object_class_number):
                if i == selected_name:
                    self.list_selected_folders.append(
                        self.dict_object_class_number[key])
                    self.dict_selected_folders[key] = self.dict_object_class_number[key]
                    list_selected_folders_name.append(key)

        # self.print_folders_value.set(list_selected_folders_name)
        self.print_folders.delete("1.0", "end")
        self.print_folders.insert(1.0, '\n'.join(list_selected_folders_name))

    def select_dataset_type(self):
        self.list_selected_datatype = []
        list_selected_datatype_name = []
        for key in self.dataset_type_all:
            self.flags_dataset_type[key] = False
        # print(self.listbox.curselection())
        for selected_name in self.listbox_dataset_type.curselection():
            for i, key in enumerate(self.flags_dataset_type):
                if i == selected_name:
                    self.flags_dataset_type[key] = True
                    self.list_selected_datatype.append(key)
                    list_selected_datatype_name.append(key)

        #self.print_datatypes_value.set(list_selected_datatype_name)
        self.print_datatypes_value.delete("1.0", "end")
        self.print_datatypes_value.insert(1.0, ', '.join(list_selected_datatype_name))

    def select_aug_type(self):
        self.list_selected_augtype = []
        list_selected_augtype_name = []
        for key in self.augmentation_type_all:
            self.flags_aug_type[key] = False
        # print(self.listbox.curselection())
        for selected_name in self.listbox_aug_type.curselection():
            for i, key in enumerate(self.flags_aug_type):
                if i == selected_name:
                    self.flags_aug_type[key] = True
                    self.list_selected_augtype.append(key)
                    list_selected_augtype_name.append(key)

        #self.print_augtypes_value.set(list_selected_augtype_name)
        self.print_augtypes_value.delete("1.0", "end")
        self.print_augtypes_value.insert(1.0, ', '.join(list_selected_augtype_name))

    def tkinter_callback(self, event):
        if event.widget["bg"] == "SystemButtonFace":
            event.widget["bg"] = "blue"
        else:
            event.widget["bg"] = "SystemButtonFace"

    def click_start(self,):
        # print("start")
        self.tki.destroy()

    def create_buttons(self):
        # Create labels and buttons
        y_axis_step = 25
        y_axis = 10
        self.radio_value_split = tkinter.IntVar()

        fontStyle = tkFont.Font(family="System", size=10, weight="bold")
        self.label_title = tkinter.Label(
            self.tki, text='Data Augmentation mainly for Mask R-CNN', font=fontStyle)
        self.label_title.place(x=25, y=y_axis)
        y_axis += y_axis_step

        self.label_explain1 = tkinter.Label(
            self.tki, text='Default targets are all folders in ')
        self.label_explain1.place(x=25, y=y_axis)
        self.text_datasource = tkinter.StringVar()
        self.text_datasource.set('./DataSource/rgbdt')
        self.label_explain2 = tkinter.Label(
            self.tki, textvariable=self.text_datasource)
        self.label_explain2.place(x=200, y=y_axis)
        y_axis += y_axis_step

        self.label_explain3 = tkinter.Label(
            self.tki, text='Click to change target folder ---------->')
        self.label_explain3.place(x=25, y=y_axis)

        btn_listbox = tkinter.Button(
            self.tki, text="Change Parent Directory", command=self.change_parent_direstory)
        btn_listbox.place(x=250,  y=y_axis)

        y_axis += y_axis_step + 10

        y_axis_step = 30
        # -------------------------------
        # ----- Show target folders -----
        list_target_folder_children_name = [
            name for name in self.dict_object_class_number]
        self.list_object_class_number_name_tk = tkinter.StringVar()
        self.list_object_class_number_name_tk.set(
            list_target_folder_children_name)  # dict_tk?

        # Scroll Bar??? (Not Available. Why?)
        self.scroll = tkinter.Scrollbar(self.tki)
        self.listbox_target_folders = tkinter.Listbox(self.tki, listvariable=self.list_object_class_number_name_tk,
                                       height=7, width=35, selectmode='multiple',
                                       yscrollcommand=self.scroll.set)

        self.listbox_target_folders.place(x=25,  y=y_axis)
        #self.listbox.pack(side="left", fill="both")
        self.scroll.config(command=self.listbox_target_folders.yview)

        # Click to bring up a window to select the target folder 
        btn_listbox_target_folders = tkinter.Button(
            self.tki, text="Select Target Folders", command=self.select_class_number_folders)
        btn_listbox_target_folders.place(x=250,  y=y_axis)
        btn_listbox_target_folders.bind("<1>", self.tkinter_callback)

        y_axis += y_axis_step

        # Show a list of folders selected on the right 
        self.print_folders = tkinter.Text(self.tki)
        self.print_folders.insert(1.0, '\n'.join(self.list_selected_folders))
        self.print_folders.place(x=250,  y=y_axis, height=85, width=220)
        # ----- End of Showing target folders -----

        y_axis += y_axis_step + 65

        # ------------------------------
        # ----- Show dataset types -----
        self.label_dataset_types = tkinter.Label(
            self.tki, text='Select dataset_type (Blue is ON)')
        self.label_dataset_types.place(x=25, y=y_axis)

        y_axis += y_axis_step

        list_dataset_type_all = [
            name for name in self.dataset_type_all]
        self.list_dataset_type_all_tk = tkinter.StringVar()
        self.list_dataset_type_all_tk.set(
            list_dataset_type_all)  # dict_tk?

        # Scroll Bar??? (Not Available. Why?)
        self.scroll = tkinter.Scrollbar(self.tki)
        self.listbox_dataset_type = tkinter.Listbox(self.tki, listvariable=self.list_dataset_type_all_tk,
                                       height=5, width=15, selectmode='multiple',
                                       yscrollcommand=self.scroll.set)

        self.listbox_dataset_type.place(x=25,  y=y_axis)
        #self.listbox.pack(side="left", fill="both")
        self.scroll.config(command=self.listbox_dataset_type.yview)

        # Click to bring up a window to select the target folder 
        btn_listbox_dataset_type = tkinter.Button(
            self.tki, text="Select dataset_type", command=self.select_dataset_type)
        btn_listbox_dataset_type.place(x=175,  y=y_axis)
        btn_listbox_dataset_type.bind("<1>", self.tkinter_callback)

        y_axis += y_axis_step

        # Show a list of folders selected on the right 
        self.print_datatypes_value = tkinter.Text(self.tki)
        self.print_datatypes_value.insert(1.0, '\n'.join(self.list_selected_datatype))
        self.print_datatypes_value.place(x=175,  y=y_axis, height=30, width=150)
        # ----- End of Showing dataset types -----

        y_axis += y_axis_step + 25

        # ------------------------------
        # ----- Show augmentation types -----
        self.label_aug_types = tkinter.Label(
            self.tki, text='Select aug_type (Blue is ON)')
        self.label_aug_types.place(x=25, y=y_axis)

        y_axis += y_axis_step

        list_augmentation_type_all = [
            name for name in self.augmentation_type_all]
        self.list_augmentation_type_all_tk = tkinter.StringVar()
        self.list_augmentation_type_all_tk.set(
            list_augmentation_type_all)  # dict_tk?

        # Scroll Bar??? (Not Available. Why?)
        self.scroll = tkinter.Scrollbar(self.tki)
        self.listbox_aug_type = tkinter.Listbox(self.tki, listvariable=self.list_augmentation_type_all_tk,
                                       height=5, width=15, selectmode='multiple',
                                       yscrollcommand=self.scroll.set)

        self.listbox_aug_type.place(x=25,  y=y_axis)
        #self.listbox.pack(side="left", fill="both")
        self.scroll.config(command=self.listbox_aug_type.yview)

        # Click to bring up a window to select the target folder 
        btn_listbox_aug_type = tkinter.Button(
            self.tki, text="Select aug_type", command=self.select_aug_type)
        btn_listbox_aug_type.place(x=175,  y=y_axis)
        btn_listbox_aug_type.bind("<1>", self.tkinter_callback)

        y_axis += y_axis_step

        # Show a list of folders selected on the right 
        self.print_augtypes_value = tkinter.Text(self.tki)
        self.print_augtypes_value.insert(1.0, '\n'.join(self.list_selected_augtype))
        self.print_augtypes_value.place(x=175,  y=y_axis, height=30, width=150)
        # ----- End of Showing dataset types -----

        y_axis += y_axis_step + 25

        # ----- Ganmma Correction

        label_gc_degree = tkinter.Label(
            self.tki, text="Ganmma Correction \n(The bigger, the brighter) ")
        label_gc_degree.place(x=25, y=y_axis)
        y_axis += y_axis_step + 5

        self.var_gc_degree.set(0.5)
        self.sp_epochs = tkinter.Spinbox(
            self.tki, from_=0.0, to=1, textvariable=self.var_gc_degree, increment=0.1)
        self.sp_epochs.place(x=25, y=y_axis)

        # ----- Number of deformation -----
        y_axis -= y_axis_step

        label_df_number = tkinter.Label(
            self.tki, text="Number of deformation ")
        label_df_number.place(x=200, y=y_axis)
        y_axis += y_axis_step

        self.var_df_number.set(1)
        spinbox = tkinter.Spinbox(
            self.tki, from_=0, to=10, textvariable=self.var_df_number, increment=1)
        spinbox.place(x=200, y=y_axis)
        y_axis += y_axis_step

        # ----- Start -----
        label_start = tkinter.Label(self.tki, text="Start (Close this window)")
        label_start.place(x=150, y=y_axis)
        #y_axis += y_axis_step
        y_axis += 25
        btn_start = tkinter.Button(
            self.tki, text="Start", command=self.click_start)
        btn_start.place(x=150, y=y_axis)

        # Display the button window
        btn_start.bind("<1>", self.tkinter_callback)
        self.tki.mainloop()
