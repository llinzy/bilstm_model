import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
from sklearn import preprocessing
import altair as alt
st.set_option('deprecation.showfileUploaderEncoding', False)

data=pd.read_csv('dt.csv')

transposed=data.T
transposed=transposed.reset_index()
transposed.columns=transposed.iloc[0,:]
transposed=transposed.iloc[1:,:]
transposed.columns=['word','Critical_Thinking', 'Instructing', 
                     'Management_of_Financial_Resources',  'Mathematics',
                      'Quality_Control_Analysis',  'Service_Orientation', 
                     'Speaking','Technology_Design']
                     
means=[np.mean(np.array(transposed.iloc[i,1:])) for i in range (0,len(transposed))]
means=[int(float(i)) for i in means]
means=pd.Series(means, name='word_mean').copy()

transposed['mean']=means
transposed=transposed.fillna(0)
relevant=transposed[transposed['mean']>np.mean(np.array(means))]

df=relevant.T
df=df.reset_index()
df.columns=df.iloc[0,:]
df=df.iloc[1:,:]
df=df.rename(columns={'word':'skill_category'})
df=df.iloc[:8,:]

st.write('Words Having a Mean Occurence Greater Than 22 for each Skill Category')

st.subheader('Data')
default_type=st.multiselect('Select a Skill Category', list(df.skill_category.unique()), 
                            default=['Critical_Thinking', 'Instructing', 'Management_of_Financial_Resources',
                                      'Mathematics', 'Quality_Control_Analysis', 'Service_Orientation', 'Speaking'])
new_data=df[df.skill_category.isin(default_type)]
st.write(new_data)

relevant2=relevant.set_index('word')
trimmed_data=[]
for i in relevant2:
    trimmed_data.append(relevant2[i].sort_values(ascending=False)[:50])

bar_data=pd.DataFrame(trimmed_data[0]).join(pd.DataFrame(trimmed_data[1]), how='outer')\
.join(pd.DataFrame(trimmed_data[2]), how='outer')\
.join(pd.DataFrame(trimmed_data[3]), how='outer')\
.join(pd.DataFrame(trimmed_data[4]), how='outer')\
.join(pd.DataFrame(trimmed_data[5]), how='outer')\
.join(pd.DataFrame(trimmed_data[6]), how='outer')\
.join(pd.DataFrame(trimmed_data[7]), how='outer')
bar_data=bar_data.fillna(0)
bar_data=bar_data.reset_index()

st.subheader('Top 50 Word Occurrences for Skill Category')
bar_x=st.selectbox('X', bar_data.columns[1:])
bar_fig=px.bar(bar_data, x =bar_data.word, y=bar_x)
st.plotly_chart(bar_fig)


st.subheader('Word Comparison Within Skill Group')
pred=st.selectbox('X', df.columns[:],index=1)
deft=st.selectbox('Y', df.columns[:],index=3)
fig = px.scatter(new_data, x =pred,y=deft, color='skill_category')
st.plotly_chart(fig)


st.subheader('Skill Group Cluster Analysis')
relevant_c=relevant.iloc[:,1:9]
val=relevant_c.values
relevant_scaled=preprocessing.normalize(val,norm='l2')
relevant_scaled=pd.DataFrame(relevant_scaled)
relevant_scaled.columns=relevant_c.columns


cls_X=st.selectbox('X', relevant_scaled.columns[:],index=1)
cls_Y=st.selectbox('Y', relevant_scaled.columns[:],index=4)
c = alt.Chart(relevant_scaled).mark_circle().encode(x=cls_X, y=cls_Y)
st.altair_chart(c, use_container_width=True)

df_full=pd.read_csv('df_full_10000.csv')

st.subheader('Skill Category Alignment by Ranked Order for Each ID')
default_type=st.selectbox('Select an ID', list(df_full.ids.unique()))
                          
                          
new_data=df_full[df_full.ids==default_type]
st.write(new_data.iloc[:,1:])

cat_ranked_df_full=pd.read_csv('cat_ranked_df_20000.csv')

st.subheader('Top Ranked ID for each Skill Category')
cat_ranked_df_full_default_type=st.selectbox('Select Skill Category', list(cat_ranked_df_full.skill_category.unique()))
cat_ranked_df_full_default_type2=st.selectbox('Select Skill Rank', list(cat_ranked_df_full.rank_.unique()))
                          
cat_ranked_df=cat_ranked_df_full[(cat_ranked_df_full.skill_category==cat_ranked_df_full_default_type)&(cat_ranked_df_full.rank_==cat_ranked_df_full_default_type2)]
st.write(cat_ranked_df.iloc[:,2:])




st.subheader('Upload Job Posting to Assess Rank for Each Skill Category')
uploaded_file = st.file_uploader("Choose a file")

data = uploaded_file.read()

st.write(data)

profiles=pickle.load(open('top_profile_words.pkl', 'rb'))

skill_ranks=[]
skills=[]

for k in profiles:

    skills.append(k)
    skill_ranks.append(len(list(set([p for p in data.split() if p in profiles[k]])))/len(profiles[k])*100)
    
df=pd.concat([pd.Series(skills, name='skill_category'), 
	      pd.Series(skill_ranks, name='skill_category_alignment')], axis=1)
	      
ranking=list(range(1,len(df)+1))

df_sorted=df.sort_values(['skill_category_alignment'], ascending=False)
df_sorted=df_sorted.reset_index()

df_sorted=pd.concat([pd.Series(ranking, name='alignment_rank'), 
		     df_sorted.iloc[:,1:]], axis=1)
		     
		     
st.subheader('Skill Category Alignment by Ranked Order')
default_type=st.selectbox('Select an Rank', list(df_sorted.alignment_rank.unique()))
		          
		          
new_data=df_sorted[df_sorted.alignment_rank==default_type]
st.write(new_data)       

st.subheader('Job Posting Alignment by Skill Category')
default_type2=st.selectbox('Select an Skill Category', list(df_sorted.skill_category.unique()))
		          
		          
new_data2=df_sorted[df_sorted.skill_category==default_type2]
st.write(new_data2)


