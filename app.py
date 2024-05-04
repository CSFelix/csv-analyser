import os
from pathlib import Path

import pandas as pd
from ydata_profiling import ProfileReport

import streamlit as st
from streamlit_pandas_profiling import st_profile_report # pip install streamlit-pandas-profiling
from streamlit_option_menu import option_menu # pip install streamlit-option-menu
from streamlit_extras.colored_header import colored_header # pip install streamlit-extras
from streamlit_extras.metric_cards import style_metric_cards # pip install streamlit-extras

import plotly.express as px # pip install plotly

# ---- PATH SETTINGS ----
current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
css_file = current_dir / 'css' / 'main.css'



# ---- VARIABLES ----
PAGE_TITLE = 'CSV Analyser'
PAGE_ICON = ':bar_chart:'
PAGE_LAYOUT = 'wide'
SIDEBAR_INITIAL_STATE = 'collapsed' # 'auto', 'collapsed', 'expanded'

UPLOADED_FILE_FLAG = False

EMAIL = 'csfelix08@gmail.com'
SOCIAL_MEDIAS = {
	'GitHub': 'https://github.com/csfelix'
	, 'Kaggle': 'https://www.kaggle.com/dsfelix'
	, 'Portfolio': 'https://csfelix.github.io'
	, 'LinkedIn': 'https://linkedin.com/in/csfelix'
}



# ---- PAGE SETTINGS ----
st.set_page_config(
	page_title=PAGE_TITLE
	, page_icon=PAGE_ICON
	, layout=PAGE_LAYOUT
	, initial_sidebar_state=SIDEBAR_INITIAL_STATE
)




# ---- LOADING CSS FILE ----
with open(css_file) as f:
	st.markdown(f'<style>{ f.read() }</style>', unsafe_allow_html=True)



# ---- SIDEBAR ----
with st.sidebar:
	# Social Medias
	st.header('🤳 Social Medias')
	st.markdown('#')
	cols = st.columns(len(SOCIAL_MEDIAS))
	for index, (platform, link) in enumerate(SOCIAL_MEDIAS.items()):
		cols[index].write(f'[{platform}]({link})')

	st.markdown('----')

	# Email
	st.header('📧 Hit me up by E-Mail')
	st.markdown('#')
	contact_form = f"""
	<form action="https://formsubmit.co/{EMAIL}" method="POST">
		<input type="hidden" name="_captcha" value="false" />
		<input type="text" name="name" placeholder="Your Name" required />
		<input type="email" name="email" placeholder="Your Email" required />
		<textarea name="message" placeholder="Your Message Here..." required></textarea>
		<button type"submit" class="button">Send!</button>
	</form>
	"""
	st.markdown(contact_form, unsafe_allow_html=True)



# ---- PAGE TITLE ----
colored_header(
	label=PAGE_ICON + ' ' + PAGE_TITLE
	, description='Upload any CSV file to get significant insights!'
	, color_name='violet-70'
)
st.markdown('#')



# ---- TABS ----
tab1, tab2, tab3, tab4 = st.tabs(['Uploader', 'Metrics', 'Dashboard', 'Report'])



# ---- UPLOADER ----
with tab1:
	uploaded_file = st.file_uploader('Choose any CSV File and tap on the tabs', type='csv')

	# When file has been uploaded, some info about it is displayed
	if uploaded_file:
		# Reading Dataset
		st.markdown('----')
		df = pd.read_csv(uploaded_file)
		UPLOADED_FILE_FLAG = True
		file_size = round( uploaded_file.size / 1024, 2)
		file_name = uploaded_file.name

		# Metric Cards
		col1, col2, col3 = st.columns(3)
		col1.metric(label='Nº Registers', value=df.shape[0])
		col2.metric(label='Nº Features', value=df.shape[1])
		col3.metric(label='File Size', value=f'{file_size} kB')
		style_metric_cards(
			background_color='#0a394d'
			, border_left_color='#7159c1'
			, border_color='#ffffff'
			, border_size_px=5
			, border_radius_px=100
			, box_shadow=True
		)

		# Info
		st.info(f'File Name: {file_name}', icon='📁')

		# Dataset
		st.dataframe(df)



# ---- METRICS ----
with tab2:
	if uploaded_file == None: st.warning('🤔 Uh-oh, it looks like you forgot to upload a CSV file in the first tab!')
	else:
		st.info('💭 It can take a few seconds to dysplay the metrics after generating the report!')
		
		# Metric Cards
		numerical_features = [feature for feature in df.columns if df[feature].dtype in ['int', 'float']]
		number_numerical_features = len(numerical_features)
		selected_features = st.multiselect('Select the Features:', options=numerical_features, default=numerical_features)
		cols = st.columns(3)

		for feature in selected_features:
			metrics = {
				'AVG'      :  round(df[feature].mean(), 2)
				, 'STD'    :  round(df[feature].std(), 2)
				, 'Median' :  round(df[feature].median(), 2)
			}

			for (col, metric) in zip(cols, metrics.keys()):
				col.metric(label=f'{feature} {metric}', value=metrics[metric])


# ---- DASHBOARD ----
with tab3:
	if uploaded_file == None: st.warning('🤔 Uh-oh, it looks like you forgot to upload a CSV file in the first tab!')	
	else:
		st.info('💭 It can take a few seconds to display the Regression Plot due to Linar Calculations!')

		# Numerical Features Correlation
		numerical_features = [feature for feature in df.columns if df[feature].dtype in ['int', 'float']]
		numerical_feature1 = st.selectbox('What feature would you like to see the correlation?', numerical_features, index=0)
		numerical_feature2 = st.selectbox('What other feature would you like to see the correlation?', numerical_features, index=1 if len(numerical_features) > 1 else 0)

		# If both selected features are the same, a warning is displayed
		if numerical_feature1 == numerical_feature2: st.warning('🤔 Uh-oh, it looks like you have choosen the same feature twice. Try again with different ones!')

		# else, a Regression Plot is displayed
		else:
			regression_plot = px.scatter(df, x=numerical_feature1, y=numerical_feature2, trendline='ols', trendline_color_override='red')
			st.plotly_chart(regression_plot, use_container_width=True)



# ---- REPORT ----
with tab4:
	if uploaded_file == None: st.warning('🤔 Uh-oh, it looks like you forgot to upload a CSV file in the first tab!')
	
	else:
		st.info('💭 Tap on the button bellow to generate the report (it can take a few seconds to generate the report!).')
		generate_report_btn = st.button(label='Generate Report', type='primary')

		if generate_report_btn:
			profile_report = df.profile_report()	
			st_profile_report(profile_report)