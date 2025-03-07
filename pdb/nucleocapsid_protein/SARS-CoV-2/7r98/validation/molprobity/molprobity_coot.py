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
data['omega'] = [('D', ' 116 ', 'PRO', None, (28.809420000000003, -52.15634, -7.1359699999999995)), ('E', ' 116 ', 'PRO', None, (1.55631, -48.50022, -6.59021)), ('F', ' 116 ', 'PRO', None, (12.04452, -74.3122, -7.33539))]
data['rota'] = [('D', '   7 ', 'SER', 0.140894398237099, (36.3581, -36.38701, -8.59494)), ('D', '  26 ', 'SER', 0.2821264390774225, (36.91539000000003, -48.46644, 2.60547)), ('D', '  72 ', 'SER', 0.10722549729351684, (42.095060000000025, -46.30394, -17.89236)), ('D', ' 103 ', 'LEU', 0.10507119777808033, (37.06659, -61.06849, -15.03733)), ('E', '   7 ', 'SER', 0.0, (-15.94702000000001, -49.85851000000001, -8.40956)), ('E', '  57 ', 'SER', 0.08639042520976029, (-3.7404400000000004, -34.13043999999999, -21.40629)), ('E', '  65 ', 'VAL', 0.17105139292725316, (-10.009490000000007, -51.04611000000003, -26.38259)), ('E', '  72 ', 'SER', 0.004278688040810347, (-10.24316, -39.61556999999999, -17.15308)), ('E', '  80 ', 'VAL', 0.2649266775940225, (-9.596309999999994, -42.28722, -12.07586)), ('E', ' 103 ', 'LEU', 0.12543119211832435, (5.01928, -36.59866, -13.88286)), ('F', '  57 ', 'SER', 0.14548212747771752, (1.51863, -85.47862, -22.15871)), ('F', '  72 ', 'SER', 0.0018373414189587563, (10.04113, -88.67725, -18.06771)), ('F', '  80 ', 'VAL', 0.18924294071692496, (11.99143000000001, -86.94884, -12.84976)), ('F', ' 103 ', 'LEU', 0.20249464950284624, (-0.30525, -76.96005, -14.714599999999999))]
data['cbeta'] = [('E', '  32 ', 'THR', ' ', 0.3128953571347551, (1.8626500000000001, -34.13135, -9.72252)), ('E', '  65 ', 'VAL', ' ', 0.27349115020264964, (-9.296080000000007, -50.93257000000003, -25.03041)), ('F', '  32 ', 'THR', ' ', 0.2516246619000945, (-0.7036100000000006, -81.10937, -10.4006))]
data['probe'] = [(' C 154  ASN HD22', ' E   1  GLU  HB2', -0.916, (-2.417, -52.416, 4.034)), (' F  65  VAL HG13', ' F  69  PHE  HB2', -0.81, (17.822, -85.21, -25.027)), (' D  65  VAL HG13', ' D  69  PHE  CG ', -0.662, (34.348, -40.203, -24.641)), (' E  55  SER  HG ', ' E  57  SER  HG ', -0.659, (-1.37, -33.066, -19.05)), (' D  31  SER  O  ', ' D  32  THR HG22', -0.656, (40.819, -58.313, -9.044)), (' F  23  VAL HG22', ' F  79  THR HG22', -0.654, (14.241, -89.274, -7.741)), (' A 154  ASN  HB3', ' F   1  GLU  HB2', -0.654, (18.632, -76.321, 3.722)), (' D  23  VAL HG22', ' D  79  THR HG22', -0.652, (40.991, -42.931, -7.544)), (' F  31  SER  O  ', ' F  32  THR HG22', -0.645, (1.028, -81.716, -8.865)), (' C 118  GLU  HB3', ' C 121  LEU HD12', -0.595, (-0.471, -76.171, 6.633)), (' D  65  VAL HG13', ' D  69  PHE  HB2', -0.59, (34.286, -40.831, -24.462)), (' E  23  VAL HG22', ' E  79  THR HG22', -0.586, (-12.184, -42.569, -6.573)), (' E  31  SER  O  ', ' E  32  THR HG22', -0.582, (0.622, -35.265, -8.21)), (' D  65  VAL  CG1', ' D  69  PHE  HB2', -0.573, (34.438, -41.475, -24.724)), (' E  35  MET  SD ', ' E  99  SER  HA ', -0.564, (-2.087, -44.106, -10.563)), (' F  31  SER  O  ', ' F  32  THR  CG2', -0.564, (0.596, -81.127, -9.213)), (' E  31  SER  O  ', ' E  32  THR  CG2', -0.555, (0.877, -35.495, -8.378)), (' C 112  TYR  CD2', ' C 146  ILE HG21', -0.543, (0.515, -63.291, -0.388)), (' B 112  TYR  CD2', ' B 146  ILE HG21', -0.536, (16.872, -43.735, -0.118)), (' D 114  PHE  O  ', ' D 115  ALA  HB2', -0.532, (25.52, -53.395, -10.601)), (' F 114  PHE  O  ', ' F 115  ALA  HB2', -0.527, (12.396, -70.884, -10.488)), (' F  65  VAL HG13', ' F  69  PHE  CB ', -0.51, (18.271, -85.262, -24.524)), (' C 146  ILE HG23', ' E  -1  MET  HG3', -0.507, (0.662, -60.439, 0.204)), (' C  64  LEU  O  ', ' C 131  ILE HG21', -0.506, (-10.866, -78.091, 0.83)), (' E  84  MET  HE1', ' E 123  VAL HG21', -0.494, (-16.112, -53.333, -16.746)), (' F  49  VAL HG13', ' F  65  VAL HG21', -0.487, (19.469, -81.661, -23.298)), (' A 173  ALA  O  ', ' A 174  GLU  C  ', -0.484, (35.426, -85.992, -6.425)), (' B  87  TYR  CE1', ' B 110  PHE  HB2', -0.478, (16.428, -33.171, 0.916)), (' F  34  ALA  O  ', ' F 100  GLY  N  ', -0.478, (8.179, -77.364, -12.85)), (' E  20  LEU  HG ', ' E  84  MET  HE2', -0.478, (-15.814, -50.246, -16.747)), (' D  63  ASP  N  ', ' D  64  PRO  HD2', -0.477, (28.026, -43.51, -28.369)), (' C 154  ASN  ND2', ' E   1  GLU  H  ', -0.473, (-1.247, -52.905, 3.73)), (' D  89  PRO  O  ', ' D  92  SER  HB2', -0.473, (27.233, -29.706, -21.346)), (' D  65  VAL HG13', ' D  69  PHE  CB ', -0.473, (34.888, -40.346, -24.327)), (' E  89  PRO  O  ', ' E  92  SER  HB2', -0.472, (-16.74, -60.551, -21.806)), (' E  92  SER  OG ', ' E 124  THR  HA ', -0.467, (-18.067, -60.395, -18.084)), (' E  65  VAL HG13', ' E  69  PHE  HB2', -0.465, (-10.477, -48.609, -24.183)), (' D  18  LEU  HB3', ' D  84  MET  HE3', -0.461, (36.644, -33.57, -18.508)), (' B  55  ALA  HB2', ' B 109  TYR  CE2', -0.46, (20.87, -32.108, 7.554)), (' F  35  MET  SD ', ' F  99  SER  HA ', -0.455, (9.842, -79.573, -11.258)), (' A  87  TYR  CE1', ' A 110  PHE  HB2', -0.455, (34.149, -72.786, 0.095)), (' A 123  TYR  CD1', ' A 132  TRP  CE3', -0.449, (36.646, -62.32, -1.71)), (' E  55  SER  OG ', ' E  57  SER  OG ', -0.449, (-1.734, -33.084, -18.947)), (' B  92  ARG  CB ', ' B 104  LEU HD12', -0.446, (20.523, -23.589, 16.152)), (' A 146  ILE HG23', ' F  -1  MET  HG3', -0.446, (22.615, -68.692, -0.315)), (' E  89  PRO  HA ', ' E 125  VAL  HB ', -0.446, (-18.932, -59.228, -22.65)), (' A  58  GLN  NE2', ' A  62  GLU  O  ', -0.445, (47.094, -77.258, 2.877)), (' D  31  SER  O  ', ' D  32  THR  CG2', -0.444, (40.304, -58.496, -9.306)), (' E  23  VAL HG22', ' E  79  THR  CG2', -0.443, (-12.63, -42.291, -6.56)), (' E  63  ASP  N  ', ' E  64  PRO  HD2', -0.443, (-5.475, -52.854, -27.612)), (' C  79  SER  HB3', ' C  80  PRO  HD2', -0.442, (3.794, -62.378, -11.176)), (' F  31  SER  C  ', ' F  32  THR HG22', -0.441, (0.52, -81.757, -8.851)), (' C  77  ASN  OD1', ' E 117  TRP  HB2', -0.439, (-0.773, -53.842, -6.319)), (' F  84  MET  HE1', ' F 123  VAL HG21', -0.436, (24.357, -87.429, -17.781)), (' F  55  SER  OG ', ' F  57  SER  OG ', -0.436, (-0.533, -83.621, -20.01)), (' F  65  VAL HG13', ' F  69  PHE  CD2', -0.434, (19.189, -84.621, -24.263)), (' C 123  TYR  CD1', ' C 132  TRP  CE3', -0.432, (-0.358, -76.078, -1.738)), (' C 167  LEU HD22', ' C 171  PHE  HB3', -0.431, (-17.398, -71.372, -2.602)), (' D   6  ALA  HA ', ' D  21  SER  O  ', -0.429, (36.184, -40.151, -9.569)), (' F  23  VAL HG22', ' F  79  THR  CG2', -0.425, (13.697, -89.733, -7.537)), (' E  69  PHE  CD1', ' E  69  PHE  N  ', -0.424, (-13.15, -48.51, -24.35)), (' A 155  ALA  O  ', ' F   1  GLU  HG3', -0.424, (20.502, -78.35, 3.296)), (' A 155  ALA  HB3', ' F   1  GLU  OE2', -0.423, (19.815, -80.596, 4.778)), (' B 118  GLU  HB3', ' B 121  LEU HD12', -0.419, (6.017, -36.777, 7.488)), (' D  31  SER  C  ', ' D  32  THR HG22', -0.416, (40.944, -57.865, -9.357)), (' E  41  ALA  HB3', ' E  44  LYS  HB2', -0.415, (-8.217, -63.097, -19.778)), (' F  65  VAL HG22', ' F  69  PHE  CD2', -0.415, (20.504, -83.751, -24.134)), (' E  23  VAL  HA ', ' E  79  THR HG22', -0.412, (-11.24, -42.477, -6.158)), (' E  69  PHE  HD1', ' E  69  PHE  N  ', -0.412, (-13.481, -48.569, -24.578)), (' E  18  LEU  HB3', ' E  84  MET  HE3', -0.41, (-17.817, -51.106, -18.196)), (' D  65  VAL HG13', ' D  69  PHE  CD2', -0.406, (33.825, -39.926, -23.698)), (' F  20  LEU  HG ', ' F  84  MET  HE2', -0.405, (21.921, -88.542, -17.307)), (' D  24  ALA  HB1', ' D  28  ARG  HB3', -0.404, (36.89, -49.854, -3.238)), (' C  55  ALA  HB2', ' C 109  TYR  CE2', -0.403, (-11.591, -66.041, 7.419)), (' D 105  GLY  O  ', ' D 107  THR  N  ', -0.403, (32.406, -57.266, -23.031)), (' C  87  TYR  CE2', ' C 110  PHE  HB2', -0.401, (-8.579, -69.006, 0.677)), (' D  89  PRO  HA ', ' D 125  VAL  HB ', -0.4, (29.683, -28.685, -23.237))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
