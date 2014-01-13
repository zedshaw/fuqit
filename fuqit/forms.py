from fuqit.web import RequestDict

def read(web, **expected):
    results = web.params.copy()

    for key, value in expected.items():
        if key in results:
            try:
                if isinstance(value, int):
                    results[key] = int(results[key])
                elif isinstance(value, float):
                    results[key] = float(results[key])
                elif isinstance(value, bool):
                    results[key] = bool(results[key])
                else:
                    results[key] = results[key]
            except ValueError:
                # TODO: log these since they might matter
                results[key] = value
        else:
            results[key] = value

    return RequestDict(results)
