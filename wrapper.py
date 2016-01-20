from pickle_storage import *
from options import *
from module_map import *
from E2_page import *
from db.etwo import EtwoStore
import os.path
try:
    from plot_page import *
except (ImportError, RuntimeError):
    pass


class MASS(object):
    def __init__(self, options = None):
        if not options:
            self.options = Options.default("Real")
        else:
            self.options = options
        self.resolution_flag = False
        self.resolution_loaded_flag = False
        self.resolution_no_mat_flag = False
        self.resolution_no_mat_loaded_flag = False
        self.E_2_page_flag = False
        self.E_2_page_no_mat_flag = False
    
    def get_options(self):
        return self.options

    def set_case(self, case):
        self.get_options().case = case

    def set_comm_db(self, database):
        self.get_options().commutativity_database = database

    def set_adem_db(self, database):
        self.get_options().adem_database = database

    def set_degree_bounds(self, bounds):
        self.get_options().degree_bounds = bounds
        self.resolution_flag = False

    def set_log_file(self, filename):
        self.get_options().log_file = filename

    def set_logging_level(self, level):
        self.get_options().logging_level = level

    def set_resolution_file(self, filename):
        self.get_options().resolution_file = filename
        
    def set_dual_resolution_file(self, filename):
        self.get_options().dual_resolution_file = filename
    
    def set_t(self, t):
        self.get_options().t =t 
    
    def set_p(self, p):
        self.get_options().p = p

    def set_p_dual(self, p_dual):
        self.get_options().p_dual = p_dual

    def set_t_dual(self, t_dual):
        self.get_options().t_dual = t_dual

    def set_degree_dictionary(self, dictionary):
        self.get_options().degree_dictionary = dictionary

    def set_numpcs(self, number):
        self.get_options().numpcs = number

    def start_session(self):
        """
        This starts the various shared database servers
        """
        self.get_options().get_comm_db()
        self.get_options().get_adem_db()

    def stop_session(self):
        """
        This method properly closes out of shared dictionary
        servers, and pickles any modifications to the 
        dictionaries.
        """
        self.get_options().get_comm_db().shutdown()
        self.get_options().get_adem_db().shutdown()
        self.get_E_2_page_no_mat().pickle_lol_storage(self.get_options())
        #which E_2_page gets the LOL?

    def initialize_resolution(self):
        module_map = make_initial_map(self.get_options())
        pickle_file = open(self.get_options().get_resolution_file(), "wb")
        new_resolution = Resolution([module_map], self.get_options())
        pickle.dump(new_resolution, pickle_file, -1)
        pickle_file.close()

    def load_pickled_resolution(self):
        logging.basicConfig(filename=self.get_options().get_log_file(), 
                            level=self.get_options().get_logging_level())
        logging.warning("loading pickled resolution")
        pickle_file = open(self.get_options().get_resolution_file(), "rb")
        self.resolution = pickle.load(pickle_file)
        pickle_file.close()
        self.resolution_loaded_flag = True

    def compute_resolution(self, length):
        logging.basicConfig(filename=self.get_options().get_log_file(), 
                            level=self.get_options().get_logging_level())
        logging.warning("continuing resolution")
        logging.warning(time.ctime())
        if not self.resolution_loaded_flag:
            self.load_pickled_resolution()
        current_length = self.resolution.get_length()
        logging.warning("i'm at " + str(current_length))
        logging.warning(time.ctime())
        while current_length <= length:
            logging.warning("moving on to next resolvant")
            logging.warning(time.ctime())
            last_map = self.resolution.get_map_list()[-1]
            self.resolution.get_map_list().append(
                last_map.get_next_resolvant(
                    "h" + str(current_length), 
                    self.get_options()))
            current_length = current_length + 1
            pickle_filename = self.get_options().get_resolution_file()
            pickle_file = open(pickle_filename, "wb")
            pickle.dump(self.resolution, pickle_file, -1)
            pickle_file.close()
        logging.warning(time.ctime())
        logging.warning("DONE!!!")

    def extend_resolution(self, new_degree_bounds):
        logging.basicConfig(filename=self.get_options().get_log_file(), 
                            level=self.get_options().get_logging_level())
        if not self.resolution_loaded_flag:
            self.load_pickled_resolution()
        logging.warning("continuing resolution")
        logging.warning(time.ctime())
        new_resolution = []
        new_resolution.append(extend_initial_map(
                new_degree_bounds, 
                self.get_options()))
        for index in xrange(len(self.resolution.get_map_list()) - 1):
            logging.warning("moving on to next resolvant")
            logging.warning(time.ctime())
            _map = new_resolution[index]
            logging.warning("got the map")
            new_resolution.append(
                _map.extend_next_resolvant(
                    self.resolution.get_map_list()[index+1], 
                    "h" + str(index+2), 
                    new_degree_bounds, 
                    self.get_options()))
            logging.warning("extended resolution")
            pickle_file = open(self.get_options().get_resolution_file(), 
                               "wb")
            the_resolution = Resolution(new_resolution, self.get_options())
            pickle.dump(the_resolution, pickle_file, -1)
            pickle_file.close()
        self.resolution = the_resolution
        self.get_options().degree_bounds = new_degree_bounds

    def make_resolution(self):
        if os.path.isfile(self.get_options(
                    ).get_resolution_file()):
            if not self.resolution_loaded_flag:
                self.load_pickled_resolution()
            first_map = self.resolution.get_map_list()[0]
            old_bounds = first_map.get_domain().get_deg_bounds()
            new_bounds = self.get_options().get_degree_bounds()
            if (old_bounds[0] < new_bounds[0] 
                or old_bounds[1] < new_bounds[1]):
                self.get_options().degree_bounds = old_bounds
                self.extend_resolution(new_bounds)
                self.compute_resolution(
                    self.get_options().get_degree_bounds()[0]/2 + 1)
            elif (len(self.resolution.get_map_list()) 
                  < self.get_options().get_degree_bounds()[0]/2 + 1):
                self.compute_resolution(
                    self.get_options().get_degree_bounds()[0]/2 + 1)
            self.resolution_flag = True
            self.resolution_loaded_flag = True
            self.resolution_no_mat_flag = False
            self.resolution_no_mat_loaded_flag = False
            self.E_2_page_flag = False
            self.E_2_page_no_mat_flag = False
        else:
            self.initialize_resolution()
            self.compute_resolution(
                self.get_options().get_degree_bounds()[0]/2 + 1)
            self.resolution_flag = True
            self.resolution_loaded_flag = True

    def get_resolution(self):
        if not self.resolution_flag or not self.resolution_loaded_flag:
            self.make_resolution()
        return self.resolution

    def make_no_mat_resolution(self):
        if not self.resolution_no_mat_flag:
            newres = []
            for amap in self.get_resolution().get_map_list():
                domain = amap.domain
                codomain = amap.codomain
                generator_map = amap.generator_map
                amap_copy = FreeAModuleMap(domain, codomain, generator_map)
                newres.append(amap_copy)
            resolution = Resolution(newres, self.get_options())
            pickle_file = open(self.get_options().get_resolution_file_no_mat(), "wb")
            pickle.dump(resolution, pickle_file, -1)
            pickle_file.close()

    def load_no_mat_resolution(self):
        if not self.resolution_no_mat_loaded_flag:
            try:
                pickle_file = open(self.get_options().get_resolution_file_no_mat(), "rb")
                self.resolution_no_mat = pickle.load(pickle_file)
                pickle_file.close()
                first_map = self.resolution_no_mat.get_map_list()[0]
                old_bounds = first_map.get_domain().get_deg_bounds()
                new_bounds = self.get_options().get_degree_bounds()
                if (old_bounds[0] == new_bounds[0] 
                    and old_bounds[1] == new_bounds[1]):
                    self.resolution_no_mat_loaded_flag = True
                else:
                    self.make_no_mat_resolution()
            except (IOError, EOFError):
                self.make_no_mat_resolution()
        else:
            first_map = self.resolution_no_mat.get_map_list()[0]
            old_bounds = first_map.get_domain().get_deg_bounds()
            new_bounds = self.get_options().get_degree_bounds()
            if (old_bounds[0] == new_bounds[0] 
                and old_bounds[1] == new_bounds[1]):
                self.resolution_no_mat_loaded_flag = True
            else:
                self.make_no_mat_resolution()

    def get_no_mat_resolution(self):
        if (not self.resolution_no_mat_loaded_flag 
            or not self.resolution_no_mat_flag):
            self.load_no_mat_resolution()
        return self.resolution_no_mat

    def compute_E_2_page(self):
        self.E_2_page = E2Page(self.get_resolution(), self.get_options())
        self.E_2_page_flag = True

    def get_E_2_page(self):
        if not self.E_2_page_flag:
            self.compute_E_2_page()
        return self.E_2_page

    def compute_E_2_page_no_mat(self):
        self.E_2_page_no_mat = E2Page(self.get_no_mat_resolution(), self.get_options())
        self.E_2_page_no_mat_flag = True

    def get_E_2_page_no_mat(self):
        if not self.E_2_page_no_mat_flag:
            self.compute_E_2_page_no_mat()
        return self.E_2_page_no_mat

    def make_dual_resolution(self):
        self.get_E_2_page_no_mat().make_dual_resolution(self.get_options())

    def get_printout(self, filename):
        self.get_E_2_page_no_mat().printout(filename, self.get_options())

    def make_charts(self):
        charts(self.get_E_2_page_no_mat(), self.options)

    def make_charts_with_mat(self):
        #Important note: list of lifts is only saved for 
        #E_2 page without mat! 
        charts(self.get_E_2_page(), self.options)

    def make_isaksen_chart(self):
        if self.options.get_case() == "Classical":
            return
        for diff in range(0, self.options.get_degree_bounds()[0]):
            isaksen_chart(self.get_E_2_page(), diff, self.options)

    def make_classical_chart(self):
        if self.options.get_case() != "Classical":
            return
        classical_chart(self.get_E_2_page(), self.options)

    def cohomology_info(self, level, position):
        output = ""
        e2 = self.get_E_2_page()
        cohom = e2.get_cohomology(self.options)[level][position]
        output += "outgoing matrix \n"
        output += str(cohom.get_B()) + "\n"
        output += "incoming matrix \n"
        output += str(cohom.get_A()) + "\n"
        output += "kernel basis \n"
        for vect in cohom.get_kernel().get_basis():
            output += str(e2.element_from_vector(vect, level, 
                                                 position, 
                                                 self.options)) + "\n"
        output += "image basis \n"
        for vect in cohom.get_image().get_basis():
            output += str(e2.element_from_vector(vect, level, 
                                                 position, 
                                                 self.options)) + "\n"
        prev_cohom = e2.get_cohomology(self.options)[level-1][position]
        output += "what is mapping in to 0 under A \n"
        for vect in prev_cohom.get_kernel().get_basis():
            output += str(e2.element_from_vector(vect, level - 1, 
                                                 position, 
                                                 self.options)) + "\n"
        mod_basis = e2.get_dual_resolution(self.options).get_map_list()[level - 1].get_domain().get_array(self.options)[position].get_basis()
        output += "basis for domain of A \n"
        if mod_basis:
            for thing in mod_basis:
                output += str(thing) + "\n"
        else:
            output += "the basis is empty \n"

        mod_basis = e2.get_dual_resolution(self.options).get_map_list()[level].get_domain().get_array(self.options)[position].get_basis()
        output += "basis for domain of B \n"
        if mod_basis:
            for thing in mod_basis:
                output += str(thing) + "\n"
        else:
            output += "the basis is empty\n"

        mod_basis = e2.get_dual_resolution(self.options).get_map_list()[level - 1].get_domain().get_generator_list()
        output += "basis for h-dual module for A \n"
        if mod_basis:
            for thing in mod_basis:
                output += str(thing) + "\n"

        mod_basis = e2.get_dual_resolution(self.options).get_map_list()[level].get_domain().get_generator_list()
        output += "basis for h-dual module for B \n"
        if mod_basis:
            for thing in mod_basis:
                output += str(thing) + "\n"

        return output

    def cohomology_printout(self, filename):
        output = ""
        e2 = self.get_E_2_page()
        for level in xrange(len(e2.get_cohomology(self.options))):
            for position in e2.get_cohomology(self.options)[level].keys():
                output += "At level " + str(level) + " position " + str(position) + "\n"
                output += self.cohomology_info(level, position)
        _file = open(filename, 'w+')
        _file.write(output)
        _file.close()

    def compute_product_structure(self):
        self.get_E_2_page_no_mat().compute_product_structure(self.get_options())
        
        
    def make_product_database(self):
        e2 = self.get_E_2_page_no_mat()
        EtwoStore.prepare()
        for z_index in xrange(len(e2.get_cohomology(self.options))):
            z_level = e2.get_cohomology(self.options)[z_index]
            for position in z_level.keys():
                if e2.get_dual_resolution(self.options).get_map_list()[z_index].get_domain().get_array(self.options)[position].get_basis():
                    for thing in z_level[position].get_product().get_basis():
                        elt = e2.get_dual_resolution(self.options\
                        ).get_map_list()[z_index].get_domain(\
                        ).element_from_vector(position, thing, self.options)
                        for product in e2.product_description_string(elt, self.options):
                            EtwoStore.save(elt, z_index, product, self.options)
            
    def p_operator(self, xx, pos_xx):
        h3 = ModElt(ModuleMonomial(RSq(), Generator("h1(8, 4)0", 
                                                    (8, 4))))
        h04 = ModElt(ModuleMonomial(RSq(), Generator("h4(4, 0)0", 
                                                     (4, 0))))
        if self.options.get_case() == "Classical":
            h3 = ModElt(ModuleMonomial(RSq(), Generator("h1(8, 0)0", 
                                                        (8, 0))))
        massey_out = self.get_E_2_page().level_one_m_product(
            h3, 1, h04, 4, xx, pos_xx, self.get_options())
        return massey_out

    def massey_product_printout(self, filename):
        output = ""
        map_list = self.get_E_2_page().get_dual_resolution(self.options).get_map_list()
        for index in xrange(len(map_list)-5):
            amap = map_list[index]
            for element in amap.get_domain().get_generator_list():
                output += "<h1(8, 4)0, h4(4, 0), " + str(element) 
                output += "> contains "
                try:
                    m_product = self.p_operator(element, index)
                    output += str(m_product) + "\n"
                except (KeyError, AttributeError):
                    output += "??? \n"
        out_file = open(filename, "w+")
        out_file.write(output)
        out_file.close()
                

    #The following would work with suitable modifications. 
    #Need to have the bar resolution, so that it is a DG algebra! 

    # def massey_product(self, uu, level_uu, vv, level_vv, ww, level_ww):
    #     massey_out = self.get_E_2_page().massey_product(
    #         uu, level_uu, vv, level_vv, ww, level_ww, 
    #         self.get_options())
    #     return massey_out

    # def total_massey_product(self, uu, level_uu, vv, level_vv, ww, 
    #                          level_ww):
    #     massey_out = self.get_E_2_page().total_massey_product(
    #         uu, level_uu, vv, level_vv, ww, level_ww, 
    #         self.get_options())
    #     return massey_out
