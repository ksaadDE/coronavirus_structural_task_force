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
data['rama'] = [('B', ' 209 ', 'GLY', 0.03466810837606577, (44.118999999999986, -38.33, 31.556)), ('C', '  49 ', 'SER', 0.0008551852339814667, (-13.390999999999995, 9.648000000000003, 28.614)), ('C', ' 189 ', 'CYS', 0.007540712420100703, (56.075, 35.233, 23.295000000000005)), ('C', ' 190 ', 'LYS', 0.000521030766220355, (55.188999999999965, 32.688999999999986, 20.872)), ('C', ' 302 ', 'ASP', 0.0434463260652191, (35.87499999999999, 18.737, 35.984))]
data['omega'] = [('C', ' 189 ', 'CYS', None, (55.58299999999999, 35.469, 24.641)), ('C', ' 190 ', 'LYS', None, (55.172, 33.349, 22.17))]
data['rota'] = [('D', '   7 ', 'VAL', 0.2620322774099282, (66.19700000000002, 10.438, 25.015000000000004)), ('D', ' 146 ', 'ASN', 0.15931494287161474, (50.203999999999986, 1.5580000000000003, 13.524)), ('D', ' 194 ', 'GLN', 0.15221418581041163, (2.716999999999997, 7.591000000000001, 10.06)), ('D', ' 210 ', 'THR', 0.26837207689364795, (18.84199999999999, -6.014, 5.805000000000001)), ('A', '  21 ', 'VAL', 0.24627622973709398, (53.752999999999986, -26.136000000000006, 55.012)), ('A', ' 179 ', 'ASP', 0.001591390779349543, (19.718000000000004, -32.902, 23.250000000000004)), ('A', ' 182 ', 'LYS', 0.2301134022872428, (14.055000000000001, -30.823, 18.725)), ('A', ' 191 ', 'THR', 0.26424947916008085, (10.401999999999997, -19.601, -6.861)), ('A', ' 192 ', 'CYS', 0.07571255691498276, (12.443999999999997, -22.254000000000005, -5.001)), ('A', ' 279 ', 'LYS', 0.2049682512705575, (3.2349999999999994, -14.194000000000003, 37.73)), ('A', ' 280 ', 'GLU', 0.04814665097737836, (-0.14999999999999147, -13.092, 39.079)), ('B', '   6 ', 'LYS', 0.21118008881848507, (14.972, -36.469, -18.137)), ('B', '  18 ', 'THR', 0.0013599335943581536, (15.081, -41.05, -13.258)), ('C', '  14 ', 'ILE', 0.11100912757066447, (-0.3789999999999978, 25.865, 27.643)), ('C', '  18 ', 'THR', 0.2250251140653469, (-9.246999999999996, 22.218000000000004, 19.959)), ('C', ' 143 ', 'GLU', 0.015126810821580359, (10.399999999999999, 15.729000000000003, 41.27)), ('C', ' 180 ', 'SER', 0.17016412646952173, (27.077999999999985, 38.19400000000001, 30.182)), ('C', ' 187 ', 'VAL', 0.019245024572398402, (49.909000000000006, 34.986000000000004, 26.201)), ('C', ' 190 ', 'LYS', 0.0, (55.188999999999965, 32.688999999999986, 20.872)), ('C', ' 191 ', 'THR', 0.0013599335943581536, (56.834, 34.95, 18.291)), ('C', ' 192 ', 'CYS', 0.018307194113731384, (54.45799999999999, 37.832999999999984, 19.122)), ('C', ' 302 ', 'ASP', 0.12799346970406572, (35.87499999999999, 18.737, 35.984))]
data['cbeta'] = []
data['probe'] = [(' C 190  LYS  C  ', ' C 190  LYS  HE3', -1.168, (56.498, 33.118, 18.861)), (' C 190  LYS  HD3', ' C 225  THR  OG1', -1.155, (53.841, 31.055, 16.167)), (' C 186  ASN  ND2', ' C 194  GLN  OE1', -1.032, (49.164, 39.972, 25.942)), (' C 213  TYR  OH ', ' C 307  GLU  OE2', -1.004, (38.037, 33.639, 37.838)), (' C  48  ASN  O  ', ' C  50  HIS  N  ', -0.959, (-12.246, 10.905, 26.027)), (' B 122  GLN  OE1', ' B 277  THR  OG1', -0.957, (53.138, -38.234, 10.822)), (' D 120  LEU  O  ', ' D 136  TYR  OH ', -0.924, (39.776, 4.853, 3.513)), (' A 113  LEU HD11', ' A 152  LEU HD21', -0.922, (29.636, -11.891, 34.794)), (' C  76  ASP  O  ', ' C 601  HOH  O  ', -0.871, (10.991, 17.93, 17.324)), (' A 189  CYS  SG ', ' A 192  CYS  HB3', -0.855, (12.798, -19.802, -4.022)), (' B 254  LYS  O  ', ' B 257  THR HG22', -0.854, (58.953, -39.981, 20.229)), (' C 190  LYS  HD2', ' C 225  THR  N  ', -0.843, (52.688, 29.987, 18.772)), (' C 190  LYS  HB2', ' C 224  CYS  SG ', -0.827, (52.915, 31.203, 21.041)), (' D 255  HIS  NE2', ' D 279  LYS  O  ', -0.807, (33.392, -5.104, -12.154)), (' A 283  TYR  HD2', ' A 290  LEU HD11', -0.793, (7.137, -7.478, 41.251)), (' B 127  PHE  O  ', ' B 133  GLN  NE2', -0.791, (34.477, -48.575, 6.15)), (' C  27  TYR  HH ', ' C  50  HIS  HD1', -0.786, (-9.012, 10.474, 23.194)), (' B   5  ILE HG23', ' B  23  MET  CE ', -0.783, (14.334, -30.076, -21.683)), (' A 179  ASP  N  ', ' A 179  ASP  OD1', -0.771, (20.874, -32.232, 24.415)), (' C 190  LYS  CE ', ' C 226  CYS  H  ', -0.769, (55.164, 30.894, 17.341)), (' D  83  TYR  OH ', ' D 146  ASN  ND2', -0.757, (50.407, 3.631, 16.289)), (' D 234  LEU HD21', ' D 237  GLN  HB2', -0.747, (19.151, 7.386, 1.571)), (' C 190  LYS  HG3', ' C 191  THR  H  ', -0.74, (54.698, 33.825, 18.172)), (' D 151  ILE HG12', ' D 172  LEU HD11', -0.737, (39.658, 0.924, 12.364)), (' C 190  LYS  HE3', ' C 190  LYS  O  ', -0.73, (56.805, 32.265, 19.768)), (' C 190  LYS  CA ', ' C 190  LYS  HE3', -0.722, (55.232, 32.127, 19.933)), (' C 190  LYS  HD2', ' C 224  CYS  HB3', -0.719, (53.889, 30.142, 19.639)), (' C  82  ARG  NH1', ' C 156  ASN  OD1', -0.718, (19.027, 15.669, 20.029)), (' B 281  THR HG21', ' B 292  LYS  HG3', -0.709, (63.12, -33.944, 10.058)), (' C 184  VAL HG23', ' C 236  GLN  H  ', -0.705, (40.998, 38.466, 31.258)), (' C 282  LEU HD12', ' C 295  GLU  HA ', -0.683, (39.011, 16.545, 50.944)), (' C 308  ASN  OD1', ' C 309  SER  N  ', -0.681, (34.701, 38.35, 40.733)), (' C 190  LYS  HZ1', ' C 226  CYS  HB2', -0.678, (56.579, 29.384, 18.367)), (' D  74  THR HG21', ' D  79  PHE  CD2', -0.677, (42.583, 6.03, 22.986)), (' C 190  LYS  HD2', ' C 225  THR  H  ', -0.665, (52.534, 30.199, 18.526)), (' A 221  GLN  OE1', ' A 231  THR HG22', -0.664, (6.699, -13.835, 3.914)), (' C  12  ASP  OD2', ' C  15  ASN  ND2', -0.659, (2.193, 26.961, 23.015)), (' A 103  SER  HB2', ' A 118  LEU HD21', -0.658, (16.468, -10.992, 40.908)), (' A  75  THR  HG1', ' B 268  TYR  HH ', -0.653, (40.963, -27.333, 25.759)), (' C  22  ASP  OD1', ' C  24  SER  OG ', -0.652, (-13.724, 7.399, 12.046)), (' D 301  THR HG23', ' D 302  ASP  OD1', -0.646, (29.073, -7.995, 7.914)), (' B 308  ASN  OD1', ' B 309  SER  N  ', -0.641, (49.649, -55.951, 19.775)), (' B 187  VAL HG22', ' B 232  LYS  HB2', -0.638, (41.879, -47.393, 37.891)), (' A 162  LEU HD11', ' C 270  CYS  HB2', -0.637, (29.595, -0.291, 28.927)), (' C 283  TYR  HD1', ' C 290  LEU HD11', -0.633, (28.334, 14.129, 52.403)), (' D  45  LYS  HD3', ' D  46  PRO  HD2', -0.631, (69.504, 1.844, 33.209)), (' A 283  TYR  CD2', ' A 290  LEU HD11', -0.625, (7.365, -7.976, 40.746)), (' C  71  TYR  CE2', ' C 131  ALA  HB2', -0.624, (8.618, 23.221, 27.564)), (' D   5  ILE HD13', ' D  47  HIS  O  ', -0.619, (70.89, 5.141, 26.834)), (' C 190  LYS  HE3', ' C 191  THR  N  ', -0.616, (55.741, 33.229, 19.121)), (' C 207  TYR  HE2', ' C 210  THR HG22', -0.609, (44.024, 24.346, 31.782)), (' A 502  EDO  O2 ', ' A 601  HOH  O  ', -0.609, (0.591, -24.035, 8.361)), (' C  76  ASP  OD1', ' C  78  SER  N  ', -0.607, (13.074, 15.553, 16.252)), (' B   5  ILE HG23', ' B  23  MET  HE2', -0.605, (14.788, -29.846, -20.729)), (' C 190  LYS  HG3', ' C 191  THR  N  ', -0.602, (55.126, 34.052, 18.474)), (' D  33  PRO  HB2', ' D  58  LEU HD23', -0.601, (53.802, 3.356, 30.636)), (' B 185  LEU HD13', ' B 232  LYS  HD2', -0.597, (41.113, -46.896, 33.63)), (' D 283  TYR  CE1', ' D 292  LYS  HG2', -0.595, (39.797, -11.43, -9.642)), (' A 308  ASN  OD1', ' A 309  SER  N  ', -0.587, (4.446, -29.607, 24.52)), (' D  23  MET  O  ', ' D  45  LYS  HD2', -0.586, (71.468, 1.656, 34.267)), (' B 183  ARG  NE ', ' B 237  GLN  OE1', -0.585, (43.961, -49.395, 26.192)), (' C  19  GLN  HG2', ' C  31  PHE  HE1', -0.584, (-7.032, 16.756, 15.918)), (' D  45  LYS  HD3', ' D  46  PRO  CD ', -0.583, (69.016, 1.383, 33.061)), (' C 186  ASN  OD1', ' C 196  GLN  HA ', -0.577, (46.217, 39.057, 25.04)), (' C 248  PRO  HB3', ' C 301  THR HG22', -0.575, (38.676, 12.591, 34.327)), (' C 190  LYS  CA ', ' C 190  LYS  CE ', -0.573, (55.325, 32.032, 19.31)), (' B 301  THR HG23', ' B 302  ASP  OD2', -0.571, (44.735, -33.522, 20.689)), (' A 219  GLY  HA2', ' A 232  LYS  O  ', -0.571, (7.199, -18.294, 9.296)), (' D 259  THR  OG1', ' D 306  LYS  HG3', -0.57, (30.603, 1.725, -3.731)), (' B 103  SER  HB2', ' B 118  LEU HD21', -0.57, (48.863, -33.255, 5.754)), (' C 190  LYS  HD3', ' C 225  THR  CB ', -0.569, (53.174, 30.71, 16.657)), (' D 236  GLN  HG3', ' D 311  THR HG22', -0.568, (16.95, 13.262, 0.02)), (' C 244  MET  O  ', ' C 302  ASP  HA ', -0.565, (36.802, 19.99, 35.399)), (' C 189  CYS  HB2', ' C 193  GLY  HA2', -0.565, (57.026, 37.577, 23.063)), (' B 206  MET  HE3', ' B 243  MET  SD ', -0.556, (40.738, -39.965, 20.09)), (' D   7  VAL HG12', ' D  50  HIS  O  ', -0.555, (67.951, 7.616, 24.31)), (' B 186  ASN  HB3', ' B 233  TYR  CE1', -0.554, (44.895, -52.888, 37.857)), (' C 119  THR HG21', ' C 304  PHE  CE2', -0.553, (29.23, 20.727, 37.793)), (' A  47  HIS  CG ', ' A  48  ASN  H  ', -0.55, (48.304, -18.821, 60.787)), (' B 255  HIS  ND1', ' B 256  GLY  N  ', -0.545, (61.405, -40.693, 16.462)), (' A  62  ASP  O  ', ' A  66  VAL HG23', -0.544, (45.025, -34.797, 34.313)), (' B   5  ILE HG23', ' B  23  MET  HE3', -0.542, (13.556, -30.269, -21.252)), (' A 173  PHE  HB3', ' A 202  VAL HG22', -0.541, (21.938, -24.262, 24.689)), (' A 211  LEU HD22', ' A 303  VAL HG23', -0.54, (11.401, -10.846, 23.087)), (' A  72  TYR  HB2', ' A  74  THR HG22', -0.54, (36.092, -26.957, 33.817)), (' C 190  LYS  HD3', ' C 225  THR  HG1', -0.538, (53.402, 32.112, 16.341)), (' C 188  VAL  O  ', ' C 230  ALA  HB1', -0.537, (53.528, 33.024, 24.962)), (' C  13  ASN  HB2', ' C  56  TYR  OH ', -0.535, (2.743, 20.051, 28.264)), (' B 254  LYS  HD3', ' B 255  HIS  O  ', -0.533, (62.163, -40.618, 20.122)), (' D  26  THR HG22', ' D  44  ILE  C  ', -0.533, (65.325, -0.993, 33.4)), (' C 186  ASN  OD1', ' C 196  GLN  CA ', -0.531, (46.167, 39.628, 24.936)), (' C 190  LYS  HE2', ' C 226  CYS  H  ', -0.529, (55.658, 30.738, 17.334)), (' C  57  VAL HG12', ' C  58  LEU  O  ', -0.527, (2.212, 17.012, 16.565)), (' B 243  MET  HE3', ' B 304  PHE  CZ ', -0.526, (43.714, -38.479, 18.015)), (' B 281  THR  CG2', ' B 292  LYS  HG3', -0.525, (62.675, -34.103, 9.802)), (' B 115  THR HG21', ' B 262  SER  CB ', -0.525, (46.832, -32.83, 16.552)), (' C  19  GLN  HG2', ' C  31  PHE  CE1', -0.523, (-6.866, 16.154, 16.113)), (' A 178  LEU  O  ', ' A 201  GLY  HA2', -0.523, (18.922, -30.047, 22.533)), (' B 136  TYR  CE2', ' B 140  ARG  HD2', -0.521, (42.717, -43.753, 3.462)), (' D  21  VAL HG12', ' D  31  PHE  CZ ', -0.521, (64.387, 8.805, 30.46)), (' B 184  VAL HG23', ' B 235  VAL  HB ', -0.519, (43.997, -55.36, 31.633)), (' D   4  THR  HA ', ' D  23  MET  HG3', -0.519, (72.803, 7.579, 31.431)), (' B  87  LEU  HG ', ' B  91  LYS  HD2', -0.518, (31.098, -29.616, -2.992)), (' B 183  ARG HH21', ' B 242  VAL HG12', -0.517, (44.241, -48.08, 23.856)), (' C 283  TYR  CD1', ' C 290  LEU HD11', -0.517, (28.281, 14.328, 52.178)), (' D 285  ILE HG12', ' D 290  LEU HD13', -0.517, (40.993, -9.655, -3.29)), (' B 211  LEU HD23', ' B 300  ILE HG22', -0.516, (49.504, -34.398, 23.477)), (' C 190  LYS  NZ ', ' C 226  CYS  H  ', -0.515, (55.525, 30.07, 18.109)), (' D  33  PRO  HB2', ' D  58  LEU  CD2', -0.513, (52.996, 3.364, 30.337)), (' C 190  LYS  NZ ', ' C 226  CYS  HB2', -0.511, (56.289, 29.757, 18.177)), (' C 190  LYS  HE2', ' C 226  CYS  CB ', -0.511, (56.313, 30.808, 17.08)), (' C 254  LYS  NZ ', ' C 295  GLU  OE1', -0.511, (44.75, 18.14, 52.511)), (' C 257  THR  O  ', ' C 257  THR HG22', -0.51, (40.135, 25.576, 45.524)), (' C  71  TYR  CD2', ' C 131  ALA  HB2', -0.51, (9.286, 23.292, 27.345)), (' C 119  THR HG23', ' C 260  CYS  SG ', -0.51, (29.337, 21.011, 40.882)), (' C  11  VAL HG13', ' C  64  LEU HD22', -0.509, (2.116, 21.546, 19.154)), (' B 281  THR HG21', ' B 292  LYS  CG ', -0.508, (63.432, -33.267, 9.678)), (' C 190  LYS  HE2', ' C 226  CYS  SG ', -0.508, (56.282, 31.085, 16.863)), (' A 280  GLU  OE2', ' A 283  TYR  OH ', -0.507, (2.652, -9.802, 42.594)), (' D  28  GLY  N  ', ' D  42  THR  O  ', -0.507, (61.046, 1.781, 33.446)), (' B 190  LYS  HA ', ' B 190  LYS  HE2', -0.507, (44.636, -50.072, 48.918)), (' C 190  LYS  CG ', ' C 191  THR  N  ', -0.506, (55.086, 33.575, 18.938)), (' A 129  PRO  HG2', ' A 132  LEU  HB2', -0.505, (28.106, -26.361, 34.681)), (' B 127  PHE  N  ', ' B 133  GLN HE22', -0.504, (36.186, -47.397, 6.803)), (' A 289  LEU HD12', ' A 290  LEU  H  ', -0.503, (11.977, -2.573, 43.498)), (' C  22  ASP  O  ', ' C  23  MET  HB2', -0.501, (-15.571, 8.343, 16.221)), (' B 208  MET  HE3', ' B 247  PRO  HD3', -0.499, (41.747, -33.972, 29.354)), (' D 128  ASN  HB2', ' D 129  PRO  HD3', -0.499, (37.85, 12.421, 14.801)), (' C 190  LYS  HE2', ' C 226  CYS  HB2', -0.498, (56.45, 30.749, 17.482)), (' B  71  TYR  CE2', ' B 131  ALA  HB2', -0.497, (28.064, -41.478, 1.552)), (' A  71  TYR  CD1', ' A 130  PRO  HB2', -0.497, (32.328, -30.657, 39.317)), (' C 188  VAL  O  ', ' C 230  ALA  CB ', -0.497, (53.905, 32.323, 24.742)), (' C 188  VAL HG12', ' C 189  CYS  H  ', -0.496, (56.319, 35.818, 25.571)), (' C   7  VAL HG12', ' C   8  PHE  N  ', -0.496, (-7.787, 17.103, 22.336)), (' D 133  GLN  HA ', ' D 133  GLN  OE1', -0.495, (42.67, 10.076, 8.806)), (' A 120  LEU HD21', ' A 169  MET  HE1', -0.493, (20.103, -20.011, 31.031)), (' C 169  MET  HE3', ' C 173  PHE  CZ ', -0.492, (27.358, 23.417, 33.846)), (' C 184  VAL  CG2', ' C 236  GLN  H  ', -0.491, (40.445, 38.362, 31.487)), (' C 213  TYR  HB2', ' C 305  TYR  CE2', -0.491, (39.15, 25.979, 39.651)), (' A 117  LEU  O  ', ' A 121  GLN  HG3', -0.49, (17.478, -17.807, 38.081)), (' C   7  VAL  CG1', ' C   8  PHE  N  ', -0.49, (-8.166, 16.88, 22.568)), (' B 115  THR HG21', ' B 262  SER  HB3', -0.49, (46.45, -32.088, 16.122)), (' C 219  GLY  HA2', ' C 232  LYS  O  ', -0.488, (48.478, 31.386, 32.736)), (' C 236  GLN  HA ', ' C 310  TYR  O  ', -0.488, (39.607, 39.226, 35.658)), (' C 190  LYS  CE ', ' C 226  CYS  HB2', -0.487, (56.297, 30.535, 17.728)), (' D 213  TYR  HB2', ' D 305  TYR  CE2', -0.487, (22.693, -1.154, -0.373)), (' C 115  THR HG21', ' C 262  SER  OG ', -0.486, (30.182, 15.539, 38.759)), (' C  10  THR HG21', ' C  13  ASN  HA ', -0.485, (-0.178, 20.98, 26.317)), (' D 308  ASN  OD1', ' D 309  SER  N  ', -0.484, (23.937, 11.317, -3.827)), (' D  34  THR HG23', ' D  57  VAL HG12', -0.483, (58.263, 6.411, 28.58)), (' C 186  ASN  HB2', ' C 235  VAL HG21', -0.482, (45.395, 38.802, 28.916)), (' A   9  THR HG23', ' A  19  GLN  HG3', -0.481, (48.299, -28.735, 49.207)), (' C 186  ASN  HB3', ' C 233  TYR  CZ ', -0.481, (48.446, 37.979, 28.806)), (' C  28  GLY  HA3', ' D 192  CYS  O  ', -0.479, (-1.122, 6.235, 14.818)), (' A 103  SER  OG ', ' A 104  ILE  N  ', -0.478, (19.598, -9.997, 41.434)), (' D 162  LEU HD13', ' D 163  GLY  N  ', -0.478, (35.674, -11.361, 16.532)), (' C 190  LYS  CD ', ' C 226  CYS  H  ', -0.477, (54.413, 30.537, 17.571)), (' C 188  VAL HG12', ' C 189  CYS  N  ', -0.476, (56.2, 35.593, 25.588)), (' C 120  LEU  O  ', ' C 136  TYR  OH ', -0.475, (20.937, 24.86, 39.814)), (' B  71  TYR  CD2', ' B 131  ALA  HB2', -0.475, (27.407, -42.154, 1.481)), (' C 190  LYS  CD ', ' C 224  CYS  HB3', -0.474, (53.707, 31.138, 19.376)), (' B  74  THR HG21', ' B  79  PHE  CG ', -0.472, (23.845, -37.347, 7.703)), (' C 186  ASN  OD1', ' C 196  GLN  CB ', -0.47, (45.854, 40.023, 24.756)), (' B 172  LEU  O  ', ' B 175  HIS  N  ', -0.47, (32.899, -43.798, 13.626)), (' C 162  LEU HD22', ' C 269  GLN  O  ', -0.47, (31.401, 4.316, 28.104)), (' A 188  VAL  O  ', ' A 188  VAL HG23', -0.47, (7.773, -19.424, 1.011)), (' C 264  TYR  CE1', ' C 271  GLY  HA3', -0.468, (32.516, 5.659, 33.353)), (' A 115  THR HG21', ' A 262  SER  OG ', -0.468, (17.021, -10.068, 30.878)), (' C  23  MET  HB3', ' C  23  MET  HE2', -0.467, (-15.654, 6.934, 18.826)), (' B 128  ASN  HB2', ' B 129  PRO  HD3', -0.467, (29.938, -47.032, 9.352)), (' A   8  PHE  HB2', ' A  54  THR  HA ', -0.467, (41.668, -27.918, 51.754)), (' C 190  LYS  HE2', ' C 191  THR  OG1', -0.465, (56.047, 32.379, 17.006)), (' C 211  LEU  O  ', ' C 305  TYR  OH ', -0.465, (40.373, 22.984, 40.091)), (' B 165  VAL  O  ', ' B 169  MET  HG2', -0.463, (40.012, -35.968, 17.002)), (' B 207  TYR  CE2', ' B 209  GLY  HA3', -0.463, (44.134, -39.788, 31.701)), (' C 184  VAL HG23', ' C 236  GLN  N  ', -0.463, (41.314, 38.82, 31.902)), (' A 109  ASN  HB3', ' A 162  LEU HD23', -0.461, (28.206, -3.326, 32.631)), (' A 269  GLN  CG ', ' C 269  GLN  CD ', -0.459, (31.5, 2.484, 24.839)), (' C 132  LEU  HG ', ' C 154  TYR  CE2', -0.458, (15.998, 21.854, 28.356)), (' B 115  THR HG21', ' B 262  SER  OG ', -0.458, (46.313, -33.141, 15.95)), (' C 191  THR  OG1', ' C 226  CYS  SG ', -0.458, (56.673, 32.43, 16.491)), (' A 181  CYS  HA ', ' A 238  GLU  O  ', -0.456, (13.435, -30.43, 22.448)), (' A 162  LEU  CD1', ' A 269  GLN  O  ', -0.456, (29.287, -0.839, 27.291)), (' B 282  LEU  HB2', ' B 293  SER  O  ', -0.456, (62.073, -33.475, 14.654)), (' C 255  HIS  HA ', ' C 282  LEU HD21', -0.456, (36.987, 20.597, 50.312)), (' B 257  THR  O  ', ' B 257  THR  OG1', -0.454, (56.823, -43.042, 22.293)), (' C  27  TYR  OH ', ' C  50  HIS  ND1', -0.454, (-8.606, 9.535, 23.541)), (' D 103  SER  HB2', ' D 118  LEU HD21', -0.452, (43.694, -6.29, 1.691)), (' A 269  GLN  HG3', ' C 269  GLN  CG ', -0.452, (32.173, 1.589, 25.063)), (' A  10  THR HG21', ' A  13  ASN  HA ', -0.451, (37.937, -28.434, 46.695)), (' D  34  THR HG23', ' D  57  VAL  CG1', -0.45, (58.689, 6.359, 28.185)), (' B  10  THR  HB ', ' B  16  LEU HD23', -0.449, (21.743, -40.102, -8.123)), (' A  86  ALA  O  ', ' A  90  THR HG23', -0.448, (33.745, -12.245, 40.874)), (' C 112  TYR  CZ ', ' C 163  GLY  HA3', -0.447, (25.229, 10.544, 30.581)), (' C 285  ILE HG12', ' C 290  LEU HD13', -0.447, (26.467, 13.117, 49.886)), (' C 158  THR  OG1', ' C 161  GLU  HG3', -0.446, (20.91, 5.37, 24.654)), (' C 212  SER  HB3', ' C 215  GLN  HB2', -0.446, (45.636, 24.392, 38.58)), (' B 263  GLU  O  ', ' B 273  TYR  HA ', -0.444, (47.362, -27.552, 17.528)), (' C 207  TYR  CE2', ' C 210  THR HG22', -0.443, (43.691, 24.575, 32.091)), (' B   5  ILE HD11', ' B  46  PRO  HB3', -0.443, (16.056, -29.289, -16.877)), (' A 226  CYS  SG ', ' A 228  LYS  HE2', -0.442, (13.397, -15.332, -5.381)), (' C  42  THR HG22', ' D 192  CYS  SG ', -0.442, (0.343, 4.609, 16.848)), (' B 213  TYR  HB2', ' B 305  TYR  CE2', -0.44, (50.77, -43.258, 24.159)), (' B 262  SER  O  ', ' B 301  THR HG22', -0.439, (47.615, -31.831, 20.351)), (' A  33  PRO  HA ', ' A  42  THR  OG1', -0.439, (49.091, -17.865, 43.84)), (' B 211  LEU HD21', ' B 300  ILE  O  ', -0.439, (49.006, -32.977, 25.134)), (' C 125  LEU  C  ', ' C 126  LYS  HD3', -0.439, (20.273, 30.23, 37.04)), (' D 206  MET  HE3', ' D 243  MET  SD ', -0.439, (28.428, -0.368, 9.88)), (' C  89  HIS  HB2', ' C 159  VAL HG21', -0.438, (14.534, 6.441, 30.436)), (' C 188  VAL  CG1', ' C 189  CYS  H  ', -0.438, (55.909, 36.232, 26.103)), (' A 113  LEU HD11', ' A 152  LEU  CD2', -0.437, (29.78, -12.143, 35.223)), (' D 186  ASN  HB2', ' D 235  VAL  CG2', -0.437, (10.008, 8.854, 4.848)), (' B 183  ARG  NH2', ' B 242  VAL HG12', -0.436, (44.276, -47.824, 23.867)), (' B 291  THR HG22', ' B 292  LYS  N  ', -0.436, (60.514, -28.571, 11.359)), (' B 226  CYS  SG ', ' B 227  GLY  N  ', -0.436, (38.121, -42.396, 48.565)), (' B  35  TYR  CG ', ' B  84  MET  HE2', -0.434, (24.404, -29.888, -3.32)), (' A 162  LEU HD12', ' A 269  GLN  O  ', -0.434, (29.647, -1.018, 27.198)), (' C 190  LYS  CD ', ' C 225  THR  N  ', -0.433, (53.291, 30.584, 17.934)), (' C 138  ARG  HA ', ' C 138  ARG  HD2', -0.431, (9.298, 21.227, 41.074)), (' C  21  VAL HG11', ' C  46  PRO  HG3', -0.43, (-10.171, 10.136, 19.502)), (' B 235  VAL  HA ', ' B 312  THR HG22', -0.429, (48.22, -55.55, 32.862)), (' D 190  LYS  HD3', ' D 228  LYS  NZ ', -0.429, (-3.658, -3.933, 9.124)), (' A 280  GLU  H  ', ' A 280  GLU  HG3', -0.429, (1.873, -13.271, 40.69)), (' D 120  LEU HD22', ' D 125  LEU  CD2', -0.428, (37.173, 4.455, 7.389)), (' A  36  LEU  CD1', ' A  54  THR  O  ', -0.427, (40.771, -22.828, 51.841)), (' C  87  LEU  O  ', ' C  91  LYS  HG2', -0.426, (9.171, 8.458, 32.811)), (' B   2  VAL  O  ', ' B   2  VAL HG23', -0.426, (5.625, -30.331, -22.963)), (' A 134  ASP  O  ', ' A 138  ARG  HG2', -0.426, (25.636, -24.989, 44.304)), (' B 188  VAL HG23', ' B 194  GLN  HG2', -0.425, (43.851, -53.14, 44.151)), (' D 120  LEU  CD2', ' D 125  LEU HD22', -0.425, (36.282, 4.391, 7.586)), (' D 198  THR  O  ', ' D 199  LEU HD23', -0.425, (17.183, 10.16, 13.011)), (' D 308  ASN  CG ', ' D 309  SER  H  ', -0.425, (24.081, 11.33, -4.412)), (' A 269  GLN  OE1', ' C 269  GLN  OE1', -0.423, (31.559, 4.172, 25.482)), (' D  44  ILE  O  ', ' D  44  ILE HG13', -0.421, (65.27, -0.599, 30.532)), (' A 128  ASN  N  ', ' A 129  PRO  HD2', -0.421, (26.59, -28.791, 32.977)), (' B 255  HIS  HE2', ' B 280  GLU  C  ', -0.421, (63.519, -39.587, 12.353)), (' A 192  CYS  O  ', ' A 192  CYS  SG ', -0.421, (13.442, -23.417, -3.376)), (' A 277  THR HG23', ' A 283  TYR  HB2', -0.42, (7.477, -10.463, 38.104)), (' A 269  GLN  CG ', ' C 269  GLN  CG ', -0.419, (31.724, 1.766, 25.446)), (' B  25  MET  O  ', ' B  30  GLN  NE2', -0.419, (11.121, -26.958, -12.984)), (' B  74  THR  O  ', ' B  74  THR HG23', -0.418, (21.826, -39.925, 8.342)), (' A 127  PHE  CD1', ' A 132  LEU HD13', -0.418, (25.633, -24.499, 33.33)), (' B  64  LEU  HA ', ' B  64  LEU HD23', -0.417, (16.348, -42.526, -1.318)), (' C 213  TYR  HB2', ' C 305  TYR  CD2', -0.417, (38.895, 26.754, 39.723)), (' C 115  THR HG23', ' C 275  HIS  ND1', -0.417, (28.563, 15.841, 41.418)), (' B 206  MET  CE ', ' B 243  MET  SD ', -0.417, (40.384, -40.119, 20.635)), (' C   5  ILE HD12', ' C  48  ASN  HA ', -0.416, (-15.235, 9.975, 24.123)), (' C 264  TYR  CZ ', ' C 271  GLY  HA3', -0.416, (32.946, 5.837, 32.942)), (' B 188  VAL  O  ', ' B 188  VAL HG13', -0.416, (44.944, -48.898, 43.779)), (' D  23  MET  HB3', ' D  23  MET  HE2', -0.415, (72.976, 3.664, 31.845)), (' B 211  LEU  CD2', ' B 300  ILE HG22', -0.415, (49.755, -34.197, 24.175)), (' C 301  THR  O  ', ' C 301  THR  OG1', -0.415, (35.044, 15.019, 35.388)), (' A 217  LYS  HD3', ' A 310  TYR  CE2', -0.415, (2.212, -23.276, 17.665)), (' A 192  CYS  SG ', ' B  42  THR  CG2', -0.414, (15.295, -24.081, -3.85)), (' D   9  THR  HA ', ' D  55  PHE  O  ', -0.414, (59.268, 9.669, 24.786)), (' A   9  THR HG23', ' A  19  GLN  CG ', -0.413, (47.744, -28.756, 49.359)), (' D  41  VAL  HB ', ' D  44  ILE HG12', -0.413, (63.221, -0.756, 29.11)), (' D 158  THR HG22', ' D 161  GLU  OE2', -0.412, (40.476, -8.793, 23.646)), (' D   5  ILE  CD1', ' D  50  HIS  HB2', -0.411, (69.41, 5.116, 26.072)), (' C 190  LYS  NZ ', ' C 226  CYS  N  ', -0.41, (55.36, 29.434, 17.745)), (' A  41  VAL  HB ', ' A  44  ILE HD11', -0.41, (47.131, -16.054, 51.686)), (' B 128  ASN  O  ', ' B 129  PRO  C  ', -0.409, (30.572, -47.146, 5.586)), (' A 253  LEU  HB3', ' A 258  PHE  CE1', -0.407, (5.269, -9.795, 29.112)), (' C 250  GLN  HB3', ' C 297  LYS  NZ ', -0.407, (46.547, 11.025, 43.272)), (' B 181  CYS  HA ', ' B 238  GLU  O  ', -0.407, (40.964, -54.008, 20.565)), (' D  36  LEU  C  ', ' D  36  LEU HD13', -0.406, (60.7, 1.001, 20.834)), (' D 172  LEU  HA ', ' D 172  LEU HD23', -0.406, (37.026, 4.226, 15.05)), (' C  83  TYR  HE1', ' C 150  LEU  HG ', -0.405, (11.746, 16.769, 29.828)), (' A 115  THR HG23', ' A 275  HIS  HD1', -0.405, (15.665, -11.093, 33.358)), (' A 276  ILE HD11', ' A 296  TYR  CZ ', -0.404, (10.04, -3.954, 32.458)), (' B  62  ASP  O  ', ' B  66  VAL HG23', -0.404, (13.537, -45.108, 2.838)), (' C  57  VAL HG12', ' C  58  LEU  N  ', -0.404, (2.108, 16.093, 17.595)), (' C  83  TYR  CE1', ' C 150  LEU  HG ', -0.403, (11.697, 16.881, 29.583)), (' B  89  HIS  HA ', ' B  92  LYS  HE3', -0.403, (34.091, -22.451, -0.247)), (' A  21  VAL  O  ', ' A  21  VAL HG23', -0.403, (53.74, -24.235, 56.333)), (' A  10  THR  O  ', ' A  56  TYR  HA ', -0.403, (42.232, -25.482, 45.068)), (' B 242  VAL  CG2', ' B 305  TYR  HB2', -0.402, (48.886, -45.817, 21.849)), (' C 184  VAL  CG2', ' C 236  GLN  HB3', -0.402, (39.457, 39.675, 31.434)), (' C 112  TYR  CE2', ' C 163  GLY  HA3', -0.402, (25.774, 10.8, 30.481)), (' C 248  PRO  HB3', ' C 301  THR  CG2', -0.401, (38.204, 12.141, 34.79)), (' A 166  ARG  NE ', ' A 603  HOH  O  ', -0.401, (21.328, -11.71, 21.03)), (' C 280  GLU  HG3', ' C 281  THR  N  ', -0.401, (32.09, 19.859, 56.537)), (' C 190  LYS  CE ', ' C 191  THR  OG1', -0.401, (55.908, 32.298, 17.663)), (' C 184  VAL  CG2', ' C 236  GLN  N  ', -0.4, (40.775, 38.743, 31.995)), (' B   9  THR  HA ', ' B  55  PHE  O  ', -0.4, (19.798, -35.657, -8.808)), (' C 112  TYR  CE1', ' C 163  GLY  HA3', -0.4, (25.474, 9.729, 30.307)), (' C  95  TYR  CD2', ' C 144  ALA  HB3', -0.4, (15.463, 13.596, 39.407)), (' D 234  LEU HD21', ' D 237  GLN  CB ', -0.4, (19.613, 7.145, 1.56))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
