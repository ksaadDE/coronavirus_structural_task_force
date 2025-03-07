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
data['rama'] = [('A', '  32 ', 'PHE', 0.017937019962200505, (163.172, 165.54700000000005, 204.56600000000003))]
data['omega'] = [('B', ' 157 ', 'PHE', None, (191.0120000000001, 254.752, 240.841)), ('B', ' 158 ', 'ARG', None, (189.561, 256.7340000000001, 238.142)), ('C', ' 157 ', 'PHE', None, (249.97900000000007, 175.708, 243.01900000000003)), ('C', ' 158 ', 'ARG', None, (252.44400000000005, 175.86, 240.334))]
data['rota'] = []
data['cbeta'] = []
data['probe'] = [(' A  33  THR  OG1', ' A 219  GLY  O  ', -0.783, (160.702, 170.321, 203.699)), (' A 978  ASN  O  ', ' A 982  SER  OG ', -0.769, (177.966, 202.985, 221.131)), (' B 813  SER  OG ', ' B 868  GLU  OE2', -0.765, (221.391, 218.289, 170.919)), (' B  14  GLN  O  ', ' B 158  ARG  NH1', -0.752, (183.691, 255.819, 238.788)), (' A 758  SER  OG ', ' B 965  GLN  NE2', -0.75, (198.575, 211.358, 200.864)), (' B  96  GLU  OE1', ' B 190  ARG  NH2', -0.737, (195.084, 253.785, 219.425)), (' C 813  SER  OG ', ' C 868  GLU  OE2', -0.721, (204.556, 165.068, 171.666)), (' A 674  TYR  OH ', ' A 690  GLN  OE1', -0.721, (170.494, 164.392, 182.053)), (' A1031  GLU  OE2', ' B1039  ARG  NE ', -0.72, (195.646, 199.015, 159.716)), (' A 310  LYS  NZ ', ' A 663  ASP  OD2', -0.712, (176.688, 171.339, 177.874)), (' B 561  PRO  O  ', ' B 577  ARG  NH1', -0.697, (157.786, 192.994, 219.526)), (' C 310  LYS  NZ ', ' C 663  ASP  OD2', -0.693, (229.819, 191.958, 177.772)), (' A  14  GLN  N  ', ' A 255  SER  HG ', -0.69, (148.695, 157.281, 239.757)), (' B 883  THR  O  ', ' B 901  GLN  NE2', -0.69, (214.224, 207.965, 147.877)), (' C  96  GLU  OE1', ' C 190  ARG  NH2', -0.67, (247.344, 171.112, 221.524)), (' A 717  ASN  OD1', ' A 718  PHE  N  ', -0.664, (179.691, 180.995, 144.065)), (' A 368  LEU  O  ', ' A 372  ALA  N  ', -0.662, (202.528, 160.369, 248.454)), (' B 645  THR  OG1', ' B 648  GLY  O  ', -0.649, (171.168, 217.625, 186.173)), (' C 645  THR  OG1', ' C 648  GLY  O  ', -0.648, (229.609, 208.81, 186.732)), (' B 559  PHE  CE2', ' B 584  ILE HG21', -0.635, (159.705, 197.635, 211.922)), (' C1135  ASN  OD1', ' C1136  THR  N  ', -0.632, (213.756, 206.095, 122.1)), (' B 344  ALA  HB3', ' B 347  PHE  HE1', -0.63, (173.492, 190.539, 251.414)), (' C  32  PHE  HD2', ' C  33  THR HG23', -0.621, (239.989, 181.142, 202.361)), (' C 951  VAL  O  ', ' C 955  ASN  ND2', -0.613, (205.741, 182.601, 184.464)), (' A  32  PHE  CD2', ' A  33  THR HG23', -0.611, (163.071, 168.148, 201.928)), (' A 318  PHE  N  ', ' A 593  GLY  O  ', -0.609, (191.221, 168.58, 199.302)), (' A 287  ASP  OD1', ' A 288  ALA  N  ', -0.607, (165.797, 176.426, 201.517)), (' B1135  ASN  OD1', ' B1136  THR  N  ', -0.607, (180.167, 205.071, 121.58)), (' B 916  LEU  O  ', ' B 920  GLN  N  ', -0.603, (204.097, 217.686, 139.103)), (' A 122  ASN  ND2', ' A 124  THR  OG1', -0.597, (144.766, 174.964, 233.481)), (' C 287  ASP  OD1', ' C 288  ALA  N  ', -0.596, (231.208, 179.244, 201.99)), (' B 340  GLU  O  ', ' B 344  ALA  HB2', -0.591, (170.985, 192.158, 250.117)), (' B1091  ARG  NE ', ' B1118  ASP  O  ', -0.59, (193.29, 198.402, 129.077)), (' B 310  LYS  NZ ', ' B 663  ASP  OD2', -0.589, (185.467, 227.339, 176.984)), (' A 122  ASN  OD1', ' A 125  ASN  N  ', -0.586, (146.099, 174.992, 231.446)), (' B 287  ASP  OD1', ' B 288  ALA  N  ', -0.585, (195.469, 235.315, 200.776)), (' B 109  THR  OG1', ' B 111  ASP  OD1', -0.581, (183.335, 240.072, 239.358)), (' C 457  ARG  NH1', ' C 459  SER  OG ', -0.579, (179.463, 220.624, 237.778)), (' C 157  PHE  HB2', ' C 158  ARG  HA ', -0.575, (252.015, 177.945, 241.455)), (' A 965  GLN  NE2', ' C 758  SER  OG ', -0.575, (184.601, 190.631, 201.674)), (' A1135  ASN  OD1', ' A1136  THR  N  ', -0.567, (198.63, 175.742, 121.876)), (' A 336  CYS  N  ', ' A 362  VAL  O  ', -0.565, (217.372, 162.694, 240.392)), (' A 802  PHE  HE2', ' A 882  ILE HG23', -0.563, (173.784, 200.47, 151.371)), (' A  37  TYR  OH ', ' A 195  LYS  NZ ', -0.562, (169.397, 175.771, 217.631)), (' A 968  SER  OG ', ' C 755  GLN  O  ', -0.561, (185.605, 190.801, 208.84)), (' B 365  TYR  O  ', ' B 369  TYR  N  ', -0.559, (177.307, 204.643, 240.763)), (' C 916  LEU  O  ', ' C 920  GLN  N  ', -0.554, (212.998, 179.633, 139.806)), (' B 543  PHE  CD2', ' B 576  VAL HG11', -0.54, (164.443, 203.619, 216.849)), (' C  32  PHE  CD2', ' C  33  THR HG23', -0.539, (239.861, 181.762, 202.096)), (' B 559  PHE  HE2', ' B 584  ILE HG21', -0.538, (159.8, 197.456, 211.417)), (' A 742  ILE  O  ', ' A1000  ARG  NH1', -0.536, (182.593, 203.002, 208.908)), (' B  67  VAL HG23', ' B  79  PHE  HD1', -0.534, (183.979, 257.835, 223.205)), (' A 341  VAL HG23', ' A 342  PHE  H  ', -0.529, (214.536, 163.856, 252.014)), (' A 425  LEU HD23', ' A 429  PHE  CD2', -0.528, (208.416, 178.325, 251.715)), (' C 122  ASN  ND2', ' C 124  THR  OG1', -0.527, (242.055, 163.231, 233.616)), (' A 701  ALA  O  ', ' C 787  GLN  NE2', -0.526, (189.471, 167.898, 159.648)), (' C 108  THR  OG1', ' C 234  ASN  O  ', -0.525, (235.285, 189.247, 234.872)), (' C 340  GLU  O  ', ' C 344  ALA  HB2', -0.524, (206.534, 223.617, 250.362)), (' A  43  PHE  CB ', ' B 563  GLN HE22', -0.524, (163.286, 192.599, 211.541)), (' A 395  VAL HG13', ' A 515  PHE  CE1', -0.521, (213.494, 172.01, 244.661)), (' A 884  SER  OG ', ' B 707  TYR  OH ', -0.52, (178.076, 209.784, 150.726)), (' C 344  ALA  HB3', ' C 347  PHE  HE1', -0.518, (204.183, 222.465, 251.379)), (' B 391  CYS  HA ', ' B 525  CYS  HB3', -0.516, (170.397, 200.552, 230.385)), (' B  34  ARG  NH2', ' B 218  GLN  O  ', -0.513, (194.35, 247.816, 205.236)), (' A 102  ARG HH21', ' A 179  LEU HD21', -0.512, (144.888, 166.793, 227.013)), (' B 188  ASN  OD1', ' B 207  HIS  NE2', -0.511, (201.03, 253.714, 215.498)), (' B  83  VAL HG12', ' B 237  ARG  HB3', -0.508, (180.414, 242.053, 228.754)), (' A 341  VAL HG23', ' A 342  PHE  N  ', -0.502, (214.536, 163.992, 252.502)), (' B 725  GLU  OE2', ' B1028  LYS  NZ ', -0.5, (199.466, 207.063, 165.286)), (' B1094  VAL HG13', ' B1107  ARG  HE ', -0.5, (185.937, 203.406, 138.545)), (' B 405  ASP  O  ', ' B 408  ARG  NH1', -0.5, (195.91, 188.051, 247.968)), (' B1056  ALA  HB2', ' B1061  VAL HG23', -0.498, (207.586, 214.961, 169.693)), (' C 474  GLN  NE2', ' C 478  LYS  O  ', -0.496, (164.505, 223.033, 247.789)), (' B 864  LEU HD13', ' C 665  PRO  HB2', -0.496, (222.817, 201.87, 180.04)), (' A 118  LEU  HG ', ' A 120  VAL HG23', -0.495, (155.703, 169.129, 235.116)), (' B  99  ASN  OD1', ' B 190  ARG  NH2', -0.495, (196.018, 253.961, 220.714)), (' B 951  VAL  O  ', ' B 955  ASN  ND2', -0.494, (205.694, 211.264, 184.175)), (' A  32  PHE  CE2', ' A  33  THR HG23', -0.49, (163.298, 168.927, 201.641)), (' C  67  VAL HG23', ' C  79  PHE  HD1', -0.489, (255.629, 179.02, 225.664)), (' B 555  SER  OG ', ' B 586  ASP  OD1', -0.487, (159.794, 200.524, 209.06)), (' C 324  GLU  H  ', ' C 539  VAL HG12', -0.487, (230.052, 215.239, 214.167)), (' B  65  PHE  HE2', ' B  84  LEU HD11', -0.485, (182.261, 246.752, 221.565)), (' B 725  GLU  OE1', ' B1064  HIS  NE2', -0.483, (200.601, 209.805, 162.997)), (' B 157  PHE  HB2', ' B 158  ARG  HA ', -0.483, (188.009, 255.625, 239.43)), (' C 125  ASN  ND2', ' C 172  SER  O  ', -0.483, (235.042, 163.449, 232.168)), (' B 905  ARG  NE ', ' B1050  MET  SD ', -0.481, (207.213, 207.359, 150.335)), (' A1094  VAL HG12', ' C 904  TYR  OH ', -0.48, (197.788, 181.805, 138.833)), (' B 631  PRO  O  ', ' B 634  ARG  NH1', -0.479, (174.898, 224.874, 203.053)), (' C 543  PHE  CE2', ' C 576  VAL HG11', -0.478, (220.01, 223.586, 215.607)), (' C1082  CYS  N  ', ' C1133  VAL  O  ', -0.476, (212.041, 211.641, 125.778)), (' B  43  PHE  CB ', ' C 563  GLN HE22', -0.472, (210.348, 228.895, 210.847)), (' A 244  LEU  HB3', ' A 258  TRP  HB3', -0.471, (144.752, 155.768, 230.67)), (' A 811  LYS  NZ ', ' A 820  ASP  OD2', -0.468, (162.469, 198.824, 166.663)), (' A 864  LEU HD13', ' B 665  PRO  HB2', -0.465, (180.309, 216.001, 179.628)), (' A  18  LEU HD11', ' A 244  LEU HD22', -0.465, (148.15, 154.609, 230.796)), (' A 563  GLN HE22', ' C  43  PHE  N  ', -0.462, (218.204, 170.725, 212.626)), (' C 610  VAL HG21', ' C 633  TRP  CH2', -0.46, (232.77, 199.847, 196.001)), (' C 543  PHE  CD2', ' C 576  VAL HG11', -0.459, (219.841, 223.278, 216.276)), (' B 598  ILE HG23', ' B 664  ILE HG21', -0.459, (182.309, 223.09, 183.67)), (' A 105  ILE HD11', ' A 241  LEU HD21', -0.458, (156.642, 163.292, 233.906)), (' B 318  PHE  O  ', ' B 319  ARG  NH1', -0.457, (177.805, 215.235, 203.075)), (' C 561  PRO  O  ', ' C 577  ARG  NH1', -0.456, (213.762, 234.659, 218.547)), (' C 108  THR  O  ', ' C 237  ARG  NH2', -0.454, (241.538, 191.203, 235.268)), (' A 951  VAL  O  ', ' A 955  ASN  ND2', -0.454, (180.834, 196.418, 184.797)), (' A 131  CYS  HB2', ' A 133  PHE  CE1', -0.453, (159.776, 170.325, 241.622)), (' A 737  ASP  OD2', ' B 317  ASN  ND2', -0.452, (181.228, 212.476, 200.169)), (' C1028  LYS  O  ', ' C1032  CYS  N  ', -0.452, (200.183, 186.381, 160.418)), (' A 802  PHE  CE2', ' A 882  ILE HG23', -0.451, (173.468, 200.538, 151.623)), (' B 861  LEU HD23', ' C 613  GLN HE22', -0.45, (219.342, 205.989, 189.565)), (' C 391  CYS  HA ', ' C 525  CYS  HB3', -0.45, (213.721, 219.94, 230.126)), (' A 244  LEU  HG ', ' A 260  ALA  HB2', -0.45, (146.471, 156.147, 227.095)), (' B  17  ASN  OD1', ' B 158  ARG  NH2', -0.449, (180.782, 255.684, 235.882)), (' A  43  PHE  HB3', ' B 563  GLN HE22', -0.448, (163.537, 192.607, 211.541)), (' A 613  GLN HE22', ' C 861  LEU HD23', -0.448, (194.578, 173.166, 189.758)), (' A 880  GLY  O  ', ' A 884  SER  N  ', -0.448, (178.464, 206.384, 151.318)), (' A 897  PRO  HD3', ' B 711  SER  O  ', -0.447, (177.59, 207.323, 140.582)), (' A 869  MET  CE ', ' B 699  LEU HD21', -0.447, (176.251, 214.417, 171.087)), (' B 543  PHE  CE2', ' B 576  VAL HG11', -0.447, (164.314, 203.871, 216.42)), (' A 100  ILE HD12', ' A 263  ALA  HB3', -0.446, (148.749, 159.133, 221.084)), (' C 109  THR  OG1', ' C 111  ASP  OD1', -0.445, (240.522, 189.11, 240.738)), (' B 559  PHE  CD2', ' B 584  ILE HG21', -0.445, (159.79, 196.723, 212.123)), (' A 699  LEU HD12', ' C 872  GLN  OE1', -0.444, (194.937, 166.38, 167.54)), (' A 563  GLN HE21', ' A 565  PHE  C  ', -0.444, (216.297, 169.744, 214.457)), (' B 787  GLN  NE2', ' C 701  ALA  O  ', -0.443, (226.343, 203.805, 159.678)), (' C 986  PRO  N  ', ' C 987  PRO  HD2', -0.442, (194.448, 186.031, 227.105)), (' B 986  PRO  N  ', ' B 987  PRO  HD2', -0.439, (208.883, 200.638, 227.105)), (' B 856  LYS  HE2', ' C 570  ALA  HB1', -0.439, (210.508, 216.215, 203.981)), (' A 885  GLY  O  ', ' A 888  PHE  CD2', -0.439, (182.788, 206.59, 152.697)), (' A 984  LEU  O  ', ' B 386  LYS  NZ ', -0.435, (182.874, 205.329, 225.456)), (' B 872  GLN  OE1', ' C 699  LEU HD12', -0.435, (224.896, 209.018, 167.707)), (' B 646  ARG  HB3', ' B 668  ALA  HB2', -0.435, (171.449, 212.772, 181.939)), (' A1080  ALA  HB2', ' A1089  PHE  CE1', -0.434, (206.461, 179.379, 131.804)), (' A 563  GLN HE22', ' C  43  PHE  CB ', -0.434, (218.463, 170.129, 212.152)), (' A  53  ASP  OD1', ' A  54  LEU  N  ', -0.431, (173.082, 175.549, 216.457)), (' B 406  GLU  HB3', ' B 418  ILE HD12', -0.431, (191.764, 184.362, 247.245)), (' A 105  ILE  CD1', ' A 241  LEU HD21', -0.43, (156.845, 163.06, 233.662)), (' A 986  PRO  N  ', ' A 987  PRO  HD2', -0.427, (188.483, 206.631, 226.307)), (' C 350  VAL HG23', ' C 351  TYR  N  ', -0.425, (188.728, 218.695, 247.789)), (' A 982  SER  O  ', ' B 386  LYS  HD3', -0.425, (179.561, 204.378, 226.0)), (' A 395  VAL HG13', ' A 515  PHE  HE1', -0.425, (213.525, 171.712, 245.403)), (' A 342  PHE  CE1', ' A 511  VAL HG11', -0.424, (212.131, 166.575, 251.692)), (' B 374  PHE  HA ', ' B 436  TRP  HD1', -0.424, (181.94, 199.851, 251.005)), (' A 787  GLN HE21', ' B 703  ASN  HB3', -0.42, (178.314, 216.607, 154.937)), (' A 438  SER  HB3', ' A 442  ASP  HB2', -0.419, (211.721, 161.78, 264.272)), (' B 802  PHE  CE2', ' B 882  ILE HG23', -0.418, (213.25, 215.282, 151.452)), (' B 452  LEU  CB ', ' B 492  LEU HD11', -0.418, (183.661, 176.486, 253.671)), (' A 570  ALA  HB2', ' C 856  LYS  HE2', -0.418, (208.012, 176.099, 203.785)), (' C 645  THR  N  ', ' C 648  GLY  O  ', -0.416, (230.111, 210.015, 186.514)), (' B 324  GLU  H  ', ' B 539  VAL HG12', -0.416, (166.095, 216.558, 215.547)), (' A 887  THR HG21', ' A 894  LEU HD12', -0.416, (184.829, 209.419, 146.642)), (' C 320  VAL  N  ', ' C 591  SER  OG ', -0.414, (225.755, 208.958, 206.024)), (' B 194  PHE  HE1', ' B 203  ILE HG23', -0.414, (196.077, 241.766, 222.124)), (' B  99  ASN  OD1', ' B 190  ARG  NH1', -0.413, (197.075, 253.222, 221.334)), (' B 543  PHE  HD2', ' B 576  VAL HG11', -0.413, (165.006, 202.965, 217.119)), (' B 744  GLY  O  ', ' B 745  ASP  HB2', -0.413, (216.971, 209.711, 210.699)), (' A 433  VAL HG23', ' A 512  VAL HG22', -0.412, (209.768, 173.485, 255.194)), (' B 372  ALA  N  ', ' C 417  ASN  OD1', -0.412, (181.656, 207.638, 246.834)), (' C 744  GLY  O  ', ' C 745  ASP  HB2', -0.41, (199.319, 174.565, 211.491)), (' A 869  MET  HE3', ' B 699  LEU HD21', -0.408, (176.063, 214.616, 170.968)), (' B 617  CYS  HA ', ' B 620  VAL HG12', -0.408, (166.826, 220.297, 195.3)), (' C 454  ARG  NH1', ' C 469  SER  O  ', -0.408, (181.066, 224.357, 248.099)), (' A 121  ASN  OD1', ' A 123  ALA  N  ', -0.408, (146.61, 172.542, 229.889)), (' C 102  ARG  NH2', ' C 121  ASN  O  ', -0.408, (246.892, 167.78, 231.018)), (' B 376  THR HG22', ' B 435  ALA  HB3', -0.408, (186.695, 196.563, 246.646)), (' A 858  LEU HD21', ' A 959  LEU HD22', -0.408, (178.693, 200.8, 193.976)), (' C 712  ILE  O  ', ' C1075  PHE  N  ', -0.408, (221.725, 202.876, 138.966)), (' B 200  TYR  OH ', ' C 516  GLU  OE2', -0.407, (201.231, 225.752, 230.038)), (' A1056  ALA  HB2', ' A1061  VAL HG23', -0.406, (176.267, 196.139, 170.281)), (' A  37  TYR  OH ', ' A  53  ASP  OD2', -0.406, (170.095, 177.1, 216.86)), (' A 102  ARG  NH2', ' A 179  LEU HD21', -0.406, (144.883, 167.247, 227.099)), (' A 738  CYS  HB3', ' A 742  ILE HD12', -0.405, (186.959, 207.264, 203.955)), (' B  83  VAL HG12', ' B 237  ARG  CB ', -0.405, (180.803, 241.61, 229.024)), (' C 407  VAL HG13', ' C 408  ARG  N  ', -0.404, (195.165, 206.397, 246.684)), (' B 154  GLU  N  ', ' B 154  GLU  OE1', -0.403, (198.127, 257.93, 234.046)), (' A 790  LYS  NZ ', ' B 702  GLU  OE2', -0.403, (169.162, 215.999, 158.53)), (' C 439  ASN  O  ', ' C 443  SER  OG ', -0.402, (199.35, 210.792, 262.233)), (' A 425  LEU HD23', ' A 429  PHE  CE2', -0.402, (208.664, 177.891, 251.802)), (' C 555  SER  OG ', ' C 586  ASP  OD1', -0.402, (219.606, 228.688, 207.981)), (' C  65  PHE  HE2', ' C  84  LEU HD11', -0.401, (247.287, 185.945, 223.462)), (' A 645  THR  OG1', ' A 648  GLY  O  ', -0.401, (192.254, 163.773, 187.095)), (' A 193  VAL  O  ', ' A 203  ILE  HA ', -0.401, (162.161, 174.623, 222.247)), (' B 454  ARG  NH2', ' B 469  SER  O  ', -0.4, (181.356, 170.793, 248.513)), (' A 445  VAL  O  ', ' A 446  SER  HB3', -0.4, (213.668, 159.076, 277.148))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
