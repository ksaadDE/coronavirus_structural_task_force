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
data['rama'] = [('A', '  25 ', 'SER', 0.01383025591165417, (22.173999999999992, 59.574000000000005, -9.061000000000002)), ('A', '  37 ', 'LEU', 0.022897836437644276, (4.097000000000002, 59.833, -13.596)), ('A', '  40 ', 'ALA', 0.0019430585939382967, (4.4209999999999985, 61.722, -18.663)), ('A', '  60 ', 'PRO', 0.006172523387652912, (5.276999999999999, 44.730000000000004, -11.312)), ('A', ' 193 ', 'CYS', 0.045264672722355105, (-30.544999999999987, 13.759, -39.894)), ('A', ' 227 ', 'CYS', 0.022765307981987077, (-24.542, 16.132, -45.406)), ('A', ' 230 ', 'ASP', 0.006934146291390075, (-29.456999999999997, 22.809, -45.015)), ('B', ' 196 ', 'LYS', 0.002513721602706974, (5.071, 61.14500000000001, -35.0)), ('B', ' 231 ', 'ALA', 0.00840642336674341, (-1.000999999999996, 59.619, -44.284))]
data['omega'] = [('A', ' 112 ', 'OCS', None, (-15.497999999999998, 56.526, -32.54))]
data['rota'] = [('A', '  14 ', 'ASN', 0.24076805550381636, (-3.5809999999999995, 53.675, -7.556000000000001)), ('A', '  21 ', 'LEU', 0.0, (13.244, 56.463, -0.9880000000000001)), ('A', '  37 ', 'LEU', 0.01448319859590101, (4.097000000000002, 59.833, -13.596)), ('A', '  42 ', 'VAL', 0.19487548403137217, (9.508, 59.626000000000005, -16.669)), ('A', '  45 ', 'ILE', 0.0, (14.715, 60.930000000000014, -15.831)), ('A', '  48 ', 'HIS', 0.0, (13.018, 66.599, -8.645000000000001)), ('A', '  52 ', 'GLU', 0.17420003939495873, (8.604000000000003, 64.275, -4.042)), ('A', '  64 ', 'THR', 0.202567508806256, (3.8840000000000003, 42.18800000000001, -4.611)), ('A', ' 159 ', 'THR', 0.014654653649567504, (-4.3359999999999985, 51.712, -29.779)), ('A', ' 180 ', 'GLU', 0.2122282029665158, (-21.218999999999994, 33.41700000000001, -14.456000000000001)), ('A', ' 187 ', 'ASN', 0.24754396511978047, (-31.45000000000001, 22.988000000000003, -30.642)), ('A', ' 193 ', 'CYS', 0.0685652153477526, (-30.544999999999987, 13.759, -39.894)), ('A', ' 223 ', 'ILE', 0.01291169729133772, (-27.179000000000002, 27.918000000000003, -42.996)), ('A', ' 232 ', 'THR', 0.24877513914122693, (-31.52099999999999, 24.839, -38.688)), ('A', ' 236 ', 'VAL', 0.056910689162276804, (-34.850999999999985, 26.534, -26.689)), ('A', ' 264 ', 'GLU', 0.06234825617860024, (-25.219, 51.037, -37.59)), ('A', ' 281 ', 'GLU', 0.00567304801514986, (-39.87000000000001, 57.76400000000002, -26.019)), ('A', ' 294 ', 'MET', 0.0, (-36.91, 59.506, -35.7)), ('B', '  65 ', 'LEU', 0.0010073416564317322, (-9.313, 24.083, -5.9)), ('B', '  68 ', 'GLU', 0.2904376349849497, (-4.584, 24.847, -9.387)), ('B', '  78 ', 'GLU', 0.2646453234078547, (-15.745, 29.877, -14.305)), ('B', '  81 ', 'LEU', 0.08786260040985541, (-13.443999999999996, 24.095, -18.025)), ('B', '  85 ', 'MET', 0.0, (-14.432, 19.488, -21.821)), ('B', '  86 ', 'SER', 0.14118813528450877, (-17.391, 19.916000000000007, -24.099)), ('B', ' 141 ', 'ARG', 0.00658193977020701, (3.535000000000001, 19.284, -32.474)), ('B', ' 147 ', 'ASN', 0.22687291309454444, (-6.153999999999996, 18.691, -26.687000000000005)), ('B', ' 192 ', 'HIS', 0.00026860898650835926, (0.9190000000000005, 69.04300000000003, -42.514)), ('B', ' 195 ', 'GLN', 0.0, (6.01, 63.50500000000002, -37.879)), ('B', ' 209 ', 'MET', 0.0, (-4.169999999999993, 44.728, -40.202)), ('B', ' 222 ', 'SER', 0.0641126574610099, (-1.129999999999999, 54.603, -46.463)), ('B', ' 223 ', 'ILE', 0.022755462315028473, (-3.885999999999994, 54.767, -43.86)), ('B', ' 230 ', 'ASP', 0.02256146156173291, (-2.4960000000000004, 61.94, -46.891)), ('B', ' 264 ', 'GLU', 0.03616488825494291, (-5.999999999999991, 31.813, -48.228)), ('B', ' 314 ', 'THR', 0.015842378782064005, (17.594, 52.173, -43.288))]
data['cbeta'] = [('A', ' 112 ', 'OCS', ' ', 0.557742014389561, (-16.014, 54.901, -34.073)), ('A', ' 230 ', 'ASP', ' ', 0.9375959356332583, (-29.425999999999995, 24.334, -45.297))]
data['probe'] = [(' A 281  GLU  OE2', ' A 284  TYR  OH ', -1.047, (-35.847, 61.943, -26.865)), (' B 265  TYR  CE1', ' B 902  P85 H142', -0.898, (-13.024, 33.523, -44.644)), (' A 225  CYS  HB2', ' A 230  ASP  HA ', -0.89, (-28.111, 21.972, -45.11)), (' A  59  LEU  O  ', ' A  61  SER  N  ', -0.758, (7.775, 45.717, -11.722)), (' A 902  P85  O20', ' A 903  DMS  H22', -0.727, (-10.976, 47.596, -37.034)), (' A 190  CYS  HB2', ' A 193  CYS  CB ', -0.72, (-29.497, 16.163, -40.046)), (' B 165  ASP  OD1', ' B 902  P85 H182', -0.717, (-12.669, 36.172, -41.015)), (' A 264  GLU  OE1', ' A 285  ARG  NH1', -0.713, (-27.776, 55.928, -39.851)), (' A 903  DMS  H12', ' B 209  MET  HG3', -0.68, (-8.168, 45.127, -38.41)), (' A  42  VAL  CG1', ' A  45  ILE HG12', -0.678, (11.519, 62.47, -15.455)), (' A 190  CYS  CB ', ' A 193  CYS  HB2', -0.672, (-30.168, 16.853, -40.475)), (' B  84  TYR  OH ', ' B 147  ASN  OD1', -0.647, (-6.966, 19.105, -23.116)), (' A 190  CYS  HB2', ' A 193  CYS  HB2', -0.639, (-30.161, 16.663, -39.745)), (' B 298  LYS  NZ ', ' B1033  HOH  O  ', -0.624, (-1.478, 39.717, -58.363)), (' A 226  VAL  O  ', ' A 226  VAL HG12', -0.62, (-21.541, 17.459, -43.018)), (' A 187  ASN  HB3', ' A 234  TYR  CE2', -0.608, (-34.152, 23.493, -32.352)), (' A  43  THR HG22', ' A  44  LYS  HE2', -0.605, (14.026, 55.127, -18.023)), (' A 223  ILE HG12', ' A 224  PRO  HD2', -0.598, (-24.92, 29.316, -44.072)), (' A 159  THR HG23', ' B 204  GLU  OE1', -0.584, (-2.24, 48.923, -31.283)), (' A  35  THR HG22', ' A  36  TYR  N  ', -0.582, (7.793, 55.98, -13.829)), (' A 268  ASN  HB2', ' A1031  HOH  O  ', -0.582, (-15.771, 46.861, -47.674)), (' A  37  LEU HD12', ' A  38  ASP  N  ', -0.577, (2.797, 62.007, -13.261)), (' A 159  THR HG21', ' B 200  LEU  CD2', -0.574, (-0.332, 50.419, -31.366)), (' A 190  CYS  HB2', ' A 193  CYS  HB3', -0.574, (-29.566, 15.993, -39.066)), (' A  37  LEU  C  ', ' A  37  LEU HD12', -0.573, (2.929, 61.999, -13.38)), (' A 231  ALA  O  ', ' A1023  HOH  O  ', -0.568, (-28.23, 25.51, -40.748)), (' A  60  PRO  HB3', ' A  66  ARG  CG ', -0.567, (4.515, 42.078, -10.561)), (' A 225  CYS  SG ', ' A 226  VAL  N  ', -0.561, (-25.143, 19.936, -43.766)), (' A  12  VAL HG13', ' A  65  LEU HD22', -0.558, (3.014, 48.468, -8.658)), (' A 159  THR  CG2', ' B 204  GLU  OE1', -0.557, (-2.137, 48.874, -30.798)), (' A 232  THR  CG2', ' A 233  GLN  N  ', -0.551, (-32.542, 25.984, -37.481)), (' B 190  CYS  SG ', ' B 193  CYS  HB2', -0.548, (-0.205, 64.457, -40.54)), (' A 113  TYR  O  ', ' A 117  VAL HG23', -0.538, (-17.646, 50.513, -29.683)), (' A 158  LYS  NZ ', ' A 903  DMS  H21', -0.538, (-8.801, 47.574, -35.704)), (' B 190  CYS  CB ', ' B 193  CYS  HB2', -0.537, (0.594, 64.624, -41.046)), (' A  18  HIS  O  ', ' A  20  GLN  HG2', -0.533, (7.607, 52.84, -2.77)), (' A  43  THR HG22', ' A  44  LYS  CE ', -0.531, (14.43, 54.705, -18.643)), (' A 229  ARG  HD3', ' A 230  ASP  N  ', -0.53, (-30.501, 21.702, -46.311)), (' A  60  PRO  HB3', ' A  66  ARG  CA ', -0.529, (3.498, 42.751, -10.619)), (' A  42  VAL HG12', ' A  45  ILE HG12', -0.528, (11.566, 61.639, -15.122)), (' A 178  ASN  OD1', ' A 180  GLU  HG3', -0.525, (-19.904, 36.503, -12.966)), (' A 190  CYS  HB3', ' A 193  CYS  HB2', -0.516, (-29.705, 16.8, -40.727)), (' A  67  SER  O  ', ' A  71  GLU  HG2', -0.51, (-3.442, 40.472, -7.265)), (' A  60  PRO  HB3', ' A  66  ARG  HA ', -0.5, (2.962, 42.608, -10.538)), (' B 283  LEU  HB2', ' B 294  MET  O  ', -0.5, (4.579, 26.613, -54.812)), (' A 209  MET  HE3', ' B 906  DMS  H21', -0.498, (-18.168, 37.835, -37.47)), (' B 230  ASP  O  ', ' B 231  ALA  HB2', -0.493, (-2.973, 60.907, -44.224)), (' A  43  THR  CG2', ' A  44  LYS  HE2', -0.489, (13.802, 54.147, -18.066)), (' A  60  PRO  CB ', ' A  66  ARG  HG2', -0.489, (4.054, 41.99, -11.607)), (' A 902  P85 H222', ' A 903  DMS  H23', -0.488, (-10.19, 47.764, -38.45)), (' A  39  GLY  O  ', ' A  41  ASP  N  ', -0.487, (4.043, 59.201, -19.236)), (' A 264  GLU  OE1', ' A 297  TYR  OH ', -0.484, (-27.972, 53.745, -39.946)), (' A  27  THR  O  ', ' A  30  GLN  HB2', -0.483, (17.208, 55.267, -12.583)), (' A  35  THR  CG2', ' A  36  TYR  N  ', -0.48, (7.822, 55.719, -13.841)), (' A  26  MET  HB3', ' A  30  GLN  HB2', -0.479, (18.591, 54.93, -12.511)), (' A  73  TYR  CE2', ' A  81  LEU HD21', -0.478, (-2.611, 48.582, -13.989)), (' A 201  THR HG23', ' B 905  DMS  H23', -0.477, (-22.267, 26.62, -21.229)), (' B 140  ALA  CB ', ' B 145  ALA  HB2', -0.475, (-1.475, 19.359, -31.898)), (' A  49  VAL  O  ', ' A  49  VAL HG12', -0.471, (12.711, 71.77, -5.239)), (' B 140  ALA  HB1', ' B 145  ALA  HB2', -0.468, (-1.745, 19.124, -32.417)), (' A  26  MET  HB3', ' A  30  GLN  CB ', -0.466, (19.165, 54.989, -12.407)), (' A 128  PHE  O  ', ' A 134  GLN  HG2', -0.465, (-17.098, 44.445, -11.867)), (' B  65  LEU HD11', ' B1018  HOH  O  ', -0.464, (-10.539, 25.256, -1.255)), (' A 199  THR  O  ', ' B 905  DMS  H21', -0.461, (-22.68, 24.986, -23.636)), (' A 131  PRO  HA ', ' A 134  GLN  OE1', -0.46, (-13.794, 45.926, -9.593)), (' A 168  GLU  O  ', ' A 171  THR  HB ', -0.459, (-14.441, 41.208, -29.126)), (' A  37  LEU  CD1', ' A  38  ASP  OD1', -0.459, (2.071, 62.732, -11.943)), (' B 207  MET  HE3', ' B 244  MET  SD ', -0.458, (-2.701, 37.392, -36.669)), (' A  17  LEU  CD1', ' A  17  LEU  N  ', -0.458, (-1.234, 53.369, -2.997)), (' A  40  ALA  O  ', ' A  42  VAL  CG2', -0.457, (6.664, 60.972, -16.563)), (' A 152  ILE HG12', ' A 173  LEU HD21', -0.457, (-13.513, 47.669, -22.221)), (' A 902  P85  O20', ' A 903  DMS  C2 ', -0.457, (-10.883, 47.596, -37.275)), (' A  42  VAL HG12', ' A  45  ILE  CG1', -0.456, (12.045, 61.862, -15.185)), (' A 128  PHE  O  ', ' A 134  GLN  CG ', -0.454, (-16.769, 44.381, -11.867)), (' B 112  OCS  OD2', ' B 113  TYR  N  ', -0.452, (-11.358, 26.76, -40.79)), (' B 190  CYS  HB2', ' B 193  CYS  HB2', -0.452, (0.835, 64.699, -40.274)), (' A 225  CYS  CB ', ' A 229  ARG  O  ', -0.446, (-28.029, 20.211, -44.9)), (' A 116  SER  HB3', ' A 263  ASN  ND2', -0.446, (-22.595, 50.979, -31.307)), (' A 104  SER  OG ', ' A 105  ILE  N  ', -0.441, (-20.145, 59.897, -26.988)), (' A  60  PRO  HB2', ' A  66  ARG  HG2', -0.44, (4.389, 42.332, -12.178)), (' A 189  VAL  CG1', ' A 190  CYS  N  ', -0.44, (-33.031, 19.329, -38.261)), (' A  40  ALA  O  ', ' A  42  VAL HG23', -0.439, (6.47, 60.375, -16.408)), (' A 167  ARG  CD ', ' A 209  MET  HE2', -0.438, (-19.479, 39.495, -34.946)), (' A  60  PRO  CB ', ' A  66  ARG  CG ', -0.437, (4.371, 42.463, -11.343)), (' A 129  ASN  O  ', ' A 131  PRO  HD3', -0.437, (-12.523, 42.62, -10.284)), (' A 283  LEU  HB3', ' A 294  MET  HE3', -0.435, (-34.335, 55.853, -34.153)), (' A  37  LEU  HB3', ' A  42  VAL HG21', -0.431, (6.978, 61.134, -14.161)), (' B 195  GLN  O  ', ' B 196  LYS  HB2', -0.431, (3.53, 62.454, -35.647)), (' A  37  LEU  HB3', ' A  42  VAL  CG2', -0.427, (6.491, 60.871, -14.259)), (' A  19  THR  C  ', ' A  20  GLN  HG2', -0.427, (8.099, 53.24, -1.828)), (' A 253  LYS  HD2', ' A 296  GLU  OE2', -0.421, (-40.061, 51.088, -41.016)), (' A  73  TYR  CZ ', ' A  81  LEU HD21', -0.418, (-2.685, 48.696, -14.061)), (' A 158  LYS  HB3', ' A 158  LYS  HE3', -0.418, (-7.627, 49.393, -31.581)), (' B 229  ARG  HB3', ' B 230  ASP  H  ', -0.416, (-3.905, 64.583, -46.634)), (' A 251  GLU  CG ', ' A 298  LYS  HE3', -0.413, (-32.721, 49.396, -46.269)), (' A  22  VAL HG12', ' A  23  ASP  N  ', -0.413, (16.537, 58.557, -5.671)), (' B 264  GLU  HG2', ' B 265  TYR  N  ', -0.412, (-8.11, 31.432, -49.2)), (' A  11  THR  O  ', ' A  11  THR HG23', -0.411, (0.531, 52.977, -9.212)), (' A  60  PRO  HB3', ' A  66  ARG  N  ', -0.411, (3.578, 42.831, -9.79)), (' A  30  GLN  HA ', ' A  30  GLN  OE1', -0.41, (18.196, 51.694, -14.106)), (' A  29  GLY  HA3', ' A  44  LYS  HE2', -0.41, (14.507, 54.084, -16.576)), (' B 137  TYR  HB2', ' B 148  PHE  CE1', -0.41, (-0.375, 24.837, -28.043)), (' A  27  THR  O  ', ' A  30  GLN  N  ', -0.409, (16.332, 54.197, -13.05)), (' B  73  TYR  CE2', ' B  81  LEU HD11', -0.408, (-9.102, 23.362, -16.517)), (' B 265  TYR  CZ ', ' B 902  P85 H142', -0.406, (-13.861, 33.589, -44.434)), (' A  80  PHE  C  ', ' A  80  PHE  CD1', -0.405, (-1.825, 47.123, -19.128)), (' B 195  GLN  HB3', ' B 195  GLN HE21', -0.405, (7.913, 62.674, -35.977)), (' A 187  ASN  HB3', ' A 234  TYR  CD2', -0.403, (-34.142, 23.842, -32.131)), (' B 274  TYR  OH ', ' B 902  P85 H141', -0.403, (-11.254, 33.718, -42.102)), (' B 166  VAL HG11', ' B 263  ASN  ND2', -0.403, (-4.65, 32.003, -40.699)), (' A  10  THR  HB ', ' A  58  VAL HG21', -0.401, (6.284, 52.186, -8.087)), (' B 284  TYR  CZ ', ' B 293  LYS  HE2', -0.4, (5.878, 19.285, -51.387))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
