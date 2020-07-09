import numpy as np
def ipixLoader(data,pol,rangebin,mode):
    H_txpol     = 0; 
    V_txpol     = 1;
    Like_adc_I  = 0;  # when use data of 93 set these parameters(L_I,L_Q,C_I,C_Q) to 1 2 3 4;
    Like_adc_Q  = 1;  # when use data of 98 set these parameters(L_I,L_Q,C_I,C_Q) to 3 4 1 2;
    Cross_adc_I = 2;
    Cross_adc_Q = 3;

    #%% extract correct polarization from cdffile %%


    pol = pol.lower();
    if pol == 'hh':
        xiq = data[ :,H_txpol,rangebin,[Like_adc_I, Like_adc_Q]]
    elif pol == 'hv': 
        xiq = data[:,H_txpol,rangebin,[Cross_adc_I, Cross_adc_Q]];
    elif pol ==  'vv': 
        xiq = data[:,V_txpol,rangebin,[Like_adc_I, Like_adc_Q]];
    elif pol ==  'vh': 
        xiq = data[:,V_txpol,rangebin,[Cross_adc_I, Cross_adc_Q]];
    I = xiq[:,0];
    Q = xiq[:,1];
    I = np.double(I);
    Q = np.double(Q);
    if mode == 'auto':
        # Pre-processing     
        meanI, meanQ = np.mean(I), np.mean(Q);
        stdI, stdQ = np.std(I), np.std(Q);
        I = (I - meanI) / stdI;
        Q = (Q - meanQ) / stdQ;
        sin_inbal = np.mean(I*Q);
        inbal = np.arcsin(sin_inbal) * 180 / np.pi;
        I = (I - Q * sin_inbal) / np.sqrt(1 - sin_inbal**2);
        return [I,Q,[meanI, meanQ],[stdI, stdQ],inbal]
