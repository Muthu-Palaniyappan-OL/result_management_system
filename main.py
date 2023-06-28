import tabula


df = tabula.read_pdf('./1.pdf',pages = 1,lattice=True)[0]

df.to_csv('./sample.csv')