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
data['rama'] = [('A', ' 372 ', 'ALA', 0.010154322231765309, (-27.663, -18.093, 23.248)), ('A', ' 373 ', 'SER', 0.028879012059098784, (-26.753, -16.571, 26.643)), ('F', ' 126 ', 'PRO', 0.0560290276154372, (-72.809, 62.726, 32.613))]
data['omega'] = [('C', ' 147 ', 'PRO', None, (-66.661, 7.990000000000001, 60.05699999999999)), ('C', ' 149 ', 'PRO', None, (-71.498, 11.493, 58.189)), ('D', '   8 ', 'PRO', None, (-101.656, 5.285, 60.657)), ('D', '  95 ', 'PRO', None, (-91.767, 13.53, 79.145)), ('D', ' 141 ', 'PRO', None, (-93.125, 1.086, 40.10299999999999)), ('F', ' 147 ', 'PRO', None, (-66.133, 56.087, 4.8)), ('F', ' 149 ', 'PRO', None, (-62.413, 53.413, 9.000999999999996)), ('G', '   8 ', 'PRO', None, (-72.289, 24.107, 19.67)), ('G', '  95 ', 'PRO', None, (-70.252, 23.720999999999997, -2.794)), ('G', ' 141 ', 'PRO', None, (-73.354, 37.082, 31.954)), ('H', ' 147 ', 'PRO', None, (-57.589, -22.977, 78.817)), ('H', ' 149 ', 'PRO', None, (-52.539, -19.397999999999993, 79.56399999999996)), ('L', '   8 ', 'PRO', None, (-24.031000000000002, -26.625, 68.702)), ('L', '  95 ', 'PRO', None, (-38.686, -18.11, 53.687)), ('L', ' 141 ', 'PRO', None, (-26.963, -30.343999999999998, 90.245))]
data['rota'] = [('A', ' 354 ', 'ASN', 0.04909833906556253, (-30.188999999999993, 3.639, 33.573)), ('A', ' 366 ', 'SER', 0.04229168834138839, (-33.976, -11.433000000000002, 16.219)), ('A', ' 367 ', 'VAL', 0.10586643079740182, (-30.158, -11.170000000000003, 16.418)), ('A', ' 368 ', 'LEU', 0.14072621531683557, (-30.706, -10.374, 20.142999999999994)), ('A', ' 371 ', 'SER', 0.28003810876641116, (-27.989000000000004, -14.867, 21.163)), ('A', ' 408 ', 'ARG', 0.0, (-39.433000000000014, -12.385, 38.673999999999985)), ('A', ' 441 ', 'LEU', 0.06899553531598356, (-18.282, -9.602, 36.379999999999995)), ('A', ' 458 ', 'LYS', 0.0, (-43.098, 5.447, 52.327)), ('B', ' 354 ', 'ASN', 0.04791509236645353, (-104.59700000000001, 35.979, 96.186)), ('B', ' 359 ', 'SER', 0.21165371707743294, (-104.513, 39.124, 112.41999999999997)), ('B', ' 385 ', 'THR', 0.008159601566148922, (-99.922, 18.826, 115.52299999999998)), ('B', ' 430 ', 'THR', 0.2501585178829203, (-92.164, 28.391, 107.99)), ('B', ' 441 ', 'LEU', 0.04408502917150219, (-115.938, 23.037, 90.335)), ('B', ' 514 ', 'SER', 0.15368495596217566, (-97.343, 31.811999999999998, 105.95599999999997)), ('C', '  29 ', 'VAL', 0.18037985540812523, (-81.552, 32.417, 73.39199999999997)), ('C', '  53 ', 'SER', 0.17593857600477783, (-85.28, 31.543000000000003, 80.166)), ('C', ' 107 ', 'THR', 0.0816172427615017, (-75.196, 16.915, 64.138)), ('C', ' 138 ', 'LEU', 0.1966714922803622, (-72.571, 10.703999999999997, 35.095)), ('C', ' 140 ', 'CYS', 0.1151280139128252, (-69.304, 10.071000000000002, 41.674)), ('C', ' 183 ', 'THR', 0.0781823012773522, (-78.771, 12.964999999999996, 34.401)), ('C', ' 189 ', 'LEU', 0.003264066659929189, (-71.463, 16.833, 27.567)), ('C', ' 193 ', 'THR', 0.19614443367827517, (-68.237, 20.96999999999999, 33.031)), ('C', ' 196 ', 'CYS', 0.08954517143437239, (-68.797, 16.74, 42.198)), ('D', '  14 ', 'SER', 0.28047228555619963, (-102.314, 8.893, 44.832999999999984)), ('D', '  24 ', 'ARG', 0.24734962726152449, (-104.213, 8.591, 70.266)), ('D', '  65 ', 'SER', 0.14071771227658755, (-108.266, 18.391, 64.684)), ('D', '  77 ', 'SER', 0.05914531237945127, (-105.289, 17.201, 48.387)), ('D', '  81 ', 'GLU', 0.21712817594435876, (-93.924, 17.287000000000003, 47.711)), ('D', ' 104 ', 'LEU', 0.2711805644846768, (-96.43600000000002, 8.661, 53.640999999999984)), ('D', ' 106 ', 'ILE', 0.13442510976159963, (-97.25400000000002, 8.761999999999999, 46.785)), ('D', ' 129 ', 'THR', 0.08785590227407147, (-59.908, -2.588, 43.264)), ('E', ' 347 ', 'PHE', 0.07433267633270743, (-62.61, -3.631, -11.569)), ('E', ' 354 ', 'ASN', 0.04634083156053655, (-57.887, -0.993, -17.700999999999993)), ('E', ' 394 ', 'ASN', 0.1374831007171981, (-59.698, -2.5029999999999997, -33.678)), ('E', ' 405 ', 'ASP', 0.17761539068610213, (-70.954, 13.123, -9.869999999999996)), ('E', ' 430 ', 'THR', 0.20739625739926462, (-66.208, 8.138, -31.792999999999992)), ('E', ' 443 ', 'SER', 0.05472153944110148, (-68.971, -0.045, -1.046)), ('E', ' 495 ', 'TYR', 0.24146909088064625, (-62.403000000000006, 6.867000000000002, -2.569)), ('E', ' 523 ', 'THR', 0.02962945003546535, (-61.17300000000001, -7.402999999999999, -37.755)), ('F', '  29 ', 'VAL', 0.2514245788722297, (-49.026, 28.646, -7.546)), ('F', '  35 ', 'SER', 0.17704510527339237, (-59.052, 29.061999999999998, -3.766999999999999)), ('F', '  66 ', 'ARG', 0.2166982034587954, (-69.221, 37.846, -12.712)), ('F', '  68 ', 'THR', 0.15307491988305397, (-62.952000000000005, 35.329, -13.132)), ('F', ' 100A', 'ARG', 0.030720176406891876, (-59.215, 16.178, 2.1759999999999993)), ('F', ' 138 ', 'LEU', 0.17615285672326397, (-69.826, 59.906000000000006, 29.859999999999992)), ('F', ' 183 ', 'THR', 0.06388432408756724, (-66.509, 55.362, 33.361)), ('F', ' 189 ', 'LEU', 0.0018553204132398485, (-66.268, 65.366, 37.532)), ('F', ' 196 ', 'CYS', 0.2016237961281338, (-62.92, 62.964, 23.13)), ('G', '   9 ', 'SER', 0.17981977058991958, (-73.404, 28.81400000000001, 18.704)), ('G', '  24 ', 'ARG', 0.00982368092272232, (-73.522, 17.508, 11.656999999999996)), ('G', '  33 ', 'LEU', 0.22584858227766955, (-64.305, 17.78, 6.865)), ('G', '  65 ', 'SER', 0.15116496823776587, (-63.227, 12.666999999999996, 15.440999999999997)), ('G', '  77 ', 'SER', 0.05706972904358228, (-57.099000000000004, 21.551, 28.258)), ('G', '  81 ', 'GLU', 0.07515020244671192, (-54.823, 31.522, 23.324)), ('G', ' 105 ', 'GLU', 0.005621967819063891, (-65.685, 32.521, 25.312)), ('H', '  29 ', 'VAL', 0.2350890182480128, (-46.173, 0.985, 61.973)), ('H', '  53 ', 'SER', 0.005359990245779045, (-44.467, 0.23, 54.276)), ('H', ' 117 ', 'LYS', 0.24013686927088035, (-62.123, -23.983999999999995, 82.706)), ('H', ' 138 ', 'LEU', 0.18665568154821463, (-45.30700000000001, -21.355999999999995, 101.443)), ('H', ' 140 ', 'CYS', 0.24942939537911632, (-50.242, -21.813, 95.98)), ('H', ' 183 ', 'THR', 0.016319203132297844, (-39.273, -18.752, 100.589)), ('H', ' 196 ', 'CYS', 0.07076833623387244, (-50.92300000000001, -15.059, 95.987)), ('L', '   9 ', 'SER', 0.15565966230579054, (-28.206, -28.72, 70.246)), ('L', '  11 ', 'LEU', 0.0, (-24.031000000000002, -27.099, 75.695)), ('L', '  24 ', 'ARG', 0.09223353291233682, (-24.297000000000004, -23.574999999999992, 58.65999999999998)), ('L', '  65 ', 'SER', 0.17036378062905852, (-18.423, -13.901999999999996, 62.62099999999999)), ('L', '  67 ', 'SER', 0.24742963450418576, (-20.049, -14.901, 55.696)), ('L', '  77 ', 'SER', 0.061539596527854463, (-16.813000000000002, -14.520000000000001, 79.155)), ('L', '  81 ', 'GLU', 0.17434275605608246, (-27.595000000000006, -14.353999999999997, 83.082)), ('L', ' 105 ', 'GLU', 0.20179479379477888, (-26.717, -24.29, 80.443)), ('L', ' 129 ', 'THR', 0.01495926990173757, (-59.585, -34.67299999999999, 96.309))]
data['cbeta'] = []
data['probe'] = [(' H 129  LYS  NZ ', ' L 207  LYS  HZ2', -0.824, (-38.503, -29.874, 107.22)), (' H 129  LYS  NZ ', ' L 207  LYS  NZ ', -0.8, (-37.263, -29.657, 107.046)), (' F  36  TRP  CD1', ' F  69  ILE HD12', -0.769, (-59.892, 33.344, -7.097)), (' F 126  PRO  HD2', ' F 213  PRO  HA ', -0.747, (-71.584, 65.881, 31.443)), (' H 129  LYS  HZ1', ' L 207  LYS  NZ ', -0.734, (-38.069, -30.755, 107.387)), (' C 190  GLY  HA3', ' G  20  THR  HB ', -0.706, (-68.77, 18.753, 23.918)), (' E 436  TRP  HE1', ' E 509  ARG  HB2', -0.691, (-69.869, -1.596, -12.77)), (' E 436  TRP  NE1', ' E 509  ARG  HB2', -0.673, (-70.586, -1.254, -13.204)), (' H 129  LYS  HZ1', ' L 207  LYS  HZ2', -0.662, (-38.239, -30.369, 107.388)), (' F 184  VAL HG21', ' F 194  TYR  OH ', -0.652, (-63.246, 61.848, 35.022)), (' E 360  ASN  ND2', ' E 523  THR  OG1', -0.643, (-59.085, -9.663, -37.182)), (' F 184  VAL  CG2', ' F 185  PRO  HD2', -0.641, (-62.959, 58.768, 37.038)), (' C  11  LEU  HB2', ' C 147  PRO  HG3', -0.638, (-66.461, 9.45, 63.592)), (' L  78  LEU HD11', ' L 104  LEU HD21', -0.636, (-23.383, -19.264, 77.345)), (' D  37  GLN  HB2', ' D  47  LEU HD11', -0.631, (-95.952, 17.554, 57.95)), (' F  36  TRP  HD1', ' F  69  ILE HD12', -0.629, (-59.419, 32.428, -6.759)), (' F  66  ARG  NH1', ' F  86  ASP  OD2', -0.602, (-71.221, 40.839, -7.102)), (' E 354  ASN  O  ', ' E 398  ASP  HA ', -0.571, (-59.734, 0.014, -20.153)), (' H 129  LYS  HZ2', ' L 207  LYS  HZ2', -0.565, (-38.086, -29.252, 107.247)), (' F 184  VAL HG23', ' F 185  PRO  HD2', -0.561, (-62.878, 59.177, 36.573)), (' A 354  ASN  O  ', ' A 398  ASP  HA ', -0.555, (-32.434, 2.231, 31.593)), (' H 143  LYS  NZ ', ' H 171  GLN HE22', -0.546, (-55.723, -32.115, 88.683)), (' E 388  ASN  ND2', ' E 528  LYS  NZ ', -0.541, (-75.567, -6.897, -37.459)), (' A 366  SER  H  ', ' A 388  ASN  ND2', -0.541, (-34.473, -9.397, 14.396)), (' B 354  ASN  O  ', ' B 398  ASP  HA ', -0.534, (-102.677, 34.04, 98.713)), (' B 360  ASN  H  ', ' B 523  THR  HB ', -0.531, (-103.735, 39.874, 115.609)), (' E 350  VAL HG22', ' E 422  ASN  HB3', -0.525, (-59.422, 8.738, -13.853)), (' C 143  LYS  NZ ', ' C 171  GLN HE22', -0.513, (-65.832, -1.062, 49.329)), (' L  37  GLN  HB2', ' L  47  LEU HD11', -0.512, (-28.521, -13.468, 72.517)), (' H 129  LYS  NZ ', ' L 207  LYS  HZ3', -0.51, (-37.004, -30.422, 107.614)), (' G  37  GLN  HB2', ' G  47  LEU HD11', -0.507, (-58.491, 26.16, 15.615)), (' B 387  LEU HD12', ' B 390  LEU HD12', -0.505, (-97.628, 25.963, 114.395)), (' H   6  GLU  OE2', ' H 104  GLY  HA3', -0.497, (-45.672, -8.29, 70.669)), (' F 119  PRO  HB3', ' F 145  TYR  HB3', -0.496, (-68.106, 60.038, 10.851)), (' F 143  LYS  NZ ', ' F 171  GLN HE22', -0.492, (-77.545, 57.88, 11.873)), (' E 486  PHE  HZ ', ' F   2  VAL HG21', -0.49, (-45.414, 26.251, 2.669)), (' A 455  LEU HD22', ' A 493  GLN  HG3', -0.488, (-32.152, -2.766, 53.626)), (' F 159  LEU HD21', ' F 182  VAL HG21', -0.488, (-62.191, 58.7, 30.559)), (' A 417  LYS  HD3', ' A 455  LEU HD12', -0.488, (-35.992, -3.902, 51.516)), (' H 159  LEU HD21', ' H 182  VAL HG21', -0.488, (-42.634, -14.566, 98.706)), (' C 191  THR  HA ', ' G  11  LEU HD11', -0.487, (-69.185, 23.322, 25.717)), (' C  97  VAL  HB ', ' D  96  GLY  HA3', -0.486, (-92.172, 17.326, 74.755)), (' E 418  ILE  HA ', ' E 422  ASN  HB2', -0.486, (-60.285, 11.62, -13.309)), (' C 159  LEU HD21', ' C 182  VAL HG21', -0.485, (-76.001, 17.126, 36.96)), (' L  34  ALA  HB2', ' L  91  LEU HD11', -0.485, (-30.72, -11.243, 61.002)), (' F 138  LEU  HB2', ' F 211  VAL HG11', -0.484, (-69.308, 62.768, 28.843)), (' B 385  THR  HB ', ' B 386  LYS  HZ2', -0.483, (-97.725, 17.521, 116.888)), (' B 377  PHE  CE1', ' B 434  ILE HG12', -0.48, (-103.585, 22.006, 105.635)), (' B 350  VAL HG22', ' B 422  ASN  HB3', -0.471, (-98.631, 30.681, 89.795)), (' D  15  VAL HG23', ' D 106  ILE HG21', -0.471, (-98.647, 12.073, 44.18)), (' G 134  CYS  HB2', ' G 148  TRP  CH2', -0.467, (-80.728, 53.377, 25.763)), (' A 383  SER  HB2', ' A 386  LYS  HZ3', -0.467, (-45.713, -12.648, 18.254)), (' A 431  GLY  HA2', ' A 515  PHE  HD1', -0.466, (-41.534, -4.033, 24.069)), (' A 350  VAL HG22', ' A 422  ASN  HB3', -0.46, (-34.875, -0.989, 41.703)), (' H  87  THR HG23', ' H 110  THR  HA ', -0.46, (-53.239, -23.565, 71.168)), (' B 455  LEU HD22', ' B 493  GLN  HG3', -0.459, (-97.509, 29.013, 77.149)), (' D  78  LEU HD11', ' D 104  LEU HD21', -0.459, (-98.855, 12.374, 50.437)), (' B 385  THR  HB ', ' B 386  LYS  NZ ', -0.455, (-98.308, 17.254, 117.097)), (' E 417  LYS  HD3', ' E 455  LEU HD12', -0.454, (-58.454, 16.292, -6.464)), (' B 417  LYS  HD3', ' B 455  LEU HD12', -0.45, (-94.628, 27.386, 80.399)), (' F  87  THR HG23', ' F 110  THR  HA ', -0.449, (-67.581, 46.384, 1.085)), (' D 134  CYS  HB2', ' D 148  TRP  CZ2', -0.448, (-74.806, -2.601, 37.878)), (' D  34  ALA  HB2', ' D  91  LEU HD11', -0.448, (-96.897, 20.765, 69.748)), (' F 184  VAL HG22', ' F 188  SER  OG ', -0.445, (-63.756, 60.66, 37.24)), (' A 347  PHE  CD2', ' A 509  ARG  HG2', -0.444, (-26.128, -5.218, 33.769)), (' C  87  THR HG23', ' C 110  THR  HA ', -0.444, (-72.992, 7.614, 66.089)), (' G  34  ALA  HB2', ' G  91  LEU HD11', -0.443, (-61.019, 20.548, 5.878)), (' D 163 AVAL HG22', ' D 175  LEU HD12', -0.443, (-83.363, -0.013, 44.554)), (' A 383  SER  HB2', ' A 386  LYS  NZ ', -0.44, (-45.259, -12.715, 18.487)), (' F 184  VAL HG22', ' F 185  PRO  HD2', -0.44, (-63.558, 59.468, 37.091)), (' L 163 AVAL HG22', ' L 175  LEU HD12', -0.436, (-37.672, -31.139, 88.47)), (' E 393  THR HG21', ' E 518  LEU  HB2', -0.436, (-56.357, -0.506, -38.689)), (' H 143  LYS  HZ3', ' H 171  GLN HE22', -0.429, (-55.69, -31.789, 89.103)), (' E 388  ASN  CG ', ' E 528  LYS  HZ2', -0.428, (-74.795, -6.354, -37.208)), (' L 199  GLN  HB2', ' L 302  HOH  O  ', -0.421, (-27.168, -35.374, 91.387)), (' G  78  LEU HD21', ' G 104  LEU HD21', -0.42, (-61.807, 26.33, 23.889)), (' A 458 BLYS  H  ', ' A 458 BLYS  HG3', -0.42, (-41.034, 6.892, 51.445)), (' G 163 AVAL HG22', ' G 175  LEU HD12', -0.42, (-74.666, 44.021, 23.402)), (' E 486  PHE  HZ ', ' F   2  VAL  CG2', -0.419, (-45.314, 26.793, 2.823)), (' C 190  GLY  CA ', ' G  20  THR  HB ', -0.418, (-68.071, 18.712, 24.654)), (' F 143  LYS  HZ3', ' F 171  GLN HE22', -0.417, (-77.256, 58.146, 12.29)), (' E 377  PHE  CE2', ' E 379  CYS  SG ', -0.415, (-74.187, 3.794, -26.982)), (' A 704  HOH  O  ', ' L  68  GLY  HA2', -0.414, (-21.904, -16.26, 51.165)), (' C 143  LYS  HZ3', ' C 171  GLN HE22', -0.413, (-65.713, -0.361, 49.179)), (' F  82  MET  HB3', ' F  82C LEU HD21', -0.411, (-66.493, 41.757, -7.337)), (' E 444  LYS  O  ', ' E 498  GLN  OE1', -0.41, (-68.026, 0.303, 3.772)), (' C  82  MET  HB3', ' C  82C LEU HD21', -0.409, (-73.012, 12.164, 75.083)), (' F  36  TRP  CD1', ' F  69  ILE  CD1', -0.407, (-58.828, 32.57, -7.249)), (' E 499  PRO  HB3', ' E 719  HOH  O  ', -0.407, (-74.938, 0.445, 0.361)), (' H 144  ASP  HB3', ' H 175  LEU HD13', -0.407, (-59.425, -29.006, 85.712)), (' H  11  LEU  HB2', ' H 147  PRO  HG3', -0.405, (-58.214, -21.564, 75.339)), (' H  97  VAL  HB ', ' L  96  GLY  HA3', -0.404, (-36.921, -14.32, 57.628)), (' G 134  CYS  HB2', ' G 148  TRP  CZ2', -0.404, (-80.885, 52.979, 25.664)), (' C  36  TRP  HD1', ' C  69  ILE HD12', -0.403, (-80.56, 21.413, 75.815)), (' F  29  VAL HG22', ' F  34  MET  HE2', -0.402, (-50.821, 30.731, -5.537)), (' E 360 AASN  H  ', ' E 523  THR HG23', -0.402, (-60.31, -8.156, -34.7)), (' F 144  ASP  HB3', ' F 175  LEU HD13', -0.401, (-74.117, 60.046, 7.784)), (' E 360 BASN  H  ', ' E 523  THR HG23', -0.401, (-60.309, -8.158, -34.701))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
