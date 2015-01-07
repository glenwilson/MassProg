from storage_exception import StorageException

'''
@note: shelve may raise runtime exceptions, too.
'''
class MemStorage:
    def __init__(self):
        self.__mem_storage = {}
    
    '''
    iterator - for iterating over a ShelfStorage object

    @returns (on each iteration) a key/value pair of the form
    { 'key': key, 'value': value }. For example, if ( 'Sq4' : Sq4Obj )
    was a key-value pair in the storage, then on one iteration, it will
    return { 'key' : 'Sq4', 'value': Sq4Obj }.

    @usage (recommended)

    <code>
    MI6_employee_record = MemStorage
    MI6_employee_record.write('James Bond', 007)
    MI6_employee_record.write('Alec Trevelyan', 006)
    MI6_employee_record.write('Judi Dench', 'M')
    for pair in MI6_employee_record:
        print(pair['key'])
	print(pair['value'])
    </code>

    Expects: 
    James Bond
    007
    Alec Trevelyan
    006
    Judi Dench
    M
    '''
    def __iter__(self): 
       self.__iterator = self.__mem_storage.__iter__()
       return self

    def next(self):
       next_key = self.__mem_storage.next()
       return { 'key': next_key, 'value': self.__mem_storage[next_key] }

    '''
    copy - copies another storage into this one.

    @params external_storage: another data storage that implements
       an iterator 

    @throws StorageException: raised when an exception is raised
       at any stage in the iteration process.

    @usage: (recommended) 

    <code> 
    MI6_employee_record = MemStorage
    MI5_employee_record = SomeOtherStorage( params )

    try:
        MI6_employee_record.copy(MI5_employee_record)
    except StorageException:
        print 'These are two different agencies!'
    </code>
    '''
    def copy(self, external_storage):
        try:
            for pair in external_storage:
                key = pair['key']
                value = pair['value']
                self.__mem_storage[key] = value
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
    try:
	MI6_employee_record = MemStorage
        MI6_employee_record.write('James Bond', 007)
        MI6_employee_record.read('James Bond')
    except StorageException:
        print 'For British Eyes ONLY!' 
    </code>

    Expect: 007
    '''
    def read(self, key):
        if not key in self.__mem_storage:
            raise StorageException(key, 'The data you tried to\
            retrieve is not contained in the storage.')
        return self.__mem_storage[key]

    '''
    contains - query whether or not a particular key is in storage

    @params key: the key in the key/value pair to test
    
    @returns: true if the key is in there, false if not

    @usage: 

    <code> 
    MI6_employee_record = MemStorage
    MI6_employee_record.write('James Bond', '007')

    if MI6_employee_record.contains('James Bond')
        print 'Groovy'
    </code>

    Expect: 'Groovy'
    '''
    def contains(self, key):
        return key in self.__mem_storage

    '''
    write - write a key/value pair to the storage

    @params key: the key in the key/value pair

    @params value: the value in the key/value pair to store
    
    @usage: 

    <code> 
	MI6_employee_record = MemStorage
	MI6_employee_record.write('James Bond', '007')
    </code>
    '''
    def write(self, key, value):
	self.__mem_storage[key] = value
