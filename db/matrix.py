import MySQLdb as mdb
import pickle

class MatrixStore:
   @staticmethod
   def prepare():
      # check to see if there is a database
      db = mdb.connect('localhost', 'massdb', '$u13pol0nium', 'massdb')
      cursor = db.cursor()
      if count > 0:
         return
      try:
         create_query = """CREATE TABLES IF NOT EXIST matrix
                           (id           INT  UNSIGNED,
                            rows         BLOB NOT NULL,
                            rref         BLOB NULL,
                            basis_change BLOB NULL,
                            flags        TINYINT UNSIGNED,
                            row_count    INT UNSIGNED,
                            col_count    INT UNSIGNED,
                            weights      BLOB NULL,
                            timestamp    TIMESTAMP
                          )
                          ENGINE = InnoDB"""
         status = cursor.execute( create_query )
      except:
         db.rollback()
      db.close()
   
   @staticmethod
   def drop():
      db = mdb.connect('localhost', 'massdb', '$u13pol0nium', 'massdb')
      cursor = db.cursor()
      try:
         cursor.execute('DROP TABLE matrix')
      except:
         db.rollback()
      db.close()

   @staticmethod
   def save( matrix ):
      db = mdb.connect('localhost', 'massdb', '$u13pol0nium', 'massdb')
      cursor = db.cursor()
      row = pickle.dumps( matrix._rows )
      rref = pickle.dumps( matrix._rref )
      basis_change = pickle.dumps( matrix.basis_change )
      row_count = matrix.get_row_count()
      col_count = matrix.get_col_count()
      weights = pickle.dumps( matrix.row_weights )
      flags = (4 if matrix.basis_change_flag else 0) + \
              (2 if matrix._rref_flag else 0) + \
              (1 if matrix.row_weightw_flag else 0)
               
      query_str = """INSERT INTO matrix
         (rows, rref, basis_change, flags, row_count, col_count, weights, timestamp)
         VALUES
         (%s,   %s,   %s,           %i,    %i,        %i,        %s,      NOW())""" % \
         (rows, rref, basis_change, flags, row_count, col_count, weight)

      try:
         cursor.execute( query_str )
      except:
         db.rollback()
      db.close()
