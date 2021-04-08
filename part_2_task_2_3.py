import numpy as np
import random
import json

# if not os.path.exists("outputs"):
#     os.makedirs("outputs")

# def save_json(to_write,):
#     file_name = "./outputs/output.json 
#     file = open(file_name, "w")
#     json.dump(to_write, file)
#     file.close()

# def roll_porb(accepted):       # function to check the probability
# 	if(accepted>1):
# 		accepted=accepted/100
# 	if(random.uniform(0, 1)<=accepted):
# 		return 1
# 	else:
# 		return 0

# def made_arrow_prob():
# 	arr = [1,1,1,1,1,1,1,1,1,1,3,3,3,2,2,2,2,2,2,2]
# 	return random.choice(arr)

def action_ctoi(st):
  if(st=='A'):
    return 1
  elif(st=='B'):
    return 2
  elif(st=='C'):
    return 3
  elif(st=='G'):
    return 4
  elif(st=='s'):
    return 5
  elif(st=='r'):
    return 6
  elif(st=='l'):
    return 7
  elif(st=='u'):
    return 8
  elif(st=='d'):
    return 9
  else:
    return 0

def action_itop(st):
  if(st==1):
    return "SHOOT"
  elif(st==2):
    return "HIT"
  elif(st==3):
    return "CRAFT"
  elif(st==4):
    return "GATHER"
  elif(st==5):
    return "STAY"
  elif(st==6):
    return "RIGHT"
  elif(st==7):
    return "LEFT"
  elif(st==8):
    return "UP"
  elif(st==9):
    return "DOWN"
  elif(st==0):
    return "NONE"

# timestep = 0
error = 1                     # max Error of Iteration
gamma = 0.25                  # Discout factor
delta = 0.001                 # Bellman error
# MM_current_state = 'D'         # MM current state
# MM_health = 100                # MM current health
# IJ_current_state = 'N'         # IJ current state
step_cost = -10                # step cost after each timestep
# num_arrow = 3                  # current number of arrows
# num_material = 2               # current number of materials
# max_arrow = 3                  # max allowed arrow
# max_material = 2               # max allowed material
# reward = 0                     # reward of IJ
hit_reward = -40 
kill_reward = 50
# fl = 0 						   					 # to check if his steps become unsuccessful.
# run = 1                     # while look control
# moves IJ can take if present on i are in list allowed_moves[i]
allowed_moves = {
  'N':['O','N','C'],
  'S':['O','S','G'],
  'E':['O','E','A','B'],
  'W':['O','W','A'],
  'O':['O','W','N','S','E','A','B'],
}
# allowed_moves = {
#   'N':['O','N'],
#   'S':['O','S'],
#   'E':['O','E'],
#   'W':['O','W'],
#   'O':['O','W','N','S','E'],
# }
# prob_move[i][0]==sucessfull and prob_move[i][1]==unsucessfull  
prob_move = {
	'N':[85,15],
	'S':[85,15],
	'E':[100,0],
	'W':[100,0],
	'O':[85,15],
}
action_dic = {
  'A' : "SHOOT",
  'B' : "HIT",
  'C' : "CRAFT",
  'G' : "GATHER",
  'n' : "NONE",
  'l' : "LEFT", 
  'r' : "RIGHT", 
  'u' : "UP", 
  'd' : "DOWN",
  's' : "STAY" 
}

possible_states = ['N','S','E','W','O']
materials = [0,1,2]
arrows = [0,1,2,3]
health = [0,25, 50,75, 100]
MM_accept_states = ['D','R']   # MM's allowed state list  
MM_dr = 0.2
MM_dd = 0.8
MM_rd = 0.5
MM_rr = 0.5
utility = np.zeros((5,3,4,2,5))
temp_utility = np.zeros((5,3,4,2,5))
action = np.zeros((5,3,4,2,5))
iteration = 0
f = open("./outputs/part_2_task_2.3_trace.txt", "a")
while error>delta:
	error = -100000000
	print("iteration=" + str(iteration), file=f)
	iteration = iteration +1
	for a in possible_states:
		for b in  materials:
			for c in arrows:
				for d in MM_accept_states:
					for e in health:
						v = possible_states.index(a)  
						w = materials.index(b)
						x = arrows.index(c)
						y = MM_accept_states.index(d)
						z = health.index(e)
						if e !=0:
							if a == 'O': 
								max_u = -10000000000
								best_action = ''
								for i in allowed_moves[a]:
									if d == 'D':
										if i == 'A':
											if x>0:
												if e > 25:
													ab = step_cost + MM_dd*gamma*0.5*(utility[v][w][x-1][y][health.index(e-25)]+utility[v][w][x-1][y][z]) + MM_dr*gamma*0.5*(utility[v][w][x-1][1][health.index(e-25)]+utility[v][w][x-1][1][z])
												else:
													ab =  0.5*kill_reward + step_cost + MM_dd*gamma*0.5*(utility[v][w][x-1][y][0]+ utility[v][w][x-1][y][z]) + MM_dr*gamma*0.5*(utility[v][w][x-1][1][0]+ utility[v][w][x-1][1][z]) 
												if ab >= max_u:
													max_u = ab
													best_action = i
										elif i == 'B':
											if e > 50:
												ab =  step_cost + MM_dd*gamma*(0.1*utility[v][w][x][y][health.index(e-50)]+ 0.9*utility[v][w][x][y][z]) + MM_dr*gamma*(0.1*utility[v][w][x][1][health.index(e-50)]+ 0.9*utility[v][w][x][1][z])
											else:
												ab = 0.1*kill_reward + step_cost + MM_dd*gamma*(0.1*utility[v][w][x][y][0]+ 0.9*utility[v][w][x][y][z]) + MM_dr*gamma*(0.1*utility[v][w][x][1][0]+ 0.9*utility[v][w][x][1][z])
											if ab >= max_u:
												max_u = ab
												best_action = i	
										else:
											suc_prob = []
											for ii in prob_move[a]:
												suc_prob.append(float(ii)/100)
											ab = MM_dd*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][y][z]) + MM_dr*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][1][z]) + MM_dd*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][y][z]) + MM_dr*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][1][z])
											if ab >= max_u:
												max_u = ab
												best_action = i
									elif d == 'R':
										if i == 'A':
											if x>0:
												if e > 25:
													ab = step_cost + MM_rr*gamma*0.5*(utility[v][w][x-1][y][health.index(e-25)]+utility[v][w][x-1][y][z]) + MM_rd*(hit_reward) + MM_rd*gamma*(utility[v][w][0][0][health.index(min(e+25,100))])
												else:
													ab =  MM_rr*0.5*kill_reward + step_cost + MM_rr*gamma*0.5*(utility[v][w][x-1][y][0]+ utility[v][w][x-1][y][z]) + MM_rd*(hit_reward) + MM_rd*gamma*(utility[v][w][0][0][health.index(min(e+25,100))])
												if ab >= max_u:
													max_u = ab
													best_action = i
										elif i == 'B':
											if e > 50:
												ab =  step_cost + MM_rr*gamma*(0.1*utility[v][w][x][y][health.index(e-50)]+ 0.9*utility[v][w][x][y][z]) + MM_rd*(hit_reward) + MM_rd*gamma*(utility[v][w][0][0][health.index(min(e+25,100))])
											else:
												ab = MM_rr*0.1*kill_reward + step_cost + MM_rr*gamma*(0.1*utility[v][w][x][y][0]+ 0.9*utility[v][w][x][y][z]) + MM_rd*(hit_reward) + MM_rd*gamma*(utility[v][w][0][0][health.index(min(e+25,100))])
												max_u = ab
												best_action = i	
										else:
											suc_prob = []
											for ii in prob_move[a]:
												suc_prob.append(float(ii)/100)
											ab = MM_rr*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][y][z]) + MM_rr*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][1][z]) + MM_rd*(hit_reward) + MM_rd*gamma*(step_cost + utility[v][w][0][0][health.index(min(e+25,100))])
											if ab >= max_u:
												max_u = ab
												best_action = i
								if best_action =='A' or best_action =='B' or best_action =='G' or best_action =='C':
									action[v][w][x][y][z] = action_ctoi(best_action)
								else:
									num = 0
									if best_action == 'N':
										num = action_ctoi("u")
									elif best_action == 'S':
										num = action_ctoi("d")
									elif best_action == 'E':
										num = action_ctoi("r")
									elif best_action == 'W':
										num = action_ctoi("l")
									elif best_action == 'O':
										num = action_ctoi("s")
									action[v][w][x][y][z] = num
								temp_utility[v][w][x][y][z] = max_u
							elif a == 'N':
								max_u = -10000000000
								best_action = '' 
								for i in allowed_moves[a]:
									if d == 'D':
										if i == 'C':
											if b != 0 and c < 3:
												ab = step_cost + MM_dd*gamma*(0.5*utility[v][w-1][arrows.index(min(c+1,3))][y][z] + 0.35*utility[v][w-1][arrows.index(min(c+2,3))][y][z] + 0.15*utility[v][w-1][arrows.index(min(c+3,3))][y][z]) + MM_dr*gamma*(0.5*utility[v][w-1][arrows.index(min(c+1,3))][1][z] + 0.35*utility[v][w-1][arrows.index(min(c+2,3))][1][z] + 0.15*utility[v][w-1][arrows.index(min(c+3,3))][1][z])
												if ab >= max_u:
													max_u = ab
													best_action = i
										else:
											suc_prob = []
											for ii in prob_move[a]:
												suc_prob.append(float(ii)/100)
											
											ab = MM_dd*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][y][z]) + MM_dr*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][1][z]) + MM_dd*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][y][z]) + MM_dr*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][1][z])
											if ab >= max_u:
												max_u = ab
												best_action = i
									elif d == 'R':
										if i == 'C':
											if b != 0 and c < 3:
												ab = step_cost + MM_rr*gamma*(0.5*utility[v][w-1][arrows.index(min(c+1,3))][y][z] + 0.35*utility[v][w-1][arrows.index(min(c+2,3))][y][z] + 0.15*utility[v][w-1][arrows.index(min(c+3,3))][y][z]) + MM_rd*gamma*(0.5*utility[v][w-1][arrows.index(min(c+1,3))][0][z] + 0.35*utility[v][w-1][arrows.index(min(c+2,3))][0][z] + 0.15*utility[v][w-1][arrows.index(min(c+3,3))][0][z])
												if ab >= max_u:
													max_u = ab
													best_action = i
										else:
											suc_prob = []
											for ii in prob_move[a]:
												suc_prob.append(float(ii)/100)
												aa = suc_prob[0]
											ab = MM_rr*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][y][z]) + MM_rr*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][1][z]) + MM_rd*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][0][z]) + MM_rd*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][0][z]) 
											if ab >= max_u:
												max_u = ab
												best_action = i
								if best_action =='A' or best_action =='B' or best_action =='G' or best_action =='C':
									action[v][w][x][y][z] = action_ctoi(best_action)
								else:
									num = 0
									if best_action == 'N':
										num = action_ctoi("s")
									elif best_action == 'O':
										num = action_ctoi("d")
									action[v][w][x][y][z] = num
								temp_utility[v][w][x][y][z] = max_u
							elif a == 'S':
								max_u = -10000000000
								best_action = ''
								for i in allowed_moves[a]:
									if d == 'D':
										if i == 'G':
											if b < 2:
												ab = step_cost + MM_dd*gamma*(0.75*utility[v][materials.index(min(w+1,2))][x][y][z] + 0.25*utility[v][w][x][y][z]) + MM_dr*gamma*(0.75*utility[v][materials.index(min(w+1,2))][x][1][z] + 0.25*utility[v][w][x][1][z])
												if ab >= max_u:
													max_u = ab
													best_action = i
										else:
											suc_prob = []
											for ii in prob_move[a]:
												suc_prob.append(float(ii)/100)
											ab = MM_dd*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][y][z]) + MM_dr*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][1][z]) + MM_dd*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][y][z]) + MM_dr*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][1][z])
											if ab >= max_u:
												max_u = ab
												best_action = i
									elif d == 'R':
										if i == 'G':
											if b < 2:
												ab = step_cost + MM_rr*gamma*(0.75*utility[v][materials.index(min(w+1,2))][x][y][z] + 0.25*utility[v][w][x][y][z]) + MM_rd*gamma*(0.75*utility[v][materials.index(min(w+1,2))][x][0][z] + 0.25*utility[v][w][x][0][z])
												if ab >= max_u:
													max_u = ab
													best_action = i
										else:
											suc_prob = []
											for ii in prob_move[a]:
												suc_prob.append(float(ii)/100)
											ab = MM_rr*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][y][z]) + MM_rr*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][1][z]) + MM_rd*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][0][z]) + MM_rd*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][0][z]) 
											if ab >= max_u:
												max_u = ab
												best_action = i
								if best_action =='A' or best_action =='B' or best_action =='G' or best_action =='C':
									action[v][w][x][y][z] = action_ctoi(best_action)
								else:
									num = 0
									if best_action == 'S':
										num = action_ctoi("s")
									elif best_action == 'O':
										num = action_ctoi("u")
									action[v][w][x][y][z] = num
								temp_utility[v][w][x][y][z] = max_u
							elif a == 'E':
								max_u = -10000000000
								best_action = ''
								for i in allowed_moves[a]:
									if d == 'D':
										if i == 'A':
											if x>0:
												if e > 25:# ek cheeze discuss karni thi yeh neeche vali
													ab =  step_cost + MM_dd*gamma*(0.9*utility[v][w][x-1][y][health.index(e-25)]+0.1*utility[v][w][x-1][y][z]) + MM_dr*gamma*(0.9*utility[v][w][x-1][1][health.index(e-25)]+0.1*utility[v][w][x-1][1][z]) 
												else:
													ab = 0.9*kill_reward + step_cost + MM_dd*gamma*(0.9*utility[v][w][x-1][y][0]+ 0.1*utility[v][w][x-1][y][z]) + MM_dr*gamma*(0.9*utility[v][w][x-1][1][0]+ 0.1*utility[v][w][x-1][1][z])
												if ab >= max_u:
													max_u = ab
													best_action = i
										elif i == 'B':
											if e > 50:
												ab =  step_cost + MM_dd*gamma*(0.2*utility[v][w][x][y][health.index(e-50)]+ 0.8*utility[v][w][x][y][z]) + MM_dr*gamma*(0.2*utility[v][w][x][1][health.index(e-50)]+ 0.8*utility[v][w][x][1][z])
											else:
												ab = 0.2*kill_reward + step_cost + MM_dd*gamma*(0.2*utility[v][w][x][y][0]+ 0.8*utility[v][w][x][y][z]) + MM_dr*gamma*(0.2*utility[v][w][x][1][0]+ 0.8*utility[v][w][x][1][z])
											if ab >= max_u:
												max_u = ab
												best_action = i	
										else:
											suc_prob = []
											for ii in prob_move[a]:
												suc_prob.append(float(ii)/100)
											ab = MM_dd*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][y][z]) + MM_dr*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][1][z]) + MM_dd*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][y][z]) + MM_dr*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][1][z])
											if ab >= max_u:
												max_u = ab
												best_action = i
									elif d == 'R':
										if i == 'A':
											if x>0:
												if e > 25:# ek cheeze discuss karni thi yeh neeche vali
													ab =  step_cost + MM_rr*gamma*(0.9*utility[v][w][x-1][y][health.index(e-25)]+0.1*utility[v][w][x-1][y][z]) + MM_rd*(hit_reward) + MM_rd*gamma*(utility[v][w][0][0][health.index(min(e+25,100))])
												else:
													ab = MM_rd*0.9*kill_reward + step_cost + MM_rr*gamma*(0.9*utility[v][w][x-1][y][0]+ 0.1*utility[v][w][x-1][y][z]) + MM_rd*(hit_reward) + MM_rd*gamma*(utility[v][w][0][0][health.index(min(e+25,100))])
												if ab >= max_u:
													max_u = ab
													best_action = i
										elif i == 'B':
											if e > 50:
												ab =  step_cost + MM_rr*gamma*(0.2*utility[v][w][x][y][health.index(e-50)]+ 0.8*utility[v][w][x][y][z]) + MM_rd*(hit_reward) + MM_rd*gamma*(utility[v][w][0][0][health.index(min(e+25,100))])
											else:
												ab = MM_rd*0.2*kill_reward + step_cost + MM_rr*gamma*(0.2*utility[v][w][x][y][0]+ 0.8*utility[v][w][x][y][z]) + MM_rd*(hit_reward) + MM_rd*gamma*(utility[v][w][0][0][health.index(min(e+25,100))])
											if ab >= max_u:
												max_u = ab
												best_action = i	
										else:
											suc_prob = []
											for ii in prob_move[a]:
												suc_prob.append(float(ii)/100)
											ab = MM_rr*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][y][z]) + MM_rr*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][1][z]) + MM_rd*(hit_reward) + MM_rd*gamma*(step_cost + utility[v][w][0][0][health.index(min(e+25,100))])
											if ab >= max_u:
												max_u = ab
												best_action = i
								if best_action =='A' or best_action =='B' or best_action =='G' or best_action =='C':
									action[v][w][x][y][z] = action_ctoi(best_action)
								else:
									num = 0
									if best_action == 'E':
										num = action_ctoi("s")
									elif best_action == 'O':
										num = action_ctoi("l")
									action[v][w][x][y][z] = num
								temp_utility[v][w][x][y][z] = max_u
							else:
								max_u = -10000000000
								best_action = ''
								for i in allowed_moves[a]:
									if d == 'D':
										if i == 'A':
											if x>0:
												if e > 25:
													ab =  step_cost + MM_dd*gamma*(0.25*utility[v][w][x-1][y][health.index(e-25)]+0.75*utility[v][w][x-1][y][z]) + MM_dr*gamma*(0.25*utility[v][w][x-1][1][health.index(e-25)]+0.75*utility[v][w][x-1][1][z]) 
												else:
													ab = 0.25*kill_reward + step_cost + MM_dd*gamma*(0.25*utility[v][w][x-1][y][0]+ 0.75*utility[v][w][x-1][y][z]) + MM_dr*gamma*(0.25*utility[v][w][x-1][1][0]+ 0.75*utility[v][w][x-1][1][z])
												if ab >= max_u:
													max_u = ab
													best_action = i
										else:
											suc_prob = []
											for ii in prob_move[a]:
												suc_prob.append(float(ii)/100)
											ab = MM_dd*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][y][z]) + MM_dr*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][1][z]) + MM_dd*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][y][z]) + MM_dr*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][1][z])
											if ab >= max_u:
												max_u = ab
												best_action = i
									elif d == 'R':
										if i == 'A':
											if x>0:
												if e > 25:
													ab =  step_cost + MM_rr*gamma*(0.25*utility[v][w][x-1][y][health.index(e-25)]+0.75*utility[v][w][x-1][y][z]) + MM_rd*gamma*(0.25*utility[v][w][x-1][0][health.index(e-25)]+0.75*utility[v][w][x-1][0][z]) 
												else:
													ab = 0.25*kill_reward + step_cost + MM_rr*gamma*(0.25*utility[v][w][x-1][y][0]+ 0.75*utility[v][w][x-1][y][z]) + MM_rd*gamma*(0.25*utility[v][w][x-1][0][0]+ 0.75*utility[v][w][x-1][0][z])
												if ab >= max_u:
													max_u = ab
													best_action = i
										else:
											suc_prob = []
											for ii in prob_move[a]:
												suc_prob.append(float(ii)/100)
											ab = MM_rr*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][y][z]) + MM_rr*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][1][z]) + MM_rd*suc_prob[0]*(step_cost + gamma*utility[possible_states.index(i)][w][x][0][z]) + MM_rd*suc_prob[1]*(step_cost + gamma*utility[possible_states.index('E')][w][x][0][z]) 
											if ab >= max_u:
												max_u = ab
												best_action = i
								if best_action =='A' or best_action =='B' or best_action =='G' or best_action =='C':
									action[v][w][x][y][z] = action_ctoi(best_action)
								else:
									num = 0
									if best_action == 'W':
										num = action_ctoi("s")
									elif best_action == 'O':
										num = action_ctoi("r")
									action[v][w][x][y][z] = num
								temp_utility[v][w][x][y][z] = max_u 
							if (abs(temp_utility[v][w][x][y][z] - utility[v][w][x][y][z]) > error):
								error = abs(temp_utility[v][w][x][y][z] - utility[v][w][x][y][z])
						else:
							action[v][w][x][y][z] = 0
						ax = a
						if a=='O':
							ax = 'C'
						print("(" + str(ax) +","+ str(b) + "," + str(c) +"," +str(d) +"," + str(e) +") : "+ str(action_itop(action[v][w][x][y][z]))+ "=["+ str(round(temp_utility[v][w][x][y][z],3))+ "]" ,file =f )
                        # print("(", a ,",", b,",", c,",", d,",", e ,") : ", action_itop(action[v][w][x][y][z]), "=[", temp_utility[v][w][x][y][z], "]")
	np.copyto(utility, temp_utility)
	# print(str(error) + " "+ str(iteration) + '\n')
	# break
f.close()





# NOT CODE BELOW ---------------------------------------------------------------------------------------------------
# problity_to_move = {
#   'NE':15/100,
#   'NC':85/200,
#   'NN':85/200,
#   'SE':15/100,
#   'SC':85/200,
#   'SS':85/200,
#   'EE':50/100,
#   'EC':50/100,
#   'WC':50/100,
#   'WW':50/100,
#   'CC':17/100,
#   'CW':17/100,
#   'CN':17/100,
#   'CS':17/100,
#   'CE':32/100,
# }
