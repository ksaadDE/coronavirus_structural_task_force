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
data['rota'] = []
data['cbeta'] = []
data['probe'] = [(' B 514  SER  HB2', ' B 712  GOL  H31', -0.922, (39.158, -27.773, -6.133)), (' B 455  LEU HD13', ' B 701  ACT  H2 ', -0.692, (44.467, -42.698, 16.079)), (' A  13  GLN  HG2', ' A 114  SER  HB2', -0.676, (20.171, 10.866, 21.49)), (' B 430  THR  O  ', ' B 712  GOL  H11', -0.561, (41.707, -25.765, -5.15)), (' B 408  ARG  HG3', ' B 826  HOH  O  ', -0.559, (44.518, -27.377, 13.998)), (' B 453  TYR  OH ', ' B 701  ACT  H3 ', -0.556, (42.575, -42.492, 17.355)), (' B 407  VAL HG12', ' B 707  GOL  H11', -0.547, (42.187, -25.588, 10.323)), (' A  88  PRO  HA ', ' A 113  VAL  HB ', -0.542, (17.874, 5.733, 17.107)), (' B 412  PRO  HG3', ' B 429  PHE  HB3', -0.521, (46.437, -26.318, -0.652)), (' B 408  ARG  HA ', ' B 707  GOL  H12', -0.509, (44.577, -25.809, 10.485)), (' B 493  GLN  NE2', ' B 706  FMT  O2 ', -0.507, (40.641, -47.447, 18.289)), (' A  67  ARG  HD2', ' A  85  SER  HB2', -0.495, (17.868, 10.729, 7.978)), (' A  68  PHE  HA ', ' A  82  GLN  O  ', -0.477, (23.475, 6.772, 4.746)), (' A   1  GLN  HG3', ' B 900  HOH  O  ', -0.477, (40.6, -17.362, 8.687)), (' B 353  TRP  O  ', ' B 704  FMT  H  ', -0.476, (33.258, -38.589, 0.831)), (' B 515  PHE  H  ', ' B 712  GOL  C3 ', -0.472, (38.923, -26.783, -6.97)), (' B 378  LYS  HD2', ' B 707  GOL  H2 ', -0.47, (43.344, -22.381, 7.738)), (' B 714  FMT  H  ', ' B 914  HOH  O  ', -0.46, (19.942, -20.687, -18.133)), (' B 405  ASP  HB2', ' B 408  ARG  NH2', -0.453, (45.902, -29.775, 17.688)), (' A  83  MET  HE1', ' A  94  TYR  CZ ', -0.446, (22.368, 1.694, 11.374)), (' A  67  ARG  CZ ', ' A  87  LYS  HD2', -0.44, (15.479, 7.31, 9.153)), (' A  13  GLN  HA ', ' A 114  SER  HB2', -0.44, (20.15, 10.456, 21.124)), (' A  83  MET  HB3', ' A  86  LEU HD21', -0.435, (22.63, 6.092, 10.149)), (' B 515  PHE  O  ', ' B 712  GOL  H32', -0.43, (39.477, -27.509, -8.23)), (' B 453  TYR  OH ', ' B 493  GLN  HG2', -0.429, (40.648, -43.282, 17.568)), (' A  34 BMET  HB3', ' A  34 BMET  HE2', -0.423, (30.271, -5.42, 1.165)), (' A  33  GLU  HG3', ' A  53  SER  HB2', -0.419, (28.266, -8.49, -7.16)), (' A  -1  SER  HB3', ' B 380  TYR  CE2', -0.418, (46.286, -21.538, 3.336)), (' B 430  THR  H  ', ' B 712  GOL  H11', -0.41, (43.046, -26.385, -5.038)), (' B 493  GLN HE21', ' B 706  FMT  C  ', -0.406, (40.379, -48.178, 17.301)), (' B 354  ASN  O  ', ' B 398  ASP  HA ', -0.406, (33.14, -33.42, 0.988))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
