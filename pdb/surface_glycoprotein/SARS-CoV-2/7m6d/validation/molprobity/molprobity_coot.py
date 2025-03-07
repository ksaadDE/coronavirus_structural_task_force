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
data['omega'] = [('A', ' 147 ', 'PRO', None, (6.400999999999998, -54.952, -106.423)), ('A', ' 149 ', 'PRO', None, (9.782999999999996, -51.872000000000014, -110.879)), ('B', '   8 ', 'PRO', None, (-1.116, -24.41100000000001, -125.904)), ('B', '  95 ', 'PRO', None, (3.232, -19.15500000000001, -102.16899999999998)), ('B', ' 141 ', 'PRO', None, (-1.861, -39.855, -135.576)), ('H', ' 147 ', 'PRO', None, (-22.171, -18.040000000000006, -58.77)), ('H', ' 149 ', 'PRO', None, (-17.712000000000003, -14.694000000000003, -55.388)), ('L', '   8 ', 'PRO', None, (12.808, -24.293, -52.638)), ('L', ' 141 ', 'PRO', None, (0.941, -27.176, -36.213))]
data['rota'] = []
data['cbeta'] = [('C', ' 369 ', 'TYR', ' ', 0.3467206804528128, (28.017999999999997, -17.759, -102.763)), ('H', ' 144 ', 'ASP', ' ', 0.3706938078566539, (-26.78, -24.793, -52.51))]
data['probe'] = [(' C 466  ARG  NH1', ' C 468  ILE HD11', -1.049, (22.026, 8.165, -89.175)), (' A  87  THR HG22', ' A 111  VAL  H  ', -0.992, (2.243, -46.452, -103.45)), (' H   9  GLY  HA2', ' H  18  LEU HD21', -0.953, (-15.04, -10.659, -68.75)), (' B  54  ARG  HD2', ' B  58  VAL HG23', -0.941, (19.679, -21.756, -124.791)), (' B 181  LEU HD11', ' B 186  TYR  HB2', -0.912, (-12.542, -65.362, -121.261)), (' B  54  ARG  HD2', ' B  58  VAL  CG2', -0.895, (20.282, -22.163, -123.881)), (' H  30  VAL HG21', ' H  73  ASN  HB3', -0.871, (-2.615, 6.334, -77.847)), (' C 420  ASP  OD2', ' H  56  THR HG21', -0.868, (7.256, -5.091, -85.007)), (' A 200  HIS  CE1', ' A 202  PRO  HG2', -0.863, (9.805, -56.251, -108.29)), (' B 164  THR HG22', ' B 174  SER  H  ', -0.809, (3.57, -46.342, -129.468)), (' L  11  LEU HD22', ' L 104  LEU HD11', -0.803, (11.258, -19.695, -47.604)), (' C 403  ARG  HG2', ' C 406  GLU  HG3', -0.783, (19.33, -10.368, -81.269)), (' B 181  LEU  CD1', ' B 186  TYR  HB2', -0.764, (-13.781, -65.067, -120.76)), (' B 135  LEU HD21', ' B 137  ASN  HB2', -0.762, (1.79, -53.692, -133.974)), (' A  98  ILE HG22', ' C 380  TYR  HA ', -0.756, (14.695, -13.835, -101.36)), (' H 135  THR  N  ', ' H 186  SER  HG ', -0.754, (-16.438, -19.92, -22.64)), (' C 336  CYS  SG ', ' C 363  ALA  HB2', -0.744, (32.805, -5.841, -106.942)), (' H 195  ILE HG12', ' H 210  ARG  HG3', -0.743, (-28.785, -12.269, -35.161)), (' H   9  GLY  HA2', ' H  18  LEU  CD2', -0.737, (-14.476, -11.118, -68.849)), (' B   4  LEU HD21', ' B  23  CYS  SG ', -0.736, (1.992, -20.038, -116.678)), (' A  87  THR  CG2', ' A 111  VAL  H  ', -0.73, (1.532, -45.979, -103.79)), (' B  27C LEU HD22', ' B  31  ASN  HB3', -0.718, (7.429, -9.092, -115.128)), (' A   4  LEU HD12', ' A  22  CYS  SG ', -0.711, (18.425, -32.599, -102.598)), (' H  95  ASP  HA ', ' H 100B MET  H  ', -0.693, (7.148, -4.858, -67.34)), (' A  98  ILE  O  ', ' B  96  TYR  OH ', -0.691, (11.955, -18.781, -104.431)), (' L  11  LEU HD21', ' L  13  LEU HD23', -0.688, (12.715, -21.132, -44.964)), (' A 166  PHE  CE2', ' B 176  SER  HB3', -0.687, (0.899, -52.451, -126.653)), (' C 417  LYS  NZ ', ' H  97  GLU  OE2', -0.68, (14.35, -7.108, -75.344)), (' B 181  LEU HD11', ' B 186  TYR  CB ', -0.667, (-13.259, -65.475, -121.748)), (' H 163  VAL HG22', ' H 182  VAL  HB ', -0.659, (-16.744, -14.379, -36.255)), (' C 466  ARG HH11', ' C 468  ILE HD11', -0.649, (21.906, 7.942, -89.185)), (' C 466  ARG  NH1', ' C 468  ILE  CD1', -0.639, (22.333, 8.581, -88.19)), (' B  27B VAL HG23', ' B  92  TYR  CD1', -0.639, (6.151, -11.218, -109.415)), (' A  36  TRP  HB3', ' A  48  MET  HE3', -0.638, (8.164, -32.27, -102.414)), (' H  30  VAL  CG2', ' H  73  ASN  HB3', -0.637, (-2.983, 5.405, -77.638)), (' B 207  LYS  HD2', ' B 208  SER  H  ', -0.625, (-9.624, -61.434, -136.737)), (' L  11  LEU  CD2', ' L  13  LEU HD23', -0.619, (12.257, -21.094, -44.782)), (' A 195  ILE HD11', ' A 210  LYS  HG3', -0.612, (12.846, -70.483, -126.032)), (' A  83  LYS  HG2', ' A  85  SER  H  ', -0.602, (-4.042, -41.783, -100.636)), (' H 171  GLN  NE2', ' H 175  LEU  O  ', -0.601, (-21.813, -26.92, -53.213)), (' C 385  THR  O  ', ' C 386  LYS  HB2', -0.597, (23.072, -16.858, -110.114)), (' B  54  ARG  CD ', ' B  58  VAL  CG2', -0.594, (19.124, -21.455, -123.626)), (' B  54  ARG  CG ', ' B  58  VAL HG21', -0.594, (19.042, -21.792, -123.014)), (' B 116  PHE  HD1', ' B 135  LEU HD22', -0.592, (0.424, -55.548, -133.718)), (' A  98  ILE HG21', ' C 380  TYR  CD1', -0.588, (13.609, -14.2, -99.755)), (' A 126  PRO  HG3', ' A 189  LEU HD11', -0.584, (5.566, -67.055, -135.526)), (' L  37  GLN  HB2', ' L  47  LEU HD11', -0.577, (8.184, -10.626, -53.307)), (' C 460  ASN  OD1', ' H  54  GLY  HA3', -0.561, (5.661, -0.056, -83.999)), (' H  97  GLU  HG2', ' H  98  VAL  H  ', -0.56, (14.577, -4.747, -71.579)), (' A 184  VAL HG21', ' A 194  TYR  OH ', -0.557, (12.622, -63.401, -136.027)), (' C 457  ARG  NH1', ' C 467  ASP  OD2', -0.554, (13.418, 6.879, -84.914)), (' A  93  ALA  HB1', ' A 100B MET  HB3', -0.546, (14.644, -27.15, -108.112)), (' B  83  VAL HG23', ' B 104  VAL  O  ', -0.542, (7.185, -33.589, -128.045)), (' B 164  THR HG22', ' B 174  SER  N  ', -0.539, (3.116, -46.855, -129.747)), (' H  38  ARG  NE ', ' H  46  GLU  OE1', -0.538, (-2.837, -19.039, -69.511)), (' H 148  GLU  HG2', ' H 149  PRO  HA ', -0.532, (-17.247, -16.697, -54.252)), (' H  32  ASN  OD1', ' H  94  ARG  HD2', -0.529, (5.508, 1.614, -70.394)), (' A 181  VAL HG21', ' B 135  LEU HD12', -0.529, (2.333, -56.009, -129.494)), (' B  37  GLN  HB2', ' B  86  TYR  HE1', -0.527, (12.364, -28.081, -122.073)), (' L  27A SER  HA ', ' L  69  THR HG22', -0.527, (20.955, -21.283, -68.375)), (' C 411  ALA  HB3', ' C 414  GLN  HG3', -0.526, (12.103, -11.609, -91.584)), (' H 178  LEU HD23', ' H 179  SER  O  ', -0.526, (-17.696, -19.82, -44.463)), (' A 126  PRO  CG ', ' A 189  LEU HD11', -0.525, (4.974, -67.103, -135.268)), (' B 117  ILE HG22', ' B 207  LYS  HG3', -0.523, (-6.464, -60.357, -135.277)), (' A  87  THR HG22', ' A 111  VAL  N  ', -0.522, (2.684, -45.94, -103.222)), (' C 393  THR HG21', ' C 518  LEU  H  ', -0.522, (19.215, 1.62, -111.743)), (' B 129  THR HG22', ' B 130  ALA  H  ', -0.522, (-9.25, -63.3, -117.148)), (' L   2  ILE HD12', ' L  90  GLN  NE2', -0.519, (14.143, -17.323, -72.166)), (' C 379  CYS  HA ', ' C 432  CYS  HA ', -0.519, (19.818, -12.645, -99.911)), (' A  36  TRP  HD1', ' A  69  ILE HD13', -0.517, (9.691, -29.677, -98.498)), (' B  80  ALA  O  ', ' B  83  VAL HG12', -0.516, (12.61, -35.386, -129.347)), (' A  48  MET  HE1', ' A  90  TYR  HD2', -0.513, (7.049, -34.622, -102.728)), (' A 100A PRO  HD3', ' B  91  TYR  CZ ', -0.512, (14.395, -17.305, -110.851)), (' C 403  ARG  HG2', ' C 406  GLU  CG ', -0.512, (18.956, -10.126, -80.96)), (' H 100A ALA  O  ', ' L  46  LEU HD22', -0.512, (8.906, -5.154, -62.994)), (' H   5  VAL HG13', ' H 105  GLN HE22', -0.511, (-9.149, -0.918, -61.829)), (' L  39  LYS  HG2', ' L  84  ALA  HB2', -0.511, (3.139, -11.894, -49.269)), (' B  54  ARG  CG ', ' B  58  VAL  CG2', -0.509, (19.794, -21.608, -123.006)), (' A 195  ILE HD13', ' A 210  LYS  HA ', -0.509, (11.597, -68.321, -125.508)), (' A 123  PRO  HB3', ' A 209  LYS  HD2', -0.506, (5.983, -67.54, -124.165)), (' H  12  ILE HD11', ' H  17  SER  H  ', -0.506, (-18.634, -14.899, -74.126)), (' B   6  GLN  OE1', ' B  87  TYR  HA ', -0.5, (4.128, -25.894, -118.262)), (' A 166  PHE  CD2', ' B 176  SER  HB3', -0.5, (0.663, -51.83, -125.887)), (' C 338  PHE  HE2', ' C 363  ALA  CB ', -0.495, (31.317, -6.923, -105.71)), (' H 171  GLN  HG2', ' H 175  LEU  O  ', -0.495, (-21.325, -27.03, -54.238)), (' B 116  PHE  CD1', ' B 135  LEU HD22', -0.495, (0.433, -55.87, -134.179)), (' L   4  LEU HD23', ' L  23  CYS  SG ', -0.493, (13.503, -18.647, -62.444)), (' A  72  ASP  OD1', ' A  74  SER  OG ', -0.492, (23.524, -32.125, -89.181)), (' B 207  LYS  HD2', ' B 208  SER  N  ', -0.491, (-9.347, -60.93, -136.337)), (' C 486  PHE  HE1', ' H  94  ARG HH22', -0.49, (6.778, 3.496, -64.497)), (' H 171  GLN HE22', ' H 177  SER  HB2', -0.489, (-22.093, -25.431, -50.84)), (' L 158  ASN  N  ', ' L 158  ASN  OD1', -0.484, (-18.339, -39.053, -47.21)), (' B 129  THR HG22', ' B 130  ALA  N  ', -0.483, (-8.77, -63.906, -117.349)), (' C 335  LEU HD12', ' C 336  CYS  H  ', -0.478, (36.258, -5.662, -106.814)), (' A 181  VAL HG11', ' B 135  LEU HD11', -0.477, (3.286, -55.482, -130.836)), (' H   6  GLU  OE1', ' H 106  GLY  N  ', -0.476, (-6.626, -6.615, -62.063)), (' A 100A PRO  HD3', ' B  91  TYR  CE2', -0.475, (13.859, -17.012, -110.213)), (' A  38  ARG  N  ', ' A  48  MET  HE2', -0.473, (6.426, -32.666, -104.799)), (' B  54  ARG  HG2', ' B  58  VAL  CG2', -0.472, (19.591, -21.331, -122.377)), (' L  24  ARG  HA ', ' L  69  THR  O  ', -0.468, (18.232, -22.03, -62.746)), (' B  89  GLN  HB2', ' B  98  PHE  CD1', -0.467, (6.992, -24.62, -112.574)), (' A  98  ILE HG21', ' C 380  TYR  HD1', -0.465, (13.294, -13.752, -99.375)), (' C 338  PHE  HE2', ' C 363  ALA  HB1', -0.464, (31.427, -7.219, -105.085)), (' A  51  ILE HG13', ' A  57  THR  HB ', -0.463, (11.809, -25.196, -93.57)), (' A  38  ARG  NH2', ' A  63  PHE  HE1', -0.463, (0.265, -34.069, -101.984)), (' A  98  ILE HG23', ' A  99  SER  N  ', -0.461, (13.195, -15.459, -102.692)), (' B 123  GLU  N  ', ' B 123  GLU  OE1', -0.46, (-0.973, -72.214, -121.534)), (' H  96  LEU  HB2', ' H 100  GLY  O  ', -0.458, (11.009, -2.796, -67.074)), (' L 104  LEU  HA ', ' L 104  LEU HD12', -0.458, (7.979, -20.048, -47.441)), (' A 181  VAL HG11', ' B 135  LEU  CD1', -0.458, (2.822, -56.101, -130.863)), (' B  21  ILE HD11', ' B 104  VAL HG21', -0.457, (6.065, -27.269, -126.492)), (' H  12  ILE  CD1', ' H  17  SER  H  ', -0.456, (-18.469, -15.035, -73.988)), (' B  59  PRO  HD2', ' B  62  PHE  CE2', -0.456, (17.626, -25.992, -126.331)), (' A  82  TRP  HZ2', ' A  90  TYR  CE2', -0.455, (5.13, -37.24, -101.037)), (' L  11  LEU HD22', ' L 104  LEU  CD1', -0.455, (10.182, -19.613, -47.299)), (' A 181  VAL HG12', ' A 182  VAL  N  ', -0.455, (6.644, -57.157, -130.803)), (' H 200  HIS  CD2', ' H 202  PRO  HD2', -0.455, (-22.602, -13.551, -55.932)), (' H  18  LEU  HA ', ' H  18  LEU HD12', -0.454, (-17.431, -11.264, -72.589)), (' A  18  LEU  HB2', ' A  82C LEU HD11', -0.452, (5.927, -43.586, -96.188)), (' L 113  PRO  HB3', ' L 139  PHE  HB3', -0.452, (-6.125, -27.084, -33.882)), (' L  13  LEU HD12', ' L  17  GLU  OE1', -0.451, (14.803, -20.02, -39.813)), (' L  42  GLN  HB3', ' L  43  ALA  H  ', -0.449, (-1.386, -8.126, -54.465)), (' H  50  VAL HG12', ' H  58  TYR  HB2', -0.449, (3.784, -10.61, -77.113)), (' A 119  PRO  HB3', ' A 145  TYR  HB3', -0.447, (5.597, -59.545, -112.739)), (' C 337  PRO  HD2', ' C 358  ILE HG23', -0.446, (32.755, -1.76, -103.715)), (' B 140  TYR  CD1', ' B 141  PRO  HA ', -0.445, (0.513, -39.15, -134.395)), (' B 125  LEU  O  ', ' B 183  LYS  HD2', -0.444, (-8.494, -71.207, -116.555)), (' H  14  PRO  HA ', ' H  82C LEU  O  ', -0.444, (-15.843, -21.68, -73.799)), (' H  13  GLN  HG2', ' H  14  PRO  O  ', -0.442, (-20.005, -21.017, -74.464)), (' B 181  LEU HD12', ' B 182  SER  O  ', -0.441, (-13.496, -65.316, -118.972)), (' B 150  VAL HG22', ' B 189  HIS  CG ', -0.44, (-19.309, -63.861, -125.725)), (' B   8  PRO  HG2', ' B  10  SER  O  ', -0.439, (-0.908, -27.691, -127.819)), (' C 400  PHE  HZ ', ' C 410  ILE HD12', -0.439, (19.998, -6.574, -90.161)), (' B 136  LEU  O  ', ' B 174  SER  HA ', -0.438, (0.794, -48.949, -131.447)), (' H  97  GLU  CG ', ' H  98  VAL  N  ', -0.437, (13.998, -4.802, -70.758)), (' H  22  CYS  C  ', ' H  77  THR HG23', -0.436, (-8.078, -0.016, -70.24)), (' C 476  GLY  H  ', ' C 487  ASN  HB3', -0.436, (6.217, 8.318, -68.608)), (' A 209  LYS  C  ', ' A 209  LYS  HD3', -0.435, (8.408, -68.311, -123.647)), (' B 164  THR HG23', ' B 165  GLU  O  ', -0.435, (5.515, -45.047, -128.32)), (' H  97  GLU  HG2', ' H  98  VAL  N  ', -0.434, (14.362, -4.936, -70.795)), (' B  35  TRP  HB2', ' B  48  ILE  HB ', -0.434, (12.414, -20.677, -119.667)), (' L 188  LYS  HB3', ' L 188  LYS  HE3', -0.433, (-30.698, -46.003, -40.848)), (' H 141  LEU  CD2', ' H 143  LYS  HB2', -0.432, (-24.735, -24.638, -46.052)), (' C 469  SER  OG ', ' C 471  GLU  HG2', -0.43, (15.144, 11.345, -79.928)), (' B  37  GLN  HB2', ' B  86  TYR  CE1', -0.43, (11.689, -28.216, -122.191)), (' L 120  PRO  HG3', ' L 130  ALA  HB1', -0.43, (-28.045, -33.078, -40.636)), (' B  54  ARG  HG2', ' B  58  VAL HG21', -0.429, (19.413, -21.355, -122.16)), (' A 184  VAL HG23', ' A 185  PRO  HD2', -0.429, (12.134, -61.463, -137.827)), (' L 170  ASP  N  ', ' L 170  ASP  OD1', -0.426, (-2.877, -14.694, -34.506)), (' B  27B VAL  O  ', ' B  27B VAL HG22', -0.426, (7.135, -11.307, -111.681)), (' H  88  ALA  HB3', ' H  90  TYR  CE1', -0.426, (-7.92, -16.247, -66.656)), (' C 497  PHE  CE2', ' C 507  PRO  HB3', -0.425, (27.107, -8.609, -79.609)), (' L 129  THR HG22', ' L 130  ALA  N  ', -0.424, (-28.197, -32.107, -45.477)), (' C 466  ARG HH12', ' C 468  ILE HD11', -0.423, (22.903, 8.379, -88.348)), (' A  97  GLY  O  ', ' A 100  THR  OG1', -0.423, (16.088, -18.983, -104.63)), (' H  67  PHE  CD1', ' H  67  PHE  N  ', -0.423, (-7.597, -15.553, -77.452)), (' C 468  ILE  O  ', ' C 468  ILE HG22', -0.422, (21.525, 9.249, -82.772)), (' L 120  PRO  HD3', ' L 132  VAL HG22', -0.421, (-25.551, -32.442, -38.594)), (' B   6  GLN  HB3', ' B   6  GLN HE21', -0.42, (1.623, -24.463, -121.466)), (' L  54  ARG  HE ', ' L  60  ASP  HA ', -0.42, (18.173, -3.622, -50.602)), (' A  37  VAL  C  ', ' A  48  MET  HE2', -0.42, (6.99, -32.637, -104.719)), (' A 201  LYS  N  ', ' A 202  PRO  HD2', -0.418, (12.593, -56.722, -109.296)), (' L  49  TYR  O  ', ' L  53  SER  HB2', -0.418, (17.353, -5.203, -61.062)), (' B 150  VAL  O  ', ' B 150  VAL HG13', -0.418, (-19.886, -60.817, -125.991)), (' H 214  LYS  NZ ', ' L 122  ASP  OD2', -0.417, (-33.826, -27.398, -34.295)), (' A 154  TRP  CZ3', ' A 196  CYS  HB3', -0.416, (10.299, -62.172, -125.72)), (' L  82  ASP  O  ', ' L  86  TYR  OH ', -0.414, (8.193, -12.211, -47.971)), (' A  13  LYS  HG2', ' A  14  PRO  HD2', -0.413, (-1.207, -50.914, -96.469)), (' B 186  TYR  HA ', ' B 192  TYR  OH ', -0.412, (-14.936, -65.332, -122.881)), (' B 108  ARG HH12', ' B 111  ALA  HB2', -0.412, (3.108, -42.817, -139.547)), (' A  59  TYR  HE1', ' A  69  ILE HG13', -0.41, (7.172, -29.804, -95.538)), (' H 100B MET  HB3', ' H 103  TRP  NE1', -0.41, (4.433, -6.968, -62.885)), (' B  33  LEU HD13', ' B  71  PHE  CD2', -0.409, (5.026, -15.32, -117.524)), (' H  67  PHE  HD1', ' H  67  PHE  N  ', -0.409, (-7.918, -15.582, -77.556)), (' C 425  LEU HD23', ' C 426  PRO  HD2', -0.408, (15.097, -4.344, -96.795)), (' B  27D TYR  O  ', ' B  29  ASN  N  ', -0.408, (11.964, -4.735, -111.385)), (' B   6  GLN  HG2', ' B  88  CYS  SG ', -0.407, (2.723, -22.424, -118.233)), (' A 129  LYS  HB3', ' A 129  LYS  HE3', -0.407, (-4.845, -65.264, -141.921)), (' H   9  GLY  HA3', ' H 108  THR  O  ', -0.405, (-13.721, -11.63, -65.237)), (' H 205  THR HG22', ' H 207  VAL HG23', -0.405, (-29.309, -13.919, -48.945)), (' L  61  ARG  NE ', ' L  82  ASP  OD2', -0.404, (11.489, -7.89, -45.334)), (' L 209  PHE  C  ', ' L 209  PHE  CD1', -0.404, (-24.874, -35.727, -31.471)), (' B 131  SER  HA ', ' B 179  LEU  O  ', -0.404, (-7.929, -60.715, -121.263)), (' C 337  PRO  O  ', ' C 340  GLU  N  ', -0.402, (35.439, -3.974, -98.096)), (' H  12  ILE  O  ', ' H 111  VAL  HA ', -0.402, (-17.237, -19.431, -68.849)), (' A 122  PHE  CG ', ' B 124  GLN  HB2', -0.402, (-0.527, -66.556, -119.082)), (' B 207  LYS  HA ', ' B 207  LYS  HD2', -0.401, (-9.145, -59.958, -137.66)), (' B  67  SER  OG ', ' B  68  GLY  N  ', -0.401, (5.158, -7.486, -118.758)), (' A  98  ILE  CG2', ' C 380  TYR  HA ', -0.4, (14.186, -14.139, -100.769))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
