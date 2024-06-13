import xlrd

HAT_GENE_file = 'HAT_GENE.txt'
HAT_acet_file_path = './Hat-acet.xlsx'

HAT_GENEs = []

with open(HAT_GENE_file, 'r') as f:
    lines = f.readlines()
    for line in lines:
        if ';' in line:
            items = line.strip('\n').split(';')
            for item in items:
                HAT_GENEs.append(item)
        else:
            HAT_GENEs.append(line.strip('\n'))

HAT_GENEs = list(set(HAT_GENEs))

# with open('./HAT_GENE_dul.txt', 'w') as f1:
#     f1.write('\n'.join(HAT_GENEs))

HAT_gene_IDs = dict()

with open('./HAT_UniproID.txt', 'r') as f1:
    lines = f1.readlines()
    for i in range(len(lines)):
        HAT_gene_IDs[HAT_GENEs[i]] = lines[i].strip()

print(HAT_gene_IDs)

wb = xlrd.open_workbook(HAT_acet_file_path)
HAT_sheet = wb.sheet_by_name('Sheet1')
HAT_sheet_titles = HAT_sheet.row_values(0)

print(HAT_sheet_titles)

HAT_INFOS = []

for nrow in range(1, HAT_sheet.nrows):
    Sub_Gene_name = HAT_sheet.row_values(nrow)[0]
    Sub_Uniprot = HAT_sheet.row_values(nrow)[1]
    Sub_Position = HAT_sheet.row_values(nrow)[2]
    Sub_Peptide = HAT_sheet.row_values(nrow)[3]
    Hat_genes = HAT_sheet.row_values(nrow)[4]
    others = HAT_sheet.row_values(nrow)[5:]
    if ';' in Hat_genes:
        Hat_genes = Hat_genes.split(';')
        for Hat_gene in Hat_genes:
            HAT_INFOS.append(tuple([Sub_Gene_name, Sub_Uniprot, Sub_Position, Sub_Peptide, Hat_gene, HAT_gene_IDs[Hat_gene]]+others))
    else:
        HAT_INFOS.append(tuple([Sub_Gene_name, Sub_Uniprot, Sub_Position, Sub_Peptide, Hat_genes, HAT_gene_IDs[Hat_genes]] + others))


print(len(HAT_INFOS), len(set(HAT_INFOS)))
HAT_sheet_titles = HAT_sheet_titles[:5]+['HAT_UNIPROT']+HAT_sheet_titles[5:]

with open('Hat-acet_new.txt', 'w') as f2:
    f2.write('\t'.join(HAT_sheet_titles)+'\n')
    for HAT_INFO in set(HAT_INFOS):
        f2.write('\t'.join(HAT_INFO)+'\n')
