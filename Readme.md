# Value Iteration
> ### Team
> + Team : 76 : Platypus_Perry
> + Archit Jain (2019101053)
> + Pulkit Gupta (2019101078)

This part of assignment covers the concept of the Bellman equation in the basis of the value iteration algorithm for solving MDPs.

## Task 1

> + Iteration : 117 (0-based)
> + Gamma : 0.999
> + Delta : 0.001
> + Hit Penalty : -40
> + Kill Reward : 50
> + Step Cost : -10
> + Rate of convergence : 2.3935907535275573 ( here rate of convergence is defined as average of error for all the iterations )

### Inferences from Task 1 
- Policy chooses to shoot only if he has atleast one arrow.
- Policy chooses to gather only if he has less than 2 materials.
- Policy chooses to craft only if he has atleast 1 material and less than 3 arrows.
- When IJ doesn't have arrows and material in any state it moves toward the EAST to HIT MM with blade when MM in a Dormant state but when MM is in a Ready state it will try to STAY in NORTH or WEST when present there and GATHER material in the SOUTH if he has less than that max cap and other states it tries to HIT with the blade.
- When it has an arrow and present in a state in which it can't attack it will moves to the states to shoot with an arrow or hit with a blade to decrease the health of MM but more probably IJ tries to shoot with arrow if he has one, as it has more probability of getting action successful.
-  When MM is in Ready state with low heath IJ will try to attack MM when having arrow or hit with blade to get the positive reward of killing MM and if MM has sufficient health IJ will move up to safe states like NORTH may or may not to CRAFT arrows, or moves to the south to GATHER material.
-  Surprisingly, it will never move to the left and always tries to attack MM when present on east and when on centre it will move in only NORTH or SOUTH positions for crafting arrows or gathering material and if he has sufficient material and arrows it will move to east, to kill MM maybe due to high reward value. 

## Simulation
### Output format 
```
    ...
    > start state
    > action to be performed
    > state after completion of action
    ...
```
### 1. (W, 0, 0, D, 100)
One of the output from simulation run over the policy result.

```
    W 0 0 D 100
    RIGHT
    C 0 0 D 100

    C 0 0 D 100
    RIGHT
    E 0 0 D 100

    E 0 0 D 100
    HIT
    E 0 0 D 100

    E 0 0 D 100
    HIT
    E 0 0 D 50

    E 0 0 D 50
    HIT
    E 0 0 D 50

    E 0 0 D 50
    HIT
    E 0 0 D 50

    E 0 0 D 50
    HIT
    E 0 0 D 50

    E 0 0 D 50
    HIT
    E 0 0 D 50

    E 0 0 D 50
    HIT
    E 0 0 D 50

    E 0 0 D 50
    HIT
    E 0 0 D 0
```
From the bunch of outputs which are somewhat similar, we can infer that IJ will first moves to EAST and then chooses to hit with blade over any other action whenever he is at east position. So that he can defeat MM in less timestep. Since IJ has 0 arrows and 0 materials instead of first gathering material and then crafting arrow to shoot MM he is prefering to hit the MM with blade as he is getting negative reward for each timestep and wants to kill MM as early as possible. So the desired path would be to go at EAST position and then hit with blade. We can also observe that MM is not going to Ready state ever because of high probablity of it to stay in dormant state.

### 2. (C, 2, 0, R, 100)
One of the output from simulation run over the policy result.
```
    C 2 0 R 100
    UP
    N 2 0 R 100

    N 2 0 R 100
    CRAFT
    N 1 1 R 100

    N 1 1 R 100
    CRAFT
    N 0 2 R 100

    N 0 2 R 100
    STAY
    N 0 2 D 100

    N 0 2 D 100
    DOWN
    E 0 2 D 100

    E 0 2 D 100
    HIT
    E 0 2 D 100

    E 0 2 D 100
    HIT
    E 0 2 R 100

    E 0 2 R 100
    HIT
    E 0 2 R 50

    E 0 2 R 50
    SHOOT
    E 0 1 R 25

    E 0 1 R 25
    SHOOT
    E 0 0 R 0
```
From the bunch of outputs, we can infer that, IJ tries to move to NORTH position as it has material and its also a safe state for him and after crafting sufficient number of arrows (2-3), It will go to EAST via CENTER and try to attack MM but in between if MM attacks IJ, IJ will loose all its arrows and He have to hit MM with blade otherwise he will chooses to shoot with arrow because of high probability of it getting successful. So that he can defeat MM and get the positive reward in less timestep.

## Task 2

### Case 1

> + Iteration : 119 (0-based)
> + Gamma : 0.999
> + Delta : 0.001
> + Hit Penalty : -40
> + Kill Reward : 50
> + Step Cost : -10
> + Rate of convergence : 2.2927984931864627 ( here rate of convergence is defined as average of error for all the iterations )

#### Inferences from the result in above case
- Here is a slight change When Action `LEFT` is chosen IJ moves from EAST to WEST instead of centre. Whenever MM is in Ready state and IJ is at EAST position , in this case if MM health is low , IJ tries to hit the MM or shoot the MM if he has arrows to get the positive reward which it may get if the MM is killed completely else if MM health is high , IJ tries to save himself by choosing Action `LEFT` which results in WEST position which is safe position from MM. The `LEFT` action results in CENTER position which is also not safe from MM in Task 1. 

### Case 2

> + Iteration : 149 (0-based)
> + Gamma : 0.999
> + Delta : 0.001
> + Hit Penalty : -40
> + Kill Reward : 50
> + Step Cost : -10 (for all actions) 
> + Step Cost : 0 (for action STAY)
> + Rate of convergence : 1.805067655234594 ( here rate of convergence is defined as average of error for all the iterations )

#### Inferences from the result in above case
- Here the step cost which is negative reward after each timestep is reduced to `0` for `STAY` Action . So IJ is now likely to choose `STAY` action whenever possible as Value Iteration always chooses that action giving maximum reward and Action `STAY` is delaying the policy to converge instead action `SHOOT` or `HIT` to be chosen which would help in reducing the health of MM finally rewarding him `+50` reward when the MM health becomes `0`

### Case 3

> + Iteration : 7 (0-based)
> + Gamma : 0.25
> + Delta : 0.001
> + Hit Penalty : -40
> + Kill Reward : 50
> + Step Cost : -10 
> + Rate of convergence : 5.072693730545839  ( here rate of convergence is defined as average of error for all the iterations )

#### Inferences from the result in above case
- The value of gamma is decreased very much as compared to that of task 1 . And gamma is the discout factor that decides how much utility from previous iteration should be given to next iteration. If the value of discount factor is less then , it means policy is giving preference to do everything now only in present iteration. and Since only a minimal amount of utility is pass it converges very early as compared to that of task 1.
