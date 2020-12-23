def extract_student_id(bblearn_filename):
    front = bblearn_filename.split(sep='_attempt_', maxsplit=2)[0]
    return front[front.rindex('_') + 1:]
