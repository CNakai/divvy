def extract_student_id(bblearn_filename):
    front = bblearn_filename.split(sep='_attempt_', maxsplit=2)[0]
    return front[front.rindex('_') + 1:]


def remove_bblearn_prefix(bblearn_filename):
    back = bblearn_filename.split(sep='_attempt_', maxsplit=2)[1]
    return back[back.find('_') + 1:]
