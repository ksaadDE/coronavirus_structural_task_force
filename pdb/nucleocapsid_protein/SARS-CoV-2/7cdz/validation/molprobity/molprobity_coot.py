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
data['omega'] = [('B', ' 100 ', 'LYS', None, (2.722000000000001, 20.217, -2.456))]
data['rota'] = []
data['cbeta'] = []
data['probe'] = [(' B  99  PRO  HB2', ' B 101  ASP  H  ', -1.007, (3.407, 22.617, -4.407)), (' A   5  ASN  HB3', ' C  97  ASN HD22', -0.903, (13.663, 28.725, 31.97)), (' A  39  ASP  OD1', ' A 102  HIS  NE2', -0.877, (28.375, 21.029, 42.657)), (' A 129  TYR  OH ', ' B 129  TYR  CZ ', -0.838, (12.026, 1.348, 21.172)), (' B   6  THR  O  ', ' B 202  HOH  O  ', -0.818, (14.774, 22.489, 6.126)), (' A 130  ALA  O  ', ' A 201  HOH  O  ', -0.795, (18.959, 10.836, 24.269)), (' A   6  THR  N  ', ' A 202  HOH  O  ', -0.793, (14.683, 27.286, 34.527)), (' B  99  PRO  CG ', ' B 101  ASP  OD1', -0.771, (2.365, 23.055, -5.968)), (' D  55  ASP  OD1', ' D 201  HOH  O  ', -0.724, (44.159, 57.016, 27.64)), (' B  99  PRO  CB ', ' B 101  ASP  OD1', -0.709, (3.356, 22.918, -5.974)), (' A 129  TYR  HD1', ' A 129  TYR  O  ', -0.705, (14.325, 6.034, 23.057)), (' B  99  PRO  HG3', ' B 101  ASP  OD1', -0.7, (2.6, 24.021, -6.4)), (' B  99  PRO  HB2', ' B 101  ASP  N  ', -0.691, (3.708, 23.021, -3.558)), (' A  52  ARG  NH2', ' A  56  GLY  O  ', -0.677, (-10.853, 16.402, 21.542)), (' A 131  GLU  OE1', ' B  64  ARG  NH1', -0.648, (16.435, 14.503, 19.171)), (' C  64  ARG  NH1', ' C 204  HOH  O  ', -0.635, (-9.959, 42.421, 15.86)), (' A 129  TYR  CD1', ' A 129  TYR  O  ', -0.593, (14.808, 5.178, 23.175)), (' A 210  HOH  O  ', ' D   6  THR HG21', -0.587, (26.351, 30.915, 27.062)), (' A  18  LYS  H  ', ' A 126  LYS  NZ ', -0.576, (6.943, -0.896, 29.062)), (' B  39  ASP  HA ', ' B 100  LYS  HD2', -0.572, (-0.958, 18.611, -0.718)), (' A  50  ARG  NH2', ' A  60  ASP  OD1', -0.57, (-4.033, 11.932, 28.896)), (' A   6  THR HG23', ' A  73  GLY  HA2', -0.57, (14.341, 23.475, 38.525)), (' C  50  ARG  HD2', ' C  50  ARG  O  ', -0.565, (-6.516, 49.014, 9.422)), (' B  22  LYS  NZ ', ' B 203  HOH  O  ', -0.563, (10.805, -2.393, 7.162)), (' D  51  ILE  HA ', ' D 206  HOH  O  ', -0.559, (40.694, 49.357, 30.179)), (' B  99  PRO  HB2', ' B 101  ASP  OD1', -0.549, (3.474, 23.009, -4.962)), (' C  27  GLN  HB3', ' C 122  THR HG23', -0.539, (-2.784, 36.939, 37.63)), (' A  14  THR  H  ', ' A 130  ALA  HB2', -0.536, (13.873, 9.148, 25.887)), (' D  19  GLU  OE2', ' D 202  HOH  O  ', -0.522, (34.358, 45.917, 3.148)), (' A 131  GLU  HB2', ' A 216  HOH  O  ', -0.52, (17.605, 12.886, 24.388)), (' A  39  ASP  HA ', ' A 100  LYS  HE3', -0.508, (26.72, 17.351, 43.343)), (' C   6  THR  O  ', ' C 201  HOH  O  ', -0.508, (-2.37, 33.686, 14.637)), (' A   6  THR  CA ', ' A 202  HOH  O  ', -0.488, (14.83, 26.641, 34.955)), (' C  53  GLY  HA3', ' C  59  LYS  HD3', -0.474, (-12.447, 54.685, 12.658)), (' B   5  ASN  HB3', ' B 107  ASN  HB2', -0.473, (9.392, 30.393, 8.132)), (' D  12  ALA  HB2', ' D  66  TYR  CE1', -0.468, (36.63, 35.201, 19.32)), (' A  12  ALA  HB2', ' A  66  TYR  CE1', -0.467, (12.846, 16.806, 28.671)), (' B 102  HIS  HB3', ' B 246  HOH  O  ', -0.464, (0.691, 25.906, -3.918)), (' C  57  LYS  HD2', ' C  58  MET  O  ', -0.46, (-8.408, 57.812, 10.987)), (' A   5  ASN  CB ', ' C  97  ASN HD22', -0.455, (13.05, 29.618, 32.566)), (' A  55  ASP  N  ', ' A  55  ASP  OD2', -0.449, (-9.327, 11.329, 18.063)), (' C   6  THR HG22', ' C 201  HOH  O  ', -0.447, (-1.574, 33.068, 14.891)), (' B 233  HOH  O  ', ' C   6  THR HG21', -0.446, (1.401, 32.377, 13.448)), (' A  69  TYR  CE2', ' A 103  ILE HG21', -0.445, (24.206, 20.159, 37.249)), (' A   5  ASN  HB3', ' C  97  ASN  ND2', -0.439, (13.432, 29.202, 31.471)), (' B  69  TYR  HB3', ' B 100  LYS  HB2', -0.438, (3.591, 19.413, 0.89)), (' A  33  THR  HB ', ' D 110  ASN HD21', -0.438, (34.58, 18.934, 30.61)), (' C  52  ARG  NH1', ' C  56  GLY  O  ', -0.437, (-10.124, 57.93, 4.626)), (' C  50  ARG  HA ', ' C  59  LYS  O  ', -0.436, (-6.981, 52.015, 12.461)), (' A 306  HOH  O  ', ' D   6  THR HG23', -0.429, (26.618, 28.957, 26.008)), (' C  57  LYS  HE3', ' C  59  LYS  HB3', -0.427, (-10.039, 56.908, 12.905)), (' D  50  ARG  O  ', ' D  51  ILE HD13', -0.42, (39.451, 47.19, 28.615)), (' B 222  HOH  O  ', ' D  36  SER  HB2', -0.419, (25.238, 16.514, 10.945)), (' D  55  ASP  N  ', ' D  55  ASP  OD1', -0.418, (45.83, 57.66, 28.129)), (' A 129  TYR  OH ', ' B 129  TYR  OH ', -0.416, (11.619, 0.579, 20.92)), (' C  64  ARG  CZ ', ' C 204  HOH  O  ', -0.415, (-10.092, 41.947, 16.65)), (' A  69  TYR  CE1', ' A 103  ILE HD12', -0.413, (25.335, 19.085, 38.738)), (' A  18  LYS  H  ', ' A 126  LYS  HZ1', -0.411, (6.99, -0.763, 30.038)), (' B  99  PRO  HB2', ' B 101  ASP  CB ', -0.409, (4.173, 23.341, -4.404)), (' C  16  HIS  N  ', ' C 127  GLY  O  ', -0.406, (-8.603, 49.204, 27.622))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
