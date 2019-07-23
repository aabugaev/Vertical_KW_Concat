
# coding: utf-8

# In[7]:
import subprocess
import sys

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

try:
	import pandas as pd
	import numpy as np
	import xlrd
except:
    install('pandas')
    install('numpy')
    install('xlrd')

import pandas as pd
import numpy as np

print("The file with keywords should be in horizontal format.")
Keywords_File = str(input("Please give the name of the file with keywords.\n"))

Keywords = pd.read_excel(Keywords_File)


# In[8]:


Keywords_melt = Keywords.melt(var_name="Groups",value_name = "Words")
Keywords_melt.head(5)


# In[9]:


Keywords_melt_drNA = Keywords_melt.dropna()
Yandex_KW = Keywords_melt_drNA.copy()
Keywords_melt_drNA.head(5)


# In[10]:


Keywords_melt_drNA_noplus = Keywords_melt_drNA.assign(Words = Keywords_melt_drNA.loc[:,"Words"].str.replace("+","") )
Keywords_melt_drNA_noplus.head(5)


# In[11]:


Google_Broad =Keywords_melt_drNA_noplus.assign(Words = Keywords_melt_drNA_noplus.loc[:,"Words"].str.replace(" "," +"))
Google_Broad =Google_Broad.assign(Words = "+"+Google_Broad.loc[:,"Words"])

Google_Phrasal =Keywords_melt_drNA_noplus.assign(Words = "["+Keywords_melt_drNA_noplus.loc[:,"Words"]+"]")
Google_Exact = Keywords_melt_drNA_noplus.assign(Words = "\""+Keywords_melt_drNA_noplus.loc[:,"Words"]+"\"")

Google_KW = pd.concat([Google_Phrasal,Google_Exact,Google_Broad], ignore_index=True)


# In[12]:


Google_KW.rename(columns={'Groups':'Ad Group', 'Words':'Keyword'}, inplace=True)
Google_KW["Campaign"] = ""

Yandex_KW.rename(columns={'Groups':'Название группы', 'Words':'Фразы'}, inplace=True)


# In[13]:


Google_KW.to_excel("Google_KW.xlsx")
Yandex_KW.to_excel("Yandex_KW.xlsx")

