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
data['omega'] = []
data['rota'] = [('A', '  21 ', 'GLN', 0.0, (-0.17700000000000005, 12.137000000000004, 129.366)), ('A', '  34 ', 'LEU', 0.03684776443876307, (9.74, 9.837000000000003, 108.69)), ('A', ' 118 ', 'GLN', 0.09157428903605445, (-7.116, 20.669000000000004, 99.707)), ('A', ' 148 ', 'GLU', 0.21660681311171118, (-15.476999999999997, 2.068, 114.58500000000001)), ('A', ' 156 ', 'CYS', 0.0711001394253666, (-15.713999999999997, 19.651, 113.79100000000001)), ('A', ' 158 ', 'SER', 0.09593111813990263, (-11.015, 23.015000000000008, 109.903)), ('C', ' 184 ', 'LEU', 0.0, (-7.133000000000002, 5.746, 107.19)), ('B', '  34 ', 'LEU', 0.014437426711882707, (-31.725, 8.568000000000003, 145.204)), ('B', '  87 ', 'GLU', 0.010860036149967884, (-34.736, 20.662, 135.595)), ('B', ' 156 ', 'CYS', 0.07277358024936603, (-7.063, -2.9170000000000007, 139.324)), ('E', '  42P', 'CYS', 0.1168535734693542, (-8.168, 9.224000000000004, 134.878)), ('F', '  42P', 'CYS', 0.07322877645492554, (-8.956, 16.980000000000008, 124.747))]
data['cbeta'] = [('E', '  42P', 'CYS', ' ', 0.763671479959443, (-9.203, 8.887, 136.09)), ('E', '  43P', 'DAR', ' ', 1.81076523736268, (-3.6770000000000014, 9.880000000000004, 136.129)), ('F', '  42P', 'CYS', ' ', 0.8286375833244453, (-7.9430000000000005, 17.136000000000006, 123.475)), ('F', '  43P', 'DAR', ' ', 1.8208989622840925, (-9.906, 20.999000000000006, 127.291)), ('G', '  43P', 'DAR', ' ', 2.333511054731427, (-1.1889999999999998, 20.695000000000007, 122.275)), ('H', '  43P', 'DAR', ' ', 2.3178661158109066, (-11.756000000000004, 12.706, 142.297))]
data['probe'] = [(' E  43P DAR  CD ', ' E  43P DAR  NE ', -1.544, (-1.316, 7.699, 134.666)), (' F  43P DAR  CD ', ' F  43P DAR  NE ', -1.534, (-12.386, 22.684, 126.347)), (' B  22  CYS  SG ', ' B  65  CYS  SG ', -1.296, (-16.688, 19.827, 137.686)), (' A 156  CYS  SG ', ' C 209  CYS  SG ', -1.266, (-13.506, 17.342, 112.106)), (' E  43P DAR  CD ', ' E  43P DAR  CZ ', -0.879, (-1.064, 8.776, 136.324)), (' A  56  CYS  SG ', ' A  98  CYS  SG ', -0.848, (17.828, 17.376, 121.49)), (' F  42P CYS  SG ', ' G  42P CYS  SG ', -0.838, (-7.233, 16.342, 121.615)), (' B 147  LYS  HE2', ' B 490  HOH  O  ', -0.833, (-11.895, -1.911, 120.686)), (' F  43P DAR  CD ', ' F  43P DAR  CZ ', -0.829, (-12.386, 23.431, 126.747)), (' E  42P CYS  SG ', ' H  42P CYS  SG ', -0.773, (-11.84, 7.923, 136.182)), (' A  22  CYS  SG ', ' A  65  CYS  SG ', -0.772, (5.156, 16.206, 126.524)), (' A 397  HOH  O  ', ' C 219  THR HG21', -0.77, (11.559, 19.029, 99.954)), (' B  56  CYS  SG ', ' B  98  CYS  SG ', -0.734, (-25.604, 25.557, 147.896)), (' B 156  CYS  SG ', ' D 209  CYS  SG ', -0.711, (-9.852, -3.114, 138.49)), (' A  21  GLN  HG2', ' A 344  HOH  O  ', -0.685, (1.289, 9.862, 130.41)), (' D 206  ARG  NH2', ' D 728  HOH  O  ', -0.659, (-7.598, -11.928, 140.037)), (' B   3  ARG  HG3', ' B 172  PHE  CE1', -0.64, (-28.417, -15.642, 134.99)), (' A 147  LYS  HD2', ' A 357  HOH  O  ', -0.616, (-17.895, 3.769, 122.186)), (' A 162  ASP  O  ', ' G  42P CYS  HB3', -0.593, (-4.222, 18.255, 119.725)), (' D 192  GLU  HG2', ' D 752  HOH  O  ', -0.591, (-21.996, 10.71, 124.269)), (' B   7  TRP  CE2', ' B 130  GLY  HA2', -0.529, (-33.196, -2.546, 142.287)), (' C 192  GLU  HG3', ' C 813  HOH  O  ', -0.524, (-6.217, -0.281, 126.441)), (' A 147  LYS  NZ ', ' A 357  HOH  O  ', -0.52, (-18.186, 2.696, 122.661)), (' A   3  ARG  HG3', ' A   3  ARG HH11', -0.516, (-11.991, 2.568, 92.183)), (' A 151  TYR  HB3', ' C 201  MET  HG3', -0.497, (-12.82, 9.986, 111.47)), (' C 219  THR HG22', ' C 399  HOH  O  ', -0.494, (10.305, 16.703, 99.596)), (' A 168  VAL  CG2', ' C 184  LEU HD13', -0.49, (-3.884, 3.106, 107.354)), (' B 141  GLU  HG3', ' B 586  HOH  O  ', -0.486, (-3.459, 3.313, 131.464)), (' A 103  LYS  HE2', ' A 630  HOH  O  ', -0.481, (27.755, 6.302, 121.094)), (' A 447  HOH  O  ', ' D 192  GLU  HB2', -0.478, (-20.023, 9.384, 125.2)), (' A 168  VAL HG23', ' C 184  LEU HD13', -0.478, (-3.934, 3.086, 107.09)), (' A  34  LEU HD22', ' A  38  MET  HG2', -0.47, (12.77, 9.213, 107.676)), (' B  74  PHE  CZ ', ' D 218  PRO  HD3', -0.463, (-27.944, 6.67, 147.929)), (' A 108  ASN  ND2', ' A 109  ASP  H  ', -0.462, (17.627, 14.548, 107.756)), (' B  10  LYS  HE2', ' B 775  HOH  O  ', -0.461, (-37.966, -6.548, 139.17)), (' A  69  LEU HD12', ' A  72  TYR  CE2', -0.461, (5.966, 25.186, 114.489)), (' D 204  ASP  HB2', ' D 541  HOH  O  ', -0.46, (-19.768, -12.943, 142.277)), (' B 162  ASP  O  ', ' H  42P CYS  HB3', -0.449, (-12.345, 8.753, 140.464)), (' A   7  TRP  CE2', ' A 130  GLY  HA2', -0.448, (2.296, 5.795, 100.573)), (' A  52  ASN  C  ', ' A  52  ASN HD22', -0.447, (15.016, 14.294, 119.883)), (' C 205  ARG  HG3', ' C 205  ARG HH11', -0.446, (-19.002, 12.631, 105.035)), (' D 206  ARG  CZ ', ' D 728  HOH  O  ', -0.441, (-8.211, -11.957, 141.039)), (' B  67  GLY  HA2', ' H  43P DAR  O  ', -0.431, (-14.753, 13.839, 143.75)), (' A  21  GLN  H  ', ' A  21  GLN  HG2', -0.43, (0.428, 9.625, 130.23)), (' D 193  TRP  CH2', ' D 199  VAL  HB ', -0.427, (-18.007, 1.327, 131.397)), (' B   3  ARG  CG ', ' B 172  PHE  CE1', -0.421, (-28.482, -16.225, 135.493)), (' B  34  LEU HD22', ' B  38  MET  HG2', -0.418, (-34.576, 10.017, 146.419)), (' A 103  LYS  NZ ', ' A 443  HOH  O  ', -0.417, (29.405, 3.472, 122.103)), (' A 160  ASP  O  ', ' A 161  MET  C  ', -0.416, (-7.134, 22.396, 116.399)), (' A  67  GLY  HA2', ' G  43P DAR  O  ', -0.414, (1.821, 20.372, 121.147)), (' B 146  TYR  CZ ', ' D 199  VAL HG23', -0.408, (-17.755, -2.11, 130.499)), (' A  58  GLY  N  ', ' A  59  PRO  CD ', -0.407, (14.675, 22.994, 120.496)), (' A  18  ASN  OD1', ' F  41P BP4  H11', -0.407, (-1.475, 6.531, 125.565)), (' A  34  LEU  HA ', ' A  34  LEU HD23', -0.403, (10.513, 10.745, 107.467))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
