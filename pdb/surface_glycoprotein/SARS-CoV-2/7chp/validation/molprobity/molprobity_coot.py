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
data['rama'] = [('H', ' 136 ', 'SER', 0.0037113886197116465, (8.267000000000003, 89.061, 17.93)), ('H', ' 219 ', 'LYS', 0.018949748466383882, (11.104000000000003, 79.63299999999997, 33.163999999999994)), ('L', '  84 ', 'ALA', 0.03991497498088656, (3.467, 57.817, -4.256999999999998))]
data['omega'] = [('H', ' 151 ', 'PRO', None, (7.476999999999999, 48.31099999999999, 21.015)), ('H', ' 153 ', 'PRO', None, (4.155000000000002, 51.184, 16.86799999999999)), ('L', '   8 ', 'PRO', None, (12.211000000000007, 53.504, -13.582999999999997)), ('L', '  95 ', 'PRO', None, (2.992000000000001, 28.248, -9.560999999999996)), ('L', ' 143 ', 'PRO', None, (15.668000000000001, 71.159, -2.0789999999999993))]
data['rota'] = [('H', ' 117 ', 'SER', 0.09405384095519355, (12.424, 38.786999999999985, 21.612999999999996))]
data['cbeta'] = []
data['probe'] = [(' H 167  VAL HG22', ' H 186  VAL HG12', -0.767, (2.324, 70.972, 14.973)), (' L  24  ARG  NH1', ' L  70  ASP  OD2', -0.673, (12.356, 46.025, -21.947)), (' L 157  GLN  OE1', ' L 301  HOH  O  ', -0.617, (31.673, 65.108, 19.569)), (' L  23  CYS  HG ', ' L  88  CYS  HG ', -0.601, (5.726, 44.921, -13.313)), (' L  37  GLN  HB2', ' L  47  LEU HD11', -0.595, (-1.165, 54.727, -8.688)), (' E 357  ARG  HD2', ' E 359  SER  HB2', -0.518, (-19.608, 5.217, -27.896)), (' L   1  ASP  OD2', ' L 302  HOH  O  ', -0.492, (9.462, 32.559, -6.109)), (' H 166  GLY  N  ', ' H 308  HOH  O  ', -0.485, (0.605, 72.805, 8.971)), (' H 163  LEU  O  ', ' H 301  HOH  O  ', -0.481, (-2.78, 68.538, 15.383)), (' L   8  PRO  HG3', ' L  11  LEU HD13', -0.449, (12.26, 57.355, -13.673)), (' L 186  ALA  O  ', ' L 190  LYS  HG3', -0.445, (30.643, 66.66, 31.375)), (' E 339  GLY  O  ', ' E 343  ASN  HB2', -0.444, (-8.879, 15.38, -36.534)), (' L  58  VAL  O  ', ' L 303  HOH  O  ', -0.44, (-10.762, 57.044, -14.446)), (' L  47  LEU  HA ', ' L  58  VAL HG21', -0.436, (-6.536, 53.161, -10.597)), (' E 455  LEU HD11', ' H 100  GLN  HG3', -0.426, (-10.616, 35.028, -10.184)), (' L  54  LEU  HA ', ' L  54  LEU HD12', -0.425, (-7.064, 52.471, -15.338)), (' H 195  THR  OG1', ' H 196  GLN  N  ', -0.424, (-2.081, 82.336, 23.655)), (' H 218  LYS  HG2', ' H 219  LYS  H  ', -0.424, (12.005, 76.935, 32.307)), (' H 203  ASN  ND2', ' H 210  LYS  HE3', -0.423, (-4.296, 56.645, 23.054)), (' L 142  TYR  CG ', ' L 143  PRO  HA ', -0.422, (13.421, 70.04, -2.621)), (' E 399  SER  HA ', ' E 510  VAL  O  ', -0.42, (-10.14, 18.195, -25.009)), (' L  61  ARG  CZ ', ' L  79  GLN  HG3', -0.413, (-3.998, 64.462, -12.153)), (' H   4  LEU HD21', ' H  27  PHE  HZ ', -0.409, (-13.32, 42.48, 2.068)), (' L   9  SER  O  ', ' L 104  THR  HA ', -0.408, (10.613, 53.298, -7.731)), (' H 172  ALA  HA ', ' H 182  LEU  HB3', -0.406, (10.946, 58.396, 15.697)), (' L  83  PHE  O  ', ' L  84  ALA  HB2', -0.403, (1.474, 58.542, -4.251))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
