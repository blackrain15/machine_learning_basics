import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Read the input file having 3 columns - Area, # of Rooms and Cost in $1000
mydata = pd.read_csv("housepricedata.csv")

layer1_vals = np.array(mydata.iloc[:,0:3])
layer1_vals = layer1_vals.astype(float)

layer1_vals[:,0] = list(map((lambda x : ((x - np.median(layer1_vals[:,0]))/max(layer1_vals[:,0]))),layer1_vals[:,0]))
layer1_vals[:,1] = list(map((lambda x : ((x - np.median(layer1_vals[:,1]))/max(layer1_vals[:,1]))),layer1_vals[:,1]))
layer1_vals[:,2] = list(map((lambda x : ((x - np.median(layer1_vals[:,2]))/max(layer1_vals[:,2]))),layer1_vals[:,2]))

layer1_vals = np.transpose(layer1_vals)

output_act_vals = np.array(mydata.iloc[:,3])
output_act_vals = output_act_vals.reshape(1,len(mydata))

layer2_vals = np.ones((5,len(mydata)))
layer3_vals = np.ones((5,len(mydata)))

output_pred_vals = np.ones((1,len(mydata)))

bias_layer1 = np.random.random(5*len(mydata))
bias_layer1 = bias_layer1.reshape(5,len(mydata))

weights_layer1 = np.random.random(15)
weights_layer1 = weights_layer1.reshape(5,3)

bias_layer2 = np.random.random(5*len(mydata))
bias_layer2 = bias_layer2.reshape(5,len(mydata))

weights_layer2 = np.random.random(25)
weights_layer2 = weights_layer2.reshape(5,5)

bias_layer3 = np.random.random(len(mydata))
bias_layer3 = bias_layer3.reshape(1,len(mydata))

weights_layer3 = np.random.random(5)
weights_layer3 = weights_layer3.reshape(1,5)

alpha = 0.000001
cost_list = []
counter=0

while(True):

    for i in range(len(mydata)):
        for j in range(5):
            val = 0
            for k in range(3):
                val = val + layer1_vals[k,i]*weights_layer1[j,k]
            
            layer2_vals[j,i] += bias_layer1[j,i]
            layer2_vals[j,i] = 1/(1+np.exp(-val))
    
    for i in range(len(mydata)):
        for j in range(5):
            val = 0
            for k in range(5):
                val = val + layer2_vals[k,i]*weights_layer2[j,k]
                
            layer3_vals[j,i] += bias_layer2[j,i]
            layer3_vals[j,i] = 1/(1+np.exp(-val))
    
    for i in range(len(mydata)):
        for j in range(1):
            val = 0
            for k in range(5):
                val = val + layer3_vals[k,i]*weights_layer3[j,k]
                
            output_pred_vals[j,i] += bias_layer3[j,i]
            output_pred_vals[j,i] = 1/(1+np.exp(-val))
            
    cost = 0
    for i in range(len(mydata)):
        cost = cost + (output_act_vals[0,i]*np.log(output_pred_vals[0,i]) + (1-output_act_vals[0,i])*(1-np.log(output_pred_vals[0,i])))
    
    cost = -cost/len(mydata)
    cost_list.append(cost)
    counter+= 1
    
    del_layer4 = (output_pred_vals - output_act_vals)
    del_weights_layer3 = np.matmul(del_layer4, np.transpose(layer3_vals))
    
    bias_layer3 -= alpha * del_layer4
    
    del_layer3 = np.multiply(np.matmul(np.transpose(weights_layer3), del_layer4), np.multiply(layer3_vals, (np.ones((5,1460))-layer3_vals)))
    del_weights_layer2 = np.matmul(del_layer3, np.transpose(layer2_vals))
    
    bias_layer2 -= alpha * del_layer3
    
    del_layer2 = np.multiply(np.matmul(np.transpose(weights_layer2), del_layer3), np.multiply(layer2_vals, (np.ones((5,1460))-layer2_vals)))
    del_weights_layer1 = np.matmul(del_layer2, np.transpose(layer1_vals))
    
    bias_layer1 -= alpha * del_layer2
    
    weights_layer1 = weights_layer1 - alpha * del_weights_layer1
    weights_layer2 = weights_layer2 - alpha * del_weights_layer2
    weights_layer3 = weights_layer3 - alpha * del_weights_layer3
   
    if(counter>2):
        if(abs(cost_list[counter-2]-cost_list[counter-1])<0.0000001):
            break
        #if(counter>200):
            #break
        
fig, axes = plt.subplots(nrows=2, ncols =1, figsize = (12,8))

axes[0].plot(cost_list, color = 'g')
axes[0].set_xlabel("# of Iters")
axes[0].set_ylabel("Cost Func.")
axes[0].set_title("Cost vs. # of Iters.")