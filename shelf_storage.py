import shelve
from storage_exception import StorageException

'''
Class ShelfStorage - A wrapper class for shelves storage,
and exposes an iterator and read/write/contains 
functionalities without the hassle of actually opening and closing
files. 

@note: shelve may raise runtime exceptions, too.
'''
class ShelfStorage:
    def __init__(self, file_name):
        self.__file_name = file_name 

    '''
    iterator - for iterating over a ShelfStorage object

    @returns (on each iteration) a key/value pair of the form
    { 'key': key, 'value': value }. For example, if ( 'Sq4' : Sq4Obj )
    was a key-value pair in the storage, then on one iteration, it will
    return { 'key' : 'Sq4', 'value': Sq4Obj }.

    @usage (recommended)

    <code>
    MI6_employee_record = ShelfStorage('depo')
    for pair in MI6_employee_record:
        print(pair['key'])
	print(pair['value'])
    </code>
    '''
    def __iter__(self):
        self.__shelve = shelve.open( self.__file_name )
        self.__shelve_iter = self.__shelve.__iter__()
        return self

    def next(self):
        try:
	   next_key = self.__shelve_iter.next()
	   return { 'key': next_key, 'value': self.__shelve[next_key] }
	except StopIteration:
	   self.__shelve.close()
	   raise StopIteration
	except Exception:
	   return None

    '''
    copy - copies another storage into this one.

    @params external_storage: another data storage that implements
       an iterator 

    @throws StorageException: raised when shelve exception is raised

    @usage: (recommended) 

    <code> 
    MI6_employee_record = ShelfStorage('depo')
    MI5_employee_record = SomeOtherStorage('depo2')

    try:
        MI6_employee_record.copy(MI5_employee_record)
    except StorageException:
        print 'These are two different agencies!'
    </code>

    Expect: '007'
    '''
    def copy(self, external_storage):
        try:
            storage = shelve.open(self.__file_name)
            for pair in external_storage:
                key = pair['key']
                value = pair['value']
                storage[key] = value
            storage.close()
        except Exception as storage_exception:
            raise StorageException('external storage',\
            'An error occurred while copying external storage to \
            the shelf. Error exception is:\n\
            type:' + type(storage_error) + '\n\
            message:' + storage_error + '\n')

    '''
    read - access a stored value with a given key. If the key is
           not found, a StorageException is raised.

    @params key: the key in the key/value pair to access the data 
                 storage

    @throws StorageException: raised when trying to access data
                              with a key that is not in the 
                              storage 
    
    @returns: the value associated with the key

    @usage: (recommended) 

    <code> 
    MI6_employee_record = ShelfStorage('depo')
    try:
        MI6_employee_record.write('James Bond', '007')
        MI6_employee_record.read('James Bond')
    except StorageException:
        print 'For British Eyes ONLY!' 
    </code>

    Expect: '007'
    '''
    def read(self, key):
        storage = shelve.open(self.__file_name)
        if not key in storage:
            raise StorageException(key, 'The data you tried to\
            retrieve is not contained in the storage.')
        return_value = storage[key]
        storage.close()
        return return_value;

    '''
    contains - query whether or not a particular key is in storage

    @params key: the key in the key/value pair to test
    
    @returns: true if the key is in there, false if not

    @usage: 

    <code> 
    MI6_employee_record = ShelfStorage('depo')
    MI6_employee_record.write('James Bond', '007')

    if MI6_employee_record.contains('James Bond')
        print 'Groovy'
    </code>

    Expect: 'Groovy'
    '''
    def contains(self, key):
        storage = shelve.open(self.__file_name)
        is_key_in_storage = key in storage
        storage.close()
        return is_key_in_storage

    '''
    write - write a key/value pair to the storage

    @params key: the key in the key/value pair

    @params value: the value in the key/value pair to store
    
    @throws StorageException: whenever there is an exception
       associated with I/O of the shelf.

    @usage: 

    <code> 
    MI6_employee_record = ShelfStorage('depo')
    try:
        MI6_employee_record.write('James Bond', '007')
    except StorageException as storage_exception:
        print 'He is a bigger man than this tiny island nation'
    </code>
    '''
    def write(self, key, value):
        try:
            storage = shelve.open(self.__file_name)
            storage[key] = value
            storage.close()
        except Exception as storage_error:
            raise StorageException(key, 'An error occurred while\
            writing to the shelf. Error exception is:\n\
            type:' + type(storage_error) + '\n\
            message:' + storage_error + '\n')
