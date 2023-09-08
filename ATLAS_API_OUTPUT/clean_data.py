import numpy as np
import pandas as pd
import csv

df_TNS = pd.read_csv('/project2/rkessler/SURVEYS/LSST/USERS/lmercadante/ATLAS_DATA_PROJECT/TNS_GET_OUTPUT/object_get_out_50.csv', sep = ',')

MJD_peak_list = df_TNS['MJD'] 
RA_list = df_TNS['RA(deg)']
DEC_list = df_TNS['DEC(deg)']
Redshift_list = df_TNS['SN_Redshift']

MJD_pass = []
RA_pass = []
DEC_pass = []
Redshift_pass = []

df1 = pd.read_csv('/project2/rkessler/SURVEYS/LSST/USERS/lmercadante/ATLAS_DATA_PROJECT/ATLAS_API_OUTPUT/RAW_DATA/file_list.csv', sep = ',')
name_list = df1['SN_Name']
print(name_list)

names_pass = []

file_list = df1['File_Name']
print(file_list)

path = '/project2/rkessler/SURVEYS/LSST/USERS/lmercadante/ATLAS_DATA_PROJECT/ATLAS_API_OUTPUT/CLEAN_DATA/'

raw_path = '/project2/rkessler/SURVEYS/LSST/USERS/lmercadante/ATLAS_DATA_PROJECT/ATLAS_API_OUTPUT/RAW_DATA/'
for i in range(0,len(file_list)):
    df = pd.read_csv(raw_path + file_list[i], sep=",")
    print(file_list[i])
    mjd_list = df['MJD']
    MJD_peak = MJD_peak_list[i]
    
    val_list_c = []
    val_list_o = []

    filter_list = df['F']
    
    ind = []
    mag_ab = []
    mag_err = []
    mjd = []
    uJy = []
    duJy = []
    f = []
    err = []
    chi_N = []
    ra = []
    dec = []
    x = []
    y = []
    maj = []
    Min = []
    phi = []
    apfit = []
    mag5sig = []
    sky = []
    obs = []

    for index, row in df.iterrows():
        MJD = row[1]
        MAG_AB = row[2]
        MAG_ERR = row[3]
        F = row[6]

        IND = row[0]
        UJY = row[4]
        DUJY = row[5]
        ERR = row[7]
        CHI_N = row[8]
        RA = row[9]
        DEC = row[10]
        X = row[11]
        Y = row[12]
        MAJ = row[13]
        MIN = row[14]
        PHI = row[15]
        APFIT = row[16]
        MAG5SIG = row[17]
        SKY = row[18]
        OBS = row[19]

        if MAG_AB < 0 or MAG_ERR > 1:
            continue

        elif F =='c':
            if MJD > MJD_peak - 10 and MJD < MJD_peak + 10:
                val_list_c.append(True)
        elif F =='o':
            if MJD > MJD_peak - 10 and MJD < MJD_peak + 10:
                val_list_o.append(True)
        else:
            mag_ab.append(MAG_AB)
            mag_err.append(MAG_ERR)
            mjd.append(MJD)
            ind.append(IND)
            uJy.append(UJY)
            duJy.append(DUJY)
            f.append(F)
            err.append(ERR)
            chi_N.append(CHI_N)
            ra.append(RA)
            dec.append(DEC)
            x.append(X)
            y.append(Y)
            maj.append(MAJ)
            Min.append(MIN)
            phi.append(PHI)
            apfit.append(APFIT)
            mag5sig.append(MAG5SIG)
            sky.append(SKY)
            obs.append(OBS)

    if True in val_list_c:
        print('Passes c cut')
    else:
        print('Fails c cut')
        continue
    if True in val_list_o:
        print('Passes o cut')
    else:
        print('Fails o cut')
        continue

    names_pass.append(name_list[i])
    RA_pass.append(RA_list[i])
    DEC_pass.append(DEC_list[i])
    MJD_pass.append(MJD_peak_list[i])
    Redshift_pass.append(Redshift_list[i])
    header = ['Index', 'MJD', 'm','dm','uJy','duJy', 'F', 'err', 'chi/N', 'RA', 'Dec', 'x', 'y', 'maj', 'min', 'phi', 'apfit', 'mag5sig', 'Sky', 'Obs']
    print(i)
    with open(path + name_list[i] +'_c.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        for i in range(0,len(ind)):
            row = [str(ind[i]),str(mjd[i]),str(mag_ab[i]),str(mag_err[i]),str(uJy[i]),str(duJy[i]),str(f[i]),str(err[i]),str(chi_N[i]),str(ra[i]),str(dec[i]),str(x[i]),str(y[i]),str(maj[i]),str(Min[i]),str(phi[i]),str(apfit[i]),str(mag5sig[i]),str(sky[i]),str(obs[i])]
            print(row)
            csvwriter.writerow(row)

header2 = ['File_Name','SN_Name']
with open(path +'file_list_c.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header2)
    for i in range(0,len(names_pass)):
        row = [str(names_pass[i])+'_c.csv', str(names_pass[i])]
        csvwriter.writerow(row)

header3 = ['Name','RA(deg)','DEC(deg)','MJD','SN_Redshift']
with open(path +'TNS_info_c.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header3)
    for i in range(0,len(names_pass)):
        row = [str(names_pass[i]),RA_pass[i],DEC_pass[i],MJD_pass[i],Redshift_pass[i]]
        csvwriter.writerow(row)
    
