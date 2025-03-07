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
data['rama'] = [('A', ' 154 ', 'TYR', 0.03788712922490455, (-4.608999999999998, -20.789999999999996, 15.536000000000001)), ('B', '  49 ', 'MET', 0.005876607103727264, (23.715, -17.151, -7.127000000000001))]
data['omega'] = []
data['rota'] = [('A', ' 235 ', 'MET', 0.00893179933090154, (6.106999999999997, -1.501, 45.20300000000001)), ('B', '  50 ', 'LEU', 0.005120752034261082, (24.287, -13.953, -5.1370000000000005)), ('B', '  51 ', 'ASN', 0.055866856339396254, (23.848, -11.442, -8.071000000000002)), ('B', ' 270 ', 'GLU', 0.14805438675747068, (10.710999999999993, 24.014, 22.913000000000004))]
data['cbeta'] = [('A', ' 128 ', 'CYS', ' ', 0.34259478421222694, (-6.054999999999996, -3.612, 25.075)), ('B', '  54 ', 'TYR', ' ', 0.2987267053437622, (15.123999999999993, -12.306, -11.380000000000004))]
data['probe'] = [(' B 298  ARG HH11', ' B 401  DMS  H13', -0.881, (-6.997, 5.793, 10.471)), (' B 263  ASP  OD1', ' B 501  HOH  O  ', -0.872, (2.64, 27.775, 20.399)), (' B 102  LYS  NZ ', ' B 156  CYS  SG ', -0.807, (-8.918, 1.539, -4.017)), (' A  56  ASP  OD1', ' A 501  HOH  O  ', -0.793, (-40.759, -4.401, 36.943)), (' B 192  GLN  N  ', ' B 502  HOH  O  ', -0.724, (23.851, -5.438, 2.128)), (' A 216  ASP  OD2', ' A 503  HOH  O  ', -0.714, (17.648, -2.029, 22.276)), (' B  54  TYR  CB ', ' B  82  MET  HE1', -0.701, (14.019, -11.522, -12.407)), (' B 145  CYS  SG ', ' B 583  HOH  O  ', -0.697, (10.548, -14.142, 3.312)), (' B 403  DMS  O  ', ' B 503  HOH  O  ', -0.692, (-10.566, 1.153, -8.235)), (' B  92  ASP  OD1', ' B 504  HOH  O  ', -0.682, (-6.418, -22.837, -10.122)), (' B  22  CYS  SG ', ' B 511  HOH  O  ', -0.682, (10.854, -21.177, -7.924)), (' A  34  ASP  OD2', ' A 505  HOH  O  ', -0.657, (-31.52, -19.482, 16.224)), (' A  41  HIS  CD2', ' A 406  DMS  H22', -0.657, (-23.677, 1.152, 29.03)), (' B  54  TYR  HB3', ' B  82  MET  HE1', -0.642, (13.767, -12.13, -11.593)), (' B  61  LYS  NZ ', ' B 511  HOH  O  ', -0.642, (11.473, -20.347, -8.153)), (' B 138  GLY  H  ', ' B 172  HIS  HD2', -0.633, (10.147, -3.217, 10.22)), (' A  86  VAL HG13', ' A 179  GLY  HA2', -0.629, (-21.801, -9.297, 29.193)), (' B 298  ARG  HD2', ' B 401  DMS  H13', -0.628, (-7.366, 6.461, 10.39)), (' B 401  DMS  H11', ' B 557  HOH  O  ', -0.614, (-5.342, 6.821, 13.186)), (' B  86  VAL HG23', ' B 179  GLY  HA2', -0.611, (7.582, -6.133, -6.902)), (' B  60  ARG  O  ', ' B 505  HOH  O  ', -0.594, (12.858, -25.402, -15.048)), (' B  12  LYS  NZ ', ' B 513  HOH  O  ', -0.585, (-15.198, -6.182, 3.969)), (' B  54  TYR  HB2', ' B  82  MET  HE1', -0.584, (14.601, -11.108, -11.782)), (' B  75  LEU  O  ', ' B 506  HOH  O  ', -0.558, (-0.89, -24.556, -7.399)), (' B 257  THR  HA ', ' B 406  DMS  H12', -0.553, (-8.685, 21.786, 19.494)), (' A 145  CYS  SG ', ' A 638  HOH  O  ', -0.549, (-21.084, 2.642, 23.23)), (' A 187  ASP  HB2', ' A 406  DMS  H23', -0.545, (-24.101, 0.189, 31.777)), (' A 273  GLN  NE2', ' A 502  HOH  O  ', -0.545, (19.86, 1.434, 43.673)), (' A  80  HIS  NE2', ' A 513  HOH  O  ', -0.54, (-38.886, -9.901, 26.715)), (' B 300  CYS  O  ', ' B 507  HOH  O  ', -0.538, (-12.084, 13.07, 17.977)), (' B  40  ARG  HD3', ' B  85  CYS  HA ', -0.527, (12.098, -8.599, -9.161)), (' B  40  ARG  HD2', ' B  82  MET  HE3', -0.526, (13.04, -10.462, -10.49)), (' B 298  ARG  HD3', ' B 305  PHE  HZ ', -0.522, (-10.094, 4.989, 8.177)), (' A 233  VAL HG11', ' A 269  LYS  HG3', -0.518, (14.424, -1.608, 42.737)), (' B  73  VAL HG11', ' B 405  DMS  H12', -0.517, (-9.291, -23.101, -3.494)), (' B 207  TRP  NE1', ' B 288  GLU  HG3', -0.505, (2.52, 9.575, 20.027)), (' A  27  LEU HD13', ' A  39  PRO  HD2', -0.504, (-24.143, -2.78, 22.572)), (' B 406  DMS  H21', ' B 560  HOH  O  ', -0.501, (-7.996, 20.04, 24.894)), (' B  51  ASN  N  ', ' B  52  PRO  HD3', -0.497, (22.438, -12.227, -7.046)), (' A 273  GLN  HG2', ' A 274  ASN  OD1', -0.495, (19.57, 4.592, 39.083)), (' B 190  THR  O  ', ' B 502  HOH  O  ', -0.494, (23.917, -5.888, 2.131)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.494, (-1.066, -6.656, 32.324)), (' B 222  ARG  NH2', ' B 517  HOH  O  ', -0.492, (0.202, 35.237, 29.198)), (' A  40  ARG  O  ', ' A  43  ILE HG12', -0.49, (-30.148, -2.583, 27.962)), (' A 401  DMS  H23', ' B 118  TYR  HE2', -0.49, (4.267, -12.931, 11.77)), (' B 163  HIS  CE1', ' B 172  HIS  HB3', -0.486, (11.114, -6.122, 5.932)), (' A 100  LYS  HB3', ' A 100  LYS  HE3', -0.485, (-12.7, -22.836, 17.705)), (' A  56  ASP  O  ', ' A  59  ILE HG22', -0.481, (-39.598, -4.538, 32.511)), (' B  57  LEU  N  ', ' B  57  LEU HD23', -0.479, (17.956, -18.003, -14.133)), (' B  95  ASN  HB3', ' B  98  THR  OG1', -0.479, (-9.412, -12.702, -5.703)), (' B 100  LYS  HE2', ' B 403  DMS  S  ', -0.478, (-13.576, 0.383, -6.716)), (' A 102  LYS  NZ ', ' A 156  CYS  SG ', -0.473, (-10.372, -20.628, 20.912)), (' B  56  ASP  O  ', ' B  59  ILE HG22', -0.473, (15.681, -18.197, -17.106)), (' B 276  MET  HE3', ' B 285  ALA  O  ', -0.47, (9.853, 11.708, 25.196)), (' A 263  ASP  OD1', ' A 506  HOH  O  ', -0.467, (21.109, -8.846, 36.216)), (' B 109  GLY  HA2', ' B 200  ILE HD13', -0.464, (6.556, 9.227, 8.424)), (' A 113  SER  O  ', ' A 149  GLY  HA2', -0.462, (-10.368, -7.146, 21.583)), (' B 100  LYS  NZ ', ' B 156  CYS  HB2', -0.462, (-12.232, 1.594, -3.608)), (' B 257  THR HG22', ' B 406  DMS  H12', -0.457, (-8.161, 20.615, 19.627)), (' A 221  ASN  OD1', ' A 506  HOH  O  ', -0.454, (21.821, -7.375, 36.646)), (' B  50  LEU  HB3', ' B 189  GLN  HB2', -0.453, (23.814, -12.91, -2.354)), (' B 163  HIS  HE1', ' B 172  HIS  HB3', -0.451, (11.437, -5.818, 6.319)), (' B  19  GLN  HB3', ' B  69  GLN  HB3', -0.451, (0.064, -22.394, 0.588)), (' A 298  ARG  NH1', ' A 401  DMS  H13', -0.451, (1.943, -12.886, 16.49)), (' A 180  ASN  ND2', ' A 512  HOH  O  ', -0.444, (-21.913, -10.895, 36.631)), (' A   6  MET  SD ', ' A 401  DMS  H21', -0.443, (3.216, -10.087, 14.185)), (' A 187  ASP  CB ', ' A 406  DMS  H23', -0.443, (-23.526, -0.362, 32.258)), (' A 223  PHE  O  ', ' A 506  HOH  O  ', -0.438, (21.49, -8.181, 37.781)), (' A  52  PRO  HD2', ' A 188  ARG  HG2', -0.437, (-28.109, 2.189, 36.779)), (' A  21  THR  HB ', ' A  67  LEU  HB2', -0.429, (-32.279, -0.736, 15.586)), (' B 108  PRO  HG3', ' B 134  PHE  CE1', -0.429, (10.699, 7.747, 0.573)), (' B 201  THR HG21', ' B 230  PHE  HE2', -0.424, (8.971, 20.397, 11.848)), (' B 153  ASP  O  ', ' B 154  TYR  HB2', -0.418, (-13.05, 3.35, 0.559)), (' B  22  CYS  SG ', ' B  61  LYS  NZ ', -0.418, (10.583, -21.806, -9.056)), (' A 118  TYR  CE1', ' A 144  SER  HB3', -0.417, (-16.566, 3.873, 19.416)), (' A  40  ARG  HD3', ' A  85  CYS  HA ', -0.416, (-26.26, -6.667, 32.083)), (' A 267  SER  OG ', ' A 507  HOH  O  ', -0.415, (20.713, -6.755, 34.386)), (' B 113  SER  O  ', ' B 149  GLY  HA2', -0.41, (0.305, -3.129, 5.276)), (' B 100  LYS  NZ ', ' B 156  CYS  SG ', -0.41, (-11.545, 1.263, -4.133)), (' A 163  HIS  CE1', ' A 172  HIS  HB3', -0.408, (-13.825, 1.428, 27.467)), (' B 260  ALA  O  ', ' B 263  ASP  HB3', -0.408, (-0.073, 26.813, 16.422)), (' B 165  MET  HE1', ' B 186  VAL  O  ', -0.408, (17.614, -6.735, -1.311)), (' B 120  GLY  O  ', ' B 508  HOH  O  ', -0.405, (-2.978, -17.96, 3.596)), (' B 100  LYS  HZ3', ' B 156  CYS  HB2', -0.404, (-11.978, 1.103, -3.55)), (' A   1  SER  OG ', ' A 504  HOH  O  ', -0.404, (16.794, -10.328, 14.559)), (' A 108  PRO  HB3', ' A 132  PRO  HA ', -0.4, (-4.971, -5.592, 36.385))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
