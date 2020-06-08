import streamlit as st
from phue import Bridge

#https://discovery.meethue.com/
b = Bridge('192.168.1.7')

st.title("Light controller")

st.header("Individual Control")

if st.checkbox("Sofa Living Room"):
	bri1 = st.slider("Birghtness", 0, 255, 255)
	b.set_light(1,'on', True)
	b.set_light(1, 'bri', bri1)
else:
	b.set_light(1,'on', False)

if st.checkbox("Center Living Room"):
	bri2 = st.slider("Birghtness", 0, 255, 255)
	b.set_light(2,'on', True)
	b.set_light(2, 'bri', bri2)
else:
	b.set_light(2,'on', False)

if st.checkbox("TV Living Room"):
	bri3 = st.slider("Birghtness", 0, 255, 255)
	b.set_light(3,'on', True)
	b.set_light(3, 'bri', bri3)
else:
	b.set_light(3,'on', False)

st.header("Ambiance")

if st.checkbox("TV Mode"):
	b.set_light(1,'on', False)
	b.set_light(2,'on', False)
	b.set_light(3,'on', False)

if st.checkbox("Full light"):
	bri = 255
	b.set_light(1,'on', True)
	b.set_light(2,'on', True)
	b.set_light(3,'on', True)
	b.set_light(1, 'bri', bri)
	b.set_light(2, 'bri', bri)
	b.set_light(3, 'bri', bri)

if st.checkbox("Subdued"):
	bri = st.slider("Birghtness", 0, 255, 255)
	b.set_light(1,'on', True)
	b.set_light(2,'on', True)
	b.set_light(3,'on', True)
	b.set_light(1, 'bri', bri)
	b.set_light(2, 'bri', bri)
	b.set_light(3, 'bri', bri)