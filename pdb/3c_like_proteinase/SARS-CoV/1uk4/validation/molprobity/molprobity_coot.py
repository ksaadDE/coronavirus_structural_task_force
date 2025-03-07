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
data['rama'] = [('A', '  41 ', 'HIS', 0.029575141418123035, (76.416, 6.452, 8.561999999999996)), ('A', '  46 ', 'ALA', 0.019022976228235226, (72.213, 7.255000000000002, 0.212)), ('A', ' 185 ', 'PHE', 0.005831447535148164, (82.58699999999997, -5.769, 5.777)), ('A', ' 192 ', 'GLN', 0.000710935065894095, (80.963, -7.326, -0.559)), ('A', ' 284 ', 'SER', 0.04620028495121969, (64.335, -30.94900000000001, 16.873)), ('A', ' 302 ', 'GLY', 0.007719419999999999, (68.434, -22.322, 36.05)), ('B', ' 139 ', 'SER', 0.018252524101596584, (60.068, -26.87200000000001, 28.153)), ('B', ' 141 ', 'LEU', 0.031364267740105777, (59.19, -23.514, 33.346)), ('B', ' 154 ', 'TYR', 0.0326681305814068, (52.266, -0.08000000000000002, 21.443)), ('B', ' 167 ', 'LEU', 0.04075419223123948, (51.535, -31.709000000000007, 33.061)), ('B', ' 168 ', 'PRO', 0.057160829649969325, (53.568, -34.976, 32.992)), ('B', ' 169 ', 'THR', 0.0, (53.601, -35.379, 29.211999999999993)), ('B', ' 171 ', 'VAL', 0.0, (54.348999999999975, -29.26500000000001, 28.08)), ('B', ' 177 ', 'LEU', 0.03998115433706705, (44.9, -13.395, 34.579)), ('G', '   4 ', 'LEU', 0.008962532002842773, (70.137, 2.6710000000000007, 7.016))]
data['omega'] = []
data['rota'] = [('A', '   4 ', 'ARG', 0.12472202726018121, (63.689, -23.136, 23.283999999999992)), ('A', '  57 ', 'LEU', 0.11797720871457137, (81.239, 14.754000000000005, 5.843)), ('A', '  77 ', 'VAL', 0.003150532575091347, (73.839, 17.316000000000003, 22.208999999999993)), ('A', ' 104 ', 'VAL', 0.1388482326105733, (83.258, -6.756000000000002, 24.772999999999993)), ('A', ' 106 ', 'ILE', 0.01866292884112124, (82.234, -11.414, 20.872)), ('A', ' 121 ', 'SER', 0.04985358868731302, (61.30500000000001, 2.157, 20.032)), ('A', ' 188 ', 'ARG', 0.005431631742876258, (79.81899999999999, 1.7430000000000008, 2.414)), ('A', ' 189 ', 'GLN', 0.1644436508086765, (77.824, 0.61, -0.601)), ('A', ' 216 ', 'ASP', 0.1465739748830704, (67.739, -37.805, 25.725999999999992)), ('A', ' 226 ', 'THR', 0.00855152306099323, (90.59, -39.09800000000002, 17.641)), ('A', ' 227 ', 'LEU', 0.012966271608404255, (90.30199999999998, -35.305000000000014, 17.302)), ('A', ' 235 ', 'MET', 0.0, (84.623, -31.250000000000004, 7.612)), ('B', '  30 ', 'LEU', 0.03169459545432615, (52.425, -10.096, 39.459)), ('B', '  47 ', 'GLU', 0.014389819753627235, (50.922, -33.13200000000001, 50.829)), ('B', '  49 ', 'MET', 0.03510127046906602, (48.66299999999999, -31.000000000000004, 46.579)), ('B', '  55 ', 'GLU', 0.0565701979598122, (38.287000000000006, -22.931000000000008, 50.094999999999985)), ('B', '  68 ', 'VAL', 0.16637851087445374, (55.699000000000005, -10.936000000000003, 49.307)), ('B', '  75 ', 'LEU', 0.010951546978960223, (55.77199999999999, -5.63, 50.79099999999998)), ('B', ' 127 ', 'GLN', 0.2756740223064698, (57.857000000000006, -16.321, 22.14699999999999)), ('B', ' 136 ', 'ILE', 0.0, (52.009, -24.524000000000008, 25.766)), ('B', ' 171 ', 'VAL', 0.20834719685513847, (54.348999999999975, -29.26500000000001, 28.08)), ('B', ' 175 ', 'THR', 0.02991853980347514, (45.563, -19.831, 33.705)), ('B', ' 268 ', 'LEU', 0.010358322556760346, (50.60799999999998, -26.529000000000007, 1.4189999999999996)), ('B', ' 285 ', 'THR', 0.06343466144926985, (63.235, -28.136, 7.479)), ('H', '   1 ', 'ASN', 0.0, (51.528, -37.109, 38.076))]
data['cbeta'] = []
data['probe'] = [(' B2006  ATO  C1 ', ' H   5  GLN  C  ', -1.306, (56.2, -24.192, 38.653)), (' A1006  ATO  C1 ', ' G   5  GLN  C  ', -1.145, (68.705, -1.215, 9.159)), (' B2006  ATO  C1 ', ' H   5  GLN  OXT', -1.095, (56.307, -23.359, 38.928)), (' A 226  THR HG22', ' A 229  ASP  H  ', -1.033, (91.425, -38.682, 14.622)), (' A 144  SER  N  ', ' G   5  GLN  O  ', -1.007, (67.003, 0.328, 11.159)), (' B 189  GLN HE21', ' H   4  LEU HD12', -0.995, (50.948, -29.877, 41.7)), (' A1006  ATO  C1 ', ' G   5  GLN  HB3', -0.975, (70.242, -0.665, 8.548)), (' B 168  PRO  HD3', ' H   2  SER  HA ', -0.936, (52.28, -33.498, 35.671)), (' K   1  ASN  CG ', ' K   2  SER  H  ', -0.915, (43.056, -5.077, 69.074)), (' A 169  THR  HB ', ' A 171  VAL HG23', -0.89, (73.26, -13.341, 3.272)), (' B  49  MET  HA ', ' B  49  MET  HE3', -0.888, (47.796, -29.802, 45.284)), (' A 171  VAL HG12', ' A 172  HIS  H  ', -0.868, (74.223, -11.235, 7.873)), (' A 299  GLN  HB3', ' B 140  PHE  HE2', -0.865, (66.931, -24.032, 29.038)), (' H   1  ASN  H1 ', ' H   1  ASN HD22', -0.859, (51.294, -39.053, 36.539)), (' A1006  ATO  C1 ', ' G   5  GLN  CB ', -0.855, (69.808, -1.043, 8.162)), (' B 168  PRO  CD ', ' H   2  SER  HA ', -0.849, (51.41, -33.225, 35.279)), (' A1006  ATO  C1 ', ' G   5  GLN  CA ', -0.84, (69.938, -0.273, 8.73)), (' B 145  CYS  CB ', ' H   5  GLN  OXT', -0.839, (55.787, -22.503, 39.181)), (' B 145  CYS  HB2', ' H   5  GLN  OXT', -0.814, (55.265, -22.01, 39.963)), (' H   1  ASN  N  ', ' H   1  ASN HD22', -0.81, (52.02, -38.676, 36.699)), (' A  19  GLN  NE2', ' A 119  ASN  HB3', -0.806, (62.436, 7.092, 14.381)), (' A 291  PHE  HE2', ' A 299  GLN HE22', -0.786, (68.22, -22.96, 25.204)), (' A   3  PHE  HA ', ' B 140  PHE  HE1', -0.779, (64.481, -25.224, 26.107)), (' A 165  MET  HE3', ' G   1  ASN HD21', -0.773, (76.659, -2.804, 3.482)), (' B 186  VAL  H  ', ' B 192  GLN HE22', -0.757, (44.038, -30.17, 35.352)), (' B 167  LEU HD21', ' B 185  PHE  CE1', -0.753, (47.235, -31.042, 29.938)), (' A 126  TYR  CD2', ' B   6  MET  HE2', -0.752, (64.736, -10.564, 16.076)), (' A 141  LEU HD11', ' B 299  GLN  O  ', -0.749, (59.189, -6.507, 9.604)), (' B 189  GLN HE22', ' H   3  THR  HA ', -0.734, (52.908, -30.913, 40.192)), (' B 131  ARG  HB2', ' B 135  THR  O  ', -0.733, (49.486, -25.367, 23.248)), (' B 145  CYS  SG ', ' H   5  GLN  OXT', -0.73, (54.718, -23.105, 39.657)), (' B  76  ARG  HB3', ' B  92  ASP  OD2', -0.726, (52.812, -3.587, 53.64)), (' B  69  GLN  HG2', ' B  74  GLN  HG2', -0.725, (60.116, -9.243, 51.432)), (' H   1  ASN  N  ', ' H   1  ASN  ND2', -0.723, (52.429, -39.156, 37.093)), (' B2006  ATO  C1 ', ' H   5  GLN  CA ', -0.719, (55.294, -25.04, 40.26)), (' A  10  SER  O  ', ' A  14  GLU  HG3', -0.714, (65.568, -3.909, 27.148)), (' A 118  TYR  CE1', ' A 144  SER  HB3', -0.711, (64.295, -2.655, 12.133)), (' B 225  THR HG22', ' B 226  THR  O  ', -0.709, (39.925, -26.547, -1.755)), (' A 232  LEU  O  ', ' A 236  LYS  HE2', -0.707, (86.174, -35.373, 6.377)), (' B 243  THR  H  ', ' B 246  HIS  HD2', -0.699, (39.712, -22.606, 9.464)), (' A   3  PHE  HA ', ' B 140  PHE  CE1', -0.698, (64.727, -25.307, 26.103)), (' A 131  ARG  HB2', ' A 135  THR  O  ', -0.691, (76.597, -14.702, 11.01)), (' K   1  ASN  CG ', ' K   2  SER  N  ', -0.691, (42.499, -4.617, 69.269)), (' B  86  LEU  HG ', ' B 179  GLY  HA2', -0.684, (43.642, -16.695, 37.957)), (' A 226  THR HG22', ' A 229  ASP  N  ', -0.677, (91.265, -38.181, 13.932)), (' A 226  THR  CG2', ' A 229  ASP  H  ', -0.672, (91.679, -38.242, 14.641)), (' B  56  ASP  O  ', ' B  59  ILE HG22', -0.667, (39.908, -23.023, 55.307)), (' A 165  MET  HE1', ' A 188  ARG  O  ', -0.665, (77.86, -1.152, 2.769)), (' B 170  GLY  O  ', ' B 171  VAL HG22', -0.663, (53.636, -31.504, 28.659)), (' A 126  TYR  CD1', ' B   4  ARG  HG2', -0.66, (66.505, -12.827, 16.079)), (' B 269  LYS  O  ', ' B 273  GLN  HG3', -0.66, (49.484, -32.221, -0.381)), (' B 127  GLN  HA ', ' B 127  GLN HE21', -0.66, (57.032, -15.383, 22.243)), (' B 165  MET  HG2', ' H   4  LEU HD23', -0.658, (50.273, -26.892, 38.546)), (' A 165  MET  HE3', ' G   1  ASN  ND2', -0.657, (76.44, -3.195, 2.978)), (' A  49  MET  HA ', ' A  49  MET  HE2', -0.657, (77.371, 5.657, 2.288)), (' B 163  HIS  HE1', ' B 172  HIS  HB3', -0.656, (54.126, -25.088, 32.74)), (' B 243  THR  H  ', ' B 246  HIS  CD2', -0.646, (39.593, -21.548, 9.176)), (' A 100  LYS  HD2', ' A 155  ASP  OD2', -0.645, (76.18, -4.437, 38.378)), (' A 189  GLN  OE1', ' G   1  ASN  HB3', -0.645, (75.442, -2.41, -0.629)), (' A 171  VAL HG12', ' A 172  HIS  N  ', -0.645, (73.686, -10.837, 8.116)), (' A 276  MET  HE3', ' A 281  ILE HG13', -0.645, (68.531, -36.63, 17.751)), (' A 166  GLU  HB2', ' G   5  GLN  OE1', -0.643, (70.386, -4.342, 6.374)), (' A 139  SER  HA ', ' B   1  SER  O  ', -0.642, (65.599, -10.027, 9.373)), (' A  19  GLN HE21', ' A 119  ASN  HB3', -0.638, (63.026, 7.545, 14.659)), (' B  19  GLN  NE2', ' B 119  ASN  HB3', -0.638, (62.59, -16.513, 44.813)), (' A 299  GLN  HB3', ' B 140  PHE  CE2', -0.632, (66.968, -23.546, 28.619)), (' B 140  PHE  O  ', ' B 141  LEU  HG ', -0.63, (58.529, -22.628, 30.811)), (' A 135  THR  OG1', ' A 171  VAL HG11', -0.615, (75.458, -13.697, 7.532)), (' A 189  GLN  HA ', ' A 189  GLN  OE1', -0.613, (76.754, -0.343, -0.539)), (' A 117  CYS  O  ', ' A 144  SER  HA ', -0.611, (65.623, -0.706, 14.082)), (' B 161  TYR  CE1', ' B 174  GLY  HA3', -0.607, (48.902, -21.451, 31.33)), (' B 175  THR  CG2', ' B 176  ASP  O  ', -0.606, (44.891, -17.385, 34.773)), (' B 247  VAL HG13', ' B 261  VAL HG11', -0.605, (42.183, -18.188, 2.154)), (' A 291  PHE  HE2', ' A 299  GLN  NE2', -0.601, (68.702, -22.011, 25.101)), (' B 168  PRO  HG2', ' H   1  ASN  C  ', -0.598, (52.261, -35.528, 36.445)), (' A  44  CYS  SG ', ' A  49  MET  HE3', -0.592, (76.838, 7.234, 4.223)), (' B2006  ATO  C1 ', ' H   5  GLN  N  ', -0.585, (54.288, -25.096, 39.529)), (' A 189  GLN  NE2', ' G   1  ASN  O  ', -0.582, (73.83, -0.935, 0.362)), (' B  47  GLU  CD ', ' B  47  GLU  H  ', -0.581, (52.683, -32.436, 52.279)), (' B 141  LEU HD13', ' B 163  HIS  ND1', -0.58, (54.374, -23.15, 32.887)), (' B 164  HIS  CD2', ' B 175  THR  HB ', -0.577, (47.438, -20.059, 36.02)), (' A 126  TYR  CE2', ' B   6  MET  HE2', -0.571, (64.732, -10.048, 16.098)), (' B 131  ARG  HD3', ' B 132  PRO  HD2', -0.569, (48.584, -26.855, 19.417)), (' B  68  VAL HG23', ' B  75  LEU  HB2', -0.569, (55.355, -7.141, 48.524)), (' B  64  HIS  NE2', ' K   4  LEU  HG ', -0.569, (48.285, -11.137, 61.763)), (' A 186  VAL  H  ', ' A 192  GLN HE22', -0.568, (81.782, -3.729, 4.076)), (' B  33  ASP  O  ', ' B  94  SER  HA ', -0.568, (51.032, -0.162, 44.219)), (' A 111  THR HG22', ' A 129  ALA  HB2', -0.567, (74.683, -17.779, 18.814)), (' A 240  GLU  OE2', ' A 241  PRO  HD2', -0.565, (86.04, -24.474, 12.168)), (' B 131  ARG HH22', ' B 289  ASP  CG ', -0.562, (52.206, -25.422, 15.231)), (' A 140  PHE  HB3', ' A 144  SER  OG ', -0.562, (66.976, -3.558, 11.128)), (' B 109  GLY  HA2', ' B 200  ILE HD13', -0.562, (47.911, -21.843, 17.048)), (' B  49  MET  SD ', ' H   4  LEU HD13', -0.558, (49.684, -27.973, 43.425)), (' A 222  ARG  HG2', ' A 222  ARG  O  ', -0.556, (82.668, -48.893, 23.503)), (' B 175  THR HG22', ' B 176  ASP  O  ', -0.554, (44.958, -16.811, 34.75)), (' B 211  ALA  HA ', ' B 282  LEU HD13', -0.551, (60.14, -16.915, 3.744)), (' B 189  GLN  NE2', ' H   3  THR  HA ', -0.55, (52.39, -31.371, 40.713)), (' A  49  MET  C  ', ' A  52  PRO  HD3', -0.549, (79.083, 5.468, 0.174)), (' A 140  PHE  HD1', ' A 172  HIS  CD2', -0.548, (69.314, -7.4, 10.64)), (' A 113  SER  O  ', ' A 149  GLY  HA2', -0.547, (71.853, -8.15, 21.173)), (' A  63  ASN  HB3', ' A  77  VAL HG22', -0.547, (75.322, 18.86, 19.571)), (' A   5  LYS  HG2', ' A 291  PHE  CE1', -0.547, (68.777, -22.509, 20.68)), (' A 226  THR HG23', ' A 228  ASN  H  ', -0.545, (92.431, -37.179, 15.594)), (' B  31  TRP  CE2', ' B  95  ASN  HB2', -0.542, (53.974, -2.996, 42.452)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.54, (79.028, -19.698, 16.188)), (' B 163  HIS  CE1', ' B 172  HIS  HB3', -0.54, (53.694, -24.572, 32.556)), (' B  49  MET  CA ', ' B  49  MET  HE3', -0.538, (48.278, -30.412, 45.495)), (' B 217  ARG  HG2', ' B 220  LEU  CD1', -0.538, (56.053, -17.611, -5.301)), (' B  49  MET  CE ', ' B  49  MET  HA ', -0.538, (48.356, -29.592, 45.421)), (' B 165  MET  HG2', ' H   4  LEU  CD2', -0.538, (49.64, -27.236, 39.281)), (' B 141  LEU HD13', ' B 163  HIS  CE1', -0.537, (54.602, -23.279, 32.353)), (' A 163  HIS  HE1', ' A 172  HIS  HB3', -0.536, (72.39, -7.055, 9.778)), (' B 207  TRP  NE1', ' B 282  LEU HD23', -0.532, (59.025, -19.393, 8.064)), (' B 145  CYS  N  ', ' H   5  GLN  OXT', -0.529, (56.048, -22.126, 38.793)), (' B  40  ARG  O  ', ' B  43  ILE HG12', -0.528, (46.902, -21.827, 47.354)), (' A   5  LYS  HG2', ' A 291  PHE  CZ ', -0.528, (67.861, -22.297, 20.954)), (' B  49  MET  HB3', ' B 189  GLN  CG ', -0.527, (50.043, -31.517, 44.468)), (' K   1  ASN  OD1', ' K   2  SER  N  ', -0.526, (42.184, -5.812, 69.445)), (' A 163  HIS  CE1', ' A 172  HIS  HB3', -0.526, (71.841, -6.717, 10.368)), (' B  64  HIS  CD2', ' K   4  LEU  HG ', -0.52, (48.586, -10.475, 61.494)), (' A  31  TRP  CE2', ' A  75  LEU HD11', -0.518, (70.363, 10.583, 27.038)), (' G   5  GLN  HG2', ' G   5  GLN  OXT', -0.518, (68.136, -2.415, 9.298)), (' A 102  LYS  HG3', ' A 156  CYS  SG ', -0.513, (80.097, -5.163, 32.219)), (' B 225  THR  CG2', ' B 226  THR  N  ', -0.508, (40.87, -26.628, -3.035)), (' A  31  TRP  CZ2', ' A  75  LEU HD11', -0.504, (70.027, 11.043, 27.563)), (' A   3  PHE  CA ', ' B 140  PHE  HE1', -0.504, (64.59, -25.528, 25.379)), (' B 188  ARG  NE ', ' B 190  THR HG21', -0.5, (43.481, -35.247, 42.547)), (' A  55  GLU  O  ', ' A  59  ILE HG12', -0.5, (85.134, 15.473, 8.193)), (' B 131  ARG  HD3', ' B 132  PRO  CD ', -0.499, (48.695, -26.72, 19.19)), (' A  85  CYS  HB2', ' A 179  GLY  O  ', -0.499, (83.102, 0.649, 13.121)), (' B 166  GLU  O  ', ' B 167  LEU  C  ', -0.499, (53.464, -32.28, 32.966)), (' B 131  ARG  NH2', ' B 289  ASP  OD2', -0.498, (52.905, -25.244, 16.257)), (' A 166  GLU  HB2', ' G   5  GLN  CD ', -0.497, (69.612, -4.721, 6.71)), (' A 111  THR HG22', ' A 129  ALA  CB ', -0.497, (74.886, -17.92, 18.32)), (' A  48  ASP  HB3', ' A  52  PRO  HB3', -0.495, (78.374, 9.481, 1.57)), (' B 225  THR HG21', ' B 269  LYS  NZ ', -0.494, (42.899, -28.744, -2.165)), (' A 144  SER  CA ', ' G   5  GLN  O  ', -0.491, (66.891, -1.172, 11.776)), (' A 166  GLU  HG3', ' G   5  GLN HE22', -0.49, (69.099, -6.218, 6.368)), (' A  86  LEU  HG ', ' A 179  GLY  HA2', -0.49, (80.889, 1.417, 15.992)), (' A 138  GLY  O  ', ' B   2  GLY  HA3', -0.488, (66.886, -12.08, 9.712)), (' A 135  THR  CB ', ' A 171  VAL HG11', -0.487, (75.57, -12.964, 7.685)), (' A 131  ARG  NH2', ' A 289  ASP  OD2', -0.487, (74.177, -22.185, 13.866)), (' B 249  ILE  C  ', ' B 251  GLY  H  ', -0.486, (42.971, -12.888, 5.686)), (' B 138  GLY  O  ', ' B 140  PHE  N  ', -0.486, (59.175, -25.141, 29.04)), (' B  92  ASP  OD1', ' B  93  THR  N  ', -0.486, (52.927, -1.496, 50.817)), (' B 217  ARG  HG2', ' B 220  LEU HD11', -0.486, (56.085, -17.598, -4.914)), (' A  46  ALA  O  ', ' A  49  MET  HB2', -0.486, (74.827, 6.033, -0.419)), (' B  24  THR  O  ', ' B  24  THR HG22', -0.485, (59.098, -24.378, 50.745)), (' A  75  LEU HD21', ' A  93  THR  HB ', -0.485, (70.305, 14.113, 28.625)), (' G   2  SER  HA ', ' G  51  HOH  O  ', -0.484, (71.433, -0.015, 1.316)), (' A  81  SER  O  ', ' A  87  LEU HD12', -0.483, (81.189, 11.098, 16.125)), (' B  49  MET  HB3', ' B 189  GLN  HG2', -0.483, (50.453, -31.248, 43.91)), (' A   4  ARG  NH1', ' B 137  LYS  O  ', -0.48, (57.175, -24.061, 23.76)), (' A  19  GLN HE21', ' A  26  THR HG21', -0.479, (63.465, 8.232, 13.831)), (' B 188  ARG  HG2', ' B 190  THR HG23', -0.478, (45.667, -34.441, 42.173)), (' A 153  ASP  C  ', ' A 154  TYR  CD1', -0.477, (76.726, -11.241, 36.138)), (' A 139  SER  HB3', ' B   6  MET  HE1', -0.477, (63.545, -10.014, 13.397)), (' A 280  THR  HB ', ' A 283  GLY  O  ', -0.477, (63.207, -34.238, 17.637)), (' A  49  MET  O  ', ' A  52  PRO  HD3', -0.477, (79.48, 5.496, 0.535)), (' A 222  ARG  HG2', ' A 222  ARG HH11', -0.472, (82.759, -49.898, 23.734)), (' A 135  THR  HB ', ' A 171  VAL  CG1', -0.471, (75.216, -12.274, 7.767)), (' A 228  ASN  HA ', ' A1026  HOH  O  ', -0.471, (92.195, -33.595, 13.518)), (' B  47  GLU  N  ', ' B  47  GLU  OE2', -0.47, (52.749, -32.584, 51.324)), (' A 124  GLY  HA2', ' B   9  PRO  HD3', -0.47, (60.035, -6.867, 21.237)), (' A 207  TRP  O  ', ' A 210  ALA  HB3', -0.47, (71.716, -29.994, 24.525)), (' B 276  MET  HE3', ' B 281  ILE HG13', -0.469, (60.421, -25.883, 2.883)), (' B  68  VAL  CG2', ' B  75  LEU  HB2', -0.469, (55.025, -7.666, 48.805)), (' A 154  TYR  HB2', ' A 155  ASP  H  ', -0.467, (75.896, -9.062, 37.721)), (' B 138  GLY  C  ', ' B 140  PHE  N  ', -0.466, (59.274, -24.992, 28.551)), (' B 131  ARG  HD2', ' B 197  ASP  OD1', -0.465, (50.519, -28.372, 19.859)), (' B  20  VAL HG22', ' B  68  VAL HG12', -0.464, (53.314, -12.254, 48.102)), (' A 203  ASN  OD1', ' A 292  THR  HA ', -0.463, (77.577, -22.597, 21.54)), (' B 153  ASP  O  ', ' B 154  TYR  HB2', -0.461, (50.015, -0.058, 21.894)), (' B 225  THR HG22', ' B 226  THR  N  ', -0.459, (40.761, -26.409, -2.558)), (' A 169  THR  CB ', ' A 171  VAL HG23', -0.457, (73.374, -13.559, 3.342)), (' A  88  ARG  HB3', ' A  88  ARG  NH1', -0.457, (81.914, 9.356, 21.955)), (' B 100  LYS  HD2', ' B 155  ASP  OD2', -0.455, (50.285, 3.719, 27.423)), (' B 127  GLN  HA ', ' B 127  GLN  NE2', -0.455, (56.537, -14.98, 22.097)), (' A 139  SER  OG ', ' B 299  GLN  NE2', -0.454, (62.281, -11.234, 11.708)), (' A  40  ARG  C  ', ' A  42  VAL  H  ', -0.452, (76.438, 7.378, 10.524)), (' B 175  THR HG23', ' B 176  ASP  O  ', -0.448, (44.062, -17.33, 35.029)), (' A  88  ARG  CB ', ' A  88  ARG HH11', -0.447, (82.325, 9.521, 21.377)), (' A 131  ARG HH22', ' A 289  ASP  CG ', -0.447, (75.145, -23.228, 13.733)), (' A 106  ILE HD13', ' A 160  CYS  CB ', -0.446, (79.496, -9.918, 22.498)), (' B  56  ASP  OD1', ' B  60  ARG  NH1', -0.44, (40.734, -27.133, 55.876)), (' A  86  LEU HD21', ' A 162  MET  SD ', -0.438, (77.081, 1.642, 16.804)), (' B  31  TRP  CD2', ' B  95  ASN  HB2', -0.438, (54.22, -3.016, 42.384)), (' B 185  PHE  HA ', ' B 192  GLN  NE2', -0.435, (43.806, -30.687, 34.482)), (' B 186  VAL  H  ', ' B 192  GLN  NE2', -0.435, (43.728, -30.55, 35.749)), (' A 111  THR  HB ', ' A 128  CYS  O  ', -0.434, (73.541, -16.198, 20.431)), (' A 291  PHE  CE2', ' A 299  GLN  NE2', -0.432, (69.108, -22.422, 24.746)), (' B 117  CYS  SG ', ' B 122  PRO  HA ', -0.43, (61.988, -13.309, 35.653)), (' B 138  GLY  O  ', ' B 172  HIS  CE1', -0.43, (57.783, -25.819, 29.619)), (' A 165  MET  HE2', ' A 186  VAL  O  ', -0.429, (79.069, -1.911, 4.39)), (' B  54  TYR  OH ', ' B 187  ASP  HB3', -0.427, (45.605, -26.144, 42.876)), (' A  48  ASP  O  ', ' A  52  PRO  HD3', -0.426, (79.468, 6.768, 0.611)), (' A  62  SER  O  ', ' A  65  SER  HB2', -0.423, (75.009, 18.502, 13.696)), (' B 225  THR HG23', ' B 229  ASP  HB2', -0.423, (40.158, -28.767, -2.758)), (' B 229  ASP  HA ', ' B 232  LEU HD12', -0.423, (38.374, -31.962, -0.547)), (' B 145  CYS  SG ', ' H   5  GLN  CA ', -0.423, (54.514, -23.979, 40.01)), (' A 230  PHE  CZ ', ' A 268  LEU HD23', -0.422, (81.02, -33.463, 16.172)), (' B 225  THR HG21', ' B 269  LYS  HZ1', -0.421, (42.509, -29.014, -1.927)), (' A 166  GLU  HB3', ' G   2  SER  OG ', -0.42, (70.163, -4.094, 4.043)), (' B 141  LEU  HA ', ' B 144  SER  OG ', -0.42, (59.024, -21.82, 34.457)), (' A  55  GLU  CD ', ' A  55  GLU  H  ', -0.419, (85.841, 10.267, 7.297)), (' A1006  ATO  C1 ', ' G   5  GLN  OXT', -0.419, (68.666, -1.392, 10.152)), (' A  95  ASN  HA ', ' A  96  PRO  HD3', -0.419, (69.649, 9.621, 31.556)), (' B  86  LEU  HG ', ' B 179  GLY  CA ', -0.419, (43.322, -16.95, 37.697)), (' A  28  ASN HD21', ' A 144  SER  HA ', -0.417, (66.343, 0.48, 14.613)), (' B 138  GLY  C  ', ' B 140  PHE  H  ', -0.417, (59.304, -24.71, 28.403)), (' A 209  TYR  O  ', ' A 213  ILE HG13', -0.416, (73.561, -32.609, 28.814)), (' A  84  ASN  ND2', ' A 178  GLU  O  ', -0.415, (86.104, 2.023, 17.084)), (' A 121  SER  HA ', ' A 122  PRO  HD3', -0.414, (61.794, 2.333, 21.701)), (' B 189  GLN HE22', ' H   4  LEU  H  ', -0.413, (53.392, -30.089, 40.906)), (' A 153  ASP  O  ', ' A 154  TYR  CD1', -0.412, (76.562, -10.477, 36.132)), (' B 164  HIS  NE2', ' B 175  THR  HB ', -0.412, (46.801, -19.833, 36.768)), (' A 233  VAL  O  ', ' A 236  LYS  HG2', -0.412, (83.492, -35.227, 7.284)), (' B 133  ASN  O  ', ' B 134  HIS  HB2', -0.412, (44.328, -27.499, 26.027)), (' B 121  SER  HA ', ' B 122  PRO  HD3', -0.409, (63.39, -11.063, 39.085)), (' B 189  GLN  NE2', ' H   4  LEU HD12', -0.408, (51.29, -30.451, 41.646)), (' B 217  ARG  HG2', ' B 220  LEU HD12', -0.408, (56.063, -18.334, -5.485)), (' A 165  MET  SD ', ' A 187  ASP  HA ', -0.406, (78.138, -0.475, 5.822)), (' A 169  THR  HB ', ' A 171  VAL  CG2', -0.406, (73.862, -13.362, 4.14)), (' A 131  ARG  HD2', ' A 197  ASP  OD1', -0.406, (76.01, -19.492, 9.546)), (' B  93  THR HG22', ' B  94  SER  N  ', -0.405, (54.011, 0.659, 46.78)), (' B  64  HIS  HD2', ' K   5  GLN  O  ', -0.404, (47.909, -10.18, 59.925)), (' A 164  HIS  CD2', ' A 175  THR HG23', -0.402, (78.518, -1.514, 12.817)), (' A 166  GLU  CG ', ' G   5  GLN HE22', -0.402, (69.298, -6.415, 6.042)), (' A 230  PHE  HZ ', ' A 268  LEU HD23', -0.401, (81.314, -33.05, 15.882)), (' B  62  SER  O  ', ' B  65  SER  HB2', -0.401, (48.135, -15.36, 55.614)), (' B 276  MET  O  ', ' B 279  ARG  HG3', -0.401, (62.566, -29.957, -0.683)), (' B 228  ASN  O  ', ' B 232  LEU  HG ', -0.4, (37.886, -31.676, 2.063))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
