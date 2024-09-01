import ContractPoINetwork
import CONSTANTS
import Node

import csv, time
import multiprocessing as mp
import os

from itertools import repeat


def main():
    poiDivtDict = {}
    poi_info_dict = {} # Used to create PoI_info.csv, and nodes for the ContractPoINetwork
    city = "Memphis"
    num_pois = 10

    with open("LDA_Model_6/" + city + "DivVector.csv", 'r', encoding='cp1252') as rf:
        spamreader = csv.reader(rf)

        id = 0
        for eachPoI in spamreader:
            poiName = eachPoI[0]

            divVec = [float(eachPoI[i]) for i in range(1, CONSTANTS.CATEGORY_NUM+1)]

            poiDivtDict[poiName] = [0] * CONSTANTS.CATEGORY_NUM
            maxIdx = divVec.index(max(divVec))
            poiDivtDict[poiName][maxIdx] = 1

            # Storing PoI information using PoI class 
            poi_info_dict[poiName] = Node.PoI(id, poiName, maxIdx)
            id += 1

    # Create <CITY>_PoI_info.csv
    if not os.path.exists("PoI_Network/CSV/" + city + "_PoI_info.csv"):
        with open("PoI_Network/CSV/" + city + "_" + str(num_pois) + "_PoI_info.csv", 'w', newline='') as wfile:
            spamwriter = csv.writer(wfile)

            spamwriter.writerow(['id', 'name', 'category'])
            
            for poi in poi_info_dict:
                values = poi_info_dict[poi]
                spamwriter.writerow([values.poi_id, values.name, values.category])


    g = ContractPoINetwork.ContractPoINetwork()

    print("Start Inserting Nodes......")
    with open("PoI_Network/" + city + "_ns.csv", 'r') as rf:
        spamreader = csv.reader(rf)
        next(spamreader)

        count = 1

        for eachN in spamreader:
            nID, nLng, nLat, nPoiStr = int(eachN[0]), float(eachN[1]), float(eachN[2]), eachN[3]

            if eachN[4] == 'Y':
                nStarting = True
            else:
                nStarting = False

            if nPoiStr == '':
                g.add_node(id_=nID, lng_=nLng, lat_=nLat)
            else:
                nPois = set()
                nPoiL = nPoiStr.split('|')

                for eachP in nPoiL:
                    nPois.add(poi_info_dict[eachP])

                g.add_node(id_=nID, lng_=nLng, lat_=nLat, pois_=nPois)

            print("Inserted ", count, " nodes")
            g.nodes[nID].print_info()
            print("///////////////////////")
            count += 1

    print("Inserted all ", count - 1, " nodes successfully......")

    print("Starting Inserting Edges......")
    with open("PoI_Network/" + city + "_es.csv", 'r') as rf:
        spamreader = csv.reader(rf)
        next(spamreader)

        count = 1

        for eachE in spamreader:
            eID1, eID2, eW = int(eachE[0]), int(eachE[1]), float(eachE[2])
            g.add_edge(id1=eID1, id2=eID2, weight=eW)
            print("Inserted ", count, " edges")
            g.edges[(eID1, eID2)].print_info()
            print("///////////////////////")
            count += 1

    print("Inserted all ", count - 1, " edges successfully......")

    print("Start contracting network with ", mp.cpu_count(), " CPUs")

    startT = time.time()

    while True:

        uncontractedNodes = [nID for nID, nNode in g.nodes.items() if not nNode.isContracted]

        if len(uncontractedNodes) == 0:
            break

        print("=========================")
        print(len(uncontractedNodes), " nodes have not been contracted......")

        if g.cur_iter != 0:  # Only update the neighbors of the contracted node in the last iteration
            uncontractedNodes = set()
            for eachContractedN in independentSet:
                adjEdges = g.neighbor_edges[eachContractedN]
                for eachE in adjEdges:
                    if (eachE.node_id1 != eachContractedN) and (not g.nodes[eachE.node_id1].isContracted):
                        uncontractedNodes.add(eachE.node_id1)
                    if (eachE.node_id2 != eachContractedN) and (not g.nodes[eachE.node_id2].isContracted):
                        uncontractedNodes.add(eachE.node_id2)

        print(len(uncontractedNodes), " nodes have to update priority......")
        print("=========================")

        pool = mp.Pool(mp.cpu_count())

        priorityRes = pool.map(g.priority_cal, [i for i in uncontractedNodes])

        pool.close()

        #g.shortcuts.clear()

        for pID, pPriority, pShortcuts in priorityRes:
            g.nodes[pID].priority = pPriority  # Update Priority
            g.shortcuts[pID] = pShortcuts  # Update shortcuts

        ### Start find Independent set ###

        uncontractedNodes = [nID for nID, nNode in g.nodes.items() if not nNode.isContracted]

        managerIndependent = mp.Manager()

        independentDone = managerIndependent.dict()

        for i in uncontractedNodes:
            independentDone[i] = True

        pool = mp.Pool(mp.cpu_count())

        independentRes = pool.starmap(g.check_independent,
                                      zip(uncontractedNodes, repeat(independentDone))
                                      )

        pool.close()

        independentList = []

        # Pick the CONSTANTS.SizeOfIndependentSet nodes with the smallest priority
        for iID, iIndependent in independentRes:
            if iIndependent:  # If independent, return True
                independentList.append((iID, g.nodes[iID].priority))

        '''
        sortedIndependentList = sorted(independentList, key=lambda x: x[1])

        if sortedIndependentList[0][1] == 1.0:  # First iteration - if priority == 1.0, no shortcut
            independentSet = [x[0] for x in sortedIndependentList if x[1] == 1.0]
        else:
            independentSet = [val[0] for idx, val in enumerate(sortedIndependentList)
                              if idx < CONSTANTS.SizeOfIndependentSet]
        '''

        if g.cur_iter == 0:  # First iteration => if priority == 1.0 and thus no shortcut/neighbor, dead-end node
            independentSet = [x[0] for x in independentList if x[1] == 1.0]
        else:
            if len(independentList) > CONSTANTS.SizeOfIndependentSet:
                independentList = sorted(independentList, key=lambda x: x[1])

            independentSet = [val[0] for idx, val in enumerate(independentList)
                              if idx < CONSTANTS.SizeOfIndependentSet]

        print("=========================")
        print(len(independentSet), " independent nodes are going to be contracted......")
        print("=========================")

        # s1: Add shortcuts to self.edges
        # s2: Add shortcuts to self.neighbor
        # s3: Update depth of neighbors for each contracting node
        # s4: Mark node.isContracted as True and Update contractOrder to g.curIter
        # s5: Update g.curIter

        for contractingNode in independentSet:
            # s1, s2
            shortcutList = g.shortcuts[contractingNode]

            for scCost, scSrcDest in shortcutList:
                # (scCost, (scSrc, scDest)) src -> contractingNode -> dest
                scSrc, scDest = scSrcDest
                g.add_shortcut(scSrc, scDest, scCost, contractingNode)

            # s3
            g.update_depth(contractingNode)

            # s4
            g.nodes[contractingNode].isContracted = True
            g.nodes[contractingNode].contract_order = g.cur_iter

            # s5
            g.cur_iter += 1

        print("//////////////////////////////////////////////")

    endT = time.time()

    print("Time Cost: ", endT-startT)

    with open("PoI_Network/" + city + "_CH_ns_euclidean.csv", 'w', newline='') as wfile:
        spamwriter = csv.writer(wfile)

        spamwriter.writerow(['id', 'lng', 'lat', 'depth', 'order'])

        for k, v in g.nodes.items():
            spamwriter.writerow([k, v.lng, v.lat, v.depth, v.contract_order])

    with open("PoI_Network/" + city + "_CH_es_euclidean.csv", 'w', newline='') as wfile:
        spamwriter = csv.writer(wfile)

        spamwriter.writerow(['from', 'to', 'weight', 'isShortcut', 'mid_id'])

        for k, v in g.edges.items():
            nStart, nEnd, nW, nMid = v.node_id1, v.node_id2, v.weight, v.middle_id

            if v.isShortcut:
                nSC = 'Y'
            else:
                nSC = 'N'

            spamwriter.writerow([nStart, nEnd, nW, nSC, nMid])


if __name__ == "__main__":
    main()