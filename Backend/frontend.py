import streamlit as st
import requests
import time

# Expanded Translation dictionary for Top 10 Indian Languages
translations = {
    "hi": {  # Hindi (1st)
        "title": "🌱 ग्रीन मैचर्स: AI-संचालित पर्यावरणीय नौकरी क्रांति",
        "powered_by": "xAI के Grok द्वारा सेमेंटिक मैचिंग",
        "select_skills": "अपनी स्किल्स चुनें (या नई जोड़ें):",
        "button": "ग्रीन जॉब्स और कहानियां खोजें",
        "matches_header": "जॉब मैच देखें",
        "story_header": "अपनी ग्रीन कहानी पढ़ें",
        "no_matches": "कोई मैच नहीं मिला—बैकएंड के माध्यम से अधिक जॉब्स जोड़ें!",
        "enter_skills": "कृपया कम से कम एक स्किल चुनें या दर्ज करें!",
        "error": "त्रुटि: {error} - सुनिश्चित करें कि बैकएंड http://127.0.0.1:8000 पर चल रहा है!",
        "success": "मैच मिल गए!"
    },
    "bn": {  # Bengali (2nd)
        "title": "🌱 গ্রিন ম্যাচার্স: এআই-চালিত ইকো জব বিপ্লব",
        "powered_by": "xAI-এর Grok দ্বারা সেমান্টিক ম্যাচিং",
        "select_skills": "আপনার দক্ষতা নির্বাচন করুন (নতুন যোগ করুন):",
        "button": "গ্রিন চাকরি এবং গল্প আবিষ্কার করুন",
        "matches_header": "চাকরির মিল দেখুন",
        "story_header": "আপনার গ্রিন গল্প পড়ুন",
        "no_matches": "কোনো মিল পাওয়া যায়নি—ব্যাকএন্ডের মাধ্যমে আরও চাকরি যোগ করুন!",
        "enter_skills": "দয়া করে কমপক্ষে একটি দক্ষতা নির্বাচন করুন বা লিখুন!",
        "error": "ত্রুটি: {error} - নিশ্চিত করুন যে ব্যাকএন্ড http://127.0.0.1:8000 চলছে!",
        "success": "মিল পাওয়া গেছে!"
    },
    "mr": {  # Marathi (3rd)
        "title": "🌱 ग्रीन मॅचर्स: AI-द्वारे चालित इको नोकरी क्रांती",
        "powered_by": "xAI च्या Grok द्वारे सेमँटिक मॅचिंग",
        "select_skills": "तुमच्या कौशल्यांचा निवडा (किंवा नवीन जोडा):",
        "button": "ग्रीन नोकऱ्या आणि कथा शोधा",
        "matches_header": "नोकरी मॅच पहा",
        "story_header": "तुमची ग्रीन कथा वाचा",
        "no_matches": "कोणताही मॅच सापडला नाही—बॅकएंडद्वारे अधिक नोकऱ्या जोडा!",
        "enter_skills": "कृपया किमान एक कौशल्य निवडा किंवा टाका!",
        "error": "त्रुटी: {error} - सुनिश्चित करा की बॅकएंड http://127.0.0.1:8000 वर चालू आहे!",
        "success": "मॅच सापडले!"
    },
    "te": {  # Telugu (4th)
        "title": "🌱 గ్రీన్ మ్యాచర్స్: AI-చేత నడిచే ఎకో ఉద్యోగ విప్లవం",
        "powered_by": "xAI యొక్క Grok ద్వారా సెమాంటిక్ మ్యాచింగ్",
        "select_skills": "మీ నైపుణ్యాలను ఎంచుకోండి (కొత్తవి జోడించండి):",
        "button": "గ్రీన్ ఉద్యోగాలు మరియు కథలు కనుగొనండి",
        "matches_header": "ఉద్యోగ మ్యాచ్‌లు చూడండి",
        "story_header": "మీ గ్రీన్ కథను చదవండి",
        "no_matches": "మ్యాచ్‌లు లేవు—బ్యాకెండ్ ద్వారా మరిన్ని ఉద్యోగాలు జోడించండి!",
        "enter_skills": "దయచేసి కనీసం ఒక నైపుణ్యాన్ని ఎంచుకోండి లేదా ఎంటర్ చేయండి!",
        "error": "పొర్పు: {error} - బ్యాకెండ్ http://127.0.0.1:8000 పై రన్ అవుతున్నట్లు నిర్ధారించండి!",
        "success": "మ్యాచ్‌లు కనుగొనబడ్డాయి!"
    },
    "ta": {  # Tamil (5th)
        "title": "🌱 பசுமை பொருத்தங்கள்: AI-ஆல் இயக்கப்படும் பசுமை வேலைவாய்ப்பு புரட்சி",
        "powered_by": "xAI-இன் Grok மூலம் அர்த்தவுருவாக்க பொருத்தம்",
        "select_skills": "உங்கள் திறன்களைத் தேர்ந்தெடுக்கவும் (புதியவற்றை உள்ளிடவும்):",
        "button": "பசுமை வேலைகள் மற்றும் கதைகளை கண்டறி",
        "matches_header": "வேலை பொருத்தங்களை பார்",
        "story_header": "உங்கள் பசுமை கதையை படி",
        "no_matches": "பொருத்தங்கள் இல்லை—பின்னணி மூலம் மேலும் வேலைகளை சேர்க்கவும்!",
        "enter_skills": "குறைந்தது ஒரு திறமையைத் தேர்ந்தெடுக்கவும் அல்லது உள்ளிடவும்!",
        "error": "பிழை: {error} - பின்னணி http://127.0.0.1:8000 இல் இயங்குவதை உறுதி செய்யவும்!",
        "success": "பொருத்தங்கள் கிடைத்தன!"
    },
    "gu": {  # Gujarati (6th)
        "title": "🌱 ગ્રીન મેચર્સ: AI-દ્વારા ચલાવવામાં આવતી ઇકો જોબ ક્રાંતિ",
        "powered_by": "xAI ના Grok દ્વારા સેમેન્ટિક મેચિંગ",
        "select_skills": "તમારી કુશળતાઓ પસંદ કરો (અથવા નવી ઉમેરો):",
        "button": "ગ્રીન જોબ્સ અને વાર્તાઓ શોધો",
        "matches_header": "જોબ મેચ જુઓ",
        "story_header": "તમારી ગ્રીન વાર્તા વાંચો",
        "no_matches": "કોઈ મેચ મળ્યું નથી—બેકએન્ડ દ્વારા વધુ જોબ્સ ઉમેરો!",
        "enter_skills": "કૃપા કરીને ઓછામાં ઓછું એક કુશળતા પસંદ કરો અથવા લખો!",
        "error": "ભૂલ: {error} - ખાતરી કરો કે બેકએન્ડ http://127.0.0.1:8000 પર ચાલી રહ્યું છે!",
        "success": "મેચ મળ્યા!"
    },
    "ur": {  # Urdu (7th)
        "title": "🌱 گرین میچرز: AI سے چلنے والی ایکو جاب انقلاب",
        "powered_by": "xAI کے Grok کے ذریعے سیمنٹک میچنگ",
        "select_skills": "اپنی مہارتیں منتخب کریں (یا نئی شامل کریں):",
        "button": "گرین جابز اور کہانیاں تلاش کریں",
        "matches_header": "جاب میچ دیکھیں",
        "story_header": "اپنی گرین کہانی پڑھیں",
        "no_matches": "کوئی میچ نہیں ملا—بیک اینڈ کے ذریعے مزید جابز شامل کریں!",
        "enter_skills": "براہ مہربانی کم از کم ایک مہارت منتخب کریں یا درج کریں!",
        "error": "غلطی: {error} - یقینی بنائیں کہ بیک اینڈ http://127.0.0.1:8000 پر چل رہا ہے!",
        "success": "میچ مل گئے!"
    },
    "kn": {  # Kannada (8th)
        "title": "🌱 ಗ್ರೀನ್ ಮ್ಯಾಚರ್ಸ್: AI-ಚಾಲಿತ ಇಕೋ ಉದ್ಯೋಗ ಕ್ರಾಂತಿ",
        "powered_by": "xAI ನ Grok ಮೂಲಕ ಸೆಮ್ಯಾಂಟಿಕ್ ಮ್ಯಾಚಿಂಗ್",
        "select_skills": "ನಿಮ್ಮ ಕೌಶಲ್ಯಗಳನ್ನು ಆಯ್ಕೆಮಾಡಿ (ಅಥವಾ ಹೊಸದನ್ನು ಸೇರಿಸಿ):",
        "button": "ಗ್ರೀನ್ ಉದ್ಯೋಗಗಳು ಮತ್ತು ಕಥೆಗಳನ್ನು ಕಂಡುಹಿಡಿಯಿರಿ",
        "matches_header": "ಉದ್ಯೋಗ ಹೊಂದಾಣಿಕೆಗಳನ್ನು ನೋಡಿ",
        "story_header": "ನಿಮ್ಮ ಗ್ರೀನ್ ಕಥೆಯನ್ನು ಓದಿ",
        "no_matches": "ಹೊಂದಾಣಿಕೆಗಳು ದೊರೆತಿಲ್ಲ—ಬ್ಯಾಕೆಂಡ್ ಮೂಲಕ ಹೆಚ್ಚು ಉದ್ಯೋಗಗಳನ್ನು ಸೇರಿಸಿ!",
        "enter_skills": "ದಯವಿಟ್ಟು ಕನಿಷ್ಠ ಒಂದು ಕೌಶಲ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ ಅಥವಾ ನಮೂದಿಸಿ!",
        "error": "ದೋಷ: {error} - ಬ್ಯಾಕೆಂಡ್ http://127.0.0.1:8000 ನಲ್ಲಿ ಚಲಿಸುತ್ತಿದೆಯೆಂದು ಖಚಿತಪಡಿಸಿ!",
        "success": "ಹೊಂದಾಣಿಕೆಗಳು ಸಿಕ್ಕಿವೆ!"
    },
    "or": {  # Odia (9th)
        "title": "🌱 ଗ୍ରିନ୍ ମ୍ୟାଚର୍ସ: AI-ଦ୍ୱାରା ଚାଲିତ ଇକୋ ଜବ୍ ବିପ୍ଳବ",
        "powered_by": "xAIର Grok ଦ୍ୱାରା ସେମାଣ୍ଟିକ୍ ମ୍ୟାଚିଂ",
        "select_skills": "ତୁମର ସ୍କିଲ୍ଗୁଡ଼ିକୁ ବାଛନ୍ତୁ (ନାହିଁତେ ନୂଆ ଯୋଡ଼ନ୍ତୁ):",
        "button": "ଗ୍ରିନ୍ ଜବ୍ ଏବଂ କାହାଣୀ ଖୋଜନ୍ତୁ",
        "matches_header": "ଜବ୍ ମ୍ୟାଚ ଦେଖନ୍ତୁ",
        "story_header": "ତୁମର ଗ୍ରିନ୍ କାହାଣୀ ପଢ଼ନ୍ତୁ",
        "no_matches": "କୌଣସି ମ୍ୟାଚ୍ ମିଳିଲା ନାହିଁ—ବ୍ୟାକେଣ୍ଡ ମାଧ୍ୟମରେ ଅଧିକ ଜବ୍ ଯୋଡ଼ନ୍ତୁ!",
        "enter_skills": "ଦୟାକରି ଅତି କମରେ ଏକ ସ୍କିଲ୍ ବାଛନ୍ତୁ କିମ୍ବା ଲେଖନ୍ତୁ!",
        "error": "ତ୍ରୁଟି: {error} - ନିଶ୍ଚିତ କରନ୍ତୁ ଯେ ବ୍ୟାକେଣ୍ଡ http://127.0.0.1:8000 ଚାଲୁ ଅଛି!",
        "success": "ମ୍ୟାଚ୍ ମିଳିଲା!"
    },
    "ml": {  # Malayalam (10th)
        "title": "🌱 ഗ്രീൻ മാച്ചേഴ്സ്: AI-ന്‍റെ സഹായത്തോടെ പരിസ്ഥിതി സൗഹൃദ ജോലി വിപ്ലവം",
        "powered_by": "xAI-ന്റെ Grok വഴി സെമാന്റിക് മാച്ചിംഗ്",
        "select_skills": "നിങ്ങളുടെ കഴിവുകൾ തിരഞ്ഞെടുക്കുക (അല്ലെങ്കിൽ പുതിയത് ചേർക്കുക):",
        "button": "ഗ്രീൻ ജോലികളും കഥകളും കണ്ടെത്തുക",
        "matches_header": "ജോലി മാച്ചുകൾ കാണുക",
        "story_header": "നിങ്ങളുടെ ഗ്രീൻ കഥ വായിക്കുക",
        "no_matches": "മാച്ചുകൾ കിട്ടിയില്ല—ബാക്ക്‌എൻഡ് വഴി കൂടുതൽ ജോലികൾ ചേർക്കുക!",
        "enter_skills": "ദയവായി കുറഞ്ഞത് ഒരു കഴിവ് തിരഞ്ഞെടുക്കുക അല്ലെങ്കിൽ നൽകുക!",
        "error": "പിശക്: {error} - ബാക്ക്‌എൻഡ് http://127.0.0.1:8000-ൽ പ്രവർത്തിക്കുന്നുണ്ടെന്ന് ഉറപ്പാക്കുക!",
        "success": "മാച്ചുകൾ കിട്ടി!"
    },
    "en": {  # English (default, for completeness)
        "title": "🌱 Green Matchers: AI-Powered Eco Job Revolution",
        "powered_by": "Powered by xAI’s Grok for Semantic Matching",
        "select_skills": "Select your skills (or type new ones):",
        "button": "Discover Green Jobs & Stories",
        "matches_header": "View Job Matches",
        "story_header": "Read Your Green Story",
        "no_matches": "No matches found—add more jobs via backend!",
        "enter_skills": "Please select or enter at least one skill!",
        "error": "Error: {error} - Ensure backend is running at http://127.0.0.1:8000!",
        "success": "Matches found!"
    }
}

# Session state for language
if "lang" not in st.session_state:
    st.session_state.lang = "en"

# Language selector with all 10 (plus English)
lang_options = ["en", "hi", "bn", "mr", "te", "ta", "gu", "ur", "kn", "or", "ml"]
lang_names = ["English", "Hindi", "Bengali", "Marathi", "Telugu", "Tamil", "Gujarati", "Urdu", "Kannada", "Odia", "Malayalam"]
lang_index = lang_options.index(st.session_state.lang)
lang = st.selectbox("Select Language", lang_names, index=lang_index, key="lang_select")
st.session_state.lang = lang_options[lang_names.index(lang)]

# Custom CSS (unchanged from previous)
st.markdown(
    """
    <style>
    .main {
        background-color: #f0fff0; /* Light green */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #28a745; /* Green button */
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #218838;
    }
    .stHeader {
        color: #155724; /* Dark green */
        font-size: 24px;
        font-weight: bold;
        text-align: center;
    }
    .stText {
        color: #333;
        font-size: 16px;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Dynamic content
t = translations[st.session_state.lang]
st.markdown(f'<div class="stHeader">{t["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<p class="stText" style="text-align:center;">{t["powered_by"]}</p>', unsafe_allow_html=True)

# Skill input (multi-select with common skills)
skills = st.multiselect(
    t["select_skills"],
    ["Python", "Django", "AI", "Machine Learning", "Data Analysis", "Java", "Web Development"],  # Expanded options
    default=["Python"]
)
skill_text = ", ".join(skills) if skills else ""

# Button with progress
if st.button(t["button"]):
    if skill_text:
        with st.spinner(t["success"]):
            time.sleep(1)  # Simulate (remove later)
            try:
                match_response = requests.post("http://127.0.0.1:8000/match_jobs", json={"skill_text": skill_text})
                matches = match_response.json()
                if matches:
                    st.success(t["success"])
                    with st.expander(t["matches_header"]):
                        for match in matches:
                            st.markdown(f"**{match['job_title']}** (Similarity: {match['similarity']:.2f})", unsafe_allow_html=True)
                            st.markdown(f"<div class='stText'>{match['description']}</div>", unsafe_allow_html=True)
                else:
                    st.warning(t["no_matches"])

                narrative_response = requests.post("http://127.0.0.1:8000/generate_narrative", json={"skill_text": skill_text})
                narrative = narrative_response.json()["narrative"]
                with st.expander(t["story_header"]):
                    st.markdown(f"<div class='stText'>{narrative}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(t["error"].format(error=str(e)))
    else:
        st.warning(t["enter_skills"])

# PWA (unchanged)
st.markdown("""
<link rel="manifest" href="/manifest.json">
<script>
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js')
      .then(() => console.log('Service Worker registered'))
      .catch(err => console.log('Service Worker error:', err));
  }
</script>
""", unsafe_allow_html=True)

