import random
import numpy as np
import copy
def constkontrol(x):
    count=0
    if 7*x[0]+2*x[1]<=240:
        count+=1
    if x[0]+2*x[1]>=80:  
        
       count+=1
        
    if 3*x[0]+x[1]==90:  
        
        count+=1      
    if x[0]>=0 and x[1]>=0:  
        
        count+=1
    if count==4:
        return 0
    else:
        
        return 1
    
def objectiveFu(x):
    
    return 3*x[0]+5*x[1]

def grey_wolf_optimizer(obj_function, lb, ub, dim, search_agents, max_iter,esitlik,cons=90):
    bestobj=1000000
    objs=[]
    # obj_function: optimize edilecek fonksiyon
    # lb: alt sınır limitleri (lower bounds)
    # ub: üst sınır limitleri (upper bounds)
    # dim: boyut sayısı
    # search_agents: arama ajanlarının sayısı
    # max_iter: iterasyon sayısı
    positions = [[random.uniform(lb[i], ub[i]) for i in range(dim)] for j in range(search_agents)]
    positionsC=copy.deepcopy(positions)
    # Başlangıç konumlarını rastgele seçme
    for i in range(search_agents):
        while True:
                numbers=[random.uniform(0, ub[i]) for i in range(dim)]
                # eğer eşitlik var ise kısıtlarda:
                if esitlik==1:
                    summ=cons/(numbers[0]*3+numbers[1])
                    
                    numbers[0]=numbers[0]*summ
                    numbers[1]=numbers[1]*summ
                    
                durum=constkontrol(numbers)
                            
                if durum==0:
                
                    positions[i] = numbers
                    break
  
    convergence_curve = []
    
    # Ana döngü
    for l in range(max_iter):
        # Fonksiyon değerlerini hesapla
        obj_values = []
        a=2*(1-l/max_iter)
        for i in range(search_agents):
          
            numbers=positions[i]
            durum=constkontrol(numbers)
            if durum==1:
             
                positions[i]=positionsC[i]
                        
            # Hedef fonksiyonun değerini hesapla
            obj_values.append(obj_function(positions[i]))

                    
                    
        alpha, beta, delta = None, None, None
        positionsC=copy.deepcopy(positions)
        if bestobj>min(obj_values):
            

              
                bestobj=min(obj_values)
                best_position =  positionsC[np.argmin(obj_values)].copy()

        # En iyi üç kurtu seç
        sorted_positions = [positions[i] for i in sorted(range(len(obj_values)), key=lambda k: obj_values[k])]
        alpha, beta, delta = sorted_positions[0], sorted_positions[1], sorted_positions[2]
        
        # Ajanların hareketlerini güncelle
        for i in range(search_agents):
            for j in range(dim):
                A1, C1 = a*2 * random.random() - 1, a*2 * random.random()
                D_alpha, D_beta, D_delta = abs(C1 * alpha[j] - positions[i][j]), abs(C1 * beta[j] - positions[i][j]), abs(C1 * delta[j] - positions[i][j])
                X1 = alpha[j] - A1 * D_alpha
                X2 = beta[j] - A1 * D_beta
                X3 = delta[j] - A1 * D_delta
                positions[i][j] = (X1 + X2 + X3) / 3.0
        
        convergence_curve.append(min(obj_values))
       
    


    
    
    return best_position,bestobj, convergence_curve,objs

lb=[0,0]

ub=[1000,1000]
a,b,c,d=grey_wolf_optimizer(objectiveFu, lb, ub, 2, 30, 500,1,90)