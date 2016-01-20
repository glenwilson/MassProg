from shelf_storage import ShelfStorage
from pickle_storage import PickleStorage
from mem_storage import MemStorage
from free_A_module import *
import cPickle as pickle
import os.path
import logging

class Options(object):
    @staticmethod
    def make_pickled_options(filename, options):
        """
        create a pickled options object with given filename
        """
        pickle_file = open(filename, "wb")
        pickle.dump(options, pickle_file, -1)
        pickle_file.close()

    @staticmethod
    def get_pickled_options(filename):
        """
        load a pickled options object from filename
        """
        pickle_file = open(filename, "rb")
        options = pickle.load(pickle_file)
        pickle_file.close()
        return options

    @staticmethod
    def default(case):
        if case == "Real":
            return Options("real", 
                           PickleStorage("real_comm_db.pickle"),
                           PickleStorage("real_adem_db.pickle"), "t",
                           "p", "t*", "p*", 
                           { "t" : (0,1), "p" :(1,1), "u" : (1, 1), "t*" : (0, -1), 
                             "p*" : (-1, -1), "u*" : (-1, -1) }, 
                           "Real", (12, 6), logging.WARNING, 2)
        elif case == "Classical":
            return Options("cl",         
                           PickleStorage("cl_comm_db.pickle"),
                           PickleStorage("cl_adem_db.pickle"), 
                           "t", "p", "t*", "p*", 
                           { "t" : (0,1), "p" : (1,1), "u" : (1, 1), 
                             "t*" : (0, -1), "p*" : (-1, -1), "u*" : (-1, -1) }, 
                           "Classical", (20, 0), 
                           logging.WARNING, 2)
        elif case == "Complex":
            return Options("cx",
                           PickleStorage("cx_comm_db.pickle"),
                           PickleStorage("cx_adem_db.pickle"),
                           "t", "p", "t*", "p*",
                           { "t" : (0,1), "p" : (1,1), "u" : (1, 1), "t*" : (0, -1), 
                             "p*" : (-1, -1), "u*" : (-1, -1) }, "Complex", (12, 6),
                           logging.WARNING, 2)
        elif case == "FiniteOdd1":
            return Options( "fo1",
                            PickleStorage("fo1_comm_db.pickle"),
                            PickleStorage("fo1_adem_db.pickle"), "t", "p", "t*",
                            "p*", { "t" : (0,1), "p" : (1,1), "u" : (1, 1), "t*" :
                                    (0, -1), "p*" : (-1, -1), "u*" : (-1, -1) },
                            "FiniteOdd1", (12, 6), logging.WARNING, 2)
        elif case == "FiniteOdd3":
            return Options( "fo3",
                            PickleStorage("fo3_comm_db.pickle"),
                            PickleStorage("fo3_adem_db.pickle"),
                            "t", "p", "t*", "p*", 
                            { "t" : (0,1), "p" : (1,1), "u" : (1, 1), 
                              "t*" : (0, -1), "p*" : (-1, -1), "u*" : (-1, -1) },
                            "FiniteOdd3", (12, 6),logging.WARNING, 2)

        
    def __init__(self, prefix, commutativity_database, adem_database,
                 t, p, t_dual, p_dual, degree_dictionary, case,
                 degree_bounds, logging_level, numpcs):
        """
        case should be either Real, Complex, Classical right now. 
        """
        self.prefix = prefix
        self.commutativity_database = commutativity_database
        self.adem_database = adem_database
        self.t = t
        self.p = p
        self.u = "u"
        self.t_dual = t_dual
        self.p_dual = p_dual
        self.u_dual = "u*"
        self.degree_dictionary = degree_dictionary
        self.case = case
        self.degree_bounds = degree_bounds
        self.log_file = self.prefix + "_log.log"
        self.logging_level = logging_level
        self.resolution_file = self.prefix + "_resolution.pickle"
        self.resolution_file_no_mat = self.prefix + \
        "_resolution_no_mat.pickle"
        self.dual_resolution_file = self.prefix + "_dual_res.pickle"
        self.a_star_file = self.prefix + "_a_star"
        self.lol_file = self.prefix + "_lol.pickle"
        if os.path.isfile(self.a_star_file):
            print "trying to see if a star is pickled"
            self.a_star_pickled = True
        else:
            self.a_star_pickled = False
        self.a_star_loaded = False
        self.comm_db_flag = False
        self.adem_db_flag = False
        self.a_star_bounds = None
        self.numpcs = numpcs

    def compute_a_star(self, bounds = None):
        logging.basicConfig(filename=self.get_log_file(), level=self.get_logging_level())
        if not bounds:
            bounds = self.get_degree_bounds()
        if not self.a_star_pickled:
            print "computing a star!" + str(bounds)
            self.a_star = a_star(bounds[0], 
                                 bounds[1],
                                 self)
            pickle_file = open(self.a_star_file, "wb")
            pickle.dump(self.a_star, pickle_file, -1)
            pickle_file.close()
            self.a_star_pickled = True
            self.a_star_loaded = True
            self.a_star_bounds = bounds
            # max(self.a_star.keys())
        elif not self.a_star_loaded:
            logging.warning("loading a_star")
            pickle_file = open(self.a_star_file, "rb")
            self.a_star = pickle.load(pickle_file)
            pickle_file.close()
            if not bounds in self.a_star:
                print "computing a star!" + str(bounds)
                self.a_star = a_star(
                    bounds[0], 
                    bounds[1],
                    self)
                pickle_file = open(self.a_star_file, "wb")
                pickle.dump(self.a_star, pickle_file, -1)
                pickle_file.close()
                self.a_star_bounds = bounds
            self.a_star_loaded = True
        else:
            if not bounds in self.a_star:
                self.a_star = a_star(
                    bounds[0], 
                    bounds[1],
                    self)
                pickle_file = open(self.a_star_file, "wb")
                pickle.dump(self.a_star, pickle_file, -1)
                pickle_file.close()
                self.a_star_bounds = bounds

    def get_a_star(self, bounds = None):
        logging.basicConfig(filename=self.get_log_file(), level=self.get_logging_level())
        if bounds:
            if self.a_star_loaded:
                try:
                    if self.a_star_bounds[0] < bounds[0]\
                            or self.a_star_bounds[1] < bounds[1]:
                        print "computing a star"
                        self.compute_a_star(bounds)
                except (TypeError):
                    self.compute_a_star(bounds)
        else:
            if not self.a_star_pickled \
                    or not self.a_star_loaded:
                self.compute_a_star(bounds)
        return self.a_star

    def get_comm_db(self):
        if (isinstance(self.commutativity_database, 
                       PickleStorage) \
                and not self.comm_db_flag):
            #print "loading comm db"
            self.commutativity_database.load_dictionary()
            self.comm_db_flag = True
        return self.commutativity_database

    def get_adem_db(self):
        if isinstance(self.adem_database, PickleStorage) \
                and not self.adem_db_flag:
            #print "loading adem db"
            self.adem_database.load_dictionary()
            self.adem_db_flag = True
        return self.adem_database

    def get_t(self):
        return self.t

    def get_p(self):
        return self.p

    def get_u(self):
        return self.u

    def get_t_dual(self):
        return self.t_dual

    def get_p_dual(self):
        return self.p_dual

    def get_u_dual(self):
        return self.u_dual

    def get_degree_dictionary(self):
        return self.degree_dictionary

    def get_case(self):
        return self.case

    def get_degree_bounds(self):
        return self.degree_bounds
    
    def get_log_file(self):
        return self.log_file

    def get_logging_level(self):
        return self.logging_level

    def get_resolution_file(self):
        return self.resolution_file 

    def get_resolution_file_no_mat(self):
        return self.resolution_file_no_mat

    def get_dual_resolution_file(self):
        return self.dual_resolution_file

    def get_lol_file(self):
        return self.lol_file

    def get_numpcs(self):
        return self.numpcs

