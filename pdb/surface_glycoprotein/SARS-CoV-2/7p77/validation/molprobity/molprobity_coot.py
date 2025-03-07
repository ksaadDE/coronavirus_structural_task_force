# script auto-generated by phenix.molprobity


from __future__ import absolute_import, division, print_function
from six.moves import cPickle as pickle
from six.moves import range
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui(object):
  def __init__(self, title):
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window(self):
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window(self, *args):
    self.window.destroy()
    self.window = None

  def confirm_data(self, data):
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists(self, data):
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui(coot_extension_gui):
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None):
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__(self, data_file=None, data=None):
    assert ([data, data_file].count(None) == 1)
    if (data is None):
      data = load_pkl(data_file)
    if not self.confirm_data(data):
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets(self, data_key, box):
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots(self, *args):
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots(self, *args):
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui(coot_extension_gui):
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list(object):
  def __init__(self, columns, column_types, rows, box,
      default_size=(380,200)):
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)):
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns):
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange(self, treeview):
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots(show_dots, overlaps_only):
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects):
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects):
      set_display_generic_object(object_number, 0)

def load_pkl(file_name):
  pkl = open(file_name, "rb")
  data = pickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = []
data['omega'] = [('W', ' 106 ', 'PRO', None, (210.31400000000002, 166.162, 259.481)), ('X', ' 106 ', 'PRO', None, (163.891, 212.454, 258.682)), ('Y', ' 106 ', 'PRO', None, (230.313, 230.612, 258.585))]
data['rota'] = []
data['cbeta'] = [('E', '1101 ', 'HIS', ' ', 0.5964096063240025, (182.542, 216.997, 127.09600000000002))]
data['probe'] = [(' C1098  ASN  ND2', ' C1100  THR  OG1', -1.131, (228.084, 211.352, 128.961)), (' C1100  THR  OG1', ' L   1  NAG  C1 ', -1.117, (227.893, 210.985, 128.103)), (' C1100  THR  HG1', ' L   1  NAG  C1 ', -0.891, (227.15, 210.918, 128.31)), (' B1115  ILE HD12', ' B1135  ASN  ND2', -0.653, (205.284, 184.807, 127.465)), (' B  64  TRP  HE1', ' B 264  ALA  HB1', -0.624, (161.506, 157.568, 212.938)), (' C1098  ASN  CG ', ' C1100  THR  OG1', -0.611, (227.227, 211.365, 129.82)), (' E 501  ASN  HB2', ' E 506  GLN HE21', -0.602, (153.202, 204.939, 267.126)), (' B 106  PHE  HB2', ' B 117  LEU  HB3', -0.594, (166.667, 171.105, 230.419)), (' C1100  THR HG21', ' L   1  NAG  O7 ', -0.594, (230.641, 211.605, 128.017)), (' E 106  PHE  HB2', ' E 117  LEU  HB3', -0.59, (192.239, 247.683, 231.317)), (' C1101  HIS  HE2', ' L   2  NAG  H82', -0.589, (225.795, 210.341, 122.459)), (' C 113  LYS  HD2', ' C 114  THR HG23', -0.589, (245.696, 197.228, 241.332)), (' C1098  ASN  ND2', ' C1100  THR  HG1', -0.578, (227.101, 211.236, 129.129)), (' X  33  TYR  HB3', ' X  99  ALA  HB3', -0.565, (169.691, 215.351, 248.569)), (' D  36  TRP  HE1', ' D  90  TYR  HB3', -0.554, (221.815, 242.265, 284.371)), (' B 136  CYS  SG ', ' B 137  ASN  N  ', -0.552, (161.792, 156.232, 237.313)), (' Y  33  TYR  HB3', ' Y  99  ALA  HB3', -0.549, (229.758, 223.816, 248.658)), (' E1080  ALA  HB3', ' E1132  ILE HG12', -0.549, (181.633, 200.592, 132.666)), (' C 703  ASN  ND2', ' E 787  GLN  OE1', -0.546, (227.947, 212.816, 157.214)), (' W  33  TYR  HB3', ' W  99  ALA  HB3', -0.545, (205.66, 169.923, 249.231)), (' W  50  ALA  HB3', ' W  59  TYR  HB2', -0.544, (207.033, 161.507, 254.736)), (' E 190  ARG HH21', ' E 192  PHE  HZ ', -0.543, (196.862, 256.317, 219.424)), (' C 106  PHE  HB2', ' C 117  LEU  HB3', -0.539, (246.643, 187.902, 231.452)), (' E 969  ASN  O  ', ' E 995  ARG  NH1', -0.538, (204.005, 213.155, 215.726)), (' W  91  THR HG23', ' W 122  THR  HA ', -0.535, (187.309, 160.566, 266.673)), (' C  92  PHE  HB3', ' C 192  PHE  HB2', -0.533, (249.184, 186.396, 217.801)), (' W  20  LEU HD12', ' W  81  LEU HD23', -0.532, (194.055, 160.419, 256.377)), (' B 357  ARG HH12', ' B 395  VAL  H  ', -0.531, (228.589, 180.36, 240.861)), (' E1029  MET  O  ', ' E1033  VAL  HB ', -0.527, (211.943, 212.308, 162.261)), (' B 826  VAL  HB ', ' B1057  PRO  HG2', -0.527, (178.376, 197.372, 178.236)), (' E  35  GLY  HA3', ' E  56  LEU HD12', -0.527, (190.311, 244.884, 209.732)), (' W  40  ALA  HB3', ' W  43  LYS  HB2', -0.526, (196.252, 166.527, 270.242)), (' E 136  CYS  SG ', ' E 137  ASN  N  ', -0.526, (181.37, 259.547, 237.945)), (' B 357  ARG HH22', ' B 395  VAL  HB ', -0.523, (228.448, 178.132, 240.266)), (' B1029  MET  O  ', ' B1033  VAL  HB ', -0.522, (189.475, 205.748, 162.425)), (' C 136  CYS  SG ', ' C 137  ASN  N  ', -0.52, (262.095, 191.629, 237.848)), (' B 736  VAL HG21', ' B1004  LEU HD11', -0.52, (190.011, 207.737, 198.425)), (' C 201  PHE  HB3', ' C 229  LEU  HB2', -0.52, (239.692, 184.818, 227.346)), (' X  40  ALA  HB3', ' X  43  LYS  HB2', -0.512, (170.586, 224.528, 269.758)), (' E 346  ARG  NH1', ' E 347  PHE  O  ', -0.511, (153.577, 189.489, 257.575)), (' C 751  ASN  O  ', ' C 755  GLN  NE2', -0.51, (192.998, 190.43, 215.389)), (' B1102  TRP  HD1', ' B1115  ILE HD11', -0.509, (204.629, 184.185, 130.001)), (' C 566  GLY  HA2', ' E  43  PHE  HB3', -0.508, (212.319, 237.12, 207.414)), (' E 312  ILE HD11', ' E 666  ILE HD13', -0.508, (181.366, 222.981, 184.961)), (' C 401  VAL HG22', ' C 509  ARG  HG3', -0.507, (221.328, 244.918, 256.183)), (' Y   6  GLU  O  ', ' Y 117  GLN  NE2', -0.506, (240.027, 208.547, 252.852)), (' C 294  ASP  N  ', ' C 294  ASP  OD1', -0.506, (240.317, 201.169, 198.8)), (' C 567  ARG  HA ', ' C 573  THR  HA ', -0.505, (213.909, 231.849, 206.188)), (' B 172  SER  OG ', ' B 173  GLN  N  ', -0.505, (152.448, 179.407, 224.034)), (' B 751  ASN  O  ', ' B 755  GLN  NE2', -0.503, (195.307, 216.746, 214.786)), (' B  96  GLU  OE1', ' B 190  ARG  NH1', -0.501, (154.331, 165.295, 216.656)), (' B 346  ARG  NH1', ' B 347  PHE  O  ', -0.501, (235.363, 169.442, 259.29)), (' D  68  THR  HB ', ' D  81  GLN  HB3', -0.499, (234.554, 239.001, 286.215)), (' Y  40  ALA  HB3', ' Y  43  LYS  HB2', -0.498, (237.002, 218.66, 270.069)), (' A  52  GLN  O  ', ' A  71  ARG  NH2', -0.498, (209.891, 168.312, 276.417)), (' E 759  PHE  O  ', ' E 763  LEU  HB2', -0.497, (213.846, 202.877, 199.459)), (' E 733  LYS  NZ ', ' E 775  ASP  OD2', -0.496, (220.959, 212.231, 183.594)), (' A  87  THR HG23', ' A 108  THR  HA ', -0.496, (231.57, 164.854, 292.6)), (' C 826  VAL  HB ', ' C1057  PRO  HG2', -0.495, (218.647, 183.922, 178.234)), (' C1104  VAL HG23', ' C1115  ILE HG12', -0.495, (215.02, 209.585, 130.857)), (' C 456  PHE  HB2', ' C 491  PRO  HB3', -0.494, (205.702, 241.068, 271.221)), (' B 963  VAL HG11', ' E 570  ALA  HB1', -0.494, (180.104, 198.32, 200.956)), (' C 190  ARG HH21', ' C 192  PHE  HZ ', -0.494, (251.842, 180.228, 219.301)), (' C 376  THR  HB ', ' C 435  ALA  HB3', -0.494, (224.278, 234.589, 254.843)), (' E 467  ASP  N  ', ' E 467  ASP  OD1', -0.491, (167.407, 185.583, 259.304)), (' C 277  LEU HD12', ' C 285  ILE HD13', -0.49, (236.364, 186.067, 205.205)), (' C 442  ASP  OD2', ' C 509  ARG  NH2', -0.489, (224.2, 248.061, 257.102)), (' C 734  THR HG21', ' C 959  LEU HD21', -0.488, (208.911, 187.086, 194.016)), (' C 172  SER  OG ', ' C 173  GLN  N  ', -0.487, (245.763, 171.947, 225.276)), (' E1028  LYS  NZ ', ' E1042  PHE  O  ', -0.486, (201.386, 211.436, 164.98)), (' D  39  LYS  HE3', ' D  45  ARG  HE ', -0.485, (214.597, 246.189, 278.766)), (' C 742  ILE  HA ', ' C1000  ARG  HD2', -0.485, (205.957, 189.092, 207.797)), (' E 726  ILE HD13', ' E 945  LEU HD13', -0.484, (204.607, 223.378, 173.283)), (' E 277  LEU HD12', ' E 285  ILE HD13', -0.484, (199.243, 240.15, 205.347)), (' E 444  LYS  HZ1', ' E 449  TYR  H  ', -0.484, (148.766, 193.575, 267.299)), (' C 402  ILE HD11', ' C 418  ILE HD12', -0.483, (215.553, 238.089, 262.232)), (' C  99  ASN  O  ', ' C 102  ARG  NH2', -0.48, (262.257, 177.961, 223.125)), (' D  87  THR HG23', ' D 108  THR  HA ', -0.48, (221.426, 251.906, 291.006)), (' C 229  LEU  HB3', ' C 231  ILE HG12', -0.477, (239.972, 184.031, 229.898)), (' B 858  LEU HD13', ' B 959  LEU HD22', -0.476, (184.079, 203.356, 196.412)), (' E 172  SER  OG ', ' E 173  GLN  N  ', -0.475, (207.045, 255.252, 225.439)), (' E 433  VAL HG12', ' E 512  VAL HG22', -0.475, (167.047, 197.927, 251.649)), (' X   6  GLU  O  ', ' X 117  GLN  NE2', -0.475, (178.238, 232.031, 252.594)), (' H  29  VAL  O  ', ' H  71  ARG  NH1', -0.474, (167.567, 211.298, 276.613)), (' X  91  THR HG23', ' X 122  THR  HA ', -0.473, (170.684, 235.271, 266.453)), (' E  99  ASN  O  ', ' E 102  ARG  NH2', -0.472, (193.757, 266.555, 223.321)), (' B 760  CYS  HA ', ' B 763  LEU  HB2', -0.471, (194.505, 212.359, 200.232)), (' X  50  ALA  HB3', ' X  59  TYR  HB2', -0.47, (161.45, 217.995, 254.07)), (' E 903  ALA  HB1', ' E 913  GLN  HG2', -0.469, (207.731, 215.229, 141.657)), (' E 802  PHE  HD1', ' E 805  ILE HD11', -0.469, (212.206, 224.771, 157.466)), (' C 735  SER  HA ', ' C 767  LEU HD13', -0.469, (202.768, 186.948, 194.347)), (' E 376  THR  HB ', ' E 435  ALA  HB3', -0.469, (163.643, 205.322, 254.875)), (' B 726  ILE HD13', ' B 945  LEU HD13', -0.468, (183.194, 193.661, 173.311)), (' C 802  PHE  HD1', ' C 805  ILE HD11', -0.467, (216.762, 182.69, 157.903)), (' C 346  ARG  NH1', ' C 347  PHE  O  ', -0.466, (216.045, 251.369, 257.664)), (' B 627  ASP  N  ', ' B 627  ASP  OD1', -0.465, (192.908, 162.352, 207.941)), (' B  34  ARG  NH2', ' B 221  SER  OG ', -0.465, (164.23, 172.748, 206.227)), (' C 299  THR  HA ', ' C 302  THR HG22', -0.465, (230.918, 200.837, 195.759)), (' C 369  TYR  O  ', ' Y  55  ASN  ND2', -0.465, (232.409, 235.304, 244.014)), (' E 278  LYS  HD3', ' E 287  ASP  HB2', -0.464, (198.061, 241.097, 197.024)), (' E 761  THR HG22', ' E 765  ARG HH21', -0.463, (219.011, 198.404, 197.452)), (' E 336  CYS  HB2', ' E 361  CYS  HB3', -0.461, (157.075, 193.558, 236.524)), (' C 360  ASN  H  ', ' C 523  THR  HB ', -0.46, (210.629, 243.354, 234.95)), (' H  39  LYS  HE3', ' H  45  ARG  HE ', -0.46, (158.542, 190.442, 278.96)), (' E 826  VAL  HB ', ' E1057  PRO  HG2', -0.459, (210.665, 225.583, 178.249)), (' B 189  LEU HD22', ' B 217  PRO  HG2', -0.458, (159.927, 165.395, 206.307)), (' B 945  LEU HD12', ' B 948  LEU HD12', -0.456, (182.177, 195.654, 175.421)), (' B 401  VAL HG22', ' B 507  PRO  HB2', -0.456, (224.709, 167.363, 261.756)), (' E 369  TYR  O  ', ' X  55  ASN  ND2', -0.455, (158.969, 212.467, 244.06)), (' C 442  ASP  O  ', ' C 448  ASN  ND2', -0.454, (225.564, 248.583, 263.246)), (' A  40  ALA  HB3', ' A  43  LYS  HB2', -0.454, (235.109, 165.94, 283.017)), (' H  15  GLY  H  ', ' H  82C LEU  HB2', -0.453, (144.562, 203.591, 292.05)), (' B  48  LEU HD13', ' B 305  SER  HA ', -0.453, (177.751, 183.602, 194.288)), (' E 327  VAL  HA ', ' E 542  ASN  HB3', -0.453, (165.096, 207.727, 220.279)), (' Y  50  ALA  HB3', ' Y  59  TYR  HB2', -0.451, (236.337, 230.014, 254.141)), (' B 442  ASP  OD2', ' B 509  ARG  NH2', -0.449, (228.905, 164.205, 258.964)), (' C1028  LYS  NZ ', ' C1042  PHE  O  ', -0.447, (210.769, 197.993, 165.306)), (' X  67  ARG  NH1', ' X  85  SER  O  ', -0.447, (158.612, 232.668, 263.667)), (' B 196  ASN  HB2', ' B 201  PHE  HD1', -0.446, (171.254, 175.825, 225.286)), (' A  20  LEU  HG ', ' A  82  MET  HE1', -0.444, (220.782, 165.736, 290.553)), (' H  87  THR HG23', ' H 108  THR  HA ', -0.444, (150.098, 194.413, 291.322)), (' B 193  VAL  HB ', ' B 204  TYR  HB2', -0.444, (167.319, 175.432, 215.452)), (' B 767  LEU HD23', ' B 770  ILE HD12', -0.444, (192.841, 208.205, 190.912)), (' B 109  THR  HG1', ' B 114  THR  HG1', -0.444, (172.447, 167.644, 239.339)), (' C 710  ASN  N  ', ' C 710  ASN  OD1', -0.444, (222.608, 222.11, 140.548)), (' E  93  ALA  HB3', ' E 266  TYR  HB2', -0.443, (187.481, 253.058, 213.141)), (' C  93  ALA  HB3', ' C 266  TYR  HB2', -0.443, (253.818, 190.018, 213.435)), (' E 401  VAL HG22', ' E 507  PRO  HB2', -0.442, (156.958, 199.825, 260.59)), (' C 328  ARG  HA ', ' C 328  ARG  HD2', -0.442, (227.067, 237.247, 219.734)), (' B  84  LEU HD22', ' B 267  VAL HG11', -0.442, (170.595, 162.159, 220.093)), (' B 222  ALA  HB2', ' B 285  ILE  HB ', -0.442, (166.849, 179.339, 204.383)), (' C 701  ALA  HB3', ' E 787  GLN  HG2', -0.441, (229.953, 211.626, 161.067)), (' D  45  ARG HH12', ' D 101  ILE HD13', -0.441, (213.827, 241.627, 278.01)), (' E 159  VAL HG13', ' E 160  TYR  HD1', -0.441, (190.887, 258.852, 236.954)), (' B1028  LYS  NZ ', ' B1042  PHE  O  ', -0.441, (194.8, 197.329, 165.4)), (' D  51  ILE HD11', ' D  69  ILE HG12', -0.44, (229.559, 235.303, 280.64)), (' E 710  ASN  N  ', ' E 710  ASN  OD1', -0.44, (175.212, 209.736, 140.375)), (' Y  91  THR HG23', ' Y 122  THR  HA ', -0.438, (246.21, 213.134, 266.761)), (' E 299  THR  HA ', ' E 302  THR HG22', -0.436, (189.579, 227.998, 195.856)), (' C 389  ASP  N  ', ' C 389  ASP  OD1', -0.435, (221.907, 231.319, 233.877)), (' C 627  ASP  N  ', ' C 627  ASP  OD1', -0.435, (242.146, 214.589, 207.912)), (' W  83  MET  HB3', ' W  86  LEU HD21', -0.435, (192.613, 154.349, 260.49)), (' B 130  VAL HG12', ' B 168  PHE  HB3', -0.435, (163.811, 178.358, 235.215)), (' B 792  PRO  HG3', ' E 707  TYR  HB3', -0.434, (174.483, 210.14, 150.28)), (' W  67  ARG  NH1', ' W  85  SER  O  ', -0.433, (195.589, 151.795, 264.072)), (' A   4  LEU HD11', ' A  94  VAL HG12', -0.433, (217.78, 177.34, 279.805)), (' E 627  ASP  N  ', ' E 627  ASP  OD1', -0.432, (171.879, 230.381, 208.179)), (' E 430  THR  OG1', ' E 515  PHE  O  ', -0.431, (174.026, 195.213, 243.19)), (' E 406  GLU  HB3', ' E 409  GLN  HB2', -0.431, (169.951, 201.371, 263.099)), (' C 430  THR  OG1', ' C 515  PHE  O  ', -0.429, (210.214, 230.572, 243.287)), (' B 328  ARG  HA ', ' B 328  ARG  HD2', -0.429, (219.697, 166.268, 220.524)), (' E 760  CYS  SG ', ' E 764  ASN  ND2', -0.429, (218.137, 205.783, 200.275)), (' X  88  PRO  HA ', ' X 123  VAL HG23', -0.429, (165.023, 235.271, 268.374)), (' B 894  LEU HD13', ' E 715  PRO  HD3', -0.428, (188.638, 216.106, 147.273)), (' E 407  VAL HG21', ' E 508  TYR  HD2', -0.428, (163.001, 205.036, 259.452)), (' B 985  ASP  HA ', ' B 986  PRO  HD3', -0.428, (187.858, 209.009, 228.926)), (' B 433  VAL HG12', ' B 512  VAL HG22', -0.428, (222.263, 176.769, 252.593)), (' E 498  GLN  O  ', ' E 506  GLN  NE2', -0.428, (152.175, 203.726, 266.636)), (' E1115  ILE HD12', ' E1135  ASN HD21', -0.427, (185.842, 209.237, 128.125)), (' B 742  ILE  O  ', ' B1000  ARG  NH1', -0.427, (186.804, 206.11, 210.137)), (' Y  67  ARG  NH1', ' Y  85  SER  O  ', -0.426, (250.447, 225.103, 263.807)), (' C 598  ILE HG23', ' C 664  ILE HG21', -0.426, (232.916, 206.605, 184.34)), (' C 159  VAL HG13', ' C 160  TYR  HD1', -0.425, (256.831, 183.907, 236.951)), (' E 310  LYS  NZ ', ' E 663  ASP  OD1', -0.424, (187.278, 229.063, 177.951)), (' C 327  VAL  HA ', ' C 542  ASN  HB3', -0.424, (225.772, 232.085, 220.362)), (' Y  37  PHE  HB2', ' Y  95  TYR  HB2', -0.424, (234.879, 217.471, 258.381)), (' C 976  VAL HG12', ' C 979  ASP  H  ', -0.424, (211.32, 185.272, 220.813)), (' B 415  THR  OG1', ' B 416  GLY  N  ', -0.424, (217.018, 185.039, 265.318)), (' C 953  ASN  O  ', ' C 957  GLN  OE1', -0.423, (218.458, 192.389, 190.168)), (' B 478  THR  OG1', ' B 487  ASN  ND2', -0.423, (233.593, 191.124, 284.611)), (' A  66  ARG  NH2', ' A  86  ASP  OD2', -0.422, (227.023, 157.717, 287.282)), (' H  51  ILE HG12', ' H  57  THR HG22', -0.421, (159.335, 211.66, 277.623)), (' B 159  VAL HG13', ' B 160  TYR  HD1', -0.421, (157.286, 164.978, 236.299)), (' B 598  ILE HG23', ' B 664  ILE HG21', -0.42, (190.627, 173.929, 184.432)), (' C 395  VAL HG11', ' C 524  VAL  HB ', -0.42, (214.233, 240.318, 238.227)), (' B 727  LEU HD11', ' B1028  LYS  HD2', -0.418, (192.341, 199.05, 168.797)), (' E 442  ASP  OD2', ' E 509  ARG  NH2', -0.418, (152.198, 198.427, 257.408)), (' E1086  LYS  HB2', ' E1086  LYS  HE3', -0.418, (186.833, 198.009, 124.39)), (' C 407  VAL HG21', ' C 508  TYR  HD2', -0.418, (223.965, 234.998, 259.3)), (' E 415  THR  OG1', ' E 416  GLY  N  ', -0.418, (175.888, 196.903, 264.606)), (' B1135  ASN  CG ', ' B1136  THR  H  ', -0.418, (206.304, 183.217, 125.412)), (' E 329  PHE  O  ', ' E 580  GLN  NE2', -0.418, (158.007, 202.783, 221.93)), (' X  48  VAL HG13', ' X  64  VAL HG21', -0.416, (162.115, 224.5, 260.182)), (' C 357  ARG HH22', ' C 395  VAL  HB ', -0.416, (211.11, 240.817, 239.096)), (' E 567  ARG  HA ', ' E 573  THR  HA ', -0.415, (171.371, 197.522, 206.546)), (' E1104  VAL HG23', ' E1115  ILE HG12', -0.415, (190.078, 209.752, 131.026)), (' B 324  GLU  H  ', ' B 539  VAL HG23', -0.415, (208.456, 165.757, 214.543)), (' C 645  THR  OG1', ' C 646  ARG  N  ', -0.415, (231.133, 220.796, 185.392)), (' E 597  VAL HG22', ' E 610  VAL HG22', -0.414, (181.438, 228.31, 193.889)), (' C 542  ASN  HA ', ' C 547  THR HG22', -0.414, (222.258, 229.909, 218.78)), (' B1046  GLY  HA2', ' C 890  ALA  HA ', -0.413, (195.656, 188.957, 156.523)), (' W  48  VAL HG13', ' W  64  VAL HG21', -0.412, (200.843, 159.199, 261.053)), (' B 340  GLU  O  ', ' B 344  ALA  CB ', -0.412, (233.147, 164.317, 251.094)), (' D  40  ALA  HB3', ' D  43  LYS  HB2', -0.412, (218.993, 253.947, 280.805)), (' H  40  ALA  HB3', ' H  43  LYS  HB2', -0.412, (149.603, 191.129, 280.826)), (' E 389  ASP  N  ', ' E 389  ASP  OD1', -0.412, (167.443, 205.06, 233.847)), (' A  67  PHE  HB3', ' A  80  LEU HD11', -0.412, (219.46, 160.994, 284.371)), (' B 552  LEU HD13', ' B 587  ILE HG22', -0.411, (217.741, 170.127, 208.949)), (' E 328  ARG  HA ', ' E 328  ARG  HD2', -0.411, (160.076, 205.58, 220.249)), (' B 344  ALA  HB3', ' B 347  PHE  HE1', -0.411, (232.318, 164.932, 253.028)), (' C 310  LYS  NZ ', ' C 663  ASP  OD1', -0.41, (233.012, 202.276, 178.063)), (' E 294  ASP  N  ', ' E 294  ASP  OD1', -0.41, (184.412, 235.949, 198.776)), (' E 289  VAL  HB ', ' E 297  SER  HB3', -0.409, (189.673, 235.943, 198.777)), (' B 456  PHE  HB2', ' B 491  PRO  HB3', -0.409, (230.455, 183.531, 272.553)), (' B1115  ILE HG22', ' B1137  VAL HG13', -0.408, (205.273, 190.06, 126.492)), (' E 574  ASP  O  ', ' E 587  ILE  N  ', -0.408, (166.018, 202.301, 205.58)), (' C1013  ILE HG21', ' E1012  LEU  HG ', -0.408, (207.245, 202.462, 188.768)), (' A  47  TRP  HE1', ' A  50  ALA  HB2', -0.406, (220.016, 166.32, 276.09)), (' B 356  LYS  H  ', ' B 356  LYS  HG2', -0.406, (232.75, 176.905, 249.539)), (' A  51  ILE HD11', ' A  69  ILE HG12', -0.406, (213.689, 165.391, 281.553)), (' W  87  LYS  HB3', ' W  87  LYS  HE2', -0.405, (195.026, 151.312, 268.393)), (' B 825  LYS  HD2', ' B 945  LEU HD23', -0.404, (178.427, 191.325, 174.389)), (' E 405  ASP  N  ', ' E 405  ASP  OD1', -0.404, (163.941, 202.731, 264.958)), (' H  51  ILE HD11', ' H  69  ILE HG12', -0.404, (159.745, 210.091, 280.6)), (' B 787  GLN  OE1', ' E 703  ASN  ND2', -0.404, (180.764, 219.331, 157.36)), (' B 430  THR  OG1', ' B 515  PHE  O  ', -0.404, (220.314, 183.849, 243.722)), (' C 415  THR  OG1', ' C 416  GLY  N  ', -0.403, (210.888, 228.184, 264.561)), (' B 906  PHE  HB3', ' B 911  VAL HG23', -0.403, (191.071, 195.481, 145.003)), (' Y  48  VAL HG13', ' Y  64  VAL HG21', -0.403, (241.563, 225.733, 260.136)), (' B 767  LEU  HA ', ' B 767  LEU HD23', -0.402, (192.227, 209.494, 191.346)), (' C 667  GLY  HA2', ' E 864  LEU  HA ', -0.402, (225.039, 214.476, 182.028)), (' B 299  THR  HA ', ' B 302  THR HG22', -0.402, (186.856, 178.907, 195.408)), (' E 229  LEU  HB3', ' E 231  ILE HG12', -0.401, (199.629, 244.116, 230.133)), (' E 401  VAL  HA ', ' E 509  ARG  HA ', -0.401, (158.422, 198.43, 257.248)), (' C 187  LYS  HA ', ' C 187  LYS  HD2', -0.4, (261.428, 178.431, 207.551)), (' C 613  GLN  HA ', ' C 648  GLY  HA3', -0.4, (229.559, 217.161, 191.171))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
