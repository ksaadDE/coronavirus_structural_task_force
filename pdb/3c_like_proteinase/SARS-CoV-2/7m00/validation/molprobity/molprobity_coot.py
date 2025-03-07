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
data['rama'] = [('B', ' 277 ', 'ASN', 0.02401382527464228, (-0.11299999999999955, 27.286999999999995, 27.453000000000007))]
data['omega'] = []
data['rota'] = [('A', ' 104 ', 'VAL', 0.29037815827034097, (8.025999999999998, -8.426000000000005, 48.089000000000006)), ('A', ' 125 ', 'VAL', 0.23901830877705596, (2.3900000000000023, -4.838, 29.82)), ('B', '  26 ', 'THR', 0.07315783025898945, (26.992, -12.388, 18.203)), ('B', '  49 ', 'MET', 0.11821096262999808, (31.049999999999997, -3.342000000000002, 8.411)), ('B', ' 228 ', 'ASN', 0.2914427919803069, (-9.245, 21.165000000000006, 3.521)), ('B', ' 238 ', 'ASN', 0.18591892154634215, (4.650999999999999, 19.045, 9.183)), ('B', ' 274 ', 'ASN', 0.23896305345469018, (-1.516, 28.373, 20.153))]
data['cbeta'] = []
data['probe'] = [(' A 285  ALA  HB3', ' B 285  ALA  HB3', -0.687, (5.434, 18.39, 27.518)), (' B 198  THR HG22', ' B 238  ASN  OD1', -0.574, (6.261, 17.08, 7.634)), (' A 276  MET  HE3', ' A 281  ILE HG13', -0.566, (13.884, 19.015, 28.519)), (' B  44  CYS  HB2', ' B  49  MET  HE2', -0.55, (29.29, -6.929, 10.814)), (' A  30  LEU HD21', ' A  32  LEU HD11', -0.515, (2.078, -14.935, 41.753)), (' A  86  VAL HG13', ' A 179  GLY  HA2', -0.513, (-4.106, -8.892, 48.994)), (' B 276  MET  O  ', ' B 279  ARG  N  ', -0.507, (-0.479, 24.045, 29.003)), (' A 261  VAL HG23', ' A 561  HOH  O  ', -0.498, (27.361, 12.559, 42.065)), (' B 276  MET  O  ', ' B 278  GLY  N  ', -0.496, (0.236, 25.447, 28.141)), (' B  52  PRO  HG2', ' B  54  TYR  CE2', -0.496, (26.919, -5.472, 3.688)), (' A  52  PRO  HG2', ' A  54  TYR  CE2', -0.486, (-15.616, -5.065, 51.722)), (' B  95  ASN  HB3', ' B  98  THR  OG1', -0.48, (9.353, -23.289, 16.492)), (' B  27  LEU HD21', ' B  42  VAL  HB ', -0.462, (24.318, -11.254, 12.761)), (' B 199  THR HG21', ' B 239  TYR  CZ ', -0.461, (1.577, 16.07, 14.806)), (' B 239  TYR  CZ ', ' B 272  LEU HD21', -0.444, (0.006, 19.112, 15.46)), (' A 113  SER  O  ', ' A 149  GLY  HA2', -0.432, (3.8, -5.289, 37.377)), (' B 127  GLN  HG2', ' B 533  HOH  O  ', -0.428, (1.663, 1.529, 21.176)), (' A 263  ASP  O  ', ' A 266  ALA  HB3', -0.428, (24.153, 21.509, 38.669)), (' B  30  LEU HD21', ' B  32  LEU HD11', -0.421, (9.836, -15.207, 13.976)), (' A  55  GLU  O  ', ' A  59  ILE HG12', -0.416, (-17.908, -14.621, 57.148)), (' A 221  ASN  C  ', ' A 221  ASN  OD1', -0.411, (25.222, 24.599, 35.642)), (' B 154  TYR  CB ', ' B 516  HOH  O  ', -0.41, (-6.153, -14.82, 16.744)), (' A 199  THR HG21', ' A 239  TYR  CZ ', -0.408, (10.18, 16.419, 40.353)), (' B  86  VAL HG13', ' B 179  GLY  HA2', -0.405, (15.967, -9.394, 6.733)), (' A 239  TYR  CZ ', ' A 272  LEU HD21', -0.4, (11.412, 19.188, 39.931)), (' B 113  SER  O  ', ' B 149  GLY  HA2', -0.4, (7.631, -6.068, 17.89))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
