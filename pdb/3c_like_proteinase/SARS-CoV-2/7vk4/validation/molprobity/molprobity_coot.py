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
data['rama'] = [('A', '  84 ', 'ASN', 0.04424654872448304, (-25.08, 12.627, -34.743)), ('B', '  84 ', 'ASN', 0.029248930184578373, (10.193, 4.0859999999999985, 12.068))]
data['omega'] = []
data['rota'] = [('A', '   4 ', 'ARG', 0.035682775911541606, (6.734, 4.7, -17.674)), ('B', '  82 ', 'MET', 0.16294104750662963, (8.021999999999997, 9.272999999999998, 14.212)), ('B', '  86 ', 'VAL', 0.05594834752359623, (7.526, 7.868000000000001, 8.487)), ('B', ' 165 ', 'MET', 0.19143864240948402, (14.325, 7.286, -2.476))]
data['cbeta'] = [('A', '   4 ', 'ARG', ' ', 0.3510260752043893, (5.963, 4.227, -16.418)), ('A', '  84 ', 'ASN', ' ', 0.3201712009322938, (-23.66, 13.142, -34.983))]
data['probe'] = [(' B   3  PHE  O  ', ' B 401  HOH  O  ', -1.1, (-3.263, -5.593, -24.395)), (' B 155  ASP  HB2', ' B 402  HOH  O  ', -0.985, (-16.624, 2.322, -0.921)), (' A 211  ALA  HA ', ' A 282  LEU HD11', -0.841, (15.917, 8.089, -24.385)), (' A   4  ARG  NH1', ' B 127  GLN  O  ', -0.834, (2.884, 0.012, -14.591)), (' A 107  GLN  N  ', ' A 110  GLN  OE1', -0.784, (-5.961, 13.767, -32.898)), (' A 140  PHE  HB2', ' A 172  HIS  CE1', -0.779, (-13.385, -2.372, -25.637)), (' B 140  PHE  HB2', ' B 172  HIS  CE1', -0.746, (10.638, 8.318, -9.15)), (' A 231  ASN  O  ', ' A 235  MET  HG2', -0.707, (7.978, 5.436, -47.523)), (' A  58  LEU HD11', ' A  80  HIS  CD2', -0.69, (-36.09, 11.559, -27.968)), (' B 155  ASP  CB ', ' B 402  HOH  O  ', -0.68, (-16.876, 2.132, -1.167)), (' B  21  THR  HB ', ' B  67  LEU  HB2', -0.644, (5.89, 24.116, 4.401)), (' B 249  ILE  CG2', ' B 294  PHE  HE1', -0.629, (-3.24, -16.036, -7.359)), (' A 114  VAL HG11', ' A 140  PHE  HZ ', -0.628, (-11.955, 3.385, -23.064)), (' B 288  GLU  OE1', ' B 290  GLU  N  ', -0.585, (4.555, -8.153, -15.764)), (' B 245  ASP  O  ', ' B 249  ILE HG12', -0.556, (-0.751, -20.659, -5.368)), (' A 166  GLU  HG3', ' A 172  HIS  CD2', -0.549, (-13.406, -3.951, -29.065)), (' A 114  VAL HG11', ' A 140  PHE  CZ ', -0.537, (-11.418, 2.823, -23.088)), (' A  58  LEU HD11', ' A  80  HIS  HD2', -0.514, (-35.169, 11.992, -27.95)), (' B 249  ILE  CG2', ' B 294  PHE  CE1', -0.514, (-3.807, -15.668, -7.047)), (' A 211  ALA  HA ', ' A 282  LEU  CD1', -0.505, (16.25, 7.399, -24.03)), (' B  27  LEU HD21', ' B  42  VAL  HB ', -0.502, (9.833, 15.129, 3.847)), (' B  27  LEU HD13', ' B  39  PRO  HD2', -0.497, (7.31, 13.144, 1.939)), (' B  17  MET  HG3', ' B 117  CYS  SG ', -0.491, (-0.758, 12.953, -4.953)), (' B 199  THR HG21', ' B 239  TYR  CZ ', -0.491, (10.446, -14.608, -17.019)), (' A  55  GLU  CD ', ' A  55  GLU  H  ', -0.49, (-33.5, 7.326, -37.56)), (' B 262  LEU  N  ', ' B 262  LEU HD12', -0.489, (0.704, -27.931, -13.59)), (' B 140  PHE  HD1', ' B 144  SER  HB2', -0.482, (7.093, 10.161, -7.483)), (' A  58  LEU  CD1', ' A  80  HIS  CD2', -0.47, (-35.779, 10.874, -27.954)), (' A 188  ARG  CZ ', ' A 190  THR HG21', -0.468, (-25.049, -2.474, -42.595)), (' A  76  ARG  NH2', ' A  78  ILE HD11', -0.467, (-40.088, 17.362, -15.426)), (' A 298  ARG  HG2', ' A 298  ARG  O  ', -0.461, (5.474, 19.032, -20.017)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.46, (-0.23, 7.938, -33.062)), (' B 140  PHE  HB3', ' B 144  SER  OG ', -0.459, (9.094, 11.006, -8.082)), (' B 165 AMET  HB2', ' B 165 AMET  HE2', -0.454, (15.399, 4.83, -2.151)), (' B 294  PHE  CD1', ' B 294  PHE  N  ', -0.449, (-4.461, -13.112, -8.644)), (' A  13  VAL HG21', ' A 150  PHE  CD1', -0.448, (-11.273, 11.291, -18.021)), (' A 106  ILE  HB ', ' A 110  GLN  OE1', -0.443, (-6.356, 13.852, -31.425)), (' B 249  ILE HG21', ' B 294  PHE  HE1', -0.433, (-2.736, -15.819, -6.85)), (' B 282  LEU  HA ', ' B 282  LEU HD23', -0.431, (-2.56, -11.178, -27.269)), (' A  78  ILE  HA ', ' A  78  ILE HD12', -0.428, (-38.205, 15.345, -17.82)), (' B 130  MET  HE1', ' B 182  TYR  CG ', -0.427, (7.801, -2.776, -0.543)), (' A  13  VAL HG21', ' A 150  PHE  CE1', -0.421, (-11.086, 10.834, -17.43)), (' A 273  GLN  HG3', ' A 274  ASN  OD1', -0.418, (20.585, -3.042, -39.839)), (' A 272  LEU  HA ', ' A 272  LEU HD23', -0.407, (13.207, -1.331, -37.347)), (' B 114  VAL HG11', ' B 140  PHE  CZ ', -0.406, (4.813, 5.902, -7.486))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
