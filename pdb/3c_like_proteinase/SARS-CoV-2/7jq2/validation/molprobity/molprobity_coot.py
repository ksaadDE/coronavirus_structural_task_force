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
data['rama'] = [('A', ' 154 ', 'TYR', 0.027054085189141604, (11.205000000000007, -10.296, -8.104)), ('A', ' 217 ', 'ARG', 0.013887694050170235, (6.173, 20.509, 0.30600000000000005))]
data['omega'] = [('A', ' 294 ', 'PHE', None, (10.566000000000003, 5.189, -10.876))]
data['rota'] = []
data['cbeta'] = [('A', '  47 ', 'GLU', ' ', 0.35120042327706663, (54.408, -0.744, -19.395)), ('A', ' 294 ', 'PHE', ' ', 0.30437134693725704, (10.253, 2.892000000000001, -11.777000000000001))]
data['probe'] = [(' A   4  ARG  NH1', ' A 505  HOH  O  ', -0.658, (19.416, 7.759, 6.522)), (' A 221  ASN HD22', ' A 270  GLU  HG3', -0.638, (7.184, 29.1, -8.877)), (' A 167  LEU  HB3', ' A 168  PRO  HD2', -0.592, (37.612, 10.603, -17.222)), (' A 217  ARG HH11', ' A 220  LEU HD12', -0.579, (1.762, 20.797, -2.033)), (' A 222  ARG  NH2', ' A 508  HOH  O  ', -0.578, (-2.054, 30.027, -11.199)), (' A  72  ASN  O  ', ' A  74  GLN  HG3', -0.577, (39.135, -22.797, -4.391)), (' A  66  PHE  CE1', ' A  87  LEU HD21', -0.577, (41.903, -13.747, -19.52)), (' A 168  PRO  HB3', ' A 401  VHM  C2 ', -0.555, (42.358, 12.139, -17.232)), (' A  51  ASN  OD1', ' A 502  HOH  O  ', -0.545, (46.278, 1.241, -27.827)), (' A  69  GLN  HG2', ' A  74  GLN  HG2', -0.543, (39.575, -20.684, -5.544)), (' A 240  GLU  OE1', ' A 503  HOH  O  ', -0.533, (16.413, 12.395, -19.485)), (' A  27  LEU HD13', ' A  39  PRO  HD2', -0.519, (38.047, -8.04, -14.037)), (' A 221  ASN  ND2', ' A 270  GLU  HG3', -0.497, (6.85, 28.591, -9.117)), (' A 191  ALA  HA ', ' A 401  VHM  C3 ', -0.489, (42.363, 10.679, -19.067)), (' A 293  PRO  HB2', ' A 294  PHE  HD1', -0.487, (9.323, 5.652, -12.843)), (' A 293  PRO  HB2', ' A 294  PHE  CD1', -0.483, (9.027, 6.158, -13.331)), (' A 222  ARG  HG3', ' A 222  ARG  O  ', -0.47, (-0.231, 30.452, -9.057)), (' A 191  ALA  HA ', ' A 401  VHM  C2 ', -0.469, (42.894, 11.062, -19.429)), (' A  69  GLN  HG2', ' A  74  GLN  CD ', -0.461, (40.616, -20.481, -5.179)), (' A  95  ASN  HB3', ' A  98  THR  OG1', -0.448, (25.742, -20.13, -11.637)), (' A  86  VAL HG13', ' A 179  GLY  HA2', -0.445, (32.638, -6.382, -21.509)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.432, (19.432, 9.791, -15.067)), (' A 266  ALA  O  ', ' A 270  GLU  HG2', -0.432, (8.235, 27.252, -10.544)), (' A 305  PHE  O  ', ' A 306  GLN  HB2', -0.43, (12.58, -11.593, -1.971)), (' A  70  ALA  O  ', ' A  73  VAL  HB ', -0.426, (34.982, -21.139, -4.128)), (' A 154  TYR  H  ', ' A 305  PHE  HD1', -0.423, (11.792, -8.195, -7.987)), (' A 166  GLU  O  ', ' A 401  VHM  N10', -0.421, (40.722, 6.423, -14.868)), (' A 292  THR  C  ', ' A 294  PHE  N  ', -0.421, (11.306, 6.039, -10.808)), (' A 249  ILE HG23', ' A 294  PHE  HE1', -0.42, (8.693, 6.103, -15.345)), (' A  17  MET  HG3', ' A 117  CYS  SG ', -0.415, (31.237, -9.02, -5.566)), (' A  69  GLN  HG2', ' A  74  GLN  CG ', -0.413, (40.11, -20.986, -5.308))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
