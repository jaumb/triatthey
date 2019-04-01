#!/usr/bin/env python

import csv
import sys
import os

NAME='name'
SWIM='swim'
BIKE='bike'
RUN='run'
SWIM_RANK='swim rank'
BIKE_RANK='bike rank'
RUN_RANK='run rank'
SUM='sum'
OUTPUT_SUFFIX='_processed'


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


# Override DictReader fieldnames to strip leading/trailing whitespace from field names
class DictReaderStrip(csv.DictReader):
    @property
    def fieldnames(self):
        if self._fieldnames is None:
            csv.DictReader.fieldnames.fget(self)
            if self._fieldnames is not None:
                self._fieldnames = [name.strip() for name in self._fieldnames]
                self._fieldnames = [name.lower() for name in self._fieldnames]
        return self._fieldnames


# common function to format output file name
def get_output_name(filename: str):
    return filename.rstrip('.csv') + OUTPUT_SUFFIX + '.csv'


# calculate each participant's rank for each event
def calculate_ranks(participants: list):
    # calculate swim rank
    participants.sort(key=lambda p: p.swim(), reverse=True)
    for i in range(len(participants)):
        participants[i].set_swim_rank(i + 1)

    # calculate bike rank
    participants.sort(key=lambda p: p.bike(), reverse=True)
    for i in range(len(participants)):
        participants[i].set_bike_rank(i + 1)

    # calculate run rank
    participants.sort(key=lambda p: p.run(), reverse=True)
    for i in range(len(participants)):
        participants[i].set_run_rank(i + 1)


# write results to a csv file with output suffix
def write_results(filename: str, participants: list):
    # sort by name
    participants.sort(key=lambda p: p.name())
    with open(get_output_name(filename), 'w', newline='') as csvfile:
        fieldnames = [NAME,SWIM,BIKE,RUN,SWIM_RANK,BIKE_RANK,RUN_RANK,SUM]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for p in participants:
            row = {}
            row[NAME] = p.name()
            row[SWIM] = p.swim()
            row[BIKE] = p.bike()
            row[RUN] = p.run()
            row[SWIM_RANK] = p.swim_rank()
            row[BIKE_RANK] = p.bike_rank()
            row[RUN_RANK] = p.run_rank()
            row[SUM] = p.sum()
            writer.writerow(row)


# open's the csv file and controls the overall processing flow
def process_results(filename: str):
    with open(filename, newline='') as csvfile:
        csvreader = DictReaderStrip(csvfile, dialect='excel')
        participants = []
        for row in csvreader:
            participants.append(Participant(row[NAME], float(row[SWIM]), float(row[BIKE]), float(row[RUN])))

    calculate_ranks(participants)
    write_results(filename, participants)


# do some basic sanity checks and report the output file name
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:",sys.argv[0],"<path-to-csv>")
        exit(1)

    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print("File",filename,"does not exist.")
        exit(1)

    process_results(filename)
    print("Results saved as",get_output_name(filename))
