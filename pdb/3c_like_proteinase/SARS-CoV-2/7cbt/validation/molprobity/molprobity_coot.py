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
data['rama'] = [('A', '  81 ', 'SER', 0.04678422503292611, (5.108, 12.916999999999998, 5.272)), ('A', ' 154 ', 'TYR', 0.024053561542949214, (-13.603, -0.176, -16.574)), ('A', ' 252 ', 'PRO', 0.052992522589953746, (-14.662, 8.373, -34.514)), ('A', ' 261 ', 'VAL', 0.02214837740159967, (-13.464000000000004, 17.019, -39.246)), ('A', ' 277 ', 'ASN', 0.0155888840433352, (-27.725, 35.105, -34.452)), ('B', '  46 ', 'SER', 0.0016280633146416735, (-39.328, -7.949999999999999, -29.679999999999996)), ('B', '  47 ', 'GLU', 0.01251014679504615, (-42.920999999999985, -7.806999999999999, -30.768)), ('B', ' 194 ', 'ALA', 0.03423969225895488, (-45.021, 14.262000000000002, -25.905)), ('B', ' 238 ', 'ASN', 0.01807572878755103, (-45.014, 29.677, -21.563)), ('B', ' 243 ', 'THR', 0.0037874211328015137, (-49.19699999999999, 29.225999999999996, -7.061)), ('B', ' 261 ', 'VAL', 0.00512602, (-41.012999999999984, 37.27, -4.345)), ('B', ' 274 ', 'ASN', 0.03729642808478794, (-35.679, 41.97999999999998, -24.037)), ('B', ' 275 ', 'GLY', 0.06501133953269515, (-33.44500000000001, 38.989, -23.352))]
data['omega'] = [('B', ' 246 ', 'HIS', None, (-45.82, 27.208, -3.959)), ('B', ' 249 ', 'ILE', None, (-41.955, 27.759999999999998, -0.339))]
data['rota'] = []
data['cbeta'] = [('B', '  47 ', 'GLU', ' ', 0.34179257794799195, (-42.77, -9.085999999999999, -31.449))]
data['probe'] = [(' B 276  MET  SD ', ' B 502  HOH  O  ', -0.966, (-29.008, 34.676, -22.331)), (' B 221  ASN  O  ', ' B 501  HOH  O  ', -0.925, (-35.765, 44.799, -9.71)), (' B  46  SER  O  ', ' B  47  GLU  HB2', -0.867, (-41.375, -9.273, -32.206)), (' B 285  ALA  O  ', ' B 502  HOH  O  ', -0.811, (-29.058, 34.691, -22.608)), (' B  27  LEU HD21', ' B  42  VAL  HB ', -0.787, (-37.075, -5.662, -18.69)), (' B 292  THR  OG1', ' B 295  ASP  N  ', -0.775, (-32.832, 22.506, -5.113)), (' A 226  THR HG22', ' A 228  ASN  H  ', -0.751, (-4.287, 23.376, -42.416)), (' B 281  ILE HG22', ' B 282  LEU  HG ', -0.739, (-26.62, 33.828, -12.802)), (' A 219  PHE  HE2', ' A 264  MET  HE1', -0.736, (-21.801, 20.823, -37.196)), (' A 229  ASP  OD1', ' A 501  HOH  O  ', -0.708, (-7.645, 26.733, -46.762)), (' B 217  ARG HH21', ' B 220  LEU HD22', -0.699, (-29.197, 43.809, -6.631)), (' B 218  TRP  CE2', ' B 279  ARG  HG2', -0.695, (-25.65, 39.919, -17.839)), (' B 244  GLN  HA ', ' B 247  VAL  CG2', -0.66, (-47.122, 31.984, -4.103)), (' B 261  VAL  O  ', ' B 264  MET  HB3', -0.63, (-40.205, 37.835, -7.458)), (' B 218  TRP  CZ2', ' B 279  ARG  CG ', -0.619, (-25.906, 39.31, -18.442)), (' B 266  ALA  HA ', ' B 269  LYS  HD3', -0.617, (-41.318, 41.556, -13.735)), (' B 271  LEU HD22', ' B 276  MET  HG3', -0.602, (-32.185, 36.765, -19.622)), (' A  80  HIS  NE2', ' A 505  HOH  O  ', -0.599, (6.423, 15.393, 10.356)), (' B 107  GLN  NE2', ' B 503  HOH  O  ', -0.599, (-48.388, 15.375, -8.455)), (' B 271  LEU  CD2', ' B 276  MET  HG3', -0.597, (-31.601, 37.455, -20.068)), (' B 180  ASN  ND2', ' B 511  HOH  O  ', -0.59, (-48.125, 3.823, -7.78)), (' A 188  ARG  HG2', ' A 190  THR HG22', -0.588, (-0.28, 33.311, -0.434)), (' A  88  LYS  NZ ', ' A 507  HOH  O  ', -0.585, (5.914, 11.705, -0.832)), (' B 244  GLN  HA ', ' B 247  VAL HG23', -0.583, (-47.568, 31.547, -4.209)), (' B 276  MET  HE1', ' B 286  LEU  HA ', -0.581, (-30.659, 32.927, -21.994)), (' B 261  VAL  HB ', ' B 262  LEU  CD1', -0.581, (-43.379, 37.711, -4.928)), (' B 243  THR  OG1', ' B 244  GLN  N  ', -0.58, (-49.112, 29.0, -5.019)), (' B 218  TRP  CZ2', ' B 279  ARG  HG2', -0.579, (-25.86, 39.382, -17.458)), (' A 219  PHE  CE2', ' A 264  MET  HE1', -0.579, (-22.357, 21.17, -37.103)), (' A  54  TYR  HB3', ' A  82  MET  HE1', -0.577, (5.163, 21.878, 4.186)), (' B 260  ALA  O  ', ' B 262  LEU  N  ', -0.576, (-40.446, 39.362, -4.812)), (' B  40  ARG  O  ', ' B  43  ILE HG12', -0.576, (-42.604, -8.119, -19.029)), (' A 113  SER  HB3', ' A 127  GLN  OE1', -0.575, (-17.405, 13.317, -14.44)), (' A 299  GLN  HG2', ' A 299  GLN  O  ', -0.556, (-24.823, 10.64, -24.491)), (' B 217  ARG  NH2', ' B 220  LEU HD22', -0.555, (-29.178, 44.318, -6.815)), (' B 261  VAL  HB ', ' B 262  LEU HD12', -0.555, (-42.885, 37.486, -4.44)), (' B 270  GLU  HA ', ' B 273  GLN  HB3', -0.549, (-38.049, 42.776, -20.458)), (' B 219  PHE  HD1', ' B 267  SER  HB3', -0.545, (-34.233, 40.25, -13.111)), (' B 244  GLN  HG3', ' B 244  GLN  O  ', -0.545, (-48.741, 30.912, -1.457)), (' B 228  ASN  OD1', ' B 504  HOH  O  ', -0.543, (-52.937, 36.458, -10.591)), (' A  10  SER  OG ', ' A  14  GLU  OE2', -0.532, (-20.898, 8.424, -5.814)), (' B 224  THR HG22', ' B 225  THR  N  ', -0.528, (-44.272, 45.022, -7.951)), (' B 217  ARG  HG3', ' B 220  LEU HD22', -0.526, (-29.174, 43.362, -8.078)), (' B 249  ILE HG23', ' B 293  PRO  HG2', -0.525, (-39.474, 26.55, -3.738)), (' B 207  TRP  CH2', ' B 281  ILE  HB ', -0.525, (-28.978, 33.326, -15.568)), (' A 226  THR HG22', ' A 228  ASN  N  ', -0.524, (-4.964, 24.125, -42.256)), (' A  44  CYS  HB3', ' A  49  MET  HG3', -0.521, (-2.99, 27.885, 7.159)), (' A  65  ASN  ND2', ' A 512  HOH  O  ', -0.52, (0.287, 19.946, 17.071)), (' A 142  ASN  OD1', ' A 502  HOH  O  ', -0.518, (-16.441, 28.801, 1.792)), (' A   4  ARG  NH2', ' B 127  GLN  O  ', -0.516, (-29.607, 16.802, -16.098)), (' B 268  LEU  HB3', ' B 519  HOH  O  ', -0.515, (-40.488, 37.312, -14.508)), (' A  40  ARG  HD3', ' A  85  CYS  HA ', -0.513, (2.345, 20.786, 0.257)), (' B  55  GLU  O  ', ' B  59  ILE HG12', -0.513, (-50.495, -13.965, -17.1)), (' B 269  LYS  HD2', ' B 269  LYS  N  ', -0.511, (-41.137, 39.387, -15.497)), (' B 234  ALA  O  ', ' B 237  TYR  N  ', -0.508, (-44.803, 32.956, -21.511)), (' B  66  PHE  CE1', ' B  87  LEU HD21', -0.508, (-39.95, -10.984, -14.859)), (' B 270  GLU  HA ', ' B 273  GLN  CB ', -0.508, (-38.345, 42.31, -20.399)), (' B 113  SER  O  ', ' B 149  GLY  HA2', -0.503, (-32.054, 9.639, -10.355)), (' B 231  ASN  O  ', ' B 235  MET  HB2', -0.503, (-48.875, 34.402, -18.637)), (' B 218  TRP  CH2', ' B 281  ILE HG13', -0.502, (-28.046, 37.314, -17.304)), (' A 101  TYR  HA ', ' A 157  VAL  O  ', -0.502, (-7.462, 4.002, -9.838)), (' B 279  ARG  HG3', ' B 280  THR  N  ', -0.502, (-24.813, 37.575, -18.886)), (' B 175  THR HG22', ' B 181  PHE  HA ', -0.502, (-45.095, 5.159, -15.139)), (' B 279  ARG  HG3', ' B 280  THR  H  ', -0.499, (-24.625, 37.624, -19.133)), (' A 120  GLY  O  ', ' A 503  HOH  O  ', -0.499, (-16.084, 10.372, 4.258)), (' B  40  ARG  HD3', ' B  85  CYS  HA ', -0.499, (-45.892, -3.334, -15.726)), (' B 288  GLU  HG2', ' B 291  PHE  CE2', -0.498, (-29.749, 25.795, -14.005)), (' A   9  PRO  HD3', ' B 124  GLY  HA2', -0.496, (-20.98, 7.042, -14.637)), (' B 222  ARG  HA ', ' B 222  ARG  HE ', -0.495, (-35.584, 48.633, -9.149)), (' B 218  TRP  CZ2', ' B 279  ARG  HG3', -0.494, (-25.607, 38.352, -18.114)), (' B  45  THR  O  ', ' B  47  GLU  N  ', -0.494, (-41.302, -8.363, -28.757)), (' B 292  THR HG23', ' B 295  ASP  OD2', -0.494, (-33.454, 21.182, -8.068)), (' B 204  VAL HG11', ' B 268  LEU  CD1', -0.494, (-37.64, 33.072, -15.268)), (' B  48  ASP  O  ', ' B  52  PRO  HB3', -0.493, (-46.455, -6.324, -25.8)), (' A 164  HIS  CD2', ' A 175  THR HG23', -0.491, (-4.013, 21.135, -4.702)), (' A 108  PRO  HB3', ' A 132  PRO  HA ', -0.491, (-5.445, 23.854, -21.005)), (' A 104  VAL HG23', ' A 160  CYS  HB3', -0.49, (-6.038, 12.361, -13.776)), (' B 165  MET  CG ', ' B 401  K36  H10', -0.489, (-41.433, 2.295, -24.309)), (' B 233  VAL  O  ', ' B 237  TYR  CD2', -0.489, (-44.099, 36.564, -22.471)), (' B 209  TYR  CD1', ' B 264  MET  HE2', -0.486, (-34.921, 36.009, -5.446)), (' B 208  LEU  O  ', ' B 211  ALA  HB3', -0.484, (-30.533, 35.793, -9.082)), (' A  40  ARG  O  ', ' A  43  ILE HG12', -0.484, (-0.06, 22.12, 6.141)), (' B 262  LEU  N  ', ' B 262  LEU HD12', -0.484, (-42.426, 38.85, -4.593)), (' B  20  VAL  HB ', ' B  27  LEU HD12', -0.482, (-33.807, -7.067, -15.939)), (' A 299  GLN  CG ', ' A 299  GLN  O  ', -0.482, (-24.308, 10.405, -24.281)), (' B 217  ARG  NH2', ' B 220  LEU  CD2', -0.48, (-29.759, 44.618, -6.995)), (' A 223  PHE  O  ', ' A 263  ASP  OD1', -0.479, (-17.592, 22.431, -45.411)), (' B 234  ALA  C  ', ' B 236  LYS  N  ', -0.478, (-46.125, 34.174, -20.658)), (' B 151  ASN  ND2', ' B 518  HOH  O  ', -0.477, (-32.94, 16.084, -5.889)), (' B 112  PHE  CD2', ' B 149  GLY  HA3', -0.475, (-34.593, 10.252, -11.066)), (' B 269  LYS  HD2', ' B 519  HOH  O  ', -0.468, (-41.495, 38.474, -14.868)), (' B 276  MET  SD ', ' B 285  ALA  O  ', -0.467, (-29.45, 34.304, -21.871)), (' B 222  ARG  HA ', ' B 222  ARG  NE ', -0.462, (-35.311, 48.497, -8.722)), (' A  34  ASP  OD2', ' A  90  LYS  HE2', -0.459, (1.075, 1.424, 5.467)), (' B 244  GLN  HA ', ' B 247  VAL HG21', -0.456, (-47.45, 32.36, -3.332)), (' A 165  MET  HG2', ' A 401  K36  H11', -0.456, (-5.675, 28.696, -1.831)), (' B 251  GLY  N  ', ' B 252  PRO  CD ', -0.455, (-38.279, 29.984, 1.193)), (' A  40  ARG  CD ', ' A  85  CYS  HA ', -0.455, (1.983, 21.071, -0.145)), (' A  31  TRP  CE2', ' A  95  ASN  HB2', -0.454, (-8.664, 3.095, 3.992)), (' A 292  THR  O  ', ' A 296  VAL HG23', -0.453, (-17.26, 14.739, -26.56)), (' A  46  SER  HA ', ' A  49  MET  HE2', -0.453, (-6.226, 30.118, 8.361)), (' B 211  ALA  HA ', ' B 282  LEU HD21', -0.45, (-26.2, 34.801, -9.815)), (' B  37  TYR  CD1', ' B  37  TYR  N  ', -0.45, (-37.142, -4.183, -6.983)), (' B 226  THR  OG1', ' B 227  LEU  N  ', -0.449, (-49.588, 40.209, -7.85)), (' B 288  GLU  HG2', ' B 291  PHE  HE2', -0.446, (-29.247, 25.708, -13.789)), (' B 218  TRP  CE3', ' B 219  PHE  N  ', -0.444, (-28.815, 41.441, -15.081)), (' B  86  VAL HG13', ' B 179  GLY  HA2', -0.443, (-43.309, 0.298, -12.355)), (' A  87  LEU HD21', ' A  89  LEU HD21', -0.439, (-0.464, 15.03, 7.937)), (' A 233  VAL HG21', ' A 269  LYS  HE2', -0.439, (-10.857, 30.465, -40.921)), (' B 280  THR  OG1', ' B 284  SER  C  ', -0.438, (-25.535, 32.142, -19.128)), (' B 234  ALA  O  ', ' B 238  ASN  N  ', -0.436, (-44.698, 32.074, -21.464)), (' B  40  ARG  HD2', ' B  82  MET  SD ', -0.435, (-46.952, -6.272, -16.083)), (' B  20  VAL  HB ', ' B  27  LEU  CD1', -0.435, (-34.256, -6.578, -15.993)), (' B  83  GLN  OE1', ' B  88  LYS  NZ ', -0.43, (-45.286, -4.197, -5.818)), (' B  47  GLU  HA ', ' B  50  LEU  CD1', -0.43, (-43.268, -6.23, -31.409)), (' B 243  THR  OG1', ' B 245  ASP  N  ', -0.43, (-48.237, 28.148, -3.878)), (' B  10  SER  HB2', ' B 115  LEU HD13', -0.427, (-24.931, 6.482, -8.992)), (' B   5  LYS  NZ ', ' B 288  GLU  OE1', -0.426, (-30.087, 23.397, -16.154)), (' B 231  ASN  O  ', ' B 235  MET  CB ', -0.424, (-48.628, 33.795, -18.317)), (' B  21  THR HG23', ' B  25  THR  O  ', -0.423, (-33.161, -10.262, -20.842)), (' A  31  TRP  CD2', ' A  95  ASN  HB2', -0.423, (-9.025, 3.439, 3.784)), (' B 138  GLY  H  ', ' B 172  HIS  HD2', -0.423, (-34.324, 12.516, -21.246)), (' B 218  TRP  CE2', ' B 279  ARG  CG ', -0.422, (-25.149, 39.477, -17.763)), (' B 254  SER  HB2', ' B 259  ILE  O  ', -0.422, (-37.957, 37.403, -1.041)), (' B 204  VAL  CG1', ' B 268  LEU HD13', -0.422, (-37.295, 33.74, -14.575)), (' B   8  PHE  HE2', ' B 151  ASN HD22', -0.421, (-32.066, 14.919, -4.974)), (' B 218  TRP  HZ2', ' B 280  THR  C  ', -0.42, (-25.567, 36.659, -17.41)), (' B  83  GLN  OE1', ' B  88  LYS  HE2', -0.419, (-44.812, -3.734, -6.552)), (' B  45  THR HG23', ' B  48  ASP  H  ', -0.418, (-43.099, -9.745, -28.624)), (' B 233  VAL  O  ', ' B 237  TYR  HD2', -0.418, (-44.051, 36.073, -22.031)), (' B 224  THR HG22', ' B 225  THR  H  ', -0.418, (-43.914, 44.196, -8.22)), (' B 228  ASN  HA ', ' B 504  HOH  O  ', -0.417, (-52.633, 36.31, -11.333)), (' B 218  TRP  CH2', ' B 281  ILE  CG1', -0.416, (-28.099, 37.218, -16.514)), (' B 190  THR  O  ', ' B 192  GLN  HG3', -0.416, (-46.185, 5.843, -28.053)), (' B 297  VAL  O  ', ' B 301  SER  HB3', -0.414, (-27.097, 25.103, 0.678)), (' B 166  GLU  HB2', ' B 401  K36  C29', -0.414, (-35.392, 5.604, -24.951)), (' B 209  TYR  HA ', ' B 264  MET  HE1', -0.414, (-33.278, 36.047, -6.458)), (' B 167  LEU  HB3', ' B 168  PRO  CD ', -0.411, (-42.069, 10.59, -27.751)), (' A 114  VAL  O  ', ' A 125  VAL  HA ', -0.411, (-19.078, 15.369, -7.916)), (' B 222  ARG  O  ', ' B 223  PHE  CG ', -0.411, (-38.806, 49.368, -12.36)), (' A  40  ARG  HD2', ' A  82  MET  HE2', -0.41, (3.418, 20.886, 3.178)), (' A 238  ASN  ND2', ' A 521  HOH  O  ', -0.409, (-9.392, 36.878, -27.138)), (' B 225  THR HG21', ' B 269  LYS  NZ ', -0.407, (-44.853, 42.465, -13.474)), (' A  28  ASN  O  ', ' A 146  GLY  HA3', -0.407, (-9.313, 16.646, 1.401)), (' B 204  VAL HG11', ' B 268  LEU HD11', -0.406, (-37.922, 33.336, -15.525)), (' A 113  SER  O  ', ' A 149  GLY  HA2', -0.406, (-13.341, 14.275, -10.147)), (' B  63  ASN  OD1', ' B  80  HIS  ND1', -0.405, (-42.167, -16.613, -10.228)), (' B 270  GLU  HG3', ' B 270  GLU  O  ', -0.405, (-35.502, 42.61, -19.656)), (' A   5  LYS  HG2', ' A 127  GLN  HB2', -0.403, (-20.071, 17.458, -16.808)), (' B 204  VAL HG11', ' B 268  LEU HD13', -0.401, (-37.488, 33.692, -14.82)), (' A  19  GLN HE21', ' A  26  THR HG21', -0.4, (-14.093, 17.664, 10.039))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
