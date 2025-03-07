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
data['rama'] = [('D', '  30 ', 'SER', 0.023338509279918363, (25.945, -32.799, -41.606)), ('F', ' 384 ', 'PRO', 0.020394844898962382, (22.47, 7.859999999999997, -25.397))]
data['omega'] = [('A', ' 159 ', 'PRO', None, (6.93099999999999, 43.29, -58.088)), ('A', ' 161 ', 'PRO', None, (12.613, 41.087, -57.377)), ('B', '   8 ', 'PRO', None, (20.890999999999995, 24.752, -30.243)), ('B', '  95 ', 'PRO', None, (3.124000000000001, 13.886999999999997, -41.06400000000003)), ('B', ' 141 ', 'PRO', None, (27.325, 41.658, -30.956000000000014)), ('D', ' 159 ', 'PRO', None, (21.151000000000007, -71.816, -38.99600000000002)), ('D', ' 161 ', 'PRO', None, (24.245, -69.602, -43.805)), ('E', '   8 ', 'PRO', None, (7.736, -53.54000000000003, -67.496)), ('E', '  95 ', 'PRO', None, (3.909, -43.352, -46.874)), ('E', ' 141 ', 'PRO', None, (13.695999999999989, -69.88800000000003, -72.102))]
data['rota'] = [('A', ' 139 ', 'CYS', 0.09282801759839235, (20.422, 66.50000000000006, -40.688)), ('A', ' 145 ', 'GLU', 0.01596107790367965, (31.772999999999996, 63.53600000000003, -37.498)), ('A', ' 218 ', 'LYS', 0.2993702817533785, (16.025000000000002, 51.57700000000003, -63.76400000000003)), ('A', ' 221 ', 'LYS', 0.1484288602319353, (19.622999999999998, 58.874, -57.856)), ('B', '  42 ', 'LYS', 0.0742278799441992, (20.019, 28.01300000000001, -52.098000000000006)), ('B', ' 107 ', 'LYS', 0.19904593118538338, (32.31100000000001, 34.354, -33.668)), ('C', ' 360 ', 'ASN', 0.01172347042527796, (-11.728000000000002, -22.772000000000013, -80.264)), ('C', ' 390 ', 'LEU', 0.06004119712921266, (-6.528000000000004, -34.380000000000024, -75.86200000000005)), ('C', ' 441 ', 'LEU', 0.03245244236201816, (15.125, -7.387, -74.274)), ('C', ' 524 ', 'VAL', 0.12524827164743038, (-9.312, -26.525000000000013, -77.86)), ('D', ' 145 ', 'GLU', 0.010123774859713077, (21.619999999999997, -91.84000000000002, -71.51800000000006)), ('D', ' 190 ', 'LEU', 0.044837244303176316, (19.061, -77.048, -50.74300000000003)), ('E', ' 211 ', 'GLU', 0.06673364028003524, (12.635000000000003, -100.76, -60.57)), ('E', ' 212 ', 'CYS', 0.0782726829672272, (16.067000000000004, -99.93600000000004, -59.03400000000001)), ('F', ' 524 ', 'VAL', 0.25776449209985536, (20.293, -2.439, -12.357))]
data['cbeta'] = [('B', '  61 ', 'ARG', ' ', 0.2729423205634804, (34.714, 18.162, -40.79300000000001)), ('B', ' 152 ', 'ASN', ' ', 0.25585293681655424, (10.393999999999998, 62.21100000000001, -25.041)), ('C', ' 393 ', 'THR', ' ', 0.2686541287252059, (-13.871, -26.403, -71.628)), ('C', ' 405 ', 'ASP', ' ', 0.25144396740368385, (17.438, -17.213000000000005, -58.814)), ('E', '  81 ', 'GLU', ' ', 0.26578035353607476, (28.284, -53.447, -65.618)), ('F', ' 405 ', 'ASP', ' ', 0.27187447823732197, (23.001999999999995, -9.59, -45.422))]
data['probe'] = [(' E 211  GLU  O  ', ' E 212  CYS  HB2', -0.817, (14.429, -98.377, -58.575)), (' C 363  ALA  HB2', ' C 524  VAL HG12', -0.617, (-6.411, -26.02, -78.551)), (' B   4  MET  HE3', ' B  23  CYS  SG ', -0.598, (14.497, 16.141, -35.279)), (' F 520  ALA  HB1', ' F 521  PRO  HD2', -0.546, (10.016, -4.456, -7.594)), (' E  22  THR HG22', ' E  72  THR HG22', -0.543, (7.554, -45.322, -69.601)), (' E   4  MET  HE3', ' E  23  CYS  SG ', -0.536, (6.616, -45.068, -59.941)), (' F 359  SER  HA ', ' F 524  VAL HG22', -0.533, (19.813, -5.868, -12.825)), (' F 388  ASN  HA ', ' F 526  GLY  HA3', -0.5, (24.311, 3.743, -16.266)), (' A  36  TRP  CE2', ' A  81  MET  HB2', -0.492, (5.839, 20.034, -56.921)), (' B  22  THR HG22', ' B  72  THR HG22', -0.475, (23.18, 16.786, -29.837)), (' E  29  ILE  HA ', ' E  92  TYR  CD2', -0.465, (3.147, -35.817, -56.052)), (' E  21  ILE HG12', ' E 102  THR HG21', -0.461, (12.323, -52.454, -66.545)), (' D  36  TRP  CE2', ' D  81  MET  HB2', -0.45, (18.278, -48.348, -38.74)), (' D 221  LYS  NZ ', ' E 123  GLU  OE1', -0.444, (24.101, -90.338, -46.214)), (' D  52  ILE HD13', ' F 490  PHE  CE1', -0.437, (13.477, -32.745, -39.821)), (' E 136  LEU HD11', ' E 146  VAL HG22', -0.436, (10.352, -77.704, -64.166)), (' E 166  GLN  HG3', ' E 173  TYR  CZ ', -0.435, (18.173, -65.719, -66.515)), (' D 190  LEU  C  ', ' D 190  LEU HD12', -0.426, (20.762, -78.071, -51.232)), (' F 412  PRO  HG3', ' F 429  PHE  HB3', -0.426, (12.885, -1.448, -30.636)), (' B  37  GLN  HB2', ' B  47  LEU HD11', -0.422, (24.355, 20.732, -43.924)), (' E 208  ASN  HB3', ' E 211  GLU  HB3', -0.421, (10.897, -99.28, -62.167)), (' E  37  GLN  HB2', ' E  47  LEU HD11', -0.419, (19.961, -48.195, -61.94)), (' B 136  LEU HD11', ' B 146  VAL HG22', -0.416, (18.939, 49.152, -33.429)), (' D 158  PHE  HA ', ' D 159  PRO  HA ', -0.413, (19.426, -72.361, -40.716)), (' C 431  GLY  HA3', ' C 513  LEU  O  ', -0.407, (-1.013, -25.578, -68.028)), (' E 211  GLU  O  ', ' E 212  CYS  CB ', -0.407, (14.665, -98.83, -58.849)), (' C 336  CYS  HA ', ' C 337  PRO  HD3', -0.405, (-5.658, -20.265, -81.988)), (' A 153  LEU  HG ', ' A 155  LYS  HG3', -0.404, (11.541, 54.257, -49.188)), (' A 171  LEU HD21', ' A 194  VAL HG21', -0.403, (29.652, 54.38, -51.243)), (' B  81 AGLU  HG3', ' B 310  HOH  O  ', -0.401, (33.902, 22.983, -47.452)), (' C 380  TYR  O  ', ' C 430  THR  HA ', -0.401, (-1.03, -30.676, -65.006))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
