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
data['rama'] = [('A', '  98 ', 'ARG', 0.023879407274768432, (29.05, 14.285, 30.481))]
data['omega'] = []
data['rota'] = [('A', '  15 ', 'ILE', 0.18464836025075348, (19.963000000000005, 11.367999999999999, 41.54)), ('A', '  78 ', 'GLU', 0.2177148747763204, (9.788000000000004, -12.536, 0.9489999999999997)), ('A', ' 105 ', 'LEU', 0.09027749808553255, (23.872, 7.666000000000002, 19.349999999999994)), ('M', '  21 ', 'VAL', 0.007351242675213143, (3.4370000000000007, 8.756000000000002, 11.375))]
data['cbeta'] = []
data['probe'] = [(' A 272  CYS  HG ', ' A 319  EDO  HO2', -0.863, (33.873, -4.275, 3.492)), (' A 125  VAL HG21', ' A 313  EDO  H11', -0.784, (19.737, 16.923, 24.777)), (' M  57  VAL HG22', ' M 204  EDO  H12', -0.764, (-5.256, 22.86, 40.716)), (' A  90 BASP  OD2', ' A 401  HOH  O  ', -0.718, (26.744, -4.219, 9.281)), (' A 130  ASN HD22', ' M  83  HIS  HD1', -0.679, (5.737, 17.021, 22.729)), (' M 204  EDO  H21', ' M 427  HOH  O  ', -0.67, (-9.145, 22.214, 38.692)), (' A 288  LYS  O  ', ' A 402  HOH  O  ', -0.6, (25.979, -24.859, -5.018)), (' A 272  CYS  SG ', ' A 319  EDO  O2 ', -0.566, (34.174, -3.91, 2.57)), (' A 130  ASN  ND2', ' M  83  HIS  HD1', -0.565, (5.707, 16.829, 22.531)), (' A   3  ASN  N  ', ' A 405  HOH  O  ', -0.545, (11.892, -9.314, 34.859)), (' A 200  LYS  HB3', ' M  21 AVAL HG13', -0.54, (5.577, 8.221, 9.259)), (' A  62  MET  HE3', ' A  72  MET  SD ', -0.539, (8.459, -0.9, 12.879)), (' A  49 AMET  SD ', ' A 316  EDO  H22', -0.527, (6.887, 22.736, 33.748)), (' A   3  ASN  ND2', ' A 408  HOH  O  ', -0.512, (11.423, -7.608, 38.89)), (' M  21 AVAL HG23', ' M 399  HOH  O  ', -0.495, (1.323, 6.335, 10.349)), (' A  52  ARG HH21', ' A 313  EDO  C1 ', -0.476, (20.105, 18.24, 25.233)), (' A 260  TYR  OH ', ' A 289  ARG  NH1', -0.466, (26.098, -20.672, 1.657)), (' A 136  VAL HG12', ' A 313  EDO  H22', -0.449, (22.046, 15.896, 25.34)), (' M  30  TYR  CE2', ' M  35  GLY  HA3', -0.446, (-1.503, -3.838, 21.474)), (' M  39  THR  HA ', ' M 209  EDO  H21', -0.435, (-1.354, 0.061, 32.298)), (' A   3  ASN  HB3', ' A 605  HOH  O  ', -0.435, (14.054, -6.823, 35.205)), (' A 257  HIS  CE1', ' A 264  HIS  HB2', -0.422, (33.555, -9.361, 1.206)), (' A  49 BMET  HB2', ' A  49 BMET  HE2', -0.412, (10.705, 25.221, 37.811)), (' A 260  TYR  HB3', ' A 283  HIS  CD2', -0.412, (29.904, -16.245, -1.072)), (' A  65  GLN  HA ', ' A 317  EDO  H12', -0.407, (1.78, -7.866, 12.824)), (' A 130  ASN HD21', ' M  83  HIS  H  ', -0.406, (5.435, 16.802, 21.164))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
