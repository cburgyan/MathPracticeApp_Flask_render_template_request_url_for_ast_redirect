


class StatsRecord(dict):

    def __init__(self):
        super().__init__()
        self = {'correct': 0, 'wrong': 0, 'percent-correct': 0, 'total-time': 0, 'average-time / problem': 0,
         'average-time / correct-answer': 0, 'total-time-for-only-correct-answers': 0,
         'average-correct-answer-time / correct-answer': 0}
