# Data_Structures
# DQ

from abc import ABC, abstractmethod

####################################################
# abstract base class
# defines methods a 'Data_Structure' class must have
####################################################
class Data_Structure(ABC):

    @property
    @abstractmethod
    def is_full(self):
        pass

    @property
    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def items(self):
        pass

    @abstractmethod
    def _add_items(self, *args):
        pass

    @abstractmethod
    def _retrieve_item(self):
        pass

class Circular_Queue(Data_Structure):
    __MAX_SIZE = 5
    
    def __init__(self):
        self.__items = [None for _ in range(Circular_Queue.__MAX_SIZE)]
        self.__front_pointer = 0
        self.__rear_pointer = 0 
        self.__size = 0
        self.__is_circled = False

    @property
    def items(self):
        if self.__is_circled:
            items = self.__items[self.__front_pointer:]
            items += self.__items[:self.__rear_pointer]
            return items
        return self.__items[self.__front_pointer:self.__rear_pointer]

    @property 
    def is_full(self):
        return self.__size == Circular_Queue.__MAX_SIZE
    
    @property
    def is_empty(self):
        return self.__size == 0

    def enqueue(self, items, multiple_values=False):
        if isinstance(multiple_values, bool):
            self._add_items(items, multiple_values)

    #################################################################################
    # add items to the queue
    # if multiple_values == True, recursively (tail recursion) add each item to queue
    # unless/until queue is full
    # increases size by 1
    # changes value of rear pointer (see def __circle)
    #################################################################################
    def _add_items(self, items, multiple_values):
        if not self.is_full and ((items and not multiple_values) or (len(items) and multiple_values)):
            if not multiple_values:
                self.__items[self.__rear_pointer] = items
                self.__rear_pointer += 1
                self.__rear_pointer = self.__circle_pointer(self.__rear_pointer)
                self.__size += 1
            else:
                self._add_items(items[0], False)
                if items[1:]:
                    self._add_items(items[1:], True)
                
    def dequeue(self):
        return self._retrieve_item()
    
    ###################################################
    # returns first item in the queue
    # only runs if queue is not empty
    # decreases size by 1
    # changes value of front pointer (see def __circle)
    ###################################################
    def _retrieve_item(self):
        if not self.is_empty:
            self.__front_pointer += 1
            self.__front_pointer = self.__circle_pointer(self.__front_pointer)
            self.__size -= 1
            return self.__items[self.__front_pointer - 1]

    ########################################################################
    # if the pointer refers to an index that cannot be accessed by the queue
    # let the value of the pointer equal 0
    ########################################################################
    def __circle_pointer(self, pointer):
        if pointer == self.__MAX_SIZE:
            pointer = 0
            self.__is_circled = not self.__is_circled
        return pointer

class Stack(Data_Structure):
    __MAX_SIZE = 6

    def __init__(self):
        self.__items = [None for i in range(Stack.__MAX_SIZE)]
        self.__tos = 0
        self.__size = 0

    @property
    def items(self):
        return self.__items[:self.__tos]

    @property
    def is_full(self):
        return self.__size == self.__MAX_SIZE

    @property
    def is_empty(self):
        return not self.__size

    def push(self, item):
        self._add_items(item)

    def _add_items(self, item):
        if not self.is_full:
            self.__items[self.__tos] = item
            self.__tos += 1
            self.__size += 1

    def pop(self):
        return self._retrieve_item()
    
    def _retrieve_item(self):
        if not self.is_empty:
            item = self.__items[self.__tos -1]
            self.__size -= 1
            self.__tos -= 1
        return item
    
    def peek(self):
        if not self.is_empty:
            return self.__items[self.__tos -1]
    
    def peek_2(self):
        if self.__size >= 2:
            return self.__items[self.__tos -2:self.__tos]
