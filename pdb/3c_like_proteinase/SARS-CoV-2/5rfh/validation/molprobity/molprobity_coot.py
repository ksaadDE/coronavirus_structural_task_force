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
data['rama'] = [('A', '  25 ', 'THR', 0.016083749097470144, (3.6830000000000016, -10.757000000000003, 26.003000000000004)), ('A', ' 154 ', 'TYR', 0.013135945856020695, (10.442999999999998, -11.584, -9.35))]
data['omega'] = [('A', '  26 ', 'THR', None, (3.835000000000001, -10.472000000000003, 23.592)), ('A', ' 165 ', 'MET', None, (11.602000000000002, -0.214, 17.243))]
data['rota'] = [('A', '   1 ', 'SER', 0.2104847837203481, (-2.018, 5.561000000000002, -16.439)), ('A', '  72 ', 'ASN', 0.07972230133282769, (-2.6839999999999984, -22.386000000000003, 15.51)), ('A', ' 216 ', 'ASP', 0.22736945832274522, (0.8039999999999998, 16.193, -14.779))]
data['cbeta'] = []
data['probe'] = [(' A 217  ARG  NH2', ' A 501  HOH  O  ', -0.818, (3.531, 12.384, -21.981)), (' A 110  GLN  HG3', ' A 683  HOH  O  ', -0.73, (19.413, 0.528, -1.657)), (' A  19  GLN HE21', ' A 119  ASN  HB3', -0.711, (-0.015, -13.58, 18.621)), (' A 165  MET  HB3', ' A 173  ALA  HB3', -0.686, (13.873, 1.877, 16.346)), (' A 403  DMS  H23', ' A 687  HOH  O  ', -0.612, (3.45, -21.429, 7.337)), (' A 288  GLU  OE1', ' A 502  HOH  O  ', -0.58, (5.699, 10.416, -1.655)), (' A  19  GLN  HG3', ' A  26  THR  CG2', -0.555, (2.352, -13.313, 19.131)), (' A  70  ALA  O  ', ' A  73 AVAL HG12', -0.548, (1.489, -22.961, 13.061)), (' A 236  LYS  HD3', ' A 793  HOH  O  ', -0.538, (17.98, 28.993, -1.512)), (' A 118  TYR  CE1', ' A 144  SER  HB3', -0.535, (1.963, -3.35, 15.239)), (' A 298  ARG  HD2', ' A 402  DMS  O  ', -0.526, (7.76, -1.819, -8.477)), (' A  19  GLN  NE2', ' A 119  ASN  HB3', -0.513, (-0.234, -13.719, 18.615)), (' A 298  ARG  HG3', ' A 303  VAL  HB ', -0.512, (8.473, -3.667, -12.361)), (' A  52  PRO  HD2', ' A 188  ARG  HG3', -0.508, (18.491, 0.02, 27.383)), (' A  86  VAL HG13', ' A 179  GLY  HA2', -0.502, (18.292, -7.998, 14.226)), (' A  19  GLN  HG3', ' A  26  THR HG21', -0.484, (2.23, -13.136, 19.629)), (' A  19  GLN  CG ', ' A  26  THR  CG2', -0.471, (2.733, -13.321, 19.712)), (' A  40  ARG  HA ', ' A  87  LEU  HG ', -0.464, (16.067, -11.394, 20.555)), (' A 101  TYR  HA ', ' A 157  VAL  O  ', -0.453, (14.283, -13.024, -0.351)), (' A 286  LEU  C  ', ' A 286  LEU HD12', -0.423, (4.636, 16.53, -1.664)), (' A  19  GLN  CG ', ' A  26  THR HG21', -0.421, (2.329, -13.7, 19.54)), (' A  41  HIS  HE1', ' A 164  HIS  O  ', -0.414, (11.481, -2.554, 19.352)), (' A  31  TRP  CD2', ' A  95  ASN  HB2', -0.408, (8.895, -21.403, 8.712)), (' A  73 AVAL  CG1', ' A  73 AVAL  O  ', -0.405, (2.065, -23.859, 14.423)), (' A 262  LEU  HA ', ' A 262  LEU HD23', -0.402, (19.762, 18.972, -13.671)), (' A  50  LEU  O  ', ' A 188  ARG  NE ', -0.402, (18.734, 2.497, 28.884)), (' A 117  CYS  O  ', ' A 144  SER  HA ', -0.401, (2.96, -5.875, 14.833))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
