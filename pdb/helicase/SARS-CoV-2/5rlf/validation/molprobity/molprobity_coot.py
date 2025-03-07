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
data['rama'] = [('A', '   7 ', 'LEU', 0.006104152215348613, (7.571999999999987, 42.834, -63.194)), ('A', ' 195 ', 'ILE', 0.02510710588416521, (-33.437, 29.247, -54.771)), ('A', ' 219 ', 'LEU', 0.020386528523645434, (-41.245, 29.151999999999994, -59.91399999999999)), ('A', ' 228 ', 'THR', 0.028611597945063374, (-23.358000000000004, 34.827, -60.29699999999998)), ('A', ' 340 ', 'VAL', 0.07228509203700852, (-26.122, 20.507999999999996, -61.95699999999999)), ('A', ' 484 ', 'VAL', 0.010161293680314347, (-31.722999999999995, 38.812, -81.181)), ('B', '  11 ', 'GLN', 0.014944030545358885, (8.619999999999997, 3.6079999999999988, -42.35))]
data['omega'] = []
data['rota'] = [('A', '   6 ', 'VAL', 0.2525690283813065, (4.962999999999989, 42.334, -60.36099999999999)), ('A', '   7 ', 'LEU', 0.12631534937868386, (7.571999999999987, 42.834, -63.194)), ('A', '  11 ', 'GLN', 0.0, (10.47399999999999, 44.581, -53.13799999999999)), ('A', '  12 ', 'THR', 0.0013599335943581536, (8.363999999999995, 47.766, -52.609)), ('A', '  20 ', 'ILE', 0.004975784334997501, (-8.089000000000002, 47.03699999999999, -60.89799999999999)), ('A', '  51 ', 'ASN', 0.12448919415119933, (-2.0410000000000093, 66.212, -47.49899999999999)), ('A', '  81 ', 'PHE', 0.0043712921743401184, (11.396999999999995, 66.678, -53.436)), ('A', ' 156 ', 'GLU', 0.02841805499294018, (-45.939, 34.44199999999999, -65.0)), ('A', ' 157 ', 'VAL', 0.036064534093091224, (-45.51299999999999, 30.598999999999993, -64.927)), ('A', ' 162 ', 'GLU', 0.1394330475709371, (-41.989000000000004, 27.447, -69.347)), ('A', ' 163 ', 'LEU', 0.2773218169078678, (-42.177, 31.084999999999994, -68.01399999999998)), ('A', ' 173 ', 'ARG', 0.0422352861408385, (-30.241999999999997, 42.053, -71.201)), ('A', ' 209 ', 'VAL', 0.03780638799071312, (-39.078, 31.061999999999998, -72.99)), ('A', ' 217 ', 'TYR', 0.22696491099398441, (-38.60900000000001, 24.816999999999997, -57.066999999999986)), ('A', ' 230 ', 'HIS', 0.14078874185545465, (-17.982, 35.266, -57.908)), ('A', ' 247 ', 'VAL', 0.0045911810174552505, (17.192, 10.576, -67.128)), ('A', ' 255 ', 'THR', 0.058866316054288055, (4.861999999999998, -2.689, -64.23)), ('A', ' 307 ', 'THR', 0.2294851668373576, (-9.032000000000007, 17.240999999999993, -63.23999999999999)), ('A', ' 337 ', 'ARG', 0.2475448357722287, (-23.121000000000002, 24.127000000000002, -54.281)), ('A', ' 340 ', 'VAL', 0.07555543467341773, (-26.122, 20.507999999999996, -61.95699999999999)), ('A', ' 344 ', 'ASP', 0.029455582599572625, (-22.859, 8.880000000000004, -59.08599999999999)), ('A', ' 376 ', 'ILE', 0.1780246078449684, (-6.691000000000001, 21.505000000000003, -72.06)), ('A', ' 502 ', 'ARG', 0.08487757389999175, (-35.897, 9.382000000000001, -97.595)), ('A', ' 530 ', 'THR', 0.02991853980347514, (-30.22399999999999, 18.753, -80.211)), ('A', ' 531 ', 'GLN', 0.042549925823251775, (-26.66800000000001, 19.921999999999997, -79.368)), ('A', ' 592 ', 'ILE', 0.01670230507707456, (-31.936999999999998, 19.653999999999996, -104.159)), ('B', '  11 ', 'GLN', 0.10742160163762997, (8.619999999999997, 3.6079999999999988, -42.35)), ('B', '  12 ', 'THR', 0.0013599335943581536, (6.272000000000002, 0.8499999999999979, -43.75999999999999)), ('B', '  20 ', 'ILE', 0.004201723015381483, (-11.160000000000002, 2.271000000000001, -38.895)), ('B', '  35 ', 'ILE', 0.29130124541545704, (-1.3869999999999978, -10.891000000000005, -32.178)), ('B', '  51 ', 'ASN', 0.14698340842150195, (-5.231000000000006, -14.938999999999997, -53.695999999999984)), ('B', '  68 ', 'MET', 0.2296556681178974, (4.834000000000004, -12.585, -55.296)), ('B', '  69 ', 'SER', 0.004019992775283754, (1.1579999999999986, -13.516000000000005, -54.359999999999985)), ('B', '  92 ', 'LEU', 0.1212904121853594, (8.775999999999994, -3.0399999999999974, -46.534)), ('B', '  95 ', 'ASN', 0.23701782951559913, (15.552999999999999, -3.6179999999999986, -41.593)), ('B', ' 103 ', 'VAL', 0.03885656769853085, (1.5189999999999992, -1.3399999999999999, -27.596)), ('B', ' 124 ', 'ASN', 0.08119452352405856, (-5.892000000000001, 12.449, -23.225)), ('B', ' 158 ', 'LEU', 0.17201507515158823, (-49.393, 19.096, -40.886)), ('B', ' 164 ', 'HIS', 0.01889045388696054, (-45.717000000000006, 14.005999999999998, -39.60499999999999)), ('B', ' 188 ', 'THR', 0.1026297106914132, (-35.09000000000001, 14.744, -58.24399999999999)), ('B', ' 191 ', 'SER', 0.13376624332635192, (-30.730999999999998, 11.915999999999997, -57.612999999999985)), ('B', ' 192 ', 'LYS', 0.22701168456746804, (-31.39800000000001, 14.279999999999992, -54.57299999999999)), ('B', ' 219 ', 'LEU', 0.04625106392817411, (-41.507, 21.192, -47.797)), ('B', ' 220 ', 'ASN', 0.0, (-43.903, 18.565, -49.158)), ('B', ' 228 ', 'THR', 0.025152844579776793, (-25.052999999999997, 15.382999999999997, -42.066999999999986)), ('B', ' 231 ', 'THR', 0.07050979716660244, (-15.325000000000003, 13.223999999999998, -43.82799999999999)), ('B', ' 247 ', 'VAL', 0.026254437398165464, (12.784999999999997, 36.445, -20.871)), ('B', ' 257 ', 'ASN', 0.0, (-0.778000000000004, 54.337, -24.705999999999992)), ('B', ' 307 ', 'THR', 0.2849397046595631, (-10.654000000000005, 31.232, -34.0)), ('B', ' 351 ', 'THR', 0.02447880688123405, (-7.147000000000006, 35.782, -45.742999999999995)), ('B', ' 376 ', 'ILE', 0.21773563842472005, (-11.516000000000004, 26.228, -25.259)), ('B', ' 484 ', 'VAL', 0.023956740543295645, (-37.813, 8.496, -25.704))]
data['cbeta'] = [('A', '  20 ', 'ILE', ' ', 0.2789945543102888, (-9.273999999999997, 46.61, -61.869)), ('A', ' 484 ', 'VAL', ' ', 0.2594628703602386, (-31.455000000000005, 38.807, -79.631)), ('A', ' 592 ', 'ILE', ' ', 0.30267840757495257, (-32.804, 19.159, -102.921))]
data['probe'] = [(' A 158  LEU HD21', ' A 164  HIS  CE1', -0.805, (-46.598, 32.435, -71.521)), (' A 331  SER  HB2', ' A 353  GLU  HG3', -0.748, (-12.023, 8.206, -53.258)), (' A 326  PRO  HG2', ' A 329  LYS  NZ ', -0.682, (-7.748, -0.548, -57.71)), (' A 386  VAL HG13', ' A 390  ARG  HE ', -0.668, (-7.858, 26.093, -57.164)), (' A 326  PRO  HB2', ' A 329  LYS  HZ3', -0.649, (-9.001, -0.171, -57.254)), (' A 238  PRO  HG3', ' A 990  HOH  O  ', -0.647, (6.331, 28.66, -62.198)), (' A 158  LEU HD11', ' A 164  HIS  CE1', -0.626, (-45.316, 31.971, -72.0)), (' A 519  ASN  HB3', ' A 530  THR  CG2', -0.608, (-30.601, 21.947, -80.307)), (' A   6  VAL  O  ', ' A   6  VAL HG23', -0.607, (3.424, 43.566, -62.328)), (' B 511  PHE  HB3', ' B 530  THR HG22', -0.606, (-38.478, 28.417, -20.312)), (' B 510  VAL HG21', ' B 541  TYR  CD1', -0.581, (-32.598, 34.933, -21.602)), (' A 519  ASN  HB3', ' A 530  THR HG23', -0.564, (-30.343, 21.978, -80.306)), (' A 326  PRO  HG2', ' A 329  LYS  HZ1', -0.561, (-7.01, -0.943, -57.055)), (' B 279  THR  HB ', ' B 429  MET  HE2', -0.549, (-6.15, 28.14, -20.648)), (' A 158  LEU HD21', ' A 164  HIS  HE1', -0.549, (-46.416, 32.253, -71.529)), (' B 333  ILE  HB ', ' B 358  CYS  HB2', -0.535, (-11.767, 32.782, -41.098)), (' A 510  VAL HG21', ' A 541  TYR  CD1', -0.534, (-25.644, 12.548, -80.745)), (' A 333  ILE  HB ', ' A 358  CYS  HB2', -0.531, (-13.375, 16.158, -56.952)), (' A 326  PRO  CG ', ' A 329  LYS  HZ3', -0.53, (-8.247, -0.741, -57.504)), (' A 244  GLU  HB2', ' A 276  LYS  HB2', -0.53, (10.198, 18.549, -64.152)), (' A 326  PRO  CB ', ' A 329  LYS  HZ3', -0.529, (-8.688, -0.486, -57.493)), (' A 279  THR  HB ', ' A 429  MET  HE2', -0.52, (0.014, 18.878, -74.913)), (' A 139  LYS  O  ', ' A 143  GLU  HG2', -0.519, (-14.11, 38.513, -63.466)), (' A 445  PRO  HB3', ' A 468  SER  HB3', -0.518, (-18.068, 5.85, -92.32)), (' B   8  CYS  SG ', ' B  99  GLY  O  ', -0.516, (8.769, 0.871, -32.035)), (' B 445  PRO  HB3', ' B 468  SER  HB3', -0.51, (-27.825, 40.243, -7.783)), (' B 451  THR HG21', ' B 585  LEU HD23', -0.501, (-25.553, 27.495, -6.075)), (' A 326  PRO  HG2', ' A 329  LYS  HZ3', -0.493, (-7.877, -0.149, -57.397)), (' B  15  ARG  HG3', ' B  24  PHE  CD2', -0.491, (-0.123, 1.966, -44.201)), (' A 158  LEU HD21', ' A 164  HIS  ND1', -0.491, (-45.885, 32.703, -70.521)), (' B 442  ARG HH11', ' B 464  HIS  CE1', -0.49, (-17.274, 47.047, -11.827)), (' A 293  ILE HG13', ' A 320  LYS  HB3', -0.489, (-10.676, 6.131, -67.985)), (' B 244  GLU  HB2', ' B 276  LYS  HB2', -0.488, (7.669, 29.18, -26.975)), (' A  19  CYS  HB2', ' A  23  PRO  HD2', -0.487, (-2.446, 47.815, -60.108)), (' A 332  ARG  CZ ', ' A 342  CYS  SG ', -0.487, (-18.995, 14.964, -60.841)), (' A 326  PRO  HB2', ' A 329  LYS  NZ ', -0.484, (-8.421, -0.423, -56.696)), (' B 293  ILE HG13', ' B 320  LYS  HB3', -0.484, (-14.228, 41.738, -29.522)), (' B  19  CYS  HB2', ' B  23  PRO  HD2', -0.48, (-5.788, 0.993, -38.657)), (' A 451  THR HG21', ' A 585  LEU HD23', -0.474, (-14.744, 18.056, -94.225)), (' A 176  LEU HD22', ' A 200  PHE  HB2', -0.469, (-32.139, 32.876, -70.242)), (' B 252  LEU  HB3', ' B 299  TYR  CD1', -0.463, (2.943, 42.509, -28.997)), (' B  12  THR  OG1', ' B  26  CYS  HA ', -0.462, (5.73, -0.098, -40.896)), (' A 367  THR HG22', ' A 392  ARG  HB3', -0.461, (1.763, 18.987, -53.282)), (' A 409  ARG  NH2', ' A 422  PHE  O  ', -0.458, (-7.01, 31.191, -73.561)), (' B 538  GLY  HA2', ' B 705  PO4  O1 ', -0.456, (-20.876, 32.917, -22.741)), (' A 263  SER  HA ', ' A 266  VAL HG13', -0.454, (1.961, -0.637, -73.679)), (' B 276  LYS  NZ ', ' B 811  HOH  O  ', -0.452, (7.441, 30.597, -32.891)), (' B 508  LYS  HD2', ' B 873  HOH  O  ', -0.451, (-36.383, 41.725, -18.097)), (' B 183  THR  OG1', ' B 228  THR  OG1', -0.45, (-27.263, 18.228, -42.757)), (' B 185  TYR  CE2', ' B 194  GLN  HG2', -0.448, (-28.394, 17.187, -49.428)), (' A 519  ASN  HB3', ' A 530  THR HG21', -0.446, (-31.282, 22.283, -80.059)), (' A 280  LEU HD11', ' A 438  LEU  HG ', -0.446, (-1.971, 11.257, -77.635)), (' A   6  VAL  HA ', ' A 129  ARG  HD2', -0.446, (5.557, 40.317, -60.678)), (' A 533  VAL HG11', ' A 560  ARG  HG3', -0.441, (-18.339, 23.691, -83.711)), (' A 512  ILE  O  ', ' A 546  PHE  HA ', -0.438, (-25.828, 20.49, -87.156)), (' B 533  VAL HG11', ' B 560  ARG  HG3', -0.437, (-26.105, 23.231, -17.684)), (' B 376  ILE HG22', ' B 400  GLY  HA3', -0.434, (-11.161, 27.653, -22.705)), (' A  12  THR  OG1', ' A  26  CYS  HA ', -0.432, (8.749, 48.383, -56.094)), (' B 409  ARG  NH2', ' B 422  PHE  O  ', -0.429, (-12.464, 16.534, -24.869)), (' A   6  VAL  CG2', ' A   6  VAL  O  ', -0.428, (3.708, 43.414, -61.62)), (' A  60  VAL HG13', ' A  84  CYS  SG ', -0.426, (4.414, 59.974, -60.158)), (' B 376  ILE HG12', ' B 425  VAL HG11', -0.424, (-7.503, 25.848, -24.568)), (' B 183  THR  HG1', ' B 228  THR  HG1', -0.424, (-26.765, 17.632, -43.254)), (' A 297  LEU HD11', ' A 324  TYR  HB3', -0.424, (-7.316, 0.005, -66.436)), (' A 516  ASN  ND2', ' A 814  HOH  O  ', -0.418, (-26.323, 30.351, -78.887)), (' B 154  VAL HG22', ' B 163  LEU HD13', -0.418, (-41.317, 17.032, -43.064)), (' B 297  LEU HD11', ' B 324  TYR  HB3', -0.416, (-10.011, 48.042, -29.112)), (' A 376  ILE HG22', ' A 400  GLY  HA3', -0.415, (-5.526, 19.865, -74.46)), (' B 512  ILE  O  ', ' B 546  PHE  HA ', -0.412, (-34.094, 26.087, -15.504)), (' A 237  ALA  O  ', ' A 385  SER  OG ', -0.411, (-0.863, 30.621, -60.833)), (' B 376  ILE  HA ', ' B 376  ILE HD12', -0.411, (-10.932, 25.918, -26.864)), (' A 376  ILE HG12', ' A 425  VAL HG11', -0.408, (-2.258, 21.689, -71.573)), (' A 163  LEU  HG ', ' A 211  TYR  HB3', -0.408, (-38.539, 29.798, -66.771)), (' A 158  LEU  HB2', ' A 162  GLU  HB2', -0.406, (-44.589, 27.742, -69.865)), (' B 280  LEU HD11', ' B 438  LEU  HG ', -0.401, (-8.912, 35.966, -17.933))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
