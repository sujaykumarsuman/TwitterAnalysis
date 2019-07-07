def percentage(part, whole):
    return 100 * float(part)/float(whole)


def check_poll(sen):
    if sen == 0.0:
        return 'Neutral'
    elif sen > 0.0:
        return 'Positive'
    else:
        return 'Negative'
