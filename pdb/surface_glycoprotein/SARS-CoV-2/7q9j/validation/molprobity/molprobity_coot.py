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
data['rota'] = [('A', '  65 ', 'PHE', 0.13783237110191468, (238.988, 163.914, 182.889)), ('A', ' 328 ', 'ASN', 0.012329474261002582, (183.844, 139.566, 176.187)), ('A', ' 718 ', 'SER', 0.2277572059856333, (206.32100000000005, 182.101, 244.238)), ('A', ' 802 ', 'ILE', 0.03674701788172307, (209.28500000000005, 196.729, 238.56)), ('A', ' 817 ', 'ASP', 0.2250330919645526, (212.734, 197.092, 229.316)), ('A', ' 879 ', 'ILE', 0.13425135775219188, (201.56200000000007, 198.91499999999994, 246.535)), ('B', '  51 ', 'THR', 0.2870483820918889, (166.104, 161.73, 193.188)), ('B', '  65 ', 'PHE', 0.03155000609334937, (139.38499999999993, 147.957, 182.982)), ('B', ' 575 ', 'ASP', 0.2880493857727894, (148.77100000000004, 205.895, 186.168)), ('B', ' 757 ', 'CYS', 0.23658417458859662, (195.99000000000007, 176.7, 198.017)), ('B', ' 817 ', 'ASP', 0.21099705888093656, (181.31100000000006, 153.882, 229.14699999999996)), ('B', ' 885 ', 'PHE', 0.19095086777287132, (196.16400000000004, 169.51299999999998, 245.258)), ('C', '  47 ', 'VAL', 0.27893968757003557, (165.44700000000006, 210.732, 202.516)), ('C', '  65 ', 'PHE', 0.06331152968896964, (175.28400000000008, 241.404, 181.992)), ('C', ' 575 ', 'ASP', 0.2399123261096417, (221.013, 204.484, 186.081)), ('C', '1048 ', 'SER', 0.14754446375608507, (171.8280000000001, 194.39799999999994, 241.24)), ('C', '1101 ', 'VAL', 0.2994341263221481, (190.409, 198.52600000000004, 266.805)), ('C', '1130 ', 'VAL', 0.24284369133445913, (203.94800000000004, 199.41000000000005, 269.95)), ('H', '   6 ', 'GLN', 0.0, (182.551, 141.50500000000002, 102.134)), ('E', '   6 ', 'GLN', 0.0, (142.192, 206.797, 102.379)), ('J', '   6 ', 'GLN', 0.0, (227.36400000000006, 216.239, 104.371))]
data['cbeta'] = []
data['probe'] = [(' C 909  THR HG21', ' C1103  GLN HE21', -1.138, (182.469, 195.155, 262.662)), (' C 909  THR  CG2', ' C1103  GLN HE21', -1.013, (182.664, 195.725, 261.883)), (' B 942  LEU HD12', ' B 945  LEU HD22', -0.908, (178.53, 164.6, 224.496)), (' A  96  GLU  OE1', ' A 100  ILE  HB ', -0.907, (244.131, 174.524, 181.367)), (' C 909  THR HG21', ' C1103  GLN  NE2', -0.856, (182.105, 196.507, 262.83)), (' C 760  LEU HD13', ' C1001  LEU  HG ', -0.814, (174.474, 183.743, 200.343)), (' E  24  VAL  O  ', ' E  76  ASN  ND2', -0.737, (141.607, 207.833, 113.97)), (' A 554  LYS  NZ ', ' A 571  ASP  OD2', -0.734, (180.897, 149.829, 198.666)), (' A 799  PHE  CD2', ' A 879  ILE HD11', -0.722, (206.311, 197.242, 243.94)), (' A 277  ASN  OD1', ' A 280  GLY  N  ', -0.721, (224.969, 191.15, 200.281)), (' A 277  ASN  OD1', ' A 279  ASN  N  ', -0.713, (225.905, 191.643, 200.898)), (' B 560  GLN  O  ', ' B 574  ARG  NH2', -0.709, (154.753, 212.089, 187.526)), (' B  99  ASN  OD1', ' B 190  ARG  NH2', -0.702, (151.486, 135.027, 183.431)), (' B 717  ILE HG13', ' B 920  ILE HG23', -0.701, (174.924, 165.305, 250.777)), (' C 486  TYR  HE1', ' J  33  TYR  HE1', -0.699, (224.929, 198.0, 116.162)), (' A1038  ASP  O  ', ' A1038  ASP  OD1', -0.696, (193.841, 178.807, 236.458)), (' A1042  LYS  NZ ', ' B 887  ALA  O  ', -0.688, (200.941, 173.884, 242.709)), (' B 595  ILE HD11', ' B 663  ILE HG12', -0.683, (154.441, 176.89, 215.111)), (' C  40  ASP  OD1', ' C  42  VAL  N  ', -0.682, (162.924, 210.637, 189.329)), (' B 798  ASN  ND2', ' P   1  NAG  O7 ', -0.68, (179.505, 151.531, 247.796)), (' A 895  PHE  HZ ', ' A1047  MET  HE1', -0.68, (203.62, 192.843, 247.712)), (' C 942  LEU HD12', ' C 945  LEU HD12', -0.672, (169.915, 200.36, 224.84)), (' B  91  TYR  OH ', ' B 191  GLU  OE1', -0.671, (151.882, 148.009, 189.941)), (' C 565  ASP  OD1', ' C 566  ILE  N  ', -0.671, (211.44, 193.819, 200.147)), (' B 306  GLU  N  ', ' B 306  GLU  OE1', -0.671, (162.583, 163.298, 214.183)), (' C 663  ILE HD12', ' C 667  ILE HG22', -0.67, (195.975, 215.167, 217.631)), (' B 913  LEU HD12', ' B 920  ILE HD12', -0.67, (177.157, 165.345, 255.623)), (' A 616  GLU  N  ', ' A 616  GLU  OE1', -0.67, (202.695, 151.075, 201.026)), (' B 813  SER  N  ', ' B 816  GLU  OE1', -0.663, (185.709, 155.544, 232.866)), (' B 899  MET  HE1', ' B1046  LEU HD13', -0.662, (178.871, 168.023, 249.715)), (' B  57  PRO  O  ', ' B  60  SER  OG ', -0.662, (150.01, 159.09, 191.98)), (' A 325  ARG  NH2', ' A 528  THR  O  ', -0.66, (190.974, 142.798, 180.628)), (' C  57  PRO  O  ', ' C  60  SER  OG ', -0.659, (180.061, 226.627, 191.105)), (' C 722  GLU  OE1', ' C1061  HIS  NE2', -0.656, (176.581, 195.698, 235.871)), (' C 575  ASP  OD1', ' C 577  GLN  N  ', -0.656, (222.782, 206.211, 182.821)), (' B1103  GLN  NE2', ' B1108  GLU  OE1', -0.656, (173.226, 174.131, 262.721)), (' A  29  THR HG22', ' A  30  ASN  H  ', -0.654, (233.507, 164.359, 193.026)), (' B 139  PRO  HB3', ' B 159  VAL HG13', -0.65, (147.082, 143.09, 167.298)), (' B 284  ASP  OD1', ' B 285  ALA  N  ', -0.641, (158.866, 153.728, 200.941)), (' C  31  SER  OG ', ' C  60  SER  N  ', -0.637, (179.702, 229.48, 192.386)), (' C 139  PRO  HB3', ' C 159  VAL HG13', -0.637, (167.589, 237.48, 166.886)), (' A1047  MET  HE3', ' A1049  PHE  HZ ', -0.635, (203.074, 192.321, 245.11)), (' A 216  LEU HD12', ' A 217  PRO  HD2', -0.634, (236.88, 171.653, 192.091)), (' B 575  ASP  OD1', ' B 577  GLN  N  ', -0.63, (146.498, 206.748, 182.917)), (' A1103  GLN  NE2', ' A1108  GLU  OE1', -0.624, (198.046, 179.866, 262.32)), (' C 482  GLY  O  ', ' J  33  TYR  OH ', -0.62, (227.358, 195.543, 116.174)), (' K  91  ASP  O  ', ' K  95  ASP  N  ', -0.619, (224.755, 190.456, 104.658)), (' L  91  ASP  O  ', ' L  95  ASP  N  ', -0.618, (161.58, 155.352, 106.385)), (' C 793  ASP  N  ', ' C 793  ASP  OD1', -0.616, (155.38, 197.694, 252.047)), (' B 595  ILE  CD1', ' B 663  ILE HG12', -0.616, (154.71, 176.171, 214.891)), (' C 909  THR  CG2', ' C1103  GLN  NE2', -0.614, (182.498, 196.474, 262.246)), (' A 419  ASN  OD1', ' A 451  ARG  N  ', -0.61, (173.691, 149.778, 134.25)), (' F  91  ASP  O  ', ' F  95  ASP  N  ', -0.61, (166.387, 215.875, 104.905)), (' B 966  ASN  OD1', ' B 972  SER  N  ', -0.603, (180.128, 168.835, 185.238)), (' A1050  PRO  O  ', ' A1051  GLN  NE2', -0.603, (204.335, 195.698, 235.451)), (' A 653  VAL HG12', ' A 655  ASN  H  ', -0.603, (211.536, 152.733, 226.479)), (' C 760  LEU  CD1', ' C1001  LEU  HG ', -0.601, (174.602, 183.166, 200.24)), (' C 305  VAL  HB ', ' C 599  THR HG23', -0.6, (178.302, 218.181, 211.09)), (' B 799  PHE  HD2', ' B 802  ILE HD11', -0.6, (183.197, 159.658, 243.337)), (' C 390  THR  O  ', ' C 520  THR  OG1', -0.596, (219.739, 194.121, 163.746)), (' C 728  MET  N  ', ' C 771  GLN  OE1', -0.589, (169.969, 188.968, 218.725)), (' E  11  LEU HD11', ' E 121  SER  OG ', -0.588, (139.919, 211.697, 84.469)), (' B1050  PRO  O  ', ' B1051  GLN  NE2', -0.588, (184.78, 161.776, 235.305)), (' A  43  PHE  N  ', ' C 562  PHE  O  ', -0.586, (218.635, 193.506, 191.955)), (' C 486  TYR  HE1', ' J  33  TYR  CE1', -0.583, (225.047, 197.738, 116.061)), (' A 109  THR  OG1', ' A 111  ASP  OD1', -0.578, (225.674, 168.702, 161.91)), (' C1095  ASN  ND2', ' U   1  NAG  O7 ', -0.577, (191.399, 211.474, 268.823)), (' C  91  TYR  OH ', ' C 191  GLU  OE1', -0.576, (169.289, 230.235, 189.59)), (' A 284  ASP  OD1', ' A 285  ALA  N  ', -0.575, (223.897, 178.189, 200.666)), (' B 895  PHE  HZ ', ' B1047  MET  HE1', -0.569, (183.188, 164.027, 248.125)), (' C1025  LYS  NZ ', ' C1039  PHE  O  ', -0.569, (180.831, 192.718, 235.375)), (' A 965  SER  HB3', ' B 752  GLN  O  ', -0.568, (197.842, 183.87, 190.106)), (' H  11  LEU HD11', ' H 121  SER  OG ', -0.565, (178.86, 138.566, 83.586)), (' C 325  ARG  NH2', ' C 528  THR  O  ', -0.565, (217.755, 210.926, 180.518)), (' A 323  ILE  N  ', ' A 537  ASN  O  ', -0.565, (193.688, 150.537, 183.963)), (' J  11  LEU HD11', ' J 121  SER  OG ', -0.565, (232.339, 217.516, 85.924)), (' B1036  ARG  NE ', ' C1028  GLU  OE2', -0.562, (181.229, 183.073, 237.811)), (' C 482  GLY  C  ', ' J  33  TYR  OH ', -0.561, (227.184, 196.009, 115.602)), (' B 663  ILE HD11', ' B 669  ALA  HB2', -0.56, (152.391, 175.684, 216.778)), (' A  96  GLU  OE1', ' A 100  ILE  CB ', -0.559, (245.093, 174.641, 181.136)), (' A 913  LEU HD12', ' A 920  ILE HD12', -0.559, (204.867, 187.535, 255.424)), (' A 968  GLY  O  ', ' A 992  ARG  NH1', -0.558, (193.1, 184.285, 181.197)), (' A 779  PHE  O  ', ' A 781  GLN  N  ', -0.558, (192.293, 201.159, 232.896)), (' B1086  PHE  HZ ', ' B1126  VAL HG21', -0.556, (170.842, 197.882, 265.839)), (' B 325  ARG  NH2', ' B 528  THR  O  ', -0.554, (145.123, 199.628, 180.899)), (' A 895  PHE  CZ ', ' A1047  MET  HE1', -0.552, (203.449, 193.577, 248.003)), (' B 609  TYR  HE2', ' B 648  ILE HD12', -0.551, (148.085, 176.494, 205.518)), (' C1088  ARG  NH1', ' C1115  ASP  O  ', -0.551, (187.0, 188.652, 270.238)), (' L  32  VAL  N  ', ' L  50  ASP  OD1', -0.551, (171.001, 166.293, 108.857)), (' B 565  ASP  OD1', ' B 566  ILE  N  ', -0.55, (162.703, 203.744, 200.68)), (' C 563  GLY  N  ', ' C 572  ALA  O  ', -0.549, (216.967, 197.455, 191.852)), (' B 892  GLN  N  ', ' B 892  GLN  OE1', -0.549, (197.316, 163.431, 252.337)), (' A 723  ILE HG23', ' A1058  VAL HG22', -0.546, (203.271, 188.875, 228.215)), (' A 575  ASP  OD1', ' A 577  GLN  N  ', -0.545, (183.856, 140.868, 183.047)), (' C 143  VAL HG13', ' C 243  ILE HD11', -0.544, (158.175, 243.044, 171.758)), (' B 714  ASN  OD1', ' B 715  PHE  N  ', -0.542, (166.787, 168.35, 254.254)), (' C  53  ASP  OD1', ' C  54  LEU  N  ', -0.542, (175.358, 216.029, 185.822)), (' B  32  PHE  O  ', ' B  59  PHE  N  ', -0.539, (149.018, 156.841, 196.412)), (' C  81  ASN  O  ', ' C 239  GLN  NE2', -0.539, (175.0, 239.508, 171.077)), (' B 306  GLU  O  ', ' B 310  TYR  OH ', -0.539, (161.482, 167.086, 214.96)), (' C 909  THR HG23', ' C1103  GLN  HG2', -0.537, (182.995, 196.109, 260.755)), (' C 411  GLN  O  ', ' C 421  LYS  NZ ', -0.537, (210.19, 198.357, 138.988)), (' B 189  LEU HD21', ' B 191  GLU  OE2', -0.536, (151.26, 144.871, 191.963)), (' C 190  ARG  HE ', ' C 207  HIS  CE1', -0.536, (158.426, 234.507, 185.002)), (' C 287  ASP  OD1', ' C 289  ALA  N  ', -0.535, (181.871, 219.055, 196.346)), (' C 913  LEU HD12', ' C 920  ILE  CD1', -0.533, (172.447, 200.951, 254.866)), (' B 911  ASN  OD1', ' B 912  VAL  N  ', -0.533, (176.493, 171.741, 261.85)), (' B 575  ASP  OD1', ' B 578  THR  N  ', -0.533, (145.61, 207.214, 183.86)), (' C 284  ASP  OD1', ' C 285  ALA  N  ', -0.531, (170.634, 221.725, 200.462)), (' A  81  ASN  O  ', ' A 239  GLN  NE2', -0.53, (237.87, 165.125, 172.063)), (' B1132  ASN  OD1', ' B1133  THR  N  ', -0.53, (165.288, 188.569, 275.956)), (' C 453  PHE  CE2', ' J 103  GLY  HA3', -0.528, (221.261, 198.245, 123.045)), (' A 919  LEU HD11', ' A 923  GLN HE21', -0.527, (212.101, 182.097, 253.245)), (' B 738  TYR  CZ ', ' B 963  LEU HD21', -0.526, (186.368, 169.285, 195.496)), (' K  32  VAL  N  ', ' K  50  ASP  OD1', -0.525, (211.014, 193.388, 106.863)), (' A 143  VAL HG13', ' A 243  ILE HD11', -0.525, (248.85, 177.23, 172.541)), (' C1077  ALA  HB3', ' C1129  ILE HD12', -0.524, (202.583, 193.453, 267.072)), (' C 575  ASP  OD1', ' C 578  THR  N  ', -0.523, (223.668, 206.177, 183.742)), (' A 716  THR HG22', ' A1065  VAL  O  ', -0.523, (204.748, 177.245, 249.02)), (' C 733  VAL HG12', ' C 764  LEU HD12', -0.521, (169.722, 183.97, 204.457)), (' A 794  PHE  CE2', ' A 879  ILE HD13', -0.519, (206.344, 199.855, 246.223)), (' B 602  SER  OG ', ' B 603  ASN  N  ', -0.518, (150.065, 161.771, 213.874)), (' C 779  PHE  O  ', ' C 781  GLN  N  ', -0.517, (166.228, 183.288, 233.363)), (' B 307  LYS  HG3', ' B 661  ILE HD11', -0.517, (156.832, 168.401, 218.836)), (' B 454  ARG  NH1', ' B 456  SER  OG ', -0.517, (169.859, 209.624, 133.367)), (' C 193  VAL HG23', ' C 223  LEU HD22', -0.516, (168.328, 225.437, 186.154)), (' A  53  ASP  OD1', ' A  54  LEU  N  ', -0.515, (216.775, 176.646, 186.158)), (' A 286  VAL HG23', ' A 303  PHE  CE2', -0.513, (220.623, 176.819, 202.428)), (' B  53  ASP  OD1', ' B  54  LEU  N  ', -0.512, (161.504, 160.498, 186.556)), (' C 706  ASN  ND2', ' C1309  NAG  O7 ', -0.511, (208.356, 201.449, 259.452)), (' A 855  LEU  N  ', ' A 855  LEU HD12', -0.511, (198.154, 198.8, 200.464)), (' B 187  LYS  NZ ', ' B 213  VAL  O  ', -0.511, (140.267, 139.264, 191.139)), (' A 886  GLY  HA2', ' A1031  LEU HD22', -0.51, (191.342, 199.722, 241.164)), (' A 435  SER  OG ', ' A 439  ASP  OD2', -0.508, (182.822, 139.224, 140.605)), (' C 760  LEU  CD1', ' C1001  LEU  CD2', -0.507, (173.749, 182.915, 199.802)), (' L   4  LEU HD11', ' L  89  VAL HG22', -0.506, (168.109, 161.973, 102.792)), (' A  40  ASP  OD1', ' A  42  VAL  N  ', -0.506, (218.44, 190.093, 189.448)), (' A 332  LEU  O  ', ' A 332  LEU HD12', -0.505, (177.397, 140.248, 163.813)), (' C 141  LEU  O  ', ' C 244  SER  N  ', -0.505, (162.693, 244.357, 171.545)), (' B 788  THR HG21', ' B 803  LEU HD22', -0.503, (188.883, 156.851, 242.455)), (' A1097  THR  HG1', ' A1098  HIS  CE1', -0.501, (201.555, 164.691, 274.198)), (' B 448  TYR  C  ', ' B 449  LEU HD12', -0.5, (150.069, 212.601, 132.567)), (' B1088  ARG  NH1', ' B1115  ASP  O  ', -0.499, (180.391, 184.862, 270.208)), (' B1120  SER  OG ', ' C 915  GLU  OE2', -0.498, (176.318, 200.009, 266.645)), (' K   4  LEU HD11', ' K  89  VAL HG22', -0.498, (216.421, 193.924, 101.059)), (' A1036  ARG  NE ', ' B1028  GLU  OE2', -0.498, (186.864, 182.684, 237.697)), (' B  81  ASN  O  ', ' B 239  GLN  NE2', -0.498, (141.818, 148.667, 171.776)), (' C  96  GLU  HG3', ' C  98  SER  O  ', -0.497, (161.913, 240.854, 182.292)), (' A 903  PHE  HE1', ' A1046  LEU HD11', -0.497, (200.745, 185.619, 250.801)), (' C  30  ASN  OD1', ' C  32  PHE  N  ', -0.496, (177.388, 232.222, 195.498)), (' F  32  VAL  N  ', ' F  50  ASP  OD1', -0.495, (169.695, 202.023, 106.543)), (' A1038  ASP  HB3', ' B1027  SER  HB3', -0.495, (191.947, 177.203, 238.161)), (' B 143  VAL HG13', ' B 243  ILE HD11', -0.494, (146.148, 132.687, 172.68)), (' C 760  LEU HD13', ' C1001  LEU  CG ', -0.494, (173.72, 183.743, 200.343)), (' C1028  GLU  OE1', ' C1036  ARG  NH1', -0.494, (181.235, 186.274, 237.121)), (' C1029  CYS  O  ', ' C1048  SER  OG ', -0.493, (173.489, 192.299, 241.137)), (' B1078  ILE HD12', ' B1092  PHE  CZ ', -0.491, (169.206, 188.488, 269.369)), (' B 608  LEU HD22', ' B 663  ILE HG23', -0.489, (155.09, 179.039, 213.45)), (' C 419  ASN  OD1', ' C 451  ARG  N  ', -0.489, (223.096, 199.991, 134.124)), (' C 189  LEU HD21', ' C 191  GLU  OE2', -0.488, (167.062, 232.358, 191.172)), (' A 810  SER  O  ', ' A 812  ARG  N  ', -0.488, (210.531, 204.011, 231.012)), (' C 760  LEU HD12', ' C1001  LEU  CD2', -0.487, (173.151, 182.658, 200.02)), (' A1025  LYS  O  ', ' A1029  CYS  HB2', -0.485, (193.395, 190.014, 237.571)), (' B 819  LEU HD13', ' B1053  ALA  HB2', -0.485, (180.783, 162.384, 227.974)), (' B 810  SER  O  ', ' B 812  ARG  N  ', -0.485, (188.165, 152.533, 231.163)), (' A 960  VAL HG11', ' C 567  ALA  HB1', -0.484, (204.604, 193.318, 198.437)), (' C 799  PHE  HD2', ' C 802  ILE HD11', -0.483, (163.894, 198.894, 243.28)), (' A 867  ILE  O  ', ' A 871  THR HG23', -0.483, (201.24, 201.015, 231.065)), (' F   4  LEU HD11', ' F  89  VAL HG22', -0.482, (167.572, 206.687, 100.524)), (' A 794  PHE  HE2', ' A 879  ILE HD13', -0.481, (206.597, 199.395, 246.203)), (' A1079  CYS  HB2', ' A1129  ILE HD11', -0.48, (182.644, 163.674, 271.475)), (' B 305  VAL  HB ', ' B 599  THR HG23', -0.479, (158.526, 163.333, 212.042)), (' C 913  LEU HD12', ' C 920  ILE HD13', -0.479, (172.765, 200.808, 254.627)), (' B 194  PHE  HE1', ' B 203  ILE HG23', -0.479, (157.895, 147.512, 180.534)), (' B 895  PHE  CZ ', ' B1047  MET  HE1', -0.478, (183.228, 164.196, 248.366)), (' B 194  PHE  CE1', ' B 203  ILE HG23', -0.478, (157.541, 147.716, 180.182)), (' B 723  ILE HG21', ' B 942  LEU HD13', -0.477, (177.083, 165.711, 226.64)), (' A 328  ASN  N  ', ' A 328  ASN  OD1', -0.477, (182.474, 139.332, 177.493)), (' A 723  ILE HD13', ' A 942  LEU HD13', -0.474, (205.812, 187.177, 227.308)), (' B 323  ILE  N  ', ' B 537  ASN  O  ', -0.474, (150.199, 192.959, 183.938)), (' A 738  TYR  OH ', ' A 959  LEU  O  ', -0.474, (197.321, 191.554, 197.855)), (' B1048  SER  OG ', ' B1061  HIS  ND1', -0.473, (180.605, 171.094, 239.26)), (' B1091  VAL HG13', ' C 901  TYR  OH ', -0.473, (170.706, 186.364, 259.08)), (' K  34  TRP  O  ', ' K  46  VAL HG22', -0.472, (209.584, 203.348, 105.146)), (' B 919  LEU HD11', ' B 923  GLN HE21', -0.472, (167.938, 162.313, 253.452)), (' F  34  TRP  O  ', ' F  46  VAL HG22', -0.472, (161.328, 196.477, 104.056)), (' A 723  ILE HD12', ' A 941  ALA  O  ', -0.47, (205.238, 184.683, 227.222)), (' C 453  PHE  CE2', ' J 103  GLY  C  ', -0.47, (221.307, 198.201, 121.97)), (' B 719  VAL HG23', ' B 927  ALA  CB ', -0.47, (173.065, 163.152, 243.663)), (' B1029  CYS  SG ', ' B1045  HIS  NE2', -0.468, (181.625, 172.687, 242.115)), (' A 300  LEU HD11', ' A 310  TYR  CD2', -0.468, (208.775, 173.862, 210.55)), (' A 798  ASN  ND2', ' I   1  NAG  O7 ', -0.466, (216.171, 196.111, 247.267)), (' B 974  LEU HD11', ' B 990  ILE HG12', -0.466, (189.898, 170.384, 184.24)), (' C 733  VAL HG12', ' C 764  LEU  CD1', -0.464, (170.181, 184.302, 204.986)), (' C 595  ILE HD12', ' C 647  LEU HD11', -0.464, (193.397, 217.081, 213.154)), (' A 942  LEU  N  ', ' A 942  LEU HD22', -0.464, (208.321, 186.007, 226.106)), (' L  34  TRP  O  ', ' L  46  VAL HG22', -0.463, (180.128, 163.036, 105.813)), (' B 694  MET  HE3', ' B 696  LEU HD21', -0.463, (157.241, 183.377, 227.778)), (' B 529  ASN  OD1', ' B 530  LEU  N  ', -0.463, (142.056, 198.573, 184.02)), (' C 760  LEU HD12', ' C1001  LEU HD21', -0.463, (172.572, 182.851, 199.809)), (' A 719  VAL HG22', ' A1062  VAL HG22', -0.461, (205.463, 187.455, 243.107)), (' A 965  SER  HB2', ' A 967  PHE  CE2', -0.46, (197.032, 186.514, 191.502)), (' A 891  LEU  HB3', ' C 710  ALA  HB3', -0.459, (193.083, 205.163, 252.872)), (' A 788  THR HG21', ' A 803  LEU HD22', -0.459, (206.475, 202.481, 241.986)), (' A 313  SER  OG ', ' A 314  ASN  N  ', -0.458, (204.318, 166.116, 199.558)), (' B 119  ILE HG12', ' B 128  ILE HG23', -0.458, (158.702, 145.753, 171.863)), (' C 529  ASN  OD1', ' C 530  LEU  N  ', -0.458, (218.098, 214.444, 183.925)), (' A 673  THR  HA ', ' A 687  GLN  HA ', -0.458, (221.215, 159.417, 221.682)), (' A 793  ASP  N  ', ' A 793  ASP  OD1', -0.458, (210.03, 203.602, 252.054)), (' A 722  GLU  OE1', ' A1061  HIS  NE2', -0.457, (197.927, 185.362, 235.773)), (' A 454  ARG  NH1', ' A 456  SER  OG ', -0.457, (167.132, 159.777, 135.132)), (' C 205  SER  N  ', ' C 224  GLU  O  ', -0.457, (163.31, 223.377, 185.105)), (' A 714  ASN  OD1', ' A 715  PHE  N  ', -0.457, (207.352, 177.392, 254.457)), (' B 143  VAL HG12', ' B 154  GLU  HB3', -0.456, (147.823, 130.575, 172.124)), (' A1059  PHE  O  ', ' A1060  LEU HD23', -0.455, (204.534, 188.961, 235.107)), (' A 767  ILE HD11', ' A1009  LEU  HA ', -0.455, (188.28, 191.898, 211.591)), (' A 898  GLN  OE1', ' A 902  ARG  NH2', -0.454, (197.345, 194.19, 247.827)), (' B 767  ILE  O  ', ' B 771  GLN  HG2', -0.452, (191.994, 172.838, 216.14)), (' A 913  LEU HD12', ' A 920  ILE  CD1', -0.451, (204.948, 187.097, 255.115)), (' B1074  THR  OG1', ' B1075  ALA  N  ', -0.45, (163.96, 189.58, 262.971)), (' C 663  ILE HD11', ' C 669  ALA  HB2', -0.45, (193.362, 216.669, 217.53)), (' H   2  VAL HG22', ' H  27  ALA  HB2', -0.45, (184.129, 145.945, 117.299)), (' B 419  ASN  OD1', ' B 451  ARG  N  ', -0.449, (157.668, 209.223, 133.44)), (' C 119  ILE HG12', ' C 128  ILE HG23', -0.449, (164.02, 225.555, 171.252)), (' B 119  ILE HG23', ' B 128  ILE HG12', -0.449, (158.038, 143.622, 173.499)), (' J  16  GLU  O  ', ' J  85  VAL HG22', -0.448, (237.939, 209.637, 91.459)), (' J   2  VAL HG22', ' J  27  ALA  HB2', -0.447, (222.14, 213.05, 119.017)), (' A 187  LYS  NZ ', ' A 213  VAL  O  ', -0.447, (246.082, 169.304, 191.379)), (' B  65  PHE  CD1', ' B  65  PHE  N  ', -0.446, (140.916, 148.989, 182.919)), (' B 324  VAL  N  ', ' B 528  THR  OG1', -0.446, (148.171, 196.437, 181.438)), (' A 899  MET  HB2', ' A 913  LEU HD21', -0.446, (202.473, 191.106, 254.815)), (' A1025  LYS  O  ', ' A1029  CYS  CB ', -0.446, (193.594, 190.238, 237.709)), (' E  67  VAL HG13', ' E  80  LEU HD11', -0.445, (150.617, 216.842, 99.975)), (' B  40  ASP  OD1', ' B  42  VAL  N  ', -0.444, (172.188, 152.424, 190.4)), (' E   2  VAL HG22', ' E  27  ALA  HB2', -0.444, (146.619, 202.455, 116.762)), (' H  67  VAL HG13', ' H  80  LEU HD11', -0.443, (169.449, 142.87, 100.286)), (' A 189  LEU HD22', ' A 217  PRO  HG3', -0.443, (237.973, 174.613, 193.293)), (' A 119  ILE HG12', ' A 128  ILE HG23', -0.442, (231.173, 181.58, 171.786)), (' A1031  LEU HD13', ' C1038  ASP  OD2', -0.442, (188.992, 198.1, 239.366)), (' H  16  GLU  O  ', ' H  85  VAL HG22', -0.442, (170.127, 136.842, 90.024)), (' H   2  VAL HG22', ' H  27  ALA  CB ', -0.442, (183.969, 146.103, 116.729)), (' B1048  SER  HG ', ' B1061  HIS  HD1', -0.441, (180.845, 171.288, 239.833)), (' E  16  GLU  O  ', ' E  85  VAL HG22', -0.441, (144.091, 220.247, 90.621)), (' C1102  THR  OG1', ' C1108  GLU  N  ', -0.441, (185.702, 201.943, 263.131)), (' A 663  ILE HD11', ' A 669  ALA  CB ', -0.44, (207.639, 161.575, 217.895)), (' E   2  VAL HG22', ' E  27  ALA  CB ', -0.44, (146.518, 202.66, 116.489)), (' A 277  ASN  C  ', ' A 277  ASN  OD1', -0.44, (224.588, 190.567, 201.916)), (' A 529  ASN  OD1', ' A 530  LEU  N  ', -0.439, (193.432, 140.417, 184.25)), (' C 855  LEU HD21', ' C 959  LEU HD23', -0.439, (169.845, 190.881, 202.547)), (' C  96  GLU  CG ', ' C  98  SER  O  ', -0.439, (161.282, 240.939, 182.732)), (' A 704  TYR  CD1', ' B 880  THR HG22', -0.438, (191.424, 159.405, 250.426)), (' A  21  ARG  NH2', ' A 137  ASN  O  ', -0.438, (239.526, 163.872, 166.929)), (' J  67  VAL HG13', ' J  80  LEU HD11', -0.438, (232.885, 204.204, 100.785)), (' J  90  THR HG23', ' J 119  THR  HA ', -0.438, (227.679, 213.299, 89.367)), (' C 453  PHE  CE2', ' J 103  GLY  CA ', -0.437, (221.009, 198.634, 122.883)), (' C 653  VAL HG12', ' C 654  ASN  N  ', -0.435, (198.724, 223.837, 224.741)), (' A 139  PRO  HB3', ' A 159  VAL HG13', -0.435, (239.335, 172.425, 167.166)), (' B1094  SER  HB2', ' B1099  TRP  CD2', -0.435, (161.516, 185.905, 268.579)), (' B 106  PHE  HB3', ' B 235  ILE HD13', -0.435, (155.532, 153.432, 172.619)), (' B 109  THR  OG1', ' B 114  THR  OG1', -0.435, (152.213, 156.717, 163.124)), (' J   2  VAL HG22', ' J  27  ALA  CB ', -0.435, (222.076, 212.786, 118.411)), (' A 767  ILE  O  ', ' A 771  GLN  HG2', -0.435, (191.23, 197.041, 216.048)), (' A 819  LEU HD21', ' A 935  LEU HD13', -0.433, (209.156, 189.75, 230.567)), (' A  30  ASN  OD1', ' A  32  PHE  N  ', -0.432, (229.575, 166.938, 195.951)), (' B 390  THR  N  ', ' B 513  GLU  O  ', -0.431, (164.023, 205.631, 161.786)), (' B 723  ILE  O  ', ' B 724  LEU HD23', -0.431, (178.411, 171.912, 228.4)), (' C1045  HIS  NE2', ' C1048  SER  OG ', -0.431, (174.801, 193.396, 242.228)), (' L  27  ILE HG22', ' L  68  ASN  HA ', -0.431, (164.815, 171.024, 103.471)), (' B 481  LYS  HE2', ' E  54  THR HG21', -0.431, (154.826, 219.023, 119.688)), (' C 220  PHE  CE2', ' C 284  ASP  HA ', -0.43, (168.68, 222.788, 199.507)), (' B 108  THR HG22', ' B 236  THR HG23', -0.43, (153.129, 160.504, 170.264)), (' C  65  PHE  CD1', ' C  65  PHE  N  ', -0.43, (175.64, 239.568, 181.986)), (' A1083  LYS  HB3', ' A1119  VAL HG13', -0.429, (178.512, 169.896, 273.754)), (' H  90  THR HG23', ' H 119  THR  HA ', -0.429, (178.04, 143.842, 87.686)), (' K  27  ILE HG22', ' K  68  ASN  HA ', -0.428, (210.129, 186.723, 100.173)), (' B 328  ASN  O  ', ' B 329  ILE  C  ', -0.427, (146.992, 208.941, 174.087)), (' B 802  ILE HG22', ' B 815  ILE HD12', -0.427, (179.966, 158.798, 237.328)), (' C 861  LEU  HG ', ' C 862  LEU HD12', -0.427, (160.568, 182.864, 223.047)), (' B 193  VAL HG23', ' B 223  LEU HD22', -0.427, (156.583, 149.573, 187.186)), (' H 108  THR  OG1', ' L  45  LEU HD13', -0.427, (177.355, 159.691, 108.805)), (' A 911  ASN  ND2', ' A1108  GLU  OE2', -0.426, (199.268, 182.296, 264.687)), (' B1136  ASP  OD1', ' B1138  LEU  N  ', -0.426, (178.407, 184.986, 281.904)), (' C 786  TYR  OH ', ' C 890  ALA  HB2', -0.426, (161.356, 182.419, 245.091)), (' C1097  THR  HG1', ' C1098  HIS  CE1', -0.426, (194.003, 209.304, 274.442)), (' A 886  GLY  CA ', ' A1031  LEU HD22', -0.426, (190.909, 199.503, 241.741)), (' B 613  ASN  OD1', ' B 614  CYS  N  ', -0.426, (145.344, 186.907, 206.714)), (' A1047  MET  HE3', ' A1049  PHE  CZ ', -0.425, (203.193, 192.053, 245.02)), (' J 108  THR  OG1', ' K  45  LEU HD13', -0.425, (213.745, 202.084, 108.273)), (' C 453  PHE  CD1', ' C 453  PHE  N  ', -0.425, (222.214, 197.327, 127.289)), (' J  78  PHE  HZ ', ' J  95  CYS  HB2', -0.424, (226.659, 209.576, 108.181)), (' C 109  THR  OG1', ' C 114  THR  HB ', -0.424, (176.81, 225.381, 162.189)), (' B  64  TRP  HB3', ' B 263  TYR  CD2', -0.424, (142.854, 149.488, 188.015)), (' H  78  PHE  HZ ', ' H  95  CYS  HB2', -0.424, (177.607, 144.785, 106.948)), (' A1079  CYS  HB2', ' A1129  ILE  CD1', -0.423, (182.59, 163.621, 271.463)), (' A 300  LEU HD11', ' A 310  TYR  CE2', -0.423, (209.067, 174.188, 211.175)), (' B 194  PHE  HB3', ' B 201  PHE  CZ ', -0.422, (156.931, 151.792, 177.875)), (' E  90  THR HG23', ' E 119  THR  HA ', -0.422, (145.365, 209.574, 87.675)), (' B1069  GLU  OE2', ' C 889  ALA  HB3', -0.422, (161.654, 176.543, 249.59)), (' A 911  ASN  OD1', ' A 912  VAL  N  ', -0.422, (200.607, 184.186, 261.846)), (' C 613  ASN  OD1', ' C 614  CYS  N  ', -0.421, (205.591, 216.825, 206.414)), (' A 901  TYR  OH ', ' C1091  VAL HG13', -0.421, (193.013, 196.272, 258.828)), (' C 723  ILE HG23', ' C1058  VAL HG22', -0.42, (171.344, 198.756, 228.805)), (' C 704  TYR  CD1', ' C 705  SER  N  ', -0.42, (204.012, 205.071, 253.026)), (' B1087  PRO  HA ', ' B1117  THR HG22', -0.419, (173.774, 188.114, 267.722)), (' A 706  ASN  ND2', ' A1307  NAG  O7 ', -0.419, (187.922, 155.362, 259.573)), (' C1071  ASN  OD1', ' C1310  NAG  N2 ', -0.419, (195.139, 211.666, 255.369)), (' L  90  TRP  NE1', ' L  95  ASP  OD1', -0.419, (164.199, 154.333, 109.683)), (' C 291  ASP  OD1', ' C 293  LEU  N  ', -0.418, (183.876, 220.748, 204.611)), (' B 279  ASN  OD1', ' B1304  NAG  N2 ', -0.418, (170.247, 141.851, 203.739)), (' A  91  TYR  OH ', ' A 191  GLU  OE1', -0.418, (232.355, 174.729, 190.172)), (' B 307  LYS  CG ', ' B 661  ILE HD11', -0.418, (156.986, 168.544, 219.347)), (' A1028  GLU  OE2', ' C1036  ARG  NE ', -0.416, (185.035, 187.632, 237.694)), (' A 293  LEU HD11', ' A 297  LYS  HE3', -0.416, (217.658, 171.108, 207.8)), (' A1002  GLN  NE2', ' C1003  THR  OG1', -0.415, (182.203, 189.592, 200.339)), (' A1074  THR  OG1', ' A1075  ALA  N  ', -0.415, (191.338, 164.498, 262.906)), (' C1025  LYS  O  ', ' C1029  CYS  HB2', -0.415, (175.485, 189.752, 238.046)), (' A 911  ASN  C  ', ' A 911  ASN  OD1', -0.414, (200.737, 184.569, 262.515)), (' C 802  ILE HG22', ' C 815  ILE HD12', -0.414, (164.569, 201.887, 237.502)), (' A  31  SER  OG ', ' A  60  SER  N  ', -0.414, (226.556, 166.439, 193.006)), (' C 388  CYS  HB3', ' C 519  ALA  HB1', -0.413, (214.796, 196.63, 167.581)), (' B 899  MET  SD ', ' B1047  MET  HE2', -0.413, (181.314, 166.323, 248.655)), (' A  65  PHE  CD1', ' A  65  PHE  N  ', -0.413, (237.137, 164.317, 182.841)), (' C 287  ASP  O  ', ' C 294  SER  HB3', -0.413, (180.079, 219.411, 200.222)), (' A 932  GLN  O  ', ' A 936  SER  N  ', -0.413, (214.831, 187.702, 232.241)), (' B  49  HIS  CE1', ' B  51  THR HG23', -0.412, (168.967, 159.85, 193.646)), (' C 966  ASN  OD1', ' C 972  SER  N  ', -0.411, (172.878, 196.092, 185.721)), (' B  48  LEU  HB3', ' B 273  LEU HD11', -0.411, (166.36, 159.186, 201.628)), (' C1103  GLN  NE2', ' C1108  GLU  OE1', -0.411, (182.329, 198.29, 263.251)), (' B 924  PHE  HE2', ' B1062  VAL HG11', -0.411, (178.291, 164.797, 245.933)), (' C 719  VAL HG22', ' C1062  VAL HG22', -0.409, (171.461, 201.882, 243.298)), (' C 114  THR HG22', ' C 115  GLN  N  ', -0.409, (174.27, 222.984, 162.436)), (' E 100  CYS  HA ', ' E 105  CYS  HA ', -0.409, (159.024, 205.761, 116.486)), (' A 724  LEU HD11', ' A1025  LYS  HD2', -0.409, (195.068, 187.919, 232.007)), (' A 663  ILE HD11', ' A 669  ALA  HB2', -0.408, (207.968, 161.147, 217.926)), (' H  18  LEU HD22', ' H 118  VAL HG11', -0.408, (175.45, 140.76, 92.789)), (' B 924  PHE  CE2', ' B1062  VAL HG11', -0.408, (177.922, 165.073, 246.072)), (' C 108  THR HG22', ' C 236  THR HG23', -0.407, (179.335, 223.293, 169.434)), (' B 109  THR  OG1', ' B 111  ASP  OD1', -0.407, (150.879, 156.155, 162.439)), (' A 726  VAL HG23', ' A1056  GLY  HA2', -0.407, (198.431, 192.955, 225.466)), (' B 705  SER  OG ', ' B 706  ASN  N  ', -0.407, (156.677, 192.146, 256.818)), (' B 983  PRO  N  ', ' B 984  PRO  CD ', -0.407, (192.464, 173.577, 173.67)), (' A 417  ASP  O  ', ' A 458  LEU  N  ', -0.407, (171.557, 158.803, 136.989)), (' C 723  ILE  O  ', ' C 724  LEU HD23', -0.407, (176.601, 195.65, 228.623)), (' A 193  VAL HG23', ' A 223  LEU HD22', -0.406, (228.731, 178.196, 187.443)), (' A 332  LEU  C  ', ' A 332  LEU HD12', -0.406, (177.829, 140.639, 164.277)), (' E 108  THR  OG1', ' F  45  LEU HD13', -0.406, (160.547, 200.579, 107.253)), (' C 190  ARG  HB3', ' C 192  PHE  CZ ', -0.406, (162.948, 231.818, 183.544)), (' A 552  SER  OG ', ' A 581  ILE  O  ', -0.406, (183.07, 142.623, 195.185)), (' C  63  THR HG22', ' C  65  PHE  CZ ', -0.405, (179.151, 237.67, 181.253)), (' C 347  VAL HG21', ' C 415  ILE HG23', -0.405, (220.615, 202.543, 138.734)), (' A  29  THR HG22', ' A  30  ASN  N  ', -0.405, (233.058, 164.245, 193.16)), (' C 453  PHE  HE2', ' J 103  GLY  C  ', -0.405, (221.647, 197.951, 122.116)), (' A1043  GLY  HA2', ' B 887  ALA  CB ', -0.405, (197.66, 176.624, 245.261)), (' F  82  GLU  HA ', ' F 105  LEU  O  ', -0.404, (159.58, 188.835, 93.287)), (' C 278  GLU  HB2', ' C1304  NAG  H82', -0.404, (155.942, 216.169, 204.386)), (' C1072  PHE  CZ ', ' C1107  TYR  CE1', -0.404, (189.357, 206.97, 263.212)), (' B  63  THR HG22', ' B  65  PHE  CZ ', -0.404, (140.607, 153.051, 182.192)), (' B 801  GLN  NE2', ' B 932  GLN  OE1', -0.403, (175.069, 152.958, 239.329)), (' C 723  ILE HD12', ' C 941  ALA  O  ', -0.403, (173.978, 202.777, 227.544)), (' A 565  ASP  OD1', ' A 566  ILE  N  ', -0.403, (178.631, 156.453, 200.93)), (' J 100  CYS  HA ', ' J 105  CYS  HA ', -0.403, (219.293, 200.385, 117.198)), (' J  18  LEU HD22', ' J 118  VAL HG11', -0.402, (231.916, 211.515, 94.51)), (' C 194  PHE  HB3', ' C 201  PHE  CZ ', -0.402, (169.973, 224.236, 177.318)), (' A 189  LEU HD22', ' A 217  PRO  CG ', -0.401, (237.66, 174.187, 193.675)), (' K  82  GLU  HA ', ' K 105  LEU  O  ', -0.401, (203.239, 209.669, 95.549)), (' B 481  LYS  CE ', ' E  54  THR HG21', -0.401, (155.043, 219.143, 120.279)), (' B 719  VAL HG23', ' B 927  ALA  HB1', -0.401, (172.711, 163.534, 243.424)), (' A1139  GLN  N  ', ' A1140  PRO  HD2', -0.4, (189.407, 179.328, 283.936)), (' C1045  HIS  CD2', ' C1046  LEU  N  ', -0.4, (176.56, 195.305, 245.152))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
