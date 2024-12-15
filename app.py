import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def create_combined_df(df, candidate_name, column_name, candidate_column_index):
    # Calculate Count for the specific candidate (as a Series, not a DataFrame to avoid 'उम्र' column)
    candidate_count = df[df[df.columns[candidate_column_index]] == candidate_name][column_name].value_counts()
    candidate_count = candidate_count.rename('Count')

    # Calculate Total count for the entire dataset (as a Series)
    total_count = df[column_name].value_counts()
    total_count = total_count.rename('Total')

    # Combine them using outer join
    combined_df = pd.DataFrame(candidate_count).join(pd.DataFrame(total_count), how='outer')

    # Fill NaN values in 'Count' with 0 since not all ages might be present for the candidate
    combined_df['Count'] = combined_df['Count'].fillna(0)

    # Calculate Percentage
    combined_df['Percentage'] = (combined_df['Count'] / combined_df['Total']) * 100
    combined_df.sort_values(by='Count', inplace=True, ascending=False)

    return combined_df


def plot_pie_chart(df, column_name):
    # Get value counts for the specified column
    data = df[column_name].value_counts()

    # Create a pie chart using Plotly
    fig = go.Figure(data=[go.Pie(labels=data.index, values=data.values, hole=0, textinfo='label+percent')])

    # Update layout
    fig.update_layout(title_text=f"{column_name}")

    # Show the plot
    st.plotly_chart(fig)


def plot_bar_chart(df, column_name):
    # Get value counts for the specified column
    data = df[column_name].value_counts()

    # Create a bar chart using Plotly with values on bars
    fig = go.Figure([go.Bar(x=data.index, y=data.values, text=data.values, textposition='auto',
                            marker_color=px.colors.qualitative.Pastel)])

    # Update layout for better visualization
    fig.update_layout(
        title_text=f"{column_name}",
        xaxis_title="Political Party",
        yaxis_title="Count",
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig)


df = pd.read_csv("Uttam Nagar (32)-7.csv")


st.title('Uttam Nagar Analysis Report - SSPR Elections')
st.write(' ')


st.header('1. Education')
plot_pie_chart(df, 'शिक्षा')
st.header('2. Caste')
plot_bar_chart(df, 'जाति')
st.header('3. Employment')
plot_pie_chart(df, 'रोजगार')
st.header('4. State Government Satisfaction')
plot_pie_chart(df, 'क्या आप राज्य सरकार से संतुष्ट है ? \n\n')
st.header('5. Centre Government Satisfaction')
plot_pie_chart(df, 'क्या आप वर्तमान केंद्र सरकार से संतुष्ट हैं ?')
st.header('6. MLA Satisfaction')
plot_pie_chart(df, 'क्या आप वर्तमान विधायक से संतुष्ट हैं ?')
st.header('7. Party Choice')
plot_bar_chart(df, 'आप किस राजनितिक पार्टी को पसंद करते है ?')
st.header('8. State Leadership Choice')
plot_pie_chart(df, 'राज्य में आपका पसंदीदा नेता ?')
st.header('9. Central Leadership Choice')
plot_pie_chart(df, 'आपका केंद्र का पसंदीदा नेता ?')



st.title('Caste-wise Analysis')

st.subheader("1. Top castes for Naresh Balyan")
st.dataframe(create_combined_df(df,'Rank 1', 'जाति',12))
plot_bar_chart(df[df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [नरेश बालियान]'] == 'Rank 1'], 'जाति')

st.subheader("2. Top castes for Krishan Gehlot")
st.dataframe(create_combined_df(df,'Rank 1', 'जाति',13))
plot_bar_chart(df[df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [कृष्ण गहलोट]'] == 'Rank 1'], 'जाति')


st.title('Profession-wise Analysis')

st.subheader("1. Top Profession for Naresh Balyan")
st.dataframe(create_combined_df(df,'Rank 1', 'रोजगार',12))
plot_pie_chart(df[df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [नरेश बालियान]'] == 'Rank 1'], 'रोजगार')

st.subheader("2. Top Profession for Krishan Gehlot")
st.dataframe(create_combined_df(df,'Rank 1', 'रोजगार',13))
plot_pie_chart(df[df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [कृष्ण गहलोट]'] == 'Rank 1'], 'रोजगार')


st.title('Education-wise Analysis')

st.subheader("1. Top Education for Naresh Balyan")
st.dataframe(create_combined_df(df, 'Rank 1', 'शिक्षा',12))
plot_pie_chart(df[df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [नरेश बालियान]'] == 'Rank 1'], 'शिक्षा')

st.subheader("2. Top Education for Krishan Gehlot")
st.dataframe(create_combined_df(df, 'Rank 1', 'शिक्षा',13))
plot_pie_chart(df[df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [कृष्ण गहलोट]'] == 'Rank 1'], 'शिक्षा')

st.title('Rankings of potential Candidates')
naresh = df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [नरेश बालियान]'].value_counts()
naresh = naresh.rename('नरेश बालियान')
krishan = df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [कृष्ण गहलोट]'].value_counts()
krishan  = krishan.rename('कृष्ण गहलोट')
pawan = df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [पवन शर्मा]'].value_counts()
pawan = pawan.rename('पवन शर्मा')
subhash = df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [सुभाष मग्गो]'].value_counts()
subhash = subhash.rename('सुभाष मग्गो')
sachin = df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [सचिन गंभीर]'].value_counts()
sachin = sachin.rename('सचिन गंभीर')
mukesh = df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [मुकेश शर्मा]'].value_counts()
mukesh = mukesh.rename('मुकेश शर्मा')

rank_df = pd.concat([naresh,krishan,pawan,subhash,sachin,mukesh],axis = 1).sort_index()
rank_df = rank_df.apply(lambda col: (col / col.sum()) * 100, axis=1)
st.dataframe(rank_df)


def Voter_Comp(df,temp_center,temp_state,col):
    #Overall
    a = df[col].value_counts()/df[col].value_counts().sum()
    a = a.rename('Overall')

    #Neutral-Central Govt
    b = temp_center[col].value_counts()/temp_center[col].value_counts().sum()
    b = b.rename('Neutral Voters - Central Govt')

    #Neutral-State Govt
    c = temp_state[col].value_counts()/temp_state[col].value_counts().sum()
    c = c.rename('Neutral Voters - State Govt')

    data = pd.concat([a, b, c], axis=1).sort_index() * 100
    data.index.name = 'Ranking'

    return data

st.title('Neutral Voters Analysis')

temp_state = df[df['क्या आप राज्य सरकार से संतुष्ट है ? \n\n']==2]
temp_center = df[df['क्या आप वर्तमान केंद्र सरकार से संतुष्ट हैं ?']==2]

st.subheader("1. Naresh Balyan")
st.dataframe(Voter_Comp(df,temp_center,temp_state,df.columns[12]))

st.subheader("2. Krishan Gehlot")
st.dataframe(Voter_Comp(df,temp_center,temp_state,df.columns[13]))


st.title('Ward-wise Analysis')
# Function to extract ward numbers 113 and 114
def extract_ward(colony):
  if '113' in colony or '(113)' in colony:
      return 113
  elif '114' in colony:
      return 114
  else:
    return None

df['Ward'] = df['Ward 114 Mohan garden '].apply(extract_ward)
colony_113 = ['Mohan garden', 'NAWADA GANV', 'K 1,2,3 BLOCK', 'Block R 3 A 3 convent of gagan bharti school mohan garden ',
 'Mohan garden ', 'Z BLOCK VIPIN GARDEN', 'NAWADA SANIK ENCLAVE VIPIN GARDEN', 'divan state', 'NAWADA VIPIN GARDEN MAIN',
 'R3 A3 block', 'Block R 3 A 2 convent of gagan bharti school mohan garden ', 'AB Block vipin garden', 'Laxmi puri Nawada',
 'ABC block vipin garden', 'Block p mohan garden Kamal model sr.se.school', 'Block R3 a3convent of gagan bharti school',
 'Block R3 convent of gagan bharti school', 'A block', 'Block L2 DA mohan garden ', 'Nawada housing board',
 'NAVAWADA VIPIN GARDEN X', 'R1 block', 'Block L2 mohan garden ', 'Nawada housing complex', 'Block R 3 A 3 convent of gagan bharti school ',
 'Block L-2 Mohan Garden ', 'R3A2 Block','Block R 3 ', 'bhagwati garden','E block Mohan garden ','Nawada laxman puri',
 'Block L-1 mohan garden ', 'Block R3', 'Block R3 ', 'Block R 3 B ', 'Block R 3 A 2 convent of gagan bharti school ',
 'K 1 ', 'Block b', 'Govt school ', 'R block Jbs school mohan garden ','Block L-2 mohan gardhan ', 'Block L1', 'Block s',
 'Block r3', 'Block L-2 mohan garden ', 'Block s ', 'Pratap encouraged ', 'Pratap enclave ', 'M ', 'Block k ', 'Block 3',
 'E Block', 'Ms block ', 'New ms block ', 'Q1 block, Mohan garden', 'K3 ','E black mohan garden ', 'Mohan garden e block ',
 'R extension ', 'L 1 block ', 'Block M ', 'Block R ', 'R block JBS school ', 'R bock  Jbs school mohan garden ',
 'Block R 3', 'Block L-3', 'Block L-1', 'Block L2', 'K 2', 'Block l2 mohan garden ', 'Extaison l2 ', 'Block R 3 A 2 ',
 'Block l3 ', 'Block L3 ', 'Block l1 ', 'Extinction part 1 ', 'Extension part 1', 'Extension Part 1', 'Block B',
 ' Block R3 convent of gagan bharti school  ', 'L extinction ', 'R block JBS school mohan gardhan ','L extension',
 'Block L3', 'Block m','Block l_1','Block p mohan garden Kamal model sr.se.school ', 'K1 ',
 ' Block R 3 A 3 convent of gagan bharti school mohan garden ', 'Block R 3 A 3 convent school mohan garden ',
 'Block R 3 B', 'Block R3 convent', 'Block R 3 A 3 ','Block B ','Block P','Block R 3 A 3 convent of gagan bharti School ',
 'Block R3 convent of gagan bharti school  ', 'Block R 3 A 3 convent of gagan bharti school mohan garden k'
]

temp_df_1 = df[df['Ward 114 Mohan garden '].isin(colony_113)]
temp_df_2 = df[df['Ward']==113.0]
temp_df = pd.concat([temp_df_1,temp_df_2])

naresh = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [नरेश बालियान]'].value_counts()
naresh = naresh.rename('नरेश बालियान')
krishan = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [कृष्ण गहलोट]'].value_counts()
krishan  = krishan.rename('कृष्ण गहलोट')
pawan = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [पवन शर्मा]'].value_counts()
pawan = pawan.rename('पवन शर्मा')
subhash = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [सुभाष मग्गो]'].value_counts()
subhash = subhash.rename('सुभाष मग्गो')
sachin = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [सचिन गंभीर]'].value_counts()
sachin = sachin.rename('सचिन गंभीर')
mukesh = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [मुकेश शर्मा]'].value_counts()
mukesh = mukesh.rename('मुकेश शर्मा')

rank_df = pd.concat([naresh,krishan,pawan,subhash,sachin,mukesh],axis = 1).sort_index()
rank_df = rank_df.apply(lambda col: (col / col.sum()) * 100, axis=1)

st.subheader("1. Ward No 113 Rankings")
st.dataframe(rank_df)

st.subheader("2. Ward No 114 Rankings")
colony_114 = ['RAMCHANDRA ENCLAVE','Ramchandra enclave ','NAWADA GANV','ZAILDAR ENCLAVE Vijay Nagar  BLOCK','L, L1,L2,L3 BLOCK, Mohan garden','W BLOCK'
         ,'K 1,2,3 BLOCK','R BLOCK,VANI VIHAR','AI 1 BLOCK','L X BLOCK , NIYAR SARKARI SCHOOL','RAMA PARK (A,B,C,C1 BLOCK)','A,B,C,D Block, Gulab bhai',
          'Anoop nagar, bindapur, CD block','A,B,C Block, Ram Nagar om vihar','DAL MEEL ROAD','Prtap enclave '
         ]
temp_df_1 = df[df['Ward 114 Mohan garden '].isin(colony_114)]
temp_df_2 = df[df['Ward']==114.0]
temp_df = pd.concat([temp_df_1,temp_df_2])

naresh = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [नरेश बालियान]'].value_counts()
naresh = naresh.rename('नरेश बालियान')
krishan = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [कृष्ण गहलोट]'].value_counts()
krishan  = krishan.rename('कृष्ण गहलोट')
pawan = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [पवन शर्मा]'].value_counts()
pawan = pawan.rename('पवन शर्मा')
subhash = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [सुभाष मग्गो]'].value_counts()
subhash = subhash.rename('सुभाष मग्गो')
sachin = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [सचिन गंभीर]'].value_counts()
sachin = sachin.rename('सचिन गंभीर')
mukesh = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [मुकेश शर्मा]'].value_counts()
mukesh = mukesh.rename('मुकेश शर्मा')

rank_df = pd.concat([naresh,krishan,pawan,subhash,sachin,mukesh],axis = 1).sort_index()
rank_df = rank_df.apply(lambda col: (col / col.sum()) * 100, axis=1)
st.dataframe(rank_df)

st.subheader("3. Ward No 115 Rankings")
colony_115 = [ 'Q,Q,X BLOCK Uttam Nagar,VIKAS VIHAR','B Block,bhagwati vihar,  sector ACD','OM VIHAR','A,A1,B,B1,C,C1,D BLOCK,SANJAY ENCLAVE',
         'A,B,B1,C block, Kiran garden','A,A1,B,B1,B2,CD,E,F Gram Sabha block, sevak park','A,B,G BLOCK, NANDRAM PARK','AB BLOCK SISH RAM PARK',
         'A,B,C,D BLOCK,SHUBASH PARK','T,T,A block, shukar bazar, Uttam Nagar','MANAS KUNJ, VIKAS VIHAR','O,OX BLOCK GEETA ENCLAVE',
          'A,B,C,D Block, Niyar gagan bharti school','B BLOCK, INDRA PARK','Block R 3 A 3 convent of gagan bharti school mohan garden ',
          'RZ BLOCK, NEW Uttam Nagar','S BLOCK, PARAMPURI','INDRA PARK X,PART 1,E BLOCK, EAST Uttam Nagar','Indra park , Prajapathi colony',
           'MANGAL BAZAR ROAD, PARAMPURI',
         ]

temp_df = df[df['Ward 114 Mohan garden '].isin(colony_115)]

naresh = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [नरेश बालियान]'].value_counts()
naresh = naresh.rename('नरेश बालियान')
krishan = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [कृष्ण गहलोट]'].value_counts()
krishan  = krishan.rename('कृष्ण गहलोट')
pawan = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [पवन शर्मा]'].value_counts()
pawan = pawan.rename('पवन शर्मा')
subhash = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [सुभाष मग्गो]'].value_counts()
subhash = subhash.rename('सुभाष मग्गो')
sachin = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [सचिन गंभीर]'].value_counts()
sachin = sachin.rename('सचिन गंभीर')
mukesh = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [मुकेश शर्मा]'].value_counts()
mukesh = mukesh.rename('मुकेश शर्मा')

rank_df = pd.concat([naresh,krishan,pawan,subhash,sachin,mukesh],axis = 1).sort_index()
rank_df = rank_df.apply(lambda col: (col / col.sum()) * 100, axis=1)
st.dataframe(rank_df)

st.subheader("4. Ward No 116 Rankings")

temp_df = df.iloc[3195:4311]

naresh = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [नरेश बालियान]'].value_counts()
naresh = naresh.rename('नरेश बालियान')
krishan = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [कृष्ण गहलोट]'].value_counts()
krishan  = krishan.rename('कृष्ण गहलोट')
pawan = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [पवन शर्मा]'].value_counts()
pawan = pawan.rename('पवन शर्मा')
subhash = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [सुभाष मग्गो]'].value_counts()
subhash = subhash.rename('सुभाष मग्गो')
sachin = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [सचिन गंभीर]'].value_counts()
sachin = sachin.rename('सचिन गंभीर')
mukesh = temp_df['आपके अनुसार निम्नलिखित (विधानसभा के नेताओं को) स्थान दीजिए ? [मुकेश शर्मा]'].value_counts()
mukesh = mukesh.rename('मुकेश शर्मा')

rank_df = pd.concat([naresh,krishan,pawan,subhash,sachin,mukesh],axis = 1).sort_index()
rank_df = rank_df.apply(lambda col: (col / col.sum()) * 100, axis=1)
st.dataframe(rank_df)