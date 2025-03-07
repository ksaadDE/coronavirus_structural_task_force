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
data['rota'] = [('A', '  22 ', 'CYS', 0.2672380583911825, (-33.669, 0.313, -20.477)), ('A', '  24 ', 'THR', 0.014447480649627236, (-33.061, -5.91, -20.079000000000004)), ('A', '  45 ', 'THR', 0.16634737356095325, (-33.119, -5.468, -27.605)), ('A', '  46 ', 'SER', 0.05731098526755034, (-30.858000000000008, -8.223000000000003, -29.178)), ('A', '  59 ', 'ILE', 0.006484894544762176, (-40.15, 7.762, -30.346000000000004)), ('A', ' 102 ', 'LYS', 0.0005411026382420654, (-14.833999999999996, 20.214, -22.721)), ('A', ' 121 ', 'SER', 0.14938206594703032, (-18.856, 1.828, -10.777)), ('A', ' 169 ', 'THR', 0.006674789062494013, (-9.272, -8.805, -33.79)), ('A', ' 235 ', 'MET', 0.0, (6.636, 2.152000000000001, -44.986)), ('A', ' 269 ', 'LYS', 0.009423154998315607, (15.952, 2.996000000000001, -39.509)), ('B', '  24 ', 'THR', 0.22095956824695137, (14.005999999999997, 24.761, 1.751)), ('B', '  46 ', 'SER', 0.16026861570722659, (21.407999999999994, 19.203, 2.146)), ('B', '  51 ', 'ASN', 0.09294845272328021, (24.789, 11.684, 8.096)), ('B', '  57 ', 'LEU', 0.011620691586360183, (16.971999999999994, 17.214, 14.253)), ('B', '  86 ', 'VAL', 0.1486720945660385, (7.7109999999999985, 8.48, 8.724)), ('B', ' 121 ', 'SER', 0.04111350247990243, (-1.177, 17.772, -6.73)), ('B', ' 177 ', 'LEU', 0.10270029778102145, (3.064000000000001, 3.809000000000001, 6.155)), ('B', ' 196 ', 'THR', 0.21356994760009662, (20.329, -8.737, -8.184)), ('B', ' 225 ', 'THR', 0.2841371873300951, (7.468, -31.40700000000001, -16.144)), ('B', ' 227 ', 'LEU', 0.2381750258869973, (8.556, -28.805999999999997, -9.812)), ('B', ' 232 ', 'LEU', 0.1308135459152094, (16.495, -26.36300000000001, -11.554)), ('B', ' 257 ', 'THR', 0.012360611102634781, (-8.022, -23.464, -19.771))]
data['cbeta'] = [('A', ' 127 ', 'GLN', ' ', 0.261370465465528, (-2.202, 5.331, -21.385000000000005))]
data['probe'] = [(' B 257  THR HG23', ' B 259  ILE HG12', -0.898, (-5.378, -23.764, -20.783)), (' A   4  ARG  H  ', ' A 299  GLN HE22', -0.89, (6.36, 6.886, -17.305)), (' A 189  GLN  HG2', ' A 189  GLN  O  ', -0.732, (-23.954, -8.664, -36.479)), (' B  49  MET  HA ', ' B  49  MET  HE3', -0.684, (19.925, 14.078, 4.515)), (' B 257  THR HG23', ' B 259  ILE  CG1', -0.672, (-4.636, -23.987, -20.987)), (' B 260  ALA  HB3', ' B 263  ASP  HB2', -0.637, (-0.209, -29.585, -17.931)), (' B 253  LEU  O  ', ' B 257  THR  HB ', -0.634, (-6.392, -21.989, -17.476)), (' A 140  PHE  O  ', ' B   1  SER  N  ', -0.606, (-13.496, -7.219, -23.974)), (' A 216  ASP  OD2', ' A 501  HOH  O  ', -0.589, (17.525, 2.496, -22.492)), (' A   4  ARG  H  ', ' A 299  GLN  NE2', -0.588, (7.133, 6.949, -17.555)), (' B 209  TYR  CE1', ' B 264  MET  HE2', -0.582, (-1.895, -22.476, -18.546)), (' B 244  GLN  NE2', ' B 248  ASP  OD1', -0.576, (-1.323, -27.03, -4.72)), (' B  67  LEU  HG ', ' B  74  GLN HE22', -0.556, (2.172, 26.184, 4.578)), (' B 109  GLY  HA2', ' B 200  ILE HD13', -0.551, (5.939, -10.421, -7.644)), (' B 270  GLU  O  ', ' B 274  ASN  ND2', -0.541, (13.186, -22.346, -25.979)), (' A 101  TYR  HA ', ' A 157  VAL  O  ', -0.538, (-13.803, 18.964, -19.411)), (' B 262  LEU  H  ', ' B 262  LEU HD12', -0.526, (2.154, -28.443, -13.406)), (' B 110  GLN  HG2', ' B 575  HOH  O  ', -0.525, (0.168, -10.169, -4.047)), (' B  19  GLN HE21', ' B 119  ASN HD22', -0.504, (5.375, 21.945, -3.652)), (' A 113  SER  O  ', ' A 149  GLY  HA2', -0.503, (-9.952, 7.581, -21.349)), (' A 286  LEU HD22', ' A 682  HOH  O  ', -0.495, (8.033, -5.631, -32.195)), (' A  95  ASN  HB3', ' A  98  THR  OG1', -0.491, (-22.481, 16.842, -12.76)), (' A   6  MET  HE1', ' B 589  HOH  O  ', -0.482, (4.124, 12.469, -14.499)), (' B 113  SER  O  ', ' B 149  GLY  HA2', -0.477, (0.278, 3.345, -4.96)), (' A 273  GLN  NE2', ' A 503  HOH  O  ', -0.476, (20.864, -0.973, -43.57)), (' B  62  SER  HB2', ' B  64  HIS  CE1', -0.474, (8.815, 25.573, 16.733)), (' B 165  MET  HE1', ' B 186  VAL  O  ', -0.472, (18.023, 5.259, 2.131)), (' A  48  ASP  O  ', ' A  52  PRO  HB3', -0.466, (-31.479, -2.185, -33.631)), (' A 285  ALA  HB3', ' B 285  ALA  HB3', -0.45, (10.541, -7.51, -26.641)), (' A   3  PHE  HA ', ' A 299  GLN  NE2', -0.448, (7.89, 7.284, -17.356)), (' B 222  ARG  HG3', ' B 222  ARG HH21', -0.44, (3.668, -34.373, -26.453)), (' B  43  ILE HD12', ' B  57  LEU  HB3', -0.433, (15.242, 16.53, 12.267)), (' B  93  THR HG22', ' B 606  HOH  O  ', -0.431, (-10.858, 22.906, 11.551)), (' B 401  O6K  C13', ' B 568  HOH  O  ', -0.429, (13.728, 16.424, -0.878)), (' B 260  ALA  O  ', ' B 263  ASP  HB3', -0.428, (0.363, -27.108, -17.946)), (' B  31  TRP  CE2', ' B  75  LEU HD21', -0.426, (-5.916, 18.289, 6.37)), (' A 126  TYR  CE1', ' B   6  MET  HE2', -0.423, (-8.384, -1.228, -18.772)), (' A  34  ASP  OD2', ' A  90  LYS  HE2', -0.421, (-30.992, 20.536, -17.479)), (' B  95  ASN  HB3', ' B  98  THR  OG1', -0.421, (-9.501, 12.736, 6.269)), (' B  57  LEU  HA ', ' B  57  LEU HD13', -0.417, (17.961, 18.54, 13.805)), (' B  22  CYS  HB3', ' B  42  VAL  O  ', -0.416, (11.729, 19.597, 6.13)), (' B 159  PHE  HB3', ' B 177  LEU HD13', -0.412, (-0.462, 3.659, 2.714)), (' B 227  LEU  HA ', ' B 227  LEU HD12', -0.409, (7.837, -27.251, -10.066)), (' B 255  ALA  C  ', ' B 257  THR  H  ', -0.409, (-8.992, -24.248, -17.47)), (' B  34  ASP  O  ', ' B  91  VAL HG22', -0.408, (-3.92, 16.499, 11.363))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
