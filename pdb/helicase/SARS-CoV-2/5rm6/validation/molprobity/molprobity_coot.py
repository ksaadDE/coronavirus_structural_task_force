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
data['rama'] = [('A', ' 195 ', 'ILE', 0.059945601456023546, (-33.91400000000001, 28.963, -54.603)), ('A', ' 219 ', 'LEU', 0.04675033916557204, (-41.71300000000001, 28.763, -59.56199999999999)), ('A', ' 484 ', 'VAL', 0.017278133952835135, (-31.72800000000001, 38.243999999999986, -80.832)), ('B', ' 187 ', 'VAL', 0.07319645879427483, (-36.565999999999995, 13.364999999999995, -54.457999999999984))]
data['omega'] = []
data['rota'] = [('A', '  12 ', 'THR', 0.0013599335943581536, (7.895000000000004, 47.37400000000001, -51.986)), ('A', '  20 ', 'ILE', 0.014123842015764419, (-8.332000000000004, 46.49799999999999, -60.431999999999995)), ('A', '  35 ', 'ILE', 0.05929634472970894, (4.370000000000004, 57.759, -66.49)), ('A', '  51 ', 'ASN', 0.05108349854216956, (-2.213999999999994, 65.76499999999997, -47.12799999999999)), ('A', '  81 ', 'PHE', 0.05079995164808374, (11.288, 66.202, -53.245)), ('A', ' 173 ', 'ARG', 0.0859975961752795, (-30.310000000000016, 41.3, -71.282)), ('A', ' 207 ', 'ASP', 0.11016854206271108, (-43.15899999999999, 34.824, -76.04199999999999)), ('A', ' 209 ', 'VAL', 0.01739106283073522, (-39.290000000000006, 30.661999999999992, -72.627)), ('A', ' 217 ', 'TYR', 0.027793999003460784, (-39.047000000000004, 24.481999999999992, -56.928)), ('A', ' 255 ', 'THR', 0.011314446630912358, (4.3530000000000015, -3.0390000000000015, -63.549)), ('A', ' 301 ', 'SER', 0.2520802867231753, (0.487000000000001, 2.1179999999999914, -56.28299999999999)), ('A', ' 345 ', 'LYS', 0.2582932089031962, (-21.233000000000004, 5.209000000000001, -58.809)), ('A', ' 376 ', 'ILE', 0.24009166156191314, (-6.886999999999999, 21.010999999999992, -71.582)), ('A', ' 432 ', 'ILE', 0.26135017786789017, (7.219000000000004, 23.147999999999993, -79.377)), ('A', ' 502 ', 'ARG', 0.026826361207130524, (-35.72500000000001, 8.85499999999999, -97.17099999999998)), ('A', ' 530 ', 'THR', 0.0258387386566028, (-30.155, 18.30099999999999, -79.912)), ('A', ' 531 ', 'GLN', 0.02594955911600621, (-26.590000000000003, 19.41, -79.054)), ('A', ' 592 ', 'ILE', 0.017443960977782075, (-32.01, 19.094, -103.672)), ('B', '   8 ', 'CYS', 0.15510234807947465, (7.602999999999999, 3.8979999999999997, -33.62)), ('B', '  12 ', 'THR', 0.0025962347726545556, (6.475999999999999, 0.694999999999995, -43.30299999999999)), ('B', '  35 ', 'ILE', 0.21265004475427515, (-1.2710000000000008, -11.131000000000009, -32.012)), ('B', '  68 ', 'MET', 0.03416171010197031, (4.752000000000006, -12.545000000000002, -55.167)), ('B', '  69 ', 'SER', 0.084466342110509, (1.1079999999999997, -13.558000000000003, -54.272999999999996)), ('B', '  79 ', 'ILE', 0.1503033201541875, (8.006000000000004, -22.417000000000012, -51.68)), ('B', '  92 ', 'LEU', 0.2835637283132195, (8.866, -3.330000000000007, -46.195999999999984)), ('B', '  96 ', 'THR', 0.06989246099141971, (14.481000000000002, -0.3000000000000007, -39.851)), ('B', ' 103 ', 'VAL', 0.034687092580971274, (1.73, -1.577, -27.206)), ('B', ' 124 ', 'ASN', 0.1027881936976223, (-5.73, 12.339, -23.166)), ('B', ' 158 ', 'LEU', 0.13554874515262458, (-49.43800000000002, 18.724, -40.428)), ('B', ' 160 ', 'ASP', 0.10387532773608076, (-46.13999999999999, 25.018, -40.618)), ('B', ' 177 ', 'ASN', 0.1178904490257155, (-32.90400000000001, 17.756, -29.802999999999994)), ('B', ' 187 ', 'VAL', 0.21749037848573177, (-36.565999999999995, 13.364999999999995, -54.457999999999984)), ('B', ' 188 ', 'THR', 0.0785648354794216, (-35.207000000000015, 14.437999999999997, -57.97099999999999)), ('B', ' 191 ', 'SER', 0.24291627099331325, (-30.90600000000001, 11.679999999999996, -57.40899999999999)), ('B', ' 192 ', 'LYS', 0.001676356328230726, (-31.395999999999997, 13.947999999999993, -54.268)), ('B', ' 195 ', 'ILE', 0.010868080070807884, (-33.019, 21.448, -48.971)), ('B', ' 219 ', 'LEU', 0.08322868082249865, (-41.40899999999999, 21.144, -47.47)), ('B', ' 228 ', 'THR', 0.23008125133046328, (-24.827999999999992, 14.975999999999999, -42.307)), ('B', ' 257 ', 'ASN', 0.27593782716121906, (-0.6219999999999972, 54.306, -24.936999999999998)), ('B', ' 289 ', 'SER', 0.24687886893182556, (-13.786000000000001, 38.60499999999998, -25.462)), ('B', ' 301 ', 'SER', 0.23853757454147484, (1.313999999999993, 45.658, -35.311)), ('B', ' 353 ', 'GLU', 0.0433158543556407, (-6.054000000000003, 40.849, -43.444)), ('B', ' 365 ', 'GLU', 0.2890089477710791, (-2.943999999999999, 27.409, -44.12)), ('B', ' 486 ', 'SER', 0.24710055146707852, (-35.287, 13.114, -22.161)), ('B', ' 508 ', 'LYS', 0.08436782426357117, (-39.256000000000014, 38.481000000000016, -18.196))]
data['cbeta'] = [('A', '  81 ', 'PHE', ' ', 0.2996577096243739, (11.905000000000003, 65.006, -52.504)), ('A', ' 484 ', 'VAL', ' ', 0.2510419107847684, (-31.484, 38.138, -79.276)), ('A', ' 592 ', 'ILE', ' ', 0.3064371752456898, (-32.829000000000015, 18.512999999999984, -102.43799999999997)), ('B', '  20 ', 'ILE', ' ', 0.258034429985079, (-12.411, 2.758999999999997, -38.17)), ('B', ' 483 ', 'ASP', ' ', 0.26485760990391244, (-40.448, 11.254999999999999, -23.601))]
data['probe'] = [(' A 326  PRO  CG ', ' A 329  LYS  HZ1', -0.82, (-8.177, -0.846, -58.048)), (' B 279  THR  HB ', ' B 429  MET  HE2', -0.748, (-5.82, 27.489, -20.948)), (' A 326  PRO  HG2', ' A 329  LYS  HZ1', -0.723, (-8.444, -1.205, -57.404)), (' A 279  THR  HB ', ' A 429  MET  HE2', -0.688, (-0.191, 18.628, -74.509)), (' A 331  SER  HB2', ' A 353  GLU  HG3', -0.686, (-13.189, 7.854, -53.192)), (' A 326  PRO  HB2', ' A 329  LYS  HZ2', -0.666, (-9.794, -0.212, -56.664)), (' A 326  PRO  CD ', ' A 329  LYS  HZ1', -0.632, (-8.116, -0.357, -58.261)), (' A  19  CYS  HB2', ' A  23  PRO  HD2', -0.629, (-3.098, 47.436, -60.209)), (' A 326  PRO  HB2', ' A 329  LYS  NZ ', -0.626, (-9.169, 0.014, -57.001)), (' A 326  PRO  HD2', ' A 329  LYS  NZ ', -0.614, (-8.226, 0.777, -57.824)), (' A 244  GLU  HB2', ' A 276  LYS  HB2', -0.613, (9.726, 18.022, -63.447)), (' A 151  ILE HG12', ' A 226  VAL HG22', -0.612, (-30.187, 40.599, -60.846)), (' B 445  PRO  HB3', ' B 468  SER  HB3', -0.598, (-28.175, 40.246, -8.056)), (' A 445  PRO  HB3', ' A 468  SER  HB3', -0.595, (-17.858, 5.851, -91.63)), (' A 326  PRO  HD2', ' A 329  LYS  HZ1', -0.592, (-8.131, 0.078, -58.242)), (' B  19  CYS  HB2', ' B  23  PRO  HD2', -0.591, (-5.915, 0.456, -38.222)), (' B 502  ARG HH21', ' B 701  HR5  H10', -0.581, (-46.169, 29.53, -4.664)), (' B 244  GLU  HB2', ' B 276  LYS  HB2', -0.579, (7.275, 28.512, -27.279)), (' B  12  THR HG21', ' B  26  CYS  HA ', -0.548, (5.679, -1.258, -40.235)), (' B 451  THR HG21', ' B 585  LEU HD23', -0.547, (-25.435, 27.524, -6.306)), (' A   7  LEU HD13', ' A 103  VAL HG22', -0.546, (7.104, 46.138, -65.724)), (' A 293  ILE HG13', ' A 320  LYS  HB3', -0.542, (-10.782, 5.832, -67.684)), (' B 474 BMET  HG2', ' B 590  LEU  HB2', -0.541, (-38.492, 28.32, -2.713)), (' B  15  ARG  HG3', ' B  24  PHE  CD2', -0.537, (-0.119, 1.956, -43.876)), (' A   7  LEU HD21', ' A 106  PHE  HB2', -0.531, (4.423, 43.77, -65.771)), (' A 297  LEU HD11', ' A 324  TYR  HB3', -0.53, (-8.116, -0.609, -66.213)), (' B   7  LEU HD21', ' B 106  PHE  HB2', -0.527, (-0.217, 2.099, -30.214)), (' A 425  VAL HG12', ' A 429  MET  HE3', -0.525, (-1.539, 21.412, -73.591)), (' A 519  ASN  HB3', ' A 530  THR  CG2', -0.524, (-30.766, 21.863, -80.252)), (' B  13  SER  HB3', ' B  92  LEU  HB2', -0.522, (6.717, -2.61, -47.183)), (' A 451  THR HG21', ' A 585  LEU HD23', -0.519, (-15.192, 17.606, -93.927)), (' B 100  SER  HB2', ' B 103  VAL HG23', -0.515, (4.484, -1.29, -29.215)), (' A 146  LYS  HE2', ' A 227  LEU  HB3', -0.508, (-23.408, 36.316, -63.608)), (' B  13  SER  O  ', ' B  44  SER  HA ', -0.503, (1.645, -1.998, -46.889)), (' B 502  ARG  HE ', ' B 701  HR5  H4 ', -0.502, (-45.77, 31.861, -4.0)), (' B 371  VAL HG23', ' B 393  ALA  HB2', -0.501, (-0.558, 31.584, -34.91)), (' B 185  TYR  CE2', ' B 194  GLN  HG2', -0.5, (-28.666, 16.799, -49.751)), (' B 293  ILE HG13', ' B 320  LYS  HB3', -0.499, (-14.034, 41.413, -29.649)), (' B 155  ARG  HE ', ' B 164  HIS  CD2', -0.496, (-47.763, 10.075, -40.16)), (' B 425  VAL HG12', ' B 429  MET  HE3', -0.488, (-6.799, 25.605, -21.986)), (' B 297  LEU HD11', ' B 324  TYR  HB3', -0.482, (-9.868, 48.089, -29.187)), (' B 252  LEU  HB3', ' B 299  TYR  CD1', -0.482, (3.297, 42.026, -29.247)), (' B 228  THR HG22', ' B 230  HIS  CE1', -0.481, (-22.445, 16.216, -44.527)), (' A  20  ILE HD11', ' A 140  ALA  HB1', -0.481, (-11.428, 42.27, -61.183)), (' B 498  GLU  HG3', ' B 502  ARG  NH2', -0.48, (-48.045, 29.371, -5.564)), (' A 132  LEU  O  ', ' A 136  GLU  HG3', -0.48, (-3.629, 36.714, -62.141)), (' A 371  VAL HG23', ' A 393  ALA  HB2', -0.477, (-0.317, 16.116, -58.653)), (' B 510  VAL HG21', ' B 541  TYR  CD1', -0.476, (-32.705, 34.577, -21.27)), (' B  12  THR  OG1', ' B  26  CYS  HA ', -0.475, (6.154, -0.445, -40.103)), (' A  19  CYS  CB ', ' A  23  PRO  HD2', -0.468, (-3.118, 47.129, -60.393)), (' B   8  CYS  SG ', ' B  99  GLY  O  ', -0.464, (9.015, 0.526, -31.17)), (' A 280  LEU HD11', ' A 438  LEU  HG ', -0.464, (-2.112, 10.691, -77.042)), (' A 498  GLU  HG3', ' A 502  ARG  NH2', -0.462, (-37.386, 15.216, -99.705)), (' B   7  LEU HD13', ' B 103  VAL HG22', -0.461, (2.321, -0.409, -30.249)), (' A 519  ASN  HB3', ' A 530  THR HG23', -0.461, (-30.303, 21.624, -79.766)), (' B   8  CYS  SG ', ' B  99  GLY  N  ', -0.46, (9.199, 0.244, -32.451)), (' B  19  CYS  CB ', ' B  23  PRO  HD2', -0.459, (-6.089, 0.818, -37.724)), (' A 326  PRO  CB ', ' A 329  LYS  NZ ', -0.458, (-9.313, -0.599, -57.152)), (' B 192  LYS  H  ', ' B 192  LYS  HD2', -0.458, (-29.475, 12.566, -54.574)), (' B 192  LYS  HD2', ' B 192  LYS  N  ', -0.458, (-29.777, 12.365, -54.546)), (' B 278  SER  HB2', ' B 436  MET  HE2', -0.456, (-1.865, 32.964, -21.259)), (' B 508  LYS  HD2', ' B 869  HOH  O  ', -0.456, (-35.943, 41.609, -17.811)), (' B  12  THR  CG2', ' B  26  CYS  HA ', -0.455, (6.134, -1.167, -40.807)), (' B  13  SER  CB ', ' B  92  LEU  HB2', -0.452, (6.685, -2.093, -47.452)), (' A 510  VAL HG21', ' A 541  TYR  CD1', -0.448, (-25.334, 11.968, -80.055)), (' A 326  PRO  CG ', ' A 329  LYS  NZ ', -0.448, (-8.75, -0.448, -57.016)), (' A 157  VAL HG21', ' A 219  LEU  O  ', -0.447, (-44.0, 30.112, -60.746)), (' B 183  THR  OG1', ' B 228  THR  OG1', -0.446, (-27.289, 17.361, -43.184)), (' B  65  LEU HD23', ' B  81  PHE  CZ ', -0.445, (7.574, -12.94, -49.384)), (' B 154  VAL HG22', ' B 163  LEU HD13', -0.444, (-41.232, 16.681, -42.587)), (' A 158  LEU HD12', ' A 162  GLU  HB3', -0.443, (-43.746, 28.2, -70.53)), (' A 277  TYR  HA ', ' A 396  TYR  O  ', -0.443, (3.037, 16.52, -66.119)), (' A 580  ASP  OD1', ' A 584  LYS  HE2', -0.441, (-11.38, 25.414, -97.21)), (' B 182  PHE  HB3', ' B 225  PHE  HB3', -0.438, (-32.925, 15.906, -41.219)), (' B 462  LYS  HA ', ' B 462  LYS  HD3', -0.437, (-14.513, 36.96, -4.975)), (' B 184  GLY  HA3', ' B 195  ILE HG22', -0.435, (-34.385, 19.341, -46.803)), (' A 252  LEU  HB3', ' A 299  TYR  CD2', -0.434, (4.718, 5.399, -61.605)), (' A 139  LYS  O  ', ' A 143  GLU  HG2', -0.433, (-14.216, 37.696, -62.984)), (' B  13  SER  OG ', ' B  44  SER  OG ', -0.431, (3.191, -3.543, -48.349)), (' A 329  LYS  HB2', ' A 329  LYS  NZ ', -0.43, (-8.716, 1.452, -56.199)), (' A   6  VAL  HA ', ' A 129  ARG  HD2', -0.428, (5.272, 39.76, -59.807)), (' A 367  THR HG22', ' A 392  ARG  HB3', -0.428, (1.359, 18.529, -52.723)), (' A  14  LEU  HB2', ' A  25  LEU  O  ', -0.427, (5.7, 49.663, -55.727)), (' A 127  THR HG23', ' A 130  LEU  H  ', -0.427, (4.821, 37.788, -66.084)), (' B  16  CYS  O  ', ' B  22  ARG  HA ', -0.426, (-5.836, 0.396, -40.773)), (' B 258  ILE HG13', ' B 259  SER  N  ', -0.425, (-5.407, 51.148, -23.498)), (' A 278  SER  HB2', ' A 436  MET  HE2', -0.421, (3.509, 13.993, -71.516)), (' B  14  LEU  HB2', ' B  25  LEU  O  ', -0.419, (3.167, -2.152, -40.989)), (' A 480  ILE HG21', ' A 550  THR HG22', -0.419, (-27.553, 33.112, -90.369)), (' A 326  PRO  CD ', ' A 329  LYS  NZ ', -0.418, (-8.83, 0.026, -57.611)), (' B  31  TYR  CZ ', ' B  35  ILE HG21', -0.417, (2.469, -12.568, -33.02)), (' B 154  VAL HG13', ' B 163  LEU HD22', -0.416, (-43.792, 16.975, -43.204)), (' B 376  ILE  HA ', ' B 376  ILE HD12', -0.415, (-10.747, 25.803, -26.81)), (' B 533  VAL HG11', ' B 560  ARG  O  ', -0.415, (-25.557, 23.923, -16.745)), (' A 442  ARG  HA ', ' A 464  HIS  HB3', -0.412, (-10.086, 4.031, -85.212)), (' B 442  ARG  HA ', ' B 464  HIS  HB3', -0.408, (-18.68, 42.374, -11.618)), (' B 280  LEU HD11', ' B 438  LEU  HG ', -0.408, (-8.442, 35.805, -18.237)), (' A 519  ASN  HB3', ' A 530  THR HG21', -0.407, (-31.216, 21.928, -79.547)), (' B 474 BMET  CG ', ' B 590  LEU  HB2', -0.407, (-38.216, 28.059, -3.123)), (' A 512  ILE  O  ', ' A 546  PHE  HA ', -0.406, (-25.726, 19.965, -86.868)), (' B 277  TYR  HA ', ' B 396  TYR  O  ', -0.405, (0.345, 30.349, -26.433)), (' A 533  VAL HG11', ' A 560  ARG  O  ', -0.405, (-17.497, 22.144, -84.017)), (' A 462  LYS  HA ', ' A 462  LYS  HD3', -0.4, (-4.522, 8.631, -90.869))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
