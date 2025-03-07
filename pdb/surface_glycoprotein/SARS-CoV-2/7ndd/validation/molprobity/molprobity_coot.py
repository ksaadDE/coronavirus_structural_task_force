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
data['rama'] = [('A', ' 527 ', 'PRO', 0.04514973474744314, (214.29200000000006, 258.639, 199.43)), ('B', ' 322 ', 'PRO', 0.0, (262.273, 238.777, 222.15999999999997)), ('B', ' 331 ', 'ASN', 0.021047387458431235, (271.366, 221.46099999999996, 207.018)), ('B', ' 332 ', 'ILE', 0.0, (271.506, 220.154, 203.527)), ('B', ' 334 ', 'ASN', 0.0, (270.427, 214.48599999999996, 199.87500000000003)), ('B', ' 527 ', 'PRO', 0.021215520262434805, (265.75, 224.38899999999998, 202.259)), ('B', ' 528 ', 'LYS', 0.007947876624536818, (263.787, 226.86099999999996, 203.94100000000003)), ('B', ' 591 ', 'SER', 0.01624712230014804, (260.156, 236.36899999999994, 231.91299999999998)), ('C', ' 529 ', 'LYS', 0.012063898492455826, (210.944, 197.24499999999998, 204.22200000000004))]
data['omega'] = [('A', ' 527 ', 'PRO', None, (215.30700000000002, 257.632, 199.746)), ('B', ' 332 ', 'ILE', None, (271.198, 220.11599999999996, 204.952)), ('B', ' 334 ', 'ASN', None, (270.885, 214.873, 201.22)), ('B', ' 528 ', 'LYS', None, (263.935, 225.53599999999997, 203.343)), ('B', ' 529 ', 'LYS', None, (265.721, 228.22099999999998, 204.59800000000004)), ('B', ' 592 ', 'PHE', None, (257.784, 236.84599999999998, 231.523)), ('C', ' 527 ', 'PRO', None, (212.192, 203.37499999999994, 200.326)), ('E', '   8 ', 'PRO', None, (260.373, 152.832, 169.286)), ('G', '   8 ', 'PRO', None, (143.833, 241.452, 172.751)), ('L', '   8 ', 'PRO', None, (281.62599999999986, 298.581, 172.383))]
data['rota'] = [('A', ' 367 ', 'VAL', 0.17436715099242164, (215.38100000000006, 251.81299999999996, 191.31199999999998)), ('B', ' 367 ', 'VAL', 0.1729489485146664, (268.689, 228.73899999999998, 192.62800000000001)), ('B', ' 914 ', 'ASN', 0.053114769202367226, (230.84100000000007, 245.72200000000007, 295.877)), ('C', ' 367 ', 'VAL', 0.1771072928720759, (217.58599999999998, 206.396, 191.75000000000003)), ('C', ' 914 ', 'ASN', 0.046745079880901756, (243.11399999999998, 220.724, 295.843)), ('D', '  12 ', 'VAL', 0.16096216077077485, (284.172, 178.376, 158.33)), ('E', '  14 ', 'SER', 0.26218990519075513, (246.678, 158.454, 163.368)), ('E', '  34 ', 'LEU', 0.21377626702087765, (264.791, 161.943, 183.016)), ('F', '  12 ', 'VAL', 0.16034798245638504, (154.14299999999994, 208.898, 159.637)), ('G', '  14 ', 'SER', 0.2615939859429157, (154.97599999999997, 251.089, 166.637)), ('G', '  34 ', 'LEU', 0.21238953153498927, (150.46699999999998, 232.598, 185.721)), ('H', '  12 ', 'VAL', 0.16168806183851195, (248.228, 303.9709999999999, 158.465)), ('L', '  14 ', 'SER', 0.25949768809758555, (285.327, 284.2459999999999, 166.526)), ('L', '  34 ', 'LEU', 0.21340627874007262, (270.4799999999999, 296.849, 185.103))]
data['cbeta'] = [('B', ' 527 ', 'PRO', ' ', 0.34348663696677567, (266.675, 225.46099999999998, 201.66000000000003))]
data['probe'] = [(' B 335  LEU  O  ', ' B 361  CYS  HB2', -0.777, (267.01, 215.993, 196.502)), (' A 147  LYS  NZ ', ' F  57  ASN  OD1', -0.705, (153.625, 209.674, 191.162)), (' C 147  LYS  NZ ', ' D  57  ASN  OD1', -0.689, (283.735, 174.938, 189.726)), (' A 394  ASN  ND2', ' B 200  TYR  OH ', -0.677, (232.958, 261.277, 203.747)), (' A 564  GLN  NE2', ' A 577  ARG  O  ', -0.673, (219.669, 266.106, 215.363)), (' B 521  PRO  HB3', ' C 200  TYR  CZ ', -0.637, (254.505, 210.588, 206.063)), (' C1028  LYS  O  ', ' C1032  CYS  CB ', -0.636, (240.288, 227.761, 270.844)), (' B 564  GLN  NE2', ' B 577  ARG  O  ', -0.635, (266.273, 218.907, 216.656)), (' B 557  LYS  NZ ', ' B 574  ASP  OD2', -0.635, (262.969, 219.709, 229.78)), (' B 596  SER  OG ', ' B 613  GLN  NE2', -0.633, (251.684, 243.204, 241.007)), (' A 273  ARG  NH1', ' A 290  ASP  OD2', -0.632, (192.38, 233.577, 225.927)), (' C1028  LYS  O  ', ' C1032  CYS  HB2', -0.623, (239.539, 227.906, 270.265)), (' A 388  ASN  HB2', ' A 527  PRO  HD3', -0.619, (215.372, 254.493, 198.893)), (' C 557  LYS  NZ ', ' C 574  ASP  OD2', -0.615, (204.588, 205.412, 228.661)), (' B1028  LYS  O  ', ' B1032  CYS  CB ', -0.615, (225.911, 239.365, 270.56)), (' A 557  LYS  NZ ', ' A 574  ASP  OD2', -0.615, (220.992, 263.103, 228.556)), (' B 273  ARG  NH1', ' B 290  ASP  OD2', -0.613, (251.154, 260.294, 225.835)), (' L  38  GLN  HB2', ' L  48  LEU HD11', -0.606, (271.628, 288.163, 174.565)), (' C 736  VAL HG22', ' C 858  LEU  HG ', -0.605, (246.357, 231.18, 236.133)), (' A1028  LYS  O  ', ' A1032  CYS  CB ', -0.602, (223.219, 221.672, 270.638)), (' E  38  GLN  HB2', ' E  48  LEU HD11', -0.593, (257.249, 166.393, 172.892)), (' G  38  GLN  HB2', ' G  48  LEU HD11', -0.593, (157.742, 237.393, 175.071)), (' H  83  MET  HB3', ' H  86  LEU HD21', -0.582, (250.134, 305.33, 166.626)), (' B 132  GLU  N  ', ' B 164  ASN  O  ', -0.574, (247.242, 271.073, 190.954)), (' C 197  ILE HG22', ' C 198  ASP  H  ', -0.574, (248.231, 206.69, 209.095)), (' C 328  ARG  NH2', ' C 531  THR  O  ', -0.573, (208.102, 193.365, 211.754)), (' D  83  MET  HB3', ' D  86  LEU HD21', -0.57, (283.371, 175.208, 166.788)), (' C  19  THR  H  ', ' C 255  SER  HB2', -0.57, (258.793, 170.726, 198.919)), (' A  19  THR  H  ', ' A 255  SER  HB2', -0.568, (161.754, 233.342, 200.931)), (' B 333  THR  O  ', ' B 334  ASN  O  ', -0.567, (269.893, 217.244, 200.572)), (' B 102  ARG  HG3', ' B 141  LEU HD12', -0.563, (248.303, 286.306, 204.725)), (' F  83  MET  HB3', ' F  86  LEU HD21', -0.563, (152.378, 210.367, 168.122)), (' B1028  LYS  O  ', ' B1032  CYS  HB2', -0.562, (226.393, 239.12, 271.019)), (' A  33  THR  OG1', ' A 219  GLY  O  ', -0.561, (183.85, 225.298, 231.024)), (' A 197  ILE HG22', ' A 198  ASP  H  ', -0.56, (199.029, 225.826, 208.513)), (' C 193  VAL HG23', ' C 223  LEU HD22', -0.559, (257.218, 195.818, 218.113)), (' C 102  ARG  HG3', ' C 141  LEU HD12', -0.558, (267.613, 185.41, 203.993)), (' B 197  ILE HG22', ' B 198  ASP  H  ', -0.556, (241.133, 258.053, 208.425)), (' A 193  VAL HG23', ' A 223  LEU HD22', -0.551, (185.84, 222.461, 218.325)), (' C  27  ALA  HB3', ' C  64  TRP  HB3', -0.55, (252.521, 177.9, 218.869)), (' C 715  PRO  HB3', ' C1069  PRO  HB3', -0.55, (235.063, 210.138, 285.694)), (' C 273  ARG  NH1', ' C 290  ASP  OD2', -0.549, (244.256, 195.651, 225.94)), (' A1028  LYS  O  ', ' A1032  CYS  HB2', -0.549, (223.421, 222.005, 270.525)), (' C 376  THR  HB ', ' C 435  ALA  HB3', -0.548, (218.945, 222.649, 188.019)), (' B1086  LYS  HD2', ' B1122  VAL HG11', -0.547, (242.365, 221.019, 307.864)), (' B1103  PHE  HZ ', ' R   1  NAG  H62', -0.547, (247.674, 243.265, 305.417)), (' A 132  GLU  N  ', ' A 164  ASN  O  ', -0.546, (184.031, 224.637, 191.258)), (' A 195  LYS  HE2', ' A 204  TYR  HE1', -0.546, (192.815, 222.204, 214.325)), (' A  27  ALA  HB3', ' A  64  TRP  HB3', -0.542, (171.763, 234.981, 220.277)), (' A 102  ARG  HG3', ' A 141  LEU HD12', -0.542, (170.89, 218.538, 204.73)), (' B 976  VAL HG12', ' B 979  ASP  H  ', -0.541, (221.036, 248.889, 216.923)), (' A1091  ARG  NH1', ' A1120  THR  O  ', -0.54, (227.315, 236.675, 303.851)), (' C 564  GLN  NE2', ' C 577  ARG  O  ', -0.536, (202.764, 203.087, 215.549)), (' C 811  LYS  NZ ', ' C 820  ASP  OD2', -0.532, (263.571, 221.282, 263.916)), (' B 763  LEU HD22', ' B1008  VAL HG21', -0.531, (221.593, 234.537, 236.203)), (' B  19  THR  H  ', ' B 255  SER  HB2', -0.531, (265.541, 287.32, 200.504)), (' C1086  LYS  HD2', ' C1122  VAL HG11', -0.53, (216.721, 223.171, 308.467)), (' C 374  PHE  HA ', ' C 436  TRP  HB3', -0.528, (219.015, 217.671, 184.978)), (' A1031  GLU  CD ', ' C1039  ARG  HE ', -0.527, (230.017, 226.19, 271.255)), (' A 393  THR HG21', ' A 520  ALA  HB3', -0.527, (229.245, 261.508, 209.028)), (' C 976  VAL HG12', ' C 979  ASP  H  ', -0.526, (250.123, 227.27, 216.341)), (' C 195  LYS  HE2', ' C 204  TYR  HE1', -0.525, (253.882, 202.082, 214.544)), (' B 374  PHE  HA ', ' B 436  TRP  HB3', -0.525, (266.711, 228.498, 179.315)), (' A 898  PHE  HZ ', ' A1050  MET  HE1', -0.525, (214.439, 215.776, 281.036)), (' A1039  ARG  HE ', ' B1031  GLU  CD ', -0.523, (226.242, 231.376, 271.184)), (' B 376  THR  HB ', ' B 435  ALA  HB3', -0.523, (260.821, 228.065, 177.543)), (' C 393  THR HG21', ' C 520  ALA  HB3', -0.522, (201.753, 213.488, 209.45)), (' C 763  LEU HD22', ' C1008  VAL HG21', -0.52, (237.953, 234.122, 236.303)), (' B  14  GLN  HG3', ' B 157  PHE  HB3', -0.52, (250.906, 285.397, 191.527)), (' C1103  PHE  HZ ', ' W   1  NAG  H62', -0.519, (233.288, 207.287, 305.787)), (' A  18  LEU HD11', ' A 258  TRP  CD1', -0.519, (161.089, 228.727, 202.859)), (' C  18  LEU HD11', ' C 258  TRP  CD1', -0.518, (263.151, 172.047, 201.035)), (' B1039  ARG  HE ', ' C1031  GLU  CD ', -0.518, (232.951, 231.59, 271.119)), (' B  33  THR  OG1', ' B 219  GLY  O  ', -0.517, (247.882, 271.67, 230.867)), (' B 328  ARG  NH2', ' B 531  THR  O  ', -0.515, (271.614, 227.967, 212.807)), (' B 898  PHE  HZ ', ' B1050  MET  HE1', -0.514, (225.208, 249.622, 280.865)), (' B 193  VAL HG23', ' B 223  LEU HD22', -0.514, (244.056, 271.406, 218.266)), (' H 110  MET  HE1', ' L  98  PHE  HZ ', -0.511, (262.558, 296.697, 177.479)), (' B 578  ASP  HB3', ' B 581  THR  O  ', -0.51, (271.312, 220.176, 217.418)), (' C 327  VAL  HB ', ' C 531  THR HG23', -0.509, (213.035, 196.516, 209.336)), (' B 215  ASP  N  ', ' B 215  ASP  OD1', -0.508, (256.526, 281.366, 227.176)), (' A  92  PHE  O  ', ' A 192  PHE  N  ', -0.508, (181.648, 222.59, 216.806)), (' B 332  ILE  O  ', ' B 332  ILE HG23', -0.508, (273.789, 219.847, 202.532)), (' C 520  ALA  HB1', ' C 521  PRO  HD2', -0.508, (199.473, 211.69, 210.572)), (' A 976  VAL HG12', ' A 979  ASP  H  ', -0.504, (217.149, 212.967, 216.576)), (' A 520  ALA  HB1', ' A 521  PRO  HD2', -0.504, (229.053, 264.824, 210.209)), (' C  33  THR  OG1', ' C 219  GLY  O  ', -0.503, (255.422, 192.03, 230.759)), (' C  14  GLN  HG3', ' C 157  PHE  HB3', -0.502, (265.875, 184.289, 191.267)), (' A1086  LYS  HD2', ' A1122  VAL HG11', -0.501, (230.99, 244.628, 308.045)), (' G  49  ILE HD13', ' G  55  ARG  HA ', -0.501, (158.876, 238.896, 184.242)), (' D  47  TRP  HB2', ' E  98  PHE  HE1', -0.501, (272.25, 167.297, 175.368)), (' F  17  SER  OG ', ' F  82  GLN  NE2', -0.499, (154.86, 204.206, 169.012)), (' A 376  THR  HB ', ' A 435  ALA  HB3', -0.499, (228.791, 242.385, 187.707)), (' E  49  ILE HD13', ' E  55  ARG  HA ', -0.499, (254.966, 166.699, 181.916)), (' F  47  TRP  HB2', ' G  98  PHE  HE1', -0.499, (151.238, 223.244, 177.46)), (' B  27  ALA  HB3', ' B  64  TRP  HB3', -0.498, (261.994, 277.231, 219.994)), (' B1091  ARG  NH1', ' B1120  THR  O  ', -0.497, (237.023, 228.309, 303.699)), (' H  12  VAL HG21', ' H  18  LEU  HB2', -0.497, (246.861, 302.821, 162.114)), (' L  49  ILE HD13', ' L  55  ARG  HA ', -0.495, (272.263, 286.577, 183.774)), (' B 388  ASN  O  ', ' B 527  PRO  HD2', -0.494, (262.872, 226.065, 200.338)), (' B 520  ALA  HB1', ' B 521  PRO  HD2', -0.494, (252.893, 209.497, 202.152)), (' B 337  PRO  HG2', ' B 356  LYS  HE3', -0.494, (267.062, 212.592, 188.813)), (' A 327  VAL  HB ', ' A 531  THR HG23', -0.492, (208.48, 260.358, 209.162)), (' B 147  LYS  NZ ', ' H  57  ASN  OD1', -0.492, (248.915, 305.349, 190.361)), (' C 109  THR  OG1', ' C 111  ASP  OD1', -0.492, (248.469, 190.024, 193.955)), (' F  12  VAL HG21', ' F  18  LEU  HB2', -0.492, (155.692, 208.531, 163.761)), (' C 980  ILE HG23', ' C 984  LEU HD12', -0.491, (243.529, 229.328, 211.901)), (' B  18  LEU HD12', ' B 255  SER  HA ', -0.49, (263.476, 288.984, 200.219)), (' C 200  TYR  HD2', ' C 228  ASP  HB2', -0.49, (256.647, 207.116, 208.554)), (' C 578  ASP  HB3', ' C 581  THR  O  ', -0.489, (200.957, 197.512, 215.913)), (' A 805  ILE HG22', ' A 818  ILE HD12', -0.489, (209.347, 212.794, 270.627)), (' B 330  PRO  HD3', ' B 544  ASN  OD1', -0.488, (264.716, 220.091, 211.102)), (' C 914  ASN  H  ', ' C 914  ASN HD22', -0.485, (240.833, 220.925, 295.388)), (' B1028  LYS  O  ', ' B1032  CYS  HB3', -0.485, (225.749, 239.887, 271.053)), (' A 215  ASP  N  ', ' A 215  ASP  OD1', -0.485, (171.169, 228.267, 227.541)), (' A 331  ASN  ND2', ' A 331  ASN  O  ', -0.484, (215.063, 271.884, 204.249)), (' D  12  VAL HG21', ' D  18  LEU  HB2', -0.484, (283.78, 179.836, 162.104)), (' A  14  GLN  HG3', ' A 157  PHE  HB3', -0.484, (170.189, 221.274, 192.088)), (' A 379  CYS  HA ', ' A 432  CYS  HA ', -0.484, (226.769, 245.113, 197.694)), (' D  17  SER  OG ', ' D  82  GLN  NE2', -0.483, (287.459, 180.393, 167.94)), (' C1028  LYS  O  ', ' C1032  CYS  HB3', -0.482, (240.512, 227.891, 270.85)), (' A 526  GLY  O  ', ' A 528  LYS  N  ', -0.481, (214.225, 258.582, 201.608)), (' B  92  PHE  O  ', ' B 192  PHE  N  ', -0.481, (246.669, 275.099, 216.662)), (' C 950  ASP  OD2', ' C 954  GLN  NE2', -0.48, (239.362, 218.583, 248.984)), (' F 110  MET  HE1', ' G  98  PHE  HZ ', -0.48, (153.94, 225.299, 178.409)), (' B 195  LYS  HE2', ' B 204  TYR  HE1', -0.48, (241.46, 265.002, 214.206)), (' C 215  ASP  N  ', ' C 215  ASP  OD1', -0.479, (258.73, 179.427, 226.223)), (' C 353  TRP  O  ', ' C 466  ARG  NE ', -0.477, (201.468, 227.025, 191.1)), (' C 143  VAL HG12', ' C 152  TRP  HE3', -0.477, (275.817, 179.217, 201.825)), (' B 328  ARG  HD2', ' B 533  LEU HD12', -0.477, (269.152, 226.501, 216.84)), (' A 656  VAL HG12', ' A 658  ASN  H  ', -0.477, (193.845, 249.453, 258.813)), (' C 331  ASN  ND2', ' C 331  ASN  O  ', -0.476, (200.631, 195.747, 204.482)), (' A 374  PHE  HA ', ' A 436  TRP  HB3', -0.474, (224.852, 245.235, 184.481)), (' B 914  ASN  H  ', ' B 914  ASN HD22', -0.473, (231.353, 243.564, 295.33)), (' D 110  MET  HE1', ' E  98  PHE  HZ ', -0.472, (269.586, 168.962, 176.291)), (' C 379  CYS  HA ', ' C 432  CYS  HA ', -0.472, (217.889, 220.135, 198.111)), (' A 950  ASP  OD2', ' A 954  GLN  NE2', -0.469, (215.231, 226.893, 249.163)), (' B 726  ILE HD13', ' B 945  LEU HD13', -0.468, (230.582, 250.634, 259.62)), (' H  47  TRP  HB2', ' L  98  PHE  HE1', -0.468, (261.883, 300.231, 176.723)), (' C  91  TYR  OH ', ' C 191  GLU  OE1', -0.468, (258.032, 191.022, 222.386)), (' A 193  VAL  HB ', ' A 204  TYR  HB2', -0.468, (188.398, 221.339, 216.77)), (' A 565  PHE  HD1', ' A 576  VAL HG12', -0.467, (220.755, 261.342, 218.565)), (' B 188  ASN  HA ', ' B 209  PRO  HA ', -0.466, (244.135, 285.265, 223.642)), (' B 172  SER  OG ', ' B 173  GLN  N  ', -0.466, (234.035, 279.114, 207.283)), (' B 379  CYS  HA ', ' B 432  CYS  HA ', -0.466, (255.38, 226.65, 186.183)), (' B 726  ILE HG12', ' B1061  VAL HG22', -0.465, (229.291, 249.258, 262.277)), (' A  91  TYR  OH ', ' A 191  GLU  OE1', -0.465, (181.512, 223.786, 222.828)), (' A 763  LEU HD22', ' A1008  VAL HG21', -0.464, (229.619, 220.431, 236.2)), (' A  18  LEU HD12', ' A 255  SER  HA ', -0.463, (161.255, 230.189, 200.89)), (' B 146  HIS  CE1', ' B 148  ASN  HB2', -0.463, (241.908, 299.19, 191.617)), (' B  18  LEU HD11', ' B 258  TRP  CD1', -0.462, (261.997, 289.971, 202.651)), (' A1028  LYS  O  ', ' A1032  CYS  HB3', -0.462, (223.039, 221.108, 270.709)), (' A 200  TYR  OH ', ' C 394  ASN  OD1', -0.462, (200.361, 216.933, 204.058)), (' A 198  ASP  OD1', ' A 199  GLY  N  ', -0.461, (198.984, 224.667, 205.212)), (' A 726  ILE HG12', ' A1061  VAL HG22', -0.461, (212.645, 219.538, 262.476)), (' A 294  ASP  OD1', ' A 297  SER  N  ', -0.46, (194.518, 234.051, 236.163)), (' B 206  LYS  HB2', ' B 223  LEU  HA ', -0.459, (240.41, 274.207, 220.99)), (' B 393  THR HG21', ' B 520  ALA  HB3', -0.459, (252.303, 211.648, 199.988)), (' A 172  SER  OG ', ' A 173  GLN  N  ', -0.459, (183.976, 209.341, 207.635)), (' C 172  SER  OG ', ' C 173  GLN  N  ', -0.459, (269.855, 200.911, 208.124)), (' C 146  HIS  CE1', ' C 148  ASN  HB2', -0.459, (282.433, 184.131, 191.275)), (' C 198  ASP  OD1', ' C 199  GLY  N  ', -0.458, (249.532, 207.427, 206.022)), (' B 360  ASN  HA ', ' B 523  THR  HB ', -0.458, (261.87, 212.209, 199.715)), (' A 421  TYR  CD1', ' A 457  ARG  HB3', -0.457, (251.049, 243.29, 192.605)), (' C1091  ARG  NH1', ' C1120  THR  O  ', -0.457, (225.372, 224.75, 303.748)), (' A1040  VAL HG21', ' B1035  GLY  HA3', -0.457, (222.097, 235.978, 277.096)), (' C 914  ASN  N  ', ' C 914  ASN HD22', -0.456, (241.36, 221.041, 295.282)), (' B 987  PRO  HG3', ' C 427  ASP  OD2', -0.456, (216.931, 234.283, 205.138)), (' B 656  VAL HG12', ' B 658  ASN  H  ', -0.456, (264.631, 250.948, 258.631)), (' C 726  ILE HG12', ' C1061  VAL HG22', -0.456, (247.063, 220.372, 262.381)), (' B 104  TRP  CD1', ' B 240  THR HG23', -0.455, (251.087, 277.395, 209.224)), (' B 198  ASP  OD1', ' B 199  GLY  N  ', -0.455, (240.293, 258.678, 205.275)), (' B 143  VAL HG12', ' B 152  TRP  HE3', -0.454, (248.729, 296.619, 202.296)), (' B 805  ILE HG22', ' B 818  ILE HD12', -0.453, (225.345, 255.637, 270.438)), (' H  91  THR HG23', ' H 120  THR  HA ', -0.451, (255.541, 301.39, 159.335)), (' A 902  MET  HE1', ' A1049  LEU HD13', -0.451, (214.875, 221.06, 283.059)), (' B 565  PHE  O  ', ' C  42  VAL  HA ', -0.45, (260.202, 214.452, 222.268)), (' C 188  ASN  HA ', ' C 209  PRO  HA ', -0.45, (268.906, 188.136, 223.941)), (' A 146  HIS  CE1', ' A 148  ASN  HB2', -0.449, (162.272, 206.611, 192.038)), (' F  91  THR HG23', ' F 120  THR  HA ', -0.448, (153.131, 216.616, 160.234)), (' H  12  VAL HG11', ' H  86  LEU HD12', -0.448, (248.845, 305.392, 162.301)), (' H  17  SER  OG ', ' H  82  GLN  NE2', -0.448, (243.684, 305.422, 167.723)), (' A 143  VAL HG12', ' A 152  TRP  HE3', -0.448, (161.866, 214.056, 202.976)), (' A 578  ASP  HB3', ' A 581  THR  O  ', -0.446, (216.095, 270.283, 216.104)), (' H   5  VAL HG23', ' H  23  ALA  HB3', -0.446, (246.36, 287.139, 171.58)), (' B 950  ASP  OD2', ' B 954  GLN  NE2', -0.445, (234.201, 243.446, 249.133)), (' B 363  ALA  O  ', ' B 526  GLY  HA2', -0.444, (264.082, 222.586, 198.66)), (' C 884  SER  HB2', ' C 887  THR  OG1', -0.443, (248.296, 236.958, 281.79)), (' B  52  GLN  HA ', ' B 274  THR  HA ', -0.443, (244.051, 256.193, 223.813)), (' B 396  TYR  HB2', ' B 514  SER  OG ', -0.442, (255.467, 215.514, 187.148)), (' D  91  THR HG23', ' D 120  THR  HA ', -0.442, (277.927, 173.718, 158.515)), (' C 805  ILE HG22', ' C 818  ILE HD12', -0.442, (254.176, 220.813, 270.615)), (' C 332  ILE HG12', ' C 333  THR  H  ', -0.442, (201.088, 200.389, 199.948)), (' A 206  LYS  HB2', ' A 223  LEU  HA ', -0.441, (185.813, 217.602, 221.129)), (' A 458  LYS  HA ', ' A 458  LYS  HD3', -0.439, (257.133, 242.598, 193.601)), (' B 699  LEU HD22', ' C 873  TYR  CE2', -0.439, (253.283, 238.572, 262.565)), (' D   5  VAL HG23', ' D  23  ALA  HB3', -0.439, (270.826, 188.261, 172.02)), (' B 914  ASN  N  ', ' B 914  ASN HD22', -0.439, (231.481, 244.056, 295.351)), (' A 310  LYS  HG3', ' A 600  PRO  HA ', -0.438, (197.435, 234.068, 250.209)), (' B 565  PHE  HD1', ' B 576  VAL HG12', -0.438, (261.499, 220.447, 219.965)), (' C 296  LEU HD13', ' C 608  VAL HG11', -0.438, (241.534, 196.421, 241.616)), (' B 358  ILE  HB ', ' B 395  VAL  HB ', -0.436, (260.709, 215.534, 191.966)), (' A 351  TYR  CE1', ' A 452  LEU  HB2', -0.436, (245.706, 250.445, 182.849)), (' B  57  PRO  O  ', ' B  60  SER  HB2', -0.434, (253.327, 265.607, 224.757)), (' F   5  VAL HG23', ' F  23  ALA  HB3', -0.434, (169.767, 215.182, 172.705)), (' A 336  CYS  HB2', ' A 363  ALA  HB2', -0.434, (221.774, 259.475, 195.062)), (' A 712  ILE HG22', ' A1077  THR  HB ', -0.434, (214.163, 245.067, 294.046)), (' A 736  VAL HG22', ' A 858  LEU  HG ', -0.433, (221.764, 214.055, 236.262)), (' B 189  LEU  N  ', ' B 208  THR  O  ', -0.433, (244.986, 282.948, 222.918)), (' A1097  SER  HB2', ' A1102  TRP  CD2', -0.431, (213.529, 245.761, 301.848)), (' B 252  GLY  HA3', ' L  33  TYR  OH ', -0.431, (263.712, 296.858, 193.485)), (' C 502  GLY  O  ', ' C 506  GLN  HG3', -0.431, (221.174, 229.593, 176.713)), (' A1083  HIS  CE1', ' A1137  VAL  H  ', -0.431, (221.585, 243.436, 311.761)), (' C 320  VAL HG21', ' C 619  GLU  HG2', -0.43, (221.172, 195.059, 230.223)), (' B 770  ILE  O  ', ' B 774  GLN  HG2', -0.43, (218.683, 238.352, 248.8)), (' B 712  ILE HG22', ' B1077  THR  HB ', -0.429, (250.841, 235.622, 293.982)), (' A 280  ASN HD21', ' A 284  THR  HB ', -0.429, (190.868, 212.526, 231.156)), (' A 188  ASN  HA ', ' A 209  PRO  HA ', -0.429, (173.823, 215.557, 224.178)), (' C  57  PRO  O  ', ' C  60  SER  HB2', -0.428, (247.27, 190.827, 224.201)), (' B 884  SER  HB2', ' B 887  THR  OG1', -0.428, (214.173, 241.757, 282.014)), (' F  12  VAL HG11', ' F  86  LEU HD12', -0.428, (152.609, 208.844, 163.535)), (' B 331  ASN  O  ', ' B 332  ILE  HB ', -0.427, (271.274, 222.142, 204.231)), (' B 106  PHE  HB2', ' B 117  LEU  HB3', -0.427, (247.638, 270.0, 202.52)), (' B 335  LEU  O  ', ' B 336  CYS  SG ', -0.427, (266.705, 216.46, 196.296)), (' C 898  PHE  HZ ', ' C1050  MET  HE1', -0.426, (249.457, 223.888, 281.178)), (' A 770  ILE  O  ', ' A 774  GLN  HG2', -0.425, (227.187, 215.391, 249.116)), (' C 431  GLY  HA2', ' C 515  PHE  CD2', -0.424, (213.464, 218.076, 201.062)), (' B1097  SER  HB2', ' B1102  TRP  CD2', -0.424, (252.104, 236.169, 301.792)), (' A1080  ALA  C  ', ' A1132  ILE HG13', -0.424, (222.671, 248.819, 301.725)), (' D  12  VAL HG11', ' D  86  LEU HD12', -0.424, (284.83, 176.808, 162.123)), (' B1083  HIS  CE1', ' B1137  VAL  H  ', -0.423, (245.758, 229.931, 311.588)), (' B 704  SER  HB3', ' C 790  LYS  HE2', -0.423, (261.223, 239.31, 276.827)), (' C  18  LEU HD12', ' C 255  SER  HA ', -0.423, (261.831, 171.619, 199.254)), (' C 360  ASN  HA ', ' C 523  THR  HB ', -0.423, (201.402, 207.747, 202.163)), (' A 320  VAL HG21', ' A 619  GLU  HG2', -0.422, (203.482, 254.391, 230.721)), (' B1073  LYS  HB2', ' B1075  PHE  CE2', -0.421, (250.104, 244.778, 293.138)), (' B 140  PHE  O  ', ' B 158  ARG  HB2', -0.421, (253.009, 285.406, 198.79)), (' C 167  THR HG21', ' C1308  NAG  H61', -0.421, (254.7, 203.199, 192.43)), (' C 358  ILE  HB ', ' C 395  VAL  HB ', -0.42, (205.473, 213.634, 197.958)), (' C 140  PHE  O  ', ' C 158  ARG  HB2', -0.42, (265.057, 182.056, 197.803)), (' C 106  PHE  HB2', ' C 117  LEU  HB3', -0.42, (254.935, 195.145, 202.211)), (' C 336  CYS  HB2', ' C 363  ALA  HB2', -0.419, (207.988, 208.082, 195.651)), (' C 351  TYR  CE1', ' C 452  LEU  HB2', -0.419, (203.456, 233.167, 182.827)), (' B 521  PRO  HG2', ' C 230  PRO  HB3', -0.419, (255.915, 208.93, 202.73)), (' A 328  ARG  NH2', ' A 531  THR  O  ', -0.419, (209.208, 265.971, 211.83)), (' B 321  GLN  HA ', ' B 322  PRO  HD2', -0.418, (258.577, 240.074, 223.262)), (' C 421  TYR  CD1', ' C 457  ARG  HB3', -0.418, (206.78, 241.314, 192.588)), (' B 353  TRP  O  ', ' B 466  ARG  NE ', -0.418, (257.984, 210.021, 177.714)), (' B 727  LEU HD11', ' B1028  LYS  HD2', -0.416, (229.005, 240.061, 265.015)), (' B1080  ALA  C  ', ' B1132  ILE HG13', -0.415, (250.029, 226.291, 301.502)), (' C1097  SER  HB2', ' C1102  TRP  CD2', -0.414, (224.487, 207.299, 301.902)), (' B 502  GLY  O  ', ' B 506  GLN  HG3', -0.414, (265.221, 229.585, 164.944)), (' B 811  LYS  NZ ', ' B 820  ASP  OD2', -0.414, (220.035, 263.128, 264.356)), (' A 502  GLY  O  ', ' A 506  GLN  HG3', -0.414, (233.838, 237.106, 176.375)), (' A 215  ASP  HA ', ' A 266  TYR  OH ', -0.414, (172.224, 228.043, 224.366)), (' B 331  ASN  HB2', ' B 332  ILE HG22', -0.414, (273.506, 221.43, 205.329)), (' C 656  VAL HG12', ' C 658  ASN  H  ', -0.413, (229.776, 188.198, 258.87)), (' B 340  GLU  O  ', ' B 344  ALA  HB2', -0.412, (269.609, 215.467, 182.173)), (' B 318  PHE  N  ', ' B 593  GLY  O  ', -0.411, (254.232, 241.612, 233.692)), (' B 326  ILE  O  ', ' B 542  ASN  N  ', -0.411, (263.513, 229.335, 215.204)), (' A  64  TRP  HE1', ' A 264  ALA  HB1', -0.411, (170.695, 229.111, 219.715)), (' D  44  GLY  HA2', ' E  88  TYR  OH ', -0.409, (267.129, 164.688, 166.708)), (' A 811  LYS  NZ ', ' A 820  ASP  OD2', -0.408, (205.564, 204.45, 264.413)), (' A 360  ASN  HA ', ' A 523  THR  HB ', -0.407, (224.319, 265.54, 201.819)), (' F  44  GLY  HA2', ' G  88  TYR  OH ', -0.407, (150.714, 230.088, 169.225)), (' C 189  LEU  N  ', ' C 208  THR  O  ', -0.407, (266.536, 188.632, 222.788)), (' D  83  MET  HE2', ' D  86  LEU HD21', -0.406, (283.035, 174.919, 165.898)), (' C 328  ARG  HD2', ' C 533  LEU HD12', -0.406, (207.523, 196.363, 215.382)), (' C 770  ILE  O  ', ' C 774  GLN  HG2', -0.405, (243.001, 234.55, 249.01)), (' C 148  ASN  O  ', ' C 149  ASN  HB2', -0.405, (283.233, 185.587, 195.165)), (' C 715  PRO  CB ', ' C1069  PRO  HB3', -0.404, (235.368, 210.322, 286.43)), (' B 148  ASN  O  ', ' B 149  ASN  HB2', -0.404, (240.092, 298.876, 195.194)), (' B 421  TYR  CD1', ' B 457  ARG  HB3', -0.404, (247.105, 213.141, 167.679)), (' F  83  MET  HE2', ' F  86  LEU HD21', -0.404, (152.291, 211.568, 167.485)), (' C 796  ASP  N  ', ' C 796  ASP  OD1', -0.404, (260.515, 227.489, 285.127)), (' B 930  ALA  O  ', ' B 934  ILE HG12', -0.402, (233.34, 255.325, 272.685)), (' B 980  ILE HG23', ' B 984  LEU HD12', -0.402, (222.692, 242.071, 211.927)), (' B 715  PRO  HB3', ' B1069  PRO  HB3', -0.401, (243.827, 244.172, 285.695)), (' H  44  GLY  HA2', ' L  88  TYR  OH ', -0.401, (268.341, 297.507, 168.503)), (' C 722  VAL  HA ', ' C1064  HIS  O  ', -0.401, (244.527, 217.426, 274.403)), (' A 252  GLY  HA3', ' G  33  TYR  OH ', -0.4, (153.747, 226.327, 193.81)), (' A 148  ASN  O  ', ' A 149  ASN  HB2', -0.4, (163.562, 205.02, 195.773)), (' C 461  LEU HD21', ' C 467  ASP  HB2', -0.4, (202.76, 235.881, 193.787))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
