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
data['rama'] = [('L', ' 385 ', 'THR', 0.021976030063421026, (92.794, 68.252, 75.545)), ('L', ' 522 ', 'ALA', 0.018738089575331417, (105.18200000000003, 51.17000000000001, 73.789))]
data['omega'] = [('A', ' 161 ', 'PRO', None, (67.854, -18.257, -2.8)), ('A', ' 163 ', 'PRO', None, (67.186, -13.703999999999995, -6.961000000000002)), ('B', '   8 ', 'PRO', None, (36.478, -4.715, -15.184)), ('B', '  95 ', 'PRO', None, (39.32, -2.59, 8.304)), ('B', ' 141 ', 'PRO', None, (44.97, -14.313000000000004, -27.74)), ('D', ' 161 ', 'PRO', None, (9.167, 82.936, 65.884)), ('D', ' 163 ', 'PRO', None, (15.153999999999986, 84.361, 66.414)), ('E', '   8 ', 'PRO', None, (33.804, 61.71599999999998, 81.888)), ('E', '  95 ', 'PRO', None, (22.158, 51.036, 64.248)), ('E', ' 141 ', 'PRO', None, (31.253, 76.21099999999998, 90.802)), ('G', ' 161 ', 'PRO', None, (77.99899999999997, 13.052, 56.383)), ('G', ' 163 ', 'PRO', None, (79.82699999999994, 10.664, 51.029)), ('H', '   8 ', 'PRO', None, (79.804, 31.263, 24.887)), ('H', '  95 ', 'PRO', None, (92.62099999999995, 40.84499999999998, 42.536)), ('H', ' 141 ', 'PRO', None, (67.241, 19.456, 24.209)), ('J', ' 161 ', 'PRO', None, (64.469, 105.98499999999996, 79.705)), ('J', ' 163 ', 'PRO', None, (60.27799999999994, 101.383, 78.6)), ('K', '   8 ', 'PRO', None, (64.495, 85.15800000000006, 49.943)), ('K', '  95 ', 'PRO', None, (84.072, 82.293, 63.48200000000001)), ('K', ' 141 ', 'PRO', None, (50.006, 97.78, 50.532000000000004))]
data['rota'] = [('A', ' 119 ', 'GLN', 0.0, (60.256, 2.426, -2.512)), ('A', ' 164 ', 'VAL', 0.2592677536889238, (68.63599999999997, -15.844999999999999, -11.147)), ('B', '  70 ', 'GLU', 0.0, (29.763, 2.5909999999999993, -7.15)), ('B', ' 142 ', 'ARG', 0.0, (46.80699999999999, -15.207999999999995, -23.289)), ('B', ' 190 ', 'LYS', 0.044615142264458105, (56.522000000000006, -44.461, -23.117)), ('C', ' 354 ', 'ASN', 0.26770239464664525, (23.678000000000015, 29.49200000000001, 11.887)), ('C', ' 403 ', 'ARG', 6.930166281141203e-05, (34.81, 25.422, 0.064)), ('C', ' 519 ', 'HIS', 0.04643281913625324, (29.453, 30.972000000000005, 36.70400000000001)), ('D', ' 110 ', 'ARG', 0.01643670154389511, (35.25999999999999, 51.710999999999984, 56.551)), ('D', ' 119 ', 'GLN', 0.0, (28.010000000000016, 73.804, 57.57700000000001)), ('E', '  53 ', 'SER', 0.2807396629285126, (44.509, 57.394, 64.486)), ('E', ' 142 ', 'ARG', 0.02111996970920727, (27.622, 75.636, 87.523)), ('E', ' 176 ', 'SER', 0.136239483446415, (17.647, 81.94399999999997, 85.813)), ('F', ' 408 ', 'ARG', 0.1131415042354802, (45.292, 49.102, 48.272)), ('F', ' 519 ', 'HIS', 0.23631712604314745, (35.077, 22.614999999999995, 32.652)), ('G', ' 119 ', 'GLN', 0.001556397976833192, (95.003, 16.547, 43.042)), ('G', ' 134 ', 'SER', 0.096217251173666, (66.445, 7.661999999999999, 55.342)), ('H', '  55 ', 'GLN', 0.0, (100.82699999999998, 24.213, 25.909000000000006)), ('H', ' 176 ', 'SER', 0.09793411361145672, (64.699, 15.492, 39.306)), ('I', ' 388 ', 'ASN', 0.0, (113.802, 52.61399999999999, 46.697)), ('I', ' 390 ', 'LEU', 0.24316645638625717, (119.201, 53.141, 47.819)), ('I', ' 484 ', 'GLU', 0.17032713215446577, (128.433, 36.537, 0.663)), ('J', ' 119 ', 'GLN', 0.00013241242608999265, (64.36399999999996, 85.935, 76.991)), ('K', ' 176 ', 'SER', 0.19550266239024477, (53.455999999999996, 108.14999999999999, 61.428000000000004)), ('K', ' 207 ', 'LYS', 0.017399237503017247, (46.80499999999997, 117.404, 53.251)), ('L', ' 498 ', 'GLN', 0.027968743189330385, (67.222, 57.334, 53.07200000000001))]
data['cbeta'] = []
data['probe'] = [(' C 384  PRO  HA ', ' C 387  LEU HD23', -0.917, (37.396, 15.646, 21.405)), (' E 142  ARG HH22', ' E 163  VAL HG11', -0.828, (23.308, 75.114, 82.487)), (' A   5  LEU  HA ', ' A 119  GLN HE22', -0.768, (63.102, 4.62, 0.338)), (' A  11  LEU HD11', ' A 161  PRO  HG3', -0.707, (68.018, -15.606, -0.403)), (' H  32  TYR  HD2', ' H  92  ASN  HA ', -0.692, (98.766, 39.865, 34.264)), (' F 468  ILE HD11', ' H 158  ASN  HB3', -0.684, (58.764, 26.904, 49.61)), (' J 108  TYR  HA ', ' L 376  THR HG23', -0.675, (79.777, 63.028, 70.634)), (' G   5  LEU  HA ', ' G 119  GLN HE22', -0.674, (99.02, 16.061, 45.587)), (' D   5  LEU  HA ', ' D 119  GLN HE22', -0.663, (27.748, 73.827, 52.479)), (' G  11  LEU HD11', ' G 161  PRO  HG3', -0.645, (81.632, 14.422, 57.304)), (' B  32  TYR  HD2', ' B  92  ASN  HA ', -0.644, (37.164, 6.406, 4.693)), (' L 393  THR  HA ', ' L 522  ALA  HA ', -0.642, (103.555, 50.329, 72.739)), (' D  83  MET  HE2', ' D  86  LEU HD21', -0.636, (11.945, 66.573, 58.308)), (' E  24  ARG  HG2', ' E  70  GLU  HG3', -0.635, (34.212, 51.031, 78.459)), (' A 207  THR HG23', ' A 224  LYS  HE3', -0.631, (78.085, -24.945, -29.289)), (' G 133  PRO  HB3', ' G 159  TYR  HB3', -0.63, (71.451, 10.28, 54.061)), (' G 108  TYR  HA ', ' I 376  THR HG23', -0.625, (111.879, 37.465, 34.321)), (' A 108  TYR  HA ', ' C 376  THR HG23', -0.625, (40.926, 18.302, 9.334)), (' A 145  THR HG22', ' A 150  ALA  HB2', -0.621, (64.348, -26.684, -36.02)), (' G 108  TYR  HB2', ' I 378  LYS  HE3', -0.62, (113.825, 35.457, 36.302)), (' J 161  PRO  O  ', ' J 214  HIS  NE2', -0.612, (61.052, 105.563, 79.262)), (' J  37  VAL HG22', ' J  47  TRP  HA ', -0.603, (75.602, 84.362, 68.571)), (' D 133  PRO  HB3', ' D 159  TYR  HB3', -0.598, (8.698, 87.317, 71.599)), (' A 133  PRO  HB3', ' A 159  TYR  HB3', -0.594, (68.191, -22.37, -8.996)), (' D   6  GLU  OE2', ' D  96  CYS  N  ', -0.582, (25.312, 68.221, 56.299)), (' I 388  ASN  N  ', ' I 388  ASN  OD1', -0.577, (113.241, 51.168, 45.879)), (' H 108  ARG  NH1', ' H 109  THR  O  ', -0.574, (67.389, 14.105, 20.315)), (' F 431  GLY  HA2', ' F 515  PHE  CE2', -0.571, (35.185, 36.05, 43.134)), (' G 111  GLU  HG3', ' H  32  TYR  CE1', -0.568, (102.088, 38.284, 30.914)), (' I 382  VAL HG11', ' I 387  LEU HD13', -0.568, (118.195, 47.757, 44.294)), (' A 113  ALA  O  ', ' B  46  ARG  NH1', -0.566, (46.313, 9.793, -0.986)), (' J   2  VAL HG11', ' J 116  ILE HD13', -0.565, (66.967, 73.752, 77.032)), (' C 392  PHE  CD1', ' C 515  PHE  HB3', -0.563, (33.169, 23.514, 26.814)), (' J  91  THR HG23', ' J 124  THR  HA ', -0.562, (72.049, 100.144, 73.304)), (' L 388  ASN  O  ', ' L 526  GLY  HA3', -0.562, (100.948, 62.313, 71.252)), (' K  46  ARG  HD3', ' K  49  TYR  HB3', -0.558, (67.701, 72.351, 65.194)), (' E 142  ARG  NH2', ' E 163  VAL HG11', -0.556, (23.933, 75.093, 83.361)), (' L 520  ALA  HB1', ' L 521  PRO  HD2', -0.55, (106.06, 45.884, 73.907)), (' D   2  VAL HG11', ' D 116  ILE HD13', -0.548, (36.317, 65.964, 52.327)), (' G  11  LEU HD23', ' G 124  THR  HB ', -0.547, (82.892, 17.925, 55.213)), (' E  32  TYR  HD2', ' E  92  ASN  HA ', -0.543, (31.678, 49.356, 62.284)), (' I 393  THR  HA ', ' I 522  ALA  HA ', -0.543, (125.541, 59.285, 42.871)), (' I 384  PRO  HA ', ' I 387  LEU  HB2', -0.543, (114.917, 47.063, 44.243)), (' G 108  TYR  CD2', ' G 109  PHE  HB2', -0.539, (110.555, 32.696, 33.097)), (' D 207  THR HG23', ' D 224  LYS  HE3', -0.538, (14.439, 105.581, 82.402)), (' G 158  ASP  OD1', ' G 185  GLN  NE2', -0.536, (67.463, 16.604, 54.24)), (' K  32  TYR  HD2', ' K  92  ASN  HA ', -0.535, (79.724, 73.445, 62.368)), (' H  39  LYS  HD3', ' H  84  ALA  HB2', -0.535, (86.561, 17.531, 28.735)), (' D  11  LEU HD21', ' D 161  PRO  HG3', -0.533, (9.715, 81.046, 62.261)), (' A   6  GLU  OE2', ' A  96  CYS  N  ', -0.529, (56.813, 1.475, 2.067)), (' A  86  LEU  HB3', ' A 125  VAL HG21', -0.529, (57.981, -14.144, 7.779)), (' D  47  TRP  CZ2', ' D  50  VAL HG23', -0.528, (23.658, 56.131, 58.156)), (' E  33  LEU HD22', ' E  71  PHE  CG ', -0.526, (37.062, 53.675, 71.248)), (' C 350  VAL HG22', ' C 422  ASN  HB3', -0.526, (31.664, 33.227, 6.496)), (' K 120  PRO  HD3', ' K 132  VAL HG22', -0.524, (53.094, 121.622, 62.98)), (' A  11  LEU HD23', ' A 124  THR  HB ', -0.523, (64.169, -14.087, 1.506)), (' A  47  TRP  CZ2', ' A  50  VAL HG23', -0.522, (45.897, 1.321, 8.208)), (' J 101  TYR  HB3', ' J 108  TYR  HB3', -0.521, (77.637, 65.656, 73.367)), (' G 156  VAL HG11', ' G 164  VAL HG11', -0.52, (71.885, 7.378, 49.642)), (' A  94  TYR  O  ', ' A 120  GLY  HA2', -0.518, (58.397, -1.668, 0.874)), (' E   8  PRO  HG3', ' E  11  MET  HE3', -0.518, (35.791, 63.983, 83.423)), (' H  37  GLN  HB2', ' H  47  LEU HD11', -0.517, (90.653, 22.418, 27.383)), (' J  47  TRP  CZ2', ' J  50  VAL HG23', -0.516, (80.455, 81.264, 69.94)), (' K  78  LEU HD21', ' K 104  LEU HD21', -0.514, (54.792, 80.856, 55.66)), (' K  33  LEU HD22', ' K  71  PHE  CG ', -0.513, (71.505, 75.161, 55.042)), (' K  14  SER  HB3', ' K 107  LYS  HB3', -0.513, (47.295, 85.881, 50.923)), (' K 161  GLU  HA ', ' K 176  SER  O  ', -0.51, (56.717, 108.438, 60.905)), (' C 398  ASP  O  ', ' C 511  VAL  HA ', -0.509, (28.938, 24.366, 12.695)), (' D 111  GLU  HG3', ' E  32  TYR  CD1', -0.508, (36.67, 50.305, 61.072)), (' D  34  MET  HB3', ' D  79  LEU HD22', -0.505, (25.28, 62.443, 51.858)), (' A 119  GLN  H  ', ' A 119  GLN  NE2', -0.504, (61.089, 3.659, -1.092)), (' J   6  GLU  OE2', ' J  96  CYS  N  ', -0.504, (70.27, 85.12, 76.336)), (' I 359  SER  HA ', ' I 524  VAL HG22', -0.502, (121.2, 60.69, 37.782)), (' I 366  SER  HB2', ' I 388  ASN  ND2', -0.501, (109.339, 52.228, 45.448)), (' H  89  LEU  HB2', ' H  98  PHE  CD1', -0.5, (90.798, 30.763, 35.609)), (' E   6  GLN  O  ', ' E 100  GLN  NE2', -0.499, (29.168, 60.235, 79.547)), (' K 113  PRO  HD3', ' K 198  HIS  ND1', -0.498, (47.605, 103.766, 50.343)), (' J  94  TYR  O  ', ' J 120  GLY  HA2', -0.497, (69.102, 88.632, 75.72)), (' K   7  SER  OG ', ' K  24  ARG  NH1', -0.496, (69.513, 83.428, 47.912)), (' H  24  ARG  NH1', ' H  70  GLU  OE2', -0.496, (84.117, 41.328, 23.599)), (' F 392  PHE  CD1', ' F 515  PHE  HB3', -0.494, (34.059, 31.579, 40.325)), (' J  34  MET  HB3', ' J  79  LEU HD22', -0.493, (75.465, 80.366, 78.321)), (' D 108  TYR  HA ', ' F 376  THR HG23', -0.492, (37.697, 48.372, 50.716)), (' C 398  ASP  OD2', ' C 423  TYR  OH ', -0.492, (31.22, 29.173, 15.763)), (' A  36  TRP  NE1', ' A  81  LEU  HB2', -0.491, (55.863, -1.072, 9.431)), (' G  47  TRP  CZ2', ' G  50  VAL HG23', -0.488, (96.581, 34.714, 44.316)), (' G   6  GLU  OE2', ' G  96  CYS  N  ', -0.487, (95.874, 22.228, 45.116)), (' B   8  PRO  HG3', ' B  11  MET  HE3', -0.486, (37.318, -4.479, -18.809)), (' G  34  MET  HB3', ' G  79  LEU HD22', -0.484, (101.834, 26.546, 46.672)), (' A  47  TRP  HE1', ' A  50  VAL HG23', -0.482, (46.568, 1.699, 7.154)), (' D  20  LEU HD12', ' D  81  LEU HD23', -0.48, (17.965, 66.46, 55.93)), (' I 518  LEU  HG ', ' I 519  HIS  H  ', -0.48, (134.488, 56.515, 42.55)), (' A 115  ASP  N  ', ' A 115  ASP  OD1', -0.478, (50.05, 10.153, -0.22)), (' J 115  ASP  N  ', ' J 115  ASP  OD1', -0.477, (69.027, 74.416, 71.948)), (' B  67  SER  HA ', ' B  71  PHE  CE2', -0.477, (31.579, 7.112, -4.448)), (' G   2  VAL HG11', ' G 116  ILE HD13', -0.477, (105.224, 21.221, 37.784)), (' K 184  ALA  O  ', ' K 188  LYS  HG3', -0.476, (60.394, 131.006, 62.94)), (' J  83  MET  HE2', ' J  86  LEU HD21', -0.475, (78.825, 95.05, 75.758)), (' A 144  SER  HA ', ' B 116  PHE  HD2', -0.475, (59.85, -27.735, -31.628)), (' E  37  GLN  HB2', ' E  47  LEU HD11', -0.474, (38.191, 67.597, 69.389)), (' D 110  ARG  NH2', ' F 374  PHE  O  ', -0.474, (33.371, 45.9, 56.641)), (' K  78  LEU  HA ', ' K  78  LEU HD23', -0.474, (52.337, 78.432, 56.478)), (' B 191  VAL HG22', ' B 210  ASN  OD1', -0.474, (54.912, -42.733, -27.724)), (' H  33  LEU HD22', ' H  71  PHE  CG ', -0.473, (92.191, 36.148, 26.117)), (' C 443  SER  HB3', ' C 499  PRO  HD3', -0.471, (27.321, 19.664, -8.431)), (' F 366  SER  HB2', ' F 388  ASN  ND2', -0.469, (23.989, 36.384, 50.417)), (' J 108  TYR  CD2', ' J 109  PHE  HB2', -0.469, (74.731, 64.51, 71.294)), (' A  73  ASP  OD1', ' A  75  SER  OG ', -0.468, (62.767, 10.062, 18.521)), (' F 359  SER  HB3', ' F 394  ASN  OD1', -0.467, (36.721, 22.963, 44.595)), (' G 101  TYR  HB3', ' G 108  TYR  HB3', -0.467, (110.844, 33.23, 36.656)), (' A   2  VAL HG11', ' A 116  ILE HD13', -0.466, (54.779, 12.666, 0.847)), (' D 113  ALA  O  ', ' E  46  ARG  NH1', -0.466, (35.955, 59.63, 59.435)), (' G  40  ALA  HB3', ' G  43  LYS  HB2', -0.466, (81.529, 26.565, 43.563)), (' L 412  PRO  HG3', ' L 429  PHE  HB3', -0.465, (84.651, 52.528, 77.932)), (' D 115  ASP  N  ', ' D 115  ASP  OD1', -0.463, (35.255, 62.563, 56.472)), (' L 502  GLY  O  ', ' L 506  GLN  HG3', -0.462, (68.524, 60.943, 59.747)), (' D  47  TRP  HZ2', ' D  50  VAL HG23', -0.461, (23.435, 55.664, 58.371)), (' I 401  VAL HG22', ' I 509  ARG  HG2', -0.461, (111.307, 45.882, 22.386)), (' H   8  PRO  HG3', ' H  11  MET  HE3', -0.461, (78.916, 28.586, 22.236)), (' B 161  GLU  HA ', ' B 176  SER  O  ', -0.46, (54.343, -23.304, -17.499)), (' L 401  VAL HG22', ' L 509  ARG  HG2', -0.459, (79.905, 54.584, 58.485)), (' D 101  TYR  HB3', ' D 108  TYR  HB3', -0.459, (36.755, 52.781, 50.15)), (' G 101  TYR  CE1', ' G 103  ASP  HB2', -0.458, (113.421, 33.782, 40.958)), (' D 182  ALA  HA ', ' D 192  LEU  HB3', -0.457, (15.055, 82.478, 76.196)), (' G 115  ASP  N  ', ' G 115  ASP  OD1', -0.457, (101.713, 26.054, 35.768)), (' D  36  TRP  CE2', ' D  81  LEU  HB2', -0.457, (19.913, 64.443, 53.632)), (' C 366  SER  HB2', ' C 388  ASN  ND2', -0.457, (33.134, 10.035, 23.825)), (' G 140  PRO  HG2', ' G 227  PRO  HB3', -0.456, (55.117, -0.674, 41.186)), (' J   2  VAL HG13', ' J  27  PHE  CD1', -0.456, (68.207, 73.819, 80.402)), (' C 365  TYR  CG ', ' C 387  LEU HD11', -0.456, (32.938, 16.045, 22.828)), (' C 431  GLY  HA2', ' C 515  PHE  CE2', -0.456, (35.443, 22.247, 22.241)), (' J  11  LEU HD11', ' J 126  SER  HB3', -0.456, (72.493, 105.269, 76.558)), (' B 124  GLN  O  ', ' B 127  SER  OG ', -0.454, (68.321, -35.184, -12.62)), (' G  12  VAL HG13', ' G 125  VAL HG22', -0.453, (85.338, 23.5, 57.972)), (' G  83  MET  HE2', ' G  86  LEU HD21', -0.451, (89.024, 27.039, 54.981)), (' D 119  GLN  H  ', ' D 119  GLN  NE2', -0.451, (27.802, 73.561, 55.028)), (' B 145  LYS  HB3', ' B 197  THR  OG1', -0.45, (42.797, -25.479, -23.575)), (' K 166  GLN HE21', ' K 171  SER  HB3', -0.449, (47.616, 92.079, 56.569)), (' F 476  GLY  N  ', ' F 487  ASN  HB3', -0.449, (74.996, 44.203, 43.948)), (' C 454  ARG  NH2', ' C 467  ASP  O  ', -0.448, (27.437, 40.175, 6.181)), (' G  35  ASN  ND2', ' G  50  VAL HG22', -0.447, (98.371, 32.502, 42.698)), (' E 142  ARG  HB3', ' E 173  TYR  CG ', -0.447, (28.248, 77.205, 84.999)), (' A 111  GLU  HG3', ' B  32  TYR  CE1', -0.446, (37.444, 11.606, 2.593)), (' D 214  HIS  CD2', ' D 216  PRO  HD2', -0.446, (11.436, 87.776, 65.805)), (' C 412  PRO  HG3', ' C 429  PHE  HB3', -0.445, (40.354, 28.722, 18.673)), (' J 161  PRO  HD2', ' J 216  PRO  HB2', -0.444, (63.185, 105.136, 82.024)), (' E 134  CYS  HB2', ' E 148  TRP  CH2', -0.442, (13.078, 82.57, 91.462)), (' F 354  ASN  O  ', ' F 398  ASP  HA ', -0.442, (45.251, 31.905, 50.844)), (' H 125  LEU  O  ', ' H 183  LYS  HD2', -0.442, (53.788, 12.449, 58.408)), (' L 398  ASP  OD2', ' L 423  TYR  OH ', -0.441, (86.745, 48.998, 69.196)), (' K   8  PRO  HG3', ' K  11  MET  HE3', -0.441, (60.675, 84.984, 48.936)), (' G 113  ALA  O  ', ' H  46  ARG  NH1', -0.44, (100.563, 28.703, 33.162)), (' F 357  ARG  NH1', ' H 190  LYS  HD3', -0.44, (40.258, 19.595, 45.915)), (' B  33  LEU HD22', ' B  71  PHE  CD2', -0.44, (35.249, 5.56, -5.773)), (' F 412  PRO  HG3', ' F 429  PHE  HB3', -0.439, (41.759, 41.316, 39.795)), (' H  82  ASP  O  ', ' H  86  TYR  OH ', -0.438, (86.993, 20.04, 24.979)), (' E  89  LEU  HB2', ' E  98  PHE  CD2', -0.438, (29.188, 60.383, 67.165)), (' B  78  LEU  HA ', ' B  78  LEU HD23', -0.438, (44.284, 5.423, -22.349)), (' A  36  TRP  CE2', ' A  81  LEU  HB2', -0.438, (55.868, -0.819, 9.035)), (' F 350  VAL HG22', ' F 422  ASN  HB3', -0.437, (52.897, 39.179, 50.108)), (' A 101  TYR  HB3', ' A 108  TYR  HB3', -0.436, (44.898, 16.828, 8.573)), (' J   2  VAL HG12', ' J 116  ILE HG21', -0.436, (66.107, 75.511, 78.287)), (' A  47  TRP  HZ2', ' A  50  VAL HG23', -0.436, (46.041, 1.294, 8.725)), (' K 113  PRO  HB3', ' K 139  PHE  HB3', -0.436, (47.537, 104.137, 53.635)), (' D  35  ASN  CG ', ' D  50  VAL HG22', -0.436, (25.924, 57.629, 57.06)), (' E  50  ALA  C  ', ' E  52  SER  H  ', -0.436, (41.853, 54.871, 66.314)), (' H  33  LEU HD11', ' H  88  CYS  HB2', -0.436, (90.338, 33.736, 29.706)), (' J 115  ASP  HB3', ' K  46  ARG  NH2', -0.435, (67.323, 71.832, 69.693)), (' F 398  ASP  O  ', ' F 511  VAL  HA ', -0.435, (42.609, 35.521, 52.151)), (' D   6  GLU  HA ', ' D  21  SER  O  ', -0.434, (22.464, 70.969, 51.557)), (' I 439  ASN  O  ', ' I 443  SER  HB2', -0.433, (102.88, 41.905, 17.673)), (' G  86  LEU  HB3', ' G 125  VAL HG21', -0.433, (85.143, 26.094, 56.927)), (' J  47  TRP  HZ2', ' J  50  VAL HG23', -0.433, (81.065, 81.119, 70.311)), (' H  30  SER  OG ', ' H  31  ASN  N  ', -0.433, (98.537, 41.037, 28.996)), (' L 443  SER  HB3', ' L 499  PRO  HD3', -0.432, (69.736, 58.839, 51.251)), (' J 202  SER  HB2', ' J 206  GLN  HG2', -0.432, (30.747, 110.499, 71.503)), (' D 200  SER  HA ', ' D 203  LEU  HG ', -0.432, (20.579, 101.108, 92.262)), (' K  50  ALA  C  ', ' K  52  SER  H  ', -0.431, (69.472, 69.399, 59.111)), (' J  70  ILE HD11', ' J  79  LEU HD11', -0.43, (78.865, 82.086, 77.912)), (' H 145  LYS  HB3', ' H 197  THR  OG1', -0.43, (59.329, 25.388, 30.768)), (' K  11  MET  SD ', ' K  19  VAL HG13', -0.43, (58.063, 82.717, 51.073)), (' C 355  ARG  HD3', ' C 396  TYR  CD1', -0.43, (25.717, 29.958, 20.26)), (' F 431  GLY  HA2', ' F 515  PHE  CD2', -0.429, (35.6, 36.306, 43.016)), (' H  67  SER  HA ', ' H  71  PHE  CE2', -0.428, (94.462, 39.5, 24.611)), (' I 354  ASN  O  ', ' I 398  ASP  HA ', -0.428, (120.343, 50.998, 26.785)), (' H  83  PHE  CE2', ' H 106  ILE HG12', -0.427, (80.012, 14.993, 22.659)), (' I 390  LEU  HA ', ' I 390  LEU HD12', -0.427, (120.369, 53.226, 49.101)), (' H  50  ALA  C  ', ' H  52  SER  H  ', -0.427, (98.505, 33.495, 25.063)), (' E 125  LEU  O  ', ' E 183  LYS  HD2', -0.426, (-4.017, 89.578, 86.199)), (' A 111  GLU  HG3', ' B  32  TYR  CD1', -0.425, (37.575, 11.325, 2.345)), (' H  20  THR HG23', ' H  72  THR HG23', -0.424, (86.789, 31.948, 19.156)), (' I 502  GLY  O  ', ' I 506  GLN  HG3', -0.422, (105.697, 34.342, 20.366)), (' F 349  SER  OG ', ' F 451  TYR  HA ', -0.421, (54.943, 37.428, 58.924)), (' L 365  TYR  HD2', ' L 388  ASN  HB3', -0.42, (97.676, 62.37, 70.23)), (' J  61  ALA  HB3', ' J  64  VAL HG22', -0.42, (82.438, 89.252, 69.208)), (' I 444  LYS  HB2', ' I 448  ASN  HB2', -0.419, (105.896, 43.0, 11.511)), (' G 105  SER  HB2', ' I 379  CYS  O  ', -0.419, (117.974, 39.184, 41.653)), (' J  47  TRP  HE1', ' J  50  VAL HG23', -0.418, (79.495, 80.954, 70.615)), (' A 140  PRO  HA ', ' A 144  SER  OG ', -0.418, (64.188, -28.709, -30.593)), (' G 157  LYS  NZ ', ' G 185  GLN  OE1', -0.418, (64.796, 16.688, 52.201)), (' A  68  PHE  HB3', ' A  81  LEU HD11', -0.418, (53.563, -4.897, 11.49)), (' K 166  GLN  NE2', ' K 171  SER  HB3', -0.418, (48.129, 91.849, 56.655)), (' E 145  LYS  HA ', ' E 145  LYS  HD3', -0.418, (19.448, 72.577, 91.876)), (' A 141  SER  O  ', ' A 145  THR HG23', -0.418, (63.804, -29.525, -34.604)), (' G 166  VAL  HA ', ' G 211  ASN  O  ', -0.418, (72.323, 1.993, 47.056)), (' J 164  VAL HG22', ' J 214  HIS  HB2', -0.417, (56.765, 106.823, 79.65)), (' F 502  GLY  O  ', ' F 506  GLN  HG3', -0.417, (48.632, 52.007, 62.385)), (' K  30  SER  OG ', ' K  31  ASN  N  ', -0.415, (77.823, 70.014, 57.984)), (' A  47  TRP  NE1', ' A  50  VAL HG23', -0.415, (46.246, 1.214, 7.34)), (' B   2  ILE HD13', ' B  29  ILE HG22', -0.415, (33.561, 1.486, 2.887)), (' L 485  GLY  H  ', ' L 488  CYS  HB2', -0.415, (60.978, 31.306, 61.25)), (' G  53  GLY  HA2', ' G  72  ARG  NH1', -0.414, (107.776, 30.353, 46.863)), (' I 359  SER  HA ', ' I 524  VAL  CG2', -0.414, (121.638, 60.046, 38.107)), (' E   4  MET  HE3', ' E  23  CYS  SG ', -0.414, (31.868, 55.292, 72.808)), (' D 133  PRO  HD2', ' D 219  THR HG21', -0.414, (7.649, 91.505, 69.943)), (' D  47  TRP  HE1', ' D  50  VAL HG23', -0.414, (24.659, 57.103, 58.641)), (' G  47  TRP  HE1', ' G  50  VAL HG23', -0.413, (97.139, 33.818, 43.98)), (' G 160  PHE  HA ', ' G 161  PRO  HA ', -0.412, (76.445, 14.192, 54.929)), (' D  18  LEU  HA ', ' D  18  LEU HD12', -0.412, (10.663, 71.064, 53.046)), (' B  78  LEU HD21', ' B 104  LEU HD21', -0.412, (43.961, 1.759, -20.782)), (' L 338  PHE  HE2', ' L 363  ALA  HB1', -0.411, (97.024, 58.711, 65.726)), (' A  83  MET  HE2', ' A  86  LEU HD21', -0.41, (56.931, -10.205, 8.846)), (' E  20  THR HG23', ' E  72  THR HG23', -0.409, (41.454, 58.501, 78.3)), (' E 161  GLU  HA ', ' E 176  SER  O  ', -0.408, (15.882, 78.795, 84.649)), (' J  19  ARG  HG3', ' J  82  GLN  HG2', -0.408, (80.831, 90.282, 84.509)), (' E   9  SER  O  ', ' E 102  THR  HA ', -0.408, (30.715, 65.819, 78.863)), (' F 399  SER  HA ', ' F 510  VAL  O  ', -0.408, (44.145, 36.175, 53.689)), (' E 107  LYS  HA ', ' E 140  TYR  OH ', -0.408, (36.481, 75.204, 86.997)), (' A  51  ILE HG13', ' A  58  THR HG22', -0.408, (50.093, 3.227, 15.924)), (' G  47  TRP  HZ2', ' G  50  VAL HG23', -0.407, (97.258, 34.861, 44.569)), (' C 401  VAL HG22', ' C 509  ARG  HG2', -0.407, (27.363, 22.216, 4.242)), (' G  12  VAL  O  ', ' G 125  VAL  HA ', -0.406, (83.157, 22.583, 58.589)), (' F 401  VAL HG22', ' F 509  ARG  HG2', -0.406, (46.132, 39.222, 59.53)), (' G 119  GLN  H  ', ' G 119  GLN HE21', -0.406, (97.344, 16.165, 43.895)), (' K   4  MET  HE3', ' K  23  CYS  SG ', -0.406, (72.812, 80.239, 55.596)), (' D 138  LEU  HB3', ' E 118  PHE  CD1', -0.405, (13.494, 91.492, 88.344)), (' A  34  MET  HB3', ' A  79  LEU HD22', -0.404, (54.539, 5.197, 8.366)), (' K  46  ARG  NH1', ' K  49  TYR  HB3', -0.404, (68.271, 72.024, 66.346)), (' E 124  GLN  HG2', ' E 129  THR  O  ', -0.404, (1.127, 87.56, 84.38)), (' K 166  GLN  HG2', ' K 171  SER  HA ', -0.404, (47.936, 92.885, 59.02)), (' G   5  LEU HD23', ' G 119  GLN HE22', -0.404, (99.442, 14.732, 45.03)), (' C 399  SER  HA ', ' C 510  VAL  O  ', -0.403, (28.502, 24.183, 10.531)), (' B 108  ARG  NH1', ' B 109  THR  O  ', -0.403, (47.898, -11.422, -32.511)), (' D  86  LEU  HB3', ' D 125  VAL HG21', -0.402, (9.032, 68.09, 60.893)), (' B  89  LEU  HB2', ' B  98  PHE  CD1', -0.402, (43.688, 0.575, -2.39)), (' G 133  PRO  CB ', ' G 159  TYR  HB3', -0.401, (71.19, 9.489, 54.411)), (' K  89  LEU  HB2', ' K  98  PHE  CD2', -0.401, (71.759, 81.795, 63.259)), (' K 150  VAL HG22', ' K 192  TYR  CD1', -0.401, (56.17, 123.148, 57.655)), (' A  29  PHE  O  ', ' A  72  ARG  NH2', -0.4, (54.458, 11.267, 11.414)), (' E 145  LYS  HB2', ' E 197  THR  OG1', -0.4, (20.765, 72.846, 95.652)), (' G 111  GLU  OE1', ' I 375  SER  HB2', -0.4, (105.92, 37.699, 30.946))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
