from pylab import *
from mpi4py import MPI
import urllib2
import re
from xml.dom.minidom import parseString

def serial_dot(entries, start_k, end_k):
	result = []
	for k in range(start_k,end_k):
		    lat = entries[k].split(',')[0]
		    lng = entries[k].split(',')[1]

		    try: 
	            	# download the file
		    	xml_file=urllib2.urlopen('http://nominatim.openstreetmap.org/reverse?lat='+lat+'&lon='+lng)
		    	xml_data = xml_file.read()
		    	xml_file.close()

		    	# parse the xml you downloaded
		    	dom = parseString(xml_data)
	
		    	# retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
		    	try:
				xmlCountry = dom.getElementsByTagName('country')[0].toxml()
				xmlCountry=xmlCountry.split('<country>')[1].split('</country>')[0]
		    	except Exception:
				xmlCountry = 'None'
		    	result.append(lat + ',' + lng + ',' + xmlCountry.encode('utf8')) 
		    except Exception: 
			result = result
	return result 


def parallel_dot(entries, start_k, end_k, rank, size, comm):
	# Size of each process's local problem
	n = ((end_k - start_k) / size) 
	excess = (end_k - start_k) % size
	# Compute the partial result
	if (rank<excess):
		local_dot = serial_dot(entries, start_k + rank*n+rank, start_k + (rank+1)*n+rank+1)	
	else:
		local_dot = serial_dot(entries, start_k + rank*n+excess, start_k + (rank+1)*n+excess)
	# Reduce the partial results to the root process	
	result = comm.reduce(local_dot, root=0)
	return result

# Initialize MPI constants
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
print "Hello from process %d of %d" % (rank,size)

# Size of the test problem
N = 506680

# Generate two random vectors on process 0
if rank == 0:
	# open data_combined.csv
	file = open("test.csv")
	data_file = file.read()
	file.close()

	# for final output file with labels
	fout=open("test_w_labels.csv","wb")

	# Get lat and lng
	entries = re.split('\n', data_file)	
else:
	entries = None

# Broadcast these vectors to all processes
entries = comm.bcast(entries, root=0)

# Start the clock
comm.barrier()
start_time = MPI.Wtime()

# Perform the parallel inner product
p_dot = parallel_dot(entries, 0, N, rank, size, comm)

# Stop the clock
comm.barrier()
stop_time = MPI.Wtime()

# Print results
if rank == 0:	
	for location in p_dot: 
		fout.write(location+ '\n')
	#start_time_ser = MPI.Wtime()
	#s_dot = serial_dot(a, b, 0, N)
	#stop_time_ser = MPI.Wtime()
	#rel_error = abs(p_dot - s_dot) / abs(s_dot)
	#speedup =  (stop_time_ser - start_time_ser)/(stop_time - start_time)
	#efficiency = speedup/size
	print "Time: %f secs" % (stop_time - start_time)
	#print "Time in serial: %f secs" % (stop_time_ser - start_time_ser)
	#print "Speedup: %f" % speedup
	#print "Efficiency: %f" % efficiency
	#print "Parallel Result = %f" % p_dot
	#print "Serial Result   = %f" % s_dot
	#print "Relative Error  = %e" % rel_error
	#if rel_error > 1e-10:
	#	print "***LARGE ERROR - POSSIBLE FAILURE!***"


