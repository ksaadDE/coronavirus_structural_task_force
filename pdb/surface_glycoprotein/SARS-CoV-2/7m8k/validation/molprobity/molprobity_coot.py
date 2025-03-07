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
data['rota'] = [('B', '  90 ', 'VAL', 0.1535236235210564, (177.695, 239.019, 233.844)), ('B', ' 216 ', 'LEU', 0.21184470427893423, (173.483, 248.315, 221.21)), ('B', ' 231 ', 'ILE', 0.129302198820164, (189.414, 237.271, 246.87499999999997)), ('C', '1094 ', 'VAL', 0.24571535161759828, (210.82400000000007, 192.801, 150.386))]
data['cbeta'] = []
data['probe'] = [(' B 205  SER  O  ', ' B 223  LEU HD22', -0.856, (187.552, 247.866, 228.046)), (' A 740  MET  CE ', ' C 319  ARG  HE ', -0.81, (216.139, 182.253, 216.489)), (' A 740  MET  HB2', ' C 319  ARG HH21', -0.788, (214.389, 183.612, 216.175)), (' A 740  MET  HE3', ' C 319  ARG  HE ', -0.748, (215.834, 182.235, 216.398)), (' C1101  HIS  ND1', ' M   1  NAG  H5 ', -0.723, (207.159, 180.976, 138.997)), (' B  34  ARG  NH2', ' B 219  GLY  O  ', -0.718, (180.064, 247.884, 217.883)), (' B1091  ARG  NH1', ' B1118  ASP  O  ', -0.713, (199.618, 205.822, 142.443)), (' B 908  GLY  O  ', ' B1038  LYS  NZ ', -0.713, (202.754, 211.597, 162.702)), (' A 773  GLU  OE2', ' A1019  ARG  NH1', -0.695, (206.463, 194.675, 191.742)), (' C 189  LEU HD22', ' C 210  ILE HD13', -0.686, (182.193, 155.359, 221.951)), (' A 780  GLU  O  ', ' A 784  GLN  NE2', -0.679, (209.11, 191.872, 180.988)), (' A 957  GLN  OE1', ' B 765  ARG  NH1', -0.665, (222.972, 205.584, 206.683)), (' B  31  SER  OG ', ' B  60  SER  N  ', -0.664, (173.798, 237.253, 220.853)), (' B 223  LEU HD23', ' B 224  GLU  N  ', -0.657, (189.875, 246.619, 227.061)), (' A 740  MET  HE3', ' C 319  ARG  NE ', -0.65, (215.328, 181.831, 216.666)), (' C 501  TYR  O  ', ' C 506  GLN  NE2', -0.648, (217.451, 203.295, 271.531)), (' B 206  LYS  HE3', ' B 223  LEU  HB3', -0.619, (187.419, 246.366, 225.589)), (' C 905  ARG  NH1', ' C1049  LEU  O  ', -0.615, (192.999, 199.438, 166.792)), (' A 669  GLY  HA2', ' A 697  MET  HE3', -0.599, (224.641, 226.722, 190.001)), (' A 740  MET  CE ', ' C 319  ARG  NE ', -0.594, (216.023, 181.529, 216.944)), (' A 280  ASN  OD1', ' A 284  THR  N  ', -0.593, (245.65, 195.497, 215.074)), (' B1092  GLU  N  ', ' B1092  GLU  OE1', -0.591, (196.415, 206.524, 149.24)), (' G   1  NAG  H61', ' G   2  NAG  H2 ', -0.59, (235.286, 208.248, 158.046)), (' C 105  ILE HD11', ' C 241  LEU HD21', -0.589, (186.297, 156.958, 245.418)), (' C 557  LYS  NZ ', ' C 574  ASP  OD2', -0.588, (234.661, 187.543, 216.521)), (' C 318  PHE  HZ ', ' C 615  VAL HG21', -0.585, (218.082, 175.103, 209.567)), (' A 563  GLN  O  ', ' A 577  ARG  NH1', -0.582, (202.696, 245.323, 229.473)), (' B 407  VAL HG21', ' B 508  TYR  HB3', -0.582, (175.515, 193.661, 274.813)), (' A 671  CYS  SG ', ' A 697  MET  HE2', -0.58, (226.983, 224.7, 189.992)), (' C 618  THR  OG1', ' C 619  GLU  OE1', -0.576, (224.718, 169.975, 209.438)), (' B 568  ASP  OD1', ' B 572  THR  N  ', -0.574, (183.784, 191.76, 217.504)), (' A 520  ALA  HB3', ' A 521  PRO  HD3', -0.573, (200.046, 237.694, 234.319)), (' K   1  NAG  H4 ', ' K   2  NAG  C7 ', -0.569, (186.528, 230.968, 157.063)), (' A 320  VAL HG12', ' A 322  PRO  HD3', -0.562, (227.866, 233.245, 220.099)), (' A 740  MET  HE2', ' C 319  ARG  HE ', -0.561, (216.629, 182.476, 217.302)), (' B 666  ILE HD11', ' B 672  ALA  HB2', -0.557, (175.295, 219.017, 197.236)), (' A 898  PHE  HZ ', ' A1050  MET  HE1', -0.555, (221.833, 194.977, 164.504)), (' A 902  MET  HE1', ' A1049  LEU HD13', -0.552, (221.242, 200.942, 163.214)), (' A 340  GLU  N  ', ' A 340  GLU  OE1', -0.551, (204.732, 234.35, 260.273)), (' B 347  PHE  CE2', ' B 441  LEU HD22', -0.549, (167.401, 183.922, 272.495)), (' C 324  GLU  N  ', ' C 324  GLU  OE1', -0.547, (224.493, 170.309, 225.39)), (' B 324  GLU  OE1', ' B 537  LYS  NZ ', -0.546, (166.636, 205.255, 226.553)), (' C 401  VAL HG22', ' C 509  ARG  HA ', -0.545, (227.582, 200.8, 262.03)), (' A 618  THR  OG1', ' A 619  GLU  OE1', -0.54, (227.345, 239.936, 209.624)), (' A 106  PHE  HE1', ' A 119  ILE HD12', -0.537, (253.353, 208.197, 239.902)), (' B 391  CYS  HA ', ' B 525  CYS  HB3', -0.53, (180.761, 190.646, 247.809)), (' A 553  THR  O  ', ' A 586  ASP  N  ', -0.524, (214.086, 243.453, 222.204)), (' A 569  ILE  O  ', ' B 964  LYS  NZ ', -0.522, (202.114, 228.763, 216.779)), (' C 280  ASN  OD1', ' C 284  THR  N  ', -0.521, (177.558, 175.538, 216.007)), (' B 393  THR HG22', ' B 522  ALA  O  ', -0.52, (185.994, 184.924, 247.402)), (' C 702  GLU  N  ', ' C 702  GLU  OE1', -0.519, (214.764, 174.364, 174.32)), (' B 392  PHE  O  ', ' B 524  VAL  N  ', -0.517, (182.692, 186.356, 249.315)), (' C 666  ILE HD11', ' C 672  ALA  HB2', -0.511, (210.287, 171.763, 195.269)), (' A 619  GLU  N  ', ' A 619  GLU  OE1', -0.511, (227.975, 238.551, 210.48)), (' C1097  SER  HB3', ' C1102  TRP  CD2', -0.508, (213.626, 185.581, 144.059)), (' C 457  ARG  NH2', ' C 459  SER  OG ', -0.508, (232.313, 220.867, 249.118)), (' C 895  GLN  N  ', ' C 895  GLN  OE1', -0.506, (180.621, 210.33, 161.845)), (' M   1  NAG  H61', ' M   2  NAG  C7 ', -0.506, (205.36, 181.922, 137.219)), (' A1081  ILE HD11', ' A1115  ILE HG21', -0.506, (209.993, 220.584, 141.578)), (' C 613  GLN  O  ', ' C 615  VAL HG23', -0.504, (218.637, 177.047, 206.902)), (' A 339  GLY  O  ', ' A 343  ASN  N  ', -0.502, (205.264, 230.34, 262.17)), (' C 186  PHE  CE1', ' C 210  ILE HD11', -0.502, (181.425, 151.889, 223.208)), (' C 902  MET  CE ', ' C1049  LEU HD13', -0.499, (191.724, 193.916, 163.834)), (' B 749  CYS  SG ', ' B 997  ILE HD11', -0.498, (215.922, 215.721, 224.535)), (' A 900  MET  HE1', ' C1077  THR  OG1', -0.498, (215.909, 189.556, 150.828)), (' G   1  NAG  H4 ', ' G   2  NAG  C7 ', -0.496, (235.329, 208.84, 156.651)), (' C 553  THR  OG1', ' C 586  ASP  OD1', -0.496, (235.245, 178.658, 216.624)), (' C 518  LEU  CD1', ' C 520  ALA  HB2', -0.495, (237.801, 195.543, 233.996)), (' B 741  TYR  CE1', ' B 966  LEU HD21', -0.495, (210.493, 220.642, 217.322)), (' B  31  SER  O  ', ' B  59  PHE  N  ', -0.492, (174.464, 238.281, 219.074)), (' K   1  NAG  H62', ' K   2  NAG  H2 ', -0.491, (186.324, 231.764, 159.238)), (' A 993  ILE  O  ', ' A 997  ILE HD12', -0.491, (211.63, 194.926, 226.298)), (' L   1  NAG  H4 ', ' L   2  NAG  C7 ', -0.489, (191.486, 178.397, 156.077)), (' C 518  LEU HD11', ' C 520  ALA  HB2', -0.487, (238.582, 195.409, 234.5)), (' B 392  PHE  CE1', ' B 517  LEU HD11', -0.486, (185.683, 191.926, 253.192)), (' B 342  PHE  HE2', ' B 511  VAL HG21', -0.486, (174.487, 188.869, 263.594)), (' B 562  PHE  O  ', ' B 564  GLN  NE2', -0.483, (176.667, 180.41, 229.165)), (' B 905  ARG  NH1', ' B1049  LEU  O  ', -0.481, (205.515, 218.995, 166.883)), (' A 324  GLU  HB3', ' A 539  VAL HG12', -0.479, (225.759, 238.186, 227.424)), (' B 336  CYS  H  ', ' B 363  ALA  HB2', -0.473, (172.891, 185.715, 251.376)), (' B 405  ASP  N  ', ' B 504  GLY  O  ', -0.471, (176.675, 195.23, 281.536)), (' B 350  VAL HG23', ' B 495  TYR  OH ', -0.47, (179.066, 185.777, 276.951)), (' B 600  PRO  HD3', ' B 692  ILE HD11', -0.47, (176.555, 227.703, 200.052)), (' B 138  TYR  O  ', ' B 160  TYR  OH ', -0.469, (169.379, 253.874, 249.764)), (' A 898  PHE  CZ ', ' A1050  MET  HE1', -0.467, (221.858, 194.621, 164.144)), (' C  96  GLU  OE2', ' C 100  ILE  N  ', -0.464, (177.715, 151.643, 234.913)), (' C 578  ASP  OD2', ' C 580  GLN  N  ', -0.464, (239.572, 178.601, 232.064)), (' C 909  ILE HD12', ' C1047  TYR  HB3', -0.463, (200.056, 195.707, 164.654)), (' B 365  TYR  H  ', ' B 387  LEU HD12', -0.461, (174.033, 194.28, 252.036)), (' C 902  MET  SD ', ' C1050  MET  HE3', -0.461, (189.327, 196.503, 164.443)), (' E   1  NAG  H4 ', ' E   2  NAG  C7 ', -0.46, (227.415, 221.178, 138.908)), (' B  53  ASP  OD1', ' B  54  LEU  N  ', -0.46, (186.357, 232.159, 229.086)), (' B  91  TYR  HD1', ' B 193  VAL HG22', -0.459, (181.076, 241.668, 229.295)), (' C 414  GLN  O  ', ' C 424  LYS  NZ ', -0.459, (221.979, 213.174, 247.751)), (' C 404  GLY  N  ', ' C 506  GLN  O  ', -0.458, (220.666, 204.57, 264.598)), (' C1142  GLN  NE2', ' C1146  ASP  OD1', -0.458, (205.719, 200.503, 123.262)), (' C 767  LEU HD21', ' C1008  VAL HG22', -0.455, (194.728, 206.325, 208.166)), (' C 125  ASN  O  ', ' C 125  ASN  OD1', -0.454, (172.712, 162.403, 243.033)), (' B 104  TRP  HH2', ' B 192  PHE  CE1', -0.453, (180.623, 250.036, 234.607)), (' C 417  THR  O  ', ' C 421  TYR  N  ', -0.453, (226.872, 215.49, 253.947)), (' B 423  TYR  O  ', ' B 424  LYS  C  ', -0.452, (190.774, 190.669, 271.907)), (' B 825  LYS  NZ ', ' B 942  ALA  O  ', -0.451, (193.675, 233.204, 189.079)), (' B 569  ILE HG22', ' C  47  VAL HG11', -0.45, (183.167, 185.139, 211.356)), (' J   1  NAG  H4 ', ' J   2  NAG  H2 ', -0.449, (201.935, 243.25, 170.53)), (' B 990  GLU  N  ', ' B 990  GLU  OE1', -0.449, (215.005, 212.703, 234.928)), (' C1144  GLU  C  ', ' C1145  LEU HD12', -0.448, (199.953, 199.332, 126.424)), (' A 442  ASP  OD2', ' A 451  TYR  OH ', -0.448, (196.541, 222.885, 268.59)), (' B  38  TYR  CE1', ' B 285  ILE HD12', -0.446, (192.18, 242.776, 222.535)), (' H   1  NAG  H4 ', ' H   2  NAG  C7 ', -0.446, (175.409, 194.53, 137.692)), (' A  34  ARG  NH2', ' A 191  GLU  OE2', -0.443, (255.992, 206.269, 220.773)), (' A 106  PHE  CE1', ' A 119  ILE HD12', -0.442, (253.04, 208.657, 239.892)), (' B 130  VAL HG11', ' B 231  ILE HD13', -0.442, (186.65, 240.453, 248.628)), (' A 483  VAL HG12', ' A 485  GLY  H  ', -0.438, (167.883, 210.916, 265.91)), (' B 417  THR  OG1', ' B 421  TYR  OH ', -0.435, (185.135, 190.938, 281.809)), (' C 534  VAL HG11', ' C 537  LYS  CE ', -0.433, (229.735, 168.548, 223.243)), (' C 617  CYS  SG ', ' C 644  GLN  NE2', -0.432, (220.854, 170.191, 202.971)), (' B 731  MET  N  ', ' B 774  GLN  OE1', -0.432, (210.533, 219.164, 195.446)), (' C 996  LEU HD11', ' C1000  ARG  NE ', -0.43, (193.325, 200.062, 223.537)), (' B 115  GLN  OE1', ' B 131  CYS  HA ', -0.43, (183.782, 241.547, 253.671)), (' B  40  ASP  OD1', ' B  41  LYS  N  ', -0.43, (197.177, 237.103, 229.195)), (' B 403  ARG  O  ', ' B 407  VAL HG23', -0.43, (177.646, 193.09, 277.471)), (' B  53  ASP  OD2', ' B 195  LYS  NZ ', -0.429, (188.711, 234.471, 229.873)), (' C 763  LEU HD21', ' C1005  GLN  NE2', -0.428, (200.306, 209.657, 213.588)), (' B 104  TRP  CH2', ' B 192  PHE  CE1', -0.428, (180.561, 249.74, 234.583)), (' C 567  ARG  NH1', ' C 571  ASP  O  ', -0.427, (228.797, 193.32, 223.64)), (' F   1  NAG  H2 ', ' F   1  NAG  H83', -0.427, (237.153, 190.166, 164.735)), (' B 736  VAL HG22', ' B 767  LEU  CD1', -0.427, (215.073, 216.628, 208.837)), (' C  31  SER  OG ', ' C  62  VAL HG13', -0.427, (194.572, 159.551, 224.019)), (' A 741  TYR  CD2', ' A1004  LEU HD21', -0.426, (214.413, 193.837, 214.274)), (' I   1  NAG  H4 ', ' I   2  NAG  H2 ', -0.425, (179.887, 218.957, 140.785)), (' B 206  LYS  HG3', ' B 223  LEU  HB3', -0.424, (187.129, 247.475, 226.402)), (' A 699  LEU HD11', ' B 869  MET  HB3', -0.423, (220.997, 228.077, 184.295)), (' C 143  VAL HG23', ' C 244  LEU  O  ', -0.423, (178.698, 145.4, 243.17)), (' K   1  NAG  H2 ', ' K   1  NAG  H83', -0.421, (185.725, 228.473, 155.716)), (' B 805  ILE HD12', ' B 878  LEU HD11', -0.42, (207.354, 229.748, 173.194)), (' C  53  ASP  OD2', ' C 195  LYS  NZ ', -0.42, (190.913, 175.405, 229.264)), (' A 903  ALA  HB2', ' A 916  LEU HD22', -0.419, (220.528, 197.625, 155.297)), (' E   1  NAG  H4 ', ' E   2  NAG  H2 ', -0.419, (227.112, 220.441, 139.242)), (' B 409  GLN  OE1', ' B 417  THR  N  ', -0.418, (186.591, 193.752, 279.945)), (' B 189  LEU  HB2', ' B 210  ILE HG21', -0.417, (177.884, 253.223, 223.035)), (' B 366  SER  HA ', ' B 369  TYR  HB3', -0.417, (171.767, 197.926, 255.577)), (' A 805  ILE HD12', ' A 878  LEU HD11', -0.415, (224.341, 191.601, 171.676)), (' B 358  ILE  O  ', ' B 395  VAL  N  ', -0.414, (182.159, 183.316, 254.644)), (' C 779  GLN  O  ', ' C 783  ALA  HB3', -0.414, (187.377, 211.203, 184.415)), (' F   1  NAG  H4 ', ' F   2  NAG  H2 ', -0.413, (238.682, 189.777, 167.87)), (' C 130  VAL HG21', ' C 168  PHE  CE1', -0.412, (183.548, 172.704, 247.634)), (' C 249  LEU HD23', ' C 251  PRO  HD3', -0.412, (188.821, 145.411, 253.815)), (' C 393  THR HG21', ' C 520  ALA  HB3', -0.412, (237.476, 193.619, 236.093)), (' C 534  VAL HG11', ' C 537  LYS  HE3', -0.411, (229.914, 168.917, 223.752)), (' H   1  NAG  H4 ', ' H   2  NAG  H2 ', -0.41, (176.26, 194.461, 137.233)), (' B 559  PHE  CZ ', ' B 584  ILE HD12', -0.41, (172.395, 183.981, 223.536)), (' C 125  ASN  C  ', ' C 125  ASN  OD1', -0.41, (172.648, 162.637, 242.954)), (' B 518  LEU  O  ', ' B 518  LEU HD23', -0.409, (193.414, 186.532, 247.74)), (' A 871  ALA  O  ', ' A 874  THR  OG1', -0.407, (221.866, 186.216, 179.204)), (' C 922  LEU HD21', ' L   1  NAG  H5 ', -0.406, (191.418, 182.134, 157.908)), (' A 518  LEU HD12', ' A 520  ALA  H  ', -0.405, (201.576, 234.733, 234.587)), (' B 454  ARG  NE ', ' B 471  GLU  OE1', -0.405, (189.262, 181.145, 280.677)), (' B 461  LEU HD21', ' B 467  ASP  HB2', -0.403, (191.618, 183.281, 272.923)), (' A 955  ASN  O  ', ' A 959  LEU HD23', -0.402, (220.601, 196.453, 204.413)), (' L   1  NAG  H62', ' L   2  NAG  O5 ', -0.401, (190.23, 179.09, 159.022))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
