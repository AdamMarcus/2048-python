import grading
import imp
import optparse
import os
import re
import sys
import projectParams
import random
random.seed(0)
try:
    from pacman import GameState
except:
    pass

# register arguments and set default values
def readCommand(argv):
    parser = optparse.OptionParser(
        description='Run public tests on student code')
    parser.set_defaults(generateSolutions=False, edxOutput=False, gsOutput=False,
                        muteOutput=False, printTestCase=False, noGraphics=False)
    parser.add_option('--test-directory',
                      dest='testRoot',
                      default='test_cases',
                      help='Root test directory which contains subdirectories corresponding to each question')
    parser.add_option('--student-code',
                      dest='studentCode',
                      default=projectParams.STUDENT_CODE_DEFAULT,
                      help='comma separated list of student code files')
    parser.add_option('--code-directory',
                      dest='codeRoot',
                      default="",
                      help='Root directory containing the student and testClass code')
    parser.add_option('--test-case-code',
                      dest='testCaseCode',
                      default=projectParams.PROJECT_TEST_CLASSES,
                      help='class containing testClass classes for this project')
    parser.add_option('--generate-solutions',
                      dest='generateSolutions',
                      action='store_true',
                      help='Write solutions generated to .solution file')
    parser.add_option('--edx-output',
                      dest='edxOutput',
                      action='store_true',
                      help='Generate edX output files')
    parser.add_option('--gradescope-output',
                      dest='gsOutput',
                      action='store_true',
                      help='Generate GradeScope output files')
    parser.add_option('--mute',
                      dest='muteOutput',
                      action='store_true',
                      help='Mute output from executing tests')
    parser.add_option('--print-tests', '-p',
                      dest='printTestCase',
                      action='store_true',
                      help='Print each test case before running them.')
    parser.add_option('--test', '-t',
                      dest='runTest',
                      default=None,
                      help='Run one particular test.  Relative to test root.')
    parser.add_option('--question', '-q',
                      dest='gradeQuestion',
                      default=None,
                      help='Grade one particular question.')
    parser.add_option('--no-graphics',
                      dest='noGraphics',
                      action='store_true',
                      help='No graphics display for pacman games.')
    (options, args) = parser.parse_args(argv)
    return options