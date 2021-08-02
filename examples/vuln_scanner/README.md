# README

GOALS: 
    The automaton must be able to sense the response or effect of its own actions
    The automaton need a history or recent memory (which actions were performed and succeeded?)
    The actions need access to the automaton knowledge in due to extract useful parameters to its actions
    The automatons need to be reactive: Change of states needs to trigger a plan
    The automatons need to communicate to each other and combine plans
    
    

Steps:

- discover active network nodes
- find hosts with port 80 open
- scan for http vuln
- report vuln hosts
- exploit vuln hosts


Sensors

* discover network nodes: 
  * states: 
    * active_nodes: List[hosts|ips]
    * found_new_nodes: bool
    * vuln_nodes: List[host|ips]

Actions

* scan hosts
* scan host vuln
* exploit host vuln