#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install pulp


# ### **Production time per unit(h)**
# 
# Sectors 1 2 3 4 Production time available per week(h) 
# 
# A 1.5 2.2 1.3 2.2 27
# 
# B 1.3 2.5 1.3 2.6 33
# 
# C 1.9 1.6 1.2 1.1 22
# 
# Profits per unit($)/25/34/24/33/
# 
# ### **a) Formulate an LP model to find an optimal product mix**
# 
# * Maximize P = 25x_1 + 34x_2 + 24x_3 + 33x_4
# 
# * 1.5x_1 + 2.2x_2 + 1.3x_3 + 2.2x_4 <= 27 Sector A
# 
# * 1.3x_1 + 2.5x_2 + 1.3x_3 + 2.6x_4 <= 33 Sector B
# 
# * 1.9x_1 + 1.6x_2 + 1.2x_3 + 1.1x_4 <= 22 Sector C
# 
# * x_1, x_2, x_3, x_4 >= 0
# 
# 
# 
# 

# ### **b)**

# In[2]:


from pulp import *

# Creating the maximization problem called Term_Project_1
prob = LpProblem("Term_Project_1", LpMaximize)

# Defining decision variables
X1 = LpVariable("Product_1", 0, None, LpInteger)  
X2 = LpVariable("Product_2", 0, None, LpInteger) 
X3 = LpVariable("Product_3", 0, None, LpInteger)  
X4 = LpVariable("Product_4", 0, None, LpInteger)  

# Adding objective function
prob += 25*X1 + 34*X2 + 24*X3 + 33*X4, "Total_Profit"

# Adding constraints to the problem
prob += 1.5*X1 + 2.2*X2 + 1.3*X3 + 2.2*X4 <= 27, "Sector_A"
prob += 1.3*X1 + 2.5*X2 + 1.3*X3 + 2.6*X4 <= 33, "Sector_B"
prob += 1.9*X1 + 1.6*X2 + 1.2*X3 + 1.1*X4 <= 22, "Sector_C"

# Applying .solve() method
prob.solve()

# Showing the status of the problem
print("Status:", LpStatus[prob.status])

# Showing the values of variables
for v in prob.variables():
    print(v.name, "=", v.varValue)

# Multiplying constraints with values
print("Used production time in Sector A = ", 1.5*X1.varValue + 2.2*X2.varValue + 1.3*X3.varValue + 2.2*X4.varValue)
print("Used production time in Sector B = ", 1.3*X1.varValue + 2.5*X2.varValue + 1.3*X3.varValue + 2.6*X4.varValue)
print("Used production time in Sector C = ", 1.9*X1.varValue + 1.6*X2.varValue + 1.2*X3.varValue + 1.1*X4.varValue)

# Showing the optimal value
print("Total profit = ", value(prob.objective))


# ### **c)**

# In[3]:



import pandas as pd
data = pd.read_excel('termproject.xlsx')
data = data.T


# In[ ]:


data.columns = data.iloc[0]
data = data.drop(data.index[0])
data


# In[ ]:


# Production times and profits
production_times = data.iloc[0:4, 0:3]
profits = data.iloc[0:4, 3]
production_available = data.loc['Production time available per week(h)', 'A':'C']

prob = LpProblem("Product_Mix_Problem", LpMaximize)

# Adding variables to the problem
products = LpVariable.dicts("Product", [1, 2, 3, 4], 0, None, LpInteger)

# Adding objective function to the problem
prob += lpSum([profits[i+1]*products[i+1] for i in range(4)]), "Total_Profit"

# Adding constraints to the problem
for i in range(3):
    prob += lpSum([production_times.loc[j+1, chr(65+i)]*products[j+1] for j in range(4)]) <= production_available[chr(65+i)], f"Sector_{chr(65+i)}"

prob.solve()

print("Status:", LpStatus[prob.status])

# Assigning values to variables
for v in prob.variables():
    print(v.name, "=", v.varValue)

# Showing the used production time in each sector
for i in range(3):
    print(f"Used production time in Sector {chr(65+i)} = ", sum([production_times.loc[j+1, chr(65+i)]*products[j+1].varValue for j in range(4)]))

# Showing the optimal value
print("Total profit = ", value(prob.objective))


# ### **d) Interpret the shadow price of each constraint.**
# 

# In[ ]:


print("Shadow Prices")
# Indicating shadow prices
for name, constraint in prob.constraints.items():
    print(name, ":", constraint.pi)


#  ### **e) If the profit of product 2 were to increase by 1 dollar and product 3 were to decrease 1 dollar what would be the new optimal solution to the problem?**

# 

# In[ ]:


# Creating a new problem to apply sensitivity analysis
prob2 = LpProblem("Product_Mix_Problem_e", LpMaximize)

# Defining decision variables
X1 = LpVariable("Product_1", 0, None, LpInteger)
X2 = LpVariable("Product_2", 0, None, LpInteger)
X3 = LpVariable("Product_3", 0, None, LpInteger)
X4 = LpVariable("Product_4", 0, None, LpInteger)

# Adding objective function
prob2 += 25*X1 + 35*X2 + 23*X3 + 33*X4, "Total_Profit"

prob2 += 1.5*X1 + 2.2*X2 + 1.3*X3 + 2.2*X4 <= 27, "Sector_A"
prob2 += 1.3*X1 + 2.5*X2 + 1.3*X3 + 2.6*X4 <= 33, "Sector_B"
prob2 += 1.9*X1 + 1.6*X2 + 1.2*X3 + 1.1*X4 <= 22, "Sector_C"

# Applying .solve() method
prob2.solve()

# Showing the status of the problem
print("Status:", LpStatus[prob2.status])

# Showing the values of variables
for v in prob2.variables():
    print(v.name, "=", v.varValue)

# Multiplying constraints with values
print("Used production time in Sector A = ", 1.5*X1.varValue + 2.2*X2.varValue + 1.3*X3.varValue + 2.2*X4.varValue)
print("Used production time in Sector B = ", 1.3*X1.varValue + 2.5*X2.varValue + 1.3*X3.varValue + 2.6*X4.varValue)
print("Used production time in Sector C = ", 1.9*X1.varValue + 1.6*X2.varValue + 1.2*X3.varValue + 1.1*X4.varValue)

# Showing the optimal value
print("Total profit = ", value(prob2.objective)) 


# In[ ]:


# SENSITIVITY ANALYSIS

# Remove the existing objective function
prob2.objective = None

# Update the profit coefficients for product 2 and product 3
prob2 += 25*X1 + 35*X2 + 23*X3 + 33*X4, "Total_Profit"

# Solve the modified problem
prob2.solve()

# Showing the status of the problem
print("Status:", LpStatus[prob2.status])

# Showing the values of variables
for v in prob2.variables():
    print(v.name, "=", v.varValue)

# Multiplying constraints with values
print("Used production time in Sector A =", 1.5*X1.varValue + 2.2*X2.varValue + 1.3*X3.varValue + 2.2*X4.varValue)
print("Used production time in Sector B =", 1.3*X1.varValue + 2.5*X2.varValue + 1.3*X3.varValue + 2.6*X4.varValue)
print("Used production time in Sector C =", 1.9*X1.varValue + 1.6*X2.varValue + 1.2*X3.varValue + 1.1*X4.varValue)

# Showing the new optimal value
print("Total profit =", value(prob2.objective))


# ### **f) If the profit of product 1 were to increase by 1 dollar and product 2 , product 3, product4 is decreased by 1 dollar  each what would be the new optimal solution to the problem?**

# In[ ]:


# Creating a new problem to apply sensitivity analysis
prob3 = LpProblem("Product_Mix_Problem_f", LpMaximize)

# Defining decision variables
X1 = LpVariable("Product_1", 0, None, LpInteger)
X2 = LpVariable("Product_2", 0, None, LpInteger)
X3 = LpVariable("Product_3", 0, None, LpInteger)
X4 = LpVariable("Product_4", 0, None, LpInteger)

# Adding objective function
prob3 += 26*X1 + 33*X2 + 23*X3 + 32*X4, "Total_Profit"

prob3 += 1.5*X1 + 2.2*X2 + 1.3*X3 + 2.2*X4 <= 27, "Sector_A"
prob3 += 1.3*X1 + 2.5*X2 + 1.3*X3 + 2.6*X4 <= 33, "Sector_B"
prob3 += 1.9*X1 + 1.6*X2 + 1.2*X3 + 1.1*X4 <= 22, "Sector_C"

# Applying .solve() method
prob3.solve()

# Showing the status of the problem
print("Status:", LpStatus[prob2.status])

# Showing the values of variables
for v in prob3.variables():
    print(v.name, "=", v.varValue)

# Multiplying constraints with values
print("Used production time in Sector A = ", 1.5*X1.varValue + 2.2*X2.varValue + 1.3*X3.varValue + 2.2*X4.varValue)
print("Used production time in Sector B = ", 1.3*X1.varValue + 2.5*X2.varValue + 1.3*X3.varValue + 2.6*X4.varValue)
print("Used production time in Sector C = ", 1.9*X1.varValue + 1.6*X2.varValue + 1.2*X3.varValue + 1.1*X4.varValue)

# Showing the optimal value
print("Total profit = ", value(prob3.objective)) 


# In[ ]:


#SENSITIVITY ANALYSIS

# Removing the existing objective function
prob3.objective = None

# Updating the profit coefficients for product 1, product 2, product 3, product 4
prob3 += 26*X1 + 33*X2 + 23*X3 + 32*X4, "Total_Profit"

# Applying .solve() method
prob3.solve()

# Showing the status of the problem
print("Status:", LpStatus[prob3.status])

# Showing the values of variables
for v in prob3.variables():
    print(v.name, "=", v.varValue)

# Multiplying constraints with values
print("Used production time in Sector A =", 1.5*X1.varValue + 2.2*X2.varValue + 1.3*X3.varValue + 2.2*X4.varValue)
print("Used production time in Sector B =", 1.3*X1.varValue + 2.5*X2.varValue + 1.3*X3.varValue + 2.6*X4.varValue)
print("Used production time in Sector C =", 1.9*X1.varValue + 1.6*X2.varValue + 1.2*X3.varValue + 1.1*X4.varValue)

# Showing the new optimal value
print("Total profit =", value(prob3.objective))


# ### **g) The company's R&D team develops product 5 and makes it much more profitable. The profit of new product 5 is $40 and spends 1 hour/unit in each sector. What would be the new optimal solution to the problem? Explain how new product 5 had an impact on the company's profit.**
# 

# In[ ]:


prob4 = LpProblem("Product_Mix_Problem_4", LpMaximize)

X2 = LpVariable("Product_2", 0, None, LpInteger)
X3 = LpVariable("Product_3", 0, None, LpInteger)
X4 = LpVariable("Product_4", 0, None, LpInteger)
X5 = LpVariable("Product_5", 0, None, LpInteger)  # yeni

prob4 += 25*X1 + 34*X2 + 24*X3 + 33*X4 + 40*X5, "Total_Profit"

prob4 += 1.5*X1 + 2.2*X2 + 1.3*X3 + 2.2*X4 + 1*X5 <= 27, "Sector_A"
prob4 += 1.3*X1 + 2.5*X2 + 1.3*X3 + 2.6*X4 + 1*X5 <= 33, "Sector_B"
prob4 += 1.9*X1 + 1.6*X2 + 1.2*X3 + 1.1*X4 + 1*X5 <= 22, "Sector_C"

prob4.solve()

print("Status:", LpStatus[prob4.status])

for v in prob4.variables():
    print(v.name, "=", v.varValue)

print("Used production time in Sector A = ", 1.5*X1.varValue + 2.2*X2.varValue + 1.3*X3.varValue + 2.2*X4.varValue + 1*X5.varValue)
print("Used production time in Sector B = ", 1.3*X1.varValue + 2.5*X2.varValue + 1.3*X3.varValue + 2.6*X4.varValue + 1*X5.varValue)
print("Used production time in Sector C = ", 1.9*X1.varValue + 1.6*X2.varValue + 1.2*X3.varValue + 1.1*X4.varValue + 1*X5.varValue)

print("Total profit = ", value(prob4.objective))


# In[ ]:





# In[ ]:





# In[ ]:




