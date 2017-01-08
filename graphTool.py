#!/usr/bin/python

try:
	import config
except:
    print("Failed to open config.py. graphTool.py requres the configuration to run.")
    print("Please copy example/config.py to config.py and edit it.")

import argparse
import agGraph
from traceback import traceback
from pprint import pprint

elStr = "--createRRD can be used with --geiger and --enviro. --graph can also be used with both, but if they are not specified it will generate graphs or RRD files for both. If --timing is not specified with --graph all graphs will be generated."


# If we're being executed and not included...
if __name__ == "__main__":
    # Set up command line interface.
    parser = argparse.ArgumentParser(description = "AutoGeiger graph tool.", epilog = elStr)
    parser.add_argument('--createRRD', action = 'store_true', help = 'Create empty RRD database files. Generates both DBs by default.')
    parser.add_argument('--graph', action = 'store_true', help = 'Generate graphs from RRD files. Generates both graphs by default.')
    parser.add_argument('--geiger', action = 'store_true', help = 'Target geiger counter RRD.')
    parser.add_argument('--enviro', action = 'store_true', help = 'Target environmental data RRD.')
    parser.add_argument('--timing', choices = ['1h', '1d', '1w', '30d'], help = 'Time frame graph to generate. Defaults to generating all time frames when used with --graph.')
    args = parser.parse_args()
    
    try:
        # Build graph interface object.
        agG = agGraph.agGraph()
        
        # Which dataset do we want to effect?
        graphTargets = []
        
        # Do we want to do things with the geiger RRD?
        if args.geiger == True:
            graphTargets.append = ["geiger"]
        
        # Do we want to do things with the enviro RRD?
        if args.enviro == True:
            graphTargets.append = ["enviro"]
        
        # If neither was specified assume they want both.
        if (args.geiger == False) and (args.enviro == False):
            graphTargets = ["geiger", "enviro"]
        
        # We want to create RRD files...
        if args.createRRD == True:
            # For each type of RRD we want to build
            for rrdTgt in graphTargets:
                # Build it.
                agG.createRRD(rrdTgt)
        
        # We want to graph then...
        elif args.graph == True:
            # Set a dummy value that will trigger generation of all timeframes.
            timingSuffix = ["1h", "1d", "1w", "1m"]
            
            # If we specify a timing suffix set it.
            if args.timing == "1h":
                timingSuffix = ["1h"]        
            if args.timing == "1d":
                timingSuffix = ["1d"]
            if args.timing == "1w":
                timingSuffix = ["1w"]
            if args.timing == "1m":
                timingSuffix = ["1m"]
            
            # For each type of graph we're going to generate
            for rrdTgt in graphTargets:
                # Generate it based on timing suffix.
                for suffix in timingSuffix:
                    # Generate target name
                    tName = "%s%s" %(rrdTgt, suffix)
                    
                    # Generate the given graph
                    agG.createGraph(tName)
        
        else:
            print("You must specify --createRRD or --graph.")
    
    except KeyboardInterrupt:
        print("Caught keyboard interrupt. Quitting.")
    
    except:
        tb = traceback.format_exc()
        print("Caught unhandled exception:\n%s" %tb)