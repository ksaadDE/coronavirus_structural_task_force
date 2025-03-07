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
data['omega'] = [('A', ' 146 ', 'PRO', None, (-59.20300000000001, 18.174, -41.234)), ('A', ' 211 ', 'GLU', None, (-75.207, 42.066, -5.281)), ('A', ' 213 ', 'SER', None, (-77.282, 42.063, 1.425)), ('A', ' 627 ', 'ALA', None, (-31.176000000000016, 64.16900000000004, -33.349)), ('B', ' 520 ', 'ALA', None, (-135.355, 19.524, -4.139999999999999))]
data['rota'] = []
data['cbeta'] = [('A', ' 635 ', 'TRP', ' ', 0.26861113619272603, (-36.185, 54.161, -41.517999999999994))]
data['probe'] = [(' A 120  LEU HD21', ' A 183  TYR  HE2', -0.743, (-66.983, 39.431, -35.066)), (' A 198  ASP  OD2', ' A 465  LYS  HG3', -0.718, (-61.498, 48.424, -22.662)), (' B 520  ALA  HB1', ' B 521  PRO  HD2', -0.705, (-135.508, 20.319, -7.846)), (' A 183  TYR  OH ', ' A 509  ASP  OD1', -0.691, (-66.59, 39.553, -31.703)), (' A  54  ILE HD11', ' A 343  VAL HG23', -0.687, (-73.604, 19.732, -39.73)), (' A 177  ARG  NH2', ' A 470  LYS  O  ', -0.686, (-51.414, 47.07, -35.888)), (' A 251  THR HG21', ' A 281  LEU HD22', -0.685, (-39.969, 13.484, -28.057)), (' A  31  LYS  HE2', ' B 489  TYR  HB3', -0.662, (-100.209, 41.242, -24.321)), (' A 653  GLU  OE2', ' A 657  LYS  NZ ', -0.661, (-22.489, 40.116, -59.471)), (' A 210  GLU  HG3', ' A 210  GLU  O  ', -0.661, (-77.239, 43.939, -6.501)), (' A 573  ILE HG23', ' A 574  VAL HG13', -0.65, (-69.435, 25.395, -4.322)), (' A  85  LEU  O  ', ' A  88  ILE HG22', -0.64, (-85.453, 48.541, -10.657)), (' B 396  TYR  HB2', ' B 514  SER  HB2', -0.636, (-121.388, 20.362, -12.521)), (' A 635  TRP  HB3', ' A 639  GLU  HB2', -0.608, (-36.562, 53.29, -43.44)), (' A  54  ILE  HB ', ' A 341  LYS  HB3', -0.607, (-75.436, 16.691, -43.6)), (' A  95  ARG  O  ', ' A  99  ILE HG12', -0.601, (-81.955, 39.813, -16.684)), (' A 120  LEU HD21', ' A 183  TYR  CE2', -0.597, (-66.783, 40.297, -34.966)), (' A 134  LYS  NZ ', ' A 140  GLU  OE2', -0.59, (-48.534, 16.412, -49.586)), (' A 293  VAL HG11', ' A 423  LEU HD13', -0.581, (-64.883, 1.353, -18.768)), (' A 319  SER  O  ', ' A 319  SER  OG ', -0.566, (-80.969, 13.521, -4.904)), (' A 133  CYS  HA ', ' A 141  CYS  HA ', -0.561, (-51.219, 23.4, -49.576)), (' B 383  SER  H  ', ' B 387  LEU HD12', -0.56, (-118.594, 9.688, -2.266)), (' B 366  SER  HA ', ' B 369  TYR  CD2', -0.557, (-116.419, 4.726, -9.888)), (' A 696  PRO  HG2', ' A 699  GLU  HG3', -0.553, (-23.607, 30.23, -44.124)), (' A 293  VAL HG12', ' A 297  MET  HG3', -0.552, (-64.336, 0.6, -20.757)), (' A 294  THR HG23', ' A 365  THR  HA ', -0.542, (-63.685, 2.707, -26.208)), (' A 201  ASP  OD1', ' A 219  ARG  NE ', -0.533, (-68.363, 46.714, -17.705)), (' A 233  ILE HD13', ' A 450  LEU HD13', -0.527, (-54.804, 27.991, -13.724)), (' A 131  LYS  HB3', ' A 143  LEU HD12', -0.527, (-57.691, 23.701, -47.44)), (' A 456  LEU HD12', ' A 477  TRP  HH2', -0.525, (-54.545, 34.539, -28.177)), (' B 391  CYS  HA ', ' B 525  CYS  HA ', -0.521, (-128.822, 9.976, -7.834)), (' A 288  LYS  NZ ', ' A 433  GLU  OE1', -0.511, (-43.547, 1.375, -12.002)), (' A 493  HIS  ND1', ' A 499  ASP  OD2', -0.51, (-47.336, 34.895, -35.937)), (' A  31  LYS  CE ', ' B 489  TYR  HB3', -0.509, (-100.05, 41.597, -24.476)), (' A 246  ALA  HA ', ' A 249  MET  HE3', -0.507, (-35.447, 20.014, -21.169)), (' A 388  GLN  O  ', ' A 393  ARG  NE ', -0.505, (-87.553, 28.76, -16.801)), (' A 629  GLY  O  ', ' A 631  LYS  HG2', -0.504, (-39.466, 63.769, -36.281)), (' A 456  LEU HD22', ' A 512  PHE  CD2', -0.503, (-58.425, 32.134, -25.329)), (' B 366  SER  HA ', ' B 369  TYR  CE2', -0.501, (-116.731, 3.798, -9.867)), (' A 615  ASP  N  ', ' A 615  ASP  OD1', -0.501, (-29.893, 32.509, -32.411)), (' A 168  TRP  O  ', ' A 172  VAL HG12', -0.493, (-53.189, 30.843, -40.459)), (' B 393  THR  HA ', ' B 522  ALA  HA ', -0.491, (-131.917, 15.566, -8.284)), (' B 350  VAL HG22', ' B 422  ASN  HB3', -0.49, (-108.827, 28.309, -18.11)), (' A 542  CYS  SG ', ' A 543  ASP  N  ', -0.483, (-64.554, 11.783, -5.17)), (' A 310  GLU  OE1', ' A 421  MET  HE2', -0.482, (-72.073, 1.783, -14.375)), (' A 314  PHE  O  ', ' A 318  VAL HG23', -0.479, (-74.96, 9.71, -9.408)), (' A 108  LEU HD21', ' A 189  GLU  OE1', -0.47, (-71.396, 51.432, -34.527)), (' A 318  VAL HG12', ' A 551  GLY  HA3', -0.469, (-75.545, 13.778, -5.079)), (' A 683  PHE  HZ ', ' A 704  ILE HD11', -0.466, (-27.498, 41.606, -42.775)), (' A 107  VAL HG21', ' A 193  GLY  HA3', -0.464, (-74.907, 52.231, -28.183)), (' A 514  ARG  O  ', ' A 518  ARG  HB3', -0.462, (-64.833, 27.869, -17.721)), (' A 577  ARG  NH1', ' A 578  ASN  OD1', -0.46, (-64.838, 38.324, -3.056)), (' B 449  TYR  O  ', ' B 494  SER  OG ', -0.459, (-102.852, 29.286, -30.063)), (' A 408  MET  HE1', ' A 554  LEU HD21', -0.457, (-73.916, 17.218, -10.032)), (' A  20  THR  O  ', ' A  24  GLU  HG2', -0.454, (-96.241, 49.775, -12.81)), (' A  24  GLU  OE2', ' B 476  GLY  HA2', -0.451, (-99.293, 50.575, -15.652)), (' A 318  VAL  O  ', ' A 551  GLY  HA3', -0.45, (-76.743, 13.935, -5.181)), (' B 359  SER  HA ', ' B 524  VAL  CG2', -0.448, (-129.512, 14.129, -14.033)), (' A 457  GLU  HG2', ' A 512  PHE  HB3', -0.447, (-60.234, 34.885, -23.425)), (' A 335  GLU  HB2', ' A 361  CYS  SG ', -0.445, (-72.184, 9.486, -35.754)), (' A 374  HIS  CE1', ' A 402  GLU  OE1', -0.444, (-68.062, 20.826, -20.722)), (' A 718  ASP  H  ', ' A 721  SER  HG ', -0.442, (-23.693, 56.579, -42.298)), (' A 717  LEU  HB3', ' A 721  SER  OG ', -0.442, (-24.742, 55.646, -42.209)), (' B 382  VAL HG22', ' B 387  LEU HD12', -0.441, (-119.142, 10.073, -2.812)), (' A  88  ILE HD11', ' A  93  VAL HG23', -0.441, (-88.632, 43.791, -11.032)), (' A 144  LEU  HA ', ' A 148  LEU  HB2', -0.44, (-54.888, 22.807, -40.148)), (' A 351  LEU  H  ', ' A 351  LEU HD12', -0.439, (-83.382, 20.654, -26.121)), (' A 628  LEU  HA ', ' A 628  LEU HD12', -0.438, (-34.221, 60.604, -32.994)), (' A 621  TRP  CZ3', ' A 725  LEU HD22', -0.435, (-25.302, 45.384, -31.731)), (' A 520  ILE HG21', ' A 579  MET  HG2', -0.433, (-61.531, 30.801, -9.149)), (' A 621  TRP  HZ3', ' A 725  LEU  HB2', -0.432, (-24.461, 45.6, -32.967)), (' A 269  ASP  OD1', ' A 272  GLY  N  ', -0.43, (-51.68, 24.966, -29.007)), (' A 171  GLU  O  ', ' A 175  GLN  NE2', -0.429, (-55.233, 33.294, -46.597)), (' A 621  TRP  HB2', ' A 723  GLU  HG3', -0.428, (-25.351, 50.144, -35.726)), (' A 267  LEU  HA ', ' A 278  LEU HD11', -0.426, (-46.212, 21.093, -26.259)), (' A 671  TRP  O  ', ' A 683  PHE  HA ', -0.423, (-34.621, 39.465, -39.146)), (' A 293  VAL HG13', ' A 423  LEU  HB3', -0.423, (-63.511, -0.363, -18.209)), (' A 676  LYS  HB3', ' A 679  ILE  HB ', -0.421, (-35.007, 51.252, -31.381)), (' A  41  TYR  HH ', ' B 500  THR  HG1', -0.421, (-90.77, 19.75, -28.971)), (' A 245  ARG  NH1', ' A 605  GLY  O  ', -0.418, (-37.205, 27.88, -18.297)), (' A 249  MET  HB2', ' A 249  MET  HE3', -0.418, (-34.782, 19.649, -22.406)), (' A 373  HIS  CD2', ' A 412  VAL HG21', -0.417, (-70.029, 9.41, -14.83)), (' A 652  ARG  NH2', ' A 664  LEU  HB3', -0.416, (-35.235, 35.566, -56.78)), (' A 300  GLN  NE2', ' A 422  GLY  O  ', -0.415, (-65.985, -5.709, -17.264)), (' A 333  LEU  O  ', ' A 362  THR HG22', -0.413, (-73.984, 7.558, -29.314)), (' A 528  ALA  HB2', ' A 574  VAL HG12', -0.412, (-66.844, 23.452, -2.65)), (' B 376  THR  HB ', ' B 435  ALA  HB3', -0.409, (-106.208, 14.39, -13.961)), (' A 100  LEU  HA ', ' A 100  LEU HD12', -0.409, (-83.541, 40.688, -22.61)), (' A 657  LYS  HB2', ' A 706  MET  HE1', -0.409, (-20.576, 37.632, -55.49)), (' A 477  TRP  CZ3', ' A 500  PRO  HB3', -0.408, (-53.783, 36.845, -29.328)), (' A 455  MET  HE2', ' A 480  MET  HB2', -0.408, (-49.335, 38.018, -24.238)), (' A 635  TRP  HB3', ' A 639  GLU  CB ', -0.406, (-36.681, 53.565, -43.507)), (' A 625  LYS  HB3', ' A 625  LYS  HE3', -0.405, (-29.147, 63.45, -40.225)), (' B 362  VAL HG13', ' B 526  GLY  HA2', -0.405, (-127.948, 4.977, -12.451)), (' A 567  THR  HB ', ' A 577  ARG  HG3', -0.403, (-70.215, 36.272, -3.311)), (' A 704  ILE  O  ', ' A 708  ARG  N  ', -0.402, (-21.574, 44.783, -48.183))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
