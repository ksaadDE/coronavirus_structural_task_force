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
data['rama'] = [('A', ' 195 ', 'ILE', 0.07103422802451201, (-33.63200000000002, 29.179000000000002, -54.018)), ('A', ' 484 ', 'VAL', 0.006481949928912399, (-31.838000000000008, 38.215, -80.656))]
data['omega'] = []
data['rota'] = [('A', '  12 ', 'THR', 0.0, (8.361999999999997, 47.099, -51.98200000000001)), ('A', '  35 ', 'ILE', 0.01639632074448079, (4.615, 57.595, -66.493)), ('A', '  51 ', 'ASN', 0.20331063687461243, (-1.8690000000000069, 65.54400000000001, -47.144000000000005)), ('A', '  81 ', 'PHE', 0.1295714872789861, (11.703, 65.887, -53.01400000000002)), ('A', ' 156 ', 'GLU', 0.018892621513307957, (-46.261000000000024, 34.207, -64.73)), ('A', ' 162 ', 'GLU', 0.05637157807625791, (-42.209999999999994, 26.837000000000007, -68.972)), ('A', ' 173 ', 'ARG', 0.04911973958630386, (-30.406, 41.374, -71.319)), ('A', ' 201 ', 'GLU', 0.17382930810713523, (-33.861000000000004, 28.267000000000007, -73.172)), ('A', ' 209 ', 'VAL', 0.007643575918381062, (-39.37500000000001, 30.398, -72.425)), ('A', ' 217 ', 'TYR', 0.19124744332825624, (-38.972000000000016, 24.32200000000001, -56.689)), ('A', ' 226 ', 'VAL', 0.14864846965982997, (-29.481000000000016, 37.374, -60.712)), ('A', ' 247 ', 'VAL', 0.2551760286399312, (17.042, 9.962000000000007, -66.05100000000002)), ('A', ' 255 ', 'THR', 0.013475099645914576, (4.221000000000001, -2.9879999999999924, -63.44600000000001)), ('A', ' 530 ', 'THR', 0.025482040884305165, (-30.208000000000006, 18.31800000000001, -79.73)), ('A', ' 531 ', 'GLN', 0.02017155610976457, (-26.706000000000003, 19.509, -78.79300000000002)), ('A', ' 592 ', 'ILE', 0.03808452928327978, (-32.321, 18.836, -103.35)), ('B', '   8 ', 'CYS', 0.051010502100819956, (7.4929999999999986, 3.859000000000001, -33.097)), ('B', '  15 ', 'ARG', 0.056856524770820066, (-1.3650000000000029, -0.41799999999999926, -42.052)), ('B', '  68 ', 'MET', 0.0007931552837307025, (4.946000000000001, -12.477999999999998, -55.153000000000006)), ('B', '  84 ', 'CYS', 0.05492158234119415, (3.8039999999999976, -13.538, -39.234)), ('B', '  95 ', 'ASN', 0.0037586123902399334, (15.587000000000003, -3.4479999999999933, -41.00100000000001)), ('B', '  97 ', 'CYS', 0.22499830511529964, (11.977999999999998, -1.2459999999999969, -37.209)), ('B', ' 103 ', 'VAL', 0.19031990943040236, (1.5920000000000005, -1.5980000000000008, -27.423)), ('B', ' 124 ', 'ASN', 0.13538777599781354, (-5.915000000000003, 12.298000000000002, -23.045)), ('B', ' 158 ', 'LEU', 0.1049831662859383, (-49.464, 18.684000000000005, -40.74)), ('B', ' 160 ', 'ASP', 0.14729562804524163, (-46.124000000000024, 25.054000000000006, -40.97600000000001)), ('B', ' 164 ', 'HIS', 0.05771099830315008, (-45.63900000000001, 13.824000000000007, -39.228)), ('B', ' 177 ', 'ASN', 0.0987243943292287, (-33.019000000000005, 18.061, -29.961000000000006)), ('B', ' 192 ', 'LYS', 0.1341846880575226, (-31.473000000000006, 13.919000000000008, -54.32500000000002)), ('B', ' 195 ', 'ILE', 0.13288430481942504, (-33.054000000000016, 21.398000000000003, -49.296)), ('B', ' 202 ', 'LYS', 0.03295797986210447, (-41.750000000000014, 16.298, -29.987000000000002)), ('B', ' 219 ', 'LEU', 0.07213447388447225, (-41.573, 21.001000000000005, -47.70600000000001)), ('B', ' 247 ', 'VAL', 0.29125277289295415, (13.071000000000002, 36.238, -20.797000000000008)), ('B', ' 256 ', 'LEU', 0.027934736715084417, (3.127000000000008, 52.84, -25.378000000000007)), ('B', ' 259 ', 'SER', 0.2235293481957716, (-6.9399999999999995, 52.715, -22.997000000000003)), ('B', ' 344 ', 'ASP', 0.006538799720207618, (-21.49300000000001, 39.788, -42.23200000000001)), ('B', ' 353 ', 'GLU', 0.2195524810119805, (-5.994000000000004, 40.69500000000001, -43.301)), ('B', ' 516 ', 'ASN', 0.009555158316622517, (-35.20500000000001, 19.708, -23.896000000000004))]
data['cbeta'] = [('A', ' 484 ', 'VAL', ' ', 0.2505848581493839, (-31.630000000000003, 38.06400000000001, -79.098)), ('A', ' 530 ', 'THR', ' ', 0.26099002606054583, (-31.272000000000013, 19.418000000000006, -79.755)), ('A', ' 592 ', 'ILE', ' ', 0.30758451567531453, (-33.22500000000002, 17.955, -102.393)), ('B', ' 483 ', 'ASP', ' ', 0.27798480384918345, (-40.39400000000002, 11.220000000000002, -23.641000000000002))]
data['probe'] = [(' A 326  PRO  HG2', ' A 329  LYS  NZ ', -0.855, (-7.617, -0.619, -56.695)), (' A 326  PRO  HG2', ' A 329  LYS  HZ3', -0.768, (-7.514, -1.786, -56.368)), (' B  13  SER  HB2', ' B  92  LEU  HB2', -0.724, (6.427, -1.709, -47.408)), (' A 158  LEU HD21', ' A 164  HIS  CE1', -0.712, (-46.931, 31.988, -71.003)), (' B  12  THR HG22', ' B  14  LEU  H  ', -0.71, (4.087, -0.474, -42.947)), (' B 279  THR  HB ', ' B 429  MET  HE3', -0.663, (-5.44, 27.731, -20.988)), (' B 474 BMET  HG2', ' B 590  LEU  HB2', -0.655, (-38.088, 28.229, -3.193)), (' A 158  LEU HD21', ' A 164  HIS  ND1', -0.655, (-46.428, 32.505, -70.242)), (' B 162  GLU  HG2', ' B 210  VAL HG22', -0.651, (-44.721, 21.379, -34.735)), (' B  12  THR HG21', ' B  25  LEU  O  ', -0.643, (3.791, -0.633, -40.615)), (' A 519  ASN  HB3', ' A 530  THR  CG2', -0.613, (-30.672, 21.437, -79.837)), (' A 279  THR  HB ', ' A 429  MET  HE3', -0.61, (-0.313, 18.96, -74.136)), (' A 326  PRO  HG2', ' A 329  LYS  HZ1', -0.601, (-7.085, -0.962, -57.448)), (' A  19  CYS  HB2', ' A  23  PRO  HD2', -0.586, (-2.629, 46.994, -59.796)), (' A 176  LEU HD22', ' A 200  PHE  HB2', -0.586, (-32.719, 31.699, -69.979)), (' A 158  LEU HD12', ' A 162  GLU  HB3', -0.572, (-43.764, 28.045, -70.582)), (' A 519  ASN  HB3', ' A 530  THR HG23', -0.565, (-30.414, 21.468, -79.836)), (' A 445  PRO  HD2', ' A 448  ILE HD12', -0.535, (-17.258, 9.47, -89.148)), (' B   8  CYS  SG ', ' B  99  GLY  N  ', -0.532, (9.91, -0.015, -32.621)), (' A  63  LEU  HB2', ' A  83  LEU HD12', -0.525, (3.75, 62.188, -55.023)), (' A 140  ALA  O  ', ' A 144  THR HG23', -0.512, (-14.702, 42.398, -62.109)), (' B 511  PHE  HB3', ' B 530  THR HG22', -0.512, (-38.14, 27.999, -20.708)), (' A 331  SER  HB2', ' A 353  GLU  HG3', -0.51, (-13.01, 7.828, -52.835)), (' B  12  THR HG22', ' B  14  LEU  N  ', -0.509, (3.901, -0.749, -43.387)), (' B 445  PRO  HD2', ' B 448  ILE HD12', -0.509, (-26.411, 35.72, -10.278)), (' B  19  CYS  HB2', ' B  23  PRO  HD2', -0.507, (-6.0, 0.547, -38.199)), (' B 510  VAL HG21', ' B 541  TYR  CD1', -0.505, (-32.522, 35.002, -21.535)), (' B  16  CYS  O  ', ' B  22  ARG  HA ', -0.488, (-5.702, 0.535, -40.968)), (' B  49  VAL HG23', ' B  58  THR HG22', -0.487, (-9.102, -11.918, -46.916)), (' A  49  VAL HG23', ' A  58  THR HG22', -0.483, (-5.137, 61.79, -53.8)), (' A 163  LEU HD11', ' A 200  PHE  HE2', -0.474, (-37.67, 31.046, -66.682)), (' A 198  TYR  HE2', ' A 211  TYR  CD1', -0.473, (-37.608, 27.06, -63.067)), (' A 297  LEU HD11', ' A 324  TYR  HB3', -0.472, (-8.094, -0.421, -66.13)), (' B 252  LEU  HB3', ' B 299  TYR  CD1', -0.463, (3.152, 42.237, -28.777)), (' A   7  LEU HD13', ' A 103  VAL HG22', -0.462, (7.192, 46.348, -64.956)), (' A 519  ASN  HB3', ' A 530  THR HG21', -0.459, (-31.267, 21.887, -79.378)), (' B 451  THR HG21', ' B 585  LEU HD23', -0.458, (-25.5, 27.599, -5.965)), (' A 512  ILE  O  ', ' A 546  PHE  HA ', -0.458, (-25.613, 19.767, -86.988)), (' A 510  VAL HG21', ' A 541  TYR  CD1', -0.457, (-25.935, 12.033, -80.016)), (' A 498  GLU  HG3', ' A 502  ARG  NH2', -0.454, (-37.64, 15.251, -99.275)), (' B 154  VAL HG13', ' B 163  LEU HD22', -0.452, (-43.914, 16.84, -43.435)), (' A 367  THR HG22', ' A 392  ARG  HB3', -0.45, (1.37, 18.149, -52.663)), (' B 512  ILE  O  ', ' B 546  PHE  HA ', -0.445, (-34.198, 26.407, -15.084)), (' B 154  VAL HG22', ' B 163  LEU HD13', -0.44, (-41.305, 16.489, -43.124)), (' B 249  ILE HG23', ' B 273  GLY  HA3', -0.436, (5.395, 39.315, -25.96)), (' A 163  LEU HD11', ' A 200  PHE  CE2', -0.436, (-37.586, 31.295, -66.671)), (' A 376  ILE  HA ', ' A 376  ILE HD12', -0.434, (-6.981, 21.527, -69.785)), (' B 303  ARG  NH1', ' B 353  GLU  O  ', -0.433, (-4.082, 38.353, -41.724)), (' B 279  THR  HB ', ' B 429  MET  CE ', -0.432, (-5.992, 27.733, -20.073)), (' A 279  THR  HB ', ' A 429  MET  CE ', -0.428, (-0.171, 18.845, -74.348)), (' A 451  THR HG21', ' A 585  LEU HD23', -0.428, (-14.809, 17.715, -93.572)), (' B   7  LEU HD13', ' B 103  VAL HG22', -0.428, (2.543, -0.848, -30.328)), (' B 297  LEU HD11', ' B 324  TYR  HB3', -0.427, (-10.203, 47.756, -29.296)), (' A  19  CYS  CB ', ' A  23  PRO  HD2', -0.424, (-3.084, 47.032, -60.136)), (' A 198  TYR  HE2', ' A 211  TYR  HD1', -0.424, (-37.264, 27.017, -63.213)), (' B  15  ARG  HD2', ' B  22  ARG  O  ', -0.423, (-3.091, 2.925, -42.614)), (' B 185  TYR  CE2', ' B 194  GLN  HG2', -0.42, (-28.574, 16.858, -49.802)), (' B  19  CYS  CB ', ' B  23  PRO  HD2', -0.419, (-5.75, 1.115, -37.879)), (' A 295  LEU HD21', ' A 370  ILE HG21', -0.416, (-0.244, 10.248, -64.317)), (' B 443  ARG  NH2', ' B 706  PO4  O3 ', -0.415, (-20.91, 35.113, -19.28)), (' B  12  THR HG22', ' B  13  SER  N  ', -0.415, (5.002, -0.359, -43.497)), (' A 249  ILE HG23', ' A 273  GLY  HA3', -0.414, (7.725, 7.637, -64.254)), (' B 196  GLY  HA3', ' B 215  THR HG21', -0.409, (-32.617, 24.608, -46.169)), (' B 295  LEU HD21', ' B 370  ILE HG21', -0.408, (-2.564, 36.969, -28.702)), (' B  52  ALA  CB ', ' B  75  HIS  CG ', -0.407, (-5.977, -20.445, -52.679)), (' B 455  LEU HD13', ' B 584  LYS  HD3', -0.406, (-21.317, 23.055, -5.135)), (' A 280  LEU HD11', ' A 438  LEU  HG ', -0.405, (-2.341, 10.578, -76.752)), (' B 504  PRO  HB3', ' B 507  ARG HH21', -0.405, (-47.256, 38.423, -12.663)), (' A 252  LEU  HB3', ' A 299  TYR  CD2', -0.403, (4.977, 5.205, -61.654)), (' B   2  VAL HG22', ' B  13  SER  HA ', -0.403, (4.99, 0.764, -46.688)), (' B 453  SER  HA ', ' B 457  TYR  HB2', -0.403, (-15.176, 30.235, -7.812)), (' B   8  CYS  SG ', ' B  99  GLY  O  ', -0.403, (9.083, 0.85, -31.578)), (' B 280  LEU  HB2', ' B 436  MET  HE3', -0.401, (-4.715, 33.833, -20.599)), (' B 533  VAL HG11', ' B 560  ARG  O  ', -0.401, (-25.346, 23.963, -16.288))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
