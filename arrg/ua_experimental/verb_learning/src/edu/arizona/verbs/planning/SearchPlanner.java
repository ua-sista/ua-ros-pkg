package edu.arizona.verbs.planning;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.PriorityQueue;
import java.util.TreeSet;

import org.apache.log4j.Logger;

import edu.arizona.verbs.fsm.FSMState;
import edu.arizona.verbs.planning.search.SearchNode;
import edu.arizona.verbs.planning.shared.AbstractPlanner;
import edu.arizona.verbs.planning.shared.Policy;
import edu.arizona.verbs.planning.shared.State;
import edu.arizona.verbs.shared.Environment;
import edu.arizona.verbs.shared.OOMDPState;
import edu.arizona.verbs.verb.Verb;

/*
 * An implementation of the A* search algorithm for planning with VFSMs
 */
public class SearchPlanner extends AbstractPlanner {

	private static Logger logger = Logger.getLogger(SearchPlanner.class);
	
	private SearchNode root_;
	private HashMap<String, SearchNode> knownNodes_ = new HashMap<String, SearchNode>();
	
	public SearchPlanner(Verb verb, Environment environment) {
		super(verb, environment);
		
		root_ = null;
	}
	
	@Override
	public Policy runAlgorithm(OOMDPState startState, TreeSet<FSMState> fsmState) {
		State start = lookupState(startState, fsmState);
		
		logger.info("Start state is: " + start);
		
		root_ = lookupNode(start, 0);
		
		HashSet<SearchNode> closed = new HashSet<SearchNode>();
		PriorityQueue<SearchNode> open = new PriorityQueue<SearchNode>(); 
		open.add(root_);
		HashMap<SearchNode, SearchNode> cameFrom = new HashMap<SearchNode, SearchNode>();

		int visited = 0;
		int maxVisited = 100000;
		
		while (!open.isEmpty() && visited < maxVisited) { // Hack but needs to stop if no solution 
			SearchNode x = open.remove();
			
			if (x.state.isGoal()) {
				List<SearchNode> path = reconstructPath(cameFrom, x);
//				System.out.println("DONE!");
//				System.out.println("PATH: ");
//				for (SearchNode n : path) {
//					System.out.println(n.state);
//				}
				
				return new Policy(path);
			}
			
			closed.add(x);
			
			for (SearchNode y : x.getChildren()) {
				if (closed.contains(y)) {
					continue;
				}
				
				int tentativeG = x.g + 1;
				
				boolean tentativeIsBetter;
				if (!open.contains(y)) {
					open.add(y);
					tentativeIsBetter = true;
				} else if (tentativeG < y.g) {
					tentativeIsBetter = true;
				} else {
					tentativeIsBetter = false;
				}
				
				if (tentativeIsBetter) {
					cameFrom.put(y, x);
				
					y.g = tentativeG;
//					y.h is already set
					y.f = y.g + y.h;
				}
			}
			visited++;
		}
	
		return new Policy();
	}
	
	public List<SearchNode> reconstructPath(HashMap<SearchNode, SearchNode> cameFrom, SearchNode current) {
		if (cameFrom.containsKey(current)) {
			List<SearchNode> p = reconstructPath(cameFrom, cameFrom.get(current));
			p.add(current);
			return p;
		} else {
			List<SearchNode> justMe = new ArrayList<SearchNode>();
			justMe.add(current);
			return justMe;
		}
	}
	
	public SearchNode lookupNode(State s, int depth) {
		String hashString = String.valueOf(depth) + s.toString();
		if (!knownNodes_.containsKey(hashString)) {
			knownNodes_.put(hashString, new SearchNode(this, s, depth, getVerb().getFSM().getHeuristicInt(s.getFsmState())));
		}
		
		return knownNodes_.get(hashString);
	}
	
}