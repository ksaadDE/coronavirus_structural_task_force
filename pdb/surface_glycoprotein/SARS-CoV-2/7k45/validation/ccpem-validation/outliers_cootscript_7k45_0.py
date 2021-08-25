
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
data['rota'] = []
data['cbeta'] = []
data['fdr'] = []
data['fsc'] = []
data['diffmap'] = []
data['jpred'] = []
data['clusters'] = [('H', '64', 1, 'smoc Outlier', (254.899, 268.899, 283.20799999999997)), ('H', '66', 1, 'smoc Outlier', (250.429, 267.98099999999994, 279.79699999999997)), ('H', '67', 1, 'smoc Outlier', (250.4, 271.63599999999997, 280.839)), ('H', '102', 2, 'smoc Outlier', (278.272, 280.912, 265.024)), ('H', '28', 2, 'smoc Outlier', (273.163, 282.944, 265.98999999999995)), ('L', '78', 1, 'smoc Outlier', (292.745, 271.65500000000003, 293.26099999999997)), ('L', '79', 1, 'smoc Outlier', (290.189, 273.702, 295.178)), ('L', '80', 1, 'Dihedral angle:CB:CG:CD:OE1', (290.356, 277.48799999999994, 295.384)), ('B', '391', 1, 'smoc Outlier', (265.39799999999997, 281.59, 221.319)), ('B', '519', 1, 'cablam Outlier\nsmoc Outlier', (276.6, 276.4, 221.8)), ('B', '520', 1, 'smoc Outlier', (273.601, 274.69, 220.23999999999998)), ('B', '521', 1, 'cablam Outlier', (270.9, 274.9, 217.5)), ('B', '522', 1, 'cablam Outlier', (268.5, 276.8, 219.9)), ('B', '444', 2, 'smoc Outlier', (244.212, 271.59, 254.465)), ('B', '499', 2, 'smoc Outlier', (243.096, 277.84000000000003, 255.448)), ('B', '500', 2, 'smoc Outlier', (243.26, 280.374, 258.264)), ('B', '501', 2, 'smoc Outlier', (246.83700000000002, 281.49799999999993, 257.661)), ('B', '503', 2, 'smoc Outlier', (249.003, 285.684, 253.32500000000002)), ('B', '363', 3, 'smoc Outlier', (256.857, 278.462, 223.883)), ('B', '364', 3, 'Dihedral angle:CA:CB:CG:OD1', (253.815, 280.66900000000004, 223.79299999999998)), ('B', '480', 4, 'smoc Outlier', (274.78099999999995, 261.589, 265.469)), ('B', '484', 4, 'cablam Outlier\nsmoc Outlier', (268.3, 262.6, 266.7)), ('B', '379', 5, 'smoc Outlier', (261.83299999999997, 288.58, 234.57399999999998)), ('B', '432', 5, 'smoc Outlier', (261.45599999999996, 284.49299999999994, 234.74499999999998)), ('A', '1', 1, 'Bond angle:C8:C7:N2', (250.142, 277.117, 231.471))]
data['probe'] = [(' A   1  NAG  H82', ' B 342  PHE  HB2', -0.591, (250.682, 276.232, 232.763))]
data['omega'] = [('L', '   8 ', 'PRO', None, (278.819, 262.76800000000003, 296.95000000000005))]
data['cablam'] = [('H', '108', 'ASP', 'check CA trace,carbonyls, peptide', 'bend\nE-SS-', (278.6, 270.8, 272.6)), ('L', '96', 'THR', 'check CA trace', 'bend\nSSS--', (263.4, 263.7, 275.7)), ('B', '484', 'GLU', 'check CA trace,carbonyls, peptide', ' \nT--BT', (268.3, 262.6, 266.7)), ('B', '486', 'PHE', 'check CA trace,carbonyls, peptide', 'turn\n-BTTE', (271.0, 267.5, 271.3)), ('B', '519', 'HIS', 'check CA trace,carbonyls, peptide', 'bend\n--SS-', (276.6, 276.4, 221.8)), ('B', '521', 'PRO', ' beta sheet', ' \nSS---', (270.9, 274.9, 217.5)), ('B', '522', 'ALA', ' beta sheet', ' \nS---B', (268.5, 276.8, 219.9))]
data['smoc'] = [('H', 4, u'LEU', 0.8203665971665467, (270.76, 285.29499999999996, 276.98499999999996)), ('H', 10, u'GLU', 0.7362222576957228, (256.03799999999995, 287.106, 287.843)), ('H', 28, u'THR', 0.8427157789862625, (273.163, 282.944, 265.98999999999995)), ('H', 40, u'ALA', 0.7521410793730157, (262.92799999999994, 275.678, 293.91799999999995)), ('H', 64, u'PHE', 0.8298429315225248, (254.899, 268.899, 283.20799999999997)), ('H', 66, u'GLU', 0.8043429533169445, (250.429, 267.98099999999994, 279.79699999999997)), ('H', 67, u'ARG', 0.8209245433397045, (250.4, 271.63599999999997, 280.839)), ('H', 102, u'SER', 0.849440706585863, (278.272, 280.912, 265.024)), ('H', 108, u'ASP', 0.8313817572829534, (278.569, 270.82099999999997, 272.557)), ('L', 2, u'ILE', 0.7493699383988911, (266.506, 257.89799999999997, 283.89)), ('L', 11, u'LEU', 0.7418413641137194, (281.634, 267.10900000000004, 300.412)), ('L', 14, u'SER', 0.7921013100455246, (289.48599999999993, 272.47499999999997, 302.809)), ('L', 57, u'THR', 0.770976253009234, (285.48999999999995, 277.564, 277.388)), ('L', 66, u'SER', 0.7721052159355004, (286.65400000000005, 261.67900000000003, 282.70799999999997)), ('L', 70, u'THR', 0.8054571712804556, (277.822, 254.532, 284.025)), ('L', 78, u'ARG', 0.7766160805858117, (292.745, 271.65500000000003, 293.26099999999997)), ('L', 79, u'LEU', 0.7592803074548156, (290.189, 273.702, 295.178)), ('L', 91, u'GLN', 0.8001813501532121, (272.189, 263.97299999999996, 280.747)), ('B', 519, u'HIS', 0.7955109779126641, (276.624, 276.35900000000004, 221.788)), ('B', 520, u'ALA', 0.8004069057655782, (273.601, 274.69, 220.23999999999998)), ('B', 334, u'ASN', 0.7859361479562355, (254.02100000000002, 271.777, 218.509)), ('B', 363, u'ALA', 0.8089830472274321, (256.857, 278.462, 223.883)), ('B', 379, u'CYS', 0.7610918418873946, (261.83299999999997, 288.58, 234.57399999999998)), ('B', 391, u'CYS', 0.7902107956340847, (265.39799999999997, 281.59, 221.319)), ('B', 402, u'ILE', 0.7970792630204803, (257.03799999999995, 277.805, 249.33)), ('B', 414, u'GLN', 0.8319950828685234, (269.35, 286.90599999999995, 247.61399999999998)), ('B', 432, u'CYS', 0.7087586920696899, (261.45599999999996, 284.49299999999994, 234.74499999999998)), ('B', 444, u'LYS', 0.8502807512291558, (244.212, 271.59, 254.465)), ('B', 466, u'ARG', 0.8234386241255173, (269.618, 270.116, 244.324)), ('B', 480, u'CYS', 0.8568507284863017, (274.78099999999995, 261.589, 265.469)), ('B', 484, u'GLU', 0.8070915188410728, (268.33599999999996, 262.633, 266.734)), ('B', 499, u'PRO', 0.8580096485748291, (243.096, 277.84000000000003, 255.448)), ('B', 500, u'THR', 0.8083815777495444, (243.26, 280.374, 258.264)), ('B', 501, u'ASN', 0.8313510582087192, (246.83700000000002, 281.49799999999993, 257.661)), ('B', 503, u'VAL', 0.8221107303022706, (249.003, 285.684, 253.32500000000002)), ('B', 511, u'VAL', 0.7588641635888091, (257.8, 277.98599999999993, 238.70299999999997))]
handle_read_draw_probe_dots_unformatted("/home/ccpem/agnel/gisaid/countries_seq/structure_data/emdb/EMD-22660/7k45/Model_validation_1/validation_cootdata/molprobity_probe7k45_0.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
