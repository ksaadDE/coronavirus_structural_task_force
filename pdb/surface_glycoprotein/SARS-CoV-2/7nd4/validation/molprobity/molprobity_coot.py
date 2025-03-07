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
data['rama'] = [('A', ' 123 ', 'ALA', 0.03162235156942584, (119.40799999999997, 207.674, 168.19099999999995)), ('A', ' 331 ', 'ASN', 0.015235676164315185, (132.86399999999992, 131.215, 168.38399999999993)), ('A', ' 699 ', 'LEU', 0.0018682476154449031, (136.348, 160.022, 113.23099999999997)), ('B', ' 123 ', 'ALA', 0.03162097676046885, (148.54299999999995, 103.664, 168.281)), ('B', ' 331 ', 'ASN', 0.015024596145657392, (208.061, 153.511, 168.267)), ('B', ' 699 ', 'LEU', 0.0018782714853557503, (181.235, 142.066, 113.19199999999998)), ('C', ' 123 ', 'ALA', 0.03186126108822272, (223.98199999999994, 180.806, 168.359)), ('C', ' 331 ', 'ASN', 0.015232282740103723, (151.057, 207.434, 168.293)), ('C', ' 699 ', 'LEU', 0.001863420770467564, (174.41999999999993, 189.928, 113.23399999999998))]
data['omega'] = [('D', ' 108 ', 'PRO', None, (139.964, 127.61200000000002, 229.709)), ('F', ' 108 ', 'PRO', None, (207.65999999999994, 162.453, 229.59799999999998)), ('H', ' 108 ', 'PRO', None, (143.067, 203.366, 229.478))]
data['rota'] = [('A', ' 319 ', 'ARG', 0.005172302334114948, (135.46599999999992, 157.817, 147.996)), ('B', ' 319 ', 'ARG', 0.005122526552852117, (183.667, 142.45, 147.95199999999994)), ('C', ' 319 ', 'ARG', 0.004670949097191936, (172.84599999999995, 191.839, 147.993)), ('H', '  55 ', 'ASN', 0.2877673724564841, (135.36, 188.326, 237.10699999999997)), ('H', ' 119 ', 'GLN', 0.0, (155.02200000000005, 200.78999999999994, 243.82299999999995)), ('D', '  55 ', 'ASN', 0.2879461714895007, (156.853, 128.31099999999995, 237.329)), ('D', ' 119 ', 'GLN', 0.0, (136.46300000000005, 139.739, 243.70999999999998)), ('F', '  55 ', 'ASN', 0.2886325964697786, (198.227, 176.651, 236.895)), ('F', ' 119 ', 'GLN', 0.0, (199.21800000000005, 153.464, 243.85499999999996))]
data['cbeta'] = [('A', ' 331 ', 'ASN', ' ', 0.29156918425595113, (131.69599999999994, 130.496, 167.691)), ('B', ' 331 ', 'ASN', ' ', 0.2925525160478652, (209.26599999999993, 152.857, 167.572)), ('C', ' 331 ', 'ASN', ' ', 0.291293086307142, (151.021, 208.804, 167.59799999999996))]
data['probe'] = [(' B 485  GLY  HA2', ' F 105  THR HG23', -0.671, (205.426, 174.144, 227.482)), (' B1103  PHE  HZ ', ' R   1  NAG  H62', -0.652, (174.615, 144.377, 71.698)), (' A1103  PHE  HZ ', ' M   1  NAG  H62', -0.648, (141.423, 164.734, 71.325)), (' C1103  PHE  HZ ', ' W   1  NAG  H62', -0.639, (176.215, 182.937, 71.455)), (' L   3  ALA  HB3', ' L 100  VAL HG11', -0.634, (159.078, 181.88, 228.517)), (' G   3  ALA  HB3', ' G 100  VAL HG11', -0.634, (181.489, 159.07, 228.487)), (' E   3  ALA  HB3', ' E 100  VAL HG11', -0.632, (150.967, 151.811, 227.989)), (' A 736  VAL HG22', ' A 858  LEU  HG ', -0.628, (163.457, 181.144, 141.186)), (' B 391  CYS  HA ', ' B 525  CYS  HA ', -0.627, (195.78, 160.715, 177.593)), (' C 391  CYS  HA ', ' C 525  CYS  HA ', -0.627, (150.504, 193.61, 177.772)), (' B 736  VAL HG22', ' B 858  LEU  HG ', -0.622, (149.282, 155.048, 141.123)), (' A 391  CYS  HA ', ' A 525  CYS  HA ', -0.621, (145.048, 137.765, 177.759)), (' C 736  VAL HG22', ' C 858  LEU  HG ', -0.62, (178.772, 155.485, 140.961)), (' A1040  VAL HG21', ' B1035  GLY  HA3', -0.618, (154.66, 160.923, 100.355)), (' B 557  LYS  NZ ', ' B 574  ASP  OD2', -0.613, (198.545, 159.93, 145.638)), (' C 557  LYS  NZ ', ' C 574  ASP  OD2', -0.612, (150.693, 195.687, 145.615)), (' A 854  LYS  NZ ', ' C 568  ASP  OD2', -0.609, (154.581, 191.567, 143.591)), (' A 977  LEU HD11', ' A 993  ILE HG12', -0.602, (165.904, 178.608, 160.529)), (' A 557  LYS  NZ ', ' A 574  ASP  OD2', -0.598, (142.989, 136.799, 145.81)), (' A 319  ARG  HG2', ' A 319  ARG HH11', -0.597, (137.668, 158.48, 151.298)), (' C 319  ARG  HG2', ' C 319  ARG HH11', -0.596, (171.986, 190.031, 151.007)), (' C 977  LEU HD11', ' C 993  ILE HG12', -0.594, (176.023, 155.208, 160.251)), (' B 811  LYS  NZ ', ' B 820  ASP  OD2', -0.594, (141.273, 138.203, 112.861)), (' B 319  ARG  HG2', ' B 319  ARG HH11', -0.594, (182.477, 144.065, 150.927)), (' B 521  PRO  HB2', ' C 230  PRO  HB2', -0.593, (197.566, 170.72, 174.199)), (' A 568  ASP  OD2', ' B 854  LYS  NZ ', -0.591, (145.186, 142.205, 143.469)), (' C 726  ILE HG12', ' C1061  VAL HG22', -0.589, (183.925, 164.772, 114.921)), (' B 977  LEU HD11', ' B 993  ILE HG12', -0.588, (150.606, 158.4, 160.38)), (' B 726  ILE HG12', ' B1061  VAL HG22', -0.587, (155.31, 146.615, 114.783)), (' L  36  TRP  HB2', ' L  49  ILE  HB ', -0.586, (157.267, 196.336, 224.084)), (' G  36  TRP  HB2', ' G  49  ILE  HB ', -0.585, (194.55, 153.687, 223.927)), (' C 811  LYS  NZ ', ' C 820  ASP  OD2', -0.585, (197.747, 157.047, 112.946)), (' A 726  ILE HG12', ' A1061  VAL HG22', -0.584, (153.434, 180.719, 114.693)), (' A 811  LYS  NZ ', ' A 820  ASP  OD2', -0.582, (152.929, 196.628, 112.887)), (' E  36  TRP  HB2', ' E  49  ILE  HB ', -0.578, (139.168, 143.574, 224.088)), (' F  70  THR  HB ', ' F  83  LYS  HB2', -0.572, (188.22, 169.961, 249.337)), (' F  53  ILE HD13', ' F  73  VAL HG23', -0.57, (195.955, 171.901, 243.15)), (' D  53  ILE HD13', ' D  73  VAL HG23', -0.568, (153.71, 132.258, 243.702)), (' H  70  THR  HB ', ' H  83  LYS  HB2', -0.567, (146.114, 183.826, 249.979)), (' D  70  THR  HB ', ' D  83  LYS  HB2', -0.567, (155.614, 140.291, 249.838)), (' H  53  ILE HD13', ' H  73  VAL HG23', -0.564, (140.724, 188.796, 243.506)), (' C1028  LYS  O  ', ' C1032  CYS  CB ', -0.561, (174.376, 160.514, 106.699)), (' A1028  LYS  O  ', ' A1032  CYS  CB ', -0.56, (161.618, 174.203, 106.271)), (' B 763  LEU HD22', ' B1008  VAL HG21', -0.556, (154.639, 162.919, 140.84)), (' C 763  LEU HD22', ' C1008  VAL HG21', -0.556, (169.634, 156.69, 140.922)), (' C 364  ASP  HA ', ' C 527  PRO  HG3', -0.555, (153.229, 202.862, 178.753)), (' A 763  LEU HD22', ' A1008  VAL HG21', -0.552, (168.028, 172.432, 141.068)), (' D  41  GLN  HB2', ' D  47  LEU HD23', -0.548, (142.391, 148.725, 238.611)), (' B1028  LYS  O  ', ' B1032  CYS  CB ', -0.546, (155.881, 157.012, 106.557)), (' B 364  ASP  HA ', ' B 527  PRO  HG3', -0.546, (202.951, 154.216, 179.216)), (' F  41  GLN  HB2', ' F  47  LEU HD23', -0.543, (188.273, 153.482, 239.197)), (' A 364  ASP  HA ', ' A 527  PRO  HG3', -0.541, (135.775, 135.501, 178.83)), (' H  99  ARG  HE ', ' H 115  ASP  HB3', -0.539, (145.893, 199.228, 233.608)), (' H  41  GLN  HB2', ' H  47  LEU HD23', -0.536, (160.351, 191.312, 238.969)), (' F  99  ARG  HE ', ' F 115  ASP  HB3', -0.535, (202.883, 161.911, 233.611)), (' B 568  ASP  OD2', ' C 854  LYS  NZ ', -0.533, (192.635, 158.347, 143.527)), (' A1035  GLY  HA3', ' C1040  VAL HG21', -0.53, (166.614, 173.805, 100.503)), (' D 100  HIS  NE2', ' D 112  TYR  O  ', -0.529, (147.591, 138.093, 228.972)), (' B 379  CYS  HA ', ' B 432  CYS  HA ', -0.529, (193.676, 154.99, 192.321)), (' B1040  VAL HG21', ' C1035  GLY  HA3', -0.527, (171.172, 156.881, 100.511)), (' C 379  CYS  HA ', ' C 432  CYS  HA ', -0.525, (157.465, 194.29, 192.499)), (' D  99  ARG  HE ', ' D 115  ASP  HB3', -0.523, (142.399, 131.93, 234.021)), (' A1028  LYS  O  ', ' A1032  CYS  HB3', -0.521, (161.255, 174.822, 106.645)), (' A 379  CYS  HA ', ' A 432  CYS  HA ', -0.52, (140.945, 143.401, 192.616)), (' C1028  LYS  O  ', ' C1032  CYS  HB3', -0.515, (174.703, 160.78, 106.499)), (' B1028  LYS  O  ', ' B1032  CYS  HB3', -0.514, (155.733, 156.284, 106.581)), (' F  35  ASN  HB2', ' F 100  HIS  HB3', -0.512, (195.577, 166.907, 232.896)), (' C 332  ILE  HB ', ' C1304  NAG  H82', -0.51, (146.78, 209.832, 169.904)), (' B 332  ILE  HB ', ' B1304  NAG  H82', -0.507, (212.164, 155.612, 170.252)), (' B1107  ARG HH22', ' C 907  ASN HD22', -0.506, (173.841, 160.633, 85.637)), (' H  35  ASN  HB2', ' H 100  HIS  HB3', -0.502, (144.97, 190.303, 233.393)), (' A 328  ARG  NH2', ' A 531  THR  O  ', -0.502, (129.662, 137.944, 163.131)), (' F 102  SER  HB3', ' a   1  NAG  HN2', -0.5, (195.095, 169.322, 229.149)), (' A 332  ILE  HB ', ' A1304  NAG  H82', -0.499, (133.107, 126.199, 170.122)), (' D 102  SER  HB3', ' Z   1  NAG  HN2', -0.499, (152.468, 134.102, 229.233)), (' C 804  GLN  NE2', ' C 935  GLN  OE1', -0.499, (196.781, 165.514, 105.217)), (' L  38  GLN  O  ', ' L  46  LYS  N  ', -0.498, (158.565, 200.172, 233.655)), (' A 804  GLN  NE2', ' A 935  GLN  OE1', -0.498, (146.279, 191.134, 105.416)), (' B 804  GLN  NE2', ' B 935  GLN  OE1', -0.498, (149.262, 135.051, 105.488)), (' H 102  SER  HB3', ' Y   1  NAG  HN2', -0.491, (142.688, 189.248, 229.287)), (' E  38  GLN  O  ', ' E  46  LYS  N  ', -0.49, (135.434, 142.821, 233.506)), (' C 950  ASP  OD2', ' C 954  GLN  NE2', -0.488, (177.642, 169.424, 128.378)), (' A 963  VAL HG11', ' C 570  ALA  HB1', -0.486, (155.445, 184.42, 145.601)), (' D  35  ASN  HB2', ' D 100  HIS  HB3', -0.485, (149.945, 135.557, 233.166)), (' G  38  GLN  O  ', ' G  46  LYS  N  ', -0.481, (196.912, 150.767, 233.802)), (' A 805  ILE HG22', ' A 818  ILE HD12', -0.478, (152.589, 187.122, 107.044)), (' C 805  ILE HG22', ' C 818  ILE HD12', -0.477, (190.1, 162.202, 106.941)), (' B 417  LYS  NZ ', ' G  51  TYR  OH ', -0.476, (195.089, 166.216, 217.056)), (' B1011  GLN  OE1', ' B1014  ARG  NH1', -0.476, (156.955, 155.106, 134.267)), (' A1011  GLN  OE1', ' A1014  ARG  NH1', -0.474, (159.601, 174.757, 134.298)), (' C1011  GLN  OE1', ' C1014  ARG  NH1', -0.474, (175.088, 162.847, 134.277)), (' C 486  PHE  HZ ', ' Y   1  NAG  H5 ', -0.473, (139.252, 185.785, 231.567)), (' B 715  PRO  HB3', ' B1069  PRO  HB3', -0.471, (170.274, 145.072, 91.642)), (' C 715  PRO  HB3', ' C1069  PRO  HB3', -0.471, (177.381, 179.066, 91.802)), (' B 805  ILE HG22', ' B 818  ILE HD12', -0.469, (149.265, 142.762, 106.736)), (' A 790  LYS  HE2', ' C 704  SER  HB3', -0.469, (170.45, 196.612, 100.578)), (' A 570  ALA  HB1', ' B 963  VAL HG11', -0.468, (150.292, 146.912, 145.544)), (' A 715  PRO  HB3', ' A1069  PRO  HB3', -0.467, (144.227, 167.623, 91.382)), (' B 950  ASP  OD2', ' B 954  GLN  NE2', -0.467, (161.894, 149.459, 128.418)), (' C 486  PHE  CZ ', ' Y   1  NAG  H5 ', -0.466, (139.835, 186.129, 231.408)), (' F  39  ILE HD11', ' F 114  MET  HE1', -0.465, (191.569, 160.901, 234.881)), (' F 100  HIS  NE2', ' F 112  TYR  O  ', -0.46, (194.869, 163.421, 228.935)), (' A 950  ASP  OD2', ' A 954  GLN  NE2', -0.458, (152.446, 173.068, 128.363)), (' A 565  PHE  HD1', ' A 576  VAL HG12', -0.457, (142.82, 137.472, 156.272)), (' F  38  TRP  CE2', ' F  82  LEU  HB2', -0.456, (192.853, 164.35, 245.802)), (' H  39  ILE HD11', ' H 114  MET  HE1', -0.456, (152.396, 190.257, 235.049)), (' B 565  PHE  HD1', ' B 576  VAL HG12', -0.456, (197.387, 158.987, 155.996)), (' A 393  THR  HA ', ' A 522  ALA  HA ', -0.455, (151.239, 134.921, 178.782)), (' H 100  HIS  NE2', ' H 112  TYR  O  ', -0.455, (148.576, 191.603, 229.007)), (' C 328  ARG  NH2', ' C 531  THR  O  ', -0.455, (158.53, 206.548, 162.907)), (' D  38  TRP  CE2', ' D  82  LEU  HB2', -0.454, (149.063, 139.467, 245.893)), (' H  38  TRP  CE2', ' H  82  LEU  HB2', -0.453, (148.75, 189.487, 246.185)), (' C 565  PHE  HD1', ' C 576  VAL HG12', -0.453, (151.72, 195.936, 155.93)), (' A 907  ASN HD22', ' C1107  ARG HH22', -0.451, (161.806, 173.779, 85.921)), (' B 858  LEU HD21', ' B 962  LEU HD23', -0.451, (151.441, 153.56, 142.221)), (' A 858  LEU HD21', ' A 962  LEU HD23', -0.451, (161.025, 180.11, 142.294)), (' B 393  THR  HA ', ' B 522  ALA  HA ', -0.45, (195.728, 167.443, 179.145)), (' B 570  ALA  HB1', ' C 963  VAL HG11', -0.449, (185.941, 161.147, 145.689)), (' C 363  ALA  O  ', ' C 527  PRO  HD3', -0.448, (152.915, 200.391, 179.265)), (' A 363  ALA  O  ', ' A 527  PRO  HD3', -0.447, (138.134, 136.431, 179.308)), (' B 363  ALA  O  ', ' B 527  PRO  HD3', -0.445, (200.984, 155.4, 179.274)), (' B 328  ARG  NH2', ' B 531  THR  O  ', -0.443, (203.527, 147.538, 162.909)), (' C 393  THR  HA ', ' C 522  ALA  HA ', -0.443, (145.103, 189.708, 179.146)), (' A1073  LYS  HB2', ' A1075  PHE  CE2', -0.443, (139.665, 164.432, 84.081)), (' C 393  THR HG21', ' C 518  LEU  H  ', -0.443, (145.417, 185.549, 181.408)), (' D  39  ILE HD11', ' D 114  MET  HE1', -0.443, (146.868, 142.256, 234.825)), (' C 485  GLY  O  ', ' H 103  GLY  HA2', -0.443, (137.384, 192.452, 226.65)), (' C 902  MET  HE1', ' C1049  LEU HD13', -0.442, (181.27, 165.339, 94.684)), (' B 902  MET  HE1', ' B1049  LEU HD13', -0.442, (156.976, 148.473, 94.622)), (' B1073  LYS  HB2', ' B1075  PHE  CE2', -0.442, (175.712, 142.31, 84.267)), (' B 131  CYS  HB2', ' B 133  PHE  CE2', -0.441, (156.034, 115.488, 181.303)), (' B 611  LEU HD22', ' B 666  ILE HG23', -0.44, (181.457, 139.689, 130.824)), (' C1073  LYS  HB2', ' C1075  PHE  CE2', -0.44, (176.691, 184.781, 84.094)), (' C 131  CYS  HB2', ' C 133  PHE  CE2', -0.439, (209.649, 181.244, 181.642)), (' C 858  LEU HD21', ' C 962  LEU HD23', -0.437, (178.873, 158.374, 142.233)), (' A 502  GLY  O  ', ' A 506  GLN  HG3', -0.435, (129.119, 136.109, 211.685)), (' A 131  CYS  HB2', ' A 133  PHE  CE2', -0.435, (125.82, 195.213, 181.283)), (' B  44  ARG  O  ', ' B 283  GLY  HA2', -0.435, (148.812, 129.228, 146.784)), (' A 393  THR HG21', ' A 518  LEU  H  ', -0.435, (154.429, 137.314, 181.561)), (' B 455  LEU HD22', ' B 493  GLN  HG3', -0.435, (202.493, 164.563, 218.303)), (' E  50  TYR  O  ', ' E  54  LEU  HB2', -0.434, (141.593, 137.157, 221.589)), (' B 393  THR HG21', ' B 518  LEU  H  ', -0.434, (191.974, 169.189, 181.406)), (' A 908  GLY  O  ', ' A1038  LYS  HE3', -0.434, (160.104, 167.935, 93.977)), (' C 611  LEU HD22', ' C 666  ILE HG23', -0.434, (176.28, 191.16, 130.866)), (' C 455  LEU HD22', ' C 493  GLN  HG3', -0.433, (144.168, 197.509, 218.287)), (' A 904  TYR  OH ', ' C1094  VAL HG11', -0.433, (166.324, 179.269, 85.94)), (' B 981  LEU HD21', ' B 993  ILE HD11', -0.433, (148.765, 159.083, 162.9)), (' C 502  GLY  O  ', ' C 506  GLN  HG3', -0.433, (157.387, 208.099, 211.879)), (' A 704  SER  HB3', ' B 790  LYS  HE2', -0.432, (132.623, 153.324, 100.709)), (' L  50  TYR  O  ', ' L  54  LEU  HB2', -0.432, (150.635, 197.526, 221.55)), (' C 698  SER  O  ', ' C 699  LEU  HG ', -0.431, (172.764, 191.695, 114.473)), (' A 455  LEU HD22', ' A 493  GLN  HG3', -0.431, (144.942, 130.328, 218.294)), (' A 698  SER  O  ', ' A 699  LEU  HG ', -0.431, (135.27, 157.724, 114.262)), (' B 502  GLY  O  ', ' B 506  GLN  HG3', -0.429, (205.474, 147.784, 211.878)), (' A  44  ARG  O  ', ' A 283  GLY  HA2', -0.429, (141.749, 194.337, 146.652)), (' B 908  GLY  O  ', ' B1038  LYS  HE3', -0.428, (162.573, 158.296, 93.739)), (' O   1  NAG  H61', ' O   2  NAG  N2 ', -0.428, (169.94, 135.631, 177.487)), (' A 902  MET  HE1', ' A1049  LEU HD13', -0.428, (154.078, 178.205, 94.474)), (' A1089  PHE  HB2', ' A1121  PHE  CZ ', -0.428, (157.576, 153.382, 78.802)), (' C 981  LEU HD21', ' C 993  ILE HD11', -0.427, (176.272, 153.136, 163.136)), (' B1107  ARG HH22', ' C 907  ASN  ND2', -0.426, (173.634, 161.129, 85.711)), (' C 908  GLY  O  ', ' C1038  LYS  HE3', -0.426, (169.471, 165.321, 93.992)), (' B1145  LEU HD21', ' C1145  LEU HD12', -0.426, (166.191, 165.311, 56.583)), (' B1089  PHE  HB2', ' B1121  PHE  CZ ', -0.425, (176.012, 164.01, 78.889)), (' F  92  THR HG23', ' F 124  THR  HA ', -0.425, (184.701, 152.387, 251.218)), (' G  50  TYR  O  ', ' G  54  LEU  HB2', -0.425, (198.886, 158.658, 221.33)), (' B 598  ILE HG23', ' B 664  ILE HG21', -0.424, (175.869, 135.584, 128.501)), (' H  36  TRP  HB3', ' H  80  LEU HD13', -0.424, (144.222, 192.381, 241.288)), (' I   1  NAG  H61', ' I   2  NAG  N2 ', -0.424, (136.332, 173.559, 177.26)), (' T   1  NAG  H61', ' T   2  NAG  N2 ', -0.423, (185.577, 183.403, 177.505)), (' A 656  VAL HG12', ' A 658  ASN  H  ', -0.423, (122.784, 160.372, 118.351)), (' A 598  ILE HG23', ' A 664  ILE HG21', -0.423, (133.087, 167.753, 128.715)), (' D 110  TYR  CZ ', ' E  56  PRO  HB3', -0.423, (136.876, 133.516, 226.668)), (' A 611  LEU HD22', ' A 666  ILE HG23', -0.423, (134.133, 161.146, 130.849)), (' C  44  ARG  O  ', ' C 283  GLY  HA2', -0.423, (201.637, 168.403, 146.935)), (' C 392  PHE  CD1', ' C 515  PHE  HB3', -0.423, (150.984, 190.669, 184.616)), (' C 102  ARG  HD2', ' C 141  LEU HD23', -0.421, (220.657, 187.293, 171.381)), (' G  81  SER  OG ', ' G 112  GLN  OE1', -0.421, (198.168, 132.75, 228.75)), (' B1028  LYS  O  ', ' B1032  CYS  HB2', -0.421, (156.792, 156.905, 106.609)), (' B 102  ARG  HD2', ' B 141  LEU HD23', -0.421, (155.744, 103.439, 171.323)), (' C 770  ILE  O  ', ' C 774  GLN  HG2', -0.42, (173.951, 154.002, 128.446)), (' A1028  LYS  O  ', ' A1032  CYS  HB2', -0.42, (161.379, 173.828, 106.602)), (' F  36  TRP  HB3', ' F  80  LEU HD13', -0.42, (197.219, 166.957, 241.567)), (' B 392  PHE  CD1', ' B 515  PHE  HB3', -0.42, (193.391, 161.954, 184.21)), (' A1072  GLU  HG2', ' B 894  LEU  CD2', -0.419, (141.252, 164.463, 92.078)), (' D  16  GLN  HG3', ' D  17  THR  H  ', -0.419, (153.654, 146.506, 258.226)), (' B 656  VAL HG12', ' B 658  ASN  H  ', -0.419, (187.781, 130.121, 118.366)), (' C1028  LYS  O  ', ' C1032  CYS  HB2', -0.418, (173.824, 161.396, 106.717)), (' A 981  LEU HD21', ' A 993  ILE HD11', -0.418, (167.395, 180.213, 162.917)), (' B 698  SER  O  ', ' B 699  LEU  HG ', -0.418, (183.708, 142.291, 114.169)), (' A 392  PHE  CD1', ' A 515  PHE  HB3', -0.418, (147.464, 139.826, 184.323)), (' C 656  VAL HG12', ' C 658  ASN  H  ', -0.417, (181.413, 201.485, 118.424)), (' A 102  ARG  HD2', ' A 141  LEU HD23', -0.417, (115.579, 201.456, 170.825)), (' B 770  ILE  O  ', ' B 774  GLN  HG2', -0.417, (150.371, 160.804, 128.59)), (' C 598  ILE HG23', ' C 664  ILE HG21', -0.416, (182.638, 188.573, 128.477)), (' B 697  MET  HE3', ' B 699  LEU HD21', -0.416, (181.904, 144.316, 117.149)), (' A 230  PRO  HB2', ' C 521  PRO  HB2', -0.416, (141.299, 189.429, 174.565)), (' A1094  VAL HG11', ' B 904  TYR  OH ', -0.416, (149.617, 158.177, 86.4)), (' C1089  PHE  HB2', ' C1121  PHE  CZ ', -0.416, (157.957, 174.448, 78.83)), (' F  55  ASN  HB3', ' F  56  SER  H  ', -0.415, (197.293, 178.77, 237.788)), (' A 770  ILE  O  ', ' A 774  GLN  HG2', -0.413, (168.052, 177.494, 128.508)), (' D  36  TRP  HB3', ' D  80  LEU HD13', -0.413, (149.083, 134.354, 241.31)), (' F  40  ARG  HB3', ' F  50  ILE HD11', -0.412, (187.438, 159.606, 243.498)), (' C 403  ARG HH22', ' L  53  ASP  HB2', -0.412, (153.993, 197.652, 215.355)), (' A 440  ASN  N  ', ' A 440  ASN  OD1', -0.411, (126.173, 129.944, 204.143)), (' D  92  THR HG23', ' D 124  THR  HA ', -0.41, (142.941, 152.868, 251.036)), (' B 105  ILE HD11', ' B 241  LEU HD21', -0.41, (162.041, 110.014, 175.239)), (' H  16  GLN  HG3', ' H  17  THR  H  ', -0.409, (152.374, 182.822, 258.905)), (' H  92  THR HG23', ' H 124  THR  HA ', -0.408, (163.151, 188.972, 251.472)), (' L 112  GLN  HA ', ' L 113  PRO  HD3', -0.407, (177.865, 210.492, 229.323)), (' B 376  THR  HB ', ' B 435  ALA  HB3', -0.406, (199.511, 150.956, 200.07)), (' H  40  ARG  HB3', ' H  50  ILE HD11', -0.406, (155.844, 187.667, 243.932)), (' C 493  GLN HE21', ' H 111  TYR  HE2', -0.406, (142.83, 199.104, 220.583)), (' H   4  LEU HD23', ' H  22  CYS  SG ', -0.406, (147.309, 197.076, 242.645)), (' D  37  THR  OG1', ' D  51  GLY  O  ', -0.403, (150.721, 140.532, 238.163)), (' A 718  PHE  HE1', ' A 923  ILE HG12', -0.403, (148.163, 178.135, 91.019)), (' B1086  LYS  HD2', ' B1122  VAL HG11', -0.402, (178.559, 166.278, 69.398)), (' D  61  TYR  HB2', ' D  66  LYS  HG3', -0.402, (159.681, 143.744, 241.056)), (' A 429  PHE  HE1', ' A 514  SER  HB3', -0.402, (147.431, 138.008, 192.96)), (' C 376  THR  HB ', ' C 435  ALA  HB3', -0.402, (157.134, 201.472, 200.062)), (' C 697  MET  HE3', ' C 699  LEU HD21', -0.401, (172.179, 189.459, 117.198)), (' C 127  VAL HG21', ' C1302  NAG  H5 ', -0.401, (218.698, 178.51, 176.283)), (' H 119  GLN  HB3', ' H 119  GLN HE21', -0.4, (153.394, 202.417, 244.13)), (' F  11  LEU HD23', ' F 124  THR  HB ', -0.4, (186.877, 151.657, 255.387)), (' F  16  GLN  HG3', ' F  17  THR  H  ', -0.4, (184.543, 164.519, 258.053))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
