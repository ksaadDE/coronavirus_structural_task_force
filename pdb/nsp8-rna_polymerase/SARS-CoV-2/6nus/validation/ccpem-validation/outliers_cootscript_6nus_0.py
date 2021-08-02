
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
data['probe'] = [(' A 571  PHE  CZ ', ' A 642  HIS  CD2', -0.671, (133.473, 160.242, 141.78)), (' A 487  CYS  SG ', ' A 642  HIS  ND1', -0.554, (129.682, 160.794, 141.834)), (' A 593  LYS  HE2', ' A 594  PHE  CZ ', -0.477, (128.095, 131.61, 157.252)), (' B 177  SER  N  ', ' B 178  PRO  CD ', -0.446, (173.794, 149.784, 181.726)), (' A 487  CYS  SG ', ' A 642  HIS  CE1', -0.446, (129.683, 160.598, 142.318)), (' A 393  THR  OG1', ' A 394  THR  N  ', -0.443, (160.874, 154.725, 161.647)), (' A 480  PHE  HA ', ' A 483  TYR  HE1', -0.443, (132.318, 145.64, 138.531)), (' B 112  ASP  N  ', ' B 112  ASP  OD1', -0.42, (154.288, 182.564, 148.955)), (' A 402  THR  OG1', ' A 403  ASN  N  ', -0.414, (152.907, 166.108, 175.856)), (' A 258  ASP  N  ', ' A 258  ASP  OD1', -0.408, (176.282, 168.361, 141.268)), (' B 120  ILE  N  ', ' B 121  PRO  CD ', -0.407, (156.764, 173.244, 160.441))]
data['smoc'] = [('A', 141, u'THR', 0.4920938743353728, (170.208, 136.286, 134.64299999999997)), ('A', 157, u'PHE', 0.5750827090503365, (173.01, 134.646, 146.983)), ('A', 161, u'ASP', 0.5599749301330684, (165.45100000000002, 134.318, 150.798)), ('A', 171, u'ILE', 0.2701650603435479, (168.20399999999998, 143.67499999999998, 148.598)), ('A', 196, u'MET', 0.45887717667473243, (168.662, 160.364, 115.031)), ('A', 212, u'LEU', 0.34512196879327367, (174.105, 147.55100000000002, 129.99200000000002)), ('A', 235, u'ASP', 0.32406945294579176, (156.758, 154.064, 123.88799999999999)), ('A', 240, u'LEU', 0.2616629516212788, (159.499, 148.478, 129.61399999999998)), ('A', 250, u'ALA', 0.35246732844993994, (167.684, 155.598, 138.811)), ('A', 254, u'GLU', 0.4182220998650871, (169.772, 163.88400000000001, 141.157)), ('A', 257, u'MET', 0.6011838739553425, (174.342, 169.44299999999998, 143.369)), ('A', 259, u'ALA', 0.3672183416821885, (173.45600000000002, 165.285, 139.64)), ('A', 261, u'LEU', 0.4159625497268489, (176.798, 160.92700000000002, 143.547)), ('A', 286, u'TYR', 0.33966009113715256, (165.44299999999998, 161.59, 130.911)), ('A', 287, u'PHE', 0.4203358059225724, (162.102, 161.319, 129.005)), ('A', 298, u'CYS', 0.3870068363827386, (147.736, 166.512, 137.83)), ('A', 312, u'ASN', 0.2992245902751274, (153.621, 157.751, 137.207)), ('A', 315, u'VAL', 0.3746411923390134, (156.45800000000003, 159.053, 141.54399999999998)), ('A', 325, u'SER', 0.41543340944763346, (158.466, 169.597, 150.97299999999998)), ('A', 350, u'GLU', 0.30183122332196244, (152.037, 161.54899999999998, 142.917)), ('A', 351, u'LEU', 0.25355202442426944, (149.68, 164.42600000000002, 142.068)), ('A', 383, u'ALA', 0.13843434492485698, (152.58200000000002, 174.137, 163.88600000000002)), ('A', 414, u'ASN', 0.5487920539886108, (138.873, 139.42200000000003, 176.49200000000002)), ('A', 419, u'PHE', 0.28146805259232643, (134.268, 128.635, 177.535)), ('A', 422, u'PHE', 0.3632427258082109, (134.494, 123.94300000000001, 179.318)), ('A', 459, u'ASN', 0.2729173074122057, (155.849, 150.918, 150.999)), ('A', 463, u'MET', 0.27333690785922926, (156.732, 153.401, 138.983)), ('A', 471, u'PHE', 0.3738129288324493, (145.516, 148.92700000000002, 128.95700000000002)), ('A', 475, u'VAL', 0.428704652578412, (140.064, 145.61399999999998, 131.153)), ('A', 483, u'TYR', 0.6065184300403235, (126.91000000000001, 147.306, 138.859)), ('A', 513, u'ARG', 0.5412585987687872, (126.74400000000001, 159.518, 165.934)), ('A', 535, u'VAL', 0.29936759610798724, (141.47299999999998, 169.41299999999998, 149.768)), ('A', 542, u'MET', 0.43980713916797987, (146.88500000000002, 154.238, 164.88400000000001)), ('A', 560, u'VAL', 0.06801172782498427, (139.77299999999997, 157.57299999999998, 159.196)), ('A', 596, u'GLY', 0.5931533605762483, (123.403, 127.57499999999999, 149.02)), ('A', 607, u'SER', 0.5823533232552801, (131.39800000000002, 128.252, 134.83200000000002)), ('A', 610, u'GLU', 0.5212066756347068, (137.004, 123.565, 129.324)), ('A', 619, u'TYR', 0.25076303240761666, (149.282, 139.001, 149.003)), ('A', 622, u'CYS', 0.16587055105485685, (148.64499999999998, 143.842, 151.108)), ('A', 678, u'GLY', -0.03562230098539696, (151.08800000000002, 154.813, 151.5)), ('A', 679, u'GLY', -0.011869031743667501, (149.178, 151.497, 151.74899999999997)), ('A', 680, u'THR', 0.10478394860497497, (145.55200000000002, 150.95200000000003, 152.82100000000003)), ('A', 685, u'ALA', 0.28618310485345266, (134.52, 153.11299999999997, 153.277)), ('A', 686, u'THR', 0.29376449647960895, (136.186, 151.76399999999998, 150.11899999999997)), ('A', 707, u'LEU', 0.311612052506533, (150.49800000000002, 135.95200000000003, 126.81400000000001)), ('A', 727, u'LEU', 0.4873813172025061, (147.375, 142.766, 122.44800000000001)), ('A', 737, u'VAL', 0.48636909820576973, (141.48000000000002, 153.012, 123.483)), ('A', 764, u'VAL', 0.4102970554566497, (140.602, 131.316, 139.903)), ('A', 777, u'ALA', 0.33462183068359475, (148.30200000000002, 133.24499999999998, 133.683)), ('A', 785, u'VAL', 0.2581832842347523, (153.893, 140.38600000000002, 138.94)), ('A', 789, u'GLN', 0.27121639660322555, (154.24299999999997, 145.618, 141.125)), ('A', 817, u'THR', 0.3084964452387705, (135.622, 123.55199999999999, 150.89600000000002)), ('A', 818, u'MET', 0.259964957910544, (134.17399999999998, 120.05, 150.555)), ('A', 819, u'LEU', 0.500674794513856, (131.516, 118.41400000000002, 148.364)), ('A', 824, u'ASP', 0.6063672449830387, (119.781, 113.406, 147.254)), ('A', 832, u'PRO', 0.36866192391954183, (136.80100000000002, 126.81400000000001, 159.05700000000002)), ('A', 834, u'PRO', 0.19706619294829933, (138.336, 123.006, 163.792)), ('A', 856, u'ILE', 0.4896335012563725, (125.346, 133.319, 173.74399999999997)), ('A', 859, u'PHE', 0.42394613895744043, (128.57899999999998, 131.096, 170.68)), ('A', 864, u'ILE', 0.36852340457097726, (126.793, 127.696, 163.08700000000002)), ('A', 885, u'LEU', 0.1228208816186925, (125.753, 123.021, 171.373)), ('A', 886, u'GLN', 0.5098594990021912, (126.353, 121.691, 174.848)), ('B', 87, u'MET', 0.4049615743789564, (136.23299999999998, 172.814, 168.52)), ('B', 95, u'LEU', 0.38768661072819754, (146.242, 179.695, 168.79399999999998)), ('B', 103, u'LEU', 0.034096533768472374, (155.51, 181.83100000000002, 162.92700000000002)), ('B', 118, u'ASN', 0.28190230517535697, (156.10299999999998, 169.906, 157.788)), ('B', 124, u'THR', 0.1834434076417446, (158.097, 177.511, 165.792)), ('B', 129, u'MET', 0.3428967599769963, (161.178, 165.841, 172.30100000000002)), ('B', 130, u'VAL', 0.4564522012370026, (163.76399999999998, 163.2, 171.491)), ('B', 156, u'ILE', 0.2540716207159033, (168.585, 169.52200000000002, 177.638)), ('B', 160, u'VAL', 0.23661310630417323, (162.394, 160.89700000000002, 181.634)), ('B', 161, u'ASP', 0.32333569954303415, (162.474, 157.121, 181.177)), ('B', 167, u'VAL', 0.3511684637517044, (166.98600000000002, 160.20899999999997, 184.88100000000003)), ('B', 169, u'LEU', 0.29148884781887596, (172.423, 162.98700000000002, 182.41299999999998)), ('B', 174, u'MET', 0.3482529998950615, (177.511, 152.27299999999997, 179.405))]
data['rota'] = [('A', ' 483 ', 'TYR', 0.009501776017991952, (126.91000000000005, 147.30600000000004, 138.859))]
data['clusters'] = [('A', '295', 1, 'Bond angle:CA:CB:CG', (151.242, 167.758, 133.515)), ('A', '298', 1, 'smoc Outlier', (147.736, 166.512, 137.83)), ('A', '312', 1, 'smoc Outlier', (153.621, 157.751, 137.207)), ('A', '315', 1, 'smoc Outlier', (156.45800000000003, 159.053, 141.54399999999998)), ('A', '350', 1, 'smoc Outlier', (152.037, 161.54899999999998, 142.917)), ('A', '351', 1, 'smoc Outlier', (149.68, 164.42600000000002, 142.068)), ('A', '463', 1, 'smoc Outlier', (156.732, 153.401, 138.983)), ('A', '471', 2, 'smoc Outlier', (145.516, 148.92700000000002, 128.95700000000002)), ('A', '475', 2, 'smoc Outlier', (140.064, 145.61399999999998, 131.153)), ('A', '477', 2, 'Bond angle:CA:CB:CG', (136.806, 148.638, 134.123)), ('A', '480', 2, 'side-chain clash', (132.318, 145.64, 138.531)), ('A', '481', 2, 'cablam Outlier', (130.6, 147.0, 134.0)), ('A', '483', 2, 'Rotamer\nside-chain clash\nsmoc Outlier', (132.318, 145.64, 138.531)), ('A', '459', 3, 'smoc Outlier', (155.849, 150.918, 150.999)), ('A', '677', 3, 'cablam Outlier', (154.0, 156.8, 153.2)), ('A', '678', 3, 'cablam CA Geom Outlier\nsmoc Outlier', (151.1, 154.8, 151.5)), ('A', '679', 3, 'smoc Outlier', (149.178, 151.497, 151.74899999999997)), ('A', '680', 3, 'smoc Outlier', (145.55200000000002, 150.95200000000003, 152.82100000000003)), ('A', '254', 4, 'smoc Outlier', (169.772, 163.88400000000001, 141.157)), ('A', '257', 4, 'smoc Outlier', (174.342, 169.44299999999998, 143.369)), ('A', '258', 4, 'side-chain clash', (176.282, 168.361, 141.268)), ('A', '259', 4, 'smoc Outlier', (173.45600000000002, 165.285, 139.64)), ('A', '261', 4, 'smoc Outlier', (176.798, 160.92700000000002, 143.547)), ('A', '817', 5, 'smoc Outlier', (135.622, 123.55199999999999, 150.89600000000002)), ('A', '818', 5, 'smoc Outlier', (134.17399999999998, 120.05, 150.555)), ('A', '819', 5, 'smoc Outlier', (131.516, 118.41400000000002, 148.364)), ('A', '194', 6, 'Bond angle:CA:CB:CG', (168.684, 163.789, 119.41400000000002)), ('A', '196', 6, 'smoc Outlier', (168.662, 160.364, 115.031)), ('A', '198', 6, 'Bond angle:CA:CB:CG', (169.134, 165.641, 113.518)), ('A', '487', 7, 'side-chain clash', (129.683, 160.598, 142.318)), ('A', '571', 7, 'side-chain clash', (133.473, 160.242, 141.78)), ('A', '642', 7, 'side-chain clash', (129.683, 160.598, 142.318)), ('A', '607', 8, 'cablam Outlier\nsmoc Outlier', (131.4, 128.3, 134.8)), ('A', '608', 8, 'cablam Outlier', (132.1, 126.5, 131.6)), ('A', '610', 8, 'smoc Outlier', (137.004, 123.565, 129.324)), ('A', '619', 9, 'smoc Outlier', (149.282, 139.001, 149.003)), ('A', '622', 9, 'smoc Outlier', (148.64499999999998, 143.842, 151.108)), ('A', '402', 10, 'backbone clash', (152.907, 166.108, 175.856)), ('A', '403', 10, 'backbone clash', (152.907, 166.108, 175.856)), ('A', '286', 11, 'smoc Outlier', (165.44299999999998, 161.59, 130.911)), ('A', '287', 11, 'smoc Outlier', (162.102, 161.319, 129.005)), ('A', '824', 12, 'Bond angle:C\ncablam Outlier\nsmoc Outlier', (119.781, 113.406, 147.254)), ('A', '825', 12, 'Bond angle:N:CA', (122.038, 115.74700000000001, 145.32700000000003)), ('A', '419', 13, 'smoc Outlier', (134.268, 128.635, 177.535)), ('A', '422', 13, 'smoc Outlier', (134.494, 123.94300000000001, 179.318)), ('A', '593', 14, 'side-chain clash', (128.095, 131.61, 157.252)), ('A', '594', 14, 'side-chain clash', (128.095, 131.61, 157.252)), ('A', '393', 15, 'backbone clash', (160.874, 154.725, 161.647)), ('A', '394', 15, 'backbone clash', (160.874, 154.725, 161.647)), ('A', '274', 16, 'cablam Outlier', (156.3, 173.5, 144.2)), ('A', '275', 16, 'cablam Outlier', (159.1, 171.7, 142.3)), ('A', '832', 17, 'smoc Outlier', (136.80100000000002, 126.81400000000001, 159.05700000000002)), ('A', '834', 17, 'smoc Outlier', (138.336, 123.006, 163.792)), ('A', '785', 18, 'smoc Outlier', (153.893, 140.38600000000002, 138.94)), ('A', '789', 18, 'smoc Outlier', (154.24299999999997, 145.618, 141.125)), ('A', '856', 19, 'smoc Outlier', (125.346, 133.319, 173.74399999999997)), ('A', '859', 19, 'Bond angle:CA:CB:CG\nsmoc Outlier', (128.57899999999998, 131.096, 170.68)), ('A', '885', 20, 'smoc Outlier', (125.753, 123.021, 171.373)), ('A', '886', 20, 'smoc Outlier', (126.353, 121.691, 174.848)), ('A', '161', 21, 'smoc Outlier', (165.45100000000002, 134.318, 150.798)), ('A', '167', 21, 'cablam Outlier', (163.1, 139.6, 154.7)), ('A', '741', 22, 'Bond angle:CA:CB:CG', (139.81, 144.83, 121.36999999999999)), ('A', '743', 22, 'Bond angle:CA:CB:CG', (135.87, 143.70899999999997, 124.955)), ('A', '325', 23, 'smoc Outlier', (158.466, 169.597, 150.97299999999998)), ('A', '326', 23, 'cablam CA Geom Outlier', (155.5, 167.3, 150.6)), ('A', '685', 24, 'smoc Outlier', (134.52, 153.11299999999997, 153.277)), ('A', '686', 24, 'smoc Outlier', (136.186, 151.76399999999998, 150.11899999999997)), ('B', '103', 1, 'smoc Outlier', (155.51, 181.83100000000002, 162.92700000000002)), ('B', '118', 1, 'smoc Outlier', (156.10299999999998, 169.906, 157.788)), ('B', '120', 1, 'side-chain clash', (156.764, 173.244, 160.441)), ('B', '121', 1, 'side-chain clash', (156.764, 173.244, 160.441)), ('B', '124', 1, 'smoc Outlier', (158.097, 177.511, 165.792)), ('B', '92', 1, 'Bond angle:CA:CB:CG', (141.95700000000002, 178.82200000000003, 170.68)), ('B', '95', 1, 'smoc Outlier', (146.242, 179.695, 168.79399999999998)), ('B', '99', 1, 'cablam Outlier', (150.7, 182.9, 167.5)), ('B', '160', 2, 'smoc Outlier', (162.394, 160.89700000000002, 181.634)), ('B', '161', 2, 'smoc Outlier', (162.474, 157.121, 181.177)), ('B', '167', 2, 'smoc Outlier', (166.98600000000002, 160.20899999999997, 184.88100000000003)), ('B', '169', 2, 'smoc Outlier', (172.423, 162.98700000000002, 182.41299999999998)), ('B', '174', 3, 'smoc Outlier', (177.511, 152.27299999999997, 179.405)), ('B', '177', 3, 'side-chain clash', (173.794, 149.784, 181.726)), ('B', '178', 3, 'side-chain clash', (173.794, 149.784, 181.726)), ('B', '129', 4, 'smoc Outlier', (161.178, 165.841, 172.30100000000002)), ('B', '130', 4, 'smoc Outlier', (163.76399999999998, 163.2, 171.491))]
data['omega'] = [('A', ' 505 ', 'PRO', None, (140.68499999999995, 165.00300000000001, 166.117)), ('B', ' 183 ', 'PRO', None, (163.055, 152.92100000000002, 176.0))]
data['cablam'] = [('A', '167', 'GLU', ' alpha helix', 'bend\nSSSST', (163.1, 139.6, 154.7)), ('A', '226', 'ALA', 'check CA trace,carbonyls, peptide', ' \nE--TT', (165.1, 164.1, 105.7)), ('A', '274', 'ASP', 'check CA trace,carbonyls, peptide', ' \n----H', (156.3, 173.5, 144.2)), ('A', '275', 'PHE', 'check CA trace,carbonyls, peptide', ' \n---HH', (159.1, 171.7, 142.3)), ('A', '481', 'ASP', ' alpha helix', ' \nTT-SS', (130.6, 147.0, 134.0)), ('A', '504', 'PHE', 'check CA trace,carbonyls, peptide', 'turn\n--TTG', (141.3, 162.6, 166.2)), ('A', '509', 'TRP', 'check CA trace,carbonyls, peptide', 'turn\nGGT-B', (134.5, 164.6, 172.1)), ('A', '607', 'SER', 'check CA trace,carbonyls, peptide', 'turn\nHHTT-', (131.4, 128.3, 134.8)), ('A', '608', 'ASP', 'check CA trace,carbonyls, peptide', 'turn\nHTT-S', (132.1, 126.5, 131.6)), ('A', '677', 'PRO', 'check CA trace,carbonyls, peptide', ' \nE--S-', (154.0, 156.8, 153.2)), ('A', '824', 'ASP', 'check CA trace,carbonyls, peptide', 'bend\n-SSSE', (119.8, 113.4, 147.3)), ('A', '151', 'CYS', 'check CA trace', 'bend\nTTSS-', (176.1, 145.4, 143.2)), ('A', '326', 'PHE', 'check CA trace', 'bend\nTSSEE', (155.5, 167.3, 150.6)), ('A', '678', 'GLY', 'check CA trace', 'bend\n--S--', (151.1, 154.8, 151.5)), ('A', '733', 'ARG', 'check CA trace', 'bend\nTSS--', (150.9, 151.3, 119.8)), ('B', '99', 'ASP', 'check CA trace,carbonyls, peptide', ' \nHH-SH', (150.7, 182.9, 167.5))]
handle_read_draw_probe_dots_unformatted("/home/ccpem/agnel/gisaid/countries_seq/structure_data/emdb/EMD-0521/6nus/Model_validation_1/validation_cootdata/molprobity_probe6nus_0.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
