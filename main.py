#!/usr/bin/env python3

import sys
try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
except ImportError:
    print('Please install python3-tk using your system package manager')
    sys.exit(1)
from mkpasswd import mkhash


class ScrollableFrame(tk.Tk):
    def __init__ (self, master, width, height, mousescroll=0):
        self.mousescroll = mousescroll
        self.master = master
        self.height = height
        self.width = width
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=1)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas = tk.Canvas(self.main_frame, width=self.width, height=self.height, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.bind(
            '<Configure>',
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.frame = ttk.Frame(self.canvas, width=self.width, height=self.height)
        self.frame.pack(expand=True, fill=tk.BOTH)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.frame.bind("<Enter>", self.entered)
        self.frame.bind("<Leave>", self.left)

    def _on_mouse_wheel(self,event):
        self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

    def entered(self,event):
        if self.mousescroll:
            self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def left(self,event):
        if self.mousescroll:
            self.canvas.unbind_all("<MouseWheel>")


class LabeledControl:
    def __init__(self, label_text, value):
        self.label_text = label_text
        self.label = None
        self.control = None
        self.value = value

    def show(self, frame, row):
        self.label = tk.Label(frame, text=self.label_text, width=20)
        self.label.grid(row=row, column=0)

        if isinstance(self.value, bool):
            self.checkbox_value = tk.IntVar()
            self.control = tk.Checkbutton(frame, text='', variable=self.checkbox_value, command=self._update_checkbox)
            if self.value == True:
                self.control.select()
        elif type(self.value) == list:
            self.control = ttk.Combobox(frame, values=self.value)
            self.control.set(self.value[0])
        else:
            self.control = tk.Entry(frame)
            self.control.insert(0, self.value)
        self.control.grid(row=row, column=1, sticky=tk.W)

    def _update_checkbox(self):
        self.value = bool(self.checkbox_value.get())

class MultiselectWidget(LabeledControl):
    def __init__(self, label_text, values):
        super().__init__(label_text, values)
        self.selected_values = []

    def show(self, frame, row):
        self.label = tk.Label(frame, text=self.label_text, width=20)
        self.label.grid(row=row, column=0)

        listbox_height = min(10, len(self.value))  # Limit the max height to 10 for better UI
        self.control = tk.Listbox(frame, selectmode=tk.MULTIPLE, height=listbox_height)
        for value in self.value:
            self.control.insert(tk.END, value)
        self.control.grid(row=row, column=1, sticky=tk.W)
        self.control.bind('<<ListboxSelect>>', self._update_selected_values)

    def _update_selected_values(self, event):
        selected_indices = self.control.curselection()
        self.selected_values = [self.value[index] for index in selected_indices]

    def get_selected_values(self):
        return self.selected_values

class GroupFrame:
    def __init__(self, group_name, state=True):
        self.group_name = group_name
        self.state = tk.IntVar(value=state)
        self.elements = []

    def add(self, element):
        self.elements.append(element)

    def show(self, target, row):
        label_frame = ttk.Labelframe(target, text='')
        check_button = tk.Checkbutton(label_frame, text=self.group_name, variable=self.state)
        if self.state == True:
            check_button.select()
        label_frame['labelwidget'] = check_button
        for i, element in enumerate(self.elements):
            element.show(label_frame, i)
        label_frame.grid(row=row, rowspan=len(self.elements), columnspan=2, sticky="nsew")


class App(tk.Tk):
    def __init__(self):
        self.obj = ScrollableFrame(super().__init__(), 380, 400)
        self.frame = self.obj.frame
        self.widgets = []
        self.answers = []
        self.comment_out = []

# Locale
        self.widgets.append(GroupFrame('Locale'))
        self.widgets[0].add(LabeledControl('Language', ['pl', 'en']))
        self.widgets[0].add(LabeledControl('Country', ['PL', 'EN']))
        self.widgets[0].add(LabeledControl('Locale', ['pl_PL.UTF-8', 'en_US.UTF-8']))
# Keyboard configuration
        self.widgets.append(GroupFrame('Keyboard configuration'))
        self.widgets[1].add(LabeledControl('Keymap', ['pl', 'us']))
## Non-free firmware load
        self.widgets.append(GroupFrame('Enable non-free firmware'))
        self.widgets[2].add(LabeledControl('Load non-free firmware', True))
## Network configuration
        self.widgets.append(GroupFrame('Network configuration'))
        self.widgets[3].add(LabeledControl('Network config', 'auto'))
# Hostname configuration
        self.widgets[3].add(LabeledControl('Hostname', 'debian'))
        self.widgets[3].add(LabeledControl('Domain', ''))
# Mirror settings
        self.widgets.append(GroupFrame('Mirror settings'))
        self.widgets[4].add(LabeledControl('Country', 'PL'))
        self.widgets[4].add(LabeledControl('Http', 'deb.debian.org'))
        self.widgets[4].add(LabeledControl('Proxy', ''))
# Clock and time zone setup
        self.widgets.append(GroupFrame('Clock and time'))
        self.widgets[5].add(LabeledControl('Use UTC', True))
        self.widgets[5].add(LabeledControl('Timezone', 'Europe/Warsaw'))
# Partitioning
        self.widgets.append(GroupFrame('Partitioning', state=False))
        self.widgets[6].add(LabeledControl('Disk', '/dev/sda'))
        self.widgets[6].add(LabeledControl('Method', ['regular', 'lvm', 'crypto']))
        self.widgets[6].add(LabeledControl('Recipe', ['atomic', 'home', 'multi']))
        self.widgets[6].add(LabeledControl('Create partition table', True))
        self.widgets[6].add(LabeledControl('Partition menu', 'finish'))
        self.widgets[6].add(LabeledControl('Write changes', True))
        self.widgets[6].add(LabeledControl('Overwrite', True))
# Root password
        self.widgets.append(GroupFrame('User/Password setup'))
        self.widgets[7].add(LabeledControl('Root password', ''))
# Regular user account
        self.widgets[7].add(LabeledControl('User fullname', ''))
        self.widgets[7].add(LabeledControl('Username', ''))
        self.widgets[7].add(LabeledControl('Password', ''))
# Apt setup
        self.widgets.append(GroupFrame('Apt setup'))
        self.widgets[8].add(LabeledControl('Enable non-free repo', True))
        self.widgets[8].add(LabeledControl('Enable contrib repo', True))
        self.widgets[8].add(LabeledControl('Use debian mirror', True))
# Skip scanning other media
        self.widgets.append(GroupFrame('Scan external media'))
        self.widgets[9].add(LabeledControl('Scan current cd-rom', False))
        self.widgets[9].add(LabeledControl('Scan next cd-rom', False))
        self.widgets[9].add(LabeledControl('Scan failed', False))
# Package selection
        self.widgets.append(GroupFrame('Package selection'))
        #TODO: multiselect package selection
        #self.widgets[10].add(LabeledControl('Tasksel Package install', 'standard'))
        self.widgets[10].add(MultiselectWidget('Tasksel Package install', ['standard', 'gnome-desktop', 'xfce-desktop', 'kde-desktop', 'lxde-desktop', 'web-server', 'ssh-server']))
      
# Grub bootloader setup
        self.widgets.append(GroupFrame('Grub bootloader setup'))
        self.widgets[11].add(LabeledControl('Install grub on drive', True))
        self.widgets[11].add(LabeledControl('Scan for other OS', True))
        self.widgets[11].add(LabeledControl('Choose boot device', '/dev/sda'))
# Preseeding other packages
        self.widgets.append(GroupFrame('Install additional packages'))
        self.widgets[12].add(LabeledControl('List other packages', ''))
# Disable popularity-contest
        self.widgets.append(GroupFrame('Popularity contest package'))
        self.widgets[13].add(LabeledControl('Participate', False))
# Finish installation
        self.widgets.append(GroupFrame('Finished install'))
        self.widgets[14].add(LabeledControl('Message', 'note'))

        i=0
        for widget in self.widgets:
            widget.show(self.frame, i)
            i = i+len(widget.elements)

        generate_button = tk.Button(self.frame, text='Generate', command=self.preseed_gen)
        generate_button.grid(row=i, column=1)

    def preseed_gen(self):
        self.answers.clear()
        self.comment_out.clear()
        for i in range(len(self.widgets)):
            if self.widgets[i].state.get() == 0:
                self.comment_out.append('#')
            else:
                self.comment_out.append('')
            for j in self.widgets[i].elements:
                if isinstance(j, MultiselectWidget):
                    selected_values = j.get_selected_values()
                    self.answers.append(' '.join(selected_values))
                elif isinstance(j.value, bool):
                    self.answers.append(str(j.value).lower())
                else:
                    self.answers.append(j.control.get())
                continue
        # Create and write the preseed.cfg file
        with open("preseed.cfg", "w") as preseed_file:
            preseed_file.write("# Auto-generated preseed.cfg file\n")
            preseed_file.write("{}d-i debian-installer/language string {}\n".format(self.comment_out[0], self.answers[0]))
            preseed_file.write("{}d-i debian-installer/country string {}\n".format(self.comment_out[0], self.answers[1]))
            preseed_file.write("{}d-i debian-installer/locale string {}\n".format(self.comment_out[0], self.answers[2]))
            preseed_file.write("{}d-i keyboard-configuration/xkb-keymap select {}\n".format(self.comment_out[1], self.answers[3]))
            preseed_file.write("{}d-i hw-detect/load_firmware boolean {}\n".format(self.comment_out[2], self.answers[4]))
            preseed_file.write("{}d-i netcfg/choose_interface select {}\n".format(self.comment_out[3], self.answers[5]))
            preseed_file.write("{}d-i netcfg/get_hostname string {}\n".format(self.comment_out[3], self.answers[6]))
            preseed_file.write("{}d-i netcfg/get_domain string {}\n".format(self.comment_out[3], self.answers[7]))
            preseed_file.write("{}d-i mirror/country string {}\n".format(self.comment_out[4], self.answers[8]))
            preseed_file.write("{}d-i mirror/http/mirror string {}\n".format(self.comment_out[4], self.answers[9]))
            preseed_file.write("{}d-i mirror/http/proxy string {}\n".format(self.comment_out[4], self.answers[10]))
            preseed_file.write("{}d-i clock-setup/utc boolean {}\n".format(self.comment_out[5], self.answers[11]))
            preseed_file.write("{}d-i time/zone string {}\n".format(self.comment_out[5], self.answers[12]))
            preseed_file.write("{}d-i partman-auto/disk string {}\n".format(self.comment_out[6], self.answers[13]))
            preseed_file.write("{}d-i partman-auto/method string {}\n".format(self.comment_out[6], self.answers[14]))
            preseed_file.write("{}d-i partman-auto/choose_recipe select {}\n".format(self.comment_out[6], self.answers[15]))
            preseed_file.write("{}d-i partman-partitioning/confirm_write_new_label boolean {}\n".format(self.comment_out[6], self.answers[16]))
            preseed_file.write("{}d-i partman/choose_partition select {}\n".format(self.comment_out[6], self.answers[17]))
            preseed_file.write("{}d-i partman/confirm boolean {}\n".format(self.comment_out[6], self.answers[18]))
            preseed_file.write("{}d-i partman/confirm_nooverwrite boolean {}\n".format(self.comment_out[6], self.answers[19]))
            preseed_file.write("{}d-i passwd/root-password-crypted password {}\n".format(self.comment_out[7], mkhash(self.answers[20])))
            preseed_file.write("{}d-i passwd/make-user boolean true\n".format(self.comment_out[7]))
            preseed_file.write("{}d-i passwd/user-fullname string {}\n".format(self.comment_out[7], self.answers[21]))
            preseed_file.write("{}d-i passwd/username string {}\n".format(self.comment_out[7], self.answers[22]))
            preseed_file.write("{}d-i passwd/user-password-crypted password {}\n".format(self.comment_out[7], mkhash(self.answers[23])))
            preseed_file.write("{}d-i apt-setup/non-free boolean {}\n".format(self.comment_out[8], self.answers[24]))
            preseed_file.write("{}d-i apt-setup/contrib boolean {}\n".format(self.comment_out[8], self.answers[25]))
            preseed_file.write("{}d-i apt-setup/use_mirror boolean {}\n".format(self.comment_out[8], self.answers[26]))
            preseed_file.write("{}d-i apt-setup/cdrom/set-first boolean {}\n".format(self.comment_out[9], self.answers[27]))
            preseed_file.write("{}d-i apt-setup/cdrom/set-next boolean {}\n".format(self.comment_out[9], self.answers[28]))
            preseed_file.write("{}d-i apt-setup/cdrom/set-failed boolean {}\n".format(self.comment_out[9], self.answers[29]))
            preseed_file.write("{}tasksel tasksel/first multiselect {}\n".format(self.comment_out[10], self.answers[30]))
            preseed_file.write("{}d-i grub-installer/only_debian boolean {}\n".format(self.comment_out[11], self.answers[31]))
            preseed_file.write("{}d-i grub-installer/with_other_os boolean {}\n".format(self.comment_out[11], self.answers[32]))
            preseed_file.write("{}d-i grub-installer/bootdev string {}\n".format(self.comment_out[11], self.answers[33]))
            preseed_file.write("{}d-i pkgsel/include string {}\n".format(self.comment_out[12], self.answers[34]))
            preseed_file.write("{}d-i pkgsel/upgrade select full-upgrade\n".format(self.comment_out[12]))
            preseed_file.write("{}popularity-contest popularity-contest/participate boolean {}\n".format(self.comment_out[13], self.answers[35]))
            preseed_file.write("{}d-i finish-install/reboot_in_progress {}\n".format(self.comment_out[14], self.answers[36]))
        messagebox.showinfo(title="Info", message="File preseed.cfg generated")


if __name__ == "__main__":
    app = App()
    app.title("D-I pressed generator")
    app.mainloop()
