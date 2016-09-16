import pickle


class Serializer:

    """
    Class using the library pickle in order to serialize objects.
    """

    def save(object, object_name):
        name = object_name + '.pickle'
        f = open(name, 'wb')
        pickle.dump(object, f)
        f.close()

    def load(object_name):
        name = object_name + '.pickle'
        f = open(name, 'rb')
        classifier = pickle.load(f)
        f.close()
        return classifier
