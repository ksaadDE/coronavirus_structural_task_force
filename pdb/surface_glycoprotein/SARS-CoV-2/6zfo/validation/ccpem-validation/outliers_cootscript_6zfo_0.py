
from __future__ import division
import cPickle
try :
  import gobject
except ImportError :
  gobject = None
import sys

dict_residue_prop_objects = {}
class coot_extension_gui (object) :
  def __init__ (self, title) :
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

  def finish_window (self) :
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window (self, *args) :
    self.window.destroy()
    self.window = None

  def confirm_data (self, data) :
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists (self, data) :
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
        ##save property list frame object
        dict_residue_prop_objects[data_key] = list_obj
# Molprobity result viewer
class coot_molprobity_todo_list_gui (coot_extension_gui) :
  data_keys = [ "clusters","rama", "rota", "cbeta", "probe", "smoc", "fdr",
               "fsc","diffmap","cablam",
               "jpred"]
  data_titles = { "clusters"  : "Outlier residue clusters",
                  "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes",
                  "smoc"  : "Local density fit (SMOC)",
                  "fdr": "Backbone position score (FDR)",
                  "fsc": "Local density fit (FSC)",
                  "diffmap": "Model-map difference",
                  "cablam": "Ca geometry (CaBLAM)",
                  "jpred":"SS prediction"}
  data_names = { "clusters"  : ["Chain","Residue","Cluster","Outlier types"],
                 "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"],
                 "smoc" : ["Chain", "Residue", "Name", "Score"],
                 "fdr" : ["Chain", "Residue", "Name", "Score"],
                 "fsc" : ["Chain", "Residue", "Name", "Score"],
                 "diffmap" : ["Chain", "Residue", "Name", "Score"],
                 "cablam" : ["Chain", "Residue","Name","recommendation","DSSP"],
                 "jpred" : ["Chain", "Residue","Name","predicted SS","current SS"]}
  if (gobject is not None) :
    data_types = {  "clusters" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_INT, gobject.TYPE_STRING,
                             gobject.TYPE_PYOBJECT],
                    "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "smoc" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING,gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "fdr" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING,gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "fsc" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING,gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "diffmap" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING,gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cablam" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING,gobject.TYPE_STRING,
                             gobject.TYPE_STRING,gobject.TYPE_PYOBJECT],
                   "jpred" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING,gobject.TYPE_STRING,
                             gobject.TYPE_STRING,gobject.TYPE_PYOBJECT]}
  else :
    data_types = dict([ (s, []) for s in ["clusters","rama","rota","cbeta","probe","smoc",
                                          "fdr","fsc","diffmap","cablam","jpred"] ])

  def __init__ (self, data_file=None, data=None) :
    assert ([data, data_file].count(None) == 1)
    if (data is None) :
      data = load_pkl(data_file)
    if not self.confirm_data(data) :
      return
    coot_extension_gui.__init__(self, "Validation To-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets (self, data_key, box) :
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

  def toggle_probe_dots (self, *args) :
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots (self, *args) :
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui (coot_extension_gui) :
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list (object) :
  def __init__ (self, columns, column_types, rows, box,
      default_size=(380,200)) :
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)) :
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    ##adding a column type for checkbox (bool) before atom coordinate
    if gobject is not None:
        column_types = column_types[:-1]+[bool]+[column_types[-1]]
    
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns) :
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    ##add a cell for checkbox
    cell1 = gtk.CellRendererToggle()
    cell1.connect ("toggled", self.on_selected_toggled)
    column = gtk.TreeViewColumn('Dealt with',cell1,active=i+1)
    self.listctrl.append_column(column)
    #column.set_sort_column_id(i+1)
    #column.pack_start(cell1, True)
    
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      row = row[:-1] + (False,)+(row[-1],)
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

  def OnChange (self, treeview) :
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
  ##check box toggle
  def on_selected_toggled(self,renderer,path):
    if path is not None:
      model = self.listmodel.get_model()
      it = model.get_iter(path)
      #set toggle
      model[it][-2] = not model[it][-2]
      #set checkboxes for same residues in other lists
      try:
        chain = model[it][0]
        residue = model[it][1]
        for data_key in dict_residue_prop_objects:
          prop_obj = dict_residue_prop_objects[data_key]
          for row in prop_obj.listmodel.get_model():
            if data_key == 'probe':
              atom1_split = row[0].split()
              atom2_split = row[1].split()
              if atom1_split[0] == chain and atom1_split[1] == residue:
                row[-2] = model[it][-2]
              elif atom2_split[0] == chain and atom2_split[1] == residue:
                row[-2] = model[it][-2]
            elif row[0] == chain and row[1] == residue:
              row[-2] = model[it][-2]
      except IndexError: pass

  def check_chain_residue(self,chain,residue):
      pass
  
def show_probe_dots (show_dots, overlaps_only) :
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects) :
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects) :
      set_display_generic_object(object_number, 0)

def load_pkl (file_name) :
  pkl = open(file_name, "rb")
  data = cPickle.load(pkl)
  pkl.close()
  return data
data = {}
data['rama'] = []
data['cbeta'] = []
data['fdr'] = []
data['fsc'] = []
data['diffmap'] = []
data['jpred'] = []
data['probe'] = [(' B  29  PHE  O  ', ' B  72  ARG  NH2', -0.637, (223.563, 227.045, 281.472)), (' H  29  PHE  O  ', ' H  72  ARG  NH2', -0.632, (223.305, 244.549, 209.932)), (' E 339  GLY  HA2', ' E 601  NAG  H82', -0.601, (221.335, 245.095, 238.607)), (' A 339  GLY  HA2', ' A 601  NAG  H82', -0.6, (220.125, 225.792, 253.331)), (' C 109  ARG  NH2', ' C 110  THR  O  ', -0.597, (264.586, 210.199, 299.495)), (' H 124  THR HG22', ' H 155  PRO  HD3', -0.591, (231.203, 274.526, 195.57)), (' B 124  THR HG22', ' B 155  PRO  HD3', -0.589, (228.836, 195.665, 295.035)), (' C   6  GLN  NE2', ' C  86  TYR  O  ', -0.586, (251.485, 219.053, 283.011)), (' L 109  ARG  NH2', ' L 110  THR  O  ', -0.583, (265.646, 255.108, 190.043)), (' L   6  GLN  NE2', ' L  86  TYR  O  ', -0.565, (252.23, 248.24, 207.177)), (' B  11  VAL HG11', ' B 154  PHE  CE1', -0.565, (231.853, 196.647, 289.665)), (' H  11  VAL HG11', ' H 154  PHE  CE1', -0.56, (234.251, 272.391, 201.342)), (' L  37  GLN  HB2', ' L  47  LEU HD11', -0.553, (247.438, 243.746, 201.485)), (' C  37  GLN  HB2', ' C  47  LEU HD11', -0.553, (248.006, 224.673, 288.458)), (' A 359  SER  OG ', ' A 394  ASN  OD1', -0.552, (231.278, 240.019, 252.911)), (' A 518  LEU HD11', ' E 468  ILE HD12', -0.552, (240.225, 241.562, 254.978)), (' H 167  LEU HD21', ' H 190  VAL HG21', -0.546, (253.42, 269.13, 178.416)), (' C  29  ILE HG22', ' C  92  TYR  HB3', -0.542, (245.585, 224.901, 267.941)), (' B  12  VAL HG22', ' B  16  ARG  HB2', -0.54, (225.875, 198.84, 282.063)), (' H  83  MET  HB3', ' H  86  LEU HD21', -0.54, (230.475, 264.023, 211.544)), (' L  39  LYS  HD3', ' L  84  ALA  HB2', -0.538, (248.55, 248.213, 196.265)), (' L  29  ILE HG22', ' L  92  TYR  HB3', -0.538, (245.46, 243.84, 222.434)), (' B 167  LEU HD21', ' B 190  VAL HG21', -0.538, (251.319, 197.675, 311.721)), (' H  12  VAL HG22', ' H  16  ARG  HB2', -0.538, (228.224, 271.51, 208.484)), (' B  83  MET  HB3', ' B  86  LEU HD21', -0.535, (228.202, 205.686, 279.398)), (' C  39  LYS  HD3', ' C  84  ALA  HB2', -0.534, (248.56, 219.751, 293.742)), (' E 359  SER  OG ', ' E 394  ASN  OD1', -0.528, (230.183, 230.321, 238.156)), (' A 383  SER  HA ', ' C  94  THR HG21', -0.523, (234.949, 225.88, 268.589)), (' H 153  TYR  OH ', ' H 156  GLU  OE2', -0.52, (241.467, 271.127, 194.602)), (' B  11  VAL HG11', ' B 154  PHE  CZ ', -0.511, (230.714, 196.533, 289.866)), (' H  11  VAL HG11', ' H 154  PHE  CZ ', -0.509, (233.558, 272.955, 200.977)), (' L 166  GLU  N  ', ' L 166  GLU  OE1', -0.502, (250.069, 259.962, 193.973)), (' A 380  TYR  HB3', ' C  92  TYR  CZ ', -0.501, (242.685, 226.451, 263.605)), (' A 339  GLY  CA ', ' A 601  NAG  H82', -0.5, (220.166, 226.598, 252.918)), (' E 339  GLY  CA ', ' E 601  NAG  H82', -0.5, (221.23, 244.86, 238.596)), (' C 166  GLU  N  ', ' C 166  GLU  OE1', -0.498, (249.32, 207.47, 296.09)), (' A 396  TYR  OH ', ' E 466  ARG  NH1', -0.476, (237.512, 238.931, 251.32)), (' H  91  THR HG23', ' H 118  THR  HA ', -0.474, (237.016, 267.011, 204.942)), (' A 364  ASP  OD1', ' A 366  SER  OG ', -0.472, (218.897, 228.412, 261.732)), (' B  91  THR HG23', ' B 118  THR  HA ', -0.472, (235.213, 202.195, 285.571)), (' C  90  GLN  HG3', ' C  98  THR  HG1', -0.467, (245.058, 219.408, 272.701)), (' A 354  ASN  OD1', ' A 355  ARG  N  ', -0.457, (232.809, 229.23, 244.817)), (' B   6  GLU  N  ', ' B   6  GLU  OE1', -0.456, (229.91, 216.71, 290.375)), (' E 354  ASN  OD1', ' E 355  ARG  N  ', -0.453, (232.828, 240.872, 246.461)), (' A 358  ILE  HB ', ' A 395  VAL  HB ', -0.452, (229.943, 234.743, 255.153)), (' H   6  GLU  N  ', ' H   6  GLU  OE1', -0.451, (230.428, 253.348, 200.754)), (' C  46  LEU HD12', ' C  47  LEU  N  ', -0.448, (243.696, 227.84, 284.873)), (' E 393  THR  HA ', ' E 522  ALA  HA ', -0.447, (230.397, 226.95, 232.248)), (' E 358  ILE  HB ', ' E 395  VAL  HB ', -0.446, (229.284, 235.579, 236.107)), (' A 393  THR  HA ', ' A 522  ALA  HA ', -0.444, (231.731, 243.072, 259.06)), (' H  59  TYR  HB3', ' L  95  LEU HD22', -0.443, (232.766, 250.296, 221.946)), (' L  46  LEU HD12', ' L  47  LEU  N  ', -0.442, (242.74, 240.895, 205.96)), (' L   2  ILE HD12', ' L  93  SER  HB2', -0.44, (244.664, 247.927, 223.45)), (' B  57  ASN  N  ', ' B  57  ASN  OD1', -0.438, (223.076, 224.147, 269.714)), (' C   2  ILE HD12', ' C  93  SER  HB2', -0.436, (243.317, 220.96, 267.345)), (' H 105  VAL HG21', ' L  32  TYR  CD1', -0.435, (241.394, 239.003, 219.636)), (' E 367  VAL HG11', ' E 601  NAG  H83', -0.434, (220.93, 246.432, 235.474)), (' B 105  VAL HG21', ' C  32  TYR  CG ', -0.434, (241.99, 229.67, 270.967)), (' A 367  VAL HG11', ' A 601  NAG  H83', -0.434, (220.177, 225.28, 256.037)), (' H  57  ASN  N  ', ' H  57  ASN  OD1', -0.427, (223.493, 247.04, 221.561)), (' B 111  TRP  CD1', ' C  44  PRO  O  ', -0.425, (239.413, 222.071, 287.836)), (' B 153  TYR  OH ', ' B 156  GLU  OE2', -0.424, (238.708, 197.841, 296.769)), (' A 382  VAL HG22', ' A 383  SER  N  ', -0.415, (234.649, 229.716, 267.46)), (' E 382  VAL HG22', ' E 383  SER  N  ', -0.415, (234.037, 240.265, 223.745)), (' C  29  ILE HG22', ' C  92  TYR  CB ', -0.411, (245.16, 225.277, 268.158)), (' L  29  ILE HG22', ' L  92  TYR  CB ', -0.403, (245.517, 243.319, 222.667))]
data['smoc'] = [('E', 338, u'PHE', 0.2983820924691449, (223.879, 242.059, 238.23399999999998)), ('E', 363, u'ALA', 0.2541351112518293, (223.208, 236.511, 231.677)), ('E', 364, u'ASP', 0.3139889604170167, (221.117, 239.48700000000002, 230.52800000000002)), ('E', 369, u'TYR', 0.4716555434110841, (223.637, 248.71099999999998, 226.977)), ('E', 397, u'ALA', 0.2127467128254866, (232.02, 240.605, 239.36800000000002)), ('E', 401, u'VAL', 0.36470461613610883, (235.82200000000003, 252.472, 244.45100000000002)), ('E', 402, u'ILE', 0.5034396014144263, (238.74699999999999, 254.69899999999998, 243.4)), ('E', 424, u'LYS', 0.5454267232740087, (245.859, 244.10899999999998, 239.60399999999998)), ('E', 443, u'SER', 0.5373438192935209, (230.967, 262.294, 249.26399999999998)), ('E', 448, u'ASN', 0.4432558292319515, (233.969, 260.94, 253.212)), ('E', 485, u'GLY', 0.6496517596391578, (256.83299999999997, 255.994, 264.138)), ('E', 486, u'PHE', 0.6896455238317631, (260.15000000000003, 256.665, 262.412)), ('E', 497, u'PHE', 0.5371211426457675, (236.132, 262.789, 248.92000000000002)), ('E', 501, u'ASN', 0.4790851046772092, (236.92200000000003, 268.082, 244.787)), ('E', 503, u'VAL', 0.4483887744069746, (236.92800000000003, 265.551, 238.81)), ('E', 509, u'ARG', 0.3438898463256106, (232.546, 253.20899999999997, 241.404)), ('H', 1, u'GLU', 0.5080943185998069, (230.14899999999997, 238.96, 196.508)), ('H', 26, u'ALA', 0.46891599170232334, (224.442, 240.132, 199.315)), ('H', 70, u'ILE', 0.4420576744694459, (225.651, 255.26399999999998, 214.909)), ('H', 90, u'ASP', 0.43250128539261007, (236.798, 265.08799999999997, 211.409)), ('H', 91, u'THR', 0.5044163300914283, (237.877, 265.746, 207.79899999999998)), ('H', 110, u'TYR', 0.543269457169655, (235.006, 243.668, 203.82200000000003)), ('H', 134, u'PRO', 0.4976720675018127, (259.729, 278.607, 182.141)), ('H', 142, u'GLY', 0.6011937400575026, (268.65500000000003, 270.251, 179.315)), ('H', 148, u'CYS', 0.6181284595068959, (249.45700000000002, 276.302, 185.61599999999999)), ('H', 155, u'PRO', 0.6435018002166147, (234.948, 272.559, 196.433)), ('H', 156, u'GLU', 0.6489168101203607, (236.844, 269.648, 194.9)), ('H', 157, u'PRO', 0.6799663562352608, (237.578, 268.556, 192.222)), ('H', 169, u'SER', 0.6760864414321587, (253.39000000000001, 262.49699999999996, 178.41899999999998)), ('H', 180, u'SER', 0.7118330268880179, (244.005, 278.188, 205.632)), ('H', 187, u'SER', 0.5843262495097447, (249.444, 272.841, 190.77899999999997)), ('H', 188, u'SER', 0.6138650162707536, (249.77499999999998, 271.247, 187.342)), ('H', 197, u'LEU', 0.5523308807201248, (259.381, 276.742, 173.417)), ('H', 214, u'LYS', 0.7449383844619708, (235.89100000000002, 276.605, 182.258)), ('H', 223, u'SER', 0.5432395528062123, (260.22599999999994, 288.03099999999995, 178.517)), ('L', 11, u'LEU', 0.5411641302043146, (260.873, 249.414, 202.288)), ('L', 13, u'ALA', 0.6053874396972441, (261.882, 245.35200000000003, 197.21599999999998)), ('L', 21, u'ILE', 0.6589410419806175, (257.056, 243.564, 207.695)), ('L', 71, u'PHE', 0.6991155125977533, (254.21099999999998, 240.268, 214.871)), ('L', 77, u'SER', 0.734571825280047, (257.328, 235.576, 196.593)), ('L', 81, u'GLU', 0.7323223601861908, (249.85000000000002, 243.32600000000002, 192.19899999999998)), ('L', 95, u'LEU', 0.5171500287289391, (236.672, 249.57399999999998, 222.228)), ('L', 97, u'LEU', 0.532431807183043, (240.92000000000002, 250.004, 218.14399999999998)), ('L', 106, u'GLU', 0.6195481819670443, (257.445, 250.546, 196.667)), ('L', 117, u'PHE', 0.5802155676289175, (262.459, 274.33, 188.873)), ('L', 137, u'LEU', 0.6503272071895754, (260.93899999999996, 268.63, 192.242)), ('L', 142, u'PRO', 0.6319306551986543, (262.43499999999995, 257.818, 197.04299999999998)), ('L', 144, u'GLU', 0.6231333981048311, (262.03499999999997, 261.397, 201.02700000000002)), ('L', 146, u'LYS', 0.5451204739983737, (263.575, 267.974, 201.93800000000002)), ('L', 148, u'GLN', 0.5009371167119618, (263.599, 274.394, 202.27599999999998)), ('L', 150, u'LYS', 0.3930828638652874, (265.057, 280.767, 201.877)), ('L', 151, u'VAL', 0.5233863928268878, (264.198, 284.465, 201.607)), ('L', 155, u'LEU', 0.5972224765411898, (264.92999999999995, 280.122, 206.52700000000002)), ('L', 170, u'LYS', 0.5855575155152049, (256.01099999999997, 254.62800000000001, 183.95000000000002)), ('L', 181, u'THR', 0.6648839827060297, (252.125, 281.777, 199.532)), ('L', 182, u'LEU', 0.6865932065751206, (252.289, 285.34400000000005, 200.82600000000002)), ('L', 184, u'LYS', 0.7136170600500749, (252.17, 291.519, 197.961)), ('L', 191, u'LYS', 0.549487668335533, (264.559, 290.314, 197.05800000000002)), ('L', 193, u'TYR', 0.6712196140106698, (263.756, 283.775, 196.83100000000002)), ('L', 210, u'PHE', 0.6631698294106559, (265.96099999999996, 284.224, 191.60999999999999)), ('L', 213, u'GLY', 0.5064082443843142, (261.90599999999995, 291.638, 189.23899999999998)), ('A', 515, u'PHE', 0.269972152723158, (235.569, 234.251, 258.846)), ('A', 519, u'HIS', 0.568005588134312, (239.08800000000002, 247.44, 260.556)), ('A', 354, u'ASN', 0.26122890081495553, (233.784, 227.21899999999997, 244.248)), ('A', 397, u'ALA', 0.23621032754379787, (231.844, 229.61399999999998, 251.92600000000002)), ('A', 401, u'VAL', 0.2777459154805119, (234.101, 217.42200000000003, 246.692)), ('A', 424, u'LYS', 0.5415923915139689, (245.194, 224.624, 251.07399999999998)), ('A', 435, u'ALA', 0.2811079761791493, (232.054, 217.15200000000002, 255.27299999999997)), ('A', 436, u'TRP', 0.41579267363053485, (229.311, 214.63, 254.61899999999997)), ('A', 485, u'GLY', 0.6139746862603938, (253.70299999999997, 211.708, 226.08700000000002)), ('A', 486, u'PHE', 0.6698135342533796, (257.001, 210.67299999999997, 227.664)), ('A', 499, u'PRO', 0.47527259369449587, (228.20299999999997, 202.874, 244.57299999999998)), ('A', 509, u'ARG', 0.348775121336336, (230.903, 217.034, 249.883)), ('B', 1, u'GLU', 0.5647640508208487, (231.542, 230.778, 294.959)), ('B', 17, u'SER', 0.596755930226485, (223.395, 202.38400000000001, 280.204)), ('B', 18, u'LEU', 0.6217770612915435, (223.98000000000002, 204.954, 282.93699999999995)), ('B', 28, u'THR', 0.6525508007156933, (223.788, 231.791, 285.615)), ('B', 70, u'ILE', 0.43125244762308945, (224.56, 215.35800000000003, 276.57099999999997)), ('B', 92, u'ALA', 0.5390175585609003, (236.76, 206.811, 284.57099999999997)), ('B', 93, u'VAL', 0.602385907295731, (235.846, 209.66899999999998, 286.90599999999995)), ('B', 96, u'CYS', 0.592638693745247, (231.228, 218.686, 284.787)), ('B', 97, u'ALA', 0.4866549347393132, (232.914, 221.996, 283.99399999999997)), ('B', 101, u'GLY', 0.5239179903927592, (233.212, 232.283, 277.47599999999994)), ('B', 111, u'TRP', 0.5730974705072555, (235.632, 221.901, 288.123)), ('B', 125, u'LYS', 0.7054070636663627, (230.85100000000003, 189.839, 296.663)), ('B', 132, u'LEU', 0.6939565806707272, (250.883, 187.87, 304.845)), ('B', 136, u'SER', 0.5957521079320149, (263.59299999999996, 186.54299999999998, 309.64900000000006)), ('B', 142, u'GLY', 0.6672344050182788, (266.717, 195.011, 310.477)), ('B', 157, u'PRO', 0.6947412891817606, (235.626, 200.466, 298.693)), ('B', 162, u'TRP', 0.7431921644928645, (245.27399999999997, 197.363, 311.99799999999993)), ('B', 167, u'LEU', 0.7236390064668401, (248.407, 200.586, 314.774)), ('B', 173, u'THR', 0.7004692699303221, (247.12800000000001, 200.484, 302.28)), ('B', 182, u'GLY', 0.6675519838774546, (235.876, 191.79899999999998, 287.39799999999997)), ('B', 187, u'SER', 0.6935487825575187, (246.95800000000003, 194.818, 299.67400000000004)), ('B', 197, u'LEU', 0.6491473545258112, (256.95799999999997, 189.555, 316.635)), ('B', 214, u'LYS', 0.6882482935948393, (233.35600000000002, 192.529, 308.632)), ('B', 218, u'ARG', 0.7000180704120257, (245.05800000000002, 187.10399999999998, 312.76)), ('B', 222, u'LYS', 0.5281082053566971, (255.317, 181.339, 309.306)), ('C', 13, u'ALA', 0.5644005323141311, (262.199, 220.89100000000002, 292.924)), ('C', 19, u'VAL', 0.5987361911067796, (259.884, 226.129, 288.4359999999999)), ('C', 21, u'ILE', 0.4932385991675878, (257.22099999999995, 223.463, 282.683)), ('C', 55, u'GLN', 0.6246966465935312, (242.712, 233.536, 286.23199999999997)), ('C', 69, u'THR', 0.6454366032259681, (253.84, 225.435, 269.584)), ('C', 101, u'GLY', 0.5618087003070216, (250.53, 214.12800000000001, 279.695)), ('C', 106, u'GLU', 0.5059775220159337, (257.17, 216.282, 293.589)), ('C', 107, u'ILE', 0.6600596065635811, (258.763, 217.343, 296.85)), ('C', 143, u'ARG', 0.6278299869483062, (258.23299999999995, 206.248, 291.945)), ('C', 144, u'GLU', 0.5596180266879733, (260.184, 205.026, 288.894)), ('C', 148, u'GLN', 0.5176253991018497, (260.05400000000003, 191.961, 287.405)), ('C', 149, u'TRP', 0.5728865838815174, (258.584, 188.553, 288.23299999999995)), ('C', 150, u'LYS', 0.5433125408898427, (260.71599999999995, 185.45000000000002, 287.656)), ('C', 168, u'ASP', 0.6375023216869077, (253.83700000000002, 210.11499999999998, 301.565)), ('C', 170, u'LYS', 0.6253018270928462, (255.74499999999998, 212.17399999999998, 306.29799999999994)), ('C', 210, u'PHE', 0.5502921472676319, (261.587, 181.71599999999998, 297.828))]
data['rota'] = [('H', '  50 ', 'VAL', 0.1442130604468759, (230.50400000000005, 250.16899999999995, 216.193)), ('H', '  57 ', 'ASN', 0.09528682485673119, (224.55700000000004, 248.41799999999995, 221.51800000000003)), ('H', ' 105 ', 'VAL', 0.011559342916888234, (237.2290000000001, 240.249, 219.102)), ('H', ' 212 ', 'ASN', 0.18241267354449964, (230.641, 275.698, 186.40599999999998)), ('H', ' 217 ', 'LYS', 0.1973203510640664, (245.112, 279.8840000000001, 180.037)), ('L', '  45 ', 'LYS', 0.16570414710865006, (241.3700000000001, 245.06, 201.94400000000002)), ('L', ' 182 ', 'LEU', 0.144750299776889, (252.289, 285.344, 200.82600000000002)), ('B', '  50 ', 'VAL', 0.1448144520074374, (229.924, 219.875, 275.166)), ('B', '  57 ', 'ASN', 0.09540865670967717, (224.044, 222.375, 270.072)), ('B', ' 105 ', 'VAL', 0.01159879805727411, (237.653, 228.99000000000007, 272.118)), ('B', ' 212 ', 'ASN', 0.18284115234019155, (228.109, 194.095, 304.68)), ('B', ' 217 ', 'LYS', 0.19781448752738384, (242.204, 188.17599999999993, 310.494)), ('C', '  45 ', 'LYS', 0.16471028651449812, (241.713, 223.83, 289.065)), ('C', ' 182 ', 'LEU', 0.1445220259883531, (247.52700000000002, 182.48399999999995, 289.179))]
data['clusters'] = [('E', '358', 1, 'side-chain clash', (229.284, 235.579, 236.107)), ('E', '359', 1, 'side-chain clash', (230.183, 230.321, 238.156)), ('E', '393', 1, 'side-chain clash', (230.397, 226.95, 232.248)), ('E', '394', 1, 'side-chain clash', (230.183, 230.321, 238.156)), ('E', '395', 1, 'side-chain clash', (229.284, 235.579, 236.107)), ('E', '397', 1, 'smoc Outlier', (232.02, 240.605, 239.36800000000002)), ('E', '522', 1, 'side-chain clash', (230.397, 226.95, 232.248)), ('E', '443', 2, 'smoc Outlier', (230.967, 262.294, 249.26399999999998)), ('E', '448', 2, 'smoc Outlier', (233.969, 260.94, 253.212)), ('E', '497', 2, 'smoc Outlier', (236.132, 262.789, 248.92000000000002)), ('E', '501', 2, 'smoc Outlier', (236.92200000000003, 268.082, 244.787)), ('E', '503', 2, 'smoc Outlier', (236.92800000000003, 265.551, 238.81)), ('E', '338', 3, 'smoc Outlier', (223.879, 242.059, 238.23399999999998)), ('E', '339', 3, 'side-chain clash', (221.23, 244.86, 238.596)), ('E', '367', 3, 'side-chain clash', (220.93, 246.432, 235.474)), ('E', '601', 3, 'side-chain clash', (220.93, 246.432, 235.474)), ('E', '401', 4, 'smoc Outlier', (235.82200000000003, 252.472, 244.45100000000002)), ('E', '402', 4, 'smoc Outlier', (238.74699999999999, 254.69899999999998, 243.4)), ('E', '509', 4, 'smoc Outlier', (232.546, 253.20899999999997, 241.404)), ('E', '382', 5, 'backbone clash', (234.037, 240.265, 223.745)), ('E', '383', 5, 'backbone clash', (234.037, 240.265, 223.745)), ('E', '386', 5, 'cablam Outlier', (229.2, 239.2, 220.7)), ('E', '484', 6, 'cablam CA Geom Outlier', (254.4, 253.1, 264.2)), ('E', '485', 6, 'cablam Outlier\nsmoc Outlier', (256.8, 256.0, 264.1)), ('E', '486', 6, 'cablam Outlier\nsmoc Outlier', (260.2, 256.7, 262.4)), ('E', '363', 7, 'smoc Outlier', (223.208, 236.511, 231.677)), ('E', '364', 7, 'smoc Outlier', (221.117, 239.48700000000002, 230.52800000000002)), ('E', '466', 8, 'side-chain clash', (237.512, 238.931, 251.32)), ('E', '468', 8, 'side-chain clash', (240.225, 241.562, 254.978)), ('E', '354', 9, 'backbone clash', (232.828, 240.872, 246.461)), ('E', '355', 9, 'backbone clash', (232.828, 240.872, 246.461)), ('H', '11', 1, 'side-chain clash', (233.558, 272.955, 200.977)), ('H', '120', 1, 'Bond angle:C', (235.30200000000002, 273.95099999999996, 206.095)), ('H', '121', 1, 'Bond angle:N:CA', (233.04, 277.03299999999996, 205.911)), ('H', '124', 1, 'side-chain clash', (231.203, 274.526, 195.57)), ('H', '154', 1, 'side-chain clash', (233.558, 272.955, 200.977)), ('H', '155', 1, 'side-chain clash\nsmoc Outlier', (231.203, 274.526, 195.57)), ('H', '118', 2, 'side-chain clash', (237.016, 267.011, 204.942)), ('H', '83', 2, 'side-chain clash', (230.475, 264.023, 211.544)), ('H', '86', 2, 'side-chain clash', (230.475, 264.023, 211.544)), ('H', '90', 2, 'smoc Outlier', (236.798, 265.08799999999997, 211.409)), ('H', '91', 2, 'side-chain clash\nsmoc Outlier', (237.016, 267.011, 204.942)), ('H', '153', 3, 'side-chain clash', (241.467, 271.127, 194.602)), ('H', '156', 3, 'side-chain clash\nsmoc Outlier', (241.467, 271.127, 194.602)), ('H', '157', 3, 'smoc Outlier', (237.578, 268.556, 192.222)), ('H', '167', 4, 'side-chain clash', (253.42, 269.13, 178.416)), ('H', '169', 4, 'smoc Outlier', (253.39000000000001, 262.49699999999996, 178.41899999999998)), ('H', '190', 4, 'side-chain clash', (253.42, 269.13, 178.416)), ('H', '148', 5, 'smoc Outlier', (249.45700000000002, 276.302, 185.61599999999999)), ('H', '187', 5, 'smoc Outlier', (249.444, 272.841, 190.77899999999997)), ('H', '188', 5, 'smoc Outlier', (249.77499999999998, 271.247, 187.342)), ('H', '212', 6, 'Rotamer', (230.641, 275.698, 186.40599999999998)), ('H', '214', 6, 'smoc Outlier', (235.89100000000002, 276.605, 182.258)), ('H', '1', 7, 'smoc Outlier', (230.14899999999997, 238.96, 196.508)), ('H', '26', 7, 'cablam Outlier\nsmoc Outlier', (224.4, 240.1, 199.3)), ('H', '29', 8, 'side-chain clash', (223.305, 244.549, 209.932)), ('H', '72', 8, 'side-chain clash', (223.305, 244.549, 209.932)), ('H', '105', 9, 'Rotamer', (237.2290000000001, 240.249, 219.102)), ('H', '6', 9, 'side-chain clash', (241.394, 239.003, 219.636)), ('H', '12', 10, 'side-chain clash', (228.224, 271.51, 208.484)), ('H', '16', 10, 'side-chain clash', (228.224, 271.51, 208.484)), ('L', '106', 1, 'smoc Outlier', (257.445, 250.546, 196.667)), ('L', '11', 1, 'smoc Outlier', (260.873, 249.414, 202.288)), ('L', '13', 1, 'smoc Outlier', (261.882, 245.35200000000003, 197.21599999999998)), ('L', '37', 1, 'side-chain clash', (247.438, 243.746, 201.485)), ('L', '39', 1, 'side-chain clash', (248.55, 248.213, 196.265)), ('L', '45', 1, 'Rotamer', (241.3700000000001, 245.06, 201.94400000000002)), ('L', '46', 1, 'backbone clash', (242.74, 240.895, 205.96)), ('L', '47', 1, 'side-chain clash\nbackbone clash', (242.74, 240.895, 205.96)), ('L', '81', 1, 'smoc Outlier', (249.85000000000002, 243.32600000000002, 192.19899999999998)), ('L', '83', 1, 'cablam Outlier', (252.8, 246.9, 195.7)), ('L', '84', 1, 'side-chain clash', (248.55, 248.213, 196.265)), ('L', '142', 2, 'smoc Outlier', (262.43499999999995, 257.818, 197.04299999999998)), ('L', '144', 2, 'smoc Outlier', (262.03499999999997, 261.397, 201.02700000000002)), ('L', '146', 2, 'smoc Outlier', (263.575, 267.974, 201.93800000000002)), ('L', '148', 2, 'smoc Outlier', (263.599, 274.394, 202.27599999999998)), ('L', '150', 2, 'smoc Outlier', (265.057, 280.767, 201.877)), ('L', '151', 2, 'smoc Outlier', (264.198, 284.465, 201.607)), ('L', '155', 2, 'smoc Outlier', (264.92999999999995, 280.122, 206.52700000000002)), ('L', '191', 2, 'smoc Outlier', (264.559, 290.314, 197.05800000000002)), ('L', '193', 2, 'smoc Outlier', (263.756, 283.775, 196.83100000000002)), ('L', '210', 2, 'smoc Outlier', (265.96099999999996, 284.224, 191.60999999999999)), ('L', '2', 3, 'side-chain clash', (244.664, 247.927, 223.45)), ('L', '29', 3, 'side-chain clash', (245.517, 243.319, 222.667)), ('L', '31', 3, 'cablam Outlier', (247.1, 237.1, 219.0)), ('L', '32', 3, 'side-chain clash', (241.394, 239.003, 219.636)), ('L', '92', 3, 'side-chain clash', (245.517, 243.319, 222.667)), ('L', '93', 3, 'side-chain clash', (244.664, 247.927, 223.45)), ('L', '97', 3, 'smoc Outlier', (240.92000000000002, 250.004, 218.14399999999998)), ('L', '21', 4, 'smoc Outlier', (257.056, 243.564, 207.695)), ('L', '6', 4, 'backbone clash', (252.23, 248.24, 207.177)), ('L', '86', 4, 'backbone clash', (252.23, 248.24, 207.177)), ('L', '181', 5, 'smoc Outlier', (252.125, 281.777, 199.532)), ('L', '182', 5, 'Rotamer\nsmoc Outlier', (252.289, 285.344, 200.82600000000002)), ('L', '184', 5, 'smoc Outlier', (252.17, 291.519, 197.961)), ('L', '117', 6, 'smoc Outlier', (262.459, 274.33, 188.873)), ('L', '137', 6, 'smoc Outlier', (260.93899999999996, 268.63, 192.242)), ('L', '109', 7, 'backbone clash\nDihedral angle:CD:NE:CZ:NH1', (264.23799999999994, 251.24399999999997, 191.638)), ('L', '110', 7, 'backbone clash', (265.646, 255.108, 190.043)), ('L', '69', 8, 'cablam Outlier', (254.0, 242.2, 221.0)), ('L', '71', 8, 'smoc Outlier', (254.21099999999998, 240.268, 214.871)), ('A', '364', 1, 'side-chain clash', (218.897, 228.412, 261.732)), ('A', '366', 1, 'side-chain clash', (218.897, 228.412, 261.732)), ('A', '367', 1, 'side-chain clash', (220.177, 225.28, 256.037)), ('A', '601', 1, 'side-chain clash', (220.177, 225.28, 256.037)), ('A', '358', 2, 'side-chain clash', (229.943, 234.743, 255.153)), ('A', '395', 2, 'side-chain clash', (229.943, 234.743, 255.153)), ('A', '397', 2, 'smoc Outlier', (231.844, 229.61399999999998, 251.92600000000002)), ('A', '515', 2, 'smoc Outlier', (235.569, 234.251, 258.846)), ('A', '401', 3, 'smoc Outlier', (234.101, 217.42200000000003, 246.692)), ('A', '435', 3, 'smoc Outlier', (232.054, 217.15200000000002, 255.27299999999997)), ('A', '436', 3, 'smoc Outlier', (229.311, 214.63, 254.61899999999997)), ('A', '509', 3, 'smoc Outlier', (230.903, 217.034, 249.883)), ('A', '382', 4, 'backbone clash', (234.649, 229.716, 267.46)), ('A', '383', 4, 'backbone clash', (234.649, 229.716, 267.46)), ('A', '386', 4, 'cablam Outlier', (230.0, 231.2, 270.7)), ('A', '484', 5, 'cablam CA Geom Outlier', (251.6, 214.8, 226.1)), ('A', '485', 5, 'cablam Outlier\nsmoc Outlier', (253.7, 211.7, 226.1)), ('A', '486', 5, 'cablam Outlier\nsmoc Outlier', (257.0, 210.7, 227.7)), ('A', '393', 6, 'side-chain clash', (231.731, 243.072, 259.06)), ('A', '522', 6, 'side-chain clash', (231.731, 243.072, 259.06)), ('A', '359', 7, 'side-chain clash', (242.685, 226.451, 263.605)), ('A', '394', 7, 'side-chain clash', (242.685, 226.451, 263.605)), ('A', '354', 8, 'backbone clash\nsmoc Outlier', (232.809, 229.23, 244.817)), ('A', '355', 8, 'backbone clash', (232.809, 229.23, 244.817)), ('B', '11', 1, 'side-chain clash', (230.714, 196.533, 289.866)), ('B', '120', 1, 'Bond angle:C', (232.26999999999998, 195.562, 284.857)), ('B', '121', 1, 'Bond angle:N:CA', (229.67399999999998, 192.76, 285.09099999999995)), ('B', '124', 1, 'side-chain clash', (228.836, 195.665, 295.035)), ('B', '125', 1, 'smoc Outlier', (230.85100000000003, 189.839, 296.663)), ('B', '154', 1, 'side-chain clash', (230.714, 196.533, 289.866)), ('B', '155', 1, 'side-chain clash', (228.836, 195.665, 295.035)), ('B', '182', 1, 'smoc Outlier', (235.876, 191.79899999999998, 287.39799999999997)), ('B', '101', 2, 'smoc Outlier', (233.212, 232.283, 277.47599999999994)), ('B', '111', 2, 'smoc Outlier', (235.632, 221.901, 288.123)), ('B', '57', 2, 'Rotamer\nside-chain clash', (239.413, 222.071, 287.836)), ('B', '6', 2, 'side-chain clash', (229.91, 216.71, 290.375)), ('B', '96', 2, 'smoc Outlier', (231.228, 218.686, 284.787)), ('B', '97', 2, 'smoc Outlier', (232.914, 221.996, 283.99399999999997)), ('B', '99', 2, 'cablam Outlier', (233.3, 227.2, 280.1)), ('B', '12', 3, 'side-chain clash', (225.875, 198.84, 282.063)), ('B', '16', 3, 'side-chain clash', (225.875, 198.84, 282.063)), ('B', '17', 3, 'smoc Outlier', (223.395, 202.38400000000001, 280.204)), ('B', '18', 3, 'smoc Outlier', (223.98000000000002, 204.954, 282.93699999999995)), ('B', '83', 3, 'side-chain clash', (228.202, 205.686, 279.398)), ('B', '86', 3, 'side-chain clash', (228.202, 205.686, 279.398)), ('B', '118', 4, 'side-chain clash', (235.213, 202.195, 285.571)), ('B', '91', 4, 'side-chain clash', (235.213, 202.195, 285.571)), ('B', '92', 4, 'smoc Outlier', (236.76, 206.811, 284.57099999999997)), ('B', '93', 4, 'smoc Outlier', (235.846, 209.66899999999998, 286.90599999999995)), ('B', '153', 5, 'side-chain clash', (238.708, 197.841, 296.769)), ('B', '156', 5, 'side-chain clash', (238.708, 197.841, 296.769)), ('B', '157', 5, 'smoc Outlier', (235.626, 200.466, 298.693)), ('B', '162', 6, 'smoc Outlier', (245.27399999999997, 197.363, 311.99799999999993)), ('B', '167', 6, 'side-chain clash\nsmoc Outlier', (251.319, 197.675, 311.721)), ('B', '190', 6, 'side-chain clash', (251.319, 197.675, 311.721)), ('B', '28', 7, 'smoc Outlier', (223.788, 231.791, 285.615)), ('B', '29', 7, 'side-chain clash', (223.563, 227.045, 281.472)), ('B', '72', 7, 'side-chain clash', (223.563, 227.045, 281.472)), ('B', '217', 8, 'Rotamer', (242.204, 188.17599999999993, 310.494)), ('B', '218', 8, 'smoc Outlier', (245.05800000000002, 187.10399999999998, 312.76)), ('B', '212', 9, 'Rotamer', (228.109, 194.095, 304.68)), ('B', '214', 9, 'smoc Outlier', (233.35600000000002, 192.529, 308.632)), ('B', '1', 10, 'smoc Outlier', (231.542, 230.778, 294.959)), ('B', '26', 10, 'cablam Outlier', (225.6, 230.3, 292.3)), ('B', '173', 11, 'smoc Outlier', (247.12800000000001, 200.484, 302.28)), ('B', '187', 11, 'smoc Outlier', (246.95800000000003, 194.818, 299.67400000000004)), ('C', '106', 1, 'smoc Outlier', (257.17, 216.282, 293.589)), ('C', '107', 1, 'smoc Outlier', (258.763, 217.343, 296.85)), ('C', '109', 1, 'backbone clash\nDihedral angle:CD:NE:CZ:NH1', (264.018, 214.648, 298.319)), ('C', '110', 1, 'backbone clash', (264.586, 210.199, 299.495)), ('C', '13', 1, 'smoc Outlier', (262.199, 220.89100000000002, 292.924)), ('C', '39', 1, 'side-chain clash', (248.56, 219.751, 293.742)), ('C', '83', 1, 'cablam Outlier', (253.0, 220.4, 294.8)), ('C', '84', 1, 'side-chain clash', (248.56, 219.751, 293.742)), ('C', '2', 2, 'side-chain clash', (243.317, 220.96, 267.345)), ('C', '29', 2, 'side-chain clash', (245.16, 225.277, 268.158)), ('C', '31', 2, 'cablam Outlier', (247.7, 231.4, 271.9)), ('C', '32', 2, 'side-chain clash', (241.99, 229.67, 270.967)), ('C', '90', 2, 'side-chain clash', (245.058, 219.408, 272.701)), ('C', '92', 2, 'side-chain clash', (245.16, 225.277, 268.158)), ('C', '93', 2, 'side-chain clash', (243.317, 220.96, 267.345)), ('C', '98', 2, 'side-chain clash', (245.058, 219.408, 272.701)), ('C', '37', 3, 'side-chain clash', (248.006, 224.673, 288.458)), ('C', '44', 3, 'backbone clash', (239.413, 222.071, 287.836)), ('C', '45', 3, 'Rotamer', (241.713, 223.83, 289.065)), ('C', '46', 3, 'backbone clash', (243.696, 227.84, 284.873)), ('C', '47', 3, 'side-chain clash\nbackbone clash', (243.696, 227.84, 284.873)), ('C', '55', 3, 'smoc Outlier', (242.712, 233.536, 286.23199999999997)), ('C', '148', 4, 'smoc Outlier', (260.05400000000003, 191.961, 287.405)), ('C', '149', 4, 'smoc Outlier', (258.584, 188.553, 288.23299999999995)), ('C', '150', 4, 'smoc Outlier', (260.71599999999995, 185.45000000000002, 287.656)), ('C', '101', 5, 'smoc Outlier', (250.53, 214.12800000000001, 279.695)), ('C', '6', 5, 'backbone clash', (251.485, 219.053, 283.011)), ('C', '86', 5, 'backbone clash', (251.485, 219.053, 283.011)), ('C', '168', 6, 'smoc Outlier', (253.83700000000002, 210.11499999999998, 301.565)), ('C', '170', 6, 'smoc Outlier', (255.74499999999998, 212.17399999999998, 306.29799999999994)), ('C', '19', 7, 'smoc Outlier', (259.884, 226.129, 288.4359999999999)), ('C', '21', 7, 'smoc Outlier', (257.22099999999995, 223.463, 282.683)), ('C', '143', 8, 'smoc Outlier', (258.23299999999995, 206.248, 291.945)), ('C', '144', 8, 'smoc Outlier', (260.184, 205.026, 288.894))]
data['omega'] = [('B', ' 155 ', 'PRO', None, (231.617, 195.77599999999995, 295.143)), ('B', ' 157 ', 'PRO', None, (234.296, 200.72599999999994, 298.138)), ('C', '   8 ', 'PRO', None, (259.009, 218.412, 281.589)), ('C', ' 142 ', 'PRO', None, (262.545, 208.145, 293.376)), ('H', ' 155 ', 'PRO', None, (234.265, 273.7139999999999, 195.84)), ('H', ' 157 ', 'PRO', None, (236.247, 268.458, 192.825)), ('L', '   8 ', 'PRO', None, (259.505, 248.36499999999998, 208.621)), ('L', ' 142 ', 'PRO', None, (263.798, 257.94700000000006, 196.513))]
data['cablam'] = [('E', '386', 'LYS', ' alpha helix', 'helix-3\nSGGGT', (229.2, 239.2, 220.7)), ('E', '485', 'GLY', 'check CA trace,carbonyls, peptide', 'beta bridge\n--BTT', (256.8, 256.0, 264.1)), ('E', '486', 'PHE', 'check CA trace,carbonyls, peptide', 'turn\n-BTTE', (260.2, 256.7, 262.4)), ('E', '519', 'HIS', 'check CA trace,carbonyls, peptide', 'bend\n--SS-', (236.9, 222.1, 230.5)), ('E', '484', 'GLU', 'check CA trace', ' \nS--BT', (254.4, 253.1, 264.2)), ('H', '26', 'ALA', 'check CA trace,carbonyls, peptide', 'bend\nEESS-', (224.4, 240.1, 199.3)), ('H', '99', 'ASP', ' beta sheet', ' \nEE---', (232.8, 242.4, 211.2)), ('L', '31', 'SER', 'check CA trace,carbonyls, peptide', 'bend\nESS-E', (247.1, 237.1, 219.0)), ('L', '69', 'THR', 'check CA trace,carbonyls, peptide', 'strand\nEEEEE', (254.0, 242.2, 221.0)), ('L', '83', 'PHE', 'check CA trace,carbonyls, peptide', ' \nGG-SE', (252.8, 246.9, 195.7)), ('A', '386', 'LYS', ' alpha helix', 'helix-3\nSGGGT', (230.0, 231.2, 270.7)), ('A', '485', 'GLY', 'check CA trace,carbonyls, peptide', 'beta bridge\n--BTT', (253.7, 211.7, 226.1)), ('A', '486', 'PHE', 'check CA trace,carbonyls, peptide', 'turn\n-BTTE', (257.0, 210.7, 227.7)), ('A', '519', 'HIS', 'check CA trace,carbonyls, peptide', 'bend\n--SS-', (239.1, 247.4, 260.6)), ('A', '484', 'GLU', 'check CA trace', ' \nS--BT', (251.6, 214.8, 226.1)), ('B', '26', 'ALA', 'check CA trace,carbonyls, peptide', 'bend\nEESS-', (225.6, 230.3, 292.3)), ('B', '99', 'ASP', ' beta sheet', ' \nEE---', (233.3, 227.2, 280.1)), ('C', '31', 'SER', 'check CA trace,carbonyls, peptide', 'bend\nESS-E', (247.7, 231.4, 271.9)), ('C', '69', 'THR', 'check CA trace,carbonyls, peptide', 'strand\nEEEEE', (253.8, 225.4, 269.6)), ('C', '83', 'PHE', 'check CA trace,carbonyls, peptide', ' \nGG-SE', (253.0, 220.4, 294.8))]
handle_read_draw_probe_dots_unformatted("/home/ccpem/agnel/gisaid/countries_seq/structure_data/emdb/EMD-11184/6zfo/Model_validation_1/validation_cootdata/molprobity_probe6zfo_0.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
