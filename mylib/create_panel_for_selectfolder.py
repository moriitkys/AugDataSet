'''
2021/02/16 moriitkys@ROBOTAiM
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


class CreatePanelForSelectFolder():
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
                key_for_searching_foldername):
        self.tki = tkinter.Tk()
        self.tki.geometry('500x400')
        self.tki.title('Settings')

        self.var_gc_degree = tkinter.StringVar()
        self.var_df_number = tkinter.StringVar()

        self.list_selected_folders = []
        self.dict_selected_folders = {}

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
                for filepath in glob.glob(object_class_number_path + "/*"):
                    if self.key_for_searching_foldername in filepath.replace("\\", "/"):
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
