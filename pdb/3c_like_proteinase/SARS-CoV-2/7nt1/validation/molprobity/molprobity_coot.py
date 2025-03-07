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
data['rota'] = [('A', '   5 ', 'LYS', 0.15069678736224795, (1.3929999999999993, 2.514, -17.267)), ('A', '  49 ', 'MET', 0.0811663582941101, (-21.37099999999999, -14.019000000000002, 4.924)), ('A', '  50 ', 'LEU', 0.11580845266272527, (-25.0, -12.618000000000007, 5.058)), ('A', '  57 ', 'LEU', 0.17253590438602465, (-17.071, -16.84, 14.288)), ('A', '  65 ', 'ASN', 0.09937834098952882, (-8.428, -24.968, 11.173)), ('A', '  86 ', 'VAL', 0.05003267399743712, (-7.52, -8.375, 8.643)), ('A', ' 102 ', 'LYS', 0.1025778554852461, (6.154, -0.368, 6.236)), ('A', ' 196 ', 'THR', 0.03777925745729212, (-20.327, 8.926, -8.001)), ('A', ' 222 ', 'ARG', 6.562299940888733e-05, (-1.2789999999999988, 31.384000000000007, -25.198)), ('A', ' 224 ', 'THR', 0.010278360264974728, (-3.8920000000000017, 31.558000000000007, -18.893)), ('A', ' 238 ', 'ASN', 0.20045924198593604, (-17.139, 15.863000000000001, -12.358)), ('A', ' 281 ', 'ILE', 0.10464539399179067, (-2.4970000000000017, 12.779999999999998, -26.346)), ('A', ' 284 ', 'SER', 0.051985314967724836, (-5.176, 8.132000000000001, -25.68)), ('A', ' 303 ', 'VAL', 0.2814673188579807, (15.108, 6.113, -10.879)), ('B', '  51 ', 'ASN', 0.14853453024392368, (30.148, 2.7590000000000003, -38.879)), ('B', '  61 ', 'LYS', 0.2493096481210863, (39.436, -6.265, -25.769999999999996)), ('B', '  81 ', 'SER', 0.12889867234894356, (32.261, -14.374999999999998, -27.531999999999996)), ('B', ' 121 ', 'SER', 0.025725923505212613, (18.837, -1.9769999999999999, -11.232)), ('B', ' 169 ', 'THR', 0.08668276563861009, (10.19, 8.381, -34.394)), ('B', ' 189 ', 'GLN', 0.2538517962744417, (23.587, 5.3610000000000015, -35.649)), ('B', ' 190 ', 'THR', 0.06444431666914043, (22.918, 5.648, -39.457)), ('B', ' 196 ', 'THR', 0.08320872970978793, (4.571, 2.207, -41.74499999999999)), ('B', ' 214 ', 'ASN', 0.2709482553698963, (-17.244, -8.734000000000004, -19.467)), ('B', ' 224 ', 'THR', 0.019255875962052506, (-21.69599999999999, -11.255, -41.435)), ('B', ' 240 ', 'GLU', 0.14575616813779751, (-3.2100000000000017, -5.724, -40.621)), ('B', ' 270 ', 'GLU', 0.13330136507739454, (-19.049, -0.977, -38.35399999999999)), ('B', ' 286 ', 'LEU', 0.26679017033826, (-10.442, 3.5960000000000005, -29.179)), ('B', ' 303 ', 'VAL', 0.2895470868778128, (-18.313, -16.929, -16.838))]
data['cbeta'] = [('A', ' 187 ', 'ASP', ' ', 0.30403322163661656, (-15.312, -7.567000000000001, 4.922))]
data['probe'] = [(' B  46  SER  O  ', ' B  49  MET  HG2', -0.785, (29.93, 7.91, -32.339)), (' A 219  PHE  CD2', ' A 281  ILE HD13', -0.745, (-2.439, 17.383, -25.76)), (' A 290  GLU  OE1', ' B   4  ARG  NH2', -0.66, (-5.626, 2.37, -13.511)), (' A  53  ASN  O  ', ' A  57  LEU HD12', -0.623, (-18.64, -13.692, 13.013)), (' A 219  PHE  CE2', ' A 281  ILE HD13', -0.613, (-1.607, 17.197, -25.079)), (' A  86  VAL HG13', ' A 179  GLY  CA ', -0.606, (-7.031, -4.855, 7.717)), (' B  46  SER  HA ', ' B  49  MET  HE2', -0.587, (29.459, 7.424, -29.435)), (' A  53  ASN  C  ', ' A  57  LEU HD12', -0.576, (-18.636, -13.428, 12.78)), (' A 219  PHE  CD2', ' A 281  ILE  CD1', -0.555, (-2.91, 17.057, -25.573)), (' B  86  VAL HG13', ' B 179  GLY  HA2', -0.549, (21.758, -10.554, -30.172)), (' A 167  LEU  HB3', ' A 168  PRO  CD ', -0.536, (-20.237, -2.902, -6.605)), (' A 167  LEU  HB3', ' A 168  PRO  HD2', -0.525, (-19.858, -2.39, -6.659)), (' A 224  THR  OG1', ' A 225  THR  N  ', -0.523, (-4.202, 31.879, -16.864)), (' B  51  ASN  HB2', ' B 613  HOH  O  ', -0.521, (30.456, 4.769, -41.162)), (' B 256  GLN  HG2', ' B 256  GLN  O  ', -0.521, (-17.703, -18.235, -23.842)), (' A 263  ASP  HB3', ' A 603  HOH  O  ', -0.52, (-0.531, 28.049, -21.105)), (' A 285  ALA  HB3', ' B 285  ALA  HB3', -0.516, (-10.777, 7.231, -26.627)), (' A  86  VAL HG13', ' A 179  GLY  HA3', -0.502, (-7.455, -5.005, 8.449)), (' A  87  LEU HD21', ' A  89  LEU HD21', -0.492, (-5.929, -16.843, 11.079)), (' A 276  MET  HE3', ' A 281  ILE HG13', -0.483, (-5.543, 14.489, -26.507)), (' B 230  PHE  HA ', ' B 269  LYS  HE2', -0.482, (-15.412, -6.897, -44.129)), (' A   6  MET  O  ', ' A 502  DMS  H12', -0.479, (4.631, 2.212, -12.628)), (' A 118  TYR  CE2', ' A 144  SER  HB3', -0.474, (-7.832, -13.281, -8.902)), (' A 304  THR HG22', ' B 123  SER  HB3', -0.46, (15.446, 1.592, -12.957)), (' A  87  LEU  CD2', ' A  89  LEU  HG ', -0.458, (-4.77, -15.493, 10.292)), (' B  86  VAL HG13', ' B 179  GLY  CA ', -0.452, (21.763, -10.889, -30.059)), (' A  87  LEU HD21', ' A  89  LEU  CD2', -0.445, (-5.811, -16.161, 11.052)), (' B 229  ASP  HB2', ' B 605  HOH  O  ', -0.443, (-17.512, -9.899, -47.854)), (' A   1  SER  HB3', ' B 166  GLU  OE1', -0.44, (12.396, 7.375, -26.63)), (' A 104  VAL  O  ', ' A 160  CYS  HA ', -0.437, (-0.865, 1.137, 2.515)), (' A  87  LEU HD22', ' A  89  LEU  HG ', -0.435, (-4.853, -15.561, 9.936)), (' A 256  GLN  HG2', ' A 256  GLN  O  ', -0.433, (11.107, 20.203, -18.731)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.425, (-6.059, 9.774, -8.41)), (' A 220  LEU  HA ', ' A 267  SER  OG ', -0.424, (-2.241, 23.93, -23.79)), (' B 104  VAL  O  ', ' B 160  CYS  HA ', -0.423, (12.388, -14.275, -27.457)), (' A  87  LEU  CD2', ' A  89  LEU  CD2', -0.422, (-5.375, -16.362, 11.011)), (' A 304  THR  HB ', ' B 121  SER  HB3', -0.419, (17.432, 0.503, -10.557)), (' A  70  ALA  O  ', ' A  73  VAL HG12', -0.417, (6.616, -23.587, 0.719)), (' A 186  VAL HG23', ' A 188  ARG  HB2', -0.414, (-20.415, -6.163, 5.194)), (' B 224  THR HG23', ' B 225  THR  N  ', -0.408, (-20.705, -12.451, -43.363))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
