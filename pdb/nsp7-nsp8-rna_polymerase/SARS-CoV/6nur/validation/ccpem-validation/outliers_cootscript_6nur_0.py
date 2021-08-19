
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
data['probe'] = [(' A 583  ARG  HG3', ' A 583  ARG HH11', -0.894, (124.906, 139.306, 145.095)), (' A 487  CYS  SG ', ' A 642  HIS  CE1', -0.863, (128.909, 161.139, 142.377)), (' A 412  PRO  HG3', ' C  14  LEU HD23', -0.801, (148.095, 138.694, 178.568)), (' A 631  ARG  HG3', ' A 663  LEU HD21', -0.732, (145.664, 154.338, 147.756)), (' A 306  CYS  HG ', ' A1001   ZN ZN  ', -0.719, (147.469, 164.842, 131.837)), (' A 619  TYR  HE1', ' A 786  LEU HD21', -0.718, (149.097, 140.25, 143.817)), (' A 583  ARG  HG3', ' A 583  ARG  NH1', -0.674, (124.577, 139.303, 146.168)), (' A 306  CYS  SG ', ' A1001   ZN ZN  ', -0.666, (147.459, 165.177, 131.349)), (' A 487  CYS  SG ', ' A 642  HIS  ND1', -0.664, (129.796, 161.36, 141.63)), (' A 372  LEU  HA ', ' B  87  MET  HE1', -0.652, (134.865, 171.205, 162.887)), (' A 631  ARG  HG3', ' A 663  LEU  CD2', -0.631, (146.271, 154.754, 148.143)), (' A 733  ARG  O  ', ' A 734  ASN  C  ', -0.62, (148.21, 151.919, 120.982)), (' A 718  LYS  HG2', ' A 721  ARG HH12', -0.602, (147.55, 130.954, 113.509)), (' C   5  ASP  OD2', ' D  97  LYS  NZ ', -0.569, (143.935, 119.625, 182.596)), (' A 712  GLY  O  ', ' A 721  ARG  HG3', -0.557, (151.975, 132.211, 117.531)), (' A 402  THR  O  ', ' B 129  MET  SD ', -0.53, (155.989, 166.461, 172.81)), (' A 412  PRO  HG3', ' C  14  LEU  CD2', -0.513, (148.919, 138.99, 179.225)), (' B 112  ASP  N  ', ' B 112  ASP  OD1', -0.501, (154.922, 182.798, 148.458)), (' A 571  PHE  CZ ', ' A 642  HIS  CD2', -0.497, (133.221, 160.44, 142.091)), (' A 306  CYS  O  ', ' A 310  CYS  SG ', -0.494, (148.844, 163.219, 132.902)), (' D 157  GLN  O  ', ' D 158  GLN  HG3', -0.492, (178.729, 134.853, 197.009)), (' A 456  TYR  CE1', ' A 624  ARG  HD3', -0.483, (151.082, 150.842, 156.514)), (' A 785  VAL HG13', ' A 789  GLN  HG3', -0.48, (151.808, 143.581, 138.95)), (' A 618  ASP  O  ', ' A 794  MET  SD ', -0.465, (150.701, 136.32, 146.315)), (' A 583  ARG  CG ', ' A 583  ARG  NH1', -0.457, (124.458, 138.548, 145.98)), (' C  14  LEU HD22', ' C  36  HIS  CG ', -0.457, (150.828, 137.021, 178.472)), (' A 619  TYR  CE1', ' A 786  LEU HD21', -0.447, (149.354, 140.744, 144.278)), (' B 177  SER  N  ', ' B 178  PRO  CD ', -0.446, (172.787, 149.479, 180.981)), (' A 647  ASN  O  ', ' A 651  ARG  HG3', -0.44, (134.412, 165.553, 137.151)), (' A 117  GLN  HG2', ' A 118  ARG  HG3', -0.436, (184.468, 146.45, 119.798)), (' C  14  LEU HD22', ' C  36  HIS  CD2', -0.435, (150.605, 137.59, 178.507)), (' A 164  ASP  OD1', ' A 165  PHE  N  ', -0.432, (161.524, 140.7, 149.877)), (' A 642  HIS  HB3', ' A 646  CYS  HB2', -0.422, (130.837, 162.872, 138.908)), (' A 456  TYR  CD1', ' A 624  ARG  HD3', -0.421, (151.604, 150.818, 156.513)), (' A 402  THR  OG1', ' A 403  ASN  N  ', -0.413, (152.969, 165.994, 175.548)), (' A 372  LEU  CA ', ' B  87  MET  HE1', -0.41, (134.961, 171.074, 162.459)), (' A 208  ASP  N  ', ' A 208  ASP  OD1', -0.406, (166.301, 145.305, 122.229)), (' A 712  GLY  O  ', ' A 721  ARG  CG ', -0.406, (151.924, 132.574, 117.67))]
data['smoc'] = [('A', 117, u'GLN', 0.3743776016179415, (181.4, 146.272, 118.783)), ('A', 142, u'LEU', 0.5123289228652514, (170.007, 138.771, 137.335)), ('A', 171, u'ILE', 0.33571511388777453, (168.47299999999998, 143.92000000000002, 148.304)), ('A', 178, u'LEU', 0.40664978215180253, (172.447, 149.668, 139.064)), ('A', 193, u'CYS', 0.4971258717159513, (167.37800000000001, 160.142, 119.64999999999999)), ('A', 200, u'GLY', 0.6131622409093708, (166.506, 162.33200000000002, 109.24700000000001)), ('A', 201, u'ILE', 0.5397145262184004, (166.10999999999999, 158.791, 110.573)), ('A', 222, u'PHE', 0.4944144569261584, (165.59, 152.401, 110.926)), ('A', 240, u'LEU', 0.42855436299283506, (159.42100000000002, 148.61399999999998, 129.503)), ('A', 241, u'LEU', 0.4472757575385872, (162.178, 150.39000000000001, 131.54399999999998)), ('A', 251, u'LEU', 0.44096094314241147, (167.542, 159.393, 139.504)), ('A', 259, u'ALA', 0.5173530436583234, (173.57399999999998, 165.348, 139.084)), ('A', 286, u'TYR', 0.4680561889655, (165.578, 161.708, 130.472)), ('A', 312, u'ASN', 0.386551615764693, (153.578, 157.854, 136.978)), ('A', 326, u'PHE', 0.43003793555412173, (155.49, 167.353, 150.38000000000002)), ('A', 350, u'GLU', 0.3084889199768025, (151.92600000000002, 161.737, 142.66899999999998)), ('A', 351, u'LEU', 0.374546114210421, (149.555, 164.606, 141.80700000000002)), ('A', 369, u'LYS', 0.3925867631846428, (131.60399999999998, 173.66899999999998, 158.845)), ('A', 376, u'ALA', 0.35469843470450724, (140.637, 168.253, 161.097)), ('A', 378, u'PRO', 0.3556964103715606, (147.011, 169.33200000000002, 160.917)), ('A', 382, u'ALA', 0.3079298129222627, (151.56, 170.373, 163.83100000000002)), ('A', 383, u'ALA', 0.4073137696891946, (152.466, 174.078, 163.52200000000002)), ('A', 408, u'GLN', 0.4038432088091969, (149.82700000000003, 151.585, 174.489)), ('A', 422, u'PHE', 0.5572856729925532, (132.752, 121.918, 179.843)), ('A', 423, u'ALA', 0.5281663016439725, (134.553, 121.02499999999999, 176.642)), ('A', 434, u'SER', 0.43961728423733554, (143.35600000000002, 116.509, 165.77599999999998)), ('A', 436, u'GLU', 0.3845394208079334, (143.918, 122.009, 169.168)), ('A', 475, u'VAL', 0.4451195815530524, (140.005, 145.538, 131.256)), ('A', 516, u'TYR', 0.5039705098466978, (125.74000000000001, 163.162, 162.151)), ('A', 519, u'MET', 0.43867312305805806, (124.933, 168.696, 161.078)), ('A', 525, u'ASP', 0.4391054844831133, (125.974, 168.494, 151.529)), ('A', 538, u'THR', 0.3408669075616183, (142.853, 165.16, 157.524)), ('A', 560, u'VAL', 0.3333698554156149, (139.69299999999998, 157.44299999999998, 159.83800000000002)), ('A', 575, u'LEU', 0.5475747288136018, (128.475, 152.208, 143.96800000000002)), ('A', 610, u'GLU', 0.5435187875191806, (136.993, 123.82, 129.499)), ('A', 658, u'GLU', 0.3393323342476621, (140.955, 160.797, 148.76999999999998)), ('A', 659, u'CYS', 0.3644111207752418, (144.731, 160.87, 148.334)), ('A', 663, u'LEU', 0.384607479322715, (147.347, 157.655, 150.978)), ('A', 665, u'GLU', 0.3829975164201728, (147.622, 161.577, 155.454)), ('A', 669, u'CYS', 0.3728340809524462, (150.316, 157.282, 166.976)), ('A', 676, u'LYS', 0.41939274057775705, (152.047, 157.86800000000002, 155.98600000000002)), ('A', 692, u'SER', 0.37322530832532724, (139.155, 144.252, 144.612)), ('A', 693, u'VAL', 0.3817084146668356, (139.848, 146.77599999999998, 141.88500000000002)), ('A', 707, u'LEU', 0.36937307644578377, (150.52100000000002, 135.798, 127.118)), ('A', 782, u'PHE', 0.4105650170628884, (151.53, 136.311, 139.941)), ('A', 789, u'GLN', 0.3735839457116251, (154.316, 145.83100000000002, 141.112)), ('A', 790, u'ASN', 0.41632388323214653, (154.184, 145.819, 144.915)), ('A', 794, u'MET', 0.40436572630620826, (155.33700000000002, 135.954, 147.248)), ('A', 818, u'MET', 0.511276335178093, (133.683, 120.49600000000001, 150.74299999999997)), ('A', 829, u'LEU', 0.5334540412135348, (129.54, 124.05799999999999, 152.165)), ('A', 837, u'ILE', 0.3965277564236761, (135.916, 127.91400000000002, 166.78)), ('A', 841, u'GLY', 0.3563021324302395, (134.494, 129.869, 172.442)), ('A', 864, u'ILE', 0.43145323075789144, (126.13, 128.039, 163.256)), ('A', 915, u'ARG', 0.5025341481480983, (118.23, 125.681, 157.869)), ('B', 83, u'VAL', 0.48101981340305766, (130.76399999999998, 170.459, 169.73299999999998)), ('B', 98, u'LEU', 0.3011419680753351, (151.094, 179.05, 167.71399999999997)), ('B', 103, u'LEU', 0.34674594235733947, (156.0, 181.77299999999997, 162.526)), ('B', 169, u'LEU', 0.39876900843997237, (172.191, 162.58800000000002, 182.366)), ('B', 174, u'MET', 0.5824282982194966, (176.722, 151.934, 178.79299999999998)), ('B', 185, u'ILE', 0.401572343047359, (162.56, 160.742, 175.997)), ('C', 8, u'CYS', 0.3710253424437507, (144.79399999999998, 128.74299999999997, 179.67)), ('C', 33, u'VAL', 0.39975070553408487, (154.35800000000003, 139.547, 178.004)), ('C', 48, u'ALA', 0.1251544803151681, (155.66, 125.895, 178.52700000000002)), ('C', 51, u'LYS', 0.3450309178048266, (158.04899999999998, 129.796, 181.222)), ('C', 67, u'ASP', 0.12583948634269157, (146.32100000000003, 135.54, 198.346)), ('D', 103, u'LEU', 0.36362915901915877, (155.21399999999997, 125.46600000000001, 190.44)), ('D', 122, u'LEU', 0.37215798138443235, (166.01, 129.591, 183.121)), ('D', 167, u'VAL', 0.3203180316952726, (176.722, 136.024, 206.685)), ('D', 169, u'LEU', 0.037970242877966194, (177.22, 129.71299999999997, 205.32000000000002)), ('D', 172, u'ILE', 0.24319490903987823, (173.58700000000002, 129.82000000000002, 209.437)), ('D', 180, u'LEU', 0.26816665611905544, (171.212, 136.73399999999998, 212.684))]
data['rota'] = [('A', ' 583 ', 'ARG', 0.028116265133834216, (125.30000000000004, 138.43, 142.7)), ('A', ' 631 ', 'ARG', 0.0, (145.66399999999993, 153.137, 144.937)), ('A', ' 651 ', 'ARG', 0.2810002969545315, (136.57199999999995, 164.612, 139.818)), ('A', ' 733 ', 'ARG', 0.0, (150.96399999999994, 151.433, 119.82299999999996)), ('A', ' 785 ', 'VAL', 0.25515418933865, (154.029, 140.622, 138.812))]
data['clusters'] = [('A', '369', 1, 'smoc Outlier', (131.60399999999998, 173.66899999999998, 158.845)), ('A', '376', 1, 'smoc Outlier', (140.637, 168.253, 161.097)), ('A', '377', 1, 'Bond angle:CA:CB:CG', (143.5, 170.22299999999998, 159.54299999999998)), ('A', '378', 1, 'smoc Outlier', (147.011, 169.33200000000002, 160.917)), ('A', '382', 1, 'smoc Outlier', (151.56, 170.373, 163.83100000000002)), ('A', '383', 1, 'smoc Outlier', (152.466, 174.078, 163.52200000000002)), ('A', '402', 1, 'backbone clash', (134.961, 171.074, 162.459)), ('A', '403', 1, 'backbone clash', (134.961, 171.074, 162.459)), ('A', '456', 1, 'side-chain clash', (151.604, 150.818, 156.513)), ('A', '487', 1, 'side-chain clash', (134.865, 171.205, 162.887)), ('A', '538', 1, 'smoc Outlier', (142.853, 165.16, 157.524)), ('A', '624', 1, 'side-chain clash', (151.604, 150.818, 156.513)), ('A', '631', 1, 'Rotamer\nside-chain clash', (146.271, 154.754, 148.143)), ('A', '658', 1, 'smoc Outlier', (140.955, 160.797, 148.76999999999998)), ('A', '659', 1, 'smoc Outlier', (144.731, 160.87, 148.334)), ('A', '663', 1, 'side-chain clash\nsmoc Outlier', (146.271, 154.754, 148.143)), ('A', '665', 1, 'smoc Outlier', (147.622, 161.577, 155.454)), ('A', '676', 1, 'smoc Outlier', (152.047, 157.86800000000002, 155.98600000000002)), ('A', '677', 1, 'cablam Outlier', (154.1, 157.0, 152.8)), ('A', '678', 1, 'cablam CA Geom Outlier', (151.2, 154.9, 151.2)), ('A', '618', 2, 'side-chain clash', (150.701, 136.32, 146.315)), ('A', '619', 2, 'side-chain clash', (149.354, 140.744, 144.278)), ('A', '782', 2, 'smoc Outlier', (151.53, 136.311, 139.941)), ('A', '785', 2, 'Rotamer\nside-chain clash', (151.808, 143.581, 138.95)), ('A', '786', 2, 'side-chain clash', (149.354, 140.744, 144.278)), ('A', '789', 2, 'side-chain clash\nsmoc Outlier', (151.808, 143.581, 138.95)), ('A', '790', 2, 'smoc Outlier', (154.184, 145.819, 144.915)), ('A', '794', 2, 'side-chain clash\nsmoc Outlier', (150.701, 136.32, 146.315)), ('A', '571', 3, 'side-chain clash', (133.221, 160.44, 142.091)), ('A', '642', 3, 'side-chain clash', (130.837, 162.872, 138.908)), ('A', '646', 3, 'side-chain clash', (130.837, 162.872, 138.908)), ('A', '647', 3, 'side-chain clash', (134.412, 165.553, 137.151)), ('A', '651', 3, 'Rotamer\nside-chain clash', (134.412, 165.553, 137.151)), ('A', '652', 3, 'Bond angle:CA:CB:CG', (140.164, 165.805, 140.287)), ('A', '200', 4, 'smoc Outlier', (166.506, 162.33200000000002, 109.24700000000001)), ('A', '201', 4, 'smoc Outlier', (166.10999999999999, 158.791, 110.573)), ('A', '219', 4, 'Bond angle:CA:CB:CG', (169.612, 149.69, 113.512)), ('A', '222', 4, 'smoc Outlier', (165.59, 152.401, 110.926)), ('A', '226', 4, 'cablam Outlier', (164.9, 163.6, 105.2)), ('A', '240', 5, 'smoc Outlier', (159.42100000000002, 148.61399999999998, 129.503)), ('A', '241', 5, 'smoc Outlier', (162.178, 150.39000000000001, 131.54399999999998)), ('A', '242', 5, 'Bond angle:CA:C', (159.805, 152.38500000000002, 133.765)), ('A', '243', 5, 'Bond angle:N', (159.312, 149.786, 136.6)), ('A', '164', 6, 'backbone clash', (161.524, 140.7, 149.877)), ('A', '165', 6, 'backbone clash', (161.524, 140.7, 149.877)), ('A', '167', 6, 'cablam Outlier', (163.1, 140.1, 154.7)), ('A', '712', 7, 'side-chain clash\nbackbone clash', (151.924, 132.574, 117.67)), ('A', '718', 7, 'side-chain clash', (147.55, 130.954, 113.509)), ('A', '721', 7, 'side-chain clash\nbackbone clash', (151.924, 132.574, 117.67)), ('A', '516', 8, 'smoc Outlier', (125.74000000000001, 163.162, 162.151)), ('A', '517', 8, 'Bond angle:CA:CB:CG', (123.202, 164.336, 164.73)), ('A', '519', 8, 'smoc Outlier', (124.933, 168.696, 161.078)), ('A', '607', 9, 'cablam Outlier', (131.2, 128.6, 134.9)), ('A', '608', 9, 'cablam Outlier', (132.1, 126.8, 131.7)), ('A', '610', 9, 'smoc Outlier', (136.993, 123.82, 129.499)), ('A', '692', 10, 'smoc Outlier', (139.155, 144.252, 144.612)), ('A', '693', 10, 'smoc Outlier', (139.848, 146.77599999999998, 141.88500000000002)), ('A', '818', 11, 'smoc Outlier', (133.683, 120.49600000000001, 150.74299999999997)), ('A', '829', 11, 'smoc Outlier', (129.54, 124.05799999999999, 152.165)), ('A', '824', 12, 'Bond angle:C\ncablam Outlier', (119.17499999999998, 114.009, 147.624)), ('A', '825', 12, 'Bond angle:N:CA', (121.482, 116.256, 145.642)), ('A', '193', 13, 'smoc Outlier', (167.37800000000001, 160.142, 119.64999999999999)), ('A', '194', 13, 'Bond angle:CA:CB:CG', (168.724, 163.654, 118.962)), ('A', '306', 14, 'side-chain clash', (148.844, 163.219, 132.902)), ('A', '310', 14, 'side-chain clash', (148.844, 163.219, 132.902)), ('A', '117', 15, 'side-chain clash\nsmoc Outlier', (184.468, 146.45, 119.798)), ('A', '118', 15, 'side-chain clash', (184.468, 146.45, 119.798)), ('A', '274', 16, 'cablam Outlier', (156.2, 173.6, 143.9)), ('A', '275', 16, 'cablam Outlier', (159.0, 172.0, 141.9)), ('A', '837', 17, 'smoc Outlier', (135.916, 127.91400000000002, 166.78)), ('A', '841', 17, 'smoc Outlier', (134.494, 129.869, 172.442)), ('A', '422', 18, 'smoc Outlier', (132.752, 121.918, 179.843)), ('A', '423', 18, 'smoc Outlier', (134.553, 121.02499999999999, 176.642)), ('A', '845', 19, 'cablam Outlier', (136.7, 140.3, 174.7)), ('A', '846', 19, 'Bond angle:CA:CB:CG', (135.49200000000002, 140.98100000000002, 178.296)), ('A', '434', 20, 'smoc Outlier', (143.35600000000002, 116.509, 165.77599999999998)), ('A', '436', 20, 'smoc Outlier', (143.918, 122.009, 169.168)), ('A', '151', 21, 'cablam CA Geom Outlier', (176.3, 145.6, 142.8)), ('A', '178', 21, 'smoc Outlier', (172.447, 149.668, 139.064)), ('A', '733', 22, 'Rotamer\nbackbone clash\ncablam CA Geom Outlier', (148.21, 151.919, 120.982)), ('A', '734', 22, 'backbone clash', (148.21, 151.919, 120.982)), ('A', '741', 23, 'Bond angle:CA:CB:CG', (139.991, 144.738, 121.59400000000001)), ('A', '743', 23, 'Bond angle:CA:CB:CG', (135.967, 143.571, 125.05)), ('A', '350', 24, 'smoc Outlier', (151.92600000000002, 161.737, 142.66899999999998)), ('A', '351', 24, 'smoc Outlier', (149.555, 164.606, 141.80700000000002)), ('B', '103', 1, 'smoc Outlier', (156.0, 181.77299999999997, 162.526)), ('B', '98', 1, 'smoc Outlier', (151.094, 179.05, 167.71399999999997)), ('B', '99', 1, 'cablam Outlier', (151.3, 182.8, 167.2)), ('B', '174', 2, 'smoc Outlier', (176.722, 151.934, 178.79299999999998)), ('B', '177', 2, 'side-chain clash', (172.787, 149.479, 180.981)), ('B', '178', 2, 'side-chain clash', (172.787, 149.479, 180.981)), ('C', '14', 1, 'side-chain clash', (150.605, 137.59, 178.507)), ('C', '33', 1, 'smoc Outlier', (154.35800000000003, 139.547, 178.004)), ('C', '36', 1, 'side-chain clash', (150.605, 137.59, 178.507)), ('C', '48', 2, 'smoc Outlier', (155.66, 125.895, 178.52700000000002)), ('C', '51', 2, 'smoc Outlier', (158.04899999999998, 129.796, 181.222)), ('C', '5', 3, 'Bond angle:CA:CB:CG', (145.74599999999998, 123.804, 180.61399999999998)), ('C', '8', 3, 'smoc Outlier', (144.79399999999998, 128.74299999999997, 179.67)), ('C', '64', 4, 'cablam Outlier', (150.7, 143.1, 200.0)), ('C', '67', 4, 'smoc Outlier', (146.32100000000003, 135.54, 198.346)), ('D', '167', 1, 'smoc Outlier', (176.722, 136.024, 206.685)), ('D', '169', 1, 'smoc Outlier', (177.22, 129.71299999999997, 205.32000000000002)), ('D', '172', 1, 'smoc Outlier', (173.58700000000002, 129.82000000000002, 209.437)), ('D', '157', 2, 'side-chain clash', (178.729, 134.853, 197.009)), ('D', '158', 2, 'side-chain clash', (178.729, 134.853, 197.009)), ('D', '180', 3, 'smoc Outlier', (171.212, 136.73399999999998, 212.684)), ('D', '182', 3, 'cablam CA Geom Outlier', (166.6, 137.4, 209.4))]
data['omega'] = [('A', ' 505 ', 'PRO', None, (140.83699999999988, 165.133, 165.982)), ('B', ' 183 ', 'PRO', None, (162.44799999999992, 153.121, 175.681)), ('D', ' 183 ', 'PRO', None, (165.02599999999995, 138.321, 207.82599999999994))]
data['cablam'] = [('A', '167', 'GLU', ' alpha helix', 'bend\nSSSST', (163.1, 140.1, 154.7)), ('A', '226', 'ALA', 'check CA trace,carbonyls, peptide', ' \nE--TT', (164.9, 163.6, 105.2)), ('A', '274', 'ASP', 'check CA trace,carbonyls, peptide', ' \n----H', (156.2, 173.6, 143.9)), ('A', '275', 'PHE', 'check CA trace,carbonyls, peptide', ' \n---HH', (159.0, 172.0, 141.9)), ('A', '481', 'ASP', ' alpha helix', 'turn\nTTTT-', (130.6, 147.2, 134.0)), ('A', '504', 'PHE', 'check CA trace,carbonyls, peptide', 'turn\n--TTG', (141.5, 162.7, 165.9)), ('A', '509', 'TRP', 'check CA trace,carbonyls, peptide', 'turn\nGGT-B', (134.3, 164.8, 172.0)), ('A', '607', 'SER', 'check CA trace,carbonyls, peptide', 'turn\nHHTT-', (131.2, 128.6, 134.9)), ('A', '608', 'ASP', 'check CA trace,carbonyls, peptide', 'turn\nHTT-S', (132.1, 126.8, 131.7)), ('A', '677', 'PRO', 'check CA trace,carbonyls, peptide', ' \nE--S-', (154.1, 157.0, 152.8)), ('A', '824', 'ASP', 'check CA trace,carbonyls, peptide', 'bend\n-SSSE', (119.2, 114.0, 147.6)), ('A', '845', 'ASP', 'check CA trace,carbonyls, peptide', ' \nEE-S-', (136.7, 140.3, 174.7)), ('A', '151', 'CYS', 'check CA trace', 'bend\nTTSS-', (176.3, 145.6, 142.8)), ('A', '326', 'PHE', 'check CA trace', 'bend\nGGSEE', (155.5, 167.4, 150.4)), ('A', '678', 'GLY', 'check CA trace', 'bend\n--S--', (151.2, 154.9, 151.2)), ('A', '733', 'ARG', 'check CA trace', 'bend\nTSS--', (151.0, 151.4, 119.8)), ('B', '99', 'ASP', 'check CA trace,carbonyls, peptide', ' \nHH-SH', (151.3, 182.8, 167.2)), ('B', '182', 'TRP', 'check CA trace', 'bend\nS-SSE', (164.1, 152.4, 177.3)), ('C', '64', 'GLY', 'check CA trace,carbonyls, peptide', 'bend\nS-SS-', (150.7, 143.1, 200.0)), ('D', '182', 'TRP', 'check CA trace', 'bend\nS-SSE', (166.6, 137.4, 209.4))]
handle_read_draw_probe_dots_unformatted("/home/ccpem/agnel/gisaid/countries_seq/structure_data/emdb/EMD-0520/6nur/Model_validation_1/validation_cootdata/molprobity_probe6nur_0.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
