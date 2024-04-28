import streamlit as st
from rsa import *
# from aes_old import AES
from aes import encrypt_long_text, decrypt_long_text
import random, string

# st.set_page_config(layout="wide")
HEIGHT = 150

tab1, tab2 = st.tabs(['RSA', 'AES'])
with tab1:
   st.header("RSA")
   with st.form("param_rsa1"):
      st.write("Parameters")
      p_col, q_col = st.columns(2)
      with p_col:
         p = st.number_input(label="Enter p", key='p', format='%.0f', value=st.session_state.get('generated_p', None), placeholder="A prime number. Ex: 29")
      with q_col:
         q = st.number_input(label="Enter q", key='q', format='%.0f', value=st.session_state.get('generated_q', None), placeholder="Another prime number. Ex: 37")
      btn_check_p_q, btn_gen = st.columns(2)
      with btn_check_p_q:
         check_p_q = st.form_submit_button(label="Check p and q")
      with btn_gen:
         gen_p_q = st.form_submit_button(label="Generate p and q")

      p, q = int(p) if p else None, int(q) if q else None
      if check_p_q:
         if p:
            st.write(f"❔ p = {p}", is_prime(p))
         else:
            st.write(f"⚠️ Please fill box p")
         if q==None:
            st.write(f"⚠️ Please fill box q")
         elif q==p:
            st.write(f"⚠️ Please input again!")
         else:
            st.write(f"❔ q = {q}", is_prime(q))
         
      if gen_p_q:
         p_gen, q_gen = random_p_q()
         st.session_state['generated_p'] = float(p_gen)
         st.session_state['generated_q'] = float(q_gen)
         st.experimental_rerun()

      n = p*q if (p and q) else None
      phi = (p-1)*(q-1) if n else None
      st.write(f"n = ", n)
      st.write(f"phi = ", phi)

      ###############################################################

      e_col, d_col = st.columns(2)
      with e_col:
         e = st.number_input(label="Enter e (use to encrypt)", key='e', format='%.0f', value=st.session_state.get('generated_e', None), placeholder=f"A number is gcd(e, phi) = 1. Ex: {0}")
      with d_col:
         d = st.number_input(label="Enter d (use to decrypt)", key='d', format='%.0f', value=st.session_state.get('generated_d', None), placeholder=f"A number is (d*e)%phi = 1. Ex: {0}")

      e, d = int(e) if e else None, int(d) if d else None

      btn_check_e_d, btn_gen_e_d = st.columns(2)
      with btn_check_e_d:
         check_e_d = st.form_submit_button("Check e and d")
      with btn_gen_e_d:
         gen_e_d = st.form_submit_button("Generate e and d")

      if check_e_d:
         if q==None or p==None:
            st.write(f"⚠️ Please fill box {'' if p else 'p'} {'' if q else 'q'}")
         else:
            if e:
               st.write(f"e = {e}", check_e(e, phi))
            else:
               st.write("⚠️ Please fill box e", e)
            if d:
               st.write(f"d = {d}", check_d(d, e, phi))
            else:
               st.write("⚠️ Please fill box d", d)
         
      if gen_e_d:
         e_gen = select_e(phi)
         d_gen = generate_d(e_gen, phi)
         st.session_state['generated_e'] = float(e_gen)
         st.session_state['generated_d'] = float(d_gen)
         st.experimental_rerun()

   with st.form("en_de_rsa"):
      en_col, opt, de_col = st.columns([2,1,2])
      with en_col:
         message_en = st.text_area(label="Enter Plain Text / Encrypted", height=HEIGHT, value=st.session_state.get('encrypt_text', None), placeholder="Input text")
      with opt:
         st.write("")
         en_btn = st.form_submit_button(label="Encrypt >>", )
         de_btn = st.form_submit_button(label="<< Decrypt", )
      with de_col:
         message_de = st.text_area(label="Enter Encrypted Text / Decrypted", height=HEIGHT, value=st.session_state.get('decrypt_text', None))

      if en_btn:
         with st.status("Encrypting..."):
            if message_en:
               message_en = encrypt((n, e), message_en)
               st.session_state['encrypt_text'] = None
               st.session_state['decrypt_text'] = message_en['text']
         st.experimental_rerun()

      if de_btn:
         with st.status("Decrypting..."):
            if message_de:
               message_de = decrypt((n, d), message_de)
               st.session_state['encrypt_text'] = message_de['text']
               st.session_state['decrypt_text'] = None
         st.experimental_rerun()


with tab2:
   st.header("AES")
   # encryption
   with st.form("param_aes"):
      btn_key_aes = st.text_input(label='Enter key:', value=st.session_state.get('key_aes', ''), max_chars=16, key="key_encrypt_aes")
      if len(btn_key_aes) != 16:
         st.error('Mã khóa cần có 16 ký tự.')
      key_encrypt = st.form_submit_button(label='Generate key')
      if key_encrypt:
         st.session_state['key_aes'] = ''.join(random.choice(string.ascii_letters) for _ in range(16))
         st.experimental_rerun()

   # decryption
   with st.form("main"):
      en_col, opt, de_col = st.columns([2,1,2])
      with en_col:
         message_en = st.text_area(label="Enter Plain Text / Encrypted", height=HEIGHT, value=st.session_state.get('encrypt_aes', None), placeholder="Input text")
         # message_en = st.text_input(label='Enter Plain Text / Encrypted', value=st.session_state.get('encrypt_aes', None), max_chars=16, key="aes_input")
      with opt:
         st.write("")
         en_btn = st.form_submit_button(label="Encrypt >>", )
         de_btn = st.form_submit_button(label="<< Decrypt", )
      with de_col:
         message_de = st.text_area(label="Enter Encrypted Text / Decrypted", height=HEIGHT, value=st.session_state.get('decrypt_aes', None))

      # aes = AES(int.from_bytes(btn_key_aes.encode(), 'big'))
      
      if en_btn:
         with st.status("Encrypting..."):
            if message_en!=None:
               en = encrypt_long_text(message_en, btn_key_aes)
               # split_text = [int.from_bytes(message_en[i:i+16].encode(), 'big') for i in range(0, len(message_en), 16)]
               # encrypted_text_hex = ''.join(str(hex(aes.encrypt(i))[2:]) for i in split_text)
               # encrypted_text = aes.encrypt(int.from_bytes(message_en.encode(), 'big'))
               # encrypted_text_hex = hex(encrypted_text)[2:] 
               st.session_state['encrypt_aes'] = None
               st.session_state['decrypt_aes'] = en
         st.experimental_rerun()

      if de_btn:
         with st.status("Decrypting..."):
            if message_de!=None:
               # decrypted_int = [aes.decrypt(int.from_bytes(bytes.fromhex(message_de[i:i+32]), byteorder='big')) for i in range(0, len(message_de), 32)]
               # byte_length = [(i.bit_length() + 7) // 8 or 16 for i in decrypted_int]
               # decrypted_text = ''.join(decrypted_int[i].to_bytes(byte_length[i], 'big').decode(errors='ignore').rstrip('\x00') for i in range(len(decrypted_int)))
               # ciphertext_bytes = bytes.fromhex(message_de)
               # ciphertext_int = int.from_bytes(ciphertext_bytes, byteorder='big')
               # decrypted_int = aes.decrypt(ciphertext_int)
               # byte_length = (decrypted_int.bit_length() + 7) // 8 or 16
               # decrypted_text = decrypted_int.to_bytes(byte_length, 'big').decode(errors='ignore').rstrip('\x00')
               de = decrypt_long_text(message_de, btn_key_aes)
               st.session_state['encrypt_aes'] = de
               st.session_state['decrypt_aes'] = None
         st.experimental_rerun()

# cho text st.header("RSA") ra giữa màn hình
css = """
.st-emotion-cache-l9bjmx e1nzilvr5 > p {
   font-size: 3rem !important;
}
input {
   font-size: 1rem !important;
}

.st-emotion-cache-l9bjmx > p {
   font-size: 32;
   font-weight: bold;
   
}

h2 {
   font-size: 23; 
   font-weight: bold; 
   color: red; 
   text-align: center;
}

div.stButton > button:first-child {
    margin: 5px auto;
    display: block;
}
"""

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)