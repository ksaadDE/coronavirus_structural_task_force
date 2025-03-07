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
data['omega'] = [('H', ' 157 ', 'PRO', None, (62.41781, 32.19943, 118.10777)), ('H', ' 159 ', 'PRO', None, (66.88631000000001, 28.42935, 116.17433)), ('L', ' 145 ', 'PRO', None, (61.11661999999999, 1.9161899999999985, 106.31711)), ('M', ' 157 ', 'PRO', None, (62.48904, 24.4766, 146.74734)), ('M', ' 159 ', 'PRO', None, (66.95462, 28.263449999999985, 148.64465)), ('N', ' 145 ', 'PRO', None, (61.1639, 54.72139, 158.53836))]
data['rota'] = [('B', '  90 ', 'VAL', 0.007347837199826928, (57.47311, 14.05123, 224.86564999999993)), ('B', ' 279 ', 'TYR', 0.0012125525093367776, (41.68438, 13.554349999999996, 241.89105999999998))]
data['cbeta'] = [('L', '  44 ', 'LYS', ' ', 0.2994057919791421, (63.57481, 20.540169999999993, 95.03785999999998)), ('M', '  62 ', 'GLN', ' ', 0.2880922460363974, (34.483, 30.15442, 166.84740999999997))]
data['probe'] = [(' A 150  LYS  CD ', ' A 150  LYS  CE ', -1.569, (37.47, 32.228, 74.815)), (' A 150  LYS  CE ', ' A 150  LYS  NZ ', -1.477, (37.74, 30.788, 75.158)), (' M  23  LYS  CE ', ' M  23  LYS  NZ ', -1.414, (60.216, 16.361, 180.376)), (' A 150  LYS  CE ', ' A 150  LYS  CG ', -0.952, (36.367, 31.902, 74.383)), (' M  23  LYS  CD ', ' M  23  LYS  NZ ', -0.901, (59.873, 16.506, 179.598)), (' L 198  GLN  HG2', ' L 207  GLU  HG3', -0.798, (48.988, 2.097, 121.249)), (' B  81  ASN  OD1', ' B 242  LEU HD11', -0.796, (59.074, 22.301, 210.059)), (' B 115  GLN  HG2', ' B 130  VAL HG22', -0.765, (56.435, 0.964, 210.208)), (' L  56  ARG  NH1', ' L  62  ASP  HA ', -0.743, (59.095, 6.683, 79.208)), (' B  45  SER  HB2', ' B 279  TYR  CD2', -0.738, (41.303, 9.431, 240.048)), (' A  57  PRO  HB2', ' A  60  SER  HB2', -0.737, (60.682, 36.709, 30.068)), (' A 150  LYS  CE ', ' A 150  LYS  HG2', -0.732, (36.14, 32.244, 74.743)), (' A 277  LEU HD12', ' A 284  THR HG21', -0.714, (46.291, 41.692, 26.634)), (' B 128  ILE HD12', ' B 170  TYR  HD2', -0.711, (45.401, 7.104, 213.961)), (' B  48  LEU HD12', ' B 278  LYS  HG2', -0.702, (47.508, 14.991, 245.937)), (' M  27  TYR  HB2', ' M  32  ILE HD11', -0.701, (53.885, 25.564, 186.5)), (' L 136  LEU HD12', ' L 182  LEU HD23', -0.678, (48.865, 12.305, 126.158)), (' N 136  LEU HD12', ' N 182  LEU HD23', -0.674, (48.425, 44.195, 137.728)), (' B  90  VAL HG13', ' B 194  PHE  HB2', -0.671, (55.565, 12.161, 221.948)), (' B  86  PHE  CE1', ' B  90  VAL HG12', -0.664, (57.611, 11.921, 222.078)), (' N  20  ILE HD11', ' N 107  LEU HD12', -0.66, (55.956, 50.785, 169.872)), (' L  20  ILE HD11', ' L 107  LEU HD12', -0.648, (56.08, 6.035, 94.159)), (' H  27  TYR  HB2', ' H  32  ILE HD11', -0.648, (53.608, 30.513, 77.89)), (' B 130  VAL HG12', ' B 168  PHE  HB3', -0.646, (51.301, 0.196, 211.252)), (' A 150  LYS  CD ', ' A 150  LYS  NZ ', -0.637, (37.603, 30.194, 75.638)), (' A 100  ILE HD13', ' A 263  ALA  HB2', -0.629, (53.731, 29.298, 53.952)), (' A 157  PHE  O  ', ' A 158  ARG  HB2', -0.626, (55.882, 40.387, 65.204)), (' L  56  ARG HH12', ' L  62  ASP  HB3', -0.623, (58.735, 6.277, 77.701)), (' B 141  LEU HD21', ' B 154  GLU  HG2', -0.62, (48.834, 18.248, 203.633)), (' N  28  ASP  HB3', ' N  94  THR HG22', -0.616, (37.937, 40.549, 174.21)), (' A 286  THR HG22', ' A 287  ASP  H  ', -0.611, (47.942, 37.165, 22.803)), (' B 242  LEU  N  ', ' B 242  LEU HD12', -0.604, (56.212, 20.16, 208.398)), (' B  66  HIS  HB3', ' B 264  ALA  HA ', -0.598, (57.534, 27.796, 215.627)), (' M 191  VAL HG21', ' N 139  LEU HD13', -0.596, (62.894, 45.185, 140.725)), (' A 106  PHE  HB2', ' A 117  LEU  HB3', -0.582, (56.038, 49.182, 50.067)), (' M  23  LYS  CG ', ' M  23  LYS  NZ ', -0.579, (59.079, 17.5, 180.345)), (' L  56  ARG HH12', ' L  62  ASP  CB ', -0.577, (59.297, 6.142, 78.076)), (' B 286  THR HG22', ' B 287  ASP  H  ', -0.564, (47.695, 20.01, 242.333)), (' B 130  VAL  CG1', ' B 168  PHE  HB3', -0.56, (51.784, 0.402, 211.236)), (' A  28  TYR  HB2', ' A  64  TRP  HD1', -0.553, (62.76, 26.291, 42.946)), (' H 191  VAL HG21', ' L 139  LEU HD13', -0.551, (63.061, 11.12, 123.684)), (' B  47  VAL HG22', ' B  48  LEU  H  ', -0.55, (43.5, 10.687, 247.937)), (' H 179  VAL HG21', ' L 164  GLU  HB3', -0.547, (53.301, 18.988, 117.414)), (' B 271  GLN  HB3', ' B 273  ARG  HG3', -0.545, (61.74, 12.929, 236.229)), (' L  50  ILE HD13', ' L  56  ARG  HG2', -0.54, (54.479, 10.287, 81.35)), (' A  47  VAL HG22', ' A  48  LEU  H  ', -0.538, (42.774, 45.327, 16.746)), (' H  89  GLU  N  ', ' H  89  GLU  OE1', -0.53, (46.315, 28.552, 109.877)), (' M  29  LEU HD23', ' M  72  GLU  HG2', -0.528, (49.072, 19.157, 180.157)), (' A 126  VAL  HB ', ' A 174  PRO  HA ', -0.522, (42.911, 42.947, 51.709)), (' A  41  LYS  HD3', ' A  43  PHE  HE2', -0.519, (46.503, 52.772, 26.479)), (' M 179  VAL HG21', ' N 164  GLU  HB3', -0.518, (53.365, 37.532, 147.007)), (' A 146  HIS  CE1', ' H  30  ILE HD11', -0.517, (43.706, 38.663, 75.79)), (' A 195  LYS  HE2', ' A 197  ILE HD13', -0.515, (53.893, 51.528, 35.621)), (' B 202  LYS  HA ', ' B 228  ASP  HB3', -0.511, (48.377, 5.32, 223.213)), (' B  52  GLN  OE1', ' B 274  THR  OG1', -0.511, (59.303, 7.567, 241.752)), (' A  37  TYR  OH ', ' A  54  LEU  O  ', -0.51, (53.919, 46.813, 32.759)), (' B  52  GLN  NE2', ' B 272  PRO  O  ', -0.506, (59.603, 7.332, 237.49)), (' B 126  VAL  HB ', ' B 174  PRO  HA ', -0.503, (42.722, 13.692, 212.643)), (' N  88  TYR  CE1', ' N 107  LEU HD13', -0.501, (58.055, 48.836, 170.672)), (' N  18  ILE  CD1', ' N 107  LEU HD11', -0.497, (57.844, 52.296, 171.172)), (' N 148  VAL HG12', ' N 201  HIS  HB2', -0.494, (56.098, 53.074, 152.918)), (' B 231  ILE HG22', ' B 233  ILE HG22', -0.492, (56.481, 1.476, 215.538)), (' B  86  PHE  CE1', ' B  90  VAL  CG1', -0.49, (57.648, 12.051, 221.834)), (' B 228  ASP  N  ', ' B 228  ASP  OD1', -0.484, (45.318, 4.306, 222.276)), (' N  53  VAL HG12', ' N  54  THR HG23', -0.483, (46.793, 48.878, 183.96)), (' M  91  THR HG23', ' M 120  THR  HA ', -0.479, (54.95, 25.704, 157.574)), (' A  94  SER  OG ', ' A  96  GLU  HG2', -0.478, (52.413, 30.552, 47.931)), (' M  36  TRP  HB2', ' M  70  MET  HE2', -0.476, (46.844, 25.958, 172.249)), (' A 278  LYS  HD2', ' A 286  THR  HB ', -0.476, (45.518, 37.736, 20.973)), (' M  81  MET  HB3', ' M  81  MET  HE2', -0.475, (49.494, 21.894, 169.773)), (' A  96  GLU  HA ', ' A  96  GLU  OE1', -0.475, (50.857, 27.384, 49.2)), (' B 127  VAL HG22', ' B 171  VAL HG22', -0.473, (43.6, 7.628, 207.427)), (' B 115  GLN  HG2', ' B 130  VAL  CG2', -0.471, (56.277, 1.409, 211.25)), (' L 170  LYS  HG3', ' L 176  TYR  CZ ', -0.47, (65.358, 9.623, 105.883)), (' B 279  TYR  CD1', ' B 279  TYR  N  ', -0.469, (43.296, 12.944, 241.856)), (' B 132  GLU  HG3', ' B 165  ASN  HB2', -0.469, (58.401, -1.717, 204.933)), (' M  23  LYS  CD ', ' M  23  LYS  HZ2', -0.469, (60.364, 17.045, 180.151)), (' L 185  THR  OG1', ' L 188  GLN  HG3', -0.467, (42.575, 18.544, 131.84)), (' A  41  LYS  HD3', ' A  43  PHE  CE2', -0.467, (45.986, 52.617, 26.41)), (' B 104  TRP  HB2', ' B 106  PHE  CE1', -0.467, (54.953, 12.186, 215.343)), (' A  36  VAL HG21', ' A 287  ASP  OD2', -0.465, (49.802, 38.264, 27.832)), (' H 107  THR HG22', ' L  52  ASP  OD2', -0.464, (46.864, 16.639, 77.124)), (' H  33  SER  OG ', ' H  51  PHE  HB3', -0.464, (44.501, 29.334, 83.286)), (' B 105  ILE HG22', ' B 118  LEU HD13', -0.463, (55.761, 11.391, 208.97)), (' L  56  ARG  NH1', ' L  62  ASP  CA ', -0.461, (59.223, 6.685, 78.983)), (' A 132  GLU  HG3', ' A 165  ASN  HB2', -0.461, (58.28, 58.543, 59.821)), (' H  36  TRP  HB2', ' H  70  MET  HE2', -0.46, (46.141, 30.879, 92.552)), (' A 129  LYS  HD3', ' A 169  GLU  OE2', -0.46, (47.975, 52.114, 59.813)), (' A  40  ASP  OD1', ' A 204  TYR  OH ', -0.458, (49.575, 49.759, 35.628)), (' M 129  PRO  HB3', ' M 155  TYR  HB3', -0.454, (62.403, 28.981, 140.707)), (' M 169  LEU HD21', ' M 192  VAL HG21', -0.453, (73.672, 46.007, 136.706)), (' A  96  GLU  OE2', ' A 264  ALA  N  ', -0.452, (55.088, 28.391, 49.099)), (' M  35  HIS  HB2', ' M  97  ALA  HB3', -0.452, (49.316, 30.073, 176.686)), (' B 116  SER  O  ', ' B 130  VAL  HA ', -0.45, (55.446, 4.146, 210.259)), (' A 175  PHE  CD1', ' A 226  LEU HD21', -0.449, (44.506, 43.337, 47.105)), (' B 242  LEU  H  ', ' B 242  LEU HD12', -0.448, (56.684, 20.119, 208.611)), (' B  87  ASN  OD1', ' B 269  TYR  CG ', -0.448, (63.962, 14.67, 225.612)), (' L  18  ILE HD11', ' L 107  LEU HD11', -0.447, (57.85, 4.449, 93.228)), (' M  33  SER  OG ', ' M  51  PHE  HB3', -0.446, (44.918, 27.85, 181.405)), (' M  37  VAL HG22', ' M  95  TYR  HB2', -0.446, (52.844, 31.068, 171.414)), (' B  86  PHE  HE1', ' B  90  VAL  CG1', -0.442, (57.705, 11.82, 221.386)), (' H 169  LEU HD21', ' H 192  VAL HG21', -0.44, (73.981, 10.792, 127.931)), (' M  35  HIS  ND1', ' M  50  GLY  HA3', -0.439, (44.481, 29.698, 177.036)), (' M  52  ASP  HB3', ' M  55  ALA  HB3', -0.433, (37.561, 28.862, 181.636)), (' B 194  PHE  CD1', ' B 203  ILE HG12', -0.431, (50.679, 10.914, 220.849)), (' A  14  GLN  HB3', ' A 158  ARG  HD2', -0.431, (57.685, 40.879, 68.962)), (' B 279  TYR  HD1', ' B 279  TYR  N  ', -0.428, (43.58, 12.947, 241.39)), (' A 108  THR HG22', ' A 236  THR HG23', -0.428, (64.722, 52.583, 47.385)), (' M 160  VAL HG12', ' M 210  HIS  CD2', -0.427, (66.083, 28.755, 143.532)), (' N 136  LEU  HB2', ' N 182  LEU  HB3', -0.427, (50.38, 43.17, 139.348)), (' L  68  LYS  HG2', ' L  69  SER  N  ', -0.427, (41.107, 4.854, 84.573)), (' N 198  GLN HE21', ' N 207  GLU  HG3', -0.426, (48.425, 55.415, 142.646)), (' A  41  LYS  HB3', ' A  43  PHE  CD2', -0.426, (44.671, 52.962, 27.915)), (' M  10  GLU  HB3', ' M  12  LYS  HE2', -0.426, (54.768, 17.542, 160.778)), (' A  43  PHE  HZ ', ' A  49  HIS  ND1', -0.425, (45.844, 50.522, 23.97)), (' H  35  HIS  HB2', ' H  97  ALA  HB3', -0.425, (49.155, 26.423, 88.239)), (' H  91  THR HG23', ' H 120  THR  HA ', -0.424, (54.563, 30.962, 107.146)), (' N  18  ILE HD12', ' N 107  LEU HD11', -0.423, (57.427, 52.739, 171.12)), (' M 192  VAL HG22', ' M 194  VAL HG13', -0.422, (72.343, 48.229, 136.46)), (' L  56  ARG  NH1', ' L  62  ASP  CB ', -0.422, (58.834, 6.596, 78.448)), (' B  66  HIS  HB3', ' B 264  ALA  CA ', -0.421, (57.445, 28.144, 215.892)), (' A  64  TRP  CE3', ' A 266  TYR  CE1', -0.42, (57.198, 28.094, 42.241)), (' B 277  LEU  HB3', ' B 279  TYR  HE1', -0.419, (46.366, 12.21, 239.835)), (' A  41  LYS  HB3', ' A  43  PHE  HD2', -0.417, (44.711, 53.126, 28.403)), (' B 128  ILE  O  ', ' B 169  GLU  HA ', -0.416, (47.981, 4.151, 209.839)), (' H  16  ALA  O  ', ' H  86  LEU  HG ', -0.414, (46.569, 37.996, 105.961)), (' B  41  LYS  HB3', ' B  43  PHE  CD1', -0.414, (44.294, 4.367, 236.629)), (' M 194  VAL HG11', ' M 204  TYR  CE1', -0.413, (73.625, 47.791, 134.018)), (' H 214  ASN  HB2', ' M 220  LYS  HB3', -0.412, (70.048, 37.438, 125.839)), (' N  18  ILE HD11', ' N  77  ILE HD12', -0.412, (57.803, 52.161, 172.998)), (' L  88  TYR  CE1', ' L 107  LEU HD13', -0.412, (57.951, 7.439, 93.781)), (' H  35  HIS  ND1', ' H  50  GLY  HA3', -0.412, (44.746, 26.777, 87.903)), (' M  36  TRP  HB3', ' M  48  MET  HE3', -0.41, (48.195, 26.718, 170.433)), (' N 208  LYS  HA ', ' N 208  LYS  HD3', -0.41, (54.417, 55.221, 139.067)), (' A 130  VAL HG21', ' A 231  ILE HD12', -0.41, (52.458, 54.567, 51.252)), (' H 217  VAL HG22', ' M 217  VAL HG22', -0.409, (67.287, 28.355, 132.597)), (' B  64  TRP  CE3', ' B 266  TYR  CE1', -0.408, (57.311, 28.26, 222.753)), (' B 278  LYS  HD2', ' B 286  THR  HB ', -0.407, (45.714, 18.659, 244.29)), (' A 175  PHE  O  ', ' A 190  ARG  NH2', -0.406, (44.743, 37.971, 48.88)), (' H  81  MET  HB3', ' H  81  MET  HE2', -0.405, (49.225, 34.489, 95.184)), (' H 194  VAL HG11', ' H 204  TYR  CE1', -0.404, (73.66, 9.064, 130.877)), (' A  64  TRP  NE1', ' A  66  HIS  CE1', -0.404, (60.533, 25.04, 45.372)), (' B 196  ASN  HA ', ' B 200  TYR  O  ', -0.402, (54.296, 3.646, 222.844)), (' A 233  ILE  HA ', ' A 233  ILE HD12', -0.402, (58.928, 58.377, 49.022)), (' M  27  TYR  HB2', ' M  32  ILE  CD1', -0.4, (53.313, 25.463, 186.702)), (' A 250  THR  OG1', ' A 253  ASP  OD1', -0.4, (54.875, 21.254, 73.179)), (' M 191  VAL  CG2', ' N 139  LEU HD13', -0.4, (63.35, 45.141, 140.757)), (' H  91  THR  HA ', ' H 119  VAL  O  ', -0.4, (52.971, 30.591, 105.669))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
