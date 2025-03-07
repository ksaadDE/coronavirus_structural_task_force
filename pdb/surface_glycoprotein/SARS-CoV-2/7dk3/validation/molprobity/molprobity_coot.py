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
data['rama'] = [('A', ' 445 ', 'VAL', 0.017950951477131997, (197.01, 178.241, 141.832)), ('B', ' 445 ', 'VAL', 0.016933285103964173, (192.979, 207.81, 139.221))]
data['omega'] = []
data['rota'] = [('C', ' 822 ', 'LEU', 0.21619702668889182, (177.736, 211.577, 231.30299999999997))]
data['cbeta'] = []
data['probe'] = [(' A 455  LEU  O  ', ' A 455  LEU HD23', -0.704, (184.039, 183.685, 161.013)), (' A 501  ASN  HB3', ' A 505  TYR  HB2', -0.605, (196.312, 187.314, 149.186)), (' B  24  LEU  H  ', ' B  24  LEU HD23', -0.591, (173.768, 147.656, 188.64)), (' C 294  ASP  HB2', ' C 295  PRO  HD2', -0.56, (185.854, 235.659, 203.204)), (' B 501  ASN  HB3', ' B 505  TYR  HB2', -0.545, (200.495, 205.237, 148.265)), (' A 189  LEU  C  ', ' A 189  LEU HD13', -0.524, (252.277, 220.898, 190.329)), (' B 294  ASP  HB2', ' B 295  PRO  HD2', -0.509, (182.545, 172.612, 210.794)), (' C 189  LEU  C  ', ' C 189  LEU HD13', -0.494, (162.033, 233.083, 188.506)), (' B  24  LEU  N  ', ' B  24  LEU HD23', -0.486, (173.507, 147.639, 189.079)), (' C1038  LYS  HD2', ' C1038  LYS  N  ', -0.481, (199.113, 208.514, 249.246)), (' A 192  PHE  HA ', ' A 204  TYR  O  ', -0.471, (244.941, 218.387, 186.274)), (' A 422  ASN  OD1', ' A 423  TYR  N  ', -0.465, (191.836, 179.461, 165.942)), (' C  24  LEU  C  ', ' C  24  LEU HD12', -0.461, (172.317, 249.947, 178.738)), (' C 916  LEU  O  ', ' C 920  GLN  N  ', -0.459, (183.281, 218.132, 261.086)), (' C 328  ARG  HB2', ' C 543  PHE  CD1', -0.456, (219.565, 233.975, 183.449)), (' A  24  LEU  C  ', ' A  24  LEU HD12', -0.449, (262.081, 201.547, 184.342)), (' B 916  LEU  O  ', ' B 920  GLN  N  ', -0.448, (206.72, 188.366, 265.342)), (' A 559  PHE  CD1', ' A 559  PHE  N  ', -0.445, (214.864, 164.257, 199.876)), (' B 520  ALA  HB1', ' B 521  PRO  HD2', -0.443, (171.276, 210.99, 180.599)), (' B 422  ASN  OD1', ' B 423  TYR  N  ', -0.442, (194.072, 216.333, 162.845)), (' C 435  ALA  HA ', ' C 509  ARG  O  ', -0.441, (223.347, 233.538, 147.233)), (' C 411  ALA  HB3', ' C 414  GLN  HG3', -0.439, (213.799, 221.302, 144.865)), (' C 105  ILE  O  ', ' C 238  PHE  HA ', -0.439, (172.32, 233.204, 171.586)), (' B1076  THR  O  ', ' B1097  SER  N  ', -0.435, (184.638, 199.494, 270.925)), (' A 445  VAL HG12', ' A 446  GLY  N  ', -0.434, (194.722, 178.312, 141.039)), (' B 445  VAL HG12', ' B 446  GLY  N  ', -0.432, (194.307, 209.519, 138.311)), (' C 379  CYS  SG ', ' C 384  PRO  HD3', -0.432, (214.652, 230.373, 156.667)), (' B  97  LYS  HB3', ' B 182  LYS  HB2', -0.43, (191.821, 137.556, 197.566)), (' C 393  THR  HA ', ' C 522  ALA  HA ', -0.428, (226.363, 218.834, 167.626)), (' B  85  PRO  HA ', ' B 237  ARG  HD3', -0.425, (182.077, 160.676, 181.747)), (' B 865  LEU  HG ', ' B 870  ILE HG13', -0.423, (221.552, 191.569, 232.481)), (' A 379  CYS  HA ', ' A 432  CYS  HA ', -0.422, (207.655, 184.433, 172.004)), (' B 490  PHE  CE2', ' B 492  LEU  HB3', -0.422, (194.448, 224.743, 151.697)), (' A 517  LEU  HG ', ' A 518  LEU  HG ', -0.422, (211.071, 177.121, 185.825)), (' B 517  LEU  HG ', ' B 518  LEU  HG ', -0.42, (179.159, 204.213, 182.487)), (' A 520  ALA  HB1', ' A 521  PRO  HD2', -0.417, (209.791, 166.68, 186.595)), (' A 916  LEU  O  ', ' A 920  GLN  N  ', -0.415, (221.606, 223.91, 260.665)), (' A 715  PRO  O  ', ' A1110  TYR  N  ', -0.415, (223.575, 209.668, 262.709)), (' C 347  PHE  CD2', ' C 399  SER  HB2', -0.414, (230.796, 230.701, 148.76)), (' A 359  SER  HA ', ' A 524  VAL  CG2', -0.411, (212.618, 167.722, 176.237)), (' B  41  LYS  HD2', ' B  41  LYS  N  ', -0.411, (206.746, 167.38, 191.999)), (' B 212  LEU HD22', ' B 217  PRO  HD3', -0.409, (189.554, 149.142, 203.951)), (' A 149  ASN  O  ', ' A 151  SER  N  ', -0.406, (270.71, 230.673, 173.886)), (' B 359  SER  HA ', ' B 524  VAL  CG2', -0.406, (171.714, 206.048, 171.454)), (' B 715  PRO  O  ', ' B1110  TYR  N  ', -0.405, (192.821, 193.261, 264.706)), (' B 566  GLY  HA2', ' C  43  PHE  HB3', -0.404, (169.764, 209.196, 194.148)), (' C 318  PHE  N  ', ' C 593  GLY  O  ', -0.404, (199.951, 229.445, 202.849)), (' B 379  CYS  HA ', ' B 432  CYS  HA ', -0.404, (188.893, 200.811, 170.773)), (' C 359  SER  HA ', ' C 524  VAL HG23', -0.403, (229.895, 223.716, 164.796)), (' A 896  ILE  O  ', ' A 901  GLN  NE2', -0.402, (208.643, 229.591, 253.366)), (' A 193  VAL  HB ', ' A 204  TYR  HB2', -0.402, (241.264, 217.093, 187.079)), (' B 435  ALA  HA ', ' B 509  ARG  O  ', -0.401, (189.277, 202.614, 159.385)), (' A 435  ALA  HA ', ' A 509  ARG  O  ', -0.4, (205.169, 182.071, 160.582)), (' C  24  LEU  O  ', ' C  24  LEU HD12', -0.4, (172.81, 249.897, 178.41)), (' A 294  ASP  HB2', ' A 295  PRO  CD ', -0.4, (240.526, 200.107, 208.343))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
