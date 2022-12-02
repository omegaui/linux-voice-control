from array import array


def trim(frames):
    """Trim the blank spots at the start and end"""

    def _trim(dataframe):
        snd_started = False
        r = array('h')

        for i in dataframe:
            if not snd_started and abs(i) > 500:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    frames = _trim(frames)

    # Trim to the right
    frames.reverse()
    frames = _trim(frames)
    frames.reverse()
    return frames
