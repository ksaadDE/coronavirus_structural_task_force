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
data['omega'] = [('B', '   8 ', 'PRO', None, (171.36000000000007, 181.652, 185.384)), ('B', '  95 ', 'PRO', None, (185.248, 190.724, 204.022)), ('E', '   8 ', 'PRO', None, (267.612, 194.393, 185.384)), ('E', '  95 ', 'PRO', None, (252.811, 201.884, 204.022)), ('I', '   8 ', 'PRO', None, (182.085, 215.843, 153.281)), ('J', '   8 ', 'PRO', None, (232.639, 186.586, 153.281)), ('L', '   8 ', 'PRO', None, (208.45200000000014, 271.379, 185.384)), ('L', '  95 ', 'PRO', None, (209.36500000000018, 254.81600000000003, 204.022)), ('O', '   8 ', 'PRO', None, (232.70000000000016, 244.99500000000003, 153.281))]
data['rota'] = []
data['cbeta'] = [('A', ' 480 ', 'CYS', ' ', 0.32291203776758737, (208.33900000000014, 256.214, 183.158)), ('A', ' 481 ', 'ASN', ' ', 0.33470429702400184, (206.48500000000016, 260.934, 180.968)), ('A', ' 985 ', 'CYS', ' ', 0.26672880700419144, (229.5840000000001, 205.91, 206.487)), ('A', '1082 ', 'CYS', ' ', 0.29484342684570053, (194.135, 217.82400000000013, 308.678)), ('D', ' 480 ', 'CYS', ' ', 0.323046335152793, (184.55, 189.137, 183.158)), ('D', ' 481 ', 'ASN', ' ', 0.3346579994289902, (181.389, 185.171, 180.968)), ('D', ' 985 ', 'CYS', ' ', 0.26713729232873007, (217.49200000000013, 232.68700000000004, 206.487)), ('D', '1082 ', 'CYS', ' ', 0.29401937529554256, (224.89900000000006, 196.03100000000015, 308.678)), ('K', ' 480 ', 'CYS', ' ', 0.3229372721545901, (254.535, 202.07299999999998, 183.158)), ('K', ' 481 ', 'ASN', ' ', 0.33427492127488917, (259.55, 201.319, 180.968)), ('K', ' 985 ', 'CYS', ' ', 0.2671365229151057, (200.34800000000007, 208.827, 206.487)), ('K', '1082 ', 'CYS', ' ', 0.29474755557730736, (228.39000000000013, 233.5690000000001, 308.678))]
data['probe'] = [(' A 985  CYS  SG ', ' D 383  CYS  SG ', -1.086, (229.965, 204.537, 204.22)), (' A 383  CYS  SG ', ' K 985  CYS  SG ', -1.019, (199.289, 209.363, 204.347)), (' D 985  CYS  SG ', ' K 383  CYS  SG ', -1.002, (219.849, 234.253, 204.397)), (' M  24  ALA  HB1', ' M  27  PHE  CZ ', -0.533, (197.174, 268.143, 218.315)), (' F  24  ALA  HB1', ' F  27  PHE  CZ ', -0.533, (270.207, 205.907, 217.848)), (' C  24  ALA  HB1', ' C  27  PHE  CZ ', -0.532, (179.869, 173.502, 217.829)), (' A 363  ALA  O  ', ' A 527  PRO  HD3', -0.51, (185.044, 213.54, 200.33)), (' D 363  ALA  O  ', ' D 527  PRO  HD3', -0.507, (233.415, 190.038, 200.18)), (' K 363  ALA  O  ', ' K 527  PRO  HD3', -0.501, (229.207, 243.757, 200.185)), (' A1142  GLN  N  ', ' A1143  PRO  HD2', -0.501, (209.24, 211.204, 319.542)), (' K1142  GLN  N  ', ' K1143  PRO  HD2', -0.497, (214.579, 223.795, 319.777)), (' A 363  ALA  O  ', ' A 526  GLY  HA2', -0.493, (184.59, 215.052, 200.858)), (' D1142  GLN  N  ', ' D1143  PRO  HD2', -0.493, (223.429, 212.739, 319.782)), (' D  32  PHE  HA ', ' D  59  PHE  CD1', -0.489, (262.248, 222.121, 233.295)), (' K  64  TRP  HE1', ' K 264  ALA  HB1', -0.484, (176.69, 261.45, 222.562)), (' D 363  ALA  O  ', ' D 526  GLY  HA2', -0.483, (232.168, 189.366, 200.425)), (' A  32  PHE  HA ', ' A  59  PHE  CD1', -0.482, (197.55, 172.339, 233.686)), (' K 363  ALA  O  ', ' K 526  GLY  HA2', -0.48, (230.572, 243.277, 200.425)), (' D  44  ARG  O  ', ' D 283  GLY  HA2', -0.48, (245.021, 238.612, 230.345)), (' A  64  TRP  HE1', ' A 264  ALA  HB1', -0.48, (195.594, 159.231, 222.924)), (' K  44  ARG  O  ', ' K 283  GLY  HA2', -0.477, (181.438, 229.679, 230.359)), (' D  64  TRP  HE1', ' D 264  ALA  HB1', -0.474, (274.981, 226.722, 223.042)), (' A  44  ARG  O  ', ' A 283  GLY  HA2', -0.473, (221.026, 179.454, 230.092)), (' K  32  PHE  HA ', ' K  59  PHE  CD1', -0.473, (187.373, 253.146, 233.67)), (' A 898  PHE  N  ', ' A 899  PRO  CD ', -0.469, (227.629, 195.912, 289.653)), (' K 898  PHE  N  ', ' K 899  PRO  CD ', -0.46, (192.606, 215.456, 289.755)), (' D 898  PHE  N  ', ' D 899  PRO  CD ', -0.458, (227.147, 236.122, 289.684)), (' K 431  GLY  HA2', ' K 515  PHE  CD2', -0.453, (231.281, 231.007, 201.998)), (' A 431  GLY  HA2', ' A 515  PHE  CD2', -0.453, (194.503, 221.334, 201.969)), (' D 431  GLY  HA2', ' D 515  PHE  CD2', -0.449, (221.543, 194.464, 201.946)), (' K 331  ASN  O  ', ' K 331  ASN  OD1', -0.447, (240.192, 252.21, 205.893)), (' A 331  ASN  O  ', ' A 331  ASN  OD1', -0.444, (172.173, 218.866, 205.893)), (' K 579  PRO  O  ', ' K1301  NAG  H82', -0.442, (239.911, 249.598, 210.758)), (' A 714  ILE  HA ', ' A 715  PRO  HD3', -0.44, (201.08, 202.629, 291.123)), (' K 714  ILE  HA ', ' K 715  PRO  HD3', -0.44, (211.769, 235.182, 291.105)), (' I  59  ILE  HA ', ' I  60  PRO  HD3', -0.439, (181.935, 203.889, 171.548)), (' K 898  PHE  HB3', ' K 899  PRO  HD3', -0.438, (191.85, 216.404, 288.873)), (' A 898  PHE  HB3', ' A 899  PRO  HD3', -0.435, (227.225, 194.683, 288.854)), (' D 898  PHE  HB3', ' D 899  PRO  HD3', -0.434, (228.222, 236.399, 288.873)), (' A 579  PRO  O  ', ' A1301  NAG  H82', -0.433, (174.408, 219.387, 210.968)), (' D 792  PRO  HA ', ' D 793  PRO  HD3', -0.432, (224.142, 247.898, 282.727)), (' D 579  PRO  O  ', ' D1301  NAG  H82', -0.432, (233.298, 178.264, 211.029)), (' D 331  ASN  O  ', ' D 331  ASN  OD1', -0.431, (234.931, 176.413, 205.841)), (' K 620  VAL  HB ', ' K 621  PRO  HD3', -0.43, (213.668, 255.824, 237.54)), (' K 755  GLN  HB2', ' K 755  GLN HE21', -0.429, (211.346, 204.967, 221.916)), (' D 294  ASP  HB2', ' D 295  PRO  HD2', -0.428, (253.783, 212.755, 238.614)), (' L  58  VAL  HA ', ' L  59  PRO  HD3', -0.428, (190.756, 276.156, 197.597)), (' D 388  ASN  O  ', ' D 527  PRO  HD2', -0.425, (234.533, 191.958, 202.265)), (' A 620  VAL  HB ', ' A 621  PRO  HD3', -0.422, (182.44, 194.227, 237.83)), (' A 388  ASN  O  ', ' A 527  PRO  HD2', -0.421, (186.182, 211.717, 202.543)), (' K 294  ASP  HB2', ' K 295  PRO  HD2', -0.42, (199.048, 250.198, 238.501)), (' D 755  GLN  HB2', ' D 755  GLN HE21', -0.417, (208.677, 225.519, 221.936)), (' M   6  GLU  N  ', ' M   6  GLU  OE1', -0.417, (204.896, 273.693, 216.818)), (' K 862  PRO  HA ', ' K 863  PRO  HD3', -0.417, (191.99, 208.866, 250.628)), (' I  44  ALA  HA ', ' I  45  PRO  HD3', -0.416, (168.422, 211.854, 168.816)), (' K 388  ASN  O  ', ' K 527  PRO  HD2', -0.415, (227.233, 243.628, 202.652)), (' D 620  VAL  HB ', ' D 621  PRO  HD3', -0.414, (251.193, 197.722, 237.83)), (' A 294  ASP  HB2', ' A 295  PRO  HD2', -0.413, (194.111, 184.386, 238.699)), (' M  97  ALA  HB2', ' M 112  TRP  CE3', -0.412, (203.057, 269.393, 208.848)), (' E  43  ALA  HA ', ' E  44  PRO  HD3', -0.411, (272.472, 195.715, 206.01)), (' B  58  VAL  HA ', ' B  59  PRO  HD3', -0.409, (176.059, 164.036, 197.447)), (' C  97  ALA  HB2', ' C 112  TRP  CE3', -0.407, (175.826, 177.95, 208.814)), (' A1081  ILE HG12', ' A1095  PHE  CE2', -0.405, (199.283, 213.45, 303.865)), (' B  43  ALA  HA ', ' B  44  PRO  HD3', -0.405, (170.061, 176.79, 206.005)), (' D 986  PRO  N  ', ' D 987  PRO  HD2', -0.405, (215.395, 231.368, 208.099)), (' F  97  ALA  HB2', ' F 112  TRP  CE3', -0.404, (268.477, 200.079, 208.792)), (' K1081  ILE HG12', ' K1095  PHE  CE2', -0.403, (222.02, 231.695, 304.054)), (' D1081  ILE HG12', ' D1095  PHE  CE2', -0.402, (226.206, 202.788, 303.883)), (' C   6  GLU  N  ', ' C   6  GLU  OE1', -0.4, (170.842, 177.749, 216.66))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
