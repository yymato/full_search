def selection_size(toponym):
    toponym_dictionary_size = toponym['boundedBy']['Envelope']
    delta_x = float(toponym_dictionary_size['upperCorner'].split()[0]) - float(
        toponym_dictionary_size['lowerCorner'].split()[0])
    delta_y = float(toponym_dictionary_size['upperCorner'].split()[1]) - float(
        toponym_dictionary_size['lowerCorner'].split()[1])

    return ",".join(map(str, (delta_x, delta_y)))