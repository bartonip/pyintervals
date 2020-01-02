from datetime import datetime, date

DATE = "DATE"
DATETIME = "DATETIME"

class IncorrectType(Exception):
    pass

class IntervalLengthCannotBeZero(Exception):
    pass

class InverseInterval(Exception):
    pass

class Interval(object):
    def __init__(self, start, end):
        if isinstance(start, date) and isinstance(end, date):
            self.mode = "DATE"
        elif isinstance(start, datetime) and isinstance(end, datetime):
            self.mode = "DATETIME"
        else:
            raise IncorrectType("Both start and end of interval must be same date/datetime type.")

        if start == end:
            raise IntervalLengthCannotBeZero("Length of interval cannot be zero.")

        if start > end:
            raise InverseInterval("Start of interval must be before end of interval.")

        self.start = start
        self.end = end
        
    def preceeds(self, other):
        """
        Symbol: p
        Boolean Expression: 

        This interval is before the other interval.

        """
        return (self.start < self.end < other.start)
    
    def meets(self, other):
        """
        Symbol: m
        Boolean Expression:  

        This interval starts before the interval and ends at the start of
        the other interval.

        """
        return (self.start < self.end == other.start)

    def overlaps(self, other):
        """
        Symbol: o
        Boolean Expression: 

        This interval overlaps the other interval.

        """
        return (self.start <= other.end and other.start <= self.end)

    def finished_by(self, other):
        """
        Symbol: F
        Boolean Expression: 

        This interval ends at the same time as the other interval.

        """
        return (self.start <= other.start and self.end == other.end)

    def contains(self, other):
        """
        Symbol: d
        Boolean Expression: 

        This interval starts before and ends after the other interval.

        """
        return (self.start <= other.start and self.end >= other.end)
    
    def starts(self, other):
        """
        Symbol: s
        Boolean Expression: 

        This interval starts at the same time as the other interval starts and ends 
        before the other interval ends.

        """
        return (self.start == other.start and self.end <= other.start)

    def equals(self, other):
        """
        Symbol: e
        Boolean Expression: 

        This interval is identical to the other interval.

        """
        return (self.start == other.start and self.end == other.end)

    def started_by(self, other):
        """
        Symbol: S
        Boolean Expression: 

        This interval starts when the other interval starts and ends after the 
        other interval ends.

        """
        return (self.start == other.start and self.end >= other.end)

    def during(self, other):
        """
        Symbol: d
        Boolean Expression: 

        This interval starts after the other interval starts and ends before
        the other interval ends.

        """
        return (self.start >= other.start and self.end <= other.end)

    def finishes(self, other):
        """
        Symbol: f
        Boolean Expression: 

        This interval starts after the other interval starts and ends when the other
        interval finishes.

        """
        return (self.start <= self.end == other.end)
    
    def overlapped_by(self, other):
        """
        Symbol: O
        Boolean Expression: 

        This interval starts after the other interval starts but before the other interval
        ends, and ends after the other interval ends.

        """
        return (other.start <= self.start <= other.end and self.end >= other.start)

    def met_by(self, other):
        """
        Symbol: M
        Boolean Expression: 

        This interval starts when the other interval ends.

        """
        return (other.end == self.start and self.end > other.end)

    def preceded_by(self, other):
        """
        Symbol: P
        Boolean Expression: 

        The interval starts after the other interval ends.

        """
        return (other.end < self.start)

    # Operations
    def intersection(self, other):
        """
        Returns the intersection of this interval and the other interval.
        """
        if self.overlaps(other) and not (self.meets(other) or self.met_by(other)):
            return Interval(max(self.start, other.start), min(self.end, other.end))
        else:
            return None

    def union(self, other):
        """
        Returns the union of this interval and the other interval.
        """
        return Interval(min(self.start, other.start), min(self.end, other.end))

    def subtract(self, other):
        """
        Returns and interval with the other interval subtracted from this interval.
        """
        if self.overlaps(other):
            start_datetime = self.start
            end_datetime = other.start
        elif self.overlapped_by(other):
            start_datetime = 2

            return Interval()

    # Computed Properties
    @property
    def duration(self):
        return (self.end - self.start)

    @property
    def seconds(self):
        return self.duration.total_seconds()

    # Python Operators
    def __lt__(self, other):
        return self.preceeds(other)

    def __gt__(self, other):
        return self.exceeds(other)

    def __le__(self, other):
        return self.preceeds(other) or self.meets(other)
    
    def __ge__(self, other):
        return self.exceeds(other) or self.met_by(other)

    def __eq__(self, other):
        return self.equals(other)
    
    def __ne__(self, other):
        return not self.equals(other)

    def __and__(self, other):
        return self.intersection(other)
    
    def __or__(self, other):
        return self.union(other)
    
    def __str__(self):
        return "<Interval: Start: {}, End: {}>".format(self.start.isoformat(), self.end.isoformat())
    
    def __repr__(self):
        return "<Interval: Start: {}, End: {}>".format(self.start.isoformat(), self.end.isoformat())
