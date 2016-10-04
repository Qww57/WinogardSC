import pickle


def save(object_to_save, object_name):
    """
    Serialize an object as *.pickle.
    :param object_to_save: object that should be saved
    :param object_name: name for the saved object
    :return:
    """
    try:
        name = object_name + '.pickle'
        f = open(name, 'wb')
        pickle.dump(object_to_save, f)
        f.close()
        return True
    except Exception as e:
        print(e.with_traceback())
        return False


def load(object_name):
    """
    Load a *.pickle object as an object
    :param object_name: name of the saved object
    :return: saved object if any, None if none
    """
    try:
        name = object_name + '.pickle'
        f = open(name, 'rb')
        saved_object = pickle.load(f)
        f.close()
        return saved_object
    except Exception as e:
        print(e.with_traceback())
        return None
