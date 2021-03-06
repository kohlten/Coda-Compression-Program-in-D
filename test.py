import subprocess
import os
import sys
import time
import logging

def findAllFiles(startdir):
	everthing = [x for x in os.walk(startdir)]
	files = []
	for tup in everthing:
		path = tup[0]
		for file in tup[2]:
			if ".lock" not in file:
				files.append(path + "/" + file)
	return files

def clean():
	subprocess.call(["rm", "-rf", "bin"])
	st = time.time()
	one = subprocess.Popen(["make", "re"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	logging.info("Took " + str(time.time() - st) + " seconds to build!")
	text = one.communicate()
	returncode = one.returncode;
	if returncode != 0:
		logging.critical("Failed to make\n" + str(text) + "\nWith Error code " + str(returncode))
		sys.exit(1)
	logging.info("Built successfully")

if __name__ == '__main__':
	logging.basicConfig(filename='output.log', level=logging.INFO, format="%(levelname)s: %(message)s")

	subprocess.call(["git", "clone", "https://github.com/Jebbs/DSFML.git", "bin/dsfml"])
	subprocess.call(["cp", "-rf", "bin/dsfml", "."])

	olddata = []
	oldnames = findAllFiles("dsfml")
	for file in oldnames:
		file = open(file, 'r')
		olddata.append(file.read())
		file.close()

	key = "FUNFUNWITHABUNBUN"

	st = time.time()
	subprocess.call("tar -cf tarcheck.tar bin/dsfml".split(" "))
	baselinec = (time.time() - st)

	st = time.time()
	subprocess.call("tar -xf tarcheck.tar".split(" "))
	baselineu = (time.time() - st)
	subprocess.call("rm tarcheck.tar".split(" "))

	st = time.time()
	if subprocess.call("make") != 0:
		sys.exit(1)
	logging.info("Took " + str(time.time() - st) + " seconds to build!")
	logging.info("Baselines:\n\tCompression: " + str(baselinec) + "\n\tDecompression: " + str(baselineu))

	for i in range(100):
		logging.info("Iter: " + str(i))
		os.chdir("bin")
		ot = time.time()
		logging.info("Encryption only")

		for i in range(10):
			st = time.time()
			one = subprocess.call(["./coda", "-e", "-k", key, "dsfml"])
			compression = time.time() - st
			if one != 0:
				logging.critical("Failed with exit code:" + str(one))
				clean()
				sys.exit(1)

			subprocess.call(["rm", "-rf", "dsfml"])
			st = time.time()
			two = subprocess.call(["./coda", "-d", "-k", key, "out.coda"])
			uncompression = time.time() - st
			if two != 0:
				logging.critical("Failed with exit code:" + str(two))
				clean()
				sys.exit(1)

			newdata = []
			newnames = findAllFiles("dsfml")
			for file in newnames:
				file = open(file, 'r')
				newdata.append(file.read())
				file.close()

			for j in range(len(newnames)):
				if newnames[j] != oldnames[j] or newdata[j] != olddata[j]:
					logging.error("Failed at: " + newnames[j])
					clean()
					sys.exit(1)
			logging.info("Encryption: " + str(compression) + " Decryption: " + str(uncompression)+ " thats roughly Encryption:" + str(60 / compression) + " Decryption: " + str(60 / uncompression) + " per minute")
		logging.info("Total time for encryption was: " + str(time.time() - ot) + " Average time for one iter: " + str((time.time() - ot) / 10))
		logging.info("Compression with encryption")

		for i in range(10):
			st = time.time()
			one = subprocess.call(["./coda", "-c", "-cl", "22", "-e", "-k", key, "dsfml"])
			compression = time.time() - st
			if one != 0:
				logging.critical("Failed with exit code:" + str(one))
				clean()
				sys.exit(1)

			subprocess.call(["rm", "-rf", "dsfml"])
			st = time.time()
			two = subprocess.call(["./coda", "-d", "-u", "-k", key, "out.coda"])
			uncompression = time.time() - st
			if two != 0:
				logging.critical("Failed with exit code:" + str(two))
				clean()
				sys.exit(1)

			newdata = []
			newnames = findAllFiles("dsfml")
			for file in newnames:
				file = open(file, 'r')
				newdata.append(file.read())
				file.close()

			for j in range(len(newnames)):
				if newnames[j] != oldnames[j] or newdata[j] != olddata[j]:
					logging.error("Failed at: " + newnames[j])
					clean()
					sys.exit(1)
			logging.info("Compression: " + str(compression) + " Decompression: " + str(uncompression)+ " thats roughly Compression:" + str(60 / compression) + " Decompression: " + str(60 / uncompression) + " per minute")
		logging.info("Total time for compression and encryption was: " + str(time.time() - ot) + " Average time for one iter: " + str((time.time() - ot) / 10))
		
		ot = time.time()
		logging.info("Compression only")
		for i in range(10):
			st = time.time()
			one = subprocess.call(["./coda", "-c", "-cl", "22", "-v", "dsfml"])
			compression = time.time() - st
			if one != 0:
				logging.critical("Failed with exit code:" + str(one))
				clean()
				sys.exit(1)

			if compression > baselinec:
				logging.info("Took longer than the compression baseline with " + str(compression - baselinec) + " more seconds!")
			
			subprocess.call(["rm", "-rf", "dsfml"])
			st = time.time()
			two = subprocess.call(["./coda", "-u", "out.coda"])
			uncompression = time.time() - st
			if two != 0:
				logging.critical("Failed with exit code:" + str(two))
				clean()
				sys.exit(1)
			
			if uncompression > baselineu:
				logging.info("Took longer than the uncompression baseline with " + str(uncompression - baselineu) + " more seconds!")
			
			newdata = []
			newnames = findAllFiles("dsfml")
			
			for file in newnames:
				file = open(file, 'r')
				newdata.append(file.read())
				file.close()
			
			for j in range(len(newnames)):
				if newnames[j] != oldnames[j] or newdata[j] != olddata[j]:
					logging.error("Failed at: " + newnames[j])
					clean()
					sys.exit(1)
			logging.info("Compression: " + str(compression) + " Decompression: " + str(uncompression)+ " thats roughly Compression:" + str(60 / compression) + " Decompression: " + str(60 / uncompression) + " per minute")
		logging.info("Total time for compression was: " + str(time.time() - ot) + " Average time for one iter: " + str((time.time() - ot) / 10))
		os.chdir("..")
		clean()