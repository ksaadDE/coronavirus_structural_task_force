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
data['rama'] = [('A', ' 743 ', 'CYS', 0.03752875590653617, (193.548, 192.06500000000003, 222.671)), ('A', '1036 ', 'GLN', 0.013788187495414777, (196.24299999999997, 202.71100000000007, 276.937)), ('C', ' 337 ', 'PRO', 0.013950500751508001, (230.098, 184.378, 194.942))]
data['omega'] = [('H', ' 162 ', 'PRO', None, (205.988, 234.05500000000006, 122.008)), ('H', ' 164 ', 'PRO', None, (202.20900000000006, 234.443, 127.225)), ('I', ' 162 ', 'PRO', None, (132.0819999999999, 144.40000000000003, 141.015)), ('I', ' 164 ', 'PRO', None, (135.89899999999992, 144.10200000000006, 146.222)), ('J', ' 162 ', 'PRO', None, (170.534, 210.56, 157.181)), ('J', ' 164 ', 'PRO', None, (176.056, 212.926, 159.681)), ('L', '   8 ', 'PRO', None, (204.42799999999997, 215.65100000000004, 152.18)), ('L', ' 115 ', 'PRO', None, (225.474, 228.202, 147.637)), ('L', ' 161 ', 'PRO', None, (189.996, 214.555, 142.871)), ('M', '   8 ', 'PRO', None, (162.406, 160.093, 150.12)), ('M', ' 115 ', 'PRO', None, (144.35099999999994, 175.03800000000004, 145.779)), ('M', ' 161 ', 'PRO', None, (163.747, 142.43600000000004, 148.303)), ('N', '   8 ', 'PRO', None, (185.13199999999998, 211.006, 189.381)), ('N', ' 115 ', 'PRO', None, (180.719, 189.24, 178.052)), ('N', ' 161 ', 'PRO', None, (179.627, 227.905, 183.34299999999996))]
data['rota'] = [('A', ' 657 ', 'ASN', 0.2954284164177642, (185.4850000000001, 242.88800000000003, 257.849)), ('B', '  17 ', 'ASN', 0.0035058940982652972, (209.425, 145.112, 198.64899999999997)), ('B', '  50 ', 'SER', 0.054092495640652605, (214.346, 178.356, 229.564)), ('B', '  51 ', 'THR', 0.0013599335943581536, (213.92, 177.997, 225.75499999999997)), ('B', ' 331 ', 'ASN', 0.012490947443148697, (163.461, 189.696, 210.171)), ('B', ' 657 ', 'ASN', 0.0, (184.99900000000005, 169.798, 256.464)), ('B', ' 709 ', 'ASN', 0.0, (185.087, 188.52100000000004, 290.16599999999994)), ('B', '1133 ', 'VAL', 0.0013269110689032736, (188.08199999999994, 192.54500000000007, 303.08)), ('C', ' 234 ', 'ASN', 0.001487691030378153, (234.473, 229.362, 204.375)), ('C', ' 331 ', 'ASN', 0.00015523687388281258, (240.543, 184.117, 205.13199999999998)), ('C', ' 657 ', 'ASN', 0.007099686411792323, (248.303, 205.045, 257.877)), ('C', ' 709 ', 'ASN', 0.0032340889095517464, (230.049, 196.0960000000001, 290.66099999999994)), ('C', '1100 ', 'THR', 0.0798547487116633, (230.161, 207.3100000000001, 307.354)), ('C', '1103 ', 'PHE', 0.11831542909435222, (221.615, 207.76200000000006, 302.02099999999996)), ('C', '1114 ', 'ILE', 0.1343252420097341, (219.143, 209.5540000000001, 305.407)), ('M', ' 136 ', 'PHE', 0.006215756842820627, (158.25599999999997, 130.00500000000005, 136.563))]
data['cbeta'] = [('A', ' 165 ', 'ASN', ' ', 0.28263497769944973, (163.09199999999998, 213.406, 190.838)), ('A', ' 282 ', 'ASN', ' ', 0.2608226472454187, (162.05700000000004, 201.49700000000004, 233.892)), ('B', ' 331 ', 'ASN', ' ', 0.3829129063488849, (162.481, 188.583, 210.561))]
data['probe'] = [(' B 657  ASN  N  ', ' B 657  ASN  OD1', -0.663, (185.037, 168.513, 255.2)), (' C1097  SER  HB2', ' C1102  TRP  CE2', -0.596, (226.953, 202.984, 301.837)), (' A 811  LYS  NZ ', ' A 820  ASP  OD2', -0.568, (172.829, 193.797, 261.386)), (' M 136  PHE  C  ', ' M 136  PHE  CD1', -0.563, (156.283, 130.156, 135.597)), (' B 318  PHE  CE1', ' B 595  VAL HG11', -0.539, (196.058, 177.923, 233.305)), (' M 169  LYS  NZ ', ' M 215  GLU  OE1', -0.536, (167.921, 140.484, 129.646)), (' A 964  LYS  NZ ', ' B 571  ASP  OD2', -0.521, (182.514, 205.144, 230.173)), (' A 581  THR HG22', ' E   1  NAG  H3 ', -0.521, (211.02, 255.232, 215.416)), (' B 708  SER  HB2', ' S   1  NAG  H82', -0.511, (183.745, 184.466, 289.985)), (' J 221  LYS  NZ ', ' J 223  ASP  OD2', -0.509, (171.736, 226.895, 147.732)), (' H 109  TYR  CG ', ' H 110  TYR  N  ', -0.504, (224.723, 238.951, 156.14)), (' N 133  PRO  HB3', ' N 159  PHE  CD2', -0.501, (174.154, 231.233, 177.911)), (' C 234  ASN  N  ', ' C 234  ASN  OD1', -0.495, (233.156, 229.091, 202.996)), (' A 733  LYS  NZ ', ' A 775  ASP  OD1', -0.494, (195.295, 190.149, 249.463)), (' A 571  ASP  OD2', ' C 964  LYS  NZ ', -0.493, (217.012, 227.952, 230.415)), (' B1081  ILE  CG2', ' B1135  ASN  HB3', -0.486, (192.651, 194.015, 305.195)), (' B 326  ILE HD11', ' B 534  VAL  H  ', -0.486, (172.811, 180.213, 221.195)), (' B  50  SER  HA ', ' B 275  PHE  O  ', -0.484, (214.198, 176.38, 229.006)), (' A  28  TYR  HB3', ' A  61  ASN  HB3', -0.476, (164.667, 233.728, 224.789)), (' A 897  PRO  HB3', ' B 709  ASN  HA ', -0.473, (185.495, 189.594, 288.54)), (' C 281  GLU  HB3', ' C1303  NAG  H82', -0.472, (222.662, 244.679, 238.487)), (' A 789  TYR  H  ', ' A 876  ALA  HB1', -0.472, (190.857, 186.16, 269.956)), (' A 709  ASN  N  ', ' A 709  ASN  OD1', -0.469, (202.091, 233.151, 290.579)), (' A 310  LYS  NZ ', ' A 663  ASP  OD1', -0.463, (179.976, 224.507, 255.839)), (' C 557  LYS  NZ ', ' C 586  ASP  OD1', -0.462, (235.812, 182.379, 230.33)), (' A  17  ASN  O  ', ' A  17  ASN  OD1', -0.459, (147.685, 235.135, 199.76)), (' B 164  ASN  HB3', ' P   1  NAG  H82', -0.458, (215.23, 164.127, 187.763)), (' M 136  PHE  C  ', ' M 136  PHE  HD1', -0.457, (156.613, 130.581, 135.343)), (' B 129  LYS  NZ ', ' B 169  GLU  OE2', -0.455, (224.737, 164.34, 194.632)), (' A  64  TRP  HE1', ' A 264  ALA  HB1', -0.452, (152.295, 228.749, 221.59)), (' C1097  SER  HA ', ' C1101  HIS  O  ', -0.449, (226.793, 206.416, 302.736)), (' B 526  GLY  N  ', ' B 527  PRO  HD2', -0.448, (168.866, 190.09, 202.958)), (' B 526  GLY  N  ', ' B 527  PRO  CD ', -0.447, (168.703, 190.594, 203.05)), (' L 169  LYS  NZ ', ' L 215  GLU  OE1', -0.443, (193.634, 199.943, 130.181)), (' C 790  LYS  NZ ', ' C 872  GLN  OE1', -0.443, (196.87, 235.16, 267.051)), (' N 169  LYS  NZ ', ' N 215  GLU  OE1', -0.442, (160.797, 231.323, 187.966)), (' A 489  TYR  CE2', ' A 491  PRO  HA ', -0.439, (226.554, 236.804, 164.067)), (' L  24  ARG  NH1', ' L  86  ASP  OD1', -0.433, (213.419, 214.22, 158.895)), (' B1082  CYS  O  ', ' B1134  ASN  HA ', -0.43, (188.973, 195.622, 306.869)), (' B 989  ALA  O  ', ' B 993  ILE HG12', -0.43, (219.604, 204.712, 214.68)), (' B1043  CYS  H  ', ' B1048  HIS  CE1', -0.43, (208.878, 195.455, 271.717)), (' C1096  VAL  O  ', ' C1102  TRP  HA ', -0.429, (224.788, 205.792, 301.998)), (' B 173  GLN  HB2', ' B 174  PRO  HD2', -0.429, (232.282, 160.995, 212.792)), (' C 580  GLN  HG2', ' C1304  NAG  HN2', -0.429, (241.82, 181.51, 209.755)), (' C1097  SER  HB2', ' C1102  TRP  CD2', -0.428, (226.427, 203.06, 302.34)), (' C1102  TRP  CZ2', ' C1133  VAL HG21', -0.426, (225.747, 199.903, 302.212)), (' B  53  ASP  OD2', ' B 195  LYS  NZ ', -0.421, (215.43, 172.865, 218.75)), (' B1081  ILE HG23', ' B1135  ASN  HB3', -0.421, (192.416, 193.895, 305.19)), (' I 216  LYS  N  ', ' I 217  PRO  CD ', -0.421, (131.084, 139.644, 146.285)), (' A 324  GLU  HB2', ' A 539  VAL HG22', -0.42, (197.401, 243.359, 220.988)), (' B  18  LEU  O  ', ' B  19  THR  C  ', -0.419, (206.21, 142.563, 203.283)), (' A 104  TRP  HB3', ' A 106  PHE  CE1', -0.418, (158.993, 220.373, 209.631)), (' B  38  TYR  CE1', ' B 285  ILE  HB ', -0.411, (222.51, 170.152, 226.96)), (' J  71  VAL  HB ', ' J  76  PHE  CD1', -0.411, (175.832, 190.988, 167.209)), (' J 216  LYS  N  ', ' J 217  PRO  CD ', -0.41, (175.267, 214.428, 153.286)), (' B 456  PHE  CD1', ' B 489  TYR  CE2', -0.407, (147.303, 180.705, 163.57)), (' C 773  GLU  OE1', ' C1019  ARG  NH1', -0.403, (199.75, 213.398, 248.702)), (' J  52  TRP  CZ3', ' N 114  TYR  HB2', -0.401, (182.608, 188.981, 174.904)), (' H  65  THR  HG1', ' H  67  TYR  HE1', -0.401, (229.378, 237.598, 141.654)), (' C 709  ASN  N  ', ' C 709  ASN  OD1', -0.4, (230.888, 195.119, 288.905))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
