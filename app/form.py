
def run(web):
    headers = [(k,v) for k,v in web['headers'].items()]

    result = "HEADERS: %r\nPARAMS: %r\nPATH: %r\nMETHOD: %r" % (
        headers, web['params'], web['path'], web['method'])

    return result, 200, {'content-type': 'text/plain'}


