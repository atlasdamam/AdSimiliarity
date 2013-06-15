import os
import slam_ad

path = str(os.getcwd()) + "/ads1_and_2_vset"
local_path = "ads1_and_2_vset"
listing = os.listdir(path)
for infile in listing:
    print infile
    slam_ad.slamAd(os.path.join(local_path, infile))
    print "------------------------------------------------------------------------"
    print

print "Done slamming files." 