import os
import pandas as pd


class IntraCrossTalk:
    def __init__(self, Pro_name, UniprotId, Site1, Site1Type, Site2, Site2Type):
        self.Pro_name = Pro_name
        self.UniprotId = UniprotId
        self.UniprotSite1 = int(Site1[1:])
        self.UniprotSite1Type = Site1Type
        self.UniprotSite2 = int(Site2[1:])
        self.UniprotSite2Type = Site2Type
        # self.items = items  # 其他信息
        self.uniprot1_evol_feature = dict()
        self.uniprot2_evol_feature = dict()
        self.pdbchain1_nacen_feature = dict()
        self.pdbchain2_nacen_feature = dict()
        self.pdbchain1_enm_feature = dict()
        self.pdbchain2_enm_feature = dict()
        self.features = dict()

    '''
    Str features
    pdbchain_files(follow pdb/alphafold, chain, pdbsite to extract features):
    # cij(列表, betweenness, clossness, degree, cluster, diversity, eccentricity, strength, eigen_centrality, page_rank)
    cij(列表, betweenness, closeness, degree, cluster, eccentricity, eigen_centrality)
    上面的cij算出来的特征都在一个txt文件中，而且都带有序号（注意有双引号）
    nacen(csv, unw-degree, unw-betweenness, unw-closeness, w-degree, w-betweeness, w-closeness)

    anm_cc(对称矩阵, 5_per, 5_per_20_per, 20_per_50_per, greater_60_per, top3)
    anm_prs(effectiveness是列表, prs是对称矩阵, sensitivity是列表)
    anm_sq(一维列表, sq)
    anm_stiffness(对称矩阵, stiffness)
    gnm_cc(对称矩阵, 5_per, 5_per_20_per, 20_per_50_per, greater_60_per, top3)
    gnm_eigenvector(列表, eigenvector_20, eigenvector_all, eigenvector_top3)
    gnm_prs(effectiveness是列表, prs是对称矩阵, sensitivity是列表)
    gnm_sq(列表, sq)
    上面的enm算出来的anm,gnm的特征前面都带有序号
    '''

    def pdbchain_feature_nacen(self, pdb_nacen_path):  # Alphafold
        features_nacen = ['unw_degree', 'unw_betweenness', 'unw_closeness', 'w_degree', 'w_betweeness', 'w_closeness']
        nacens_name = ['Unweighted Degree', 'Unweighted Betweenness', 'Unweighted Closeness', 'Node-weighted degree',
                       'Node-weighted Betweenness', 'Node-weighted Closeness']
        Pdb = self.UniprotId
        Chain1 = 'A'
        Chain2 = 'A'
        PdbSite1 = self.UniprotSite1
        PdbSite2 = self.UniprotSite2
        df1 = pd.read_csv(pdb_nacen_path + Pdb + '.csv', encoding='utf-8', sep='\t')
        df2 = pd.read_csv(pdb_nacen_path + Pdb + '.csv', encoding='utf-8', sep='\t')
        for i in range(len(df1['Chain'])):
            if df1['Chain'][i] == Chain1:
                PdbSite1 += i
                break
        for j in range(len(df2['Chain'])):
            if df2['Chain'][j] == Chain2:
                PdbSite2 += j
                break
        for i in range(len(features_nacen)):
            feature_name = features_nacen[i] + '_alphafold_nacen'
            self.pdbchain2_nacen_feature[feature_name] = df2[nacens_name[i]][PdbSite2 - 1]
            self.pdbchain1_nacen_feature[feature_name] = df1[nacens_name[i]][PdbSite1 - 1]
            self.features[feature_name] = str(
                (float(df1[nacens_name[i]][PdbSite1 - 1]) + float(df2[nacens_name[i]][PdbSite2 - 1])) / 2)

    def pdbchain_feature_anm_cc(self, anm_cc_path):
        files = os.listdir(anm_cc_path)
        Pdb = self.UniprotId
        Chain1 = 'A'
        Chain2 = 'A'
        PdbSite1 = self.UniprotSite1
        PdbSite2 = self.UniprotSite2
        pdbChain1_files = []
        pdbChain2_files = []
        features_1 = ['5_per', '5_per_20_per', '20_per_50_per', 'greater_60_per', 'top3']
        for file in files:
            if Pdb + '_' + Chain1 in file:
                pdbChain1_files.append(file)
            if Pdb + '_' + Chain2 in file:
                pdbChain2_files.append(file)
        for i in range(len(pdbChain1_files)):
            print(pdbChain1_files[i], pdbChain2_files[i])
            feature_name = '_'.join(pdbChain1_files[i].split('.')[0].split('_')[2:]) + '_alphafold'
            with open(anm_cc_path + '\\' + pdbChain1_files[i], 'r') as f:
                datas = f.readlines()
                try:
                    self.pdbchain1_enm_feature[feature_name] = \
                        float(datas[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')[
                                  PdbSite1 - 1].strip())
                except:
                    self.pdbchain1_enm_feature[feature_name] = \
                        float(datas[-1].strip('\n').split(':')[1].strip('[]').split(',')[
                                  -1].strip())
            with open(anm_cc_path + '\\' + pdbChain2_files[i], 'r') as f2:
                datas = f2.readlines()
                try:
                    self.pdbchain2_enm_feature[feature_name] = \
                        float(datas[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')[
                                  PdbSite2 - 1].strip())
                except:
                    self.pdbchain2_enm_feature[feature_name] = \
                        float(datas[-1].strip('\n').split(':')[1].strip('[]').split(',')[-1].strip())
            self.features[feature_name] = str(
                (self.pdbchain1_enm_feature[feature_name] + self.pdbchain2_enm_feature[feature_name]) / 2)

    def pdbchain_feature_anm_prs(self, anm_prs_path):
        files = os.listdir(anm_prs_path)
        Pdb = self.UniprotId
        Chain1 = 'A'
        Chain2 = 'A'
        PdbSite1 = self.UniprotSite1
        PdbSite2 = self.UniprotSite2
        pdbChain1_files = []
        pdbChain2_files = []
        features_1 = ['effectiveness_all', 'sensitivity_all']
        features_2 = ['prs_all']  # 对称矩阵
        for file in files:
            if Pdb + '_' + Chain1 in file:
                pdbChain1_files.append(file)
            if Pdb + '_' + Chain2 in file:
                pdbChain2_files.append(file)
        for i in range(len(pdbChain1_files)):
            feature_name = '_'.join(pdbChain1_files[i].split('.')[0].split('_')[2:]) + '_alphafold'
            print(pdbChain1_files[i], pdbChain2_files[2])
            if 'prs' in feature_name:
                with open(anm_prs_path + '\\' + pdbChain1_files[i], 'r') as f1:
                    datas1 = f1.readlines()
                    # matrixs1 = [float(item.strip()) for item in
                    #             datas1[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')]
                    try:
                        self.pdbchain1_enm_feature[feature_name] = str(
                            datas1[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                            [PdbSite1 - 1].strip())
                    except:
                        self.pdbchain1_enm_feature[feature_name] = str(
                            datas1[-1].strip('\n').split(':')[1].strip('[]').split(',')
                            [-1].strip())
                with open(anm_prs_path + '\\' + pdbChain2_files[i], 'r') as f2:
                    datas2 = f2.readlines()
                    # matrixs2 = [float(item.strip()) for item in
                    #             datas2[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')]
                    try:
                        self.pdbchain2_enm_feature[feature_name] = str(
                            datas2[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                            [PdbSite2 - 1].strip())
                    except:
                        self.pdbchain2_enm_feature[feature_name] = str(
                            datas2[-1].strip('\n').split(':')[1].strip('[]').split(',')
                            [-1].strip())
                self.features[feature_name] = str((float(self.pdbchain1_enm_feature[feature_name]) + float(
                    self.pdbchain2_enm_feature[feature_name])) / 2)
            elif 'effectiveness' in feature_name:
                with open(anm_prs_path + '\\' + pdbChain1_files[i], 'r') as f1:
                    datas1 = f1.readlines()
                    try:
                        self.pdbchain1_enm_feature[feature_name] = str(
                            datas1[PdbSite1 - 1].strip('\n').split(':')[1])
                    except:
                        self.pdbchain1_enm_feature[feature_name] = str(
                            datas1[-1].strip('\n').split(':')[1])
                with open(anm_prs_path + '\\' + pdbChain2_files[i], 'r') as f2:
                    datas2 = f2.readlines()
                    try:
                        self.pdbchain2_enm_feature[feature_name] = str(
                            datas2[PdbSite2 - 1].strip('\n').split(':')[1])
                    except:
                        self.pdbchain2_enm_feature[feature_name] = str(
                            datas2[-1].strip('\n').split(':')[1])
                self.features[feature_name] = str((float(self.pdbchain1_enm_feature[feature_name]) + float(
                    self.pdbchain2_enm_feature[feature_name])) / 2)
            elif 'sensitivity' in feature_name:
                with open(anm_prs_path + '\\' + pdbChain1_files[i], 'r') as f1:
                    datas1 = f1.readlines()
                    try:
                        self.pdbchain1_enm_feature[feature_name] = str(
                            datas1[PdbSite1 - 1].strip('\n').split(':')[1])
                    except:
                        self.pdbchain1_enm_feature[feature_name] = str(
                            datas1[-1].strip('\n').split(':')[1])
                with open(anm_prs_path + '\\' + pdbChain2_files[i], 'r') as f2:
                    datas2 = f2.readlines()
                    try:
                        self.pdbchain2_enm_feature[feature_name] = str(
                            datas2[PdbSite2 - 1].strip('\n').split(':')[1])
                    except:
                        self.pdbchain2_enm_feature[feature_name] = str(
                            datas2[-1].strip('\n').split(':')[1])
                self.features[feature_name] = str((float(self.pdbchain1_enm_feature[feature_name]) + float(
                    self.pdbchain2_enm_feature[feature_name])) / 2)

    def pdbchain_feature_anm_sq(self, anm_sq_path):
        files = os.listdir(anm_sq_path)
        Pdb = self.UniprotId
        Chain1 = 'A'
        Chain2 = 'A'
        PdbSite1 = self.UniprotSite1
        PdbSite2 = self.UniprotSite2
        pdbChain1_files = []
        pdbChain2_files = []
        features_1 = ['sq_all']
        for file in files:
            if Pdb + '_' + Chain1 in file:
                pdbChain1_files.append(file)
            if Pdb + '_' + Chain2 in file:
                pdbChain2_files.append(file)
        for i in range(len(pdbChain1_files)):
            print(pdbChain1_files[i], pdbChain2_files[i])
            feature_name = '_'.join(pdbChain1_files[i].split('.')[0].split('_')[2:]) + '_alphafold'
            with open(anm_sq_path + '\\' + pdbChain1_files[i], 'r') as f1:
                datas1 = f1.readlines()
                try:
                    self.pdbchain1_enm_feature[feature_name] = str(
                        datas1[PdbSite1 - 1].strip('\n').split(':')[1])
                except:
                    self.pdbchain1_enm_feature[feature_name] = str(
                        datas1[-1].strip('\n').split(':')[1])
            with open(anm_sq_path + '\\' + pdbChain2_files[i], 'r') as f2:
                datas2 = f2.readlines()
                try:
                    self.pdbchain2_enm_feature[feature_name] = str(
                        datas2[PdbSite2 - 1].strip('\n').split(':')[1])
                except:
                    self.pdbchain2_enm_feature[feature_name] = str(
                        datas2[-1].strip('\n').split(':')[1])
            self.features[feature_name] = str(
                (float(self.pdbchain1_enm_feature[feature_name]) + float(
                    self.pdbchain2_enm_feature[feature_name])) / 2)

    def pdbchain_feature_anm_stiffness(self, anm_stiffness_path):
        files = os.listdir(anm_stiffness_path)
        features_1 = ['stiffness']
        Pdb = self.UniprotId
        Chain1 = 'A'
        Chain2 = 'A'
        PdbSite1 = self.UniprotSite1
        PdbSite2 = self.UniprotSite2
        pdbChain1_files = []
        pdbChain2_files = []
        for file in files:
            if Pdb + '_' + Chain1 in file:
                pdbChain1_files.append(file)
            if Pdb + '_' + Chain2 in file:
                pdbChain2_files.append(file)
        for i in range(len(pdbChain1_files)):
            print(pdbChain1_files[i], pdbChain2_files[i])
            feature_name = '_'.join(pdbChain1_files[i].split('.')[0].split('_')[2:]) + '_alphafold'
            with open(anm_stiffness_path + '\\' + pdbChain1_files[i], 'r') as f:
                datas = f.readlines()
                try:
                    self.pdbchain1_enm_feature[feature_name] = \
                        str(datas[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')[
                                PdbSite1 - 1].strip())
                except:
                    self.pdbchain1_enm_feature[feature_name] = \
                        str(datas[-1].strip('\n').split(':')[1].strip('[]').split(',')[
                                -1].strip())
            with open(anm_stiffness_path + '\\' + pdbChain2_files[i], 'r') as f2:
                datas = f2.readlines()
                try:
                    self.pdbchain2_enm_feature[feature_name] = \
                        str(datas[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')[
                                PdbSite2 - 1].strip())
                except:
                    self.pdbchain2_enm_feature[feature_name] = \
                        str(datas[-1].strip('\n').split(':')[1].strip('[]').split(',')[
                                -1].strip())
            self.features[feature_name] = str(
                (float(self.pdbchain1_enm_feature[feature_name]) + float(
                    self.pdbchain2_enm_feature[feature_name])) / 2)

    def pdbchain_feature_gnm_cc(self, gnm_cc_path):
        files = os.listdir(gnm_cc_path)
        Pdb = self.UniprotId
        Chain1 = 'A'
        Chain2 = 'A'
        PdbSite1 = self.UniprotSite1
        PdbSite2 = self.UniprotSite2
        pdbChain1_files = []
        pdbChain2_files = []
        features_1 = ['5_per', '5_per_20_per', '20_per_50_per', 'greater_60_per', 'top3']
        for file in files:
            if Pdb + '_' + Chain1 in file:
                pdbChain1_files.append(file)
            if Pdb + '_' + Chain2 in file:
                pdbChain2_files.append(file)
        for i in range(len(pdbChain1_files)):
            print(pdbChain1_files[i], pdbChain2_files[i])
            feature_name = '_'.join(pdbChain1_files[i].split('.')[0].split('_')[2:]) + '_alphafold'
            with open(gnm_cc_path + '\\' + pdbChain1_files[i], 'r') as f:
                datas = f.readlines()
                try:
                    self.pdbchain1_enm_feature[feature_name] = \
                        float(datas[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')[
                                  PdbSite1 - 1].strip())
                except:
                    self.pdbchain1_enm_feature[feature_name] = \
                        float(datas[-1].strip('\n').split(':')[1].strip('[]').split(',')[
                                  -1].strip())
            with open(gnm_cc_path + '\\' + pdbChain2_files[i], 'r') as f2:
                datas = f2.readlines()
                try:
                    self.pdbchain2_enm_feature[feature_name] = \
                        float(datas[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')[
                                  PdbSite2 - 1].strip())
                except:
                    self.pdbchain2_enm_feature[feature_name] = \
                        float(datas[-1].strip('\n').split(':')[1].strip('[]').split(',')[
                                  -1].strip())
            self.features[feature_name] = str(
                (self.pdbchain1_enm_feature[feature_name] + self.pdbchain2_enm_feature[feature_name]) / 2)

    def pdbchain_feature_gnm_eigenvector(self, gnm_eigenvector_path):
        files = os.listdir(gnm_eigenvector_path)
        Pdb = self.UniprotId
        Chain1 = 'A'
        Chain2 = 'A'
        PdbSite1 = self.UniprotSite1
        PdbSite2 = self.UniprotSite2
        pdbChain1_files = []
        pdbChain2_files = []
        features_1 = ['eigenvectors_20', 'eigenvectors_all', 'eigenvectors_top3']
        for file in files:
            if Pdb + '_' + Chain1 in file:
                pdbChain1_files.append(file)
            if Pdb + '_' + Chain2 in file:
                pdbChain2_files.append(file)
        for i in range(len(pdbChain1_files)):
            print(pdbChain1_files[i], pdbChain2_files[i])
            feature_name = '_'.join(pdbChain1_files[i].split('.')[0].split('_')[2:]) + '_alphafold'
            with open(gnm_eigenvector_path + '\\' + pdbChain1_files[i], 'r') as f1:
                datas1 = f1.readlines()
                try:
                    self.pdbchain1_enm_feature[feature_name] = str(datas1[PdbSite1 - 1].strip('\n').split(':')[1])
                except:
                    self.pdbchain1_enm_feature[feature_name] = str(datas1[-1].strip('\n').split(':')[1])
            with open(gnm_eigenvector_path + '\\' + pdbChain2_files[i], 'r') as f2:
                datas2 = f2.readlines()
                try:
                    self.pdbchain2_enm_feature[feature_name] = str(datas2[PdbSite2 - 1].strip('\n').split(':')[1])
                except:
                    self.pdbchain2_enm_feature[feature_name] = str(datas2[-1].strip('\n').split(':')[1])
            self.features[feature_name] = str(
                (float(self.pdbchain1_enm_feature[feature_name]) + float(
                    self.pdbchain2_enm_feature[feature_name])) / 2)

    def pdbchain_feature_gnm_prs(self, gnm_prs_path):
        files = os.listdir(gnm_prs_path)
        Pdb = self.UniprotId
        Chain1 = 'A'
        Chain2 = 'A'
        PdbSite1 = self.UniprotSite1
        PdbSite2 = self.UniprotSite2
        pdbChain1_files = []
        pdbChain2_files = []
        features_1 = ['effectiveness_all', 'sensitivity_all']
        features_2 = ['prs_all']  # 对称矩阵
        for file in files:
            if Pdb + '_' + Chain1 in file:
                pdbChain1_files.append(file)
            if Pdb + '_' + Chain2 in file:
                pdbChain2_files.append(file)
        for i in range(len(pdbChain1_files)):
            feature_name = '_'.join(pdbChain1_files[i].split('.')[0].split('_')[2:]) + '_alphafold'
            print(pdbChain1_files[i], pdbChain2_files[2])
            if 'prs' in feature_name:
                with open(gnm_prs_path + '\\' + pdbChain1_files[i], 'r') as f1:
                    datas1 = f1.readlines()
                    # matrixs1 = [float(item.strip()) for item in
                    #             datas1[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')]
                    try:
                        self.pdbchain1_enm_feature[feature_name] = str(
                            datas1[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                            [PdbSite1 - 1].strip())
                    except:
                        self.pdbchain1_enm_feature[feature_name] = str(
                            datas1[-1].strip('\n').split(':')[1].strip('[]').split(',')
                            [-1].strip())
                with open(gnm_prs_path + '\\' + pdbChain2_files[i], 'r') as f2:
                    datas2 = f2.readlines()
                    # matrixs2 = [float(item.strip()) for item in
                    #             datas2[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')]
                    try:
                        self.pdbchain2_enm_feature[feature_name] = str(
                            datas2[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                            [PdbSite2 - 1].strip())
                    except:
                        self.pdbchain2_enm_feature[feature_name] = str(
                            datas2[-1].strip('\n').split(':')[1].strip('[]').split(',')
                            [-1].strip())
                self.features[feature_name] = str((float(self.pdbchain1_enm_feature[feature_name]) + float(
                    self.pdbchain2_enm_feature[feature_name])) / 2)
            elif 'effectiveness' in feature_name:
                with open(gnm_prs_path + '\\' + pdbChain1_files[i], 'r') as f1:
                    datas1 = f1.readlines()
                    try:
                        self.pdbchain1_enm_feature[feature_name] = str(
                            datas1[PdbSite1 - 1].strip('\n').split(':')[1])
                    except:
                        self.pdbchain1_enm_feature[feature_name] = str(
                            datas1[-1].strip('\n').split(':')[1])
                with open(gnm_prs_path + '\\' + pdbChain2_files[i], 'r') as f2:
                    datas2 = f2.readlines()
                    try:
                        self.pdbchain2_enm_feature[feature_name] = str(
                            datas2[PdbSite2 - 1].strip('\n').split(':')[1])
                    except:
                        self.pdbchain2_enm_feature[feature_name] = str(
                            datas2[-1].strip('\n').split(':')[1])
                self.features[feature_name] = str((float(self.pdbchain1_enm_feature[feature_name]) + float(
                    self.pdbchain2_enm_feature[feature_name])) / 2)
            elif 'sensitivity' in feature_name:
                with open(gnm_prs_path + '\\' + pdbChain1_files[i], 'r') as f1:
                    datas1 = f1.readlines()
                    try:
                        self.pdbchain1_enm_feature[feature_name] = str(
                            datas1[PdbSite1 - 1].strip('\n').split(':')[1])
                    except:
                        self.pdbchain1_enm_feature[feature_name] = str(
                            datas1[-1].strip('\n').split(':')[1])
                with open(gnm_prs_path + '\\' + pdbChain2_files[i], 'r') as f2:
                    datas2 = f2.readlines()
                    try:
                        self.pdbchain2_enm_feature[feature_name] = str(
                            datas2[PdbSite2 - 1].strip('\n').split(':')[1])
                    except:
                        self.pdbchain2_enm_feature[feature_name] = str(
                            datas2[-1].strip('\n').split(':')[1])
                self.features[feature_name] = str((float(self.pdbchain1_enm_feature[feature_name]) + float(
                    self.pdbchain2_enm_feature[feature_name])) / 2)

    def pdbchain_feature_gnm_sq(self, gnm_sq_path):
        files = os.listdir(gnm_sq_path)
        Pdb = self.UniprotId
        Chain1 = 'A'
        Chain2 = 'A'
        PdbSite1 = self.UniprotSite1
        PdbSite2 = self.UniprotSite2
        pdbChain1_files = []
        pdbChain2_files = []
        features_1 = ['sq_all']
        for file in files:
            if Pdb + '_' + Chain1 in file:
                pdbChain1_files.append(file)
            if Pdb + '_' + Chain2 in file:
                pdbChain2_files.append(file)
        for i in range(len(pdbChain1_files)):
            print(pdbChain1_files[i], pdbChain2_files[i])
            feature_name = '_'.join(pdbChain1_files[i].split('.')[0].split('_')[2:]) + '_alphafold'
            with open(gnm_sq_path + '\\' + pdbChain1_files[i], 'r') as f1:
                datas1 = f1.readlines()
                try:
                    self.pdbchain1_enm_feature[feature_name] = str(
                        datas1[PdbSite1 - 1].strip('\n').split(':')[1])
                except:
                    self.pdbchain1_enm_feature[feature_name] = str(
                        datas1[-1].strip('\n').split(':')[1])
            with open(gnm_sq_path + '\\' + pdbChain2_files[i], 'r') as f2:
                datas2 = f2.readlines()
                try:
                    self.pdbchain2_enm_feature[feature_name] = str(
                        datas2[PdbSite2 - 1].strip('\n').split(':')[1])
                except:
                    self.pdbchain2_enm_feature[feature_name] = str(
                        datas2[-1].strip('\n').split(':')[1])
            self.features[feature_name] = str(
                (float(self.pdbchain1_enm_feature[feature_name]) + float(
                    self.pdbchain2_enm_feature[feature_name])) / 2)

    '''
        序列特征(evol)
        uniprot_files(evol, 根据uniprot和uniprotsite取特征):
        dirinfo(非对称矩阵，M*N)
        entropy(列表)
        mifc(非对称矩阵，M*N)
        mifn(非对称矩阵，M*N)
        mutinfo(非对称矩阵，M*N)
        occupancy(列表)
        omes(非对称矩阵，M*N)
        sca(非对称矩阵，M*N)
        非对称矩阵使用这一行的平均值作为特征值
    '''

    def uninprot_feature_evol_dirinfo(self, evol_dirinfo_path):
        files = os.listdir(evol_dirinfo_path)
        UniprotId = self.UniprotId
        p1 = self.UniprotSite1
        p2 = self.UniprotSite2
        feature_name = 'evol_dirinfo'
        for file in files:
            if UniprotId == file[:6]:
                print(file)
                with open(evol_dirinfo_path + '\\' + file, 'r') as f1:
                    datas1 = f1.readlines()
                    try:
                        matrixs1 = [float(item.strip(' ')) for item in
                                    datas1[p1 - 1].strip('\n').split(' ')]
                    except:
                        matrixs1 = [float(item.strip(' ')) for item in
                                    datas1[-1].strip('\n').split(' ')]
                    self.uniprot1_evol_feature[feature_name] = str(sum(matrixs1) / len(matrixs1))
            if UniprotId == file[:6]:
                print(file)
                with open(evol_dirinfo_path + '\\' + file, 'r') as f2:
                    datas2 = f2.readlines()
                    try:
                        matrixs2 = [float(item.strip(' ')) for item in
                                    datas2[p2 - 1].strip('\n').split(' ')]
                    except:
                        matrixs2 = [float(item.strip(' ')) for item in
                                    datas2[-1].strip('\n').split(' ')]
                    self.uniprot2_evol_feature[feature_name] = str(sum(matrixs2) / len(matrixs2))
        self.features[feature_name] = str((float(self.uniprot1_evol_feature[feature_name]) + float(
            self.uniprot2_evol_feature[feature_name])) / 2)

    def uninprot_feature_evol_entropy(self, evol_entropy_path):
        files = os.listdir(evol_entropy_path)
        UniprotId = self.UniprotId
        p1 = self.UniprotSite1
        p2 = self.UniprotSite2
        feature_name = 'evol_entropy'
        for file in files:
            if UniprotId == file[:6]:
                print(file)
                with open(evol_entropy_path + '\\' + file, 'r') as f1:
                    datas1 = f1.readlines()
                    try:
                        if datas1[p1 - 1].strip('\n') == 'NA':
                            self.uniprot1_evol_feature[feature_name] = str(0)
                        else:
                            self.uniprot1_evol_feature[feature_name] = str(datas1[p1 - 1].strip('\n'))
                    except:
                        if datas1[-1].strip('\n') == 'NA':
                            self.uniprot1_evol_feature[feature_name] = str(0)
                        else:
                            self.uniprot1_evol_feature[feature_name] = str(datas1[-1].strip('\n'))
            if UniprotId == file[:6]:
                with open(evol_entropy_path + '\\' + file, 'r') as f2:
                    datas2 = f2.readlines()
                    try:
                        if datas2[p2 - 1].strip('\n') == 'NA':
                            self.uniprot2_evol_feature[feature_name] = str(0)
                        else:
                            self.uniprot2_evol_feature[feature_name] = str(datas2[p2 - 1].strip('\n'))
                    except:
                        if datas2[-1].strip('\n') == 'NA':
                            self.uniprot2_evol_feature[feature_name] = str(0)
                        else:
                            self.uniprot2_evol_feature[feature_name] = str(datas2[-1].strip('\n'))
        self.features[feature_name] = str((float(self.uniprot1_evol_feature[feature_name]) + float(
            self.uniprot2_evol_feature[feature_name])) / 2)

    def uninprot_feature_evol_mifc(self, evol_mifc_path):
        files = os.listdir(evol_mifc_path)
        UniprotId1 = self.UniprotId
        UniprotId2 = self.UniprotId
        p1 = self.UniprotSite1
        p2 = self.UniprotSite2
        feature_name = 'evol_mifc'
        for file in files:
            if UniprotId1 == file[:6]:
                print(file)
                with open(evol_mifc_path + '\\' + file, 'r') as f1:
                    datas1 = f1.readlines()
                    try:
                        matrixs1 = [float(item.strip(' ')) for item in
                                    datas1[p1 - 1].strip('\n').split(' ')]
                    except:
                        matrixs1 = [float(item.strip(' ')) for item in
                                    datas1[-1].strip('\n').split(' ')]
                    self.uniprot1_evol_feature[feature_name] = str(sum(matrixs1) / len(matrixs1))
            if UniprotId2 == file[:6]:
                print(file)
                with open(evol_mifc_path + '\\' + file, 'r') as f2:
                    datas2 = f2.readlines()
                    try:
                        matrixs2 = [float(item.strip(' ')) for item in
                                    datas2[p2 - 1].strip('\n').split(' ')]
                    except:
                        matrixs2 = [float(item.strip(' ')) for item in
                                    datas2[-1].strip('\n').split(' ')]
                    self.uniprot2_evol_feature[feature_name] = str(sum(matrixs2) / len(matrixs2))
        self.features[feature_name] = str((float(self.uniprot1_evol_feature[feature_name]) + float(
            self.uniprot2_evol_feature[feature_name])) / 2)

    def uninprot_feature_evol_mifn(self, evol_mifn_path):
        files = os.listdir(evol_mifn_path)
        UniprotId1 = self.UniprotId
        UniprotId2 = self.UniprotId
        p1 = self.UniprotSite1
        p2 = self.UniprotSite2
        feature_name = 'evol_mifn'
        for file in files:
            if UniprotId1 == file[:6]:
                print(file)
                with open(evol_mifn_path + '\\' + file, 'r') as f1:
                    datas1 = f1.readlines()
                    try:
                        matrixs1 = [float(item.strip(' ')) for item in
                                    datas1[p1 - 1].strip('\n').split(' ')]
                    except:
                        matrixs1 = [float(item.strip(' ')) for item in
                                    datas1[-1].strip('\n').split(' ')]
                    self.uniprot1_evol_feature[feature_name] = str(sum(matrixs1) / len(matrixs1))
            if UniprotId2 == file[:6]:
                print(file)
                with open(evol_mifn_path + '\\' + file, 'r') as f2:
                    datas2 = f2.readlines()
                    try:
                        matrixs2 = [float(item.strip(' ')) for item in
                                    datas2[p2 - 1].strip('\n').split(' ')]
                    except:
                        matrixs2 = [float(item.strip(' ')) for item in
                                    datas2[-1].strip('\n').split(' ')]
                    self.uniprot2_evol_feature[feature_name] = str(sum(matrixs2) / len(matrixs2))
        self.features[feature_name] = str((float(self.uniprot1_evol_feature[feature_name]) + float(
            self.uniprot2_evol_feature[feature_name])) / 2)

    def uninprot_feature_evol_mutinfo(self, evol_mutinfo_path):
        files = os.listdir(evol_mutinfo_path)
        UniprotId1 = self.UniprotId
        UniprotId2 = self.UniprotId
        p1 = self.UniprotSite1
        p2 = self.UniprotSite2
        feature_name = 'evol_mutinfo'
        for file in files:
            if UniprotId1 == file[:6]:
                print(file)
                with open(evol_mutinfo_path + '\\' + file, 'r') as f1:
                    datas1 = f1.readlines()
                    try:
                        matrixs1 = [float(item.strip(' ')) for item in
                                    datas1[p1 - 1].strip('\n').split(' ')]
                    except:
                        matrixs1 = [float(item.strip(' ')) for item in
                                    datas1[-1].strip('\n').split(' ')]
                    self.uniprot1_evol_feature[feature_name] = str(sum(matrixs1) / len(matrixs1))
            if UniprotId2 == file[:6]:
                print(file)
                with open(evol_mutinfo_path + '\\' + file, 'r') as f2:
                    datas2 = f2.readlines()
                    try:
                        matrixs2 = [float(item.strip(' ')) for item in
                                    datas2[p2 - 1].strip('\n').split(' ')]
                    except:
                        matrixs2 = [float(item.strip(' ')) for item in
                                    datas2[-1].strip('\n').split(' ')]
                    self.uniprot2_evol_feature[feature_name] = str(sum(matrixs2) / len(matrixs2))
        self.features[feature_name] = str((float(self.uniprot1_evol_feature[feature_name]) + float(
            self.uniprot2_evol_feature[feature_name])) / 2)

    def uninprot_feature_evol_occupancy(self, evol_occupancy_path):
        files = os.listdir(evol_occupancy_path)
        UniprotId1 = self.UniprotId
        UniprotId2 = self.UniprotId
        p1 = self.UniprotSite1
        p2 = self.UniprotSite2
        feature_name = 'evol_occupancy'
        for file in files:
            if UniprotId1 == file[:6]:
                print(file)
                with open(evol_occupancy_path + '\\' + file, 'r') as f1:
                    datas1 = f1.readlines()
                    try:
                        if datas1[p1 - 1].strip('\n') == 'NA':
                            self.uniprot1_evol_feature[feature_name] = str(0)
                        else:
                            self.uniprot1_evol_feature[feature_name] = str(datas1[p1 - 1].strip('\n'))
                    except:
                        if datas1[-1].strip('\n') == 'NA':
                            self.uniprot1_evol_feature[feature_name] = str(0)
                        else:
                            self.uniprot1_evol_feature[feature_name] = str(datas1[-1].strip('\n'))
            if UniprotId2 == file[:6]:
                with open(evol_occupancy_path + '\\' + file, 'r') as f2:
                    datas2 = f2.readlines()
                    try:
                        if datas2[p2 - 1].strip('\n') == 'NA':
                            self.uniprot2_evol_feature[feature_name] = str(0)
                        else:
                            self.uniprot2_evol_feature[feature_name] = str(datas2[p2 - 1].strip('\n'))
                    except:
                        if datas2[-1].strip('\n') == 'NA':
                            self.uniprot2_evol_feature[feature_name] = str(0)
                        else:
                            self.uniprot2_evol_feature[feature_name] = str(datas2[-1].strip('\n'))
        self.features[feature_name] = str((float(self.uniprot1_evol_feature[feature_name]) + float(
            self.uniprot2_evol_feature[feature_name])) / 2)

    def uninprot_feature_evol_omes(self, evol_omes_path):
        files = os.listdir(evol_omes_path)
        UniprotId1 = self.UniprotId
        UniprotId2 = self.UniprotId
        p1 = self.UniprotSite1
        p2 = self.UniprotSite2
        feature_name = 'evol_omes'
        for file in files:
            if UniprotId1 == file[:6]:
                print(file)
                with open(evol_omes_path + '\\' + file, 'r') as f1:
                    datas1 = f1.readlines()
                    try:
                        matrixs1 = [float(item.strip(' ')) for item in
                                    datas1[p1 - 1].strip('\n').split(' ')]
                    except:
                        matrixs1 = [float(item.strip(' ')) for item in
                                    datas1[-1].strip('\n').split(' ')]
                    self.uniprot1_evol_feature[feature_name] = str(sum(matrixs1) / len(matrixs1))
            if UniprotId2 == file[:6]:
                print(file)
                with open(evol_omes_path + '\\' + file, 'r') as f2:
                    datas2 = f2.readlines()
                    try:
                        matrixs2 = [float(item.strip(' ')) for item in
                                    datas2[p2 - 1].strip('\n').split(' ')]
                    except:
                        matrixs2 = [float(item.strip(' ')) for item in
                                    datas2[-1].strip('\n').split(' ')]
                    self.uniprot2_evol_feature[feature_name] = str(sum(matrixs2) / len(matrixs2))
        self.features[feature_name] = str((float(self.uniprot1_evol_feature[feature_name]) + float(
            self.uniprot2_evol_feature[feature_name])) / 2)

    def uninprot_feature_evol_sca(self, evol_sca_path):
        files = os.listdir(evol_sca_path)
        UniprotId1 = self.UniprotId
        UniprotId2 = self.UniprotId
        p1 = self.UniprotSite1
        p2 = self.UniprotSite2
        feature_name = 'evol_sca'
        for file in files:
            if UniprotId1 == file[:6]:
                print(file)
                with open(evol_sca_path + '\\' + file, 'r') as f1:
                    datas1 = f1.readlines()
                    try:
                        matrixs1 = [float(item.strip(' ')) for item in
                                    datas1[p1 - 1].strip('\n').split(' ')]
                    except:
                        matrixs1 = [float(item.strip(' ')) for item in
                                    datas1[-1].strip('\n').split(' ')]
                    self.uniprot1_evol_feature[feature_name] = str(sum(matrixs1) / len(matrixs1))
            if UniprotId2 == file[:6]:
                print(file)
                with open(evol_sca_path + '\\' + file, 'r') as f2:
                    datas2 = f2.readlines()
                    try:
                        matrixs2 = [float(item.strip(' ')) for item in
                                    datas2[p2 - 1].strip('\n').split(' ')]
                    except:
                        matrixs2 = [float(item.strip(' ')) for item in
                                    datas2[-1].strip('\n').split(' ')]
                    self.uniprot2_evol_feature[feature_name] = str(sum(matrixs2) / len(matrixs2))
        self.features[feature_name] = str((float(self.uniprot1_evol_feature[feature_name]) + float(
            self.uniprot2_evol_feature[feature_name])) / 2)
