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
data['probe'] = [(' B   6  PHE  CE1', ' B  30  VAL HG11', -0.725, (38.385, 25.349, 9.736)), (' B 137  ILE HD13', ' B 164  LEU HD23', -0.703, (39.233, 13.362, 26.323)), (' A 131  ILE HG22', ' A 201  EDO  H21', -0.679, (20.455, 46.504, 35.61)), (' B   2  MET  HA ', ' B   2  MET  HE2', -0.678, (35.37, 35.118, 2.84)), (' E 137  ILE HD13', ' E 164  LEU HD23', -0.673, (53.294, -19.46, 24.839)), (' D   1  HIS  NE2', ' D   3  VAL HG22', -0.635, (24.564, 78.38, 21.622)), (' A 132  PHE  CE1', ' A 202  EDO  H11', -0.606, (22.186, 51.612, 35.149)), (' B 101  ASN  OD1', ' E  47  GLY  CA ', -0.578, (44.431, -0.8, 21.066)), (' A  11  LYS  HE3', ' B 316  HOH  O  ', -0.545, (39.269, 32.349, 16.392)), (' C  90  LYS  HG2', ' C  91  HIS  CD2', -0.537, (14.568, 25.814, 33.097)), (' B 101  ASN  OD1', ' E  47  GLY  HA3', -0.526, (44.782, -0.498, 21.247)), (' B 135  ASP  H  ', ' B 202  EDO  H11', -0.489, (45.79, 6.442, 24.943)), (' A  80  SER  HA ', ' A  94  HIS  O  ', -0.487, (33.114, 54.413, 29.956)), (' E  80  SER  HA ', ' E  94  HIS  O  ', -0.483, (39.668, -6.164, 37.198)), (' A   9  TYR  HB3', ' A  17  TYR  HB3', -0.481, (34.84, 33.171, 24.076)), (' D   6  PHE  CE1', ' D  30  VAL HG11', -0.469, (30.305, 75.374, 12.62)), (' B  99  ASN  ND2', ' B 102  LYS  HD3', -0.469, (48.318, 0.017, 14.211)), (' C   9  TYR  HB3', ' C  17  TYR  HB3', -0.461, (23.35, 9.338, 41.882)), (' D  80  SER  HA ', ' D  94  HIS  O  ', -0.46, (41.86, 62.63, 18.806)), (' A 159  ASN  OD1', ' C  90  LYS  HG3', -0.459, (16.531, 27.916, 31.503)), (' A 132  PHE  HE1', ' A 202  EDO  H11', -0.451, (21.316, 51.85, 35.564)), (' D   1  HIS  NE2', ' D   3  VAL  CG2', -0.447, (25.139, 78.275, 21.524)), (' B   9  TYR  HB3', ' B  17  TYR  HB3', -0.446, (37.228, 26.337, 18.493)), (' C  80  SER  HA ', ' C  94  HIS  O  ', -0.441, (8.758, 25.537, 46.27)), (' B  80  SER  HA ', ' B  94  HIS  O  ', -0.439, (52.175, 13.602, 7.812)), (' E   6  PHE  CE1', ' E  30  VAL HG11', -0.437, (32.92, -19.813, 26.155)), (' D   9  TYR  HB3', ' D  17  TYR  HB3', -0.431, (26.257, 71.789, 5.709)), (' C   4  ASN  HB2', ' C   6  PHE  CE2', -0.418, (21.467, 16.14, 35.398)), (' D  75  LEU  N  ', ' D  75  LEU HD12', -0.411, (48.37, 60.35, 21.537)), (' C  29  LYS  HG3', ' C 365  HOH  O  ', -0.411, (31.674, 22.62, 40.01)), (' A 159  ASN  ND2', ' C  90  LYS  O  ', -0.408, (16.354, 29.18, 33.991)), (' E   9  TYR  HB3', ' E  17  TYR  HB3', -0.404, (40.204, -25.379, 26.063)), (' A 131  ILE  HA ', ' A 131  ILE HD12', -0.402, (16.352, 46.643, 35.52))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
