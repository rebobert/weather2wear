import streamlit as st

st.title("Contact")

st.header(":mailbox: Get In Touch With Us!")

contact_form = """
<form action="https://formsubmit.co/enteremail@email.ca" method="POST">
    <input type="hidden" name="_cc" value="email@email.com,yetanother@email.com">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit">Send</button>
     
</form>
"""

st.markdown(contact_form, unsafe_allow_html=True)

#Use local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")