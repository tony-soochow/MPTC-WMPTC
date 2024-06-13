# 对涉及到的13个蛋白质的所有PTM site进行编码
# 全部编码成数字类型：
# 首先编码蛋白质的名字，再编码PTM site
# 蛋白质的ID编码：O->1, P->2, Q->3, 剩余五位直接使用其数字
# PTM site编码：直接使用该位点的位置
# 则每个PTM site都可编码成蛋白质的ID编码+PTM site编码，例如：P04637-K101 -> 104637101

import xlrd

Dataset_excel_file_path = '../Dataset.xlsx'

All_proteins = []
All_PTM_sites = []  # 编码成蛋白质的ID编码+PTM site编码，例如：P04637-K101 -> 104637101
Protein_PTM_sites_dict = dict()  # 用来保存每个蛋白质中的所有PTM位点
Protein_PTM_stes_Decode_dict = dict()  # 用来保存每个PTM site编码前的表示以及编码后，例如：P04637-K101 -> 104637101
Intra_edgelists = []  # 用来保存编码后的边，包含了weight（四种，Combine，PTM-X，PCTpred，Ours）
Inter_edgelists = []  # 用来保存编码后的边，包含了weight(一种)

Proteins_edgelist_dict = dict()  # 用来存储没个蛋白质涉及到的所有边，包含Intra以及Inter

wb = xlrd.open_workbook(Dataset_excel_file_path)

Intra_Combine_All_sheet = wb.sheet_by_name('Intra_Combine_All')
Inter_Combine_All_sheet = wb.sheet_by_name('Inter_Combine_All')
print(Intra_Combine_All_sheet.row_values(Intra_Combine_All_sheet.nrows-1))


def decode_PTM(protein, site):
    Protein_decode = {'O': '1', 'P': '2', 'Q': '3'}
    new_name = Protein_decode[protein[0]] + protein[1:] + site[1:]
    return new_name


for nrow in range(1, Intra_Combine_All_sheet.nrows):
    Protein = Intra_Combine_All_sheet.row_values(nrow)[1]
    Site1 = Intra_Combine_All_sheet.row_values(nrow)[2]
    Site2 = Intra_Combine_All_sheet.row_values(nrow)[4]
    Combine_Score = Intra_Combine_All_sheet.row_values(nrow)[6]
    PTM_X_Score = Intra_Combine_All_sheet.row_values(nrow)[7]
    PCTpred_Score = Intra_Combine_All_sheet.row_values(nrow)[8]
    Our_Score = Intra_Combine_All_sheet.row_values(nrow)[9]

    Site1_New_name = decode_PTM(Protein, Site1)
    Site2_New_name = decode_PTM(Protein, Site2)
    All_proteins.append(Protein)
    All_PTM_sites.append(Site1_New_name)
    All_PTM_sites.append(Site2_New_name)
    if Protein not in Protein_PTM_sites_dict.keys():
        Protein_PTM_sites_dict[Protein] = {Site1, Site2}
    else:
        Protein_PTM_sites_dict[Protein].add(Site1)
        Protein_PTM_sites_dict[Protein].add(Site2)

    if Protein not in Proteins_edgelist_dict.keys():
        Proteins_edgelist_dict[Protein] = []
    Proteins_edgelist_dict[Protein].append([Site1_New_name, Site2_New_name, Combine_Score])

    Protein_PTM_stes_Decode_dict[Protein + '_' + Site1] = Site1_New_name
    Protein_PTM_stes_Decode_dict[Protein + '_' + Site2] = Site2_New_name

    Intra_edgelists.append([Site1_New_name, Site2_New_name, Combine_Score, PTM_X_Score, PCTpred_Score, Our_Score])


# print(len(set(All_proteins)))
# print(len(All_PTM_sites), len(set(All_PTM_sites)))
# print(set(All_PTM_sites))
# print(len(Protein_PTM_sites_dict.keys()))
# print(Protein_PTM_stes_Decode_dict)
# print(len(Protein_PTM_stes_Decode_dict))
# print(len(Intra_edgelists))

# with open('./Intra/All_PTM_Sites_Decode.txt', 'w') as f1:
#     for key, value in Protein_PTM_stes_Decode_dict.items():
#         f1.write(key+':\t'+value+'\n')
#
# with open('./Intra/Combine_Intra.edgelists', 'w') as f2:
#     for edgelists in Intra_edgelists:
#         if edgelists[2] != 0:
#             f2.write(edgelists[0]+'\t'+edgelists[1]+'\t'+str(edgelists[2])+'\n')
#
# with open('./Intra/PTM_X_Intra.edgelists', 'w') as f3:
#     for edgelists in Intra_edgelists:
#         if edgelists[3] != 0:
#             f3.write(edgelists[0]+'\t'+edgelists[1]+'\t'+str(edgelists[3])+'\n')
#
# with open('./Intra/PCTpred_Intra.edgelists', 'w') as f4:
#     for edgelists in Intra_edgelists:
#         if edgelists[4] != 0:
#             f4.write(edgelists[0]+'\t'+edgelists[1]+'\t'+str(edgelists[4])+'\n')
#
# with open('./Intra/Our_Intra.edgelists', 'w') as f5:
#     for edgelists in Intra_edgelists:
#         if edgelists[5] != 0:
#             f5.write(edgelists[0]+'\t'+edgelists[1]+'\t'+str(edgelists[5])+'\n')

# 对PTM site进行重新编码
Nums_Site_dict = dict()
All_PTM_sites = list(set(All_PTM_sites))
for i in range(len(All_PTM_sites)):
    Nums_Site_dict[All_PTM_sites[i]] = str(i)

with open('./Intra/New_Nums_Site_dict.txt', 'w') as f_1:
    for key, value in Nums_Site_dict.items():
        f_1.write(value+':\t'+key+'\n')

with open('./Intra/Intra_multi_1.edges', 'w') as f5:
    for edgelists in Intra_edgelists:
        edgelists = [Nums_Site_dict[edgelists[0]], Nums_Site_dict[edgelists[1]]]+edgelists[2:]
        if edgelists[2] != 0:
            f5.write('1'+'\t'+edgelists[0]+'\t'+edgelists[1]+'\t'+str(edgelists[2])+'\n')
    for edgelists in Intra_edgelists:
        edgelists = [Nums_Site_dict[edgelists[0]], Nums_Site_dict[edgelists[1]]] + edgelists[2:]
        if edgelists[3] != 0:
            f5.write('2'+'\t'+edgelists[0]+'\t'+edgelists[1]+'\t'+str(edgelists[3])+'\n')
    for edgelists in Intra_edgelists:
        edgelists = [Nums_Site_dict[edgelists[0]], Nums_Site_dict[edgelists[1]]] + edgelists[2:]
        if edgelists[4] != 0:
            f5.write('3'+'\t'+edgelists[0]+'\t'+edgelists[1]+'\t'+str(edgelists[4])+'\n')
    for edgelists in Intra_edgelists:
        edgelists = [Nums_Site_dict[edgelists[0]], Nums_Site_dict[edgelists[1]]] + edgelists[2:]
        if edgelists[5] != 0:
            f5.write('4'+'\t'+edgelists[0]+'\t'+edgelists[1]+'\t'+str(edgelists[5])+'\n')


for nrow in range(1, Inter_Combine_All_sheet.nrows):
    Protein1 = Inter_Combine_All_sheet.row_values(nrow)[1]
    Protein2 = Inter_Combine_All_sheet.row_values(nrow)[5]
    Site1 = Inter_Combine_All_sheet.row_values(nrow)[2]
    Site2 = Inter_Combine_All_sheet.row_values(nrow)[6]
    Combine_Score = Inter_Combine_All_sheet.row_values(nrow)[8]

    Site1_New_name = decode_PTM(Protein1, Site1)
    Site2_New_name = decode_PTM(Protein2, Site2)
    if Protein1 not in All_proteins:
        print(Protein1)
    if Protein2 not in All_proteins:
        print(Protein2)
    if Site1_New_name not in All_PTM_sites:
        All_PTM_sites.append(Site1_New_name)
        print(Site1_New_name)
    if Site2_New_name not in All_PTM_sites:
        print(Site2_New_name)
        All_PTM_sites.append(Site2_New_name)

    if Protein1 not in Protein_PTM_sites_dict.keys():
        Protein_PTM_sites_dict[Protein1] = {Site1}
    else:
        Protein_PTM_sites_dict[Protein1].add(Site1)

    if Protein1 not in Protein_PTM_sites_dict.keys():
        Protein_PTM_sites_dict[Protein1] = {Site1}
    else:
        Protein_PTM_sites_dict[Protein1].add(Site1)
    Protein_PTM_stes_Decode_dict[Protein1 + '_' + Site1] = Site1_New_name
    Protein_PTM_stes_Decode_dict[Protein2 + '_' + Site2] = Site2_New_name

    Inter_edgelists.append([Site1_New_name, Site2_New_name, Combine_Score])
    Proteins_edgelist_dict[Protein1].append([Site1_New_name, Site2_New_name, Combine_Score])
    # Proteins_edgelist_dict[Protein2].append([Site1_New_name, Site2_New_name, Combine_Score])


# with open('./Inter/Combine.edgelists', 'w') as f1:
#     for Inter_edgelist in Inter_edgelists:
#         f1.write('\t'.join([str(item) for item in Inter_edgelist])+'\n')


def write_edgelists(protein, dicts):
    edgelists = dicts[protein]
    with open('./Multi-Intra-Inter/'+protein+'.edgelist', 'w') as f:
        for edgelist in edgelists:
            f.write('\t'.join([str(item) for item in edgelist])+'\n')


# for key in Proteins_edgelist_dict.keys():
#     write_edgelists(key, Proteins_edgelist_dict)
