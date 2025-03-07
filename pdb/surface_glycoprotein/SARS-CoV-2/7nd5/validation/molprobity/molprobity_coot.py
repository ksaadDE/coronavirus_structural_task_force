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
data['rama'] = [('B', ' 123 ', 'ALA', 0.04072751938021581, (220.83199999999994, 183.201, 136.017))]
data['omega'] = [('B', ' 123 ', 'ALA', None, (219.88999999999993, 182.143, 135.65900000000005)), ('H', ' 151 ', 'PRO', None, (173.80399999999995, 171.03, 63.117)), ('H', ' 153 ', 'PRO', None, (171.08799999999994, 166.445, 59.846)), ('L', '   8 ', 'PRO', None, (181.65999999999994, 135.184, 66.913)), ('L', '  95 ', 'PRO', None, (176.333, 144.48600000000005, 90.03200000000002)), ('L', ' 143 ', 'PRO', None, (185.371, 141.10400000000004, 51.83300000000001))]
data['rota'] = [('A', ' 590 ', 'CYS', 0.17763404386542922, (174.86799999999994, 194.48100000000005, 159.12200000000007)), ('A', ' 615 ', 'VAL', 0.25613862273475146, (173.582, 196.26400000000007, 171.55600000000007)), ('A', ' 900 ', 'MET', 0.23515272988325375, (146.24299999999994, 165.01200000000006, 222.46900000000005)), ('A', '1004 ', 'LEU', 0.21969587376264008, (153.277, 165.371, 164.966)), ('B', ' 376 ', 'THR', 0.25801404159705427, (177.41799999999998, 137.352, 107.215)), ('B', '1017 ', 'GLU', 0.28039915153179534, (168.44, 167.281, 183.753)), ('C', ' 231 ', 'ILE', 0.13487182926903726, (152.10599999999994, 132.346, 131.51800000000006)), ('C', ' 517 ', 'LEU', 0.1416290145061902, (141.10599999999994, 177.962, 141.26500000000004)), ('C', '1004 ', 'LEU', 0.2613839214319952, (167.862, 157.026, 164.1))]
data['cbeta'] = []
data['probe'] = [(' B1126  CYS  HB2', ' B1132  ILE HD13', -0.823, (168.116, 139.639, 233.889)), (' B1129  VAL  HB ', ' B1132  ILE HD11', -0.809, (168.166, 140.058, 230.512)), (' B1040  VAL HG21', ' C1035  GLY  HA3', -0.766, (171.422, 155.738, 207.789)), (' A 736  VAL HG11', ' A1004  LEU HD21', -0.718, (148.95, 163.572, 166.081)), (' C 742  ILE  O  ', ' C1000  ARG  NH1', -0.685, (171.274, 152.421, 154.028)), (' H  29  VAL HG13', ' H  34  MET  HG3', -0.684, (157.021, 151.987, 83.011)), (' A 722  VAL HG22', ' A1065  VAL HG22', -0.683, (146.683, 174.777, 208.989)), (' A  29  THR HG23', ' A  62  VAL HG23', -0.66, (144.988, 211.876, 154.578)), (' B 736  VAL HG11', ' B1004  LEU HD21', -0.658, (168.118, 178.257, 165.926)), (' A 393  THR HG21', ' A 520  ALA  HB3', -0.64, (189.713, 180.539, 141.118)), (' A 914  ASN  ND2', ' A1111  GLU  OE2', -0.636, (155.016, 174.029, 230.367)), (' C 224  GLU  N  ', ' C 224  GLU  OE1', -0.633, (151.65, 123.629, 150.944)), (' A 326  ILE HD12', ' A 539  VAL HG21', -0.628, (179.648, 198.383, 150.002)), (' B1116  THR  OG1', ' B1118  ASP  OD1', -0.626, (173.043, 157.316, 237.897)), (' A 330  PRO  HB2', ' A 332  ILE HD13', -0.623, (190.112, 193.138, 135.107)), (' B 532  ASN  OD1', ' B 533  LEU  N  ', -0.608, (182.229, 127.669, 144.909)), (' C 722  VAL HG22', ' C1065  VAL HG22', -0.603, (162.927, 142.867, 206.916)), (' B 902  MET  HE1', ' B1049  LEU HD13', -0.6, (179.548, 170.626, 214.224)), (' C 909  ILE HD13', ' C1049  LEU HD21', -0.597, (161.097, 150.022, 214.862)), (' C 287  ASP  OD1', ' C 288  ALA  N  ', -0.592, (146.155, 130.593, 163.338)), (' B 287  ASP  OD1', ' B 288  ALA  N  ', -0.588, (200.49, 170.319, 163.089)), (' B1103  PHE  HZ ', ' K   1  NAG  H62', -0.587, (186.345, 152.474, 236.141)), (' C 720  ILE HG13', ' C 923  ILE HG23', -0.587, (161.249, 141.852, 215.088)), (' A1029  MET  HE2', ' A1053  PRO  HB3', -0.582, (146.365, 165.548, 200.173)), (' A1105  THR HG22', ' A1112  PRO  HA ', -0.576, (162.211, 179.057, 231.336)), (' H 123  PRO  HB3', ' H 149  TYR  HB3', -0.575, (178.151, 171.381, 56.51)), (' B1028  LYS  O  ', ' B1032  CYS  CB ', -0.572, (171.241, 171.03, 202.883)), (' C  64  TRP  HE1', ' C 264  ALA  HB1', -0.571, (130.277, 118.323, 147.467)), (' A1028  LYS  O  ', ' A1032  CYS  CB ', -0.571, (153.15, 166.006, 203.223)), (' L  37  GLN  HB2', ' L  47  LEU HD11', -0.567, (167.198, 138.64, 66.372)), (' C 908  GLY  O  ', ' C1038  LYS  NZ ', -0.562, (163.596, 157.152, 215.06)), (' A 195  LYS  HD3', ' A 197  ILE HD13', -0.557, (147.344, 193.915, 143.358)), (' A 552  LEU  HB3', ' A 585  LEU HD13', -0.556, (185.141, 196.351, 152.879)), (' C1029  MET  HE2', ' C1053  PRO  HB3', -0.555, (171.442, 147.908, 198.683)), (' C  65  PHE  O  ', ' C 264  ALA  HA ', -0.551, (129.925, 118.665, 144.754)), (' B 961  THR HG21', ' C 765  ARG HH22', -0.549, (177.871, 167.732, 168.334)), (' A 319  ARG  NH2', ' B 745  ASP  OD2', -0.543, (171.313, 190.523, 157.819)), (' B 703  ASN  OD1', ' B 704  SER  N  ', -0.543, (188.354, 143.521, 208.001)), (' C1106  GLN  NE2', ' C1111  GLU  OE1', -0.543, (157.219, 150.059, 227.116)), (' A1093  GLY  O  ', ' A1107  ARG  NH1', -0.539, (168.735, 173.626, 225.663)), (' B1028  LYS  NZ ', ' B1042  PHE  O  ', -0.539, (172.813, 165.5, 200.085)), (' A1028  LYS  O  ', ' A1032  CYS  HB3', -0.537, (153.028, 165.738, 202.759)), (' C 905  ARG  HD2', ' C1049  LEU  O  ', -0.537, (166.823, 149.964, 211.588)), (' B 302  THR HG21', ' B 315  THR HG22', -0.537, (188.931, 159.337, 167.807)), (' B 858  LEU HD23', ' B 959  LEU HD22', -0.535, (174.208, 178.121, 168.763)), (' B 393  THR HG23', ' B 517  LEU HD12', -0.535, (159.878, 141.948, 126.758)), (' A 122  ASN  O  ', ' A 124  THR  N  ', -0.533, (123.709, 208.524, 135.968)), (' A 707  TYR  HB3', ' B 792  PRO  HG3', -0.531, (176.867, 188.16, 215.681)), (' A 358  ILE  HB ', ' A 395  VAL  HB ', -0.531, (186.493, 180.161, 129.048)), (' H  61  ASP  OD1', ' H  64  LYS  NZ ', -0.527, (175.67, 154.165, 90.637)), (' B 908  GLY  O  ', ' B1038  LYS  NZ ', -0.527, (169.949, 164.42, 215.419)), (' B 811  LYS  O  ', ' B 813  SER  N  ', -0.527, (184.934, 192.477, 195.553)), (' A 117  LEU HD21', ' A 231  ILE HG21', -0.526, (142.05, 198.644, 133.667)), (' A  33  THR  OG1', ' A 219  GLY  O  ', -0.523, (140.055, 203.692, 161.662)), (' A 909  ILE HD13', ' A1049  LEU HD21', -0.521, (154.178, 171.979, 216.208)), (' C 328  ARG  NH1', ' C 578  ASP  OD2', -0.52, (121.578, 172.707, 146.926)), (' C 880  GLY  O  ', ' C 884  SER  OG ', -0.519, (178.526, 147.668, 209.773)), (' B1013  ILE HD13', ' C1012  LEU  HB3', -0.519, (167.237, 162.739, 175.387)), (' A 886  TRP  HZ3', ' A 905  ARG  HD3', -0.518, (152.43, 164.449, 215.42)), (' B  46  SER  N  ', ' B 279  TYR  O  ', -0.517, (194.314, 180.272, 163.075)), (' A 280  ASN  OD1', ' A 283  GLY  N  ', -0.517, (131.896, 189.112, 161.651)), (' B 376  THR  HB ', ' B 435  ALA  HB3', -0.515, (175.054, 136.255, 105.277)), (' C 902  MET  HE1', ' C1049  LEU HD13', -0.514, (164.113, 145.827, 214.126)), (' B 722  VAL HG22', ' B1065  VAL HG22', -0.513, (182.731, 171.761, 207.319)), (' A 280  ASN  ND2', ' A 284  THR  OG1', -0.51, (131.956, 191.891, 162.31)), (' C 738  CYS  SG ', ' C 739  THR  N  ', -0.51, (176.685, 156.402, 160.796)), (' B 805  ILE HG22', ' B 818  ILE HD12', -0.509, (185.048, 178.3, 202.055)), (' A 736  VAL HG22', ' A 858  LEU HD22', -0.508, (146.219, 165.173, 167.909)), (' H  82  MET  HB3', ' H  85  LEU HD21', -0.506, (169.509, 164.367, 80.654)), (' A 117  LEU HD21', ' A 231  ILE HD13', -0.505, (143.36, 198.373, 134.059)), (' B 455  LEU HD11', ' H 100  MET  HG3', -0.504, (162.237, 140.252, 87.485)), (' B 715  PRO  HD3', ' C 894  LEU HD13', -0.502, (182.335, 153.653, 217.454)), (' C1105  THR HG22', ' C1112  PRO  HA ', -0.502, (150.695, 152.072, 230.765)), (' A  39  PRO  HG3', ' A  51  THR HG21', -0.501, (144.28, 189.353, 154.844)), (' B 122  ASN  O  ', ' B 124  THR  N  ', -0.5, (218.893, 184.3, 134.899)), (' B  30  ASN  OD1', ' B  31  SER  N  ', -0.5, (210.939, 161.775, 158.31)), (' A 100  ILE HD13', ' A 263  ALA  HB2', -0.5, (131.946, 217.464, 145.995)), (' A 317  ASN  ND2', ' B 737  ASP  OD2', -0.499, (166.804, 187.959, 165.086)), (' B  52  GLN  N  ', ' B  52  GLN  OE1', -0.499, (189.982, 166.435, 153.111)), (' B1046  GLY  HA2', ' C 890  ALA  HA ', -0.497, (179.367, 159.199, 208.62)), (' C1028  LYS  O  ', ' C1032  CYS  CB ', -0.495, (167.195, 153.194, 202.121)), (' B 726  ILE HG12', ' B1061  VAL HG22', -0.494, (180.957, 172.739, 193.773)), (' C1053  PRO  O  ', ' C1054  GLN  NE2', -0.494, (170.586, 142.41, 199.616)), (' A 787  GLN  OE1', ' C 703  ASN  ND2', -0.493, (139.05, 151.416, 208.686)), (' A 804  GLN  NE2', ' F   1  NAG  O6 ', -0.489, (134.452, 179.599, 208.834)), (' B 770  ILE  O  ', ' B 774  GLN  HG2', -0.488, (166.11, 177.625, 180.923)), (' A 898  PHE  HZ ', ' A1050  MET  HE1', -0.487, (144.678, 169.764, 214.012)), (' B 537  LYS  O  ', ' B 539  VAL HG23', -0.486, (183.473, 134.619, 152.828)), (' B 354  ASN  O  ', ' B 398  ASP  HA ', -0.485, (161.578, 132.31, 109.309)), (' C 858  LEU HD23', ' C 959  LEU HD22', -0.484, (169.85, 148.136, 167.915)), (' B 858  LEU HD21', ' B 962  LEU HD23', -0.484, (173.062, 177.208, 166.76)), (' A 403  ARG  NH1', ' A 405  ASP  OD2', -0.482, (169.458, 160.055, 114.285)), (' C 303  LEU HD21', ' C 313  TYR  CE2', -0.481, (147.895, 144.112, 174.893)), (' C 756  TYR  OH ', ' C 994  ASP  OD1', -0.481, (169.129, 163.285, 151.32)), (' B 886  TRP  HB3', ' B1035  GLY  HA2', -0.48, (168.34, 174.454, 211.069)), (' C  40  ASP  N  ', ' C  40  ASP  OD1', -0.48, (155.668, 133.9, 151.937)), (' A 294  ASP  OD2', ' A 297  SER  OG ', -0.477, (151.039, 199.408, 167.345)), (' A  46  SER  HA ', ' A 279  TYR  O  ', -0.476, (135.965, 186.276, 165.025)), (' A1129  VAL HG13', ' B 917  TYR  HB3', -0.476, (182.076, 173.751, 227.878)), (' B 418  ILE  HA ', ' B 422  ASN  HB2', -0.474, (162.295, 139.317, 98.096)), (' A 852  ALA  O  ', ' A 856  ASN  ND2', -0.474, (140.026, 169.492, 164.301)), (' B 412  PRO  HG3', ' B 429  PHE  HB3', -0.473, (166.622, 146.565, 110.797)), (' B 598  ILE HG23', ' B 664  ILE HG21', -0.472, (191.596, 154.424, 178.695)), (' B1032  CYS  SG ', ' B1051  SER  OG ', -0.471, (174.468, 170.491, 204.878)), (' B1028  LYS  O  ', ' B1032  CYS  HB2', -0.47, (170.686, 170.506, 202.86)), (' C  60  SER  HA ', ' C1301  NAG  H82', -0.469, (131.557, 133.866, 155.738)), (' B 100  ILE HG22', ' B 242  LEU  HB2', -0.468, (223.07, 169.994, 139.865)), (' B 720  ILE HG13', ' B 923  ILE HG23', -0.468, (184.54, 169.913, 215.459)), (' B  33  THR  OG1', ' B 219  GLY  O  ', -0.467, (208.153, 169.298, 160.751)), (' B 369  TYR  HA ', ' B 377  PHE  HE2', -0.465, (177.924, 135.605, 116.137)), (' B1028  LYS  O  ', ' B1032  CYS  HB3', -0.464, (171.36, 171.531, 202.905)), (' C1043  CYS  HB3', ' C1048  HIS  CD2', -0.463, (163.039, 151.68, 205.723)), (' B 905  ARG  HD2', ' B1049  LEU  O  ', -0.462, (174.605, 170.994, 212.433)), (' A 328  ARG  NH1', ' A 578  ASP  OD2', -0.462, (187.853, 198.872, 145.64)), (' C1016  ALA  HA ', ' C1019  ARG  NH1', -0.462, (168.362, 161.435, 182.573)), (' A  41  LYS  HD3', ' C 520  ALA  HB2', -0.462, (136.773, 185.31, 145.119)), (' B 205  SER  HB3', ' B 226  LEU HD12', -0.461, (207.835, 178.205, 145.131)), (' A 905  ARG HH11', ' A1036  GLN  HB2', -0.46, (153.44, 164.988, 212.545)), (' B 276  LEU  HB3', ' B 289  VAL  CG2', -0.46, (195.035, 167.271, 162.712)), (' B 425  LEU HD21', ' B 512  VAL HG11', -0.459, (164.894, 140.259, 109.336)), (' A 236  THR HG21', ' D   1  NAG  H5 ', -0.459, (155.503, 203.175, 134.377)), (' C1081  ILE HD13', ' C1115  ILE HD13', -0.459, (148.624, 160.135, 236.684)), (' C1028  LYS  O  ', ' C1032  CYS  HB2', -0.458, (167.381, 154.031, 201.932)), (' B1129  VAL  HB ', ' B1132  ILE  CD1', -0.457, (168.708, 140.069, 231.001)), (' L  19  VAL HG21', ' L  78  LEU HD13', -0.456, (172.235, 133.486, 59.499)), (' A 766  ALA  O  ', ' A 770  ILE HG12', -0.456, (153.033, 158.879, 175.616)), (' B 895  GLN  N  ', ' B 895  GLN  OE1', -0.454, (169.367, 185.832, 218.22)), (' B 324  GLU  N  ', ' B 324  GLU  OE1', -0.454, (187.074, 137.261, 148.298)), (' A 880  GLY  O  ', ' A 884  SER  OG ', -0.453, (143.333, 159.063, 211.567)), (' B 366  SER  HA ', ' B 369  TYR  CZ ', -0.453, (178.577, 133.81, 122.506)), (' B 977  LEU HD11', ' B 993  ILE HG12', -0.452, (167.891, 179.416, 149.272)), (' L  24  ARG  HB2', ' L  24  ARG  HE ', -0.452, (182.404, 131.838, 75.298)), (' B 401  VAL HG22', ' B 509  ARG  HG2', -0.451, (169.766, 128.293, 102.516)), (' A 902  MET  HE1', ' A1049  LEU HD13', -0.451, (149.436, 172.282, 215.562)), (' B 778  THR HG22', ' B 865  LEU HD12', -0.449, (169.289, 182.903, 190.796)), (' B 730  SER  O  ', ' B1058  HIS  HB3', -0.448, (174.685, 176.659, 185.049)), (' H  18  LEU  HB3', ' H  82  MET  HE3', -0.447, (166.94, 165.598, 78.442)), (' B  45  SER  HB2', ' B 281  GLU  HA ', -0.446, (194.334, 184.244, 162.689)), (' A1086  LYS  HD2', ' A1122  VAL HG11', -0.446, (179.05, 166.594, 239.447)), (' C1106  GLN  HG3', ' C1109  PHE  O  ', -0.446, (154.047, 151.586, 225.313)), (' C 759  PHE  CD2', ' C1001  LEU HD21', -0.445, (171.508, 163.876, 159.56)), (' B 417  LYS  NZ ', ' L  92  ASP  OD2', -0.445, (166.577, 138.812, 89.716)), (' B 111  ASP  OD1', ' B 112  SER  N  ', -0.444, (211.373, 162.661, 122.259)), (' L  33  LEU HD13', ' L  71  PHE  CG ', -0.444, (174.444, 132.067, 77.717)), (' C 122  ASN  O  ', ' C 124  THR  N  ', -0.444, (146.86, 109.289, 134.186)), (' C 465  GLU  OE1', ' D   1  NAG  H81', -0.443, (155.006, 194.755, 131.892)), (' A 901  GLN  O  ', ' A 905  ARG  HG2', -0.442, (149.906, 166.008, 217.566)), (' B 802  PHE  HD1', ' B 805  ILE HD11', -0.441, (182.276, 179.15, 207.728)), (' B1053  PRO  O  ', ' B1054  GLN  NE2', -0.441, (179.47, 179.282, 200.797)), (' C 676  THR  HA ', ' C 690  GLN  HA ', -0.44, (130.267, 134.625, 185.536)), (' A 796  ASP  N  ', ' A 796  ASP  OD1', -0.439, (133.134, 166.887, 218.555)), (' C 734  THR HG21', ' C 959  LEU HD21', -0.437, (170.205, 149.726, 170.437)), (' B 566  GLY  HA2', ' C  43  PHE  HB3', -0.436, (164.552, 131.228, 155.836)), (' C 620  VAL HG11', ' C 651  ILE HD11', -0.435, (127.863, 150.097, 170.041)), (' A 720  ILE HG13', ' A 923  ILE HG23', -0.434, (147.449, 176.629, 217.362)), (' B 222  ALA  HB2', ' B 285  ILE  HB ', -0.434, (201.75, 176.402, 157.246)), (' B 342  PHE  HB2', ' B1305  NAG  H82', -0.431, (171.718, 126.599, 114.401)), (' C 358  ILE  HB ', ' C 395  VAL  HB ', -0.43, (136.843, 181.232, 130.245)), (' C 229  LEU  HB3', ' C 231  ILE HG23', -0.43, (152.066, 129.546, 133.479)), (' C 555  SER  HB2', ' C 586  ASP  HB2', -0.429, (125.778, 176.126, 159.233)), (' H 172  ALA  HB2', ' H 182  LEU HD12', -0.429, (177.636, 162.837, 57.22)), (' C 715  PRO  HA ', ' C1072  GLU  HA ', -0.428, (147.064, 148.401, 220.177)), (' A1013  ILE HD13', ' B1012  LEU  HB3', -0.427, (162.783, 168.998, 176.069)), (' L 165 AVAL HG22', ' L 177  LEU HD12', -0.424, (185.019, 151.397, 56.573)), (' A1106  GLN  HG3', ' A1109  PHE  O  ', -0.424, (160.12, 176.756, 226.405)), (' B 541  PHE  CZ ', ' B 587  ILE HD13', -0.423, (173.898, 136.224, 152.894)), (' A 866  THR  OG1', ' A 869  MET  SD ', -0.423, (135.04, 159.539, 190.149)), (' C 384  PRO  HA ', ' C 387  LEU  HG ', -0.423, (142.383, 169.563, 132.417)), (' C  45  SER  O  ', ' C  47  VAL HG23', -0.421, (160.729, 132.62, 164.513)), (' B 901  GLN  O  ', ' B 905  ARG  HG2', -0.421, (174.396, 173.052, 216.603)), (' B 709  ASN  ND2', ' C 796  ASP  OD2', -0.42, (177.058, 134.706, 221.247)), (' B 714  ILE HD12', ' B1096  VAL HG11', -0.42, (181.279, 151.146, 225.214)), (' A 864  LEU  HA ', ' C 667  GLY  HA2', -0.42, (139.023, 156.736, 184.321)), (' C 731  MET  N  ', ' C 774  GLN  OE1', -0.419, (170.263, 152.015, 182.055)), (' B1081  ILE HD11', ' B1115  ILE HG21', -0.419, (174.131, 149.087, 236.134)), (' A 189  LEU  HB2', ' A 210  ILE HD13', -0.417, (132.548, 210.29, 154.774)), (' C 403  ARG  NH1', ' C 405  ASP  OD2', -0.417, (163.004, 179.393, 114.327)), (' A 766  ALA  HB1', ' A1012  LEU HD11', -0.415, (155.455, 159.597, 173.912)), (' B 727  LEU HD11', ' B1028  LYS  HD2', -0.415, (173.078, 168.855, 196.461)), (' C 201  PHE  HB2', ' C 231  ILE HD11', -0.415, (148.737, 132.378, 135.014)), (' A1028  LYS  O  ', ' A1032  CYS  HB2', -0.415, (153.882, 165.787, 203.213)), (' A 961  THR HG21', ' B 762  GLN  CD ', -0.415, (153.993, 174.757, 167.998)), (' C 328  ARG  NH2', ' C 580  GLN  OE1', -0.415, (120.423, 172.044, 142.981)), (' H 175  GLN  NE2', ' H 181  SER  OG ', -0.415, (184.368, 167.87, 60.139)), (' B 296  LEU  HB2', ' B 608  VAL HG11', -0.414, (197.786, 157.691, 170.854)), (' C 749  CYS  HB2', ' C 977  LEU HD21', -0.414, (174.154, 153.723, 150.006)), (' A 825  LYS  HB2', ' A 945  LEU HD12', -0.414, (141.316, 178.219, 191.34)), (' B 763  LEU HD22', ' B1008  VAL HG21', -0.413, (163.938, 174.351, 168.276)), (' A1006  THR  O  ', ' A1010  GLN  HG2', -0.413, (157.23, 168.702, 170.699)), (' A 611  LEU HD22', ' A 666  ILE HG23', -0.413, (165.568, 193.63, 179.409)), (' A 676  THR  HA ', ' A 690  GLN  HA ', -0.413, (152.894, 206.796, 187.63)), (' B1103  PHE  CZ ', ' K   1  NAG  H62', -0.413, (185.791, 152.38, 236.086)), (' B 419  ALA  HA ', ' B 423  TYR  O  ', -0.412, (162.976, 142.27, 101.789)), (' B 802  PHE  CD1', ' B 805  ILE HD11', -0.412, (182.037, 179.112, 207.842)), (' B 905  ARG HH11', ' B1036  GLN  HB2', -0.411, (171.919, 171.445, 211.889)), (' C 290  ASP  HB3', ' C 293  LEU  HB2', -0.41, (139.698, 136.848, 161.113)), (' A 733  LYS  HE3', ' A 771  ALA  HB1', -0.41, (145.36, 158.434, 179.566)), (' A 972  ALA  HA ', ' A 992  GLN  OE1', -0.41, (153.037, 170.389, 146.562)), (' A 770  ILE HD12', ' A1015  ALA  CB ', -0.41, (154.197, 162.22, 179.438)), (' H  99  LEU  HB3', ' H 102  TYR  HB2', -0.409, (160.018, 138.369, 81.688)), (' A 894  LEU HD13', ' C 715  PRO  HD3', -0.408, (148.016, 152.261, 219.0)), (' C 770  ILE  O  ', ' C 774  GLN  HG2', -0.407, (173.739, 154.993, 180.192)), (' A 226  LEU  HA ', ' A 226  LEU HD23', -0.407, (132.817, 193.802, 144.672)), (' C  46  SER  HA ', ' C 279  TYR  O  ', -0.407, (157.618, 130.117, 165.69)), (' C1032  CYS  SG ', ' C1051  SER  OG ', -0.406, (165.407, 150.86, 204.058)), (' L 165 BVAL HG22', ' L 177  LEU HD12', -0.405, (185.322, 151.183, 56.369)), (' L  87  TYR  HB3', ' L 103  GLY  HA2', -0.405, (176.194, 141.606, 69.969)), (' C1024  LEU HD11', ' C1028  LYS  HE2', -0.405, (162.885, 155.997, 196.606)), (' A 816  SER  N  ', ' A 819  GLU  OE1', -0.403, (135.208, 170.225, 199.406)), (' A 230  PRO  HB2', ' C 355  ARG HH11', -0.403, (142.484, 189.87, 131.438)), (' A 968  SER  HB3', ' B 755  GLN  O  ', -0.403, (153.491, 175.28, 155.691)), (' A1031  GLU  HG2', ' C1040  VAL  O  ', -0.402, (157.247, 159.312, 203.963)), (' A 449  TYR  HB3', ' A 494  SER  HB3', -0.402, (182.705, 159.173, 106.921)), (' B 996  LEU  HA ', ' B 996  LEU HD23', -0.402, (170.093, 173.029, 152.94)), (' C 818  ILE  O  ', ' C 822  LEU  HG ', -0.401, (166.351, 137.967, 194.09)), (' C 727  LEU HD11', ' C1028  LYS  HD2', -0.401, (164.316, 152.789, 196.025)), (' A 234  ASN  OD1', ' A 235  ILE  N  ', -0.401, (151.956, 200.862, 133.598)), (' B 654  GLU  HB3', ' B 693  ILE HG22', -0.401, (201.206, 147.088, 182.075)), (' A 598  ILE HG23', ' A 664  ILE HG21', -0.4, (158.58, 193.517, 181.03)), (' A 727  LEU HD11', ' A1028  LYS  HD2', -0.4, (153.862, 169.408, 197.382))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
