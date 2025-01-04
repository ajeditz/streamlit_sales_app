import streamlit as st
import requests
from func import start_bot

# API endpoint
api_endpoint = "https://basic-sales-ai.fly.dev"


# Mapping of prompt and voice_id
voice_map = {
"British Lady" : "79a125e8-cd45-4c13-8a67-188112f4dd22" ,
"California Girl" : "b7d50908-b17c-442d-ad8d-810c63997ed9" ,
"Child" : "2ee87190-8f84-4925-97da-e52547f9462c" ,
"Classy British Man" : "95856005-0332-41b0-935f-352e296aa0df" ,
"Confident British Man" : "63ff761f-c1e8-414b-b969-d1833d1c870c" ,
"Doctor Mischief" : "fb26447f-308b-471e-8b00-8e9f04284eb5" ,
"Female Nurse" : "5c42302c-194b-4d0c-ba1a-8cb485c84ab9" ,
"Friendly Reading Man" : "69267136-1bdc-412f-ad78-0caad210fb40" ,
"Helpful Woman" : "156fb8d2-335b-4950-9cb3-a2d33befec77" ,
"Kentucky Man" : "726d5ae5-055f-4c3d-8355-d9677de68937" ,
"Madame Mischief" : "e13cae5c-ec59-4f71-b0a6-266df3c9bb8e" ,
"Movieman" : "c45bc5ec-dc68-4feb-8829-6e6b2748095d" ,
"Newsman" : "d46abd1d-2d02-43e8-819f-51fb652c1c61" ,
"Polite Man" : "ee7ea9f8-c0c1-498c-9279-764d6b56d189" ,
"Salesman" : "820a3788-2b37-4d21-847a-b65d8a68c99a" ,
"Southern Woman" : "f9836c6e-a0bd-460e-9d3c-f7299fa60f94" ,
"Storyteller Lady" : "996a8b96-4804-46f0-8e05-3fd4ef1a87cd" ,
"The Merchant" : "50d6beb4-80ea-4802-8387-6c948fe84208"
}

voice_map_el= {
    "Aria": "9BWtsMINqrJLrRacOk9x",
    "Roger": "CwhRBWXzGAHq8TQ4Fs17",
    "Sarah": "EXAVITQu4vr4xnSDxMaL",
    "Laura": "FGY2WhTYpPnrIDTdsKH5",
    "Charlie": "IKne3meq5aSn9XLyUdCD",
    "George": "JBFqnCBsd6RMkjVDRZzb",
    "Callum": "N2lVS1w4EtoT3dr4eOWO",
    "River": "SAz9YHcvj6GT2YYXdXww",
    "Liam": "TX3LPaxmHKxFdv7VOQHJ",
    "Charlotte": "XB0fDUnXU5powFXDhCwa",
    "Alice": "Xb7hH8MSUJpSbSDYk0k2",
    "Matilda": "XrExE9yKIg1WjnnlVkGX",
    "Will": "bIHbv24MWmeRgasZH58o"
}

prompt_dic = {
    "Specssaver broken glasses" :"""You are a customer named John, a 28-year-old who recently bought BARBOUR 11 glasses from Specsavers. Three months after purchasing, you accidentally damaged the frames while on holiday. You’re calling Specsavers Customer Service to discuss the situation and check if the damage is covered under their 100-day no-quibble, no-fuss guarantee.\nIn this conversation:\n- Only speak as John, the customer.\n- Engage naturally, asking questions like ‘Is this covered under the guarantee?’, ‘What will it cost if it isn’t?’, and ‘How long would a repair take?’. \n- Avoid providing answers on behalf of the agent. Wait for the agent’s response before continuing with your next question or statement.\n- Show your frustration when the agent says the guarantee doesn’t cover accidental damage, and try to negotiate a fair resolution.\n- When the agent says ‘SHABANG,’ stop the roleplay and provide feedback on their service.\n\nSpeak casually, as if in a real call. Remember, you’re here to help the agent practice handling customer concerns.""",
    "Specssaver headache":"""You are Julia, a 32-year-old mother of two, visiting the store for a second time. It has been 3 weeks since you bought distance vision glasses, but you’ve only worn them five times because they don’t seem to be working for you. You are experiencing headaches, discomfort behind your ears, and the glasses keep slipping off your face while you’re working.\nIn this interaction:\n- Only speak as Julia, the customer.\n- Answer only when asked specific questions by the customer service agent.\n- Start by asking for a refund, explaining that you’re frustrated and can no longer justify the cost.\n- If the agent offers a solution, you’ll only agree to keep the glasses if it seems fair.\n\nWhen the agent says ‘SHABANG,’ stop the roleplay and give feedback on their service.\n\nSpeak casually, as if in a real face-to-face conversation. Remember, you’re here to help the customer service agent practice handling customer concerns.""",
    "Specsavers varifocal":"""You are roleplaying as John, a 58-year-old male. It’s the middle of the month, and you haven’t been paid yet, so you’re less likely to spend over £300 unless you feel a strong connection, either emotionally or through a clear understanding of your lifestyle.\nIn this interaction:\n- Only speak as John, the customer.\n- You’re semi-retired, enjoy playing a lot of golf, and drive long distances.\n- You’ve already chosen the Specsavers Liam frame but are also interested in the Hugo15 frame that the technician showed you earlier.\n- Your optician recently advised you to get varifocal glasses, and now the dispensing technician is helping you decide on the best option by navigating different choices and prices.\n\nAnswer questions naturally, focusing on lifestyle needs like golf and driving to see if the technician’s options fit your activities and budget.\n\nSpeak casually, as if in a real conversation with the technician, and remember, you’re here to help the technician practice upselling glasses effectively.""",
    "Dell customer agent scenario":"""You are John, a Dell customer who has been receiving regular pop-up messages on your Dell laptop indicating that your Windows operating system is out of date and requires an update. You've been ignoring these for months because you don’t understand what this means and are afraid of "breaking the computer." One morning, your laptop starts running very slowly, and a blue screen appears, mentioning something about "critical updates." Panicking, you call Dell customer service because you believe your computer might be “broken.” You have trouble explaining your issue to the automated system and finally reach a human agent after navigating several confusing prompts. Your role is to engage with the customer service agent as a customer and explain your issue to get a solution""",
    "Marketing Sales Agent scenario":"""You are a lady who runs a small bakery in her local town. Your business is doing well with local foot traffic, but you have noticed that your online orders have been stagnant. Your current website, built years ago using a free platform, looks outdated and doesn’t function well on mobile devices. You know you need a better website to attract more customers, but you've been putting it off due to lack of time and not knowing where to start. You get a call from a sales agent, from a company that specializes in affordable website redesigns for small businesses.The agent will try to sell you his services so engage with him as a prospect. You are a skeptical and curious prospect who will question the agent about how his services are better for your business. Remember You are the prospect and not the sales person"""
    }



# Set page config
st.set_page_config(page_title="EasyCloser", layout="centered")

# Sidebar with instructions
st.sidebar.title("Instructions")
st.sidebar.write("""
1. Choose a scenario and avatar.
2. Customize additional parameters.
3. Click "Start Call" to join.
4. Use the "Join Now" button to enter the call.
""")

# Title centered
st.markdown("<h1 style='text-align: center;'>EasyCloser</h1>", unsafe_allow_html=True)

# Prompt selection
selected_prompt = st.selectbox("Select Scenario", list(prompt_dic.keys()))

# Voice ID selection
selected_voice_id = st.selectbox("Select Avatar", list(voice_map_el.keys()))

# Additional customization options
emotion = st.selectbox("Select Emotion", ["Neutral", "Happy", "Frustrated", "Curious"])
difficulty_level = st.slider("Select Difficulty Level", 1, 5, 3)
roleplay_type=st.selectbox("Select Roleplay Type",["customer","sales"])

# Start Call button with spinner and room URL as "Join Now" button
if st.button("Start Call"):
    with st.spinner("Starting call..."):
        # API request payload
        prompt = prompt_dic[selected_prompt]
        voice_id=voice_map_el[selected_voice_id]
        response = start_bot(prompt,voice_id,roleplay_type)
        room_url = response['room_url']
        room_id=response['room_id']
        
        st.success("Call setup complete!")
        
        # Display Join Now button that redirects to the room URL
        st.markdown(f"""
            <a href="{room_url}" target="_blank">
                <button style="background-color: #4CAF50; color: white; padding: 10px 24px; border: none; border-radius: 4px; cursor: pointer;">
                    Join Now
                </button>
            </a>
        """, unsafe_allow_html=True)


        Path = f'''{room_id}'''
        st.write("Room Id")
        st.code(Path, language="python")
        
