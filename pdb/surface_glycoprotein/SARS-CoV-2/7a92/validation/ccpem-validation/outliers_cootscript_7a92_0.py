
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
data['cbeta'] = []
data['fdr'] = []
data['fsc'] = []
data['diffmap'] = []
data['jpred'] = []
data['probe'] = [(' A 559  PHE  CE2', ' A 584  ILE HD12', -1.006, (206.384, 182.374, 183.551)), (' A 559  PHE  CE2', ' A 584  ILE  CD1', -0.82, (206.307, 182.761, 182.959)), (' A 559  PHE  HE2', ' A 584  ILE HD12', -0.769, (205.988, 183.349, 183.971)), (' A  67  ALA  O  ', ' A 262  ALA  HA ', -0.729, (214.63, 237.033, 152.829)), (' A 559  PHE  HE2', ' A 584  ILE  CD1', -0.72, (206.07, 183.799, 183.877)), (' A 362  VAL HG23', ' A 526  GLY  HA3', -0.639, (197.402, 200.65, 197.372)), (' A 546  LEU  CD2', ' A 565  PHE  CE2', -0.61, (208.018, 191.872, 189.529)), (' D 168  TRP  HE1', ' D 502  SER  HB3', -0.602, (211.356, 222.94, 278.595)), (' A 592  PHE  H  ', ' A 634  ARG  NH2', -0.588, (219.99, 193.245, 171.526)), (' A 393  THR  O  ', ' A 523  THR  OG1', -0.565, (199.101, 190.228, 201.618)), (' D 269  ASP  OD1', ' D 270  MET  N  ', -0.559, (214.863, 230.281, 273.516)), (' D  85  LEU  O  ', ' D  94  LYS  NZ ', -0.553, (224.719, 188.034, 254.222)), (' D 247  LYS  HB3', ' D 282  THR HG22', -0.544, (227.64, 242.0, 272.387)), (' D 261  CYS  HB2', ' D 488  VAL HG13', -0.532, (228.583, 230.362, 283.424)), (' D  32  PHE  CD1', ' D  76  GLN  HG2', -0.527, (206.773, 193.341, 251.378)), (' A 329  PHE  HE2', ' A 528  LYS  HD3', -0.507, (203.311, 202.74, 192.352)), (' A 589  PRO  O  ', ' A 590  CYS  C  ', -0.507, (216.764, 195.458, 174.566)), (' D 402  GLU  HB3', ' D 518  ARG  HD3', -0.502, (220.346, 220.501, 257.719)), (' A 546  LEU HD23', ' A 565  PHE  CE2', -0.502, (207.778, 192.118, 190.026)), (' A 457  ARG  NH1', ' A 467  ASP  OD1', -0.501, (204.018, 181.229, 229.688)), (' A  21  ARG  NH1', ' A  79  PHE  O  ', -0.495, (205.064, 232.018, 151.374)), (' A  96  GLU  OE2', ' A 101  ILE  N  ', -0.494, (210.87, 238.382, 161.797)), (' A 641  ASN  HB3', ' A 653  ALA  O  ', -0.488, (240.075, 199.147, 160.89)), (' A 503  VAL  HA ', ' A 506  GLN HE21', -0.475, (202.885, 210.941, 232.678)), (' D 204  ARG  HD2', ' D 219  ARG  O  ', -0.473, (228.478, 204.613, 268.124)), (' D 187  LYS  HB3', ' D 199  TYR  CD2', -0.468, (215.569, 203.937, 273.782)), (' D 320  LEU  HB3', ' D 321  PRO  HD2', -0.467, (218.794, 218.368, 237.487)), (' D 177  ARG  HB3', ' D 178  PRO  HD3', -0.466, (209.895, 213.832, 287.803)), (' D 457  GLU  HG2', ' D 513  ILE  HB ', -0.463, (223.948, 213.159, 268.198)), (' A 246  ARG  NH2', ' A 254  SER  O  ', -0.459, (199.217, 241.672, 148.508)), (' D 284  PRO  HB3', ' D 594  TRP  CH2', -0.458, (232.103, 243.565, 265.143)), (' A 292  ALA  CB ', ' A 321  GLN HE22', -0.457, (220.304, 207.798, 174.588)), (' D 476  LYS  O  ', ' D 480  MET  HG2', -0.456, (227.445, 217.495, 282.846)), (' A 320  VAL  O  ', ' A 320  VAL HG12', -0.456, (214.616, 203.244, 171.884)), (' A 594  GLY  O  ', ' A 612  TYR  HA ', -0.45, (230.157, 194.407, 171.57)), (' A 418  ILE HD13', ' A 422  ASN HD22', -0.447, (205.299, 192.813, 230.711)), (' A  29  THR HG23', ' A  62  VAL HG23', -0.447, (219.252, 223.41, 160.16)), (' A 108  THR HG22', ' A 109  THR HG23', -0.446, (192.368, 219.905, 164.772)), (' A 421  TYR  CD1', ' A 457  ARG  HB3', -0.446, (208.999, 185.269, 232.064)), (' D 439  LEU  HA ', ' D 439  LEU HD23', -0.444, (228.746, 235.928, 257.913)), (' A 592  PHE  H  ', ' A 634  ARG HH21', -0.443, (220.925, 192.994, 171.271)), (' A 319  ARG  HA ', ' A 319  ARG  HD3', -0.442, (219.59, 201.366, 174.311)), (' A 321  GLN  HA ', ' A 321  GLN  NE2', -0.442, (217.87, 206.651, 174.366)), (' D 291  ILE  O  ', ' D 291  ILE HG13', -0.437, (219.675, 241.497, 251.734)), (' D 398  GLU  HG3', ' D 514  ARG  HG2', -0.436, (220.996, 212.428, 261.253)), (' D  93  VAL HG12', ' D  97  LEU HD12', -0.435, (218.702, 190.382, 249.899)), (' D 455  MET  HB3', ' D 455  MET  HE3', -0.435, (225.33, 220.811, 275.294)), (' A 500  THR  OG1', ' D  41  TYR  OH ', -0.431, (198.474, 211.081, 241.846)), (' D 315  PHE  HA ', ' D 318  VAL HG12', -0.431, (220.524, 224.71, 239.195)), (' A  29  THR  OG1', ' A  30  ASN  N  ', -0.43, (222.367, 222.406, 159.63)), (' D 308  PHE  CZ ', ' D 333  LEU HD22', -0.428, (206.294, 227.712, 246.239)), (' A 185  ASN  HB2', ' A 212  LEU  O  ', -0.428, (224.912, 238.287, 157.679)), (' A 341  VAL HG23', ' A 356  LYS  HZ2', -0.428, (193.099, 197.053, 212.101)), (' A 115  GLN HE22', ' A 167  THR HG23', -0.426, (188.719, 229.477, 175.487)), (' D 336  PRO  HG2', ' D 340  GLN  O  ', -0.426, (192.607, 227.251, 253.002)), (' A 431  GLY  HA3', ' A 513  LEU  O  ', -0.424, (206.088, 196.453, 211.844)), (' A 206  LYS  HB3', ' A 223  LEU HD22', -0.417, (218.577, 231.525, 174.305)), (' D 524  GLN  HG2', ' D 583  PRO  HG2', -0.417, (235.059, 220.838, 254.399)), (' A 100  ILE HD11', ' A 245  HIS  HE1', -0.417, (211.356, 242.891, 156.009)), (' D 482  ARG HH21', ' D 489  GLU  CD ', -0.416, (225.045, 226.207, 288.22)), (' A 642  VAL HG22', ' A 651  ILE HG12', -0.416, (233.347, 197.26, 161.85)), (' A 102  ARG  HD2', ' A 121  ASN  O  ', -0.415, (204.833, 241.64, 165.044)), (' A 105  ILE HD11', ' A 239  GLN HE21', -0.414, (198.616, 229.514, 160.864)), (' D 230  PHE  HA ', ' D 233  ILE HG22', -0.414, (234.643, 221.443, 267.588)), (' A 409  GLN  OE1', ' A 418  ILE  HB ', -0.412, (209.419, 195.903, 229.114)), (' D 209  VAL HG11', ' D 565  PRO  HB3', -0.41, (230.021, 201.907, 253.401)), (' D 403  ALA  O  ', ' D 407  ILE HG23', -0.409, (224.307, 222.221, 251.471)), (' D  96  GLN  HG2', ' D 391  LEU  HB2', -0.409, (215.396, 198.199, 249.602)), (' A 355  ARG  NH2', ' A 398  ASP  OD2', -0.408, (201.809, 190.793, 215.966)), (' D 529  LEU HD21', ' D 554  LEU HD22', -0.407, (226.679, 220.877, 244.625)), (' A 382  VAL HG11', ' A 387  LEU  HB3', -0.407, (207.725, 200.683, 204.947)), (' A  33  THR  HA ', ' A  58  PHE  CD2', -0.406, (224.163, 219.946, 171.164)), (' A 200  TYR  HB3', ' A 228  ASP  OD1', -0.403, (203.217, 225.913, 181.777)), (' D 215  TYR  HE2', ' D 568  LEU HD13', -0.402, (233.722, 204.443, 247.443)), (' A  44  ARG  O  ', ' A 283  GLY  HA2', -0.4, (225.78, 227.953, 188.922))]
data['smoc'] = [('D', 23, u'GLU', 0.7932533914844154, (218.148, 184.047, 243.72)), ('D', 35, u'GLU', 0.8244744057398598, (202.843, 196.092, 246.36200000000002)), ('D', 42, u'GLN', 0.8189339514573785, (197.83800000000002, 205.55, 248.467)), ('D', 46, u'ALA', 0.8186054110814464, (195.507, 210.597, 251.83700000000002)), ('D', 57, u'GLU', 0.8459822645624723, (186.22899999999998, 212.924, 257.78099999999995)), ('D', 66, u'GLY', 0.8410483034118609, (198.26999999999998, 204.9, 257.65200000000004)), ('D', 97, u'LEU', 0.8147969885059132, (217.012, 192.79899999999998, 253.47899999999998)), ('D', 110, u'GLU', 0.8060520123751568, (203.068, 192.517, 274.835)), ('D', 121, u'ASN', 0.8385798082253522, (201.903, 209.606, 274.7)), ('D', 148, u'LEU', 0.8267035571824157, (206.62800000000001, 232.111, 277.101)), ('D', 149, u'ASN', 0.8191909332134971, (208.48200000000003, 232.248, 273.772)), ('D', 150, u'GLU', 0.8192705704336269, (207.759, 235.945, 273.244)), ('D', 155, u'SER', 0.8290814002490059, (211.65200000000002, 241.037, 277.085)), ('D', 163, u'TRP', 0.8418704816103949, (210.383, 234.142, 285.953)), ('D', 176, u'LEU', 0.8349802928297263, (208.466, 214.632, 283.34200000000004)), ('D', 196, u'TYR', 0.8624153581510204, (222.915, 196.35000000000002, 270.335)), ('D', 198, u'ASP', 0.8428570316249941, (222.24899999999997, 200.29299999999998, 274.565)), ('D', 199, u'TYR', 0.8634451076503293, (219.725, 202.64899999999997, 273.003)), ('D', 213, u'ASP', 0.8353013909748608, (236.77499999999998, 196.963, 252.476)), ('D', 216, u'ASP', 0.8327847541307035, (234.155, 200.58200000000002, 256.9959999999999)), ('D', 232, u'GLU', 0.8370522433373002, (239.343, 221.945, 266.641)), ('D', 233, u'ILE', 0.8298360966844176, (236.55800000000002, 224.577, 266.555)), ('D', 248, u'LEU', 0.7774153167743731, (226.098, 241.80700000000002, 277.05400000000003)), ('D', 251, u'ALA', 0.7923884566133632, (222.806, 245.907, 278.694)), ('D', 262, u'LEU', 0.8099359146009177, (226.72299999999998, 233.824, 280.825)), ('D', 263, u'PRO', 0.8411051293733469, (223.64299999999997, 233.041, 282.92499999999995)), ('D', 292, u'ASP', 0.8322420523451313, (216.899, 243.61899999999997, 252.726)), ('D', 293, u'VAL', 0.8601229250205011, (215.271, 243.323, 249.304)), ('D', 294, u'THR', 0.8316240806521051, (211.617, 243.055, 250.369)), ('D', 308, u'PHE', 0.8390142288356767, (209.547, 229.67, 242.374)), ('D', 316, u'VAL', 0.8145541198770926, (218.178, 224.909, 235.32500000000002)), ('D', 321, u'PRO', 0.80432128881709, (216.684, 218.95800000000003, 234.929)), ('D', 333, u'LEU', 0.8281030428063898, (201.895, 227.389, 246.66899999999998)), ('D', 341, u'LYS', 0.8379453396844654, (192.221, 226.192, 256.27)), ('D', 360, u'MET', 0.8287594305407916, (204.22299999999998, 226.63299999999998, 251.42100000000002)), ('D', 379, u'ILE', 0.8399973392782402, (212.7, 218.433, 245.55700000000002)), ('D', 399, u'GLY', 0.8457862826288914, (222.70299999999997, 214.317, 257.539)), ('D', 404, u'VAL', 0.8372935154894977, (221.834, 219.796, 250.086)), ('D', 422, u'GLY', 0.8079996438555703, (216.436, 242.30800000000002, 238.30100000000002)), ('D', 453, u'THR', 0.8364795654588466, (224.161, 219.917, 270.182)), ('D', 470, u'LYS', 0.8536609971266448, (220.077, 208.01299999999998, 288.67)), ('D', 475, u'LYS', 0.8533406512242235, (224.298, 217.51399999999998, 289.131)), ('D', 476, u'LYS', 0.8520394532221831, (226.21499999999997, 216.469, 286.02099999999996)), ('D', 494, u'ASP', 0.8558277797511504, (218.566, 219.738, 292.98299999999995)), ('D', 511, u'SER', 0.8278816943339518, (217.895, 212.035, 267.48599999999993)), ('D', 525, u'PHE', 0.8007938396967315, (230.003, 220.617, 250.008)), ('D', 529, u'LEU', 0.8440508563400655, (231.66, 223.017, 244.57299999999998)), ('D', 536, u'GLU', 0.846998493796861, (238.725, 233.146, 243.107)), ('D', 556, u'ASN', 0.8008893909863335, (227.031, 212.42100000000002, 240.4)), ('D', 558, u'LEU', 0.8252890348196972, (222.61399999999998, 212.929, 244.27899999999997)), ('D', 562, u'LYS', 0.8193649219678582, (221.281, 205.129, 249.73899999999998)), ('D', 568, u'LEU', 0.8299570754511915, (231.79899999999998, 206.694, 249.05800000000002)), ('D', 569, u'ALA', 0.8012532127179248, (228.975, 209.172, 248.469)), ('D', 570, u'LEU', 0.8346196879695986, (231.033, 211.806, 250.284)), ('D', 571, u'GLU', 0.8328254141213475, (234.19, 210.966, 248.324)), ('D', 584, u'LEU', 0.8433849943182817, (233.88400000000001, 225.696, 258.22099999999995)), ('D', 591, u'LEU', 0.8298450087510115, (235.304, 237.186, 261.294)), ('D', 603, u'PHE', 0.814169541579558, (239.036, 238.485, 278.59)), ('D', 608, u'THR', 0.8180688913399488, (233.399, 227.57299999999998, 286.452)), ('D', 609, u'ASP', 0.8159914743542257, (233.27399999999997, 229.02, 289.98299999999995)), ('D', 613, u'TYR', 0.8480194040488257, (223.24299999999997, 232.894, 293.254)), ('D', 705, u'NAG', 0.7981710755696958, (239.566, 249.54399999999998, 253.683)), ('D', 706, u'ZN', 0.826148384932021, (214.655, 221.51, 254.756)), ('A', 15, u'CYS', 0.7279459267182157, (192.231, 237.066, 153.833)), ('A', 16, u'VAL', 0.7547989462056941, (194.303, 237.148, 150.638)), ('A', 17, u'ASN', 0.7552576500286531, (196.154, 234.195, 149.11299999999997)), ('A', 20, u'THR', 0.7948345311054448, (203.972, 234.954, 142.64499999999998)), ('A', 34, u'ARG', 0.8543872684247985, (222.136, 224.13299999999998, 170.194)), ('A', 47, u'VAL', 0.801912797458464, (229.312, 221.469, 189.201)), ('A', 61, u'ASN', 0.8397497926084773, (218.953, 217.515, 161.38500000000002)), ('A', 81, u'ASN', 0.8152098128628172, (205.248, 229.71899999999997, 155.94899999999998)), ('A', 82, u'PRO', 0.8120876002566091, (204.23499999999999, 226.036, 155.98700000000002)), ('A', 88, u'ASP', 0.8388025557838561, (206.842, 216.983, 171.68)), ('A', 89, u'GLY', 0.8516289387383381, (208.017, 220.593, 171.671)), ('A', 110, u'LEU', 0.7897187573147199, (193.172, 226.01899999999998, 163.19)), ('A', 120, u'VAL', 0.8307462219519789, (201.842, 237.89700000000002, 167.835)), ('A', 121, u'ASN', 0.8068970193976772, (204.05100000000002, 240.974, 167.98000000000002)), ('A', 137, u'ASN', 0.7704659644944878, (194.904, 230.129, 154.842)), ('A', 144, u'TYR', 0.7930009836722712, (204.291, 249.689, 153.976)), ('A', 155, u'SER', 0.7719750865260551, (199.267, 248.71399999999997, 157.517)), ('A', 162, u'SER', 0.8063251314065198, (186.786, 235.71899999999997, 163.57899999999998)), ('A', 169, u'GLU', 0.8235321659129496, (194.21599999999998, 236.876, 176.97)), ('A', 173, u'GLN', 0.8413060810096669, (202.686, 247.436, 177.48100000000002)), ('A', 177, u'MET', 0.797560377469363, (209.46800000000002, 249.02, 167.031)), ('A', 181, u'GLY', 0.7890079871949613, (214.532, 247.67299999999997, 156.23)), ('A', 191, u'GLU', 0.8336141908527802, (216.262, 231.167, 170.035)), ('A', 209, u'PRO', 0.8260923806132059, (224.405, 239.162, 168.584)), ('A', 214, u'ARG', 0.788823200695784, (223.6, 231.893, 156.24399999999997)), ('A', 220, u'PHE', 0.7991227941991579, (226.752, 227.28, 173.08100000000002)), ('A', 234, u'ASN', 0.8021130350194976, (195.756, 220.24499999999998, 172.57299999999998)), ('A', 251, u'PRO', 0.7631177947793124, (203.437, 246.98000000000002, 141.672)), ('A', 260, u'ALA', 0.8111534493794615, (209.74099999999999, 239.91899999999998, 151.05800000000002)), ('A', 261, u'GLY', 0.7757808513529086, (212.727, 241.167, 153.063)), ('A', 270, u'LEU', 0.8554834884573438, (212.797, 217.74099999999999, 171.097)), ('A', 318, u'PHE', 0.6900275608566763, (222.092, 198.82200000000003, 171.993)), ('A', 321, u'GLN', 0.7021268536369595, (216.653, 205.789, 174.222)), ('A', 322, u'PRO', 0.718622028406897, (213.91299999999998, 206.607, 176.82800000000003)), ('A', 324, u'GLU', 0.8487490751670383, (207.65, 205.737, 178.026)), ('A', 336, u'CYS', 0.7949706734943647, (192.251, 199.40200000000002, 205.13)), ('A', 341, u'VAL', 0.8392564643079935, (192.889, 199.31, 215.26899999999998)), ('A', 365, u'TYR', 0.8647463430108046, (200.282, 205.712, 205.57399999999998)), ('A', 379, u'CYS', 0.8362800367525944, (210.23999999999998, 202.02700000000002, 211.792)), ('A', 386, u'LYS', 0.8815458834939777, (208.99200000000002, 204.401, 200.92000000000002)), ('A', 387, u'LEU', 0.8416763289800533, (206.317, 202.271, 202.625)), ('A', 391, u'CYS', 0.8002107682126707, (203.712, 195.702, 198.07399999999998)), ('A', 399, u'SER', 0.8063951809108368, (197.61299999999997, 196.594, 220.08)), ('A', 406, u'GLU', 0.7912625270214056, (208.61299999999997, 200.572, 229.437)), ('A', 407, u'VAL', 0.8148501989316177, (207.864, 201.73899999999998, 225.879)), ('A', 410, u'ILE', 0.786252500628792, (209.29, 197.563, 222.624)), ('A', 422, u'ASN', 0.7787856554465453, (205.195, 189.636, 227.94899999999998)), ('A', 428, u'ASP', 0.8486864709569887, (214.914, 191.224, 211.83)), ('A', 432, u'CYS', 0.8321696006376841, (206.612, 200.17399999999998, 212.676)), ('A', 442, u'ASP', 0.8495983023938694, (192.004, 205.008, 230.725)), ('A', 471, u'GLU', 0.8115470845919219, (200.55200000000002, 178.647, 236.58)), ('A', 475, u'ALA', 0.8353596545971987, (210.036, 180.077, 243.138)), ('A', 476, u'GLY', 0.8244119400381069, (212.001, 177.738, 245.412)), ('A', 484, u'GLU', 0.8270381950752507, (200.033, 180.375, 246.98100000000002)), ('A', 495, u'TYR', 0.8209083493791661, (199.059, 197.915, 236.785)), ('A', 511, u'VAL', 0.8027130095907189, (200.24299999999997, 199.57399999999998, 218.171)), ('A', 525, u'CYS', 0.7555393112526947, (199.676, 197.353, 197.731)), ('A', 529, u'LYS', 0.8500629035551185, (197.48100000000002, 204.697, 190.20999999999998)), ('A', 544, u'ASN', 0.8418923239292686, (204.33100000000002, 195.583, 192.547)), ('A', 555, u'SER', 0.8079422466017867, (205.07, 185.10999999999999, 176.85100000000003)), ('A', 556, u'ASN', 0.7539957024965521, (203.271, 181.911, 175.71899999999997)), ('A', 564, u'GLN', 0.7655092238268373, (204.82100000000003, 185.46800000000002, 190.766)), ('A', 565, u'PHE', 0.7512565534460707, (208.365, 186.117, 189.47299999999998)), ('A', 566, u'GLY', 0.7714754014610221, (210.946, 184.13899999999998, 187.529)), ('A', 567, u'ARG', 0.7946659215094791, (214.685, 184.51899999999998, 188.018)), ('A', 568, u'ASP', 0.804562872769182, (217.70499999999998, 183.40800000000002, 186.008)), ('A', 573, u'THR', 0.862751293139158, (213.9, 189.008, 187.067)), ('A', 593, u'GLY', 0.6858338308801953, (224.725, 192.972, 172.63899999999998)), ('A', 600, u'PRO', 0.7093559268619954, (243.54899999999998, 207.37, 172.98100000000002)), ('A', 603, u'ASN', 0.7922759771552332, (243.172, 215.303, 175.147)), ('A', 608, u'VAL', 0.734311108039999, (237.49800000000002, 206.137, 168.90200000000002)), ('A', 615, u'VAL', 0.662005020644768, (229.11499999999998, 190.009, 166.869)), ('A', 616, u'ASN', 0.7205816474863086, (230.91299999999998, 187.939, 164.196)), ('A', 636, u'TYR', 0.6920238496257066, (225.901, 201.26899999999998, 165.759)), ('A', 672, u'ALA', 0.6781357815200354, (245.58200000000002, 198.706, 170.288))]
data['rota'] = [('D', ' 432 ', 'ASN', 0.005899353167494171, (234.0120000000001, 245.17500000000004, 254.294)), ('D', ' 474 ', 'MET', 0.08509017420338094, (220.95500000000004, 217.219, 287.341)), ('D', ' 540 ', 'HIS', 0.1324645458437242, (231.50600000000009, 233.9, 251.89700000000002)), ('A', ' 312 ', 'ILE', 0.02288599756454586, (239.131, 200.66699999999997, 177.024)), ('A', ' 316 ', 'SER', 0.2723924692481467, (226.007, 199.578, 177.479)), ('A', ' 318 ', 'PHE', 0.20211930985675744, (222.092, 198.82200000000006, 171.99300000000002)), ('A', ' 336 ', 'CYS', 0.09684643591754138, (192.251, 199.402, 205.13)), ('A', ' 358 ', 'ILE', 0.0, (194.61599999999996, 193.265, 207.328)), ('A', ' 546 ', 'LEU', 0.03226345021783, (209.804, 196.16500000000005, 191.536)), ('A', ' 563 ', 'GLN', 0.2945702272003233, (204.663, 181.95, 192.20200000000003)), ('A', ' 590 ', 'CYS', 0.2170814483163106, (216.646, 197.338, 175.364)), ('A', ' 591 ', 'SER', 0.037591847763292954, (218.618, 194.985, 173.02900000000005)), ('A', ' 592 ', 'PHE', 0.02665699333233947, (221.09699999999998, 192.05900000000003, 173.485))]
data['clusters'] = [('D', '375', 1, 'Dihedral angle:CB:CG:CD:OE1', (212.559, 223.445, 249.48200000000003)), ('D', '379', 1, 'smoc Outlier', (212.7, 218.433, 245.55700000000002)), ('D', '398', 1, 'side-chain clash\nDihedral angle:CB:CG:CD:OE1', (220.48200000000003, 211.251, 257.86)), ('D', '399', 1, 'smoc Outlier', (222.70299999999997, 214.317, 257.539)), ('D', '402', 1, 'side-chain clash\nDihedral angle:CB:CG:CD:OE1', (219.563, 219.194, 254.86800000000002)), ('D', '403', 1, 'side-chain clash', (224.307, 222.221, 251.471)), ('D', '404', 1, 'smoc Outlier', (221.834, 219.796, 250.086)), ('D', '406', 1, 'Dihedral angle:CB:CG:CD:OE1', (221.086, 224.48200000000003, 252.71599999999998)), ('D', '407', 1, 'side-chain clash', (224.307, 222.221, 251.471)), ('D', '457', 1, 'side-chain clash', (223.948, 213.159, 268.198)), ('D', '511', 1, 'smoc Outlier', (217.895, 212.035, 267.48599999999993)), ('D', '513', 1, 'side-chain clash', (223.948, 213.159, 268.198)), ('D', '514', 1, 'side-chain clash', (220.996, 212.428, 261.253)), ('D', '518', 1, 'side-chain clash\nDihedral angle:CD:NE:CZ:NH1', (224.524, 218.83, 258.893)), ('D', '524', 1, 'side-chain clash', (235.059, 220.838, 254.399)), ('D', '525', 1, 'smoc Outlier', (230.003, 220.617, 250.008)), ('D', '529', 1, 'side-chain clash\nsmoc Outlier', (226.679, 220.877, 244.625)), ('D', '554', 1, 'side-chain clash', (226.679, 220.877, 244.625)), ('D', '583', 1, 'side-chain clash', (235.059, 220.838, 254.399)), ('D', '584', 1, 'smoc Outlier', (233.88400000000001, 225.696, 258.22099999999995)), ('D', '706', 1, 'smoc Outlier', (214.655, 221.51, 254.756)), ('D', '245', 2, 'Dihedral angle:CD:NE:CZ:NH1', (229.618, 238.47299999999998, 277.032)), ('D', '247', 2, 'side-chain clash', (227.64, 242.0, 272.387)), ('D', '248', 2, 'smoc Outlier', (226.098, 241.80700000000002, 277.05400000000003)), ('D', '251', 2, 'smoc Outlier', (222.806, 245.907, 278.694)), ('D', '252', 2, 'Dihedral angle:CA:C', (222.33, 244.131, 282.04400000000004)), ('D', '253', 2, 'Dihedral angle:N:CA', (224.593, 246.414, 284.069)), ('D', '261', 2, 'side-chain clash', (228.583, 230.362, 283.424)), ('D', '262', 2, 'smoc Outlier', (226.72299999999998, 233.824, 280.825)), ('D', '263', 2, 'smoc Outlier', (223.64299999999997, 233.041, 282.92499999999995)), ('D', '282', 2, 'side-chain clash', (227.64, 242.0, 272.387)), ('D', '488', 2, 'side-chain clash', (228.583, 230.362, 283.424)), ('D', '608', 2, 'smoc Outlier', (233.399, 227.57299999999998, 286.452)), ('D', '609', 2, 'smoc Outlier', (233.27399999999997, 229.02, 289.98299999999995)), ('D', '291', 3, 'side-chain clash', (219.675, 241.497, 251.734)), ('D', '292', 3, 'smoc Outlier', (216.899, 243.61899999999997, 252.726)), ('D', '293', 3, 'smoc Outlier', (215.271, 243.323, 249.304)), ('D', '294', 3, 'smoc Outlier', (211.617, 243.055, 250.369)), ('D', '422', 3, 'smoc Outlier', (216.436, 242.30800000000002, 238.30100000000002)), ('D', '423', 3, 'cablam CA Geom Outlier', (216.2, 243.4, 241.9)), ('D', '424', 3, 'cablam Outlier', (219.1, 244.8, 244.0)), ('D', '425', 3, 'Dihedral angle:CA:C', (219.71899999999997, 248.02800000000002, 242.016)), ('D', '426', 3, 'Dihedral angle:N:CA', (222.823, 247.665, 239.871)), ('D', '427', 3, 'cablam Outlier', (225.6, 249.8, 241.3)), ('D', '428', 3, 'cablam Outlier', (225.6, 248.8, 245.0)), ('D', '474', 4, 'Rotamer', (220.95500000000004, 217.219, 287.341)), ('D', '475', 4, 'smoc Outlier', (224.298, 217.51399999999998, 289.131)), ('D', '476', 4, 'side-chain clash\nsmoc Outlier', (227.445, 217.495, 282.846)), ('D', '479', 4, 'Dihedral angle:CB:CG:CD:OE1', (228.82800000000003, 220.571, 285.069)), ('D', '480', 4, 'side-chain clash', (227.445, 217.495, 282.846)), ('D', '483', 4, 'Dihedral angle:CB:CG:CD:OE1', (232.804, 223.189, 280.82599999999996)), ('D', '494', 4, 'smoc Outlier', (218.566, 219.738, 292.98299999999995)), ('D', '144', 5, 'cablam Outlier', (204.4, 228.0, 275.4)), ('D', '148', 5, 'smoc Outlier', (206.62800000000001, 232.111, 277.101)), ('D', '149', 5, 'smoc Outlier', (208.48200000000003, 232.248, 273.772)), ('D', '150', 5, 'smoc Outlier', (207.759, 235.945, 273.244)), ('D', '269', 5, 'backbone clash', (214.863, 230.281, 273.516)), ('D', '270', 5, 'backbone clash', (214.863, 230.281, 273.516)), ('D', '273', 5, 'Dihedral angle:CD:NE:CZ:NH1', (219.875, 226.996, 271.618)), ('D', '224', 6, 'cablam Outlier', (235.5, 209.8, 268.0)), ('D', '225', 6, 'Dihedral angle:CA:CB:CG:OD1\ncablam Outlier', (235.731, 212.38600000000002, 265.249)), ('D', '227', 6, 'Dihedral angle:CB:CG:CD:OE1', (235.505, 214.989, 269.64400000000006)), ('D', '230', 6, 'side-chain clash', (234.643, 221.443, 267.588)), ('D', '232', 6, 'Dihedral angle:CB:CG:CD:OE1\nsmoc Outlier', (239.343, 221.945, 266.641)), ('D', '233', 6, 'side-chain clash\nsmoc Outlier', (234.643, 221.443, 267.588)), ('D', '215', 7, 'side-chain clash', (233.722, 204.443, 247.443)), ('D', '568', 7, 'side-chain clash\nsmoc Outlier', (233.722, 204.443, 247.443)), ('D', '569', 7, 'smoc Outlier', (228.975, 209.172, 248.469)), ('D', '570', 7, 'smoc Outlier', (231.033, 211.806, 250.284)), ('D', '571', 7, 'smoc Outlier', (234.19, 210.966, 248.324)), ('D', '315', 8, 'side-chain clash', (220.524, 224.71, 239.195)), ('D', '316', 8, 'smoc Outlier', (218.178, 224.909, 235.32500000000002)), ('D', '318', 8, 'side-chain clash', (220.524, 224.71, 239.195)), ('D', '320', 8, 'side-chain clash', (218.794, 218.368, 237.487)), ('D', '321', 8, 'side-chain clash\nsmoc Outlier', (218.794, 218.368, 237.487)), ('D', '209', 9, 'side-chain clash', (230.021, 201.907, 253.401)), ('D', '213', 9, 'smoc Outlier', (236.77499999999998, 196.963, 252.476)), ('D', '216', 9, 'smoc Outlier', (234.155, 200.58200000000002, 256.9959999999999)), ('D', '565', 9, 'side-chain clash', (230.021, 201.907, 253.401)), ('D', '308', 10, 'side-chain clash\nsmoc Outlier', (206.294, 227.712, 246.239)), ('D', '333', 10, 'side-chain clash\nsmoc Outlier', (206.294, 227.712, 246.239)), ('D', '334', 10, 'cablam Outlier', (199.6, 230.0, 248.3)), ('D', '360', 10, 'smoc Outlier', (204.22299999999998, 226.63299999999998, 251.42100000000002)), ('D', '189', 11, 'Dihedral angle:CB:CG:CD:OE1', (216.012, 196.71599999999998, 277.178)), ('D', '192', 11, 'Dihedral angle:CD:NE:CZ:NH1', (219.598, 195.256, 274.184)), ('D', '196', 11, 'smoc Outlier', (222.915, 196.35000000000002, 270.335)), ('D', '198', 11, 'smoc Outlier', (222.24899999999997, 200.29299999999998, 274.565)), ('D', '336', 12, 'backbone clash', (192.607, 227.251, 253.002)), ('D', '340', 12, 'backbone clash', (192.607, 227.251, 253.002)), ('D', '341', 12, 'smoc Outlier', (192.221, 226.192, 256.27)), ('D', '176', 13, 'smoc Outlier', (208.466, 214.632, 283.34200000000004)), ('D', '177', 13, 'side-chain clash\nDihedral angle:CD:NE:CZ:NH1', (210.984, 213.47299999999998, 285.95799999999997)), ('D', '178', 13, 'side-chain clash', (209.895, 213.832, 287.803)), ('D', '110', 14, 'smoc Outlier', (203.068, 192.517, 274.835)), ('D', '111', 14, 'Dihedral angle:CA:CB:CG:OD1', (202.54299999999998, 193.9, 278.339)), ('D', '115', 14, 'Dihedral angle:CD:NE:CZ:NH1', (203.21699999999998, 200.772, 278.90999999999997)), ('D', '32', 15, 'side-chain clash', (206.773, 193.341, 251.378)), ('D', '35', 15, 'smoc Outlier', (202.843, 196.092, 246.36200000000002)), ('D', '76', 15, 'side-chain clash', (206.773, 193.341, 251.378)), ('D', '168', 16, 'side-chain clash', (211.356, 222.94, 278.595)), ('D', '169', 16, 'Dihedral angle:CD:NE:CZ:NH1', (211.90200000000002, 224.555, 284.242)), ('D', '502', 16, 'side-chain clash', (211.356, 222.94, 278.595)), ('D', '204', 17, 'backbone clash', (228.478, 204.613, 268.124)), ('D', '219', 17, 'backbone clash', (228.478, 204.613, 268.124)), ('D', '453', 18, 'smoc Outlier', (224.161, 219.917, 270.182)), ('D', '455', 18, 'side-chain clash', (225.33, 220.811, 275.294)), ('D', '439', 19, 'side-chain clash', (228.746, 235.928, 257.913)), ('D', '540', 19, 'Rotamer', (231.50600000000009, 233.9, 251.89700000000002)), ('D', '284', 20, 'side-chain clash', (232.103, 243.565, 265.143)), ('D', '594', 20, 'side-chain clash', (232.103, 243.565, 265.143)), ('D', '56', 21, 'Dihedral angle:CB:CG:CD:OE1', (186.373, 216.44899999999998, 259.239)), ('D', '57', 21, 'cablam Outlier\nsmoc Outlier', (186.2, 212.9, 257.8)), ('D', '589', 22, 'Dihedral angle:CB:CG:CD:OE1', (238.38700000000003, 233.495, 258.72499999999997)), ('D', '591', 22, 'smoc Outlier', (235.304, 237.186, 261.294)), ('D', '187', 23, 'side-chain clash', (215.569, 203.937, 273.782)), ('D', '199', 23, 'side-chain clash\nsmoc Outlier', (215.569, 203.937, 273.782)), ('D', '66', 24, 'smoc Outlier', (198.26999999999998, 204.9, 257.65200000000004)), ('D', '67', 24, 'Dihedral angle:CA:CB:CG:OD1', (196.96200000000002, 201.685, 259.207)), ('D', '391', 25, 'side-chain clash', (215.396, 198.199, 249.602)), ('D', '96', 25, 'side-chain clash', (215.396, 198.199, 249.602)), ('D', '85', 26, 'side-chain clash', (224.719, 188.034, 254.222)), ('D', '94', 26, 'side-chain clash', (224.719, 188.034, 254.222)), ('D', '160', 27, 'Dihedral angle:CB:CG:CD:OE1', (210.811, 238.989, 283.861)), ('D', '163', 27, 'smoc Outlier', (210.383, 234.142, 285.953)), ('D', '93', 28, 'side-chain clash', (218.702, 190.382, 249.899)), ('D', '97', 28, 'side-chain clash\nsmoc Outlier', (218.702, 190.382, 249.899)), ('D', '556', 29, 'smoc Outlier', (227.031, 212.42100000000002, 240.4)), ('D', '558', 29, 'smoc Outlier', (222.61399999999998, 212.929, 244.27899999999997)), ('D', '602', 30, 'cablam Outlier', (238.5, 242.0, 277.3)), ('D', '603', 30, 'smoc Outlier', (239.036, 238.485, 278.59)), ('D', '42', 31, 'smoc Outlier', (197.83800000000002, 205.55, 248.467)), ('D', '46', 31, 'smoc Outlier', (195.507, 210.597, 251.83700000000002)), ('D', '482', 32, 'side-chain clash', (225.045, 226.207, 288.22)), ('D', '489', 32, 'side-chain clash', (225.045, 226.207, 288.22)), ('A', '292', 1, 'side-chain clash', (220.304, 207.798, 174.588)), ('A', '315', 1, 'cablam Outlier', (229.5, 201.1, 177.9)), ('A', '316', 1, 'Rotamer\ncablam CA Geom Outlier', (226.007, 199.578, 177.479)), ('A', '317', 1, 'cablam CA Geom Outlier', (223.7, 197.4, 175.2)), ('A', '318', 1, 'Rotamer\nsmoc Outlier', (222.092, 198.82200000000006, 171.99300000000002)), ('A', '319', 1, 'side-chain clash', (219.59, 201.366, 174.311)), ('A', '320', 1, 'side-chain clash', (214.616, 203.244, 171.884)), ('A', '321', 1, 'side-chain clash\nRamachandran\ncablam Outlier\nsmoc Outlier', (216.653, 205.789, 174.222)), ('A', '322', 1, 'smoc Outlier', (213.91299999999998, 206.607, 176.82800000000003)), ('A', '324', 1, 'Dihedral angle:CB:CG:CD:OE1\nsmoc Outlier', (207.65, 205.737, 178.026)), ('A', '589', 1, 'backbone clash', (216.764, 195.458, 174.566)), ('A', '590', 1, 'Rotamer\nbackbone clash\ncablam CA Geom Outlier', (216.764, 195.458, 174.566)), ('A', '591', 1, 'Rotamer', (218.618, 194.985, 173.02900000000005)), ('A', '592', 1, 'Rotamer\nside-chain clash\ncablam Outlier', (220.925, 192.994, 171.271)), ('A', '593', 1, 'smoc Outlier', (224.725, 192.972, 172.63899999999998)), ('A', '594', 1, 'side-chain clash', (230.157, 194.407, 171.57)), ('A', '612', 1, 'side-chain clash', (230.157, 194.407, 171.57)), ('A', '615', 1, 'smoc Outlier', (229.11499999999998, 190.009, 166.869)), ('A', '616', 1, 'smoc Outlier', (230.91299999999998, 187.939, 164.196)), ('A', '634', 1, 'side-chain clash', (220.925, 192.994, 171.271)), ('A', '329', 2, 'side-chain clash', (203.311, 202.74, 192.352)), ('A', '362', 2, 'side-chain clash', (197.402, 200.65, 197.372)), ('A', '364', 2, 'Dihedral angle:CA:CB:CG:OD1', (197.584, 205.018, 202.98800000000003)), ('A', '365', 2, 'smoc Outlier', (200.282, 205.712, 205.57399999999998)), ('A', '382', 2, 'side-chain clash', (207.725, 200.683, 204.947)), ('A', '386', 2, 'smoc Outlier', (208.99200000000002, 204.401, 200.92000000000002)), ('A', '387', 2, 'side-chain clash\nsmoc Outlier', (207.725, 200.683, 204.947)), ('A', '389', 2, 'cablam Outlier', (204.2, 202.8, 197.8)), ('A', '391', 2, 'smoc Outlier', (203.712, 195.702, 198.07399999999998)), ('A', '525', 2, 'smoc Outlier', (199.676, 197.353, 197.731)), ('A', '526', 2, 'side-chain clash\ncablam CA Geom Outlier', (197.402, 200.65, 197.372)), ('A', '527', 2, 'cablam CA Geom Outlier', (198.1, 203.6, 197.0)), ('A', '528', 2, 'side-chain clash\ncablam Outlier', (203.311, 202.74, 192.352)), ('A', '529', 2, 'smoc Outlier', (197.48100000000002, 204.697, 190.20999999999998)), ('A', '544', 2, 'smoc Outlier', (204.33100000000002, 195.583, 192.547)), ('A', '546', 2, 'Rotamer\nside-chain clash', (207.778, 192.118, 190.026)), ('A', '565', 2, 'side-chain clash\nsmoc Outlier', (207.778, 192.118, 190.026)), ('A', '100', 3, 'side-chain clash', (211.356, 242.891, 156.009)), ('A', '177', 3, 'smoc Outlier', (209.46800000000002, 249.02, 167.031)), ('A', '178', 3, 'cablam Outlier', (211.9, 250.0, 164.3)), ('A', '179', 3, 'cablam Outlier', (210.4, 248.3, 161.2)), ('A', '181', 3, 'smoc Outlier', (214.532, 247.67299999999997, 156.23)), ('A', '245', 3, 'side-chain clash', (211.356, 242.891, 156.009)), ('A', '260', 3, 'cablam Outlier\nsmoc Outlier', (209.7, 239.9, 151.1)), ('A', '261', 3, 'smoc Outlier', (212.727, 241.167, 153.063)), ('A', '262', 3, 'side-chain clash', (214.63, 237.033, 152.829)), ('A', '67', 3, 'side-chain clash', (214.63, 237.033, 152.829)), ('A', '405', 4, 'Dihedral angle:CA:CB:CG:OD1', (208.66, 204.07399999999998, 230.96)), ('A', '406', 4, 'Dihedral angle:CB:CG:CD:OE1\nsmoc Outlier', (208.61299999999997, 200.572, 229.437)), ('A', '407', 4, 'smoc Outlier', (207.864, 201.73899999999998, 225.879)), ('A', '409', 4, 'side-chain clash', (209.419, 195.903, 229.114)), ('A', '410', 4, 'smoc Outlier', (209.29, 197.563, 222.624)), ('A', '418', 4, 'side-chain clash', (209.419, 195.903, 229.114)), ('A', '422', 4, 'side-chain clash\nsmoc Outlier', (205.299, 192.813, 230.711)), ('A', '559', 5, 'side-chain clash', (206.07, 183.799, 183.877)), ('A', '566', 5, 'smoc Outlier', (210.946, 184.13899999999998, 187.529)), ('A', '567', 5, 'smoc Outlier', (214.685, 184.51899999999998, 188.018)), ('A', '568', 5, 'smoc Outlier', (217.70499999999998, 183.40800000000002, 186.008)), ('A', '573', 5, 'smoc Outlier', (213.9, 189.008, 187.067)), ('A', '574', 5, 'Dihedral angle:CA:CB:CG:OD1', (213.35000000000002, 187.73299999999998, 183.463)), ('A', '584', 5, 'side-chain clash', (206.07, 183.799, 183.877)), ('A', '636', 6, 'smoc Outlier', (225.901, 201.26899999999998, 165.759)), ('A', '638', 6, 'cablam Outlier', (229.7, 200.1, 160.0)), ('A', '640', 6, 'cablam CA Geom Outlier', (235.2, 200.8, 157.5)), ('A', '641', 6, 'backbone clash', (240.075, 199.147, 160.89)), ('A', '642', 6, 'side-chain clash', (233.347, 197.26, 161.85)), ('A', '651', 6, 'side-chain clash', (233.347, 197.26, 161.85)), ('A', '653', 6, 'backbone clash', (240.075, 199.147, 160.89)), ('A', '105', 7, 'side-chain clash', (198.616, 229.514, 160.864)), ('A', '108', 7, 'side-chain clash\ncablam Outlier', (192.368, 219.905, 164.772)), ('A', '109', 7, 'side-chain clash', (192.368, 219.905, 164.772)), ('A', '110', 7, 'smoc Outlier', (193.172, 226.01899999999998, 163.19)), ('A', '112', 7, 'cablam Outlier', (187.3, 227.7, 164.7)), ('A', '239', 7, 'side-chain clash', (198.616, 229.514, 160.864)), ('A', '336', 8, 'Rotamer\nsmoc Outlier', (192.251, 199.402, 205.13)), ('A', '341', 8, 'side-chain clash\nsmoc Outlier', (193.099, 197.053, 212.101)), ('A', '356', 8, 'side-chain clash', (193.099, 197.053, 212.101)), ('A', '357', 8, 'Dihedral angle:CD:NE:CZ:NH1', (195.526, 190.685, 209.995)), ('A', '358', 8, 'Rotamer', (194.61599999999996, 193.265, 207.328)), ('A', '21', 9, 'backbone clash', (205.064, 232.018, 151.374)), ('A', '79', 9, 'backbone clash', (205.064, 232.018, 151.374)), ('A', '81', 9, 'smoc Outlier', (205.248, 229.71899999999997, 155.94899999999998)), ('A', '82', 9, 'smoc Outlier', (204.23499999999999, 226.036, 155.98700000000002)), ('A', '29', 10, 'side-chain clash\nbackbone clash', (222.367, 222.406, 159.63)), ('A', '30', 10, 'backbone clash', (222.367, 222.406, 159.63)), ('A', '61', 10, 'smoc Outlier', (218.953, 217.515, 161.38500000000002)), ('A', '62', 10, 'side-chain clash', (219.252, 223.41, 160.16)), ('A', '220', 11, 'smoc Outlier', (226.752, 227.28, 173.08100000000002)), ('A', '33', 11, 'side-chain clash', (224.163, 219.946, 171.164)), ('A', '34', 11, 'smoc Outlier', (222.136, 224.13299999999998, 170.194)), ('A', '58', 11, 'side-chain clash', (224.163, 219.946, 171.164)), ('A', '379', 12, 'smoc Outlier', (210.23999999999998, 202.02700000000002, 211.792)), ('A', '431', 12, 'backbone clash', (206.088, 196.453, 211.844)), ('A', '432', 12, 'smoc Outlier', (206.612, 200.17399999999998, 212.676)), ('A', '513', 12, 'backbone clash', (206.088, 196.453, 211.844)), ('A', '185', 13, 'backbone clash\ncablam CA Geom Outlier', (224.912, 238.287, 157.679)), ('A', '212', 13, 'backbone clash', (224.912, 238.287, 157.679)), ('A', '214', 13, 'cablam CA Geom Outlier\nsmoc Outlier', (223.6, 231.9, 156.2)), ('A', '102', 14, 'backbone clash', (204.833, 241.64, 165.044)), ('A', '120', 14, 'smoc Outlier', (201.842, 237.89700000000002, 167.835)), ('A', '121', 14, 'backbone clash\nsmoc Outlier', (204.833, 241.64, 165.044)), ('A', '270', 15, 'smoc Outlier', (212.797, 217.74099999999999, 171.097)), ('A', '88', 15, 'cablam Outlier\nsmoc Outlier', (206.8, 217.0, 171.7)), ('A', '89', 15, 'smoc Outlier', (208.017, 220.593, 171.671)), ('A', '554', 16, 'Dihedral angle:CB:CG:CD:OE1', (204.191, 188.599, 175.506)), ('A', '555', 16, 'smoc Outlier', (205.07, 185.10999999999999, 176.85100000000003)), ('A', '556', 16, 'smoc Outlier', (203.271, 181.911, 175.71899999999997)), ('A', '191', 17, 'smoc Outlier', (216.262, 231.167, 170.035)), ('A', '206', 17, 'side-chain clash', (218.577, 231.525, 174.305)), ('A', '223', 17, 'side-chain clash', (218.577, 231.525, 174.305)), ('A', '15', 18, 'smoc Outlier', (192.231, 237.066, 153.833)), ('A', '16', 18, 'smoc Outlier', (194.303, 237.148, 150.638)), ('A', '17', 18, 'smoc Outlier', (196.154, 234.195, 149.11299999999997)), ('A', '484', 19, 'cablam CA Geom Outlier\nsmoc Outlier', (200.0, 180.4, 247.0)), ('A', '485', 19, 'cablam Outlier', (201.6, 181.5, 250.2)), ('A', '486', 19, 'cablam Outlier', (205.3, 181.3, 251.1)), ('A', '475', 20, 'smoc Outlier', (210.036, 180.077, 243.138)), ('A', '476', 20, 'smoc Outlier', (212.001, 177.738, 245.412)), ('A', '477', 20, 'cablam Outlier', (212.3, 174.0, 246.1)), ('A', '666', 21, 'cablam Outlier', (241.7, 194.6, 173.8)), ('A', '672', 21, 'smoc Outlier', (245.58200000000002, 198.706, 170.288)), ('A', '283', 22, 'side-chain clash', (225.78, 227.953, 188.922)), ('A', '44', 22, 'side-chain clash', (225.78, 227.953, 188.922)), ('A', '371', 23, 'cablam CA Geom Outlier', (198.4, 212.7, 212.3)), ('A', '372', 23, 'cablam Outlier', (201.0, 214.1, 214.7)), ('A', '393', 24, 'side-chain clash', (199.101, 190.228, 201.618)), ('A', '523', 24, 'side-chain clash', (199.101, 190.228, 201.618)), ('A', '399', 25, 'smoc Outlier', (197.61299999999997, 196.594, 220.08)), ('A', '511', 25, 'smoc Outlier', (200.24299999999997, 199.57399999999998, 218.171)), ('A', '355', 26, 'side-chain clash', (201.809, 190.793, 215.966)), ('A', '398', 26, 'side-chain clash', (201.809, 190.793, 215.966)), ('A', '421', 27, 'side-chain clash', (208.999, 185.269, 232.064)), ('A', '457', 27, 'side-chain clash', (208.999, 185.269, 232.064)), ('A', '246', 28, 'backbone clash', (199.217, 241.672, 148.508)), ('A', '254', 28, 'backbone clash', (199.217, 241.672, 148.508)), ('A', '101', 29, 'backbone clash', (210.87, 238.382, 161.797)), ('A', '96', 29, 'backbone clash', (210.87, 238.382, 161.797)), ('A', '144', 30, 'smoc Outlier', (204.291, 249.689, 153.976)), ('A', '155', 30, 'smoc Outlier', (199.267, 248.71399999999997, 157.517)), ('A', '503', 31, 'side-chain clash', (202.885, 210.941, 232.678)), ('A', '506', 31, 'side-chain clash', (202.885, 210.941, 232.678)), ('A', '310', 32, 'cablam CA Geom Outlier', (243.4, 206.6, 177.3)), ('A', '600', 32, 'cablam CA Geom Outlier\nsmoc Outlier', (243.5, 207.4, 173.0)), ('A', '563', 33, 'Rotamer', (204.663, 181.95, 192.20200000000003)), ('A', '564', 33, 'smoc Outlier', (204.82100000000003, 185.46800000000002, 190.766)), ('A', '200', 34, 'side-chain clash', (203.217, 225.913, 181.777)), ('A', '228', 34, 'side-chain clash', (203.217, 225.913, 181.777)), ('A', '115', 35, 'side-chain clash', (188.719, 229.477, 175.487)), ('A', '167', 35, 'side-chain clash', (188.719, 229.477, 175.487))]
data['omega'] = [('A', ' 527 ', 'PRO', None, (198.90599999999998, 203.39999999999998, 198.221)), ('D', ' 146 ', 'PRO', None, (202.28500000000003, 231.33900000000006, 271.728))]
data['rama'] = [('A', ' 321 ', 'GLN', 0.08590283711347542, (216.653, 205.789, 174.222))]
data['cablam'] = [('D', '57', 'GLU', 'check CA trace,carbonyls, peptide', 'bend\n-SSHH', (186.2, 212.9, 257.8)), ('D', '144', 'LEU', 'check CA trace,carbonyls, peptide', 'helix-5\nB-III', (204.4, 228.0, 275.4)), ('D', '224', 'GLU', ' alpha helix', 'helix\nTHHHH', (235.5, 209.8, 268.0)), ('D', '225', 'ASP', ' alpha helix', 'helix\nHHHHH', (235.7, 212.4, 265.2)), ('D', '267', 'LEU', 'check CA trace,carbonyls, peptide', 'bend\nGGSSS', (221.2, 233.8, 275.7)), ('D', '303', 'ASP', 'check CA trace,carbonyls, peptide', ' \nT--SS', (202.9, 237.6, 242.5)), ('D', '334', 'THR', 'check CA trace,carbonyls, peptide', 'bend\n--S--', (199.6, 230.0, 248.3)), ('D', '424', 'LEU', 'check CA trace,carbonyls, peptide', 'bend\nS-S-S', (219.1, 244.8, 244.0)), ('D', '427', 'ASP', 'check CA trace,carbonyls, peptide', ' \n-S---', (225.6, 249.8, 241.3)), ('D', '428', 'PHE', 'check CA trace,carbonyls, peptide', ' \nS----', (225.6, 248.8, 245.0)), ('D', '602', 'SER', 'check CA trace,carbonyls, peptide', 'bend\nGGS--', (238.5, 242.0, 277.3)), ('D', '353', 'LYS', 'check CA trace', 'turn\nEETTE', (204.9, 207.2, 241.4)), ('D', '423', 'LEU', 'check CA trace', ' \nSS-S-', (216.2, 243.4, 241.9)), ('A', '20', 'THR', 'check CA trace,carbonyls, peptide', ' \n-----', (204.0, 235.0, 142.6)), ('A', '88', 'ASP', 'check CA trace,carbonyls, peptide', 'bend\n-SS-E', (206.8, 217.0, 171.7)), ('A', '108', 'THR', 'check CA trace,carbonyls, peptide', 'bend\nEESS-', (195.2, 221.3, 166.1)), ('A', '112', 'SER', 'check CA trace,carbonyls, peptide', 'bend\n-BSSS', (187.3, 227.7, 164.7)), ('A', '159', 'VAL', 'check CA trace,carbonyls, peptide', 'strand\nEEEEE', (195.6, 236.6, 160.4)), ('A', '178', 'ASP', ' beta sheet', ' \n-----', (211.9, 250.0, 164.3)), ('A', '179', 'LEU', ' beta sheet', ' \n-----', (210.4, 248.3, 161.2)), ('A', '231', 'ILE', ' beta sheet', ' \nEE---', (196.1, 227.6, 178.3)), ('A', '251', 'PRO', 'check CA trace,carbonyls, peptide', ' \nTS-S-', (203.4, 247.0, 141.7)), ('A', '260', 'ALA', 'check CA trace,carbonyls, peptide', ' \n-B---', (209.7, 239.9, 151.1)), ('A', '315', 'THR', 'check CA trace,carbonyls, peptide', ' \nEE--S', (229.5, 201.1, 177.9)), ('A', '321', 'GLN', 'check CA trace,carbonyls, peptide', ' \n-----', (216.7, 205.8, 174.2)), ('A', '372', 'ALA', 'check CA trace,carbonyls, peptide', ' \nHT---', (201.0, 214.1, 214.7)), ('A', '389', 'ASP', 'check CA trace,carbonyls, peptide', 'helix-3\nGGG-E', (204.2, 202.8, 197.8)), ('A', '442', 'ASP', 'check CA trace,carbonyls, peptide', 'helix\nHHH--', (192.0, 205.0, 230.7)), ('A', '477', 'SER', 'check CA trace,carbonyls, peptide', 'bend\n-SSS-', (212.3, 174.0, 246.1)), ('A', '485', 'GLY', 'check CA trace,carbonyls, peptide', 'bend\n--SSS', (201.6, 181.5, 250.2)), ('A', '486', 'PHE', 'check CA trace,carbonyls, peptide', 'bend\n-SSSE', (205.3, 181.3, 251.1)), ('A', '528', 'LYS', 'check CA trace,carbonyls, peptide', ' \n-S---', (199.4, 204.4, 193.5)), ('A', '592', 'PHE', 'check CA trace,carbonyls, peptide', ' \nSS---', (221.1, 192.1, 173.5)), ('A', '638', 'THR', 'check CA trace,carbonyls, peptide', ' \nS---S', (229.7, 200.1, 160.0)), ('A', '666', 'ILE', 'check CA trace,carbonyls, peptide', 'strand\nEEEET', (241.7, 194.6, 173.8)), ('A', '185', 'ASN', 'check CA trace', 'bend\n-SSEE', (224.0, 240.7, 156.9)), ('A', '214', 'ARG', 'check CA trace', 'bend\nESSS-', (223.6, 231.9, 156.2)), ('A', '218', 'GLN', 'check CA trace', ' \n-----', (228.2, 227.3, 166.1)), ('A', '310', 'LYS', 'check CA trace', 'bend\n--SEE', (243.4, 206.6, 177.3)), ('A', '316', 'SER', 'check CA trace', ' \nE--S-', (226.0, 199.6, 177.5)), ('A', '317', 'ASN', 'check CA trace', 'bend\n--S--', (223.7, 197.4, 175.2)), ('A', '371', 'SER', 'check CA trace', 'turn\nHHT--', (198.4, 212.7, 212.3)), ('A', '484', 'GLU', 'check CA trace', ' \nT--SS', (200.0, 180.4, 247.0)), ('A', '526', 'GLY', 'check CA trace', ' \nEE-S-', (199.0, 201.1, 197.6)), ('A', '527', 'PRO', 'check CA trace', 'bend\nE-S--', (198.1, 203.6, 197.0)), ('A', '590', 'CYS', 'check CA trace', 'bend\nE-SS-', (216.6, 197.3, 175.4)), ('A', '600', 'PRO', 'check CA trace', 'bend\nEES-T', (243.5, 207.4, 173.0)), ('A', '640', 'SER', 'check CA trace', 'bend\n--S-E', (235.2, 200.8, 157.5))]
handle_read_draw_probe_dots_unformatted("/home/ccpem/agnel/gisaid/countries_seq/structure_data/emdb/EMD-11682/7a92/Model_validation_1/validation_cootdata/molprobity_probe7a92_0.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
