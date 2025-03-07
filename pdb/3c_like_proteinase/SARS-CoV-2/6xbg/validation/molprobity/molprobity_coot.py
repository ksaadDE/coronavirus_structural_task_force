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
data['rota'] = [('A', '   4 ', 'ARG', 0.0, (-7.302, 1.15, 6.773)), ('A', '   5 ', 'LYS', 0.1772020528563162, (-4.22, 1.5020000000000004, 9.028)), ('A', '  47 ', 'GLU', 0.21559271904901625, (17.573, 18.845, 37.827)), ('A', '  50 ', 'LEU', 0.26850432115948725, (18.589, 19.376999999999992, 31.669999999999998)), ('A', '  59 ', 'ILE', 0.27198273542337364, (27.612999999999996, 4.658, 38.958)), ('B', '  59 ', 'ILE', 0.024305418178384202, (-31.192, -30.59799999999999, 13.139999999999997)), ('B', ' 303 ', 'VAL', 0.26072334515864887, (-6.223000000000002, 5.404999999999999, 30.311)), ('B', ' 305 ', 'PHE', 0.23547891892006864, (-6.456000000000002, -1.5909999999999997, 30.884)), ('E', '   2 ', 'LEU', 0.0, (-21.222000000000005, -13.908999999999999, 3.3709999999999996))]
data['cbeta'] = [('B', ' 189 ', 'GLN', ' ', 0.2697079529782296, (-25.012, -15.542000000000002, -0.505)), ('B', ' 303 ', 'VAL', ' ', 0.2663911487763951, (-7.695999999999998, 5.453, 29.855999999999998))]
data['probe'] = [(' A   4 BARG  HB2', ' A   4 BARG  NH1', -1.224, (-7.74, 0.707, 9.397)), (' A   4 BARG  CG ', ' A   4 BARG HH11', -1.012, (-8.198, -0.054, 8.455)), (' A   4 BARG  CB ', ' A   4 BARG  NH1', -0.975, (-8.286, 1.061, 8.466)), (' A   4 BARG  HG3', ' A   4 BARG HH11', -0.901, (-7.882, -0.385, 8.774)), (' A   4 BARG  CB ', ' A   4 BARG HH11', -0.857, (-8.198, 0.439, 8.356)), (' A  86  VAL HG22', ' A 162 BMET  HE1', -0.834, (16.309, 1.821, 25.537)), (' B 126  TYR  HE1', ' B 128 BCYS  SG ', -0.756, (-12.487, -2.525, 10.858)), (' A   4 BARG  CZ ', ' A   4 BARG  HB2', -0.739, (-9.106, 1.925, 9.243)), (' B  22 BCYS  SG ', ' B  61  LYS  HE3', -0.677, (-21.583, -28.867, 9.13)), (' B 126  TYR  CE1', ' B 128 BCYS  SG ', -0.676, (-12.059, -1.894, 10.886)), (' A  86  VAL HG22', ' A 162 BMET  CE ', -0.621, (15.562, 1.604, 25.31)), (' A   4 BARG  CB ', ' A   4 BARG  CZ ', -0.606, (-9.23, 1.566, 8.613)), (' B 165 AMET  HB3', ' E   2  LEU HD12', -0.597, (-22.605, -12.722, 4.993)), (' B  22 BCYS  SG ', ' B  61  LYS  CE ', -0.596, (-21.904, -28.608, 9.586)), (' B   5  LYS  HB2', ' B 503  GOL  H2 ', -0.576, (-6.915, 5.99, 12.558)), (' B 502  GOL  H11', ' B 694  HOH  O  ', -0.576, (-6.229, -21.074, 24.997)), (' B  62 ASER  HB2', ' B 501 AGOL  H31', -0.562, (-23.526, -36.125, 17.384)), (' B  76 AARG  NH1', ' B  92  ASP  OD2', -0.554, (-13.122, -33.77, 25.329)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.538, (8.148, 5.944, 4.924)), (' B 502  GOL  C1 ', ' B 694  HOH  O  ', -0.524, (-5.776, -20.887, 25.012)), (' B  62 ASER  HB2', ' B 501 AGOL  C3 ', -0.521, (-23.476, -35.558, 17.707)), (' A   5  LYS  HD2', ' B 503  GOL  H12', -0.512, (-4.18, 5.829, 9.636)), (' A  22 BCYS  SG ', ' A  66  PHE  CD1', -0.506, (16.827, 2.478, 38.076)), (' B   4  ARG  NH2', ' B 611  HOH  O  ', -0.506, (1.017, 7.965, 12.279)), (' A 139 BSER  OG ', ' B   4  ARG  HG3', -0.499, (-1.564, 9.355, 17.141)), (' A   4 BARG  NH2', ' B 127  GLN  O  ', -0.488, (-10.532, 2.03, 11.794)), (' A 165 AMET  HG3', ' C   1  P6S  O28', -0.482, (11.033, 14.767, 24.577)), (' B 109  GLY  HA2', ' B 200  ILE HD13', -0.476, (-20.629, 6.751, 14.824)), (' A   4 BARG  CG ', ' A   4 BARG  NH1', -0.464, (-8.678, 0.044, 9.662)), (' A 127  GLN  O  ', ' B   4  ARG  NH1', -0.462, (-0.544, 4.939, 12.771)), (' B 152  ILE  O  ', ' B 305  PHE  CE1', -0.454, (-10.424, 0.482, 27.893)), (' B 165 AMET  HE1', ' B 192  GLN  NE2', -0.451, (-26.622, -10.539, 3.372)), (' B  27 ALEU  C  ', ' B  27 ALEU HD12', -0.451, (-15.051, -19.794, 11.859)), (' A 543  HOH  O  ', ' B 305  PHE  HB2', -0.446, (-6.452, -2.496, 28.013)), (' A 298  ARG  NH1', ' A 408  HOH  O  ', -0.445, (1.184, -4.318, 8.686)), (' A  69  GLN  HG2', ' A  74  GLN  OE1', -0.444, (7.056, -3.606, 42.468)), (' A  56  ASP  O  ', ' A  59  ILE HG22', -0.434, (27.76, 7.933, 38.229)), (' A  82 AMET  HB2', ' A  82 AMET  HE3', -0.434, (23.679, 2.66, 31.772)), (' B 113  SER  O  ', ' B 149  GLY  HA2', -0.429, (-13.359, -5.072, 17.712)), (' B 108  PRO  HB3', ' B 132  PRO  HA ', -0.416, (-25.645, 4.799, 12.819)), (' A  58  LEU HD22', ' A  82 AMET  HE3', -0.413, (23.633, 3.195, 32.911)), (' A 300  CYS  O  ', ' A 301  SER  C  ', -0.411, (-6.008, -9.464, -1.246)), (' A 187  ASP  HA ', ' C   2  LEU HD21', -0.405, (16.248, 12.391, 26.068)), (' B 165 AMET  HE1', ' B 192  GLN HE22', -0.403, (-27.157, -10.649, 3.798)), (' B 115  LEU HD11', ' B 122  PRO  HB3', -0.4, (-5.479, -10.493, 16.356))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
