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
data['rama'] = [('C', '  98 ', 'VAL', 0.09625902937596045, (72.58, 32.938, -10.628999999999992))]
data['omega'] = [('B', '  49 ', 'PRO', None, (55.88899999999999, 75.59799999999998, 83.571)), ('D', '  49 ', 'PRO', None, (95.05899999999998, 72.61099999999999, 25.869999999999987)), ('F', '  49 ', 'PRO', None, (104.50499999999995, 6.199, 10.75)), ('H', '  49 ', 'PRO', None, (72.88399999999999, -31.985999999999997, 58.38999999999999)), ('J', '  49 ', 'PRO', None, (42.939, 10.882999999999992, 103.62999999999998))]
data['rota'] = [('A', '  58 ', 'LEU', 0.011827281660234324, (72.62299999999995, 85.188, 52.67799999999997)), ('A', ' 187 ', 'VAL', 0.18969172373270662, (38.694, 48.177, 50.97)), ('A', ' 189 ', 'CYS', 0.10969899476670035, (38.533999999999985, 41.710999999999984, 50.948999999999984)), ('A', ' 312 ', 'THR', 0.10080410126712468, (28.86099999999999, 57.55799999999995, 46.97699999999997)), ('B', '  70 ', 'THR', 0.14083827707199104, (59.89599999999999, 78.328, 79.036)), ('B', '  89 ', 'ASN', 0.22995362732457397, (55.041, 49.18699999999998, 41.893999999999984)), ('C', '   4 ', 'THR', 0.07807749267744926, (119.272, 41.535, -7.443999999999999)), ('C', '  58 ', 'LEU', 0.004386676455714152, (103.38699999999996, 42.838999999999984, 7.401999999999999)), ('C', '  78 ', 'SER', 0.24994761095374968, (97.832, 39.602, 12.932)), ('C', ' 156 ', 'ASN', 0.17736820756998692, (87.97199999999997, 36.248, 13.132999999999997)), ('C', ' 289 ', 'LEU', 0.020116820939085837, (72.549, 24.125, -6.807999999999996)), ('C', ' 312 ', 'THR', 0.19041836809216117, (52.82299999999998, 53.28899999999997, 12.796)), ('D', '   6 ', 'THR', 0.05826404583605509, (101.438, 64.688, 21.969999999999985)), ('D', '  50 ', 'SER', 0.29751686058556065, (90.79499999999996, 73.316, 26.265999999999995)), ('D', '  56 ', 'ASP', 0.03196947957750046, (83.90399999999997, 58.361, 20.33)), ('E', '  58 ', 'LEU', 0.012295057505887956, (89.34099999999997, -21.767999999999986, 27.41799999999999)), ('E', ' 186 ', 'ASN', 0.20915094266595033, (62.225, 17.095, 13.793999999999993)), ('E', ' 189 ', 'CYS', 0.18550078156965316, (60.08299999999998, 23.794, 20.592)), ('E', ' 229 ', 'GLN', 0.2164703804903649, (56.30099999999998, 20.35, 25.919999999999995)), ('F', '  21 ', 'SER', 0.2293748070390891, (91.351, -9.595, 10.946999999999996)), ('F', '  94 ', 'SER', 0.0963454482288407, (68.91899999999998, 16.145, 36.86999999999999)), ('G', '  15 ', 'ASN', 0.27735609291048835, (45.054999999999986, -30.93999999999998, 79.916)), ('G', '  51 ', 'GLU', 0.10000201175579064, (38.476, -29.409, 96.236)), ('G', '  80 ', 'LEU', 0.06486661725618866, (47.97099999999999, -15.698999999999995, 80.152)), ('G', ' 189 ', 'CYS', 0.19853242342065644, (48.742999999999995, 5.740999999999998, 35.255)), ('G', ' 269 ', 'GLN', 0.13185818448901016, (39.379, 11.358999999999993, 70.121)), ('H', '  18 ', 'SER', 0.16581152247142356, (62.328, -27.53, 73.408)), ('H', '  24 ', 'SER', 0.1244568547326317, (57.282000000000004, -22.762999999999987, 63.074999999999974)), ('H', '  50 ', 'SER', 0.058218509226674604, (71.413, -31.01499999999999, 54.418)), ('H', '  94 ', 'SER', 0.18455136299106076, (57.973, 10.447999999999995, 52.919)), ('H', ' 139 ', 'GLU', 0.02695290640236688, (61.38400000000002, -8.539999999999997, 62.791999999999994)), ('I', '  80 ', 'LEU', 0.07503394538977472, (38.11, 46.742, 93.679)), ('I', ' 189 ', 'CYS', 0.13220284726120335, (36.73599999999997, 16.640999999999984, 54.43099999999998))]
data['cbeta'] = []
data['probe'] = [(' A 263  GLU  OE1', ' A 296  TYR  OH ', -0.604, (49.718, 62.888, 23.604)), (' B   6  THR  HB ', ' B  70  THR HG23', -0.58, (62.451, 78.994, 79.199)), (' E  82  ARG  NH2', ' E 153  ALA  O  ', -0.57, (78.1, -12.929, 28.475)), (' B  47  VAL HG22', ' B  65  LEU HD21', -0.567, (54.232, 76.432, 75.764)), (' C  98  VAL  O  ', ' C  98  VAL HG12', -0.556, (70.289, 33.741, -10.169)), (' C 185  LEU HD21', ' C 216  PHE  CZ ', -0.536, (61.236, 46.695, 16.668)), (' C  98  VAL HG13', ' C 290  LEU HD22', -0.519, (70.156, 30.746, -10.26)), (' G 166  ARG  HA ', ' G 243  MET  HE1', -0.517, (38.902, -3.629, 59.886)), (' G  62  ASP  OD1', ' G  65  ARG  NH1', -0.5, (60.49, -25.697, 79.56)), (' I  33  PRO  HG2', ' I  58  LEU HD12', -0.496, (44.327, 49.437, 99.03)), (' G  82  ARG  NH2', ' G 153  ALA  O  ', -0.489, (47.991, -10.185, 74.191)), (' B  99  ARG  O  ', ' B 102  GLN  HG2', -0.479, (68.173, 53.33, 61.157)), (' I 119  THR HG21', ' I 304  PHE  CZ ', -0.479, (25.674, 40.208, 71.291)), (' G 210  THR HG21', ' G 220  VAL HG11', -0.476, (37.18, 1.989, 45.688)), (' B  55  GLN  CB ', ' B  58  VAL HG12', -0.472, (49.531, 73.014, 67.611)), (' C 178  LEU  O  ', ' C 201  GLY  HA2', -0.471, (73.326, 52.747, 12.476)), (' G 173  PHE  HB3', ' G 202  VAL HG12', -0.47, (44.219, -10.803, 57.965)), (' C 286  ASP  HB3', ' C 289  LEU  HB3', -0.467, (71.321, 23.972, -3.824)), (' C 253  LEU  HB3', ' C 258  PHE  CE1', -0.466, (59.608, 34.615, 0.732)), (' E  10  THR HG21', ' E  13  ASN  HA ', -0.465, (84.175, -27.12, 18.515)), (' C 158  THR HG22', ' C 159  VAL  O  ', -0.46, (89.786, 27.565, 8.536)), (' G  69  PHE  CE1', ' H  27  GLU  HG2', -0.455, (54.682, -20.773, 68.437)), (' B  55  GLN  HB2', ' B  58  VAL HG12', -0.455, (49.649, 73.471, 67.93)), (' G  97  GLN  NE2', ' G 102  THR  OG1', -0.454, (25.136, -15.284, 70.678)), (' F  82  LEU HD12', ' F  84  ILE HG23', -0.452, (80.125, 14.678, 33.102)), (' I 255  HIS  HA ', ' I 282  LEU HD11', -0.451, (14.064, 43.346, 61.02)), (' B  86  VAL  HA ', ' B 148  VAL  O  ', -0.448, (57.205, 50.389, 51.433)), (' J   5  LEU HD11', ' J  65  LEU HD22', -0.447, (39.789, 19.483, 101.762)), (' E 124  GLU  HB3', ' E 240  PRO  HB2', -0.446, (64.791, -5.809, 7.767)), (' C 119  THR HG21', ' C 304  PHE  CZ ', -0.443, (71.174, 39.155, 5.004)), (' H  25  VAL HG11', ' H  56  ASP  HA ', -0.442, (60.328, -19.617, 58.767)), (' C  62  ASP  O  ', ' C  66  VAL HG23', -0.438, (102.298, 55.16, 8.979)), (' C  87  LEU  O  ', ' C  91  LYS  HG2', -0.437, (92.83, 32.406, -2.331)), (' J  28  LEU HD22', ' J  60  LEU HD21', -0.434, (40.225, 23.137, 97.381)), (' B  82  LEU HD23', ' B  98  VAL  O  ', -0.431, (64.544, 49.623, 62.675)), (' B  55  GLN  HB2', ' B  58  VAL  CG1', -0.431, (49.553, 73.756, 68.094)), (' G 276  ILE  N  ', ' G 276  ILE HD12', -0.43, (25.594, -1.58, 61.426)), (' H   9  MET  HB3', ' H   9  MET  HE2', -0.429, (77.348, -20.036, 66.676)), (' H  25  VAL  CG1', ' H  56  ASP  HA ', -0.428, (59.855, -19.879, 59.054)), (' F  79  ASP  O  ', ' F  99  ARG  NH1', -0.428, (89.052, 13.932, 38.148)), (' I 181  CYS  HA ', ' I 238  GLU  O  ', -0.427, (23.11, 24.554, 75.431)), (' A  97  GLN  HA ', ' A 101  LEU  O  ', -0.426, (49.98, 80.878, 27.843)), (' H  86  VAL  HA ', ' H 148  VAL  O  ', -0.424, (55.049, 4.301, 55.273)), (' H  48  HIS  HA ', ' H  49  PRO  HA ', -0.424, (73.146, -29.587, 57.968)), (' G  10  THR HG21', ' G  13  ASN  HA ', -0.424, (42.399, -26.101, 81.915)), (' C 166  ARG  HA ', ' C 243  MET  HE1', -0.42, (72.26, 37.746, 10.814)), (' J  80  GLU  HG2', ' J  81  PRO  HD2', -0.42, (61.862, 19.229, 77.33)), (' F 114  LEU  C  ', ' F 114  LEU HD23', -0.419, (66.687, 11.815, 43.087)), (' E  23  MET  HE3', ' E  46  PRO  O  ', -0.419, (88.483, -42.427, 30.544)), (' H 132  GLU  HB2', ' H 135  LEU HD12', -0.415, (55.629, -6.276, 68.197)), (' C  26  THR  OG1', ' C  29  GLN  HG3', -0.414, (115.093, 34.528, 4.434)), (' F  86  VAL  HA ', ' F 148  VAL  O  ', -0.414, (70.692, 10.505, 31.822)), (' G 263  GLU  O  ', ' G 273  TYR  HA ', -0.414, (30.092, 2.617, 64.892)), (' J  27  GLU  O  ', ' J  31  GLN  HG2', -0.413, (43.177, 29.921, 96.69)), (' I 255  HIS  HB2', ' I 282  LEU HD13', -0.413, (12.598, 44.379, 60.282)), (' F  10  LEU  HA ', ' F  10  LEU HD23', -0.412, (106.249, 9.607, 22.132)), (' F  58  VAL  CG2', ' F  59  PRO  HD2', -0.411, (86.623, -2.095, 9.015)), (' D 114  LEU  C  ', ' D 114  LEU HD23', -0.411, (72.679, 29.195, 34.764)), (' E  10  THR  O  ', ' E  56  TYR  HA ', -0.411, (86.127, -25.881, 22.858)), (' D  86  VAL  HA ', ' D 148  VAL  O  ', -0.407, (72.864, 39.364, 29.191)), (' H 134  GLN  CD ', ' H 134  GLN  H  ', -0.406, (56.414, -3.338, 71.6)), (' I 136  TYR  OH ', ' I 140  ARG  NH2', -0.405, (19.234, 39.027, 80.631)), (' I 250  GLN  HB3', ' I 297  LYS  HE3', -0.404, (26.326, 45.22, 51.977)), (' I 128  ASN  HB2', ' I 129  PRO  HD3', -0.401, (29.416, 33.402, 87.83)), (' C  58  LEU  HA ', ' C  58  LEU HD22', -0.401, (101.732, 42.343, 7.651)), (' G  99  ASN  HB3', ' G 279  LYS  HE2', -0.401, (19.462, -13.021, 61.882)), (' D 152  LEU  HA ', ' D 152  LEU HD23', -0.4, (73.336, 29.865, 21.855))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
