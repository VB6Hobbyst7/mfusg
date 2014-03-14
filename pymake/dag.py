"""

Set of classes for building a directed acyclic graph.  Can be used to
determine the order of dependencies.  Can be used to determine compiling
order, for example.  Topological sort pseudocode obtained from:
http://en.wikipedia.org/wiki/Topological_sorting

"""

class Node(object):
    def __init__(self, name):
        self.name = name
        self.dependencies = []
        return

    def add_dependency(self, d):
        """
        Add dependency if not already in list
        """
        if d not in self.dependencies:
            self.dependencies.append(d)
        return

class DirectedAcyclicGraph(object):
    def __init__(self, nodelist):
        self.nodelist = nodelist
        return

    def toposort(self):
        """
        Perform topological sort
        """
        l = []  #empty list that will contain sorted elements

        #build a list of nodes with no dependencies
        s = set([])
        for n in self.nodelist:
            if len(n.dependencies) == 0:
                s.add(n)
        if len(s) == 0:
            raise Exception('All nodes have dependencies')

        #build up the list
        while len(s) > 0:
            n = s.pop()
            l.append(n)
            for m in self.nodelist:
                if n in m.dependencies:
                    m.dependencies.remove(n)
                    if len(m.dependencies) == 0:
                        s.add(m)

        #check to make sure no remaining dependencies
        for n in l:
            if len(n.dependencies) > 0:
                raise Exception ('Graph has at least one cycle')

        return l


def order_source_files(srcfiles):

    #create a dictionary that has module name and source file name
    #create a dictionary that has a list of modules used within each source
    #create a list of Nodes for later ordering
    #create a dictionary of nodes
    module_dict = {}
    sourcefile_module_dict = {}
    nodelist = []
    nodedict = {}
    for srcfile in srcfiles:
        node = Node(srcfile)
        nodelist.append(node)
        nodedict[srcfile] = node
        f = open(srcfile, 'r')
        modulelist = []  #list of modules used by this source file
        for line in f:
            linelist = line.strip().split()
            if len(linelist) == 0:
                continue
            if linelist[0].upper() == 'MODULE':
                modulename = linelist[1].upper()
                module_dict[modulename] = srcfile
            if linelist[0].upper() == 'USE':
                modulename = linelist[1].split(',')[0].upper()
                if modulename not in modulelist:
                    modulelist.append(modulename)
        sourcefile_module_dict[srcfile] = modulelist
        f.close()

    #go through and add the dependencies to each node
    for node in nodelist:
        srcfile = node.name
        modulelist = sourcefile_module_dict[srcfile]
        for m in modulelist:
            mlocation = module_dict[m]
            if mlocation is not srcfile:
                #print 'adding dependency: ', srcfile, mlocation
                node.add_dependency(nodedict[mlocation])

    #build the ordered dependency list using the topological sort method
    orderednodes = DirectedAcyclicGraph(nodelist).toposort()
    osrcfiles = []
    for node in orderednodes:
        osrcfiles.append(node.name)

    return osrcfiles





if __name__ == '__main__':
    a = Node('a')
    b = Node('b')
    c = Node('c')
    d = Node('d')

    a.add_dependency(b)
    a.add_dependency(c)
    c.add_dependency(d)
    d.add_dependency(b)

    nodelist = [a, b, c, d]

    dag = DirectedAcyclicGraph(nodelist)
    ordered = dag.toposort()
    print 'length of output: ', len(ordered)

    for n in ordered:
        print n.name
