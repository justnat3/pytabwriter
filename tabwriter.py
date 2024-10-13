"""
  author:  Nathan Reed <nreed@linux.com>
  desc:    A reduced buffered tabwriter implmentation
  date:    10/08/24
"""

SEGMENT_ESCAPE_CHARACTERS = ["\t", "\n"]
ILLEGAL_SEGMENT_CHARACTERS = ["\v", "\f", "\r"]

class _Cell:
    """A cell represents a segment of a line without the segment seperator"""
    def __init__(self, width=0):
        """
        Args:
            width (int): the width of the segement in the line
        """
        self.width: int = width

    def __str__(self):
        return f"({self.width})"

class TabWriter:
    """A tab writer is more or less a buffered table writer"""
    def __init__(self, sep: str):
        """
        Args:
            sep (str): a seperator to use between columns
        """
        self.sep = sep
        # to store the entire output in memory, without newlines and without seperators
        self.output = ""
        self.buff = ""

        # some state tracking
        # current incomplete segment of text to seperate in a line
        self.cell = _Cell()
        self.lines: list[list[_Cell]] = []  # lines include a bunch of cells
        self.widths = []

    def _reset(self):
        """resets the state of the tab writter"""

        self.cell = _Cell()
        self.lines = []
        self.output = ""
        self.buff = ""

    def _add_line(self):
        """add a line"""
        self.lines.append([])

    def _print_state(self):
        """KEEP: a debugging function
        """
        for i, line in enumerate(self.lines):
            print("line:", i)
            for j, cell in enumerate(line):
                print("cell:", j, "width:", cell.width)

    def _terminate_cell(self):
        """terminates a cell inside of a line """
        self.output += self.buff
        self.cell.width = len(self.buff)
        self.lines[-1].append(self.cell)
        self.cell = _Cell(0)
        self.buff = ""

    def writeln(self, s: str):
        """writes a line to the internal state of the tabwriter

        Args:
            s (str): the line to insert into the tabwriter buffer
        """
        # start with a line
        self._add_line()

        for i, char in enumerate(s):
            if char in SEGMENT_ESCAPE_CHARACTERS:
                self._terminate_cell()
                continue

            if char in ILLEGAL_SEGMENT_CHARACTERS:
                raise ValueError("illegal character given: "+str(hex(ord(char))))

            self.buff += char
            if i >= len(s)-1:
                self._terminate_cell()

        # self.print_state()

    def flush(self):
        """should be called last, as this dumps the context of the tabwriter
        """
        # find the max widths
        for line in self.lines:
            for i, cell in enumerate(line):

                if i >= len(self.widths):
                    self.widths.append(0)

                if self.widths[i] < cell.width:
                    self.widths[i] = cell.width

        pos = 0
        pad = 0

        # format and print
        for lidx, line in enumerate(self.lines):
            # dont line feed on an already empty line
            if lidx != 0:
                print() # empty

            # for all the cells in a line, print the line and determine its
            # width, based on the width of the cell
            for i, cell in enumerate(line):
                print(self.sep, " ", end="")

                for _ in range(cell.width):
                    print(self.output[pos], end="")
                    pos += 1

                pad = self.widths[i] - cell.width

                while pad > 0:
                    print(" ", end="")
                    pad -= 1

                print(" ", end="")

                if i >= len(line)-1:
                    print(self.sep, " ", end="")
        print()

        # reset the state of the tab writer
        self._reset()


# KEEP: used to test the tabwriter
def _test():
    wr = TabWriter("")
    wr.writeln("Name\tAge\tDescription")
    wr.writeln("nate\t24\tsome type of programmer laksjdlfkj")
    wr.writeln("emily\t25\tHR Representative")
    wr.flush()
