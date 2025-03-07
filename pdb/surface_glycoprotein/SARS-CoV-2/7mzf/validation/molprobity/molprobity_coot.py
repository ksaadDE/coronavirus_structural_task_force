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
data['omega'] = [('H', ' 151 ', 'PRO', None, (1.4079999999999988, 66.849, -2.246)), ('H', ' 153 ', 'PRO', None, (-1.899, 64.788, -6.988000000000001)), ('L', '  10 ', 'PRO', None, (8.003, 45.635999999999974, -22.39)), ('L', ' 141 ', 'PRO', None, (10.062, 50.504000000000026, -30.723))]
data['rota'] = []
data['cbeta'] = []
data['probe'] = [(' A 388  ASN  HB3', ' A 527  PRO  HD2', -0.819, (13.17, -0.512, 27.392)), (' A 477  SER  HB2', ' H  26  GLU  OE2', -0.722, (-24.891, 35.878, 0.875)), (' A 364  ASP  OD2', ' A 367  VAL HG23', -0.719, (13.688, -2.036, 20.518)), (' A 480  CYS  O  ', ' A 483  VAL HG12', -0.712, (-26.17, 24.304, -2.611)), (' L  33  LEU HD22', ' L  71  PHE  CG ', -0.699, (3.939, 28.18, -13.684)), (' H  82  MET  HE2', ' H  82C LEU HD21', -0.691, (1.134, 51.063, 6.639)), (' L  39  LYS  HD3', ' L  84  ALA  HB2', -0.687, (-5.921, 43.859, -19.064)), (' B   1  NAG  H61', ' B   2  NAG  C7 ', -0.68, (13.988, -4.961, 7.454)), (' A 366  SER  HA ', ' A 369  TYR  CB ', -0.664, (14.808, 3.677, 19.972)), (' L  48  ILE  CD1', ' L  54  LEU HD12', -0.657, (-6.317, 28.89, -17.442)), (' L  37  GLN  HB2', ' L  47  LEU HD11', -0.646, (-5.077, 37.809, -17.042)), (' H 203  ASN  OD1', ' H 210  LYS  HG2', -0.645, (-5.771, 75.492, -11.391)), (' L  48  ILE HD11', ' L  54  LEU HD12', -0.642, (-6.786, 29.147, -17.958)), (' A 474  GLN  OE1', ' A 479  PRO  HA ', -0.641, (-24.689, 27.879, 3.159)), (' H  66  ARG  NH2', ' H  86  ASP  OD2', -0.627, (6.324, 50.571, 7.751)), (' A 388  ASN  CB ', ' A 527  PRO  HD2', -0.624, (12.581, -0.218, 27.172)), (' A 354  ASN  HB3', ' A 751  HOH  O  ', -0.59, (-4.02, 3.682, 12.017)), (' L 108  ARG  NH1', ' L 109  THR  O  ', -0.586, (5.623, 51.995, -35.668)), (' L 164  THR  HB ', ' L 301  GOL  H32', -0.583, (2.434, 58.995, -23.112)), (' L 183  LYS  O  ', ' L 187  GLU  HG2', -0.58, (25.994, 76.919, -12.497)), (' L   4  MET  HE3', ' L  23  CYS  SG ', -0.575, (6.823, 31.841, -11.495)), (' L 161  GLU  HG2', ' L 177  SER  HB2', -0.572, (15.306, 59.67, -19.289)), (' H  33  TYR  HB2', ' H  95  ASP  O  ', -0.57, (-8.521, 32.108, 1.64)), (' L  79  GLN  HB3', ' L  80  PRO  HD2', -0.568, (-10.343, 40.212, -28.202)), (' L  45  LYS  HD3', ' L 410  HOH  O  ', -0.567, (-10.148, 37.885, -10.125)), (' H 154  VAL HG12', ' H 204  HIS  HB2', -0.566, (-0.284, 71.214, -8.848)), (' H 120  PRO  HB3', ' H 149  TYR  HB3', -0.546, (4.609, 71.06, -8.256)), (' L 145  LYS  HB3', ' L 197  THR  HB ', -0.544, (20.449, 54.023, -26.695)), (' L  47  LEU  HA ', ' L  58  VAL HG21', -0.543, (-8.369, 33.364, -15.037)), (' L   6  GLN  HB3', ' L   7  PRO  HD2', -0.538, (7.144, 36.998, -17.058)), (' A 359  SER  HA ', ' A 524  VAL  CG2', -0.535, (-0.599, -0.658, 26.258)), (' L 108  ARG  HG3', ' L 109  THR  O  ', -0.534, (5.219, 50.571, -34.963)), (' L 129  THR  HB ', ' L 433  HOH  O  ', -0.527, (15.921, 74.209, -9.644)), (' H 218  LYS  HE3', ' L 122  ASP  OD2', -0.515, (17.059, 83.668, -20.431)), (' A 431  GLY  HA3', ' A 513  LEU  O  ', -0.508, (3.602, 10.868, 22.038)), (' H 157  SER  OG ', ' H 201  ASN  HB2', -0.507, (-4.301, 74.853, -18.33)), (' L 142 BARG  CZ ', ' L 163  VAL HG21', -0.506, (10.15, 54.306, -21.182)), (' A 336  CYS  SG ', ' A 363  ALA  HB2', -0.503, (4.878, -2.032, 23.456)), (' H  82  MET  HE2', ' H  82C LEU  CD2', -0.502, (1.562, 51.385, 6.757)), (' L  30  SER  OG ', ' L  31  SER  N  ', -0.5, (3.734, 20.878, -8.553)), (' H 104  TRP  H  ', ' L  45  LYS  NZ ', -0.498, (-10.554, 40.364, -7.287)), (' A 520  ALA  HB1', ' A 521  PRO  HD2', -0.496, (-6.274, -0.137, 35.037)), (' A 455  LEU HD23', ' A 456  PHE  CE2', -0.495, (-10.663, 24.842, -0.089)), (' L  50  LYS  O  ', ' L  51  ALA  HB3', -0.495, (-1.065, 23.412, -12.596)), (' L 154  LEU  N  ', ' L 154  LEU HD12', -0.495, (30.608, 60.967, -21.243)), (' L 193  ALA  HB2', ' L 208  SER  HB3', -0.49, (25.141, 67.692, -27.188)), (' L 129  THR HG22', ' L 130  ALA  N  ', -0.487, (18.598, 73.219, -11.387)), (' L 167  ASP  O  ', ' L 171  SER  HA ', -0.485, (-0.262, 53.553, -29.18)), (' A 444  LYS  HB2', ' A 448  ASN  HB2', -0.482, (0.277, 9.525, -6.724)), (' L  33  LEU HD22', ' L  71  PHE  CB ', -0.479, (4.189, 28.3, -14.112)), (' L 105  GLU  HB3', ' L 166  GLN  OE1', -0.472, (1.419, 48.69, -26.205)), (' A 339  GLY  O  ', ' A 343  ASN  HB2', -0.472, (4.71, -2.491, 10.581)), (' L  34  ALA  HA ', ' L  48  ILE  O  ', -0.468, (-2.454, 29.914, -11.096)), (' L 113  PRO  HB3', ' L 139  PHE  HB3', -0.46, (11.297, 57.628, -30.319)), (' H  67  PHE  CE2', ' H  82  MET  HE3', -0.451, (0.824, 48.495, 6.001)), (' H  87  THR HG23', ' H 111  THR  HA ', -0.45, (2.193, 56.443, -0.065)), (' A 431  GLY  HA2', ' A 515  PHE  CD2', -0.45, (4.807, 9.661, 24.579)), (' A 350  VAL HG23', ' A 400  PHE  CD1', -0.446, (-1.254, 13.689, 9.458)), (' H   2  VAL HG22', ' H  27  PHE  CE2', -0.444, (-16.891, 38.144, -2.789)), (' L 150  VAL HG23', ' L 155  GLN  HG3', -0.443, (26.293, 65.368, -17.547)), (' L  37  GLN  HG3', ' L  86  TYR  CE1', -0.443, (-4.254, 39.49, -18.087)), (' A 487  ASN  HA ', ' A 489  TYR  CE2', -0.433, (-16.963, 29.995, -1.923)), (' A 359  SER  HA ', ' A 524  VAL HG22', -0.432, (-0.38, -1.131, 26.238)), (' H  70  SER  O  ', ' H  78  LEU HD12', -0.431, (-9.457, 41.675, 9.787)), (' A 447  GLY  HA3', ' A 449  TYR  CE1', -0.431, (-2.005, 13.897, -9.207)), (' A 392  PHE  CD1', ' A 515  PHE  HB3', -0.43, (3.315, 7.157, 28.386)), (' H 128  SER  OG ', ' H 129  SER  N  ', -0.43, (16.141, 75.695, -31.821)), (' H  44  GLY  HA3', ' H 317  HOH  O  ', -0.429, (5.636, 42.366, -7.903)), (' L 181  LEU HD11', ' L 192  TYR  HE2', -0.424, (25.166, 70.174, -16.244)), (' A 366  SER  H  ', ' A 388  ASN HD21', -0.423, (13.972, 1.001, 23.529)), (' H  98  ASP  O  ', ' L  91  TYR  HB2', -0.422, (-1.259, 29.613, -2.326)), (' A 477  SER  O  ', ' A 479  PRO  HD3', -0.419, (-27.164, 31.865, 2.761)), (' L  10  PRO  HG2', ' L  12  PHE  CZ ', -0.419, (6.749, 47.588, -25.161)), (' L 159  SER  HA ', ' L 178  THR  O  ', -0.418, (17.94, 63.709, -14.743)), (' H  50  VAL HG12', ' H  58  TYR  HB2', -0.418, (-0.626, 34.427, 7.441)), (' A 392  PHE  CE1', ' A 515  PHE  HB3', -0.415, (3.834, 7.408, 28.795)), (' L 108  ARG  HG2', ' L 140  TYR  CD2', -0.413, (4.966, 50.121, -32.193)), (' H 193  LEU  HA ', ' H 193  LEU HD23', -0.413, (5.589, 78.727, -31.697)), (' A 447  GLY  HA2', ' A 498  GLN  HG3', -0.407, (0.961, 14.202, -8.603)), (' L 108  ARG  HG3', ' L 109  THR  N  ', -0.406, (4.764, 49.953, -35.405)), (' H  39  GLN  HG3', ' H  44  GLY  O  ', -0.405, (2.769, 45.567, -6.69)), (' H  96  ARG  NH2', ' L  55  GLU  OE1', -0.403, (-10.661, 30.19, -8.881)), (' H  34  MET  HB3', ' H  78  LEU HD22', -0.402, (-9.578, 39.546, 5.154)), (' L 136  LEU HD21', ' L 196  VAL HG13', -0.4, (15.987, 58.319, -27.293)), (' H   6  GLU  HA ', ' H  21  SER  O  ', -0.4, (-10.775, 48.233, 3.056))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
