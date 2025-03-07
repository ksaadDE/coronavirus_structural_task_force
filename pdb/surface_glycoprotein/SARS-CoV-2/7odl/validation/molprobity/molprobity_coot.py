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
data['rama'] = [('A', ' 676 ', 'THR', 0.01699616911673207, (156.42100000000002, 88.29100000000003, 106.72300000000001)), ('A', '1133 ', 'VAL', 0.009871437307095615, (146.552, 53.567000000000014, 158.50300000000001)), ('C', ' 676 ', 'THR', 0.013004743155122473, (132.29199999999994, 138.441, 156.872))]
data['omega'] = []
data['rota'] = [('A', '  36 ', 'VAL', 0.14242638792813486, (143.105, 115.248, 88.48100000000001)), ('A', '  90 ', 'VAL', 0.17041893043987666, (137.957, 113.31, 77.378)), ('A', ' 189 ', 'LEU', 0.1313840774123074, (154.095, 116.68300000000004, 78.116)), ('A', ' 191 ', 'GLU', 0.17918642124857304, (147.46600000000007, 117.131, 79.344)), ('A', ' 270 ', 'LEU', 0.1981768032091204, (135.779, 110.287, 82.515)), ('A', ' 273 ', 'ARG', 0.02368339488286539, (133.116, 109.05500000000004, 90.85800000000002)), ('A', ' 293 ', 'LEU', 1.6159598001214054e-05, (138.34, 101.389, 93.085)), ('A', ' 297 ', 'SER', 0.16878106935613685, (140.291, 102.268, 99.00800000000001)), ('A', '1133 ', 'VAL', 0.26048117610699956, (146.552, 53.567000000000014, 158.50300000000001)), ('A', '1136 ', 'THR', 0.12826157289629825, (152.118, 54.90700000000001, 166.07200000000003)), ('B', '  34 ', 'ARG', 0.0006212136902497388, (79.059, 92.857, 109.885)), ('B', '  41 ', 'LYS', 0.0, (93.022, 98.44300000000003, 95.825)), ('B', '  90 ', 'VAL', 0.14382935026844573, (74.39600000000002, 103.384, 104.987)), ('B', '  94 ', 'SER', 0.15334529101154898, (68.5, 91.93600000000002, 102.927)), ('B', '  95 ', 'THR', 0.024212062972997453, (67.465, 88.254, 103.384)), ('B', ' 606 ', 'ASN', 0.28368757203415085, (87.332, 87.318, 128.105)), ('C', '1133 ', 'VAL', 0.2141631975308292, (166.87, 88.794, 172.63000000000002))]
data['cbeta'] = []
data['probe'] = [(' B1302  NAG  O3 ', ' B1302  NAG  O7 ', -0.762, (68.19, 124.64, 82.474)), (' A 457  ARG  NH1', ' A 467  ASP  OD2', -0.746, (72.882, 124.839, 95.229)), (' A  34  ARG  NH2', ' A 191  GLU  OE2', -0.73, (151.114, 114.463, 82.918)), (' C1050  MET  HE2', ' C1052  PHE  CZ ', -0.708, (122.444, 95.861, 166.247)), (' C1311  NAG  O3 ', ' C1311  NAG  O7 ', -0.705, (173.715, 89.707, 177.026)), (' B1134  ASN  HB3', ' B1311  NAG  HN2', -0.69, (127.789, 78.154, 191.35)), (' A  36  VAL  O  ', ' A 222  ALA  HA ', -0.666, (145.257, 117.216, 88.089)), (' B 569  ILE  H  ', ' B 569  ILE HD12', -0.664, (101.626, 128.967, 132.938)), (' C 324  GLU  OE2', ' C 534  VAL HG21', -0.66, (137.963, 151.048, 109.491)), (' A 294  ASP  HB3', ' A 295  PRO  HD2', -0.642, (140.576, 97.174, 96.654)), (' C1087  ALA  O  ', ' C1122  VAL HG23', -0.639, (162.258, 77.842, 169.489)), (' A  40  ASP  OD2', ' A  44  ARG  NH2', -0.637, (135.676, 124.096, 97.307)), (' A 674  TYR  OH ', ' A 690  GLN  HG3', -0.628, (153.906, 91.426, 103.032)), (' A 324  GLU  OE2', ' A 534  VAL HG21', -0.625, (116.68, 92.804, 79.054)), (' A1087  ALA  O  ', ' A1122  VAL HG23', -0.618, (141.658, 59.104, 168.245)), (' A 638  THR HG22', ' A 639  GLY  H  ', -0.613, (139.615, 82.723, 92.838)), (' C 371  SER  OG ', ' C1305  NAG  H83', -0.61, (114.807, 153.935, 79.081)), (' A 864  LEU HD11', ' C 697  MET  HE1', -0.601, (139.774, 122.608, 145.367)), (' C1050  MET  HE2', ' C1052  PHE  CE1', -0.593, (122.531, 95.196, 166.146)), (' A 326  ILE HD12', ' A 532  ASN  O  ', -0.592, (112.069, 93.806, 78.602)), (' A 704  SER  O  ', ' A 705  VAL HG23', -0.589, (144.974, 67.649, 134.152)), (' B 617  CYS  O  ', ' B 618  THR  OG1', -0.585, (81.419, 106.05, 146.694)), (' C1303  NAG  O3 ', ' C1303  NAG  O7 ', -0.582, (116.367, 158.922, 104.425)), (' C 638  THR HG22', ' C 639  GLY  H  ', -0.582, (140.53, 146.043, 138.528)), (' B 689  SER  O  ', ' B 690  GLN  HG2', -0.575, (83.996, 80.036, 135.32)), (' C 671  CYS  SG ', ' C 697  MET  HE2', -0.575, (139.421, 124.523, 146.803)), (' A 190  ARG  HD3', ' A 207  HIS  CD2', -0.574, (150.519, 122.11, 77.366)), (' A 170  TYR  OH ', ' A 173  GLN  OE1', -0.574, (143.878, 135.644, 73.224)), (' B1302  NAG  C7 ', ' B1302  NAG  HO3', -0.557, (68.573, 123.536, 82.296)), (' C 785  VAL HG22', ' C 787  GLN  H  ', -0.557, (111.923, 85.841, 156.382)), (' A 755  GLN  N  ', ' A 755  GLN  OE1', -0.548, (112.65, 132.311, 118.951)), (' C 131  CYS  HA ', ' C 166  CYS  HB3', -0.541, (100.303, 168.94, 107.662)), (' A 675  GLN  O  ', ' A 677  GLN  N  ', -0.54, (156.902, 87.24, 108.296)), (' C 638  THR HG22', ' C 639  GLY  N  ', -0.539, (140.256, 146.408, 138.311)), (' A  58  PHE  CE1', ' A 275  PHE  CE2', -0.534, (141.509, 109.827, 90.683)), (' C 170  TYR  OH ', ' C 173  GLN  OE1', -0.533, (90.23, 163.121, 122.482)), (' C 675  GLN  O  ', ' C 677  GLN  N  ', -0.528, (133.302, 137.129, 158.067)), (' C 457  ARG  NH1', ' C 467  ASP  OD2', -0.524, (117.511, 120.234, 66.908)), (' A 988  GLU  OE1', ' C 383  SER  OG ', -0.524, (115.166, 136.851, 98.317)), (' B 689  SER  C  ', ' B 690  GLN  HG2', -0.523, (83.821, 80.659, 135.331)), (' A  34  ARG  NH2', ' A 189  LEU HD21', -0.516, (151.689, 114.309, 82.121)), (' B 131  CYS  HA ', ' B 166  CYS  HB3', -0.516, (67.706, 114.157, 85.506)), (' A 790  LYS  O  ', ' C 705  VAL HG21', -0.515, (156.078, 109.428, 158.323)), (' B 130  VAL  O  ', ' B 166  CYS  HB2', -0.514, (69.879, 113.367, 85.942)), (' A 131  CYS  HA ', ' A 166  CYS  HB3', -0.513, (129.466, 128.461, 62.36)), (' B1309  NAG  O3 ', ' B1309  NAG  O7 ', -0.512, (125.955, 54.363, 139.005)), (' B1311  NAG  O3 ', ' B1311  NAG  O7 ', -0.51, (125.367, 79.345, 194.605)), (' A 638  THR HG22', ' A 639  GLY  N  ', -0.507, (139.905, 83.215, 92.838)), (' B 122  ASN  OD1', ' B 125  ASN  N  ', -0.505, (65.418, 95.701, 83.281)), (' A  34  ARG HH21', ' A 189  LEU HD21', -0.505, (151.615, 113.599, 82.295)), (' A 843  ASP  N  ', ' A 843  ASP  OD1', -0.505, (148.232, 133.376, 111.384)), (' B1077  THR HG23', ' C 900  MET  HE1', -0.5, (124.396, 81.03, 177.734)), (' B1122  VAL  O  ', ' B1122  VAL HG13', -0.497, (143.491, 81.455, 183.703)), (' C  29  THR HG22', ' C  30  ASN  H  ', -0.494, (119.999, 161.035, 138.141)), (' B 731  MET  HE1', ' B1015  ALA  HB2', -0.493, (125.098, 96.903, 123.901)), (' A 190  ARG  HD3', ' A 207  HIS  NE2', -0.492, (150.832, 122.431, 76.654)), (' C 130  VAL  O  ', ' C 166  CYS  HB2', -0.491, (99.361, 167.37, 107.984)), (' B 865  LEU HD22', ' B 869  MET  HE2', -0.49, (137.317, 80.775, 121.439)), (' C 945  LEU HD22', ' C 948  LEU HD12', -0.488, (116.684, 110.743, 153.195)), (' A 281  GLU  OE2', ' A1305  NAG  H5 ', -0.488, (156.149, 124.702, 102.887)), (' C  29  THR HG22', ' C  30  ASN  N  ', -0.488, (120.137, 160.557, 137.902)), (' A 165  ASN  C  ', ' A 165  ASN  OD1', -0.481, (126.27, 129.773, 60.19)), (' C 485  GLY  O  ', ' C 487  ASN  N  ', -0.48, (103.637, 113.722, 53.536)), (' A 294  ASP  HB3', ' A 295  PRO  CD ', -0.479, (140.336, 97.289, 96.915)), (' C 704  SER  O  ', ' C 705  VAL HG23', -0.478, (153.875, 110.492, 160.618)), (' B  29  THR HG22', ' B  30  ASN  N  ', -0.478, (70.306, 92.883, 115.48)), (' B 606  ASN  ND2', ' B 606  ASN  O  ', -0.478, (86.384, 89.37, 127.016)), (' A  58  PHE  CE1', ' A 275  PHE  HE2', -0.477, (142.232, 110.012, 90.828)), (' A 786  LYS  HA ', ' A 786  LYS  HE2', -0.476, (142.864, 114.188, 154.722)), (' B 902  MET  HE1', ' B1049  LEU HD13', -0.469, (130.547, 70.45, 151.272)), (' A 117  LEU HD13', ' A 130  VAL HG22', -0.469, (132.805, 126.339, 69.018)), (' A 164  ASN  OD1', ' A1303  NAG  H61', -0.468, (124.639, 130.371, 54.428)), (' B1050  MET  HE2', ' B1052  PHE  CZ ', -0.468, (132.161, 70.369, 143.495)), (' A 298  GLU  OE1', ' A 315  THR HG22', -0.467, (135.18, 99.196, 103.161)), (' B1090  PRO  O  ', ' B1091  ARG  HB3', -0.466, (137.939, 76.727, 175.447)), (' C 228  ASP  O  ', ' C 228  ASP  OD1', -0.466, (97.34, 153.923, 116.966)), (' A 804  GLN  NE2', ' A1310  NAG  H62', -0.465, (166.421, 102.935, 141.963)), (' B 689  SER  OG ', ' B 690  GLN  N  ', -0.464, (82.538, 81.862, 136.349)), (' C1091  ARG HH21', ' C1121  PHE  HB3', -0.464, (153.736, 76.045, 169.307)), (' A 122  ASN  OD1', ' A 125  ASN  N  ', -0.463, (148.309, 131.676, 64.15)), (' B 638  THR HG22', ' B 639  GLY  N  ', -0.463, (78.578, 99.751, 138.044)), (' B 704  SER  OG ', ' B 705  VAL  N  ', -0.459, (108.551, 82.949, 167.965)), (' B1105  THR  OG1', ' B1106  GLN  N  ', -0.454, (129.519, 72.068, 170.475)), (' C 102  ARG  NH1', ' C 122  ASN  HA ', -0.452, (97.629, 174.646, 126.577)), (' C 131  CYS  HA ', ' C 166  CYS  CB ', -0.449, (99.674, 168.753, 107.615)), (' C 897  PRO  HG2', ' C 900  MET  HE3', -0.448, (123.592, 83.146, 177.216)), (' C 442  ASP  O  ', ' C 448  ASN  ND2', -0.447, (106.902, 142.598, 63.402)), (' A  91  TYR  CD2', ' A  91  TYR  O  ', -0.446, (143.268, 111.716, 78.528)), (' B 675  GLN  HG3', ' B 693  ILE HG23', -0.446, (88.464, 85.386, 142.314)), (' C  94  SER  OG ', ' C 101  ILE HD13', -0.446, (107.307, 168.777, 133.476)), (' A  29  THR  O  ', ' A  61  ASN  HA ', -0.444, (145.203, 101.712, 79.598)), (' B 126  VAL HG12', ' B 173  GLN  HG2', -0.443, (72.458, 96.111, 84.714)), (' C 105  ILE HG22', ' C 118  LEU HD12', -0.443, (104.033, 171.213, 118.164)), (' C1090  PRO  O  ', ' C1091  ARG  HB3', -0.441, (152.185, 81.72, 170.937)), (' A 704  SER  OG ', ' A 705  VAL  N  ', -0.441, (148.217, 65.724, 133.954)), (' B 726  ILE HG12', ' B1061  VAL HG22', -0.439, (121.429, 79.582, 134.349)), (' A 165  ASN  O  ', ' A 165  ASN  OD1', -0.438, (125.977, 129.296, 60.417)), (' B 189  LEU  HG ', ' B 189  LEU  O  ', -0.438, (73.653, 88.594, 102.859)), (' C1080  ALA  HB3', ' C1132  ILE HG13', -0.438, (163.973, 85.319, 168.238)), (' A 973  ILE HD12', ' A 983  ARG HH22', -0.436, (122.03, 130.762, 98.578)), (' B 704  SER  O  ', ' B 705  VAL HG23', -0.436, (109.862, 85.656, 166.399)), (' A 293  LEU  HG ', ' A 293  LEU  O  ', -0.433, (140.303, 100.159, 92.607)), (' C 127  VAL HG13', ' C 171  VAL HG22', -0.433, (93.539, 170.061, 117.156)), (' A 131  CYS  HA ', ' A 166  CYS  CB ', -0.433, (129.196, 129.065, 62.832)), (' C 126  VAL HG12', ' C 173  GLN  HG2', -0.432, (92.327, 166.268, 124.177)), (' A 957  GLN  O  ', ' A 961  THR HG23', -0.43, (135.283, 113.75, 117.216)), (' A 165  ASN  O  ', ' A 166  CYS  HB3', -0.43, (128.085, 129.298, 61.202)), (' B1311  NAG  C7 ', ' B1311  NAG  HO3', -0.43, (125.885, 78.621, 194.221)), (' C 981  LEU HD21', ' C 993  ILE HD11', -0.429, (96.043, 122.52, 112.246)), (' A 130  VAL  O  ', ' A 166  CYS  HB2', -0.427, (129.571, 129.134, 64.277)), (' A 296  LEU  HG ', ' A 296  LEU  O  ', -0.426, (142.408, 100.751, 101.088)), (' C 641  ASN  O  ', ' C 641  ASN  OD1', -0.425, (140.599, 142.917, 143.045)), (' C 689  SER  O  ', ' C 690  GLN  HG3', -0.424, (131.36, 141.836, 156.42)), (' B 878  LEU HD21', ' B1052  PHE  HB3', -0.424, (131.098, 71.812, 138.045)), (' B 520  ALA  HB1', ' B 521  PRO  HD2', -0.424, (92.502, 144.927, 122.103)), (' B 452  LEU HD23', ' B 494  SER  HA ', -0.424, (101.804, 163.288, 86.869)), (' A  29  THR HG22', ' A  30  ASN  N  ', -0.424, (148.845, 102.399, 79.878)), (' B 325  SER  O  ', ' B 326  ILE HD13', -0.423, (76.603, 126.618, 121.673)), (' A1090  PRO  O  ', ' A1091  ARG  HB3', -0.422, (146.231, 68.358, 164.904)), (' C  35  GLY  O  ', ' C  36  VAL HG23', -0.421, (111.217, 150.244, 132.562)), (' A 228  ASP  O  ', ' A 228  ASP  OD1', -0.419, (133.798, 130.084, 80.14)), (' B 794  ILE  O  ', ' B 794  ILE HG23', -0.416, (140.547, 58.053, 138.788)), (' A 165  ASN  HB3', ' A1303  NAG  O5 ', -0.416, (124.219, 130.648, 57.51)), (' A 108  THR HG23', ' A 234  ASN  O  ', -0.415, (126.913, 117.874, 68.483)), (' C 745  ASP  N  ', ' C 745  ASP  OD1', -0.412, (92.716, 119.153, 122.292)), (' A 904  TYR  OH ', ' C1094  VAL HG13', -0.411, (151.964, 91.2, 167.897)), (' B 108  THR HG23', ' B 234  ASN  O  ', -0.411, (70.084, 116.107, 98.202)), (' B 632  THR  O  ', ' B 635  VAL HG22', -0.408, (81.243, 105.98, 136.285)), (' B  63  THR HG22', ' B  64  TRP  N  ', -0.408, (64.355, 98.267, 111.817)), (' C 704  SER  OG ', ' C 705  VAL  N  ', -0.406, (155.008, 111.756, 163.788)), (' A 172  SER  O  ', ' A 173  GLN  C  ', -0.406, (146.18, 136.172, 69.246)), (' A 785  VAL HG22', ' A 787  GLN  H  ', -0.404, (144.666, 110.833, 157.069))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
