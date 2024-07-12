# Search

## Agent

Entity that prceives its environment and acts upon that environment

## State

A configuration of the agent and its environment

## Initial state

The state that the agent begins

## Actions

Choices that can be made in a state

$Actions(s)$ returns the set of actions that can be executed in state $s$

## Transition Model

A description of what state results from perming any applicable action in any state

$Result(s,a)$ returns the state resulting from performing action $a$ in state $s$

## State space

The set of all states reachable from the initial state by any sequence of actions

## Goal test

Way to determine whether a given state is a goal state

## Path cost

Numerical cost associated with a given path

## Search Problems Summary

- initial state
- actions
- transition model
- goal test
- path cost function

## Solution

A sequence of actions that leads from the initial state to a goal state

## Optimal Solution

A solution that has the lowest path cost among all solutions

## Node

A data structure that keeps track of

- a state
- a parent (node that generated this node)
- an action (action applied to parent to get node)
- a path cost (from initial state to node)

## Approach

- Start with a frontier that contains the initial state
- Repeat:
  - If the frontier is empty, then no solution
  - Remove a node from the frontier
  - If node contains goal state, return the solution.
  - Expand node, add resulting nodes to the frontier.

## Revised Approach

- Start with a frontier that contains the initial state.
- Start with an empty explored set.
- Repeat:
  - If the frontier is empty, then no solution.
  - Remove a node from the frontier.
  - If node contains goal state, return the solution.
  - Add the node to the explored set.
  - Expand node, add resulting nodes to the frontier if they aren't already in the frontier or the explored set

## Stack

LIFO data type

## Depth-First Search (DFS)

Search algorithm that always expands the deepest node in he frontier.
Uses the stack (LIFO) as DS for frontier.
Doesn't always find the optimal solution.

## Breadth-First Search (BFS)

Search algorithm that always expands the shallowest node in the frontier
Uses the queue (FIFO) as DS for frontier.

## Uninformed Search

Search strategy that uses no problem-specific knowledge

## Informed search

Search strategy that uses problem-specific knowledge to find solutions more efficiently

### Greedy Best-First Search

> Search algorithm that expands the node that is closest to the goal, as estimated by a heurist function $h(n)$

### A\* search

> Search algorithm that expands node with lowest value of $g(n) + h(n)$
>
> $g(n)$ = cost to reach node
>
> $h(n)$ = estimated cost to goal
>
> Optimal if:
>
> - $h(n)$ is admissible (never overestimates the true cost), and
> - $h(n)$ is consistent (for every node $n$ and successor $n'$ with step cost $c$, $h(n) <= h(n') + c$)

EOF - 1:11:50
