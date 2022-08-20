# high level intergration
# 1. get user input and check for ambiguity -- input_and_ambiguity_check, get an ambiguity level
# 2. logic to check ambiguity level, and determine if the robot needs to disambiguate -- in this file
#   2(a): disambiguation needed: -- call attention check to get human attention
#       (I): disambigute via pointing and checking head gesture
#       (II): pick and place
#   2(b): disambiguation not needed: call pick and place

# use subporcess.check_output?
# run different py files in seperate threads?
# import module and use the imported variable directly?
    #e.g. in first.py a=5. in the second py, do import first, print(first.a)

import input_and_ambiguity_check

while True:
    print(input_and_ambiguity_check.userCMD)
