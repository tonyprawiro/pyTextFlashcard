import sys
import os
import random
import time
import pprint

# Settings
iPassPercentage = 70
iMaxQuestionLength = 50
iMaxQuestionDuration = 300
bShowOriginalQuestionNumber = False

# Command line arguments
try:
	sFlashcardsName = sys.argv[1]
except:
	print "Usage: flashcards-engine.py QuizName"
	print "E.g.: flashcards-engine.py HISTORICALFIGURES"
	sys.exit(1)

# Check for file existence

sFlashcardsFile = "%s-FLASHCARDS.txt" % (sFlashcardsName)

if not os.path.isfile(sFlashcardsFile):
	print "Error: Make sure %s exist in the same directory" % (sFlashcardsFile)
	sys.exit(1)

# Parse flashcards

aSections = {}
aCards = []
aCardsShuffler = []
sCurrentSection = ""
bInACard = False
iCurrentCardState = 1 # 0 = N/A, 1 = keyword, 2 = definitions
aCurrentCard = {}
iCardNumber = 0
with open(sFlashcardsFile) as fCards:
	for line in fCards:
		line = line.strip()
		if line[:1] == "[" and line[-1:] == "]":
			sCurrentSection = line[1:-1]
			temp = {}
			temp["Correct"] = 0
			temp["Incorrect"] = 0
			temp["Percentage"] = 0
			aSections[sCurrentSection] = temp
		elif line == "---":
			if bInACard == False:
				iCurrentCardState = 1
				bInACard = True
				aCurrentCard = {}
				aCurrentCard["Keywords"] = []
				aCurrentCard["Definitions"] = []
				aCurrentCard["Section"] = sCurrentSection
			else:
				aCards.append(aCurrentCard)
				aCurrentCard = {}
				iCurrentCardState = 0
				bInACard = False
				aCardsShuffler.append(iCardNumber)
				iCardNumber += 1
		elif line == "|" and bInACard and iCurrentCardState == 1:
			iCurrentCardState = 2
		elif bInACard:
			if iCurrentCardState == 1:
				aCurrentCard["Keywords"].append(line)
			elif iCurrentCardState == 2:
				aCurrentCard["Definitions"].append(line)
		else:
			pass # Not in a card, not a definition and not a card separator

# Start the session

iCorrect = 0
iIncorrect = 0
bStop = False

while True: # Keep looping until user stops

	# Shuffle the card
	random.shuffle(aCardsShuffler)

	if bStop:
		break

	for iCardIdx in aCardsShuffler:

		os.system('clear')

		if bStop:
			break

		# Show keyword (1) or show definition (2) ?
		iMode = random.randint(1,2)
		if iMode==1:
			sModeShow = "Keywords"
		elif iMode==2:
			sModeShow = "Definitions"
		iModeIndex = random.randint(0, len(aCards[iCardIdx][sModeShow])-1)
		sToShow = aCards[iCardIdx][sModeShow][iModeIndex]

		print "What is...\n"
		print sToShow
		print

		sMyAns = raw_input("Press Enter to reveal... ")
		print

		os.system('clear')

		print "Keywords:\n"
		print "\nor\n".join(aCards[iCardIdx]["Keywords"])
		print "\nDefinitions:\n"
		print "\nor\n".join(aCards[iCardIdx]["Definitions"])

		print "\n"
		print "Enter 1 if you guessed correctly"
		print "   or 0 if you don't know or if you guessed incorrectly"
		print "   or Q to abort and start assessment"
		while True:
			sMyAns = raw_input("> ")
			if len(sMyAns) > 0:
				break
		sMyAns = sMyAns.upper()

		if sMyAns == "Q":
			bStop = True
		elif sMyAns == "1":
			iCorrect += 1
			aSections[aCards[iCardIdx]["Section"]]["Correct"] += 1
		else:
			iIncorrect += 1
			aSections[aCards[iCardIdx]["Section"]]["Incorrect"] += 1

# Assessment
iAllTotal = iCorrect + iIncorrect
if iAllTotal == 0:
	iAllPercentage = 0
else:
	iAllPercentage = iCorrect * 100 / iAllTotal

print "Date/time: %s" % (time.strftime("%Y-%m-%d %H:%M"))
print "Correct: %.1f%%" % (iAllPercentage)

sAssessmentFilename = "%s-ASSESSMENT-%s.txt" % (sFlashcardsName, time.strftime("%Y%m%d-%H%M"))

with open(sAssessmentFilename, 'w') as f:
	f.write("Date/time: %s\n" % (time.strftime("%Y-%m-%d %H:%M")))
	f.write("Correct: %.1f%%" % (iAllPercentage))
	f.write("\n\n")

	for aSectionName, aSectionData in aSections.iteritems():
		f.write("\n")
		f.write("[%s]\n" % (aSectionName))
		iTotal = aSectionData["Correct"] + aSectionData["Incorrect"]
		if iTotal == 0:
			f.write("N/A (no answers)\n")
		else:
			f.write("Correct: %d\n" % (aSectionData["Correct"]))
			f.write("Incorrect: %d\n" % (aSectionData["Incorrect"]))
			fPercentage = aSectionData["Correct"] * 100 / iTotal
			f.write("Percentage: %.1f%%\n" % ( fPercentage ))
	f.close()

print "Details have been saved to %s" % (sAssessmentFilename)
