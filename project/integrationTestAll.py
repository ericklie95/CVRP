# Required for Approximate Algorithm
from reading_file import Read_File
from approximateAlgorithm import approximateAlgorithm

# Required for heuristic algorithm
from project import data_input, util
from project.solvers import clarke_wright

import os
import signal
import subprocess

print "******* Integration testing of all algorithm *******"
print "------- This is to test all the algorithms is one file. This is the pre-test before the creation of GUI class -------"

print "\n### Using filename input/eil23.vrp ###"
fn = "eil23.vrp"

print "=== Running approximation algorithm ==="
firstAlg = approximateAlgorithm()
rf = Read_File('input/'+fn)
routelist = firstAlg.solve(rf)
print '''- Expected: (List of list of type String)
[['1','13','12'],
['1','8','9','5','6','22','19','20','21','23','18','15','17','16','4','3','2','7'],
['1','10'],
['1','14','11']]
'''
print '- Result: '
print routelist
print "=== Finish testing approximateAlgorithm() ===\n"

print "=== Testing heuristic algorithm from library ==="
alg = clarke_wright.ClarkeWrightSolver()
data = data_input.read_file('input/'+fn)
solution = alg.solve(data)

routelist = []
gen = util.print_solution(solution)
for i in gen:
	tmpList = []
	tmpList.append(int(data.depot().name()))
	for j in i:
		tmpList.append(int(j.name()))
	routelist.append(tmpList)
print '''- Expected: (List of list of type int)
[[1,8,10,6,5,9,22],
[1,14,11],
[1,19,20,21,23,18,15,17,16,4,3,2,7,12,13]]
'''
print '- Result: '
print routelist

print "=== Finish testing heuristic algorithm ===\n"


print "=== Testing Symphony ==="
print "## For testing Symphony, we will need to make 3 functions. ##"
print "# The first function is called sendToTerminal with param int and String, the purpose of this function is to call the program via terminal as it can only be executed through its exectable file and the param is required for the argv for the executable program. Returned value from this function would be an object of class File and String. #"
print "# The second function is called checkIsFeasible with param File, float and int. The purpose is to check if the given input has feasible solution or not. The returned value from this function would be String which is the solution and floating point for time in secods. #"
print "# The third function is called makeRouteList with param string, integer and data_input. The purpose is to make a list of route which will be represented as type list of list with integer as the element of each. This is important as to make a generalization of the route representation to be shown in GUI later. The returned value from this function is a list of list of type int.#"

def sendToTerminal(vehicleNum, fn):

	# Try to check vehicle number if it's a number or not.
	try:
		i = int(vehicleNum)
	except:
		return 0,0

	# Remove file if exists
	try:
		os.remove('output/'+fn+"-solution")
	except:
		pass

	# Name of the new file
	solutionFile = 'output/'+str(fn)+"-thirdAlg-solution"
	f = open(solutionFile,'w+')
	words = '~/Desktop/FIT3036_Ubuntu/SYMPHONY-5.6/SYMPHONY/Applications/VRP/vrp -F '+str('input/'+fn)+' -N '+ str(vehicleNum)

	# Call out to terminal
	import subprocess
	callToTerminal = subprocess.call(words, stdout=f, shell=True, preexec_fn=os.setsid)

	# cloe the write plus file.
	f.close()

	# Open to read file
	f = open(solutionFile,'r')

	# REturn the opened file and the filename.
	return f, solutionFile

def checkFileIsFeasible(f, time, distance):
	returnSolution = []
	routeFlag = False
	optimalFlag = False
	time = ""
	for line in f:
		if "Total Wallclock Time" in line:
			words = line.split()
			time = words[len(words)-1]
			time = float(time)
		# This if-else condition is to find OPTIMAL / INFEASIBLE solution.
		if not optimalFlag:		
			if 'Infeasible' in line:
				f.close()
				return "Infeasible",time #yes it's infeasible
			elif 'Optimal' in line:
				optimalFlag = True
		else:
			if routeFlag:
				if line != "\n":
					returnSolution.append(line)
			elif "Solution Cost" in line:
				words = line.split()
				distance = float(words[len(words)-1])
				routeFlag = True


	f.close()
	return returnSolution,time #no, it's feasible


def makeRouteList(routeStr,vehicleNum,data):
	routeList = []
	for i in routeStr:
		tmpList = []
		
		for j in i.split():
			try:
				if j == "0":
					j = 0
					tmpList.append(1)
				else:
					tmpList.append(int(j)+1)
			except:
				continue
		# If vehicle is more than 0, Route will be shown, depot won't be inserted.
		if "Route" in routeStr[0]:
			tmpList.insert(0,int(data.depot().name()))
			routeList.append(tmpList)

		else:
			# If vehicle is 1, the depot is inserted automatically.
			# We use append to make it LOL, requirement for plotLine
			routeList.extend(tmpList)

	if vehicleNum == "1":
		routeList = [routeList]

	return routeList

vehicleNum = 1
routeInStr = "Infeasible"
time = 0.0
distance = 0

# If it's not feasible
while routeInStr == "Infeasible":	
	vehicleNum += 1
	solutionF, fileString = sendToTerminal(vehicleNum, fn)	
	routeInStr, time = checkFileIsFeasible(solutionF, time, distance)

data = data_input.read_file('input/'+fn)
routelist = makeRouteList(routeInStr,vehicleNum,data)
print '''First of all, we will need a loop to find the minimum number of vehicle.
This is done by executing below code:
------
1 while routeInStr == "Infeasible":	
2 	vehicleNum += 1
3	solutionF, fileString = sendToTerminal(vehicleNum, fn)	
4	routeInStr, time = checkFileIsFeasible(solutionF, time, distance)
------
Line number 1 is to check if file has feasible solution or not. The value of routeInStr is "Infeasible" initially as to make the loop works.
Line number 2 is to increase the number of vehicle by one each loop. The initial value is 1. The reason is because all the problem can be solved by using 1 vehicle but the result may not be as desired. The option to choose the vehicle number will be provided later in the GUI.
Line number 3 is used to execute the executable file and where the output file would be located.
Line number 4 is used to read the output file of line 3 and the time as well.
Note that the loop will be broken if the file is feasible. Otherwise it will go over and over again.
-Expected: (List of list of type int)
[[1, 8, 10, 9, 6, 5, 22],
[1, 11, 14],
[1, 13, 12, 7, 2, 3, 4, 17, 16, 15, 18, 23, 21, 20, 19]]
'''
print '- Result: '
print routelist

print "=== Finish testing Symphony ==="
print "\n******* Finish integration testing of all algorithm *******"
