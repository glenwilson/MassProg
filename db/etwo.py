import MySQLdb as mdb
import pickle

class EtwoStore:
   @staticmethod
   def prepare():
      # check to see if there is a database
      db = mdb.connect(host='localhost', user='compute_mass', 
                       passwd='<A324kr2Y2sS', db='compute_mass_db')
      cursor = db.cursor()
      try:
         create_query = """CREATE TABLE IF NOT EXISTS etwo (gen TEXT, extg SMALLINT, topg SMALLINT, adamsg SMALLINT, motg SMALLINT, product TEXT, thecase VARCHAR(20), id MEDIUMINT primary key NOT NULL AUTO_INCREMENT);"""
         cursor.execute( create_query )
         db.commit()
      except:
         db.rollback()
      db.close()
   
   @staticmethod
   def drop():
      db = mdb.connect(host='localhost', user='compute_mass', 
                       passwd='<A324kr2Y2sS', db='compute_mass_db')
      cursor = db.cursor()
      try:
         cursor.execute('DROP TABLE etwo')
         db.commit()
      except:
         db.rollback()
      db.close()

   @staticmethod
   def save( element, extgrading, product, options ):
      db = mdb.connect(host='localhost', user='compute_mass', 
                       passwd='<A324kr2Y2sS', db='compute_mass_db')
      cursor = db.cursor()
      gen = str(element)
      extg = extgrading
      topg = element.get_degree(options)[0]
      adamsg = topg - extg
      motg = element.get_degree(options)[1]
      thecase = options.get_case()
      query_str = """INSERT INTO etwo
         (gen, extg, topg, adamsg, motg, product, thecase)
         VALUES
         (%s,   %s,   %s,   %s,    %s,   %s,   %s)"""
      cursor.execute(query_str, (gen, extg, topg, adamsg, motg,
                                 product, thecase))
      db.commit()
      db.close()

class E2Entry:
   def __init__(self, params):
      self.__params = params
      for key in params:
         func_name = "get_%s" % (key)
         setattr(self.__class__, 
                 func_name, 
                 lambda s: s.__params[func_name])

   def as_dict(self):
      return self.__params

   def __str__(self):
      string = "|"
      for key in self.as_dict():
         string += " " + str(self.as_dict()[key]) + " |"
      return string
      
   '''
   Example:

   E2Entry.find_by([
      ("gen", "contains", "h2"),
      ("adamsg", "=", 1),
      ("motg", ">", 2)
   ])
   '''
   @staticmethod
   def find_by(params):
      db = mdb.connect(host='localhost', user='compute_mass', 
                       passwd='<A324kr2Y2sS', db='compute_mass_db') 
      cursor = db.cursor()
      query_string = "DESC etwo"
      cursor.execute(query_string) 
      table_column_names = [column[0] for column in cursor.fetchall()]

      query_string = E2Entry.__create_query(params)
      cursor.execute(query_string)
      e2entries = []
      for row in cursor.fetchall():
         params = {}
         for i in xrange(len(table_column_names)):
            column_name = table_column_names[i]
            params[column_name] = row[i]
         e2entries.append(E2Entry(params))

      db.close()
      return e2entries 

   @staticmethod
   def __create_query(params):
      query_string = """SELECT * FROM etwo WHERE """
      query_params = []
      for param in params:
         if param[1].lower() == "like" or \
            param[1].lower() == "contains":
            template = "{0} {1} \"%{2}%\""
         elif type(param[2]) == str:
            template = "{0} {1} \"{2}\"" 
         else:
            template = "{0} {1} {2}"
         query_params.append(template.format(*param))

      return query_string + " AND ".join(query_params)
