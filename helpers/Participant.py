# participant data model
class Participant(object):

    def __init__(self, name: str, swim: float, bike: float, run: float):
        self._name = name.title()
        self._swim = swim
        self._bike = bike
        self._run = run
        self._swim_rank = 0
        self._bike_rank = 0
        self._run_rank = 0

    def __str__(self):
        return """\
        <Participant
            name={},
            swim={},
            bike={},
            run={},
            swim_rank={},
            bike_rank={},
            run_rank={},
            sum={}
        >
        """.format(
            self.name(),
            self.swim(),
            self.bike(),
            self.run(),
            self.swim_rank(),
            self.bike_rank(),
            self.run_rank(),
            self.sum()
        )

    def name(self):
        return self._name

    def swim(self):
        return self._swim

    def bike(self):
        return self._bike

    def run(self):
        return self._run

    def swim_rank(self):
        return self._swim_rank

    def bike_rank(self):
        return self._bike_rank

    def run_rank(self):
        return self._run_rank

    def set_swim_rank(self, rank: int):
        self._swim_rank = rank

    def set_bike_rank(self, rank: int):
        self._bike_rank = rank

    def set_run_rank(self, rank: int):
        self._run_rank = rank
        
    def sum(self):
        return self.swim_rank() + self.bike_rank() + self.run_rank()

