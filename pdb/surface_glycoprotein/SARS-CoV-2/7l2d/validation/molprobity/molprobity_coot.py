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
data['omega'] = []
data['rota'] = [('A', ' 569 ', 'ILE', 0.25244135105893234, (189.518, 197.434, 196.759)), ('H', '  34 ', 'MET', 0.19682526185602628, (244.398, 141.257, 154.324)), ('H', '  57 ', 'THR', 0.2557414232967269, (251.844, 145.005, 151.061)), ('L', '  50 ', 'ASP', 0.2804334588447819, (250.55000000000004, 133.857, 169.434)), ('L', '  51 ', 'VAL', 0.16544395993185995, (251.592, 130.241, 170.384)), ('B', ' 245 ', 'HIS', 0.29184544480786606, (146.28600000000003, 213.44799999999998, 170.251)), ('B', ' 602 ', 'THR', 0.2938516494391624, (177.211, 212.583, 212.466)), ('C', '  17 ', 'ASN', 0.18780031683423462, (253.084, 248.97799999999992, 165.556)), ('C', ' 365 ', 'TYR', 0.06766002945477971, (231.589, 206.232, 162.802)), ('C', ' 471 ', 'GLU', 0.24891122031836654, (208.80800000000008, 172.935, 155.218))]
data['cbeta'] = [('A', ' 122 ', 'ASN', ' ', 0.257262250842074, (237.91400000000002, 165.001, 168.709)), ('A', ' 149 ', 'ASN', ' ', 0.2684245282537238, (248.07000000000002, 158.083, 158.931)), ('B', ' 145 ', 'TYR', ' ', 0.2856991106427677, (142.545, 208.73099999999997, 168.705)), ('C', '  59 ', 'PHE', ' ', 0.2903237344882464, (239.58800000000014, 235.83699999999996, 198.65599999999998)), ('C', ' 280 ', 'ASN', ' ', 0.2524289101965708, (217.22400000000016, 243.175, 199.627))]
data['probe'] = [(' L  27  SER  HA ', ' L  28  GLY  HA3', -0.64, (264.652, 131.331, 164.557)), (' C 145  TYR  HB2', ' C 152  TRP  HE3', -0.632, (241.55, 267.551, 169.511)), (' B 571  ASP  HB2', ' C1000  ARG  NH2', -0.629, (206.317, 224.848, 193.384)), (' B 806  LEU HD12', ' B 807  PRO  HD2', -0.623, (188.997, 189.44, 241.791)), (' C 902  MET  HE1', ' C1050  MET  HE1', -0.62, (207.388, 226.2, 251.395)), (' A  96  GLU  OE2', ' A 264  ALA  HB3', -0.616, (228.682, 156.538, 184.722)), (' B 720  ILE HG13', ' B 923  ILE HG23', -0.615, (186.582, 204.957, 253.869)), (' C 146  HIS  HB2', ' C 149  ASN  HB3', -0.61, (240.874, 271.096, 166.127)), (' B 143  VAL  HA ', ' B 154  GLU  O  ', -0.601, (149.805, 209.653, 164.842)), (' B 145  TYR  HA ', ' B 152  TRP  HB2', -0.599, (143.263, 207.095, 167.297)), (' C 145  TYR  HB2', ' C 152  TRP  CE3', -0.596, (240.65, 267.453, 169.868)), (' H  96  ILE HD12', ' H  99  ILE HG22', -0.592, (242.887, 141.183, 166.537)), (' A 666  ILE HD11', ' A 672  ALA  HB2', -0.591, (206.754, 178.139, 219.232)), (' C 715  PRO  HA ', ' C1072  GLU  HA ', -0.59, (229.08, 219.655, 258.607)), (' B 418  ILE  HA ', ' B 422  ASN  HB2', -0.584, (225.907, 219.815, 159.555)), (' B 729  VAL HG21', ' B 781  VAL HG11', -0.583, (199.182, 197.905, 229.346)), (' C 431  GLY  HA2', ' C 515  PHE  HD2', -0.58, (223.626, 198.276, 170.508)), (' C 144  TYR  HE1', ' C 258  TRP  CH2', -0.579, (247.162, 258.659, 165.12)), (' B 121  ASN  ND2', ' B 175  PHE  H  ', -0.578, (161.218, 203.8, 173.7)), (' A1012  LEU HD21', ' C1012  LEU HD22', -0.577, (209.619, 209.406, 214.445)), (' C 393  THR  HA ', ' C 522  ALA  HA ', -0.571, (234.724, 194.594, 175.147)), (' C 903  ALA  HB1', ' C 913  GLN  HG2', -0.57, (208.869, 222.682, 261.402)), (' L  80  ALA  HA ', ' L 106  VAL HG21', -0.569, (237.245, 110.941, 164.643)), (' B 244  LEU HD13', ' B 258  TRP  HB3', -0.568, (148.619, 219.432, 169.233)), (' C 802  PHE  HB3', ' C 806  LEU HD23', -0.566, (205.706, 235.67, 245.73)), (' H 100I TYR  HD2', ' L  32  TYR  CG ', -0.566, (253.588, 137.552, 165.762)), (' C 216  LEU HD12', ' C 217  PRO  HD2', -0.563, (237.252, 247.245, 192.112)), (' C 720  ILE HG13', ' C 923  ILE HG23', -0.562, (216.001, 229.292, 254.126)), (' A  67  ALA  HB3', ' A 263  ALA  HB3', -0.562, (226.715, 155.765, 178.63)), (' H  82C LEU HD12', ' H  86  ASP  HB2', -0.561, (249.759, 131.014, 136.846)), (' C1028  LYS  NZ ', ' C1042  PHE  O  ', -0.559, (215.433, 217.572, 238.138)), (' B 119  ILE HG12', ' B 128  ILE HG12', -0.556, (167.753, 209.101, 169.752)), (' H  12  LYS  NZ ', ' H  17  SER  O  ', -0.553, (244.014, 136.089, 132.606)), (' A  36  VAL HG21', ' A 220  PHE  CZ ', -0.551, (227.046, 176.858, 194.63)), (' L  33  VAL  HA ', ' L  89  SER  O  ', -0.549, (252.916, 131.398, 163.646)), (' B 393  THR HG21', ' B 520  ALA  HB3', -0.549, (212.605, 237.012, 177.788)), (' H  37  VAL HG21', ' H 103  TRP  HZ3', -0.549, (244.45, 131.352, 153.633)), (' B 626  ALA  O  ', ' B 634  ARG  NH1', -0.546, (177.942, 233.745, 196.954)), (' A 126  VAL HG21', ' A 175  PHE  CE2', -0.545, (234.079, 172.004, 173.051)), (' L  48  ILE HD12', ' L  51  VAL  O  ', -0.544, (249.65, 127.689, 169.861)), (' A  89  GLY  HA3', ' A 270  LEU HD12', -0.543, (218.657, 174.63, 181.419)), (' A 150  LYS  HZ1', ' H  53  GLU  HA ', -0.542, (253.082, 148.12, 162.388)), (' L  13  GLY  HA3', ' L  19  ILE HD11', -0.541, (245.975, 109.511, 167.63)), (' B 715  PRO  HA ', ' B1072  GLU  HA ', -0.541, (187.904, 220.465, 258.068)), (' A1129  VAL HG23', ' B 917  TYR  HB3', -0.54, (188.88, 199.216, 266.214)), (' A 626  ALA  HA ', ' A 629  LEU HD12', -0.539, (201.971, 173.181, 199.133)), (' A 745  ASP  HB2', ' A 978  ASN HD21', -0.537, (232.013, 206.456, 190.025)), (' H  99  ILE HG23', ' H 100H TYR  HB2', -0.536, (245.52, 142.187, 166.091)), (' H   5  VAL  HB ', ' H  23  LYS  HB3', -0.533, (232.288, 139.767, 148.111)), (' A 884  SER  OG ', ' A 887  THR  OG1', -0.529, (227.278, 211.844, 251.504)), (' A 453  TYR  HB3', ' A 495  TYR  HE1', -0.528, (191.323, 217.552, 152.619)), (' H  36  TRP  N  ', ' H  49  GLY  O  ', -0.528, (247.371, 137.823, 150.933)), (' A 756  TYR  HE1', ' C 970  PHE  HA ', -0.528, (214.487, 216.652, 192.032)), (' A  64  TRP  HE1', ' A 264  ALA  HB1', -0.527, (226.105, 156.724, 185.768)), (' A 144  TYR  O  ', ' A 153  MET  N  ', -0.527, (240.566, 155.288, 164.233)), (' C 130  VAL HG22', ' C 168  PHE  HB3', -0.526, (227.23, 238.391, 164.256)), (' A  52  GLN  HG3', ' A 274  THR HG22', -0.524, (213.176, 184.285, 191.403)), (' A 740  MET  HE1', ' A 853  GLN  HA ', -0.522, (232.732, 205.181, 200.137)), (' C 984  LEU HD22', ' C 988  GLU  HG2', -0.521, (205.616, 217.386, 177.107)), (' C 811  LYS  HD2', ' C 812  PRO  HD2', -0.521, (200.465, 245.835, 233.036)), (' A 887  THR HG21', ' A 894  LEU  HB2', -0.52, (226.726, 213.218, 254.256)), (' C 715  PRO  HG3', ' C1069  PRO  HB3', -0.519, (225.206, 219.31, 255.888)), (' A 327  VAL HG23', ' A 530  SER  HA ', -0.517, (191.882, 179.688, 175.573)), (' B 740  MET  HE1', ' B 853  GLN  HG3', -0.516, (193.789, 188.777, 198.957)), (' A1125  ASN  OD1', ' A1126  CYS  N  ', -0.515, (186.126, 201.821, 274.944)), (' B 856  ASN HD22', ' B 966  LEU HD11', -0.515, (197.392, 197.234, 198.779)), (' B 666  ILE HD11', ' B 672  ALA  HB2', -0.513, (183.908, 225.099, 219.382)), (' B 570  ALA  HB3', ' C 967  SER  HA ', -0.513, (211.789, 226.915, 194.728)), (' A 720  ILE HG13', ' A 923  ILE HG23', -0.512, (222.01, 190.589, 254.43)), (' C 302  THR HG21', ' C 316  SER  H  ', -0.511, (227.313, 220.759, 203.783)), (' A 126  VAL HG21', ' A 175  PHE  HE2', -0.511, (233.845, 172.595, 173.266)), (' A 217  PRO  C  ', ' A 219  GLY  H  ', -0.511, (228.857, 167.209, 197.674)), (' L  78  LEU HD21', ' L 106  VAL HG22', -0.51, (240.473, 111.053, 165.729)), (' C  93  ALA  HB3', ' C 266  TYR  HB2', -0.509, (238.993, 244.928, 186.77)), (' B 571  ASP  HB2', ' C1000  ARG  CZ ', -0.509, (206.124, 224.487, 194.014)), (' C  24  LEU HD12', ' C  25  PRO  HD2', -0.505, (257.019, 245.162, 184.676)), (' B  15  CYS  HA ', ' B 158  ARG  HD2', -0.503, (153.223, 218.798, 160.329)), (' C 127  VAL HG21', ' X   1  NAG  H62', -0.501, (230.132, 251.807, 164.206)), (' B 193  VAL HG23', ' B 223  LEU HD22', -0.501, (170.224, 210.295, 184.662)), (' B 349  SER  OG ', ' B 452  LEU  O  ', -0.501, (225.521, 224.094, 152.767)), (' C 358  ILE  HB ', ' C 395  VAL HG23', -0.5, (231.408, 193.992, 166.435)), (' B 575  ALA  HA ', ' B 586  ASP  HA ', -0.499, (201.361, 238.979, 191.365)), (' B 403  ARG  NH2', ' C 373  SER  OG ', -0.498, (222.293, 210.427, 152.185)), (' A 418  ILE  HA ', ' A 422  ASN  HB2', -0.498, (192.105, 217.769, 159.03)), (' A 806  LEU HD12', ' A 807  PRO  HD2', -0.497, (235.205, 201.134, 242.502)), (' A 699  LEU HD13', ' B 872  GLN  HG2', -0.497, (195.995, 183.67, 235.077)), (' A 725  GLU  OE1', ' A1064  HIS  NE2', -0.496, (217.427, 196.732, 239.011)), (' C 525  CYS  SG ', ' C 526  GLY  N  ', -0.495, (236.558, 202.314, 172.03)), (' H   4  LEU HD11', ' H  94  THR HG22', -0.494, (239.027, 138.514, 155.727)), (' A 251  PRO  HA ', ' H  96  ILE HD11', -0.493, (241.112, 139.106, 166.265)), (' A 642  VAL HG22', ' A 651  ILE HG12', -0.492, (200.597, 170.923, 211.42)), (' A 699  LEU HD21', ' B 869  MET  HB3', -0.49, (197.773, 184.687, 231.651)), (' A 278  LYS  O  ', ' A 285  ILE  HA ', -0.49, (229.271, 182.944, 196.297)), (' A 854  LYS  HG3', ' C 569  ILE HD11', -0.489, (231.349, 197.047, 202.616)), (' C 418  ILE  HA ', ' C 422  ASN  HB2', -0.488, (210.192, 189.183, 159.354)), (' B 626  ALA  HB1', ' B 634  ARG  HG3', -0.488, (178.034, 233.443, 200.016)), (' A 778  THR HG22', ' A 865  LEU HD12', -0.488, (227.383, 209.239, 228.633)), (' C 119  ILE HG23', ' C 128  ILE HG12', -0.487, (230.078, 246.041, 171.271)), (' C  31  SER  HA ', ' C 216  LEU HD23', -0.486, (239.135, 242.224, 193.034)), (' C 111  ASP  OD2', ' C 113  LYS  NZ ', -0.486, (245.4, 232.322, 161.133)), (' H  49  GLY  HA2', ' H  59  TYR  HD1', -0.485, (251.234, 139.235, 148.591)), (' C 287  ASP  HB3', ' C 306  PHE  HE2', -0.484, (224.311, 238.442, 201.717)), (' A 726  ILE HD13', ' A 945  LEU HD23', -0.484, (223.178, 191.544, 230.423)), (' L  37  GLN  HB2', ' L  47  MET  SD ', -0.483, (240.702, 125.208, 163.715)), (' A 217  PRO  C  ', ' A 219  GLY  N  ', -0.482, (228.635, 167.327, 197.679)), (' C 145  TYR  HE1', ' C 245  HIS  HB3', -0.481, (245.83, 262.743, 172.007)), (' A 517  LEU  HB2', ' B 983  ARG HH11', -0.481, (192.854, 199.466, 178.358)), (' B 642  VAL HG22', ' B 651  ILE HG12', -0.479, (179.735, 234.284, 211.434)), (' A 102  ARG  NH2', ' A 122  ASN  HA ', -0.475, (237.845, 163.251, 170.61)), (' A 145  TYR  HA ', ' A 152  TRP  HA ', -0.474, (242.368, 154.138, 164.576)), (' L  92  THR HG23', ' L  94  SER  H  ', -0.474, (260.87, 137.094, 157.629)), (' C 129  LYS  HE2', ' C 133  PHE  HZ ', -0.474, (233.561, 244.35, 161.6)), (' L  47  MET  O  ', ' L  55  PRO  HD2', -0.474, (242.435, 129.351, 169.061)), (' L  30  TYR  HB3', ' L  32  TYR  HD2', -0.472, (256.752, 137.002, 166.961)), (' A 150  LYS  NZ ', ' H  53  GLU  HA ', -0.472, (252.768, 148.675, 162.394)), (' A 962  LEU HD13', ' A1007  TYR  HB2', -0.472, (218.806, 202.75, 205.304)), (' C 616  ASN  HB2', ' C 619  GLU  HG2', -0.469, (246.16, 209.294, 208.948)), (' A  84  LEU  O  ', ' A 238  PHE  N  ', -0.468, (216.082, 166.67, 174.047)), (' B 318  PHE  O  ', ' B 321  GLN  NE2', -0.468, (184.237, 222.448, 194.744)), (' C 273  ARG  HD3', ' C 321  GLN  OE1', -0.468, (234.122, 225.465, 192.411)), (' B 364  ASP  HA ', ' B 527  PRO  HG3', -0.467, (198.425, 233.029, 165.575)), (' L  83  GLU  HA ', ' L 104  VAL HG13', -0.466, (242.579, 114.534, 162.01)), (' C 401  VAL HG22', ' C 509  ARG  HG2', -0.463, (220.18, 195.612, 151.682)), (' C 725  GLU  OE1', ' C1064  HIS  NE2', -0.463, (214.745, 222.011, 238.684)), (' A 365 BTYR  O  ', ' A 368  LEU  HB2', -0.463, (196.548, 192.246, 159.337)), (' B 126  VAL  O  ', ' B 171  VAL  HA ', -0.462, (165.537, 202.559, 166.521)), (' A 365 ATYR  O  ', ' A 368  LEU  HB2', -0.461, (196.567, 192.247, 159.337)), (' A 442  ASP  O  ', ' A 448  ASN  ND2', -0.461, (191.318, 209.016, 143.073)), (' A  27  ALA  HB3', ' A  64  TRP  HB3', -0.46, (219.974, 156.035, 187.447)), (' B 733  LYS  HE3', ' B 771  ALA  HB1', -0.459, (201.798, 193.117, 217.292)), (' C  29  THR HG21', ' C 266  TYR  HE2', -0.459, (243.422, 245.249, 190.954)), (' C1106  GLN HE21', ' C1109  PHE  HB3', -0.459, (219.912, 219.507, 263.387)), (' A 401  VAL HG22', ' A 509  ARG  HG2', -0.457, (192.364, 206.674, 151.585)), (' C 187  LYS  HB3', ' C 210  ILE HG23', -0.456, (237.574, 255.336, 191.187)), (' B 627  ASP  N  ', ' B 627  ASP  OD1', -0.455, (181.344, 235.079, 195.897)), (' B1028  LYS  O  ', ' B1032  CYS  N  ', -0.454, (200.158, 202.951, 241.542)), (' C 117  LEU HD22', ' C 231  ILE HD13', -0.454, (230.518, 237.414, 170.668)), (' A 501  ASN  HB3', ' A 505  TYR  HB2', -0.454, (201.976, 215.089, 145.513)), (' C 673  SER  OG ', ' C 695  TYR  OH ', -0.453, (233.521, 224.56, 226.135)), (' C 105  ILE HG23', ' C 241  LEU HD11', -0.453, (239.272, 244.659, 169.557)), (' C 763  LEU HD21', ' C1005  GLN  HG2', -0.452, (204.745, 211.607, 204.979)), (' H  49  GLY  HA2', ' H  59  TYR  CD1', -0.452, (251.151, 139.413, 148.431)), (' B 962  LEU HD13', ' B1007  TYR  HB2', -0.451, (198.94, 203.619, 205.48)), (' A 770  ILE  O  ', ' A 774  GLN  HG2', -0.451, (220.481, 209.432, 219.33)), (' C 411  ALA  HB3', ' C 414  GLN  HG3', -0.45, (209.403, 198.6, 166.398)), (' A 303  LEU HD12', ' A 308  VAL HG22', -0.45, (217.072, 185.057, 208.824)), (' C 598  ILE HG23', ' C 664  ILE HG21', -0.45, (231.809, 223.208, 217.749)), (' C 551  VAL HG23', ' C 590  CYS  HA ', -0.449, (238.636, 211.737, 194.784)), (' A 106  PHE  HB3', ' A 235  ILE HD12', -0.449, (219.949, 172.496, 170.895)), (' C  29  THR HG21', ' C 266  TYR  CE2', -0.449, (243.465, 245.161, 190.717)), (' C 362  VAL  HA ', ' C 525  CYS  O  ', -0.449, (237.126, 201.117, 168.799)), (' A 890  ALA  HA ', ' C1046  GLY  HA2', -0.449, (222.354, 217.903, 247.797)), (' L  83  GLU  HB3', ' L 106  VAL HG23', -0.448, (240.033, 111.661, 163.009)), (' B 951  VAL HG22', ' B1014  ARG HH22', -0.448, (193.997, 205.344, 220.881)), (' A 250  THR  HB ', ' A 253  ASP  HB2', -0.448, (237.56, 138.812, 170.042)), (' A 538  CYS  HB2', ' A 590  CYS  HB2', -0.447, (197.695, 178.832, 194.157)), (' B  53  ASP  OD1', ' B  54  LEU  N  ', -0.447, (181.268, 214.36, 185.236)), (' C 946  GLY  O  ', ' C 949  GLN  HB3', -0.447, (217.871, 229.428, 223.285)), (' C 318  PHE  CE2', ' C 322  PRO  HD2', -0.447, (234.816, 217.794, 191.247)), (' A  56  LEU HD12', ' A  57  PRO  HD2', -0.446, (216.622, 171.532, 188.925)), (' B 388  ASN  HB2', ' B 527  PRO  HD2', -0.446, (197.356, 230.793, 168.602)), (' B 102  ARG  HD2', ' B 121  ASN  O  ', -0.446, (157.1, 207.573, 171.233)), (' A 986  PRO  HD3', ' C 386  LYS  HZ1', -0.445, (225.348, 212.972, 178.883)), (' A1029  MET  HB2', ' A1029  MET  HE2', -0.444, (221.27, 204.732, 236.659)), (' B1024  LEU  HG ', ' B1028  LYS  HE3', -0.443, (198.834, 207.853, 234.899)), (' C 759  PHE  HE2', ' C1001  LEU  HB3', -0.443, (203.744, 212.796, 199.885)), (' A 417  LYS  O  ', ' A 422  ASN  ND2', -0.442, (191.928, 219.844, 158.236)), (' B 715  PRO  HG3', ' B1069  PRO  HB3', -0.442, (190.614, 217.651, 255.486)), (' B  56  LEU HD12', ' B  57  PRO  HD2', -0.442, (173.254, 220.573, 189.059)), (' C 298  GLU  HG2', ' C 315  THR  HB ', -0.441, (230.438, 221.997, 204.339)), (' C 742  ILE HD11', ' C 753  LEU HD13', -0.441, (194.314, 217.884, 197.071)), (' A 917  TYR  HB3', ' C1129  VAL HG23', -0.44, (225.404, 196.28, 266.625)), (' A 722  VAL HG22', ' A1065  VAL HG22', -0.44, (223.438, 192.674, 246.552)), (' C 947  LYS  O  ', ' C 950  ASP  HB3', -0.439, (217.074, 225.68, 222.722)), (' C1084  ASP  N  ', ' C1084  ASP  OD1', -0.438, (223.313, 198.949, 281.425)), (' A 663  ASP  N  ', ' A 663  ASP  OD1', -0.438, (210.523, 181.423, 225.458)), (' B 145  TYR  HE2', ' B 245  HIS  HB3', -0.436, (143.489, 212.609, 170.911)), (' H  48  MET  HB3', ' H  48  MET  HE3', -0.436, (250.149, 133.827, 146.96)), (' C 986  PRO  HA ', ' C 989  ALA  HB3', -0.436, (199.916, 217.354, 180.982)), (' C 791  THR HG23', ' C 806  LEU HD12', -0.435, (200.248, 235.794, 244.096)), (' C 392  PHE  HB2', ' C 524  VAL HG13', -0.435, (233.016, 197.166, 171.01)), (' C 656  VAL HG23', ' C 695  TYR  HB3', -0.435, (240.51, 222.403, 227.046)), (' C 201  PHE  HB3', ' C 229  LEU  HB2', -0.434, (227.031, 237.913, 172.778)), (' A 152  TRP  CD2', ' H 100B PRO  HA ', -0.433, (241.983, 152.157, 169.204)), (' A 108  THR  HA ', ' A 236  THR HG22', -0.432, (212.859, 170.561, 169.46)), (' A 453  TYR  HE2', ' A 455  LEU HD13', -0.432, (193.23, 223.251, 153.603)), (' B 826  VAL  HB ', ' B1057  PRO  HG2', -0.431, (185.474, 197.907, 225.181)), (' A 545  GLY  O  ', ' B 982  SER  OG ', -0.43, (194.963, 191.493, 179.198)), (' A 246  ARG HH12', ' H  27  TYR  HA ', -0.43, (232.273, 146.825, 160.139)), (' A 245  HIS  H  ', ' A 260  ALA  HB2', -0.429, (233.759, 150.94, 171.528)), (' A 160  TYR  CE2', ' A 163  ALA  HB2', -0.429, (226.717, 166.907, 158.752)), (' C 126  VAL  O  ', ' C 171  VAL  HA ', -0.429, (225.837, 249.564, 167.692)), (' C 568  ASP  HB2', ' C 574  ASP  HB3', -0.429, (233.939, 198.688, 195.842)), (' A 553  THR  OG1', ' A 586  ASP  OD1', -0.429, (186.815, 182.815, 194.91)), (' A 106  PHE  HB2', ' A 117  LEU  HB3', -0.428, (222.669, 172.052, 169.953)), (' C  68  ILE HG21', ' C 262  ALA  HA ', -0.428, (248.249, 256.334, 182.338)), (' A 377  PHE  HE2', ' A 384  PRO  HB3', -0.427, (201.123, 196.965, 167.078)), (' C 204  TYR  HD1', ' C 225  PRO  HA ', -0.427, (223.091, 240.856, 183.076)), (' B 187  LYS  HE2', ' B 212  LEU HD13', -0.427, (150.568, 212.732, 187.97)), (' B 431  GLY  HA2', ' B 515  PHE  HD2', -0.426, (210.799, 226.4, 170.629)), (' C  33  THR  OG1', ' C 219  GLY  O  ', -0.426, (232.807, 242.418, 197.74)), (' C 898  PHE  O  ', ' C 902  MET  HG2', -0.426, (206.663, 227.896, 255.506)), (' A 866  THR  H  ', ' A 869  MET  HE2', -0.426, (233.945, 210.518, 227.021)), (' L  31  ASN  O  ', ' L  51  VAL HG23', -0.425, (254.147, 132.081, 169.391)), (' A 335  LEU HD12', ' A 362  VAL HG13', -0.424, (188.295, 185.468, 163.21)), (' C 756  TYR  OH ', ' C 994  ASP  OD1', -0.424, (201.322, 210.918, 190.261)), (' A 115  GLN  HA ', ' A 132  GLU  HA ', -0.423, (219.496, 172.022, 160.876)), (' A  34  ARG  NH1', ' A 191  GLU  OE2', -0.423, (230.322, 168.78, 191.21)), (' B 277  LEU HD12', ' B 285  ILE HD13', -0.422, (177.086, 206.057, 192.903)), (' C 214  ARG  O  ', ' C 266  TYR  OH ', -0.422, (242.919, 249.265, 191.144)), (' B 327  VAL HG12', ' B 542  ASN  HB3', -0.421, (194.521, 233.618, 178.588)), (' A 395  VAL HG22', ' A 515  PHE  HB3', -0.421, (188.349, 198.53, 170.03)), (' A 599  THR  HB ', ' A 608  VAL HG12', -0.421, (213.578, 178.116, 211.866)), (' A 946  GLY  O  ', ' A 950  ASP  HB2', -0.42, (219.592, 191.091, 222.836)), (' B 726  ILE HG13', ' B1061  VAL HG23', -0.42, (188.82, 203.796, 233.635)), (' A 884  SER  HG ', ' A 887  THR  HG1', -0.419, (227.658, 211.278, 251.501)), (' L  27B ASP  HA ', ' L  92  THR  OG1', -0.418, (261.334, 134.244, 159.611)), (' C 676  THR  HA ', ' C 690  GLN  HA ', -0.418, (239.661, 234.698, 223.137)), (' C 537  LYS  HB2', ' C 537  LYS  HE3', -0.418, (245.339, 214.966, 192.181)), (' C 557  LYS  HB3', ' C 557  LYS  HE2', -0.418, (239.532, 192.926, 194.55)), (' B 176  LEU  HA ', ' B 176  LEU HD12', -0.418, (162.439, 201.744, 180.523)), (' C 145  TYR  HA ', ' C 152  TRP  HB3', -0.417, (240.316, 266.044, 168.183)), (' B 386  LYS  HZ2', ' C 985  ASP  HA ', -0.417, (198.663, 220.882, 177.294)), (' H 100H TYR  CZ ', ' H 100J GLY  HA3', -0.417, (245.784, 137.133, 163.419)), (' A  25  PRO  HA ', ' A  26  PRO  HD3', -0.417, (212.825, 153.314, 182.703)), (' B 308  VAL  HB ', ' B 602  THR HG23', -0.417, (180.424, 213.12, 210.57)), (' B 112  SER  HB3', ' B 134  GLN  HA ', -0.417, (166.348, 221.888, 158.853)), (' A 626  ALA  HB1', ' A 634  ARG  HG3', -0.417, (202.115, 169.053, 200.703)), (' A 327  VAL HG12', ' A 542  ASN  HB3', -0.416, (194.622, 183.628, 178.87)), (' A1115  ILE HD11', ' A1120  THR  HB ', -0.416, (200.652, 199.202, 272.892)), (' C 290  ASP  O  ', ' C 297  SER  HB3', -0.416, (231.373, 230.126, 201.276)), (' B 280  ASN  ND2', ' B 284  THR  OG1', -0.415, (172.714, 198.744, 196.615)), (' C 909  ILE HD12', ' C1047  TYR  HB3', -0.415, (216.071, 217.627, 251.961)), (' A 251  PRO  HG3', ' H  99  ILE HG21', -0.415, (244.117, 139.789, 167.916)), (' A 747  THR  HA ', ' C 549  THR HG23', -0.415, (232.624, 213.464, 187.223)), (' C 553  THR  HB ', ' C 586  ASP  HB3', -0.415, (242.094, 201.905, 195.364)), (' A 425  LEU HD21', ' A 512  VAL HG11', -0.414, (192.081, 208.315, 165.94)), (' C 856  ASN  HA ', ' C 856  ASN HD22', -0.414, (202.733, 227.785, 199.09)), (' A 317  ASN  HB3', ' B 739  THR HG21', -0.412, (204.864, 185.671, 197.413)), (' B 729  VAL HG12', ' B1059  GLY  HA2', -0.412, (194.743, 199.493, 227.557)), (' C 896  ILE HD11', ' C 904  TYR  HE2', -0.412, (201.805, 223.294, 259.113)), (' B 467  ASP  N  ', ' B 467  ASP  OD1', -0.412, (230.607, 226.911, 161.583)), (' B 273  ARG  HA ', ' B 273  ARG  HD3', -0.411, (181.986, 220.047, 191.322)), (' C 726  ILE HG13', ' C1061  VAL HG23', -0.411, (214.626, 227.889, 233.697)), (' B 617  CYS  N  ', ' B 649  CYS  SG ', -0.411, (186.3, 237.615, 211.396)), (' H  47  TRP  CZ2', ' H  50  GLY  HA3', -0.41, (250.771, 139.117, 153.861)), (' B1009  THR HG21', ' C1005  GLN HE22', -0.41, (207.04, 209.033, 207.478)), (' B 553  THR  O  ', ' B 585  LEU HD12', -0.41, (196.722, 242.398, 191.263)), (' B 598  ILE HD13', ' B 666  ILE HG12', -0.409, (185.646, 225.109, 217.517)), (' C 551  VAL HG21', ' C 625  HIS  NE2', -0.408, (241.447, 212.005, 196.501)), (' C 962  LEU HD13', ' C1007  TYR  HB2', -0.408, (209.051, 219.495, 205.555)), (' A 176  LEU HD22', ' A 190  ARG  HD3', -0.407, (234.559, 165.094, 180.637)), (' B 174  PRO  HB2', ' B 177  MET  HB2', -0.405, (159.305, 201.72, 175.369)), (' A 152  TRP  CE2', ' H 100B PRO  HA ', -0.404, (242.075, 151.868, 169.215)), (' A  92  PHE  O  ', ' A 192  PHE  N  ', -0.404, (227.516, 169.018, 183.45)), (' A 425  LEU  HA ', ' A 425  LEU HD23', -0.404, (191.297, 210.905, 168.017)), (' B 336  CYS  HA ', ' B 337  PRO  HD3', -0.404, (206.123, 239.281, 162.352)), (' B 558  LYS  HA ', ' B 558  LYS  HD3', -0.403, (207.398, 248.258, 191.365)), (' A 188  ASN  O  ', ' A 190  ARG  NH1', -0.403, (234.403, 162.419, 185.07)), (' A 666  ILE HD12', ' A 670  ILE HG22', -0.403, (203.719, 178.855, 220.745)), (' A 117  LEU  CD1', ' A 231  ILE HG21', -0.402, (224.38, 176.58, 169.962)), (' A 379  CYS  HA ', ' A 432  CYS  HA ', -0.402, (197.712, 202.473, 168.059)), (' C 612  TYR  CE1', ' C 624  ILE HG21', -0.401, (240.386, 217.801, 205.417)), (' C 144  TYR  CE1', ' C 258  TRP  CH2', -0.401, (246.963, 259.196, 165.715)), (' B 386  LYS  NZ ', ' C 984  LEU  O  ', -0.401, (199.379, 221.672, 178.461)), (' B 979  ASP  O  ', ' B 983  ARG  HG2', -0.401, (196.819, 196.644, 180.525)), (' C 310  LYS  HZ2', ' C 664  ILE HD11', -0.4, (230.91, 227.467, 219.722))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
